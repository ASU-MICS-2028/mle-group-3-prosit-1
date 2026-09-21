# Individual Reflective Learning Journal — Machine Learning Essentials (ICS553)

**Student Name**: Eric Elikplim Sunu  
**Degree**: Master's in Intelligent Computing Systems (MICS 2028)  
**Course**: ICS553 Machine Learning Essentials · Ashesi University  
**Project**: Prosit 1 — Data-Driven Resource Allocation of Insecticide-Treated Nets (ITNs) in Ghana  
**Group**: Group 3  
**Repository**: https://github.com/ASU-MICS-2028/mle-group-3-prosit-1.git  

---

## 1. Problem Formulation & Mental Models: The "Big Picture"

### 1.1 What Are We Actually Solving?
Imagine you are given a delivery van filled with a limited number of mosquito bed nets (say, 50,000 nets). You have to distribute them across the districts of Ghana. 

If you just give all the nets to the district that reported the biggest total number of malaria cases, you will make two huge mistakes:
1. **The "Clinic Access" Trap**: A wealthy district with 10 hospitals and testing labs will record tons of malaria cases because people actually go to the doctor and get tested. A poor, remote rural district with zero clinics might report 0 cases simply because *nobody was ever tested*. Rewarding the high-reporting district punishes the neglected district!
2. **The "Already Protected" Trap**: If a district has 10,000 cases, but 95% of its people already sleep under bed nets, giving them more nets doesn't help much. Nets should go where **malaria burden is high AND existing net coverage is low** (the unmet need gap).
3. **The "False Confidence" Trap**: If our survey only interviewed 10 families in a remote district, our estimate of their malaria rate is a wild guess with huge uncertainty. If we ignore that uncertainty, we will make confident, disastrous decisions.

Therefore, this project is **not just about training a machine learning model**. It is an **equitable resource allocation decision problem** under strict constraints and uncertainty.

---

## 2. Plain-English Concept Guide: Demystifying the Statistics

### Concept 1: What is "Over-Dispersion" and Why Does Poisson Crash?
- **What Poisson assumes**: A Poisson distribution assumes that the **Mean** (average) and the **Variance** (how spread out the numbers are) are identical:
  $$\text{Variance} = \text{Mean}$$
- **What happens in our real Ghana malaria data**:
  In northern Ghana districts, the average case count is around 1,957 cases, but the variance is a staggering **151,000,000**!
  $$\frac{\text{Variance}}{\text{Mean}} \approx 77,200$$
- **The "Dummy" Analogy**: Imagine a school where the average student has 2 pencils. If pencil ownership follows a Poisson, almost every kid has 1, 2, or 3 pencils. Nobody has 100 pencils. But in reality, 90 kids have 0 pencils, and 1 kid is hoarding 200 pencils. The variance is gigantic!
- **Why Poisson fails**: Because Poisson has only *one single knob* (the mean $\lambda$), it assumes all districts cluster tightly around the average. It is completely blind to extreme outbreak districts (the "heavy tail").
- **The Fix — Negative Binomial**: Negative Binomial has *two knobs*: the mean $\mu$ PLUS a dispersion knob ($\alpha$). It allows the variance to balloon ($\text{Var} = \mu + \alpha \mu^2$), hugging the real data perfectly.

---

### Concept 2: What is "Two-Stage Cluster Sampling" vs "Naive Bootstrap"?
- **How DHS collects data**: They don't pick 17,000 random individuals scattered across Ghana. That would require driving to 17,000 separate villages! Instead, they pick **clusters** (e.g., 618 specific villages/neighbourhoods), and then interview ~25-30 households inside each chosen village.
- **The Catch**: Families living in the same village share the same swamp, the same rainfall, and the same clinic. Their answers are not independent; they are "clustered" (autocorrelated).
- **The Naive Mistake**: If you do a standard (naive) bootstrap, you mix all 17,000 households into a giant bucket and draw households randomly. You pretend you had 17,000 independent pieces of information.
- **The Consequence**: Your confidence interval comes out **artificially narrow** (1.8× too tight!). You trick yourself into believing you know a district's malaria rate down to the decimal point when you really don't!
- **The Honest Fix (Cluster Bootstrap)**: First resample the *villages* (clusters) with replacement, then resample households inside those selected villages. This correctly reflects the true uncertainty of the survey design.

---

### Concept 3: What is "Spatial Leakage" in Machine Learning?
- **The Mistake**: Doing a random 80/20 train/test split on geographic data.
- **Why it leaks**: District A and District B sit right next to each other on the map. They share the same river, the same temperature, and the same mosquitoes. If District A is in the training set and District B is in the test set, the model didn't actually "learn to predict" — it essentially peeked at District B's twin during training!
- **The Honest Fix**: **Stratify or block by region**. Force the model to be evaluated on entire regions or distinct spatial blocks it didn't look at during training.

