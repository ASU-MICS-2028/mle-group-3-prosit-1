"""Uncertainty quantification by bootstrap.

The survey is a two-stage cluster sample, so the cluster bootstrap is the
default here (CLAUDE.md: "if we ask for a bootstrap, assume cluster"). The naive
household bootstrap is provided *only* as the counter-example for A4 -- it is
the wrong interval for this design, and showing how much too narrow it is is the
point of the exercise.
"""

from typing import Callable, Dict, Tuple

import numpy as np
import pandas as pd

RANDOM_SEED = 42


# --------------------------------------------------------------------------
# Statistics to bootstrap
# --------------------------------------------------------------------------


def weighted_proportion(
    df: pd.DataFrame, value_col: str, weight_col: str = "sample_weight"
) -> float:
    """Survey-weighted mean of a 0/1 column, as a percentage.

    DHS households carry unequal selection probabilities, so the unweighted mean
    is an estimate of the *sample*, not of the population. Weighting is what
    makes the number an estimate of Ghana.
    """
    w = df[weight_col].to_numpy(dtype=float)
    v = df[value_col].to_numpy(dtype=float)
    if w.sum() == 0:
        return float("nan")
    return float(np.average(v, weights=w) * 100.0)


def unweighted_proportion(df: pd.DataFrame, value_col: str) -> float:
    """Plain sample mean of a 0/1 column, as a percentage. Kept for the
    weighted-vs-unweighted contrast in the EDA."""
    return float(df[value_col].astype(float).mean() * 100.0)


# --------------------------------------------------------------------------
# Bootstraps
# --------------------------------------------------------------------------


def cluster_bootstrap_ci(
    df: pd.DataFrame,
    statistic_fn: Callable[[pd.DataFrame], float],
    cluster_col: str = "cluster",
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = RANDOM_SEED,
) -> Tuple[float, float, float]:
    """Two-stage cluster bootstrap: resample clusters, then households within them.

    Stage 1 resamples the *primary sampling units* with replacement, which is
    what propagates the between-cluster variation that a household-level
    resample destroys. Stage 2 resamples households inside each drawn cluster.

    Returns (point_estimate, ci_lower, ci_upper). The point estimate is computed
    on the original data, not on the bootstrap mean.
    """
    rng = np.random.default_rng(random_seed)
    point_estimate = float(statistic_fn(df))

    # Positional indices per cluster, so each draw is an integer take() rather
    # than a concat of DataFrames -- same sampling, far cheaper.
    positions = {
        c: np.flatnonzero((df[cluster_col] == c).to_numpy())
        for c in df[cluster_col].unique()
    }
    clusters = np.array(list(positions.keys()))
    n_clusters = clusters.size

    estimates = []
    for _ in range(n_bootstraps):
        drawn = rng.choice(clusters, size=n_clusters, replace=True)
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
    """Household-level bootstrap that ignores the cluster design.

    WRONG for this data -- included as the A4 counter-example. It treats
    households as independent draws, so it does not see that two households in
    the same cluster share a village, a vector environment and a distribution
    campaign. The resulting interval is too narrow.
    """
    rng = np.random.default_rng(random_seed)
    point_estimate = float(statistic_fn(df))
    n = len(df)

    estimates = [
        statistic_fn(df.take(rng.integers(0, n, size=n))) for _ in range(n_bootstraps)
    ]

    return (point_estimate, *_percentile_ci(estimates, confidence_level))


def _percentile_ci(estimates, confidence_level: float) -> Tuple[float, float]:
    """Percentile-method interval from a vector of bootstrap replicates."""
    alpha = 1.0 - confidence_level
    lo = float(np.percentile(estimates, 100 * (alpha / 2.0)))
    hi = float(np.percentile(estimates, 100 * (1.0 - alpha / 2.0)))
    return lo, hi


# --------------------------------------------------------------------------
# Comparison
# --------------------------------------------------------------------------


def design_effect(
    naive_ci: Tuple[float, float, float], cluster_ci: Tuple[float, float, float]
) -> float:
    """Approximate design effect from two interval widths.

    DEFF is a ratio of *variances*, and interval width is proportional to the
    standard error, so the ratio of widths is squared. DEFF = 2 means the cluster
    sample carries the information of a simple random sample half its size.
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
    """Run both bootstraps on the same statistic and tabulate the difference."""
    naive = naive_bootstrap_ci(
        df, statistic_fn, n_bootstraps, confidence_level, random_seed
    )
    clust = cluster_bootstrap_ci(
        df, statistic_fn, cluster_col, n_bootstraps, confidence_level, random_seed
    )

    rows = []
    for method, (est, lo, hi) in (
        ("Naive (household i.i.d.)", naive),
        ("Cluster (two-stage)", clust),
    ):
        rows.append(
            {
                "domain": label,
                "method": method,
                "estimate": est,
                "ci_low": lo,
                "ci_high": hi,
                "ci_width": hi - lo,
            }
        )
    out = pd.DataFrame(rows)
    out.attrs["design_effect"] = design_effect(naive, clust)
    return out


def summarise_sample_size(
    df: pd.DataFrame, cluster_col: str = "cluster"
) -> Dict[str, int]:
    """Households and distinct clusters behind an estimate.

    Reported next to every interval: an interval is only interpretable against
    the number of PSUs that produced it.
    """
    return {"n_households": int(len(df)), "n_clusters": int(df[cluster_col].nunique())}
