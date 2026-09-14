# Claims Table — Evidence & Source Tracing

Every claim made in the presentation deck and advisory brief must be directly traceable to a notebook cell, data source, or published reference.

| Claim ID | Claim / Statistic | Source Dataset | Notebook & Cell | Verification Status |
|---|---|---|---|---|
| C-01 | Unweighted net ownership differs from weighted net ownership by X% due to survey design effect | `ghana_mis_sample.csv` | `01_eda.ipynb` [Cell TBD] | Pending |
| C-02 | Over-dispersion in district cases (Variance/Mean > 1), rejecting Poisson model | `ghana_district_cases.csv` | `02_distributions.ipynb` [Cell TBD] | Pending |
| C-03 | Cluster bootstrap intervals are wider than naive i.i.d. household bootstrap intervals | `ghana_mis_sample.csv` | `02_distributions.ipynb` [Cell TBD] | Pending |
| C-04 | Proposed ITN allocation prioritizes high-uncertainty under-sampled districts | `ghana_district_cases.csv` | `04_allocation.ipynb` [Cell TBD] | Pending |
