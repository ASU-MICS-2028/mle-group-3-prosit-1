# Leakage Audit — Pipeline Integrity Verification

## Overview
This audit systematically checks data preprocessing and model evaluation for data leakage, comparing the disciplined pipeline against intentional leaky baselines.

## Checklist of Leakage Vectors Evaluated

| Vector | Disciplined Pipeline | Leaky Pipeline (Counter-example) | Verdict |
|---|---|---|---|
| **Split Timing** | Split first, fit preprocessors only on train data | Preprocessors fit on entire dataset before split | Verified Clean |
| **Spatial Autocorrelation** | Stratified by region (`region` / `hv024`) | Unstratified random row split leaking geography | Verified Clean |
| **Feature Construction** | Domain-informed features without target dependency | Target encoding with test set outcomes | Verified Clean |
| **Temporal Alignment** | Explicitly noted 2014-17 vs 2022 temporal gap | Ignored time gap between routine and survey data | Documented Caveat |

## Audit Methodology
- Code review of `src/io.py` and `src/features.py`.
- Validation tests in `notebooks/03_pipeline_leakage.ipynb`.
