# Datasheet for Datasets — Prosit 1 (ITN Allocation in Ghana)

## 1. Motivation
- **Purpose:** Inform data-driven, equitable allocation of insecticide-treated nets (ITNs) across Ghana's districts under severe resource constraints.
- **Creators:** Curated from open-access sources (WHO/GHO, DHS subnational indicators, Ghana Health Service routine surveillance, geoBoundaries) and a de-identified extract of the licensed Ghana 2022 DHS household microdata.

## 2. Composition
- **`data/ghana_mis_sample.csv`:** 17,933 households across 618 clusters and 16 regions. Contains household assets, net ownership (`has_net`), net counts (`num_nets`), net usage, and sampling weights (`sample_weight`).
- **`data/ghana_region_malaria.csv`:** Longitudinal region-level malaria prevalence (RDT, microscopy) and ITN indicators across six DHS surveys (2003–2022) with published confidence intervals.
- **`data/ghana_district_cases.csv`:** Routine surveillance data covering 50 districts in the 3 northern regions (Northern, Upper East, Upper West) from 2014–2017, combined with regional ITN coverage from the 2022 DHS.

## 3. Collection Process & Sampling Design
- **Household Survey:** Two-stage cluster sampling design. Primary Sampling Units (PSUs / clusters) selected with probability proportional to size; households sampled systematically within clusters.
- **Weights:** Normalized survey weights (`sample_weight`) must be accounted for to correct for over/under-sampling across regions.
- **Cluster Autocorrelation:** Observations within the same cluster are correlated; variance estimation requires cluster bootstrap.

## 4. Preprocessing & Transformations
- Extraction and de-identification executed via `data_prep/` scripts.
- Region scheme aligned to 16 administrative regions (post-2018/2022 reform).

## 5. Known Limitations & Caveats
- **Geographic Discrepancy:** District routine surveillance exists only for 50 northern districts, whereas regional survey indicators exist for all 16 regions.
- **Temporal Mismatch:** Routine district data spans 2014–2017, while household net ownership reflects 2022.
- **Denominator Scaling:** `positive_per_100k` is cumulative over the reporting period, not an annual incidence.
