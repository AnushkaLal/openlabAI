import pandas as pd


def audit_dataset(df: pd.DataFrame) -> dict:
    rows, cols = df.shape

    column_details = {}
    for col in df.columns:
        series = df[col]
        unique_count = int(series.nunique(dropna=True))

        detail = {
            "dtype": str(series.dtype),
            "missing": int(series.isna().sum()),
            "unique_values": unique_count,
            "missing_percent": round(
                float(series.isna().mean() * 100), 2
            ),
        }

        if unique_count == 1:
            detail["constant_column"] = True

        if (
            (series.dtype == "object" or
             isinstance(series.dtype, pd.CategoricalDtype))
            and (unique_count > 50 or
                 (rows > 0 and unique_count / rows > 0.30))
        ):
            detail["high_cardinality"] = True

        if pd.api.types.is_numeric_dtype(series):
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1

            if pd.notna(iqr) and iqr > 0:
                outliers = (
                    (series < q1 - 1.5 * iqr) |
                    (series > q3 + 1.5 * iqr)
                )
                detail["possible_outliers"] = int(outliers.sum())
            else:
                detail["possible_outliers"] = 0

        column_details[str(col)] = detail

    return {
        "rows": int(rows),
        "columns": int(cols),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns_detail": column_details,
    }
