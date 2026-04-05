# gt-summary

One-call styled summary statistics tables for pandas DataFrames, powered by [Great Tables](https://posit-dev.github.io/great-tables/).

```python
from gt_summary import summarize

summarize(df, group_by="species", title="Penguins by Species")
```

## Why

`pandas.describe()` returns a raw DataFrame. `gt-summary` returns a publication-ready [GT](https://posit-dev.github.io/great-tables/) table — formatted numbers, group headers, distribution sparklines, and a grand summary row — in a single call.

## Installation

```bash
pip install gt-summary
```

## Usage

### Ungrouped summary

```python
import pandas as pd
from gt_summary import summarize

summarize(df, title="Dataset Summary")
```

Produces a table with stats as rows (Mean, Std Dev, Min, Median, Max, Missing %) and your numeric columns as columns.

### Grouped summary

```python
summarize(
    df,
    group_by="species",
    columns=["bill_length_mm", "flipper_length_mm", "body_mass_g"],
    sparkline_col="bill_length_mm",
    title="Penguins by Species",
    subtitle="Mean values per group"
)
```

Produces one row per group with mean values, inline distribution sparklines, and an overall mean grand summary row.

### Custom labels

`summarize()` returns a `GT` object — chain any Great Tables method directly:

```python
summarize(df, group_by="species").cols_label(
    bill_length_mm="Bill Length",
    body_mass_g="Body Mass"
)
```
![Example](docs/example.png)

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `df` | `pd.DataFrame` | required | Input DataFrame |
| `group_by` | `str \| None` | `None` | Column to group by |
| `columns` | `list[str] \| None` | `None` | Numeric columns to include. Auto-detected if None |
| `sparklines` | `bool` | `True` | Show distribution sparkline column |
| `sparkline_col` | `str \| None` | `None` | Column to use for sparkline. Defaults to first numeric column |
| `title` | `str` | `"Summary Statistics"` | Table title |
| `subtitle` | `str \| None` | `None` | Optional subtitle |

## Requirements

- Python ≥ 3.10
- pandas ≥ 1.5
- great_tables ≥ 0.5

## License

MIT