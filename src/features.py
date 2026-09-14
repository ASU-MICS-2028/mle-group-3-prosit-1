"""Feature engineering and preprocessing pipelines.

Enforces 'split first, fit second' via scikit-learn Pipeline and ColumnTransformer.
"""

from typing import List, Optional
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def build_preprocessor(
    numeric_features: Optional[List[str]] = None,
    categorical_features: Optional[List[str]] = None,
) -> ColumnTransformer:
    """Build a ColumnTransformer pipeline for preprocessing features.

    Returns a fitted or unfitted ColumnTransformer instance.
    """
    transformers = []

    if numeric_features:
        num_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("num", num_pipeline, numeric_features))

    if categorical_features:
        cat_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )
        transformers.append(("cat", cat_pipeline, categorical_features))

    return ColumnTransformer(transformers=transformers)
