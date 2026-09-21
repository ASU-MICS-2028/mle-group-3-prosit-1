# Claims Table — Evidence & Source Tracing

Every claim made in the presentation deck, technical reports, and oral defense brief is directly traceable to an executable notebook cell, data source, or peer-reviewed literature reference.

| Claim ID | Claim / Statistic | Source Dataset | Notebook & Cell | Verification Status |
|---|---|---|---|---|
| **C-01** | Unweighted net ownership (70.96%) overstates weighted net ownership (66.77%) by **4.19 percentage points** due to survey design effects | `ghana_mis_sample.csv` | `01_eda.ipynb` [Cell eda_cd05] | **Verified** |
| **C-02** | District positive counts exhibit severe over-dispersion (**Variance/Mean = 77,183**; Poisson requires 1.0) | `ghana_district_cases.csv` | `02_distributions.ipynb` [Cell cd09 / §A1] | **Verified** |
| **C-02b** | Over-dispersion survives log-population adjustment (Poisson GLM Pearson **$\chi^2/\text{df} = 54,147$**) | `ghana_district_cases.csv` | `02_distributions.ipynb` [Cell cd25 / §A3.2] | **Verified** |
| **C-02c** | Negative Binomial outperforms Poisson by **2,393,669 AIC** for one additional dispersion parameter ($\alpha = 0.2677$) | `ghana_district_cases.csv` | `02_distributions.ipynb` [Cell cd26 / §A3.2] | **Verified** |
| **C-03** | Two-stage cluster bootstrap CI for rural Northern Region net ownership is **$2.12\times$ wider** than naive household bootstrap ($15.20\text{ pp}$ vs $7.17\text{ pp}$), yielding $\text{DEFF} \approx 4.50$ | `ghana_mis_sample.csv` | `02_distributions.ipynb` [Cell cd34 / §A4] | **Verified** |
| **C-04** | Proposed equitable allocation shifts 50,000 nets based on upper-bound epidemic risk and unmet coverage gap: high-population/unmet-need centers gain significantly (**Tamale $+1,692$**, **Sagnarigu $+1,012$**, **East Gonja $+878$**), while urban referral hubs are scaled down (**Wa $-1,516$**, **Bolgatanga $-665$**) to eliminate referral hospital bias | `ghana_district_cases.csv` | `04_allocation.ipynb` [Cell alloc_cd03, `models.compute_allocation`] | **Verified** |
| **C-05** | Preprocessing data leakage deflates test set RMSE by 212 cases ($87,144$ vs $87,356$); target encoding produces fraudulent $R^2 = 1.0000$ (vs honest $0.4905$); naive random split produces an overoptimistic **$45.5\%$ error deflation** ($47,646$ vs $87,356$) due to spatial autocorrelation | `ghana_district_cases.csv` | `03_pipeline_leakage.ipynb` & `reports/leakage_audit.md` | **Verified** |
