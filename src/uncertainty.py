"""Bootstrap confidence intervals for survey-derived quantities.

The survey is a two-stage cluster sample, so the cluster bootstrap is the
default. `naive_bootstrap_ci` is the wrong interval for this design and exists
only as the A4 counter-example.
"""

from typing import Callable, Dict, Tuple

import numpy as np
import pandas as pd

RANDOM_SEED = 42


def weighted_proportion(
    df: pd.DataFrame, value_col: str, weight_col: str = "sample_weight"
) -> float:
    """Survey-weighted mean of a 0/1 column, as a percentage."""
    w = df[weight_col].to_numpy(dtype=float)
    v = df[value_col].to_numpy(dtype=float)
    if w.sum() == 0:
        return float("nan")
    return float(np.average(v, weights=w) * 100.0)


def unweighted_proportion(df: pd.DataFrame, value_col: str) -> float:
    """Plain sample mean of a 0/1 column, as a percentage."""
    return float(df[value_col].astype(float).mean() * 100.0)


def cluster_bootstrap_ci(
    df: pd.DataFrame,
    statistic_fn: Callable[[pd.DataFrame], float],
    cluster_col: str = "cluster",
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = RANDOM_SEED,
) -> Tuple[float, float, float]:
    """Two-stage cluster bootstrap: resample clusters, then households within them.

    Stage 1 is what propagates between-cluster variation. Returns
    (point_estimate, ci_lower, ci_upper); the point estimate uses the original
    data, not the bootstrap mean.
    """
    rng = np.random.default_rng(random_seed)
    point_estimate = float(statistic_fn(df))

    positions = {
        c: np.flatnonzero((df[cluster_col] == c).to_numpy())
        for c in df[cluster_col].unique()
    }
    clusters = np.array(list(positions.keys()))

    estimates = []
    for _ in range(n_bootstraps):
        drawn = rng.choice(clusters, size=clusters.size, replace=True)
        idx = np.concatenate(
            [
                rng.choice(positions[c], size=positions[c].size, replace=True)
                for c in drawn
            ]
        )
        estimates.append(statistic_fn(df.take(idx)))

    return (point_estimate, *_percentile_ci(estimates, confidence_level))


def naive_bootstrap_ci(
    df: pd.DataFrame,
    statistic_fn: Callable[[pd.DataFrame], float],
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = RANDOM_SEED,
) -> Tuple[float, float, float]:
    """Household-level bootstrap ignoring the cluster design.

    Wrong for this data: treating households as independent assumes more
    information than the survey bought, giving an interval that is too narrow.
    Kept as the counter-example.
    """
    rng = np.random.default_rng(random_seed)
    point_estimate = float(statistic_fn(df))
    n = len(df)
    estimates = [
        statistic_fn(df.take(rng.integers(0, n, size=n))) for _ in range(n_bootstraps)
    ]
    return (point_estimate, *_percentile_ci(estimates, confidence_level))


def _percentile_ci(estimates, confidence_level: float) -> Tuple[float, float]:
    """Percentile-method interval from bootstrap replicates."""
    alpha = 1.0 - confidence_level
    return (
        float(np.percentile(estimates, 100 * (alpha / 2.0))),
        float(np.percentile(estimates, 100 * (1.0 - alpha / 2.0))),
    )


def design_effect(
    naive_ci: Tuple[float, float, float], cluster_ci: Tuple[float, float, float]
) -> float:
    """Approximate DEFF from two interval widths.

    DEFF is a variance ratio and width tracks the standard error, so the width
    ratio is squared. DEFF = 2 means the sample carries the information of a
    simple random sample half its size.
    """
    naive_width = naive_ci[2] - naive_ci[1]
    cluster_width = cluster_ci[2] - cluster_ci[1]
    if naive_width <= 0:
        return float("nan")
    return (cluster_width / naive_width) ** 2


def compare_bootstraps(
    df: pd.DataFrame,
    statistic_fn: Callable[[pd.DataFrame], float],
    label: str,
    cluster_col: str = "cluster",
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Run both bootstraps on one statistic. DEFF is in `.attrs['design_effect']`."""
    naive = naive_bootstrap_ci(
        df, statistic_fn, n_bootstraps, confidence_level, random_seed
    )
    clust = cluster_bootstrap_ci(
        df, statistic_fn, cluster_col, n_bootstraps, confidence_level, random_seed
    )

    rows = [
        {
            "domain": label,
            "method": method,
            "estimate": est,
            "ci_low": lo,
            "ci_high": hi,
            "ci_width": hi - lo,
        }
        for method, (est, lo, hi) in (
            ("Naive (household i.i.d.)", naive),
            ("Cluster (two-stage)", clust),
        )
    ]
    out = pd.DataFrame(rows)
    out.attrs["design_effect"] = design_effect(naive, clust)
    return out


def summarise_sample_size(
    df: pd.DataFrame, cluster_col: str = "cluster"
) -> Dict[str, int]:
    """Households and distinct clusters behind an estimate."""
    return {
        "n_households": int(len(df)),
        "n_clusters": int(df[cluster_col].nunique()),
    }
