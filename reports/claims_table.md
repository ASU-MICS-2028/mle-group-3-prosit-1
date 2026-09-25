# Claims Table: Evidence and Source Tracing

Every number in the presentation deck and the reports traces to a row here: the claim, the
number, and the notebook cell, script or publication that produces it. Re-verified on
2026-09-24 by re-running all four notebooks from clean kernels.

- *Script* rows come from `scripts/verify_claims.py`, an independent re-computation that prints
  aggregates only (run it from the repo root).
- *External* rows come from published sources. E-01 to E-03 were checked against the text of
  the downloaded sources on 2026-09-24, and E-04 and E-05 against the papers on 2026-09-25. The
  deck's References slide lists every source.
- Numbers retired as wrong or unreproducible are listed in `reports/LEARNING_JOURNAL.md`,
  section 4.

| ID | Claim | Number | Source | Status |
|---|---|---|---|---|
| C-01 | Unweighted net ownership overstates the weighted figure, because the survey samples some areas more heavily than others (unequal selection probabilities) | 70.96% vs 66.77% (4.19 points) | `01_eda.ipynb` eda_cd05 | Verified |
| C-02 | District positive counts are over-dispersed | Variance/mean 77,183 | `02_distributions.ipynb` cd09 | Verified |
| C-02a | A Poisson is far too narrow for these counts | SD 442 vs 122,882 (278 times) | `02_distributions.ipynb` cd15 | Verified |
| C-02b | Over-dispersion survives a log-population offset | Pearson χ²/df 54,147 | `02_distributions.ipynb` cd25 | Verified |
| C-02c | The negative binomial fits far better | α = 0.2677; AIC gap 2,393,669 | `02_distributions.ipynb` cd25, cd26 | Verified |
| C-03 | The cluster bootstrap interval for rural Northern net ownership is wider than a naive household bootstrap | 15.20 vs 7.17 points (2.12 times); design effect 4.50 at seed 42 | `02_distributions.ipynb` cd33, cd34 | Verified |
| C-03a | The design effect is stable across seeds and matches a design-based formula | 4.46 to 5.39 over 20 seeds; 4.18 by Taylor linearisation | `scripts/verify_claims.py`, section A | Verified (script) |
| C-03b | The survey-weighted Northern estimate reproduces the published DHS figure; this validates the weighting, not the interval | 67.69% vs 67.6% (0.09 points) | `02_distributions.ipynb` cd39 | Verified |
| C-04 | Proposed allocation by region | Northern 24,196; Upper East 18,631; Upper West 7,173 | `04_allocation.ipynb` alloc_cd07 | Verified |
| C-04a | Within a region the rule allocates by population, and the upper confidence bound adds one multiplier per region | 8.5 / 16.0 / 9.2 nets per 1,000 people; multipliers 1.198 / 1.342 / 1.162 | `04_allocation.ipynb` alloc_cd11 | Verified |
| C-04b | The coverage coefficient is positive: higher-coverage regions had more cases | +0.0823 per point (p = 1.7e-07) | `04_allocation.ipynb` alloc_cd11 | Verified |
| C-04c | Largest changes against the case-proportional comparator | Tamale +1,692, Sagnarigu +1,012; Wa -1,516, Bolgatanga -665 | `04_allocation.ipynb` alloc_cd09 | Verified |
| C-04d | Tamale reports the fewest cases per person of all 50 districts and Nabdam the most; Bolgatanga ranks 4th of 13 in its region | 0.37 (Tamale), 7.13 (Nabdam), 4.02 (Bolgatanga) cases per person, 2014-17 | `04_allocation.ipynb` alloc_cd11 | Verified |
| C-04e | The regional split depends on the model | A region-effects model (AIC 1,253.8 vs 1,286.8) moves 7,720 nets; the point estimate moves 1,391 | `04_allocation.ipynb` alloc_cd13 | Verified |
| C-05 | Preprocessing leakage is real in principle but negligible here | 212 cases at seed 42; 44 on average over 500 seeds | `03_pipeline_leakage.ipynb` leak_cd04, leak_cd12 | Verified |
| C-05a | Target encoding produces a fake perfect fit | Test R² 1.00 vs 0.26 | `03_pipeline_leakage.ipynb` leak_cd06 | Verified |
| C-05b | Random and region-stratified splits give the same test error | Medians 91,413 and 90,169 over 500 seeds; random lower in 48% of seeds | `03_pipeline_leakage.ipynb` leak_cd12 | Verified |
| C-05c | Holding out a whole region raises the error about four times | Pooled RMSE 365,128 | `03_pipeline_leakage.ipynb` leak_cd14 | Verified |
| C-06 | Eleven districts coded Northern now lie in Savannah or North East, where 2022 coverage differs; correcting it moves nets | Savannah 79.1%, North East 62.8% (Northern 67.7%); 3,740 nets move | `04_allocation.ipynb` alloc_cd13; `src/io.py` REGION_2019 | Verified |
| C-07 | Northern Region shows signs of under-testing | Median test positivity 65% vs 54% and 57%; 0.27 cases per person per year vs 0.88 and 0.80 | `scripts/verify_claims.py`, section E | Verified (script) |
| C-08 | Intervention status was dropped from the curated district file | IRS in 32 and SMC in 24 of 50 districts, 2014-17 | `scripts/verify_claims.py`, section E (raw workbook) | Verified (script) |
| C-09 | Per-capita case counts are implausibly high for incidence | 39 of 50 districts report more than one confirmed case per resident over 2014-17 | `scripts/verify_claims.py`, section E | Verified (script) |
| C-10 | Most of Ghana has no district surveillance data in our package | 207 of 260 districts | `scripts/verify_claims.py`, map join | Verified (script) |
| E-01 | A regional average can hide local risk: predicted prevalence across Greater Accra's 29 districts (2020 survey, children 6 months to 10 years, rapid tests) against the 2022 DHS regional figure (children 6 to 59 months, microscopy) | 0 to 49% vs 2% | Oppong et al., Malaria Journal, doi:10.1186/s12936-025-05724-9; Ghana DHS 2022 final report (FR387), Table 12.15 | External, checked 2026-09-24 |
| E-02 | Ghana allocates ITNs by population: mass campaigns at about one net per two people, excluding districts with indoor residual spraying | | PMI Ghana Malaria Operational Plan FY2017 | External, checked 2026-09-24 |
| E-03 | Tamale Teaching Hospital is the only tertiary hospital for the three northern regions; regional hospitals are secondary | | https://tth.gov.gh/about; Ghana Service Provision Assessment 2002, chapter 2 | External, checked 2026-09-24 |
| E-04 | Random hold-outs overestimated model performance by up to 28% (F1-score) against spatially blocked validation | | Kattenborn et al. 2022, doi:10.1016/j.ophoto.2022.100018 | External, checked 2026-09-25 |
| E-05 | Random validation overstates the predictive power of spatial models, which spatially blocked validation reveals | | Ploton et al. 2020, Nature Communications 11:4540, doi:10.1038/s41467-020-18321-y | External, checked 2026-09-25 |