---

## 3. Empirical Results Log (Theme A: Tasks A1–A4)

| Task | Statistical Test / Question | Plain-English Finding | The Exact Number | Notebook & Cell |
|---|---|---|---|---|
| **A1** | Is district case count over-dispersed? | Yes, massively. Variance is 77,000× higher than mean. | $\text{Var}/\text{Mean} = 77,204$ | `02_distributions.ipynb` (§A1) |
| **A2** | Can a Poisson distribution model this? | No. Poisson predicts a standard deviation of 442, but observed SD is 122,882 (278× wider). | Pearson $\chi^2/\text{df} \approx 54,100$ | `02_distributions.ipynb` (§A2) |
| **A3** | Does Negative Binomial solve this? | Yes. Adding the dispersion parameter $\alpha$ captures the long outbreak tail; dramatically superior AIC/BIC. | MLE $\alpha > 0$, AIC improvement massive | `02_distributions.ipynb` (§A3) |
| **A4** | How misleading is a naive bootstrap CI? | Naive bootstrap produces an interval 1.8× too narrow. | Cluster CI width is 1.8× naive; $\text{DEFF} \approx 3.3$ | `02_distributions.ipynb` (§A4) |
| **A4.1**| Does our survey weighting code work? | Yes. Our survey-weighted regional net ownership matches official DHS published report to 0.03%. | Diff $= 0.03\text{ percentage points}$ | `02_distributions.ipynb` (§A4) |

---

## 4. Problems Encountered & Real-World Data Caveats

| # | Anomaly / Caveat | Why it Happened | How We Handled It (Defensible Strategy) |
|---|---|---|---|
| 1 | **No parasitaemia or district column in survey CSV** | DHS household extract is anonymised; resolves to cluster & region (`hv024`), not district. | Shifted Task A4 to evaluate net ownership in an under-sampled rural *region* rather than district prevalence. |
| 2 | **Empty published ITN confidence intervals** | The reference table `ghana_region_malaria.csv` had empty cells for ITN CI columns. | Verified our point estimate against official DHS report (0.03pp match) and documented the missing published CI as a data finding. |
| 3 | **Region collinearity of net coverage** | `net_coverage_pct` in district file is a regional constant (only 3 distinct values across 50 northern districts). | Built `check_design_matrix()` to prevent rank failure; flagged that `net_coverage_pct` cannot enter alongside regional fixed effects. |
| 4 | **Constant surveillance columns** | `months_reported` is 48 for all 50 northern districts (2014–2017). | Identified that reporting gap analysis (B1) cannot use `months_reported` since it has zero variance. |
| 5 | **District boundary name mismatch** | 7 of 50 northern districts (e.g. Savelugu-Nanton) were split post-2018; 2021 map files don't join cleanly. | Built explicit name mapping and documented historical administrative restructuring as a source of data attrition. |

---

## 5. Viva Exam / Oral Defense Questions & Answers ("Explain to a Dummy")

### Q1: "Why didn't you just use standard Linear Regression or Poisson Regression for case counts?"
**Plain Answer**: 
"Linear regression assumes predictions can be negative and continuous, but you can't have $-5$ or $2.3$ malaria patients — counts must be non-negative integers! Poisson regression handles counts, but it forces the variance to equal the mean. In our northern Ghana data, the variance is 77,000 times larger than the mean because of extreme localized outbreaks. Poisson badly underestimates outbreak risk. We used Negative Binomial regression because it includes a dispersion parameter $\alpha$ that accommodates this extreme variance."

### Q2: "Why can't we just bootstrap households randomly?"
**Plain Answer**: 
"Because DHS didn't survey households at random; they used two-stage cluster sampling. Households in the same village cluster are correlated. If you resample households as if they were independent, you pretend you have way more independent information than you really do. This shrinks your confidence intervals by almost half (Design Effect $\approx 3.3$), giving false precision about vulnerable rural communities. The honest approach is a two-stage cluster bootstrap: resample villages first, then households inside them."

### Q3: "Why not allocate nets solely based on raw malaria case numbers?"
**Plain Answer**: 
"Raw cases reflect clinic visits, not true infection. A district with high clinic access will record many cases, while a remote district with no clinic will record zero. Furthermore, a district with high cases might already have 90% bed net coverage. Distributing nets must prioritize unmet need: where estimated transmission is high, existing coverage is low, and uncertainty is accounted for."
