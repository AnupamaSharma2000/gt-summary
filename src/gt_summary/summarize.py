from __future__ import annotations

import pandas as pd
from great_tables import GT

from gt_summary._stats import _compute_stats, _compute_grouped_stats
from gt_summary._spark import _build_sparkline_col


def summarize(
    df: pd.DataFrame,
    group_by: str | None = None,
    columns: list[str] | None = None,
    sparklines: bool = True,
    sparkline_col: str | None = None,
    title: str = "Summary Statistics",
    subtitle: str | None = None,
) -> GT:
    """Return a styled Great Tables summary of a pandas DataFrame.

    Parameters
    ----------
    df:
        Input DataFrame. Non-numeric columns are ignored unless used as group_by.
    group_by:
        Column name to group by. Each group becomes one row showing its mean.
        If None, shows mean/std/min/median/max/missing% across all rows.
    columns:
        Explicit list of numeric columns to include. Auto-detected if None.
    sparklines:
        Whether to include a distribution sparkline column. Default True.
    sparkline_col:
        Which numeric column to use for the sparkline. Defaults to the first
        numeric column if not specified.
    title:
        Table title passed to tab_header().
    subtitle:
        Optional subtitle passed to tab_header(). Omitted if None.
    """
    # STEP 1: validate and detect numeric columns 
    if columns is not None:
        missing = [c for c in columns if c not in df.columns]
        if missing:
            raise ValueError(f"Columns not found in DataFrame: {missing}")
        numeric_cols = [
            c for c in columns
            if pd.api.types.is_numeric_dtype(df[c])
        ]
    else:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        raise ValueError("No numeric columns found. Nothing to summarize.")

    if group_by is not None and group_by not in df.columns:
        raise ValueError(f"group_by column '{group_by}' not found in DataFrame.")

    # STEP 2: compute stats 
    if group_by is not None:
        stats_df = _compute_grouped_stats(df, group_by, numeric_cols)
    else:
        stats_df = _compute_stats(df, numeric_cols)
        stats_df.insert(0, "stat", stats_df.index)
        stats_df = stats_df.reset_index(drop=True)

    # STEP 3: build and merge sparkline column
    
    spark_col_name = None
    if sparklines and group_by is not None:   # ← add "and group_by is not None"
        s_col = sparkline_col or numeric_cols[0]
        spark_data = _build_sparkline_col(df, s_col, group_by)
        spark_col_name = f"dist_{s_col}"
        stats_df = stats_df.merge(spark_data, on=group_by)

    # STEP 4: construct GT object 
    if group_by is not None:
        table = GT(stats_df, groupname_col=group_by)
    else:
        table = GT(stats_df, rowname_col="stat")

    # STEP 5: header 
    if subtitle is not None:
        table = table.tab_header(title=title, subtitle=subtitle)
    else:
        table = table.tab_header(title=title)

    # STEP 6: format numbers
    table = table.fmt_number(columns=numeric_cols, decimals=2)

    # STEP 7: sparkline 
    if sparklines and spark_col_name is not None:
        table = table.fmt_nanoplot(columns=spark_col_name, plot_type="bar")

    #STEP 7b: auto column labels
    label_map = {col: col.replace("_", " ").title() for col in numeric_cols}
    if sparklines and spark_col_name is not None:
        source = spark_col_name.replace("dist_", "")
        label_map[spark_col_name] = source.replace("_", " ").title() + " Dist."
    table = table.cols_label(**label_map)

    # STEP 8: grand summary (grouped case only) 
    if group_by is not None:
        table = table.grand_summary_rows(
            fns={"Overall Mean": lambda x: x.mean(numeric_only=True).round(2)}
        )

    # STEP 9: missing value note 
    missing_cols = [c for c in numeric_cols if df[c].isna().any()]
    if missing_cols:
        note = f"Missing values detected in: {', '.join(missing_cols)}"
        table = table.tab_source_note(note)

    return table