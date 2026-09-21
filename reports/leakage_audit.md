# Leakage Audit — Pipeline Integrity & Generalization Defense

**Course**: ICS553 Machine Learning Essentials · Prosit 1  
**Author**: Eric Elikplim Sunu  
**Repository**: https://github.com/ASU-MICS-2028/mle-group-3-prosit-1.git  
**Rubric Anchor**: Pipeline & Leakage Handling (25% of total grade)  

---

## 1. Executive Summary & Audit Mandate

In predictive epidemiology and healthcare resource allocation, **data leakage** is catastrophic. When test data contaminates feature scaling, encoding, or validation splitting, the model produces artificially deflated error metrics. A health authority relying on a leaky model operates with false confidence, sending medical supplies to the wrong districts.

This audit evaluates four primary leakage vectors, contrasting our disciplined pipeline against **deliberate leaky counter-examples** implemented in [`notebooks/03_pipeline_leakage.ipynb`](../notebooks/03_pipeline_leakage.ipynb).

---

## 2. Empirical Leakage Audit Matrix

| Leak Vector | Disciplined Pipeline | Leaky Pipeline (Counter-example) | Empirical Metric Delta | Mechanistic Impact & Verdict |
|---|---|---|---|---|
| **1. Split Timing (Preprocessing)** | Split first; fit `StandardScaler` strictly on training set inside `Pipeline` | Fit `StandardScaler` on pooled dataset before splitting | **Test RMSE:** Clean 87,356 vs Leaky 87,144 ($-212$ cases) | **Verified Clean:** Pooled scaling leaks test distribution moments $(\mu, \sigma)$ into train, artificially deflating error. |
| **2. Feature Construction (Target Leak)** | Independent demographic/environmental features (population, region) | Target-encode district name using mean target cases before split | **Test $R^2$:** Clean 0.49 vs Leaky 1.00 ($+0.51$ artificial cheat) | **Verified Clean:** Leaky target encoding bakes the outcome into the feature matrix, enabling 100% memorization. |
| **3. Spatial Autocorrelation** | Split stratified by geographic region (`region_code`) | Naive random row-wise train/test split (`train_test_split(shuffle=True)`) | **Test RMSE:** Stratified 87,356 vs Random 47,646 (**45.5% overoptimistic error**) | **Verified Clean:** Adjacent districts share climate, rainfall, and vector ecology. Random holdouts leak geographic twins. |
| **4. Temporal Alignment** | Explicitly documented as reverse-time causality caveat | Ignored temporal gap; treated 2022 survey as concurrent | **Temporal Gap:** 2022 survey used with 2014–17 routine cases | **Documented Caveat:** Survey post-dates cases by 5–8 years. Region net effect must not be claimed as concurrent causality. |

---

## 3. Deep Technical Analysis of Evaluated Leakage Vectors

### Vector 1: Split Timing & Preprocessor Encapsulation
- **The Vulnerability**: Many pipelines compute `scaler.fit_transform(X)` on the complete matrix and subsequently call `train_test_split()`.
- **The Empirical Reality**: When the scaler sees the test set, the test set's mean $\mu_{\text{test}}$ and variance $\sigma^2_{\text{test}}$ shift the normalization parameters. In our northern Ghana dataset, this deflates test RMSE by 212 cases.
- **The Structural Fix**: In [`src/features.py`](../src/features.py), we encapsulate all imputers and scalers inside scikit-learn `Pipeline` and `ColumnTransformer` objects. Calling `pipeline.fit(X_train, y_train)` guarantees that preprocessors are fit *strictly on training rows*.

---

### Vector 2: Target Encoding & The Outcome Memorization Trap
- **The Vulnerability**: Target encoding replaces high-cardinality categorical variables with the target variable's mean:
  $$\hat{x}_i = \frac{1}{|C_k|} \sum_{j \in C_k} y_j$$
- **The Empirical Reality**: When computed globally, the model trivially achieves a test $R^2 = 1.0000$. The model has not learned any epidemiologic relationship; it simply looked up the answer key through the feature!
- **The Structural Fix**: Target encoding is strictly banned from our feature pipeline. Categorical indicators are one-hot encoded or represented by independent administrative domain indicators.

---

### Vector 3: Spatial Autocorrelation (The Headline Ecological Leak)
- **The Theoretical Reality**: Standard machine learning assumes identically and independently distributed ($i.i.d.$) samples. Spatial data explicitly violates independence:
  $$\text{Cov}(Y(s_i), Y(s_j)) > 0 \quad \text{for small } \|s_i - s_j\|$$
  A district and its neighboring district share rainfall, river basin hydrology, temperature, and mosquito vector breeding conditions ([8][9]).
- **The Empirical Reality**: Under a naive random row-wise split, Test RMSE is **47,646**. Under a disciplined region-stratified split, Test RMSE is **87,356**. 
- **The Overestimation**: Random holdouts produce an **artificially optimistic 45.5% reduction in error**. The model appears to generalize well only because test districts have geographical twins in the training set.
- **The Literature**: This matches findings by Ploton et al. (*Nature Communications*, 2020) [8], which proved ecological models severely overestimate out-of-domain power under random holdouts, and Kattenborn et al. (2022) [9], which measured a 28% performance inflation from spatial autocorrelation.
- **The Structural Fix**: [`src/io.py::split_data()`](../src/io.py) enforces region-stratified partitioning across all tasks.

---

### Vector 4: Temporal Alignment Caveat
- Routine district surveillance spans **2014–2017**, whereas household net coverage reflects the **2022 DHS survey**.
- `net_coverage_pct` resolves to a regional constant (Northern 67.7%, Upper East 79.6%, Upper West 69.8%).
- While useful as a relative structural indicator of regional net adoption, using a 2022 indicator to explain 2014–17 case counts introduces a reverse-time causality. This is documented as an unavoidable data artifact in [`reports/datasheet.md`](datasheet.md).

---

## 4. Audit Conclusion & Viva Defense Statement

When asked by the examination panel:
> *"How do you know your model's performance isn't an artifact of data leakage?"*

**The Defensible Viva Answer:**
> *"We audited our pipeline against three deliberate counter-examples. First, preprocessors are encapsulated in scikit-learn Pipelines, eliminating split-timing leakage. Second, we avoided target encoding, which achieves a fake $R^2 = 1.0$. Third, we proved that naive random train/test splits leak spatial autocorrelation between neighboring districts, overestimating performance by 45.5%. By enforcing region-stratified splits in `src/io.py`, our reported RMSE of 87,356 reflects honest out-of-region generalization."*
