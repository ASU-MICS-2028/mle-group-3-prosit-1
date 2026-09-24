# Leakage Audit: Pipeline Integrity and Generalisation

**Course:** ICS553 Machine Learning Essentials · Prosit 1  
**Author:** Eric Elikplim Sunu  
**Repository:** https://github.com/ASU-MICS-2028/mle-group-3-prosit-1  
**Rubric anchor:** Pipeline and leakage handling (25% of the grade)  
**Notebook:** [`notebooks/03_pipeline_leakage.ipynb`](../notebooks/03_pipeline_leakage.ipynb), re-verified 2026-09-24

---

## 1. Summary

We built each leak deliberately and compared it with the disciplined version. With 50 districts a
test set holds only 10, so one random split is an anecdote: every comparison is repeated over 500
random seeds before we call a difference real.

- **Target encoding** and **spatial leakage** are real and large.
- **Preprocessing leakage** is real in principle but negligible for this model.
- The **temporal mismatch** between 2022 coverage and 2014-17 cases is documented, not measurable.

The most important result is spatial. Random and region-stratified splits give the same test error,
but holding out a whole region makes the error about four times larger. Our model does not
generalise to regions it has not seen, so we do not use it to rank them.

---

## 2. Audit matrix

| Leak vector | Disciplined version | Leaky counter-example | Measured effect | Verdict |
|---|---|---|---|---|
| 1. Split timing | Scaler fitted inside a `Pipeline`, on training rows only | Scaler fitted on all 50 districts before splitting | 212 cases of RMSE at seed 42; 44 on average over 500 seeds | Real mechanism, negligible here |
| 2. Target encoding | Features that do not use the outcome (test R² 0.26) | District encoded with its own case count (test R² 1.00) | +0.74 R² | Leak confirmed; target encoding not used |
| 3. Spatial | Whole region held out (pooled RMSE 365,128) | Random or region-stratified split (median RMSE 91,413 and 90,169) | 4.0 times the stratified error | Leak confirmed; no generalisation to unseen regions |
| 4. Temporal | 2022 coverage documented as a regional proxy | Reading 2022 coverage as a cause of 2014-17 cases | Not measurable with these data | Documented caveat |

Sources: cells `leak_cd04`, `leak_cd06`, `leak_cd08`, `leak_cd12` and `leak_cd14`; the matrix
itself is printed by `leak_cd10`.

---

## 3. The four vectors

### Vector 1: split timing (preprocessing)
- **Mechanism:** fitting a scaler or imputer on the full matrix lets the test rows' mean and
  variance shape the training transform.
- **Measured:** at seed 42 the leaky pipeline's test RMSE is 212 cases lower (87,144 against
  87,356). Over 500 seeds the gap averages 44 cases (sd 123), and the leaky version looks better in
  only 57% of seeds: noise, next to errors of about 90,000. With two features, no missing values
  and a Ridge model, there is little for this leak to exploit.
- **Fix:** preprocessing lives inside a scikit-learn `Pipeline` (see `src/features.py`), fitted
  after the split from `io.split_data`.

### Vector 2: target encoding
- **Mechanism:** replacing a category with the mean outcome of its rows puts the answer into the
  feature. Each district appears once, so its encoding equals its own case count.
- **Measured:** test R² 1.00, against 0.26 for features that do not use the outcome.
- **Fix:** no target encoding in the pipeline; categories are one-hot encoded.

### Vector 3: spatial autocorrelation (the headline)
- **Mechanism:** neighbouring districts share rainfall, ecology and transmission, so a test
  district whose neighbour is in training has partly been seen already.
- **What did not show it:** at seed 42 the random split's RMSE (47,646) is 45.5% below the
  stratified split's (87,356), but the two splits drew different test districts. Over 500 seeds
  their distributions match (medians 91,413 and 90,169; the random split is lower in 48% of seeds).
  Stratifying by region keeps every region in training, which is good for representation, but it
  keeps neighbours on both sides of the split, so it cannot be the fix.
- **What did:** training on two regions and testing on the third gives RMSEs of 272,529 (Northern
  held out), 589,777 (Upper East) and 139,143 (Upper West): 365,128 pooled, about four times the
  stratified error.
- **Literature:** random validation overstates the predictive power of spatial models, which
  spatially blocked validation reveals [1]; in one study random hold-outs overestimated performance
  by up to 28% against block validation [2].
- **Fix:** `io.split_data(..., hold_out=region)` holds out whole regions. Stratification stays the
  default, for representation.
- **Consequence:** the model cannot rank districts in regions it has not seen, including the 207
  districts outside our data.

### Vector 4: temporal alignment
- Routine surveillance covers 2014-17; household net coverage comes from the 2022 DHS.
- `net_coverage_pct` takes one value per region (Northern 67.7%, Upper East 79.6%, Upper West
  69.8%), so its coefficient is a regional effect. A 2022 indicator cannot cause 2014-17 cases, so
  we do not read it causally. See [`reports/datasheet.md`](datasheet.md).

---

## 4. Viva answer

**Question:** How do you know your model's performance is not an artefact of leakage?

**Answer:** We built each leak deliberately and repeated every comparison over 500 seeds.
Preprocessing leakage is real in principle but negligible for our model. Target encoding produced a
fake R² of 1.00. For space, a region-stratified split is not enough: it gives the same error as a
random split, while holding out a whole region makes the error about four times larger. So we
report that the model does not generalise to unseen regions, and we do not use it to rank them.

---

## References

1. Ploton P. et al. Spatial validation reveals poor predictive performance of large-scale
   ecological mapping models. *Nature Communications* 11, 4540 (2020).
   doi:10.1038/s41467-020-18321-y
2. Kattenborn T. et al. Spatially autocorrelated training and validation samples inflate
   performance assessment of convolutional neural networks. *ISPRS Open Journal of Photogrammetry
   and Remote Sensing* 5, 100018 (2022). doi:10.1016/j.ophoto.2022.100018
