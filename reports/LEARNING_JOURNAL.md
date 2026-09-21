# Individual Reflective Learning Journal — Machine Learning Essentials (ICS553)

**Student Name**: Eric Elikplim Sunu  
**Degree**: Master's in Intelligent Computing Systems (MICS 2028)  
**Course**: ICS553 Machine Learning Essentials · Ashesi University  
**Project**: Prosit 1 — Data-Driven Resource Allocation of Insecticide-Treated Nets (ITNs) in Ghana  
**Group**: Group 3  
**Repository**: `https://github.com/ASU-MICS-2028/mle-group-3-prosit-1.git`  
**Evaluation Role**: Statistician & Lead Analyst

---

## 1. Problem Formulation & Mental Models: The "Big Picture"

### 1.1 What Are We Actually Solving?
Imagine you are given a delivery van filled with a limited shipment of mosquito bed nets (exactly 50,000 nets). You are tasked with distributing them across the 50 administrative districts of northern Ghana (Northern, Upper East, and Upper West regions).

If you follow the "obvious" conventional approach of giving the most nets to districts reporting the highest raw counts of malaria cases, you fall into three catastrophic epidemiological traps:
1. **The "Clinic Access" Trap**: A wealthy district with multiple district hospitals and labs will record huge case counts simply because patients have doctors to test them. A poor, remote rural district with zero clinics will record almost zero cases because *nobody was ever tested*. Allocating by raw cases rewards clinic infrastructure and starves the most neglected communities!
2. **The "Referral Hospital" Distortion**: Tertiary hospitals like Bolgatanga Regional Hospital and Wa Regional Hospital treat patients arriving from dozens of surrounding rural districts. Recording those cases at the hospital's municipal address makes the hospital district look like an isolated epicentre, even though the true infections occurred in rural farming villages 50 kilometres away.
3. **The "Already Protected" Satiation Trap**: If a district reports 10,000 cases, but 85% of its families already sleep under treated nets, pouring more nets into that district produces diminishing marginal health returns. Nets must target **unmet epidemiological need** (high transmission risk $\times$ large population $\times$ low baseline net coverage).
4. **The "False Confidence" Trap**: A survey that samples only a few rural clusters carries wide statistical uncertainty. Making policy based solely on point estimates ignores the real risk of epidemic outbreaks in under-surveyed zones.

Therefore, this project is **not merely about fitting a machine learning model**. It is an **evidence-based, uncertainty-aware resource allocation policy** built to withstand rigorous academic and public health scrutiny.

---

## 2. Plain-English Concept Guide: Demystifying the Statistics

### Concept 1: What is "Over-Dispersion" and Why Does Poisson Crash?
- **What Poisson assumes**: A Poisson distribution mathematically assumes that the **Mean** (average) and the **Variance** (spread) are identical:
  $$\text{Variance} = \text{Mean}$$
- **What happens in our northern Ghana malaria data**:
  In our 50 districts, the average case count is around 195,624 cases, but the variance is an astronomical **15,098,800,000**!
  $$\frac{\text{Variance}}{\text{Mean}} \approx 77,183$$
- **The Physical Analogy (The Pencil Hoarder)**: Imagine a classroom where the teacher calculates that the average child has 2 pencils. If pencil ownership follows a Poisson distribution, nearly every kid has 1, 2, or 3 pencils. It is mathematically impossible for anyone to have 100 pencils. But in reality, 90 children have 0 pencils, and 1 child has a backpack with 200 pencils! The variance is massive.
- **Why Poisson fails in healthcare**: Because Poisson has only *one parameter* ($\lambda = \text{mean}$), it forces all districts to cluster tightly around the average. It assumes severe outbreak districts (the "heavy tail") have a probability of practically zero ($p < 10^{-100}$). If public health planners use Poisson, they severely underestimate epidemic risks.
- **The Solution (Negative Binomial)**: Negative Binomial includes a second parameter—the dispersion knob ($\alpha$). It allows the variance to expand quadratically:
  $$\text{Var}(Y) = \mu + \alpha \mu^2$$
  With estimated $\alpha = 0.2677$, it accommodates large localized outbreaks while beating Poisson by over **2.39 million AIC points**.

