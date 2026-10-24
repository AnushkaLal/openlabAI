import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def analyze_dataset(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include="number")
    results = {
        "numeric_columns": list(numeric.columns),
        "descriptive_statistics": {},
        "correlations": [],
    }

    if numeric.empty:
        return results

    desc = numeric.describe().replace(
        [np.inf, -np.inf], np.nan
    )
    results["descriptive_statistics"] = {
        col: {
            key: (None if pd.isna(value) else float(value))
            for key, value in values.items()
        }
        for col, values in desc.to_dict().items()
    }

    # Pearson correlations using pairwise complete observations.
    for i, col_a in enumerate(numeric.columns):
        for col_b in numeric.columns[i + 1:]:
            pair = numeric[[col_a, col_b]].replace(
                [np.inf, -np.inf], np.nan
            ).dropna()

            if len(pair) < 3:
                continue

            a, b = pair[col_a], pair[col_b]

            if a.nunique() < 2 or b.nunique() < 2:
                continue

            r, p = pearsonr(a, b)

            results["correlations"].append({
                "column_a": str(col_a),
                "column_b": str(col_b),
                "pearson_r": round(float(r), 4),
                "p_value": round(float(p), 6),
                "sample_size": int(len(pair)),
            })

    results["correlations"].sort(
        key=lambda item: abs(item["pearson_r"]),
        reverse=True,
    )

    return results
