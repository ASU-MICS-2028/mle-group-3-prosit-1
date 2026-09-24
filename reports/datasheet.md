# Datasheet for Datasets — Prosit 1 (ITN Allocation in Ghana)

**Academic Course:** ICS553 Machine Learning Essentials · Ashesi University · MICS 2028  
**Advisory Group:** Group 3 Consultancy (Eric Elikplim Sunu, Lead)  
**Deliverable:** Data Provenance, Governance, Sampling Design, and Audit of 9 Known Data Issues

---

## 1. Motivation
- **Purpose:** Inform data-driven, equitable allocation of insecticide-treated nets (ITNs) across Ghana's northern districts under severe resource constraints (50,000 net ceiling).
- **Creators & Custodians:** Curated from open-access sources (WHO Global Health Observatory, DHS subnational indicators, Ghana Health Service routine DHIMS-2 surveillance, geoBoundaries / UN OCHA COD-AB) and a de-identified extract of licensed microdata from the Ghana 2022 Demographic and Health Survey (DHS-VIII).

---

## 2. Dataset Composition & Schemas

### 2.1 Household Microdata (`data/ghana_mis_sample.csv`)
- **Dimensions:** 17,933 households across 618 primary sampling clusters and 16 administrative regions.
- **Key Fields:**
  - `sample_weight`: Normalized DHS sampling weights ($w_i = \text{hv005} / 1,000,000$).
  - `has_net` (hv227): household owns at least one mosquito net of any kind, not only ITNs ($1$ = yes, $0$ = no). Survey-weighted, it agrees with the published ITN ownership figures within 0.3 points in the three northern regions.
  - `num_nets` (hml1): number of mosquito nets the household reports.
  - `residence` (hv025): 'urban' or 'rural'.
  - `region` (hv024): 2022 16-region code (1 to 16).
  - `cluster` (hv001): anonymized primary sampling unit (PSU).

### 2.2 Longitudinal Subnational Indicators (`data/ghana_region_malaria.csv`)
- **Dimensions:** 76 survey-region observations across six DHS/MIS survey rounds (2003, 2008, 2014, 2016, 2019, 2022).
- **Key Fields:** Regional net ownership, under-5 net usage, rapid diagnostic test (RDT) prevalence, microscopy prevalence, and published survey confidence intervals.

### 2.3 District Routine Surveillance (`data/ghana_district_cases.csv`)
- **Dimensions:** 50 administrative districts across 3 northern regions (Northern, Upper East, Upper West).
- **Temporal Span:** Cumulative routine surveillance totals from 2014–2017.
- **Key Fields:**
  - `suspected_cases`, `tested_cases`, `positive_cases`: Routine outpatient clinic aggregates.
  - `mean_population`: Mean annual district population estimate over the 2014–2017 period.
  - `positive_per_100k`: Cumulative positive tests per 100,000 residents.
  - `net_coverage_pct`: Imputed regional household net ownership from the 2022 DHS.

---

## 3. Sampling Design & Survey Methodology

### 3.1 Two-Stage Cluster Sampling
The DHS employs a probabilistic two-stage stratified cluster sampling design:
1. **Stage 1 (PSUs):** Clusters (enumeration areas / census tracts) are selected with probability proportional to population size within rural/urban strata.
2. **Stage 2 (Households):** A fixed number of households (typically 25–30) are systematically sampled within each selected cluster.

### 3.2 Design Effect (DEFF) & Variance Estimation
Observations within the same cluster are positively correlated due to shared spatial ecology, socioeconomic clustering, and local mosquito breeding sites (intra-cluster correlation $\rho > 0$).
- **Methodological Rule:** A simple random sample (SRS) assumption or naive household bootstrap drastically underestimates parameter variance.
- **Implementation:** A **two-stage cluster bootstrap** (resampling clusters with replacement, then households within the drawn clusters; `src/uncertainty.py`). The extract has no strata column, so strata are not used; for a single-stratum domain such as rural Northern Region this makes no difference. A design-based (Taylor linearisation) calculation gives a similar design effect: 4.2 against the bootstrap's 4.5 (`scripts/verify_claims.py`, section A).

---

## 4. Audit of 9 Known Data Issues & Methodological Mitigations

During pipeline execution, exploratory analysis and a full re-verification of the notebooks, our team identified nine data discrepancies against the course brief and standard epidemiological assumptions:

### Issue 1: Missing Parasitaemia & Missing District Identifiers in Household Microdata
- **Finding:** `ghana_mis_sample.csv` contains neither blood parasitaemia test results (RDT/microscopy) nor district-level geographic identifiers. The finest geographic resolution is region (`hv024`) and anonymized cluster.
- **Impact:** We cannot estimate district-level prevalence directly from the household survey microdata.
- **Mitigation:** In Theme A4, we evaluate survey uncertainty on **regional net ownership** rather than district prevalence. Routine surveillance (`ghana_district_cases.csv`) is used for district-level risk modeling.

### Issue 2: Empty Published ITN Confidence Intervals in Official Subnational Data
- **Finding:** In `ghana_region_malaria.csv`, `net_ownership_pct_ci_low/high` and `u5_itn_use_pct_ci_*` are 100% missing (0 of 76 rows populated). Only prevalence CIs are populated (54 of 76).
- **Impact:** We cannot mathematically validate our cluster bootstrap confidence interval against an official published interval.
- **Mitigation:** We validated the survey weighting methodology by proving that our survey-weighted point estimate reproduces the published 2022 DHS regional net ownership to within **$0.09\text{ percentage points}$** ($67.69\%$ vs $67.60\%$). We explicitly document that interval validation remains unclosed due to upstream missing data.

