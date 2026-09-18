"""Count-data models: Poisson and Negative Binomial.

Poisson is fitted to demonstrate its failure under over-dispersion.
Negative Binomial is the working model (see CLAUDE.md, statistical conventions).

Two levels are provided deliberately:

* `moment_summary` / `nb_alpha_from_moments` -- the marginal, no-covariate view.
  Transparent algebra we can defend on a slide without invoking an optimiser.
* `fit_poisson` / `fit_negative_binomial_mle` -- GLMs with covariates and an
  exposure offset, which is how the counts should actually be modelled.
"""

from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def moment_summary(y: pd.Series) -> Dict[str, float]:
    """Mean, variance and the variance-to-mean ratio of a count vector.

    A ratio of 1.0 is the Poisson signature (mean == variance). Anything
    meaningfully above 1.0 is over-dispersion, which is what A1 asks us to look
    for. Uses the sample variance (ddof=1).
    """
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
    """Method-of-moments estimate of the NB dispersion parameter alpha.

    The NB2 variance function is Var = mu + alpha * mu**2, so rearranging on the
    sample moments gives alpha = (Var - mean) / mean**2. Poisson is the alpha=0
    special case. This is the one-line derivation to put on the slide; the MLE
    in `fit_negative_binomial_mle` is the number we actually report.
    """
    m = moment_summary(y)
    if m["mean"] <= 0:
        return float("nan")
    return (m["variance"] - m["mean"]) / (m["mean"] ** 2)


def poisson_pmf_expected(
    y: pd.Series, bin_edges: np.ndarray, lam: Optional[float] = None
) -> np.ndarray:
    """Expected number of observations per histogram bin under Poisson(lam).

    Integrates the pmf over each bin via the CDF rather than evaluating it at bin
    centres, so the overlay is comparable to the observed histogram even when the
    bins are far wider than the pmf's support.
    """
    from scipy import stats

    y = pd.Series(y).dropna()
    lam = float(y.mean()) if lam is None else float(lam)
    cdf = stats.poisson.cdf(bin_edges, lam)
    return np.diff(cdf) * y.size


def nbinom_pmf_expected(
    y: pd.Series, bin_edges: np.ndarray, alpha: Optional[float] = None
) -> np.ndarray:
    """Expected observations per bin under NB2 with mean = mean(y) and dispersion alpha.

    scipy parameterises NB as (n, p); the NB2 mapping is n = 1/alpha and
    p = n / (n + mu).
    """
    from scipy import stats

    y = pd.Series(y).dropna()
    mu = float(y.mean())
    alpha = nb_alpha_from_moments(y) if alpha is None else float(alpha)
    n = 1.0 / alpha
    p = n / (n + mu)
    cdf = stats.nbinom.cdf(bin_edges, n, p)
    return np.diff(cdf) * y.size


def check_design_matrix(formula: str, data: pd.DataFrame) -> pd.DataFrame:
    """Diagnose a model formula before fitting it.

    Two failure modes bit us on this dataset and both produce a *singular*
    Hessian, which statsmodels surfaces only as an opaque LinAlgError:

    * a constant column (zero variance) is collinear with the intercept;
    * two columns that encode the same thing -- here `net_coverage_pct` is a
      region-level value joined onto districts, so it takes one distinct value
      per region and is perfectly collinear with `C(region_code)`.

    Returns one row per design column with its distinct-value count, plus a
    `rank_deficient` flag in `.attrs`. Run this before every fit.
    """
    import patsy

    y, X = patsy.dmatrices(formula, data, return_type="dataframe")
    rank = int(np.linalg.matrix_rank(X.to_numpy()))
    report = pd.DataFrame(
        {
            "n_distinct": X.nunique(),
            "std": X.std(ddof=0).round(6),
            # The intercept is constant by construction; flagging it would be noise.
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
    """Fit a Poisson GLM. Pass `offset=np.log(population)` to model a rate.

    Fitted to demonstrate its failure, not as a candidate model.
    """
    model = smf.glm(
        formula=formula, data=data, family=sm.families.Poisson(), offset=offset
    )
    return model.fit()


def fit_negative_binomial_mle(
    formula: str,
    data: pd.DataFrame,
    offset: Optional[np.ndarray] = None,
    maxiter: int = 500,
) -> Any:
    """Fit an NB2 regression, estimating alpha by maximum likelihood.

    Uses `smf.negativebinomial` rather than `smf.glm(family=NegativeBinomial())`:
    the GLM family takes alpha as a *fixed* input (defaulting to 1.0), so it
    would report a dispersion we never estimated. Here alpha comes out of the
    fit and is readable as `results.params['alpha']`.

    The optimiser is started from the Poisson coefficients plus a
    method-of-moments alpha. Cold-started on counts this large the likelihood is
    flat enough that the default Newton step fails to invert the Hessian, which
    costs us the standard errors; warm-starting fixes it. If Newton still fails
    we fall back to Nelder-Mead, which is slower but does not need the Hessian.
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
    """Pearson chi-squared dispersion ratio for a fitted Poisson GLM.

    Under a correctly specified Poisson, chi2/df is approximately 1. The ratio is
    the covariate-adjusted version of the mean-variance check: it asks whether
    over-dispersion survives after the model has explained what it can.
    """
    pearson_chi2 = float(poisson_results.pearson_chi2)
    df_resid = float(poisson_results.df_resid)
    ratio = pearson_chi2 / df_resid if df_resid > 0 else float("nan")
    return {
        "pearson_chi2": pearson_chi2,
        "df_resid": df_resid,
        "dispersion_ratio": ratio,
    }


def compare_fits(poisson_results: Any, nb_results: Any) -> pd.DataFrame:
    """Side-by-side log-likelihood / AIC / BIC table for the two fits.

    AIC and BIC are recomputed here from the log-likelihood rather than read off
    `results.aic`. statsmodels reports a *deviance-based* BIC for GLM results and
    a likelihood-based one for the discrete NB, so the built-in attributes are on
    different scales and are not comparable across the two objects.

    Parameter counts come from `len(results.params)`, which correctly charges the
    NB for its extra alpha. Lower AIC is better; both models are fitted to the
    same response, so the comparison is valid.
    """
    rows = []
    for name, res in (("Poisson", poisson_results), ("Negative Binomial", nb_results)):
        k = len(res.params)
        llf = float(res.llf)
        nobs = float(res.nobs)
        rows.append(
            {
                "model": name,
                "n_params": k,
                "log_likelihood": llf,
                "AIC": -2 * llf + 2 * k,
                "BIC": -2 * llf + k * np.log(nobs),
            }
        )
    return pd.DataFrame(rows).set_index("model")
