"""Count-data regression models: Poisson and Negative Binomial.

Poisson is fitted to demonstrate failure under over-dispersion.
Negative Binomial serves as the core allocation baseline.
"""

from typing import Any, Dict
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd


def fit_poisson(formula: str, data: pd.DataFrame) -> Any:
    """Fit a Poisson GLM to evaluate model fit and over-dispersion.

    Returns the fitted statsmodels GLMResults instance.
    """
    model = smf.glm(formula=formula, data=data, family=sm.families.Poisson())
    return model.fit()


def fit_negative_binomial(formula: str, data: pd.DataFrame) -> Any:
    """Fit a Negative Binomial regression to model over-dispersed count data.

    Returns the fitted statsmodels GLMResults instance.
    """
    model = smf.glm(formula=formula, data=data, family=sm.families.NegativeBinomial())
    return model.fit()


def check_dispersion(poisson_results: Any) -> Dict[str, float]:
    """Calculate Pearson chi-squared dispersion ratio to assess over-dispersion.

    Returns a dictionary with pearson_chi2, df_resid, and dispersion_ratio.
    """
    pearson_chi2 = poisson_results.pearson_chi2
    df_resid = poisson_results.df_resid
    ratio = pearson_chi2 / df_resid if df_resid > 0 else float("nan")
    return {
        "pearson_chi2": float(pearson_chi2),
        "df_resid": float(df_resid),
        "dispersion_ratio": float(ratio),
    }
