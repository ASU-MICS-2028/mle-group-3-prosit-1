"""Count-data models: Poisson and Negative Binomial.

Poisson is fitted to demonstrate its failure under over-dispersion; the
Negative Binomial is the working model.
"""

from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def moment_summary(y: pd.Series) -> Dict[str, float]:
    """Mean, variance and variance/mean ratio. Poisson requires the ratio to be 1."""
    y = pd.Series(y).dropna()
    mean = float(y.mean())
    var = float(y.var(ddof=1))
    return {
        "n": int(y.size),
        "mean": mean,
        "variance": var,
        "variance_mean_ratio": var / mean if mean > 0 else float("nan"),
        "min": float(y.min()),
        "max": float(y.max()),
    }


def nb_alpha_from_moments(y: pd.Series) -> float:
    """Method-of-moments alpha, from NB2's Var = mu + alpha*mu^2. Poisson is alpha=0."""
    m = moment_summary(y)
    if m["mean"] <= 0:
        return float("nan")
    return (m["variance"] - m["mean"]) / (m["mean"] ** 2)


def poisson_pmf_expected(
    y: pd.Series, bin_edges: np.ndarray, lam: Optional[float] = None
) -> np.ndarray:
    """Expected observations per histogram bin under Poisson(lam).

    Integrates the pmf over each bin via the CDF, so the overlay stays
    comparable when bins are far wider than the pmf's spread.
    """
    from scipy import stats

    y = pd.Series(y).dropna()
    lam = float(y.mean()) if lam is None else float(lam)
    return np.diff(stats.poisson.cdf(bin_edges, lam)) * y.size


def nbinom_pmf_expected(
    y: pd.Series, bin_edges: np.ndarray, alpha: Optional[float] = None
) -> np.ndarray:
    """Expected observations per bin under NB2 with mean(y) and dispersion alpha."""
    from scipy import stats

    y = pd.Series(y).dropna()
    mu = float(y.mean())
    alpha = nb_alpha_from_moments(y) if alpha is None else float(alpha)
    n = 1.0 / alpha
    return np.diff(stats.nbinom.cdf(bin_edges, n, n / (n + mu))) * y.size


def check_design_matrix(formula: str, data: pd.DataFrame) -> pd.DataFrame:
    """Flag constant and collinear design columns before fitting.

    Both make the Hessian singular, which statsmodels reports only as an opaque
    LinAlgError. Returns a per-column report; `.attrs` carries rank,
    n_columns and rank_deficient.
    """
    import patsy

    _, X = patsy.dmatrices(formula, data, return_type="dataframe")
    rank = int(np.linalg.matrix_rank(X.to_numpy()))
    report = pd.DataFrame(
        {
            "n_distinct": X.nunique(),
            "std": X.std(ddof=0).round(6),
            "constant": (X.nunique() == 1) & (X.columns != "Intercept"),
        }
    )
    report.attrs["rank"] = rank
    report.attrs["n_columns"] = int(X.shape[1])
    report.attrs["rank_deficient"] = rank < X.shape[1]
    return report


def fit_poisson(
    formula: str, data: pd.DataFrame, offset: Optional[np.ndarray] = None
) -> Any:
    """Fit a Poisson GLM. Pass offset=np.log(population) to model a rate."""
    return smf.glm(
        formula=formula, data=data, family=sm.families.Poisson(), offset=offset
    ).fit()


def fit_negative_binomial_mle(
    formula: str,
    data: pd.DataFrame,
    offset: Optional[np.ndarray] = None,
    maxiter: int = 500,
) -> Any:
    """Fit NB2, estimating alpha by MLE. Read it off `results.params['alpha']`.

    Uses smf.negativebinomial, not smf.glm(family=NegativeBinomial()), which
    takes alpha as a fixed input defaulting to 1.0. Warm-started from the
    Poisson fit, without which the Hessian fails to invert and the standard
    errors are lost; falls back to Nelder-Mead if Newton still fails.
    """
    poisson_start = fit_poisson(formula, data, offset=offset)
    y = data[formula.split("~")[0].strip()]
    alpha0 = max(nb_alpha_from_moments(y), 1e-3)
    start = np.append(np.asarray(poisson_start.params, dtype=float), alpha0)

    model = smf.negativebinomial(formula=formula, data=data, offset=offset)
    results = model.fit(start_params=start, maxiter=maxiter, disp=0)
    if not results.mle_retvals.get("converged", False):
        results = model.fit(start_params=start, method="nm", maxiter=5000, disp=0)
    return results


def check_dispersion(poisson_results: Any) -> Dict[str, float]:
    """Pearson chi2/df for a fitted Poisson GLM. A correct Poisson gives about 1."""
    pearson_chi2 = float(poisson_results.pearson_chi2)
    df_resid = float(poisson_results.df_resid)
    return {
        "pearson_chi2": pearson_chi2,
        "df_resid": df_resid,
        "dispersion_ratio": pearson_chi2 / df_resid if df_resid > 0 else float("nan"),
    }


def compare_fits(poisson_results: Any, nb_results: Any) -> pd.DataFrame:
    """Log-likelihood, AIC and BIC for both fits. Lower AIC is better.

    AIC/BIC are recomputed from the log-likelihood: statsmodels reports a
    deviance-based BIC for GLM results and a likelihood-based one for the
    discrete NB, so the built-in attributes are not comparable.
    """
    rows = []
    for name, res in (("Poisson", poisson_results), ("Negative Binomial", nb_results)):
        k = len(res.params)
        llf = float(res.llf)
        rows.append(
            {
                "model": name,
                "n_params": k,
                "log_likelihood": llf,
                "AIC": -2 * llf + 2 * k,
                "BIC": -2 * llf + k * np.log(float(res.nobs)),
            }
        )
    return pd.DataFrame(rows).set_index("model")