---

### Concept 2: What is "Two-Stage Cluster Sampling" vs "Naive Bootstrap"?
- **How DHS collects data**: The Demographic and Health Survey (DHS) does not drop 17,933 random surveyors across Ghana. That would be logistically impossible. Instead, they use **two-stage cluster sampling**:
  1. Pick 618 primary sampling units / villages (clusters) across 16 regions.
  2. Interview 25–30 households inside each chosen village.
- **The Catch**: Families in the same village share the same river, the same rainfall, and the same housing conditions. Their malaria exposure is correlated (intra-cluster correlation $\rho > 0$).
- **The Naive Mistake**: A standard "naive" bootstrap dumps all 17,933 households into a single bucket and samples them randomly with replacement. It pretends each household represents completely independent information.
- **The Dangerous Consequence**: It produces a confidence interval that is **$2.12\times$ too narrow** ($\text{DEFF} \approx 4.50$), inventing fake statistical precision.
- **The Honest Fix (Two-Stage Cluster Bootstrap)**: Resample entire *clusters* (villages) first with replacement, and then resample households within those selected clusters. This honestly mirrors the survey's true design variance.

---

### Concept 3: What is "Data Leakage" and How Did We Audit It?
Data leakage occurs when information from outside the training dataset contaminates model training, creating artificially inflated performance metrics that fail in production. We audited three distinct forms of leakage in `reports/leakage_audit.md`:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Preprocessing Leakage:                                               │
│    Fitting scalers/imputers on full data before splitting.              │
│    -> Deflates test RMSE by 212 cases (from 87,356 down to 87,144).     │
├─────────────────────────────────────────────────────────────────────────┤
│ 2. Target Encoding Catastrophe:                                         │
│    Encoding high-cardinality district categories using target means     │
│    without out-of-fold regularization.                                  │
│    -> Model memorizes training targets, faking R² = 1.0000 (honest 0.49)│
├─────────────────────────────────────────────────────────────────────────┤
│ 3. Spatial Autocorrelation Leakage:                                     │
│    Using naive random 80/20 train/test splits on geographical data.     │
│    -> Test districts sit adjacent to identical training districts.      │
│    -> Test error drops by 45.5% (from 87,356 down to 47,646) due to     │
│       geographic peeking, creating false confidence.                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Concept 4: The Allocation Policy Shift (Naive vs Equitable)
- **The Naive Formula**: Distributes nets strictly by historical case counts ($50,000 \times \frac{\text{cases}_i}{\sum \text{cases}}$).
- **The Equitable Formula**: Distributes nets by **unmet need**:
  $$\text{Need}_i = \hat{\mu}_{i,\text{upper}} \times \left(1 - \frac{\text{coverage}_i}{100}\right)$$
  using **Hamilton's largest remainder apportionment** to ensure exactly 50,000 integer nets.
- **The Major Policy Shifts**:
  - **Tamale (+1,692 nets) & Sagnarigu (+1,012 nets)**: High population centers with lower baseline coverage (~67.7%) gain substantially, closing massive population-level vulnerability gaps.
  - **Wa (-1,516 nets) & Bolgatanga (-665 nets)**: Urban tertiary hospital hubs lose nets. Their raw case counts reflect patients travelling from rural districts, while their local populations already have high coverage (~70–80%).

---

## 3. Empirical Results Log (Themes A, B, C)

