from __future__ import annotations

import pandas as pd


_DEFAULT_STATS = ["mean", "std", "min", "median", "max", "missing_pct"]

_STAT_LABELS = {
    "mean":        "Mean",
    "std":         "Std Dev",
    "min":         "Min",
    "median":      "Median",
    "max":         "Max",
    "missing_pct": "Missing %",
}


def _compute_stats(df: pd.DataFrame, numeric_cols: list[str]) -> pd.DataFrame:
    """Compute summary statistics for the ungrouped case.

    Returns a DataFrame where rows are stats and columns are numeric columns.
    """
    rows = []
    for stat in _DEFAULT_STATS:
        if stat == "mean":
            row = df[numeric_cols].mean()
        elif stat == "std":
            row = df[numeric_cols].std()
        elif stat == "min":
            row = df[numeric_cols].min()
        elif stat == "median":
            row = df[numeric_cols].median()
        elif stat == "max":
            row = df[numeric_cols].max()
        elif stat == "missing_pct":
            row = (df[numeric_cols].isna().mean() * 100).round(1)
        rows.append(row.rename(_STAT_LABELS[stat]))

    return pd.DataFrame(rows)


def _compute_grouped_stats(
    df: pd.DataFrame,
    group_by: str,
    numeric_cols: list[str],
) -> pd.DataFrame:
    """Compute per-group means.

    Returns a DataFrame with one row per group, reset_index() applied.
    """
    return (
        df.groupby(group_by)[numeric_cols]
        .mean()
        .round(2)
        .reset_index()
    )
