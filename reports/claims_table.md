# Claims Table — Evidence & Source Tracing

Every claim made in the presentation deck and advisory brief must be directly traceable to a notebook cell, data source, or published reference.

| Claim ID | Claim / Statistic | Source Dataset | Notebook & Cell | Verification Status |
|---|---|---|---|---|
| C-01 | Unweighted net ownership differs from weighted net ownership by X% due to survey design effect | `ghana_mis_sample.csv` | `01_eda.ipynb` [Cell TBD] | Pending (Theme B1) |
| C-02 | District positive counts are over-dispersed (variance/mean = 77,183, Poisson requires 1.0) | `ghana_district_cases.csv` | `02_distributions.ipynb` [Cell cd09 / §A1] | Verified |
| C-02b | Over-dispersion survives population adjustment (Poisson GLM Pearson χ²/df = 54,147 with log-population offset) | `ghana_district_cases.csv` | `02_distributions.ipynb` [Cell cd25 / §A3.2] | Verified |
| C-02c | Negative Binomial beats Poisson by 2,393,669 AIC for one extra dispersion parameter (α = 0.2677) | `ghana_district_cases.csv` | `02_distributions.ipynb` [Cell cd26 / §A3.2] | Verified |
| C-03 | Cluster bootstrap CI is 2.12x wider than naive household bootstrap (DEFF ≈ 4.50) for rural Northern Region net ownership | `ghana_mis_sample.csv` | `02_distributions.ipynb` [Cell cd34 / §A4] | Verified |
| C-04 | Proposed ITN allocation prioritizes high-uncertainty under-sampled districts | `ghana_district_cases.csv` | `04_allocation.ipynb` [Cell TBD] | Pending (Theme C) |
