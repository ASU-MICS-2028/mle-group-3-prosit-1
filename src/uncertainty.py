"""Uncertainty quantification via two-stage cluster bootstrap.

Resamples clusters with replacement, then households within clusters,
reflecting the complex survey design of the DHS sample.
"""

from typing import Callable, Tuple
import numpy as np
import pandas as pd

RANDOM_SEED = 42


def cluster_bootstrap_ci(
    df: pd.DataFrame,
    statistic_fn: Callable[[pd.DataFrame], float],
    cluster_col: str = "cluster",
    n_bootstraps: int = 1000,
    confidence_level: float = 0.95,
    random_seed: int = RANDOM_SEED,
) -> Tuple[float, float, float]:
    """Calculate point estimate and confidence interval using cluster bootstrap.

    Returns (point_estimate, ci_lower, ci_upper).
    """
    rng = np.random.default_rng(random_seed)
    clusters = df[cluster_col].unique()
    n_clusters = len(clusters)

    # Calculate point estimate on original data
    point_estimate = float(statistic_fn(df))

    # Pre-group households by cluster for efficient sampling
    cluster_groups = {c: group for c, group in df.groupby(cluster_col)}

    bootstrap_estimates = []
    for _ in range(n_bootstraps):
        # Stage 1: Resample clusters with replacement
        sampled_clusters = rng.choice(clusters, size=n_clusters, replace=True)

        # Stage 2: Sample households within selected clusters with replacement
        sample_chunks = []
        for c in sampled_clusters:
            cluster_df = cluster_groups[c]
            hh_sample = cluster_df.sample(
                n=len(cluster_df), replace=True, random_state=int(rng.integers(1e9))
            )
            sample_chunks.append(hh_sample)

        boot_sample = pd.concat(sample_chunks, ignore_index=True)
        bootstrap_estimates.append(statistic_fn(boot_sample))

    alpha = 1.0 - confidence_level
    ci_lower = float(np.percentile(bootstrap_estimates, 100 * (alpha / 2.0)))
    ci_upper = float(np.percentile(bootstrap_estimates, 100 * (1.0 - alpha / 2.0)))

    return point_estimate, ci_lower, ci_upper