| Theme & Task | Statistical Test / Research Question | Plain-English Finding | Exact Empirical Metric | Notebook & Report Citation |
|---|---|---|---|---|
| **A1** | Is district case count over-dispersed? | Yes, massively. Variance exceeds mean by 77,000×. | $\text{Var}/\text{Mean} = 77,183$ | `02_distributions.ipynb` (§A1) |
| **A2** | Can a Poisson distribution model this? | No. Poisson assumes SD of 442, but real SD is 122,882. | Pearson $\chi^2/\text{df} = 54,147$ | `02_distributions.ipynb` (§A2) |
| **A3** | Does Negative Binomial solve over-dispersion? | Yes. Dispersion $\alpha$ captures the heavy tail; massive AIC improvement. | $\Delta\text{AIC} = 2,393,669$, $\alpha = 0.2677$ | `02_distributions.ipynb` (§A3) |
| **A4** | How misleading is a naive household bootstrap? | Naive bootstrap produces an interval more than $2\times$ too narrow. | Cluster CI width ($15.20\text{ pp}$) vs Naive ($7.17\text{ pp}$); $\text{DEFF} \approx 4.50$ | `02_distributions.ipynb` (§A4) |
| **A4.1**| Does our survey weighting reproduce official benchmarks? | Yes. Survey-weighted Northern net ownership matches official DHS report to 0.09pp. | Estimated $67.69\%$ vs Published $67.60\%$ | `02_distributions.ipynb` (§A4.1) |
| **B1** | What is the survey design effect on national net ownership? | Unweighted ownership overstates weighted ownership by 4.19 pp. | Unweighted $70.96\%$ vs Weighted $66.77\%$ | `01_eda.ipynb` [C-01] |
| **B2** | Does global preprocessing leak test information? | Yes. Imputing/scaling on full data deflates test RMSE by 212 cases. | Leaky RMSE $87,144$ vs Honest $87,356$ | `reports/leakage_audit.md` |
| **B3** | What happens under unregularized target encoding? | Total target memorization. Yields fraudulent perfect fit. | Fake $R^2 = 1.0000$ vs Honest $R^2 = 0.4905$ | `reports/leakage_audit.md` |
| **B4** | What is the impact of spatial autocorrelation on train/test splits? | Random split underestimates true generalization error by $45.5\%$. | Random Split RMSE $47,646$ vs Region Stratified $87,356$ | `reports/leakage_audit.md` |
| **C1** | How does equitable allocation shift resources? | Reallocates nets from hospital hubs to rural/peri-urban populations. | Tamale $+1,692$; Wa $-1,516$; exactly 50,000 nets allocated | `04_allocation.ipynb` & `reports/allocation.md` |

---

## 4. Problems Encountered & Real-World Data Caveats

| # | Anomaly / Caveat | Root Cause | Defensible Methodological Handling |
|---|---|---|---|
| 1 | **Missing Parasitaemia & District Identifiers in Household Microdata** | DHS microdata is de-identified for privacy; resolves only to region (`hv024`) and cluster. | Reframed Task A4 to evaluate net ownership in rural Northern Region rather than district prevalence. |
| 2 | **Empty Published ITN Confidence Intervals** | DHS reference summary table `ghana_region_malaria.csv` has empty strings for net CI columns. | Verified survey weighting against published point estimate ($0.09\text{ pp}$ match); documented empty published intervals as an upstream data gap. |
| 3 | **Region Collinearity of Net Coverage** | District surveillance file contains only 3 distinct regional coverage values for 50 districts. | Used `check_design_matrix()` to reject simultaneous inclusion of region dummies; documented that coefficient captures macro-region effect. |
| 4 | **Zero-Variance Surveillance Columns** | `months_reported` (48) is constant across all 50 districts. | Excluded from regression pipelines; refocused reporting gap analysis on spatial boundaries. |
| 5 | **Administrative Boundary Splits Post-2018** | 7 northern districts (e.g. Garu-Tempane, Savelugu-Nanton) were split into new administrative units in 2018. | Built explicit aliasing and polygon-aggregation dictionary in `src/viz.py` to map all 50 districts seamlessly. |
| 6 | **Temporal Mismatch Between Datasets** | Routine clinic cases are from 2014–2017, while household survey coverage reflects 2022. | Explicitly defended as an associative planning proxy rather than a lagged causal mechanism. |

---

## 5. Comprehensive Viva Exam Defense Bank ("The Grill-Me Cheat Sheet")

