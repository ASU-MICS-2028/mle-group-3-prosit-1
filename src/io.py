"""Data loading, validation, and stratified splitting logic.

All splits must use split_data() to enforce region stratification.
"""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_mis_sample(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load the de-identified Ghana 2022 DHS household survey extract.

    Returns a pandas DataFrame of household records.
    """
    path = (data_dir or DATA_DIR) / "ghana_mis_sample.csv"
    if not path.exists():
        raise FileNotFoundError(f"Household survey dataset not found at: {path}")
    return pd.read_csv(path)


def load_region_malaria(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load the DHS subnational malaria indicators across regions.

    Returns a pandas DataFrame of regional indicators with published CIs.
    """
    path = (data_dir or DATA_DIR) / "ghana_region_malaria.csv"
    if not path.exists():
        raise FileNotFoundError(f"Regional malaria indicators not found at: {path}")
    return pd.read_csv(path)


def load_district_cases(data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load the routine surveillance district cases dataset.

    Returns a pandas DataFrame of northern Ghana district-level counts.
    """
    path = (data_dir or DATA_DIR) / "ghana_district_cases.csv"
    if not path.exists():
        raise FileNotFoundError(f"District cases dataset not found at: {path}")
    return pd.read_csv(path)


def split_data(
    df: pd.DataFrame,
    target_col: Optional[str] = None,
    test_size: float = 0.2,
    stratify_col: str = "region",
    random_seed: int = RANDOM_SEED,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Perform a train/test split stratified by region to avoid spatial leakage.

    Returns (train_df, test_df) or ((X_train, X_test), (y_train, y_test)).
    """
    if stratify_col not in df.columns:
        raise ValueError(
            f"Stratification column '{stratify_col}' missing from data. "
            "Splits must be stratified by region to prevent spatial leakage."
        )

    stratify = df[stratify_col]

    if target_col is not None:
        X = df.drop(columns=[target_col])
        y = df[target_col]
        return train_test_split(
            X, y, test_size=test_size, stratify=stratify, random_state=random_seed
        )

    return train_test_split(
        df, test_size=test_size, stratify=stratify, random_state=random_seed
    )


# ---------------------------------------------------------------------------
# Column contracts
# ---------------------------------------------------------------------------
# Transcribed from data_dictionary.md. These are what the notebooks assume.
# A mismatch is not a crash to work around -- it is a finding to report
# (CLAUDE.md: "a documented discrepancy is a finding we can report").

EXPECTED_COLUMNS = {
    "ghana_mis_sample.csv": [
        "cluster",
        "household",
        "region",
        "residence",
        "sample_weight",
        "wealth_index",
        "has_net",
        "num_nets",
        "children_under_net_last_night",
        "eligible_children",
    ],
    "ghana_district_cases.csv": [
        "district",
        "region_name",
        "region_code",
        "year_start",
        "year_end",
        "months_reported",
        "suspected_cases",
        "tested_cases",
        "positive_cases",
        "mean_population",
        "positive_per_100k",
        "net_coverage_pct",
    ],
    "ghana_region_malaria.csv": [
        "region_name",
        "dhs_region_code",
        "hv024_16region",
        "survey_year",
        "survey_id",
        "rdt_prevalence_pct",
        "rdt_prevalence_pct_ci_low",
        "rdt_prevalence_pct_ci_high",
        "microscopy_prevalence_pct",
        "microscopy_prevalence_pct_ci_low",
        "microscopy_prevalence_pct_ci_high",
        "n_children_tested_rdt_weighted",
        "n_children_tested_rdt_unweighted",
        "net_ownership_pct",
        "net_ownership_pct_ci_low",
        "net_ownership_pct_ci_high",
        "u5_itn_use_pct",
        "u5_itn_use_pct_ci_low",
        "u5_itn_use_pct_ci_high",
        "mean_itns_per_hh",
        "n_households",
    ],
}


def validate_schema(df: pd.DataFrame, dataset: str) -> pd.DataFrame:
    """Check a loaded frame against the data-dictionary column contract.

    Reports columns the dictionary promises but the file lacks, and columns the
    file carries that the dictionary does not describe. Prints nothing about the
    contents of any row -- only names, dtypes and null counts (RULES.md 1).

    Returns a per-column report; `.attrs["missing"]` and `.attrs["undocumented"]`
    hold the two discrepancy lists.
    """
    expected = EXPECTED_COLUMNS.get(dataset)
    if expected is None:
        raise KeyError(f"No column contract defined for '{dataset}'")

    missing = [c for c in expected if c not in df.columns]
    undocumented = [c for c in df.columns if c not in expected]

    report = pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "non_null": df.notna().sum(),
            "n_missing": df.isna().sum(),
            "n_distinct": df.nunique(),
            "in_contract": [c in expected for c in df.columns],
        }
    )
    report.attrs["dataset"] = dataset
    report.attrs["missing"] = missing
    report.attrs["undocumented"] = undocumented
    return report


def schema_summary(report: pd.DataFrame) -> str:
    """One-paragraph verdict from validate_schema, safe to print or paste."""
    missing = report.attrs["missing"]
    undocumented = report.attrs["undocumented"]
    lines = [f"{report.attrs['dataset']}: {len(report)} columns."]
    lines.append(f"  promised but absent : {missing if missing else 'none'}")
    lines.append(
        f"  present but undocumented : {undocumented if undocumented else 'none'}"
    )
    constant = report.index[report["n_distinct"] <= 1].tolist()
    lines.append(
        f"  constant columns (collinear with an intercept) : {constant if constant else 'none'}"
    )
    nulls = report.index[report["n_missing"] > 0].tolist()
    lines.append(f"  columns with missing values : {nulls if nulls else 'none'}")
    return "\n".join(lines)
