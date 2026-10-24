import argparse
import json
import sys
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


def investigate(csv_path: str, question: str, output_dir: str) -> None:
    source = Path(csv_path)
    out = Path(output_dir)
    plots_dir = out / "plots"

    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")

    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(source)

    if df.empty:
        raise ValueError("The CSV contains no data rows.")
    if len(df.columns) == 0:
        raise ValueError("The CSV contains no columns.")

    print(f"\nOpenLab AI | Dataset: {source}")
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.\n")

    print("[1/4] Data Auditor: measuring data quality...")
    audit = audit_dataset(df)
    save_json(out / "audit.json", audit)
    audit_notes = run_auditor(audit, question)

    print("[2/4] Research Scientist: developing analysis plan...")
    research_plan = run_scientist(audit, question)

    print("[3/4] Analysis Engineer: computing statistics and plots...")
    analysis = analyze_dataset(df)
    save_json(out / "analysis.json", analysis)
    plots = create_plots(df, str(plots_dir))

    interpretation = run_analyst(question, analysis)

    print("[4/4] Peer Reviewer: checking the interpretation...")
    review = run_reviewer(
        question, audit, analysis, interpretation
    )

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

    (out / "report.md").write_text(report, encoding="utf-8")

    print("\nInvestigation finished.")
    print(f"Report:  {out / 'report.md'}")
    print(f"Audit:   {out / 'audit.json'}")
    print(f"Results: {out / 'analysis.json'}")
    print(f"Plots:   {plots_dir}")
    print("\n--- PEER REVIEW ---\n")
    print(review)


def main():
    parser = argparse.ArgumentParser(
        description="OpenLab AI: an open-source agentic data science team"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    investigate_parser = subparsers.add_parser(
        "investigate", help="Investigate a CSV dataset"
    )
    investigate_parser.add_argument("csv", help="Path to the CSV file")
    investigate_parser.add_argument(
        "--question", required=True, help="Scientific research question"
    )
    investigate_parser.add_argument(
        "--output", default="outputs", help="Output directory"
    )

    args = parser.parse_args()

    try:
        if args.command == "investigate":
            investigate(args.csv, args.question, args.output)
    except Exception as exc:
        print(f"\nOpenLab error: {exc}", file=sys.stderr)
        print(
            "Check the CSV path, Python dependencies, and Ollama status.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