### Q1: "Why did you use Negative Binomial regression instead of ordinary least squares (OLS) or Poisson?"
> **Oral Defense Script:**  
> *"OLS assumes continuous errors that can take negative values, but clinical malaria counts are strictly non-negative integers. Poisson regression is designed for counts, but it enforces the equidispersion assumption—that variance equals the mean. In northern Ghana, the variance of district case counts is 77,183 times larger than the mean. A fitted Poisson model predicts a standard deviation of 442 against an observed standard deviation of 122,882—it is 278 times too narrow! This catastrophic failure survives even after controlling for population size ($\chi^2/\text{df} \approx 54,147$). Negative Binomial introduces a dispersion parameter $\alpha$ that allows variance to scale quadratically ($\text{Var} = \mu + \alpha \mu^2$), reducing AIC by over 2.39 million points and honestly modeling extreme epidemic surges."*

---

### Q2: "Why is a standard bootstrap invalid for DHS survey data?"
> **Oral Defense Script:**  
> *"The DHS does not take a simple random sample of independent households; they use a two-stage stratified cluster sampling design. Households living within the same census cluster share the same physical ecology, standing water, and socioeconomic status. A naive bootstrap samples households independently, ignoring this intra-cluster correlation. In rural Northern Region, a naive bootstrap yields a net ownership CI of 7.17 percentage points, whereas our design-consistent two-stage cluster bootstrap yields an interval of 15.20 percentage points—more than 2.1 times wider ($\text{DEFF} \approx 4.50$). Using a naive bootstrap would give the Ministry dangerous false precision."*

---

### Q3: "Explain what data leakage occurred in your pipeline audit and how you prevented it."
> **Oral Defense Script:**  
> *"We audited three distinct leakage vectors. First, preprocessing leakage: fitting imputers or scalers on the full dataset before splitting leaks test set distributions into the training phase, artificially lowering test RMSE by 212 cases. We prevented this structurally using scikit-learn's `Pipeline` and `ColumnTransformer`. Second, target encoding leakage: replacing categorical districts with unregularized target averages allows the model to memorize the training labels, generating a fraudulent $R^2 = 1.0000$. We rejected target encoding. Third, spatial leakage: a standard random train/test split allows adjacent, geographically correlated districts into both sets, deflating generalization error by $45.5\%$ ($47,646$ vs $87,356$). We enforced region-stratified holdouts to evaluate true spatial transferability."*

---

### Q4: "Why did you cut over 2,100 nets from Bolgatanga and Wa when their hospitals reported the most cases in the country?"
> **Oral Defense Script:**  
> *"Allocating nets by raw hospital cases falls victim to the Referral Hospital Bias. Bolgatanga Regional Hospital and Wa Regional Hospital serve as tertiary referral centers for entire regions. When a patient from rural Nabdam or Lambussie travels to Bolgatanga for treatment, the health record logs that case in Bolgatanga, not in the rural community where transmission occurred. Furthermore, DHS survey data shows that Upper East and Upper West already have baseline net ownership between 70% and 80%. Pouring thousands of additional nets into these urban referral centers produces diminishing marginal returns. Our equitable model redirects these nets to high-population, underserved rural and peri-urban districts like Tamale ($+1,692$) and Sagnarigu ($+1,012$), closing true community transmission gaps."*

---

### Q5: "How does your allocation ensure that exactly 50,000 nets are delivered without fractions?"
> **Oral Defense Script:**  
> *"We implemented Hamilton's Largest Remainder Method, the standard mathematical apportionment algorithm used in constitutional seat allocation. Each district receives its floor integer quota of nets ($\lfloor q_i \rfloor$), and the remaining unallocated nets are distributed one-by-one to districts with the largest fractional remainders. This guarantees that exactly 50,000 nets are distributed, no district receives negative nets, and zero rounding discrepancies occur."*

---

### Q6: "If the Ministry's budget is cut by 50% to 25,000 nets, does your model break?"
> **Oral Defense Script:**  
> *"No. Because our allocation index $W_i$ represents normalized relative epidemiological need, Hamilton's apportionment scales linearly. The priority ranking of districts is invariant to budget scaling. The top-priority districts remain identical whether the consignment is 25,000 or 100,000 nets."*
