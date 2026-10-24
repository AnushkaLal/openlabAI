
import argparse
import json
import sys
import traceback
from pathlib import Path

import pandas as pd

from openlab.agents.auditor import run_auditor
from openlab.agents.scientist import run_scientist
from openlab.agents.analyst import run_analyst
from openlab.agents.reviewer import run_reviewer
from openlab.reporting.report import build_report
from openlab.tools.data_audit import audit_dataset
from openlab.tools.statistics import analyze_dataset
from openlab.tools.visualization import create_plots


def save_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, indent=2, allow_nan=False),
        encoding="utf-8",
    )


def call_agent(name, function, *args, errors):
    """Run an agent and record any failure."""
    print(f"  -> {name}", flush=True)

    try:
        result = function(*args)

        if not isinstance(result, str) or not result.strip():
            raise ValueError("Agent returned an empty response.")

        return result

    except Exception as exc:
        message = f"{name}: {type(exc).__name__}: {exc}"
        errors.append(message)

        print(f"  ERROR: {message}", file=sys.stderr, flush=True)

        return (
            f"AGENT FAILED: {name}. "
            "No valid response was produced. "
            "See the Execution errors section."
        )


def investigate(
    csv_path: str,
    question: str,
    output_dir: str,
) -> None:
    source = Path(csv_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Generate filenames from the input dataset name.
    dataset_name = source.stem.lower().replace(" ", "_")

    report_path = out / f"report_{dataset_name}.md"
    audit_path = out / f"audit_{dataset_name}.json"
    analysis_path = out / f"analysis_{dataset_name}.json"
    errors_path = out / f"errors_{dataset_name}.json"
    plots_dir = out / f"plots_{dataset_name}"

    errors = []

    try:
        # Validate and load the dataset.
        if not source.is_file():
            raise FileNotFoundError(
                f"Dataset not found: {source}"
            )

        df = pd.read_csv(source)

        if df.empty:
            raise ValueError("The CSV contains no data rows.")

        if len(df.columns) == 0:
            raise ValueError("The CSV contains no columns.")

        if not df.columns.is_unique:
            raise ValueError(
                "The CSV contains duplicate column names."
            )

        print(f"\nOpenLab AI | Dataset: {source}")
        print(
            f"Loaded {len(df)} rows and "
            f"{len(df.columns)} columns.\n"
        )

        # Step 1: Deterministic data audit + Auditor agent.
        print("[1/4] Data Auditor: measuring data quality...")

        audit = audit_dataset(df)
        save_json(audit_path, audit)

        audit_notes = call_agent(
            "Data Auditor",
            run_auditor,
            audit,
            question,
            errors=errors,
        )

        # Step 2: Research plan.
        print("[2/4] Research Scientist: developing analysis plan...")

        research_plan = call_agent(
            "Research Scientist",
            run_scientist,
            audit,
            question,
            errors=errors,
        )

        # Step 3: Deterministic statistics and plots.
        print(
            "[3/4] Analysis Engineer: computing statistics and plots..."
        )

        analysis = analyze_dataset(df)
        save_json(analysis_path, analysis)

        plots = create_plots(df, str(plots_dir))

        interpretation = call_agent(
            "Analysis Engineer",
            run_analyst,
            question,
            analysis,
            errors=errors,
        )

        # Step 4: Peer review.
        print("[4/4] Peer Reviewer: checking the interpretation...")

        review = call_agent(
            "Peer Reviewer",
            run_reviewer,
            question,
            audit,
            analysis,
            interpretation,
            errors=errors,
        )

        # Build the final report.
        report = build_report(
            question=question,
            audit=audit,
            audit_notes=audit_notes,
            research_plan=research_plan,
            analysis=analysis,
            interpretation=interpretation,
            review=review,
            plots=plots,
        )

        # Clearly disclose incomplete agent execution.
        report += "\n\n## Execution errors\n\n"

        if errors:
            report += (
                "One or more agent calls failed. "
                "This report may be incomplete and should be "
                "reviewed before its findings are used.\n\n"
            )
            report += "\n".join(
                f"- `{error}`" for error in errors
            )
        else:
            report += "No agent execution errors were recorded.\n"

        report_path.write_text(report, encoding="utf-8")
        save_json(errors_path, {"errors": errors})

        print("\nInvestigation finished.")
        print(f"Report:  {report_path}")
        print(f"Audit:   {audit_path}")
        print(f"Results: {analysis_path}")
        print(f"Errors:  {errors_path}")
        print(f"Plots:   {plots_dir}")

        if errors:
            print("\nRun status: COMPLETED WITH ERRORS")
        else:
            print("\nRun status: SUCCESS")

        print("\n--- PEER REVIEW ---\n")
        print(review)

    except Exception as exc:
        # Record critical failures, such as invalid CSVs or
        # failures during statistical analysis or plot generation.
        message = f"{type(exc).__name__}: {exc}"

        print(
            f"\nFATAL ERROR: {message}",
            file=sys.stderr,
        )

        try:
            save_json(
                errors_path,
                {
                    "fatal_error": message,
                    "agent_errors": errors,
                    "traceback": traceback.format_exc(),
                },
            )

            # Preserve an existing report if this run failed
            # before generating a new report.
            if not report_path.exists():
                report_path.write_text(
                    "# OpenLab AI — Investigation Failed\n\n"
                    f"Dataset: `{source}`\n\n"
                    f"Research question: {question}\n\n"
                    f"## Fatal error\n\n`{message}`\n",
                    encoding="utf-8",
                )

        except OSError as write_error:
            print(
                f"Could not save error details: {write_error}",
                file=sys.stderr,
            )

        raise


def main():
    parser = argparse.ArgumentParser(
        description="OpenLab AI: an open-source agentic data science team"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    investigate_parser = subparsers.add_parser(
        "investigate",
        help="Investigate a CSV dataset",
    )

    investigate_parser.add_argument(
        "csv",
        help="Path to the CSV file",
    )

    investigate_parser.add_argument(
        "--question",
        required=True,
        help="Scientific research question",
    )

    investigate_parser.add_argument(
        "--output",
        default="outputs",
        help="Output directory",
    )

    args = parser.parse_args()

    try:
        if args.command == "investigate":
            investigate(
                args.csv,
                args.question,
                args.output,
            )

    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
