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
