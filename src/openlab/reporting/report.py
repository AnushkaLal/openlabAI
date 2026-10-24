from datetime import datetime, timezone


def build_report(
    question: str,
    audit: dict,
    audit_notes: str,
    research_plan: str,
    analysis: dict,
    interpretation: str,
    review: str,
    plots: list[str],
) -> str:
    lines = [
        "# OpenLab AI — Scientific Investigation",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Research question",
        question,
        "",
        "## 1. Dataset audit",
        f"- Rows: {audit['rows']}",
        f"- Columns: {audit['columns']}",
        f"- Duplicate rows: {audit['duplicate_rows']}",
        "",
        "### Column-level measurements",
    ]

    for name, details in audit["columns_detail"].items():
        lines.append(f"- **{name}**: {details}")

    lines += [
        "",
        "### Auditor's interpretation",
        audit_notes,
        "",
        "## 2. Research plan",
        research_plan,
        "",
        "## 3. Computed results",
        "### Descriptive statistics",
        "```json",
    ]

    import json
    lines.append(json.dumps(
        analysis["descriptive_statistics"], indent=2, allow_nan=False
    ))
    lines += [
        "```",
        "",
        "### Strongest Pearson correlations",
    ]

    if analysis["correlations"]:
        for item in analysis["correlations"][:10]:
            lines.append(
                f"- {item['column_a']} vs {item['column_b']}: "
                f"r = {item['pearson_r']}, p = {item['p_value']}, "
                f"n = {item['sample_size']}"
            )
    else:
        lines.append("No valid numeric column pairs were available.")

    lines += [
        "",
        "### Analyst's interpretation",
        interpretation,
        "",
        "## 4. Peer review",
        review,
        "",
        "## 5. Visualizations",
    ]

    if plots:
        lines.extend(f"- `{path}`" for path in plots)
    else:
        lines.append("No plots could be generated for this dataset.")

    lines += [
        "",
        "## 6. Limitations",
        "- Correlation does not establish causation.",
        "- Missingness and data collection methods may bias results.",
        "- Outlier flags require domain-specific investigation.",
        "- AI-generated interpretations require human verification.",
        "- This workflow performs exploratory analysis, not a full "
        "domain-specific scientific validation.",
        "",
    ]

    return "\n".join(lines)