### Issue 3: Regional-Level Resolution & Temporal Asynchrony of Net Coverage
- **Finding:** In `ghana_district_cases.csv`, `net_coverage_pct` is recorded at the regional level, taking identical values for all districts within a given region (Northern $= 67.7\%$, Upper East $= 79.6\%$, Upper West $= 69.8\%$). Additionally, net coverage is measured in **2022**, whereas case counts were recorded in **2014–2017**.
- **Impact:** `net_coverage_pct` is perfectly collinear with a region dummy and cannot enter a regression model alongside region indicators. Furthermore, the causal arrow is reversed (2022 nets cannot retroactively prevent 2014 infections).
- **Mitigation:** Pre-fit design matrix checks (`models.check_design_matrix`) catch and reject simultaneous inclusion of region dummies. We document that the coefficient on `net_coverage_pct` captures a macro-regional effect rather than a causal district-level protective efficacy.

### Issue 4: Zero-Variance Surveillance Columns
- **Finding:** The columns `months_reported` (48), `year_start` (2014), and `year_end` (2017) are completely invariant across all 50 districts.
- **Impact:** They carry zero discriminatory signal and induce exact collinearity with the intercept in regression models.
- **Mitigation:** Excluded from feature pipelines and modeling matrices. Data gap analysis is redirected to geographic discrepancies rather than temporal reporting completeness.

### Issue 5: Missing Geographic Crosswalk File
- **Finding:** `ghana_region_crosswalk.csv` (mapping DHS region codes `hv024` to UN OCHA Common Operational Datasets `adm1_pcode`) was absent from the raw course distribution.
- **Impact:** Breaks automated joining between survey microdata and GIS boundary shapefiles.
- **Mitigation:** Implemented robust regex-based string normalization in `src/viz.py` (`clean_reg` and `norm`) to join boundary polygons dynamically without external dependencies.

### Issue 6: Administrative Boundary Splits & Name Mismatches
- **Finding:** Of the 50 surveillance districts, 43 match the 2021 UN OCHA `adm2_name` boundaries directly. The 7 non-matching districts reflect pre-2018 amalgamated districts that have since been split:
  1. *Garu-Tempane* (split into Garu and Tempane)
  2. *Savelugu-Nanton* (split into Savelugu and Nanton)
  3. *Bunkpurugu-Yunyoo* (split into Bunkpurugu-Nakpanduri and Yunyoo-Nasuan)
  4. *Kasena-Nankana* (Kasena Nankana East)
  5. *Tatale-Sangule* (Tatale Sanguli)
  6. *Sagnarigu* (spelling variant Sagnerigu)
  7. *Gushiegu* (spelling variant Gushegu)
- **Impact:** Direct table joins result in 7 blank polygons on GIS choropleths.
- **Mitigation:** Developed an explicit aliasing and polygon-aggregation mapper in `src/viz.py` (`plot_district_choropleth`): all 50 districts map to 53 polygons. Two current districts, Bolga East and North East Gonja (created in 2018-19 from Bolgatanga and East Gonja), still appear as gaps although their 2014-17 cases sit inside their parent districts, and each split district's single value is painted on both of its successor areas.

### Issue 7: Districts Coded to the Wrong Current Region
- **Finding:** All 26 old Northern Region districts carry `region_code` 12 and Northern's 2022 coverage (67.7%). Eleven now lie in the regions created in 2019: Savannah (Bole, Central Gonja, East Gonja, North Gonja, Sawla-Tuna-Kalba, West Gonja) and North East (Bunkpurugu-Yunyoo, Chereponi, East Mamprusi, Mamprugu-Moagduri, West Mamprusi), where 2022 survey-weighted coverage is 79.1% and 62.8%.
- **Impact:** The coverage gap used by the allocation is wrong for these districts. Correcting it moves 3,740 nets (`04_allocation.ipynb`, alloc_cd13).
- **Mitigation:** The mapping is recorded in `src/io.py` (`REGION_2019`), and the corrected allocation is reported as a sensitivity scenario in `reports/allocation.md`.

### Issue 8: Intervention Status Dropped from the Curated File
- **Finding:** The raw workbook (`data/raw/northern-ghana-districts-routine-data-2014-17.xlsx`) records indoor residual spraying (IRS) and seasonal malaria chemoprevention (SMC) by district and month; `ghana_district_cases.csv` does not. 32 of 50 districts had IRS and 24 had SMC in at least one month of 2014-17, including every Upper East and Upper West district.
- **Impact:** Both interventions change malaria burden, and national campaigns exclude IRS districts from ITN mass distribution, so they matter for the model and for the policy.
- **Mitigation:** Documented here (`scripts/verify_claims.py`, section E); a candidate district-level covariate for the next iteration.

### Issue 9: Implausibly High Per-Capita Case Counts
- **Finding:** 39 of 50 districts report more than one confirmed positive per resident over 2014-17, and 7 report more than one per resident per year (maximum 1.78 a year).
- **Impact:** The counts likely include repeat episodes and care-seeking across district lines, or rest on undercounted population denominators, so per-capita rates are relative indicators, not incidence.
- **Mitigation:** `positive_per_100k` is used only as a relative burden indicator, as the data dictionary advises (`scripts/verify_claims.py`, section E).

---

## 5. Ethical & Privacy Protections

In compliance with DHS licensing agreements and course rules:
1. Raw household rows (`ghana_mis_sample.csv`) are strictly gitignored and excluded from version control.
2. No individual records or coordinates are displayed in public transcripts, reports, or terminal logs.
3. Analysis operates exclusively on anonymized clusters, regional aggregates, and district surveillance totals.
