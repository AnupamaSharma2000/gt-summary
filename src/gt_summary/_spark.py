from __future__ import annotations

import pandas as pd


def _build_sparkline_col(
    df: pd.DataFrame,
    col: str,
    group_by: str | None,
) -> pd.Series | dict[str, str]:
    """Build space-separated sparkline strings for fmt_nanoplot.

    Ungrouped: returns a single string (all values in the column).
    Grouped: returns a Series mapping group label → sparkline string.
    """
    def _to_spark(values: pd.Series) -> str:
        return " ".join(
            str(round(v, 1)) for v in values.dropna()
        )

    if group_by is None:
        return _to_spark(df[col])

    return (
        df.groupby(group_by)[col]
        .apply(_to_spark)
        .reset_index()
        .rename(columns={col: f"dist_{col}"})
    )