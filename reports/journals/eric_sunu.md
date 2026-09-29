# Learning journal: Eric Elikplim Sunu

ICS553 Machine Learning Essentials · MICS 2028 · Ashesi University
Prosit 1, allocating insecticide-treated nets (ITNs) in Ghana · Group 3
My seat: cartographer · My PBL role: chairperson · Last updated: 2026-09-29

This is my own record of Prosit 1: what I noticed, what I got wrong and put right, and what I
can now explain.

---

## 1. The problem, and the traps I learned to watch for

We had 50,000 nets for the 50 districts of the three northern regions as they were in 2014-17
(Northern, Upper East, Upper West). My question was where they would do the most good, and how
sure we could be.

The obvious answer is to send nets where the most cases were reported. I learned that four traps
sit between that answer and a defensible one:

1. **Clinic access.** Facility counts measure testing as well as malaria. I saw a hint of this in
   our data: Northern Region has the highest median test positivity (65%) but the fewest reported
   cases per person (0.27 a year, against 0.88 in Upper East and 0.80 in Upper West). High
   positivity with few cases looks like under-testing to me.
2. **Referral hospitals.** Patients may travel to a regional hospital and make its district look
   worse. Our early drafts leaned on this story, but when I checked, our data did not support it:
   Bolgatanga is only 4th of 13 in Upper East on cases per person, Nabdam (often named as a sending
   district) is 1st, and Tamale, home to the north's only tertiary hospital, reports the lowest
   rate of all 50 districts.
3. **Existing coverage.** A net does the most good where few households have one. But our coverage
   figure is one number per region, measured in 2022, five to eight years after the cases.
4. **False confidence.** Survey intervals must reflect how the survey was drawn, and a result
   should survive a change of random seed and a region the model has never seen.

---

## 2. Concepts I can now explain in my own words

### Over-dispersion: why the Poisson fails
- A Poisson model has one parameter, so its variance must equal its mean.
- Our 50 districts average 195,640 confirmed cases (2014-17 combined) with a variance of about
  1.51 × 10¹⁰: 77,183 times the mean.
- A Poisson with that mean implies a standard deviation of 442; the districts actually vary by
  122,882, about 278 times more.
- Part of that is population: big districts have more cases. When we modelled the rate with a
  log-population offset, the Poisson dispersion ratio was still 54,147 (a correct Poisson gives
  about 1).
- The negative binomial adds one dispersion parameter: Var = μ + αμ². With the offset, α = 0.268,
  and it beats the Poisson by 2,393,669 AIC points. It is our working model; we kept the Poisson
  only to show why one parameter is not enough.
- The analogy I use: if the average pupil owns 2 pencils, a Poisson class has nearly everyone on 1
  to 3. A real class can have many pupils on 0 and one with 200.
- I have to say which α I mean. 0.395 is the plain moments estimate with no covariates, used in
  figure a3. 0.268 is the model with the population offset.
- Where I stand: I understand why the Poisson fails here, but I am still learning to derive both
  models and to explain the dispersion parameter without notes.

### Cluster sampling and the bootstrap
- The DHS picks clusters (enumeration areas) first, then about 30 households in each. Households in
  a cluster share a village, water sources and the last net campaign, so their answers are
  correlated.
- Resampling households as if independent pretends we have more information than we do. In rural
  Northern Region (582 households in 20 clusters) the naive household bootstrap gives an interval
  7.17 points wide; the cluster bootstrap gives 15.20, 2.12 times wider. The implied design effect
  is 4.50: the sample carries the information of a simple random sample about a quarter its size.
- I checked that this was not luck. Over 20 seeds the design effect ranges from 4.46 to 5.39, and
  an independent design-based calculation (Taylor linearisation, no bootstrap) gives 14.34 against
  7.01 points, a design effect of 4.18. The conclusion stands.
- Our bootstrap also resamples households inside each drawn cluster. That second stage adds a
  little width (clusters only: 14.02 points), so our interval is slightly conservative.
- Our weighted estimate for all of Northern Region is 67.69%, against 67.6% published: 0.09 points
  apart. That validates our weights and the `has_net` coding. It does not validate the interval,
  because the published ITN intervals in our file are empty (0 of 76 rows).
- Weighted and unweighted national ownership differ (66.77% vs 70.96%) because some areas were
  deliberately oversampled, which the weights correct. I had to stop calling that a design effect:
  a design effect is about variance.
- We chose rural Northern for its link to our surveillance districts, not because it is the most
  under-sampled: it ranks 10th of 16 regions by rural clusters.

### Data leakage, and why a stratified split is not a spatial split
- **Preprocessing.** Fitting a scaler on all 50 districts before splitting lets the test data shape
  the training transform. The mechanism is real, but here the effect is negligible: 212 cases of
  RMSE at seed 42, and 44 on average over 500 seeds, noise next to errors of about 90,000. The
  leaky version looks better in only 57% of seeds.
- **Target encoding.** Encoding each district by its own case count makes the feature the answer:
  test R² 1.00, against 0.26 with honest features.
- **Spatial.** This is the one we got wrong first. Stratifying a split by region makes sure every
  region is in training and test. That is about representation; it does not block space, because
  each test district still has neighbours in training. Our first 45.5% effect compared two
  different random test sets at one seed. Over 500 seeds, random and stratified splits give the
  same error (medians 91,413 and 90,169). The real spatial test holds out a whole region: train on
  two, predict the third. That gives a pooled RMSE of 365,128, about four times larger (held-out
  Northern 272,529, Upper East 589,777, Upper West 139,143). So our model cannot predict a region
  it has not seen, and cannot rank the 207 districts outside our data.
- **Temporal.** Using 2022 coverage to explain 2014-17 cases runs time backwards. We document it
  and do not read the coefficient causally.

### Confidence interval or prediction interval
- A confidence interval for the mean says where the average count for districts like this one
  probably lies. It reflects uncertainty in the model's parameters.
- A prediction interval says where one district's actual count may fall. It adds the negative
  binomial's own randomness, so it is much wider.
- Our allocation uses the upper bound of the confidence interval for the mean (the default of
  statsmodels' `get_prediction`), although our early reports called it a prediction interval. I
  corrected that wording. Because the only covariate is regional, the upper bound is one multiplier
  per region: 1.20 for Northern, 1.34 for Upper East, 1.16 for Upper West.

### Confounding: why more nets can predict more malaria
- The model's coefficient on net coverage is +0.082 per percentage point (p = 1.7 × 10⁻⁷):
  regions with more nets had more malaria.
- Nets do not cause malaria. Nets are sent where malaria is worst, and our coverage is from 2022
  while the cases are from 2014-17. With only three distinct values, the coefficient is a region
  effect with a coverage label.
- It matters for the allocation: the coefficient raises predicted risk in high-coverage regions
  faster than the gap term (1 - coverage) lowers it. So higher coverage earns more nets per person,
  the opposite of what we intended.

### What our allocation rule actually does
- The rule: weight = upper confidence bound of expected cases × (1 - coverage). Hamilton's
  largest-remainder method turns the weights into exactly 50,000 whole nets.
- Coverage is regional, so expected cases are population times a regional rate. Within a region,
  nets follow population exactly: 8.5 nets per 1,000 people in Northern, 16.0 in Upper East, 9.2
  in Upper West.
- Compared with a case-proportional split, the more cases per person a district reported, the more
  nets per person it gives up (rank correlation -1.00 within each region). Tamale gains most
  (+1,692): the most populous district, and the fewest cases per person of all 50. Nabdam (-761)
  and Bole (-376) report the most cases per person in their regions.
- My framing: within a region this is a universal-coverage rule, close to Ghana's actual practice
  of allocating ITNs by population (about one net per two people). I think that is defensible if we
  say it openly. It is not a correction for referral bias.
- The regional split is fragile. A model with region effects instead of a coverage slope fits
  better (AIC 1,253.8 against 1,286.8) and moves 7,720 nets between regions. Correcting the coverage
  of the 11 districts now in Savannah or North East moves 3,740. Using the point estimate instead of
  the upper bound moves 1,391.

---

## 3. Numbers I checked (results log, 22 September)

The source is a notebook cell unless marked *script*, meaning `scripts/verify_claims.py`.

| Task | Result | Source |
|---|---|---|
| A1 over-dispersion | Variance/mean 77,183 | nb02 cd09 |
| A2 Poisson fit | SD 442 against 122,882 (278 times) | nb02 cd15 |
| A3 with population offset | Pearson χ²/df 54,147; NB α 0.2677; AIC gap 2,393,669 | nb02 cd25, cd26 |
| A4 survey interval | Rural Northern 76.0%; naive 7.17 vs cluster 15.20 points; 2.12 times; DEFF 4.50 | nb02 cd33, cd34 |
| A4 robustness | DEFF 4.46 to 5.39 over 20 seeds; design-based DEFF 4.18 | script, section A |
| A4.1 published check | 67.69% vs 67.6% (0.09 points) | nb02 cd39 |
| B1 weighting | Unweighted 70.96% vs weighted 66.77% | nb01 eda_cd05 |
| B2 preprocessing leak | 87,144 vs 87,356 at seed 42; 44 on average over 500 seeds | nb03 leak_cd04, leak_cd12 |
| B3 target leak | Test R² 1.0000 vs 0.2618 | nb03 leak_cd06 |
| B4 spatial leak | Random vs stratified: no difference over 500 seeds; region held out: 365,128 | nb03 leak_cd12, leak_cd14 |
| C allocation | Northern 24,196, Upper East 18,631, Upper West 7,173; all 50 rows of `reports/allocation.md` reproduce | nb04 alloc_cd07, alloc_cd09 |
| C what the rule does | 8.5 / 16.0 / 9.2 nets per 1,000 people; coverage coefficient +0.082 | nb04 alloc_cd11 |
| C sensitivity | 7,720 nets move under region effects; 3,740 with corrected coverage | nb04 alloc_cd13 |

---

## 4. What we got wrong, and what I put right

These claims were in our drafts. My checks showed they were wrong, not reproducible or
overstated, so I corrected them in the reports and the deck.

| What we said | What I found to be true | Where it appeared |
|---|---|---|
| Honest test R² 0.4905 | 0.2618; 0.4905 does not reproduce | leakage audit, claims table C-05, old deck, old journal |
| Random splits understate error by 45.5% | One seed; no difference over 500 seeds. A held-out region raises error about four times | same |
| Our 87,356 RMSE reflects out-of-region generalisation | Out-of-region RMSE is 365,128 | leakage audit |
| Preprocessing leakage deflates error by 212 cases | One seed; negligible on average | leakage audit, old deck, old journal |
| Upper bound of a 95% prediction interval | Confidence interval for the mean | framing, allocation brief, nb04, old deck |
| Depot totals 24,980 / 17,547 / 7,473 | 24,196 / 18,631 / 7,173 | allocation brief, old deck |
| Schedule total: 5,263,334 people, 9,781,209 cases | 4,788,809 and 9,781,981 | allocation brief |
| The cluster interval extends down to 60.1% | No interval reaches 60.1 (all-Northern 61.4 to 74.0) | allocation brief |
| Lower Northern coverage would justify more nets for Northern | Under our model it gives Northern fewer (22,939 vs 24,196) | allocation brief |
| Wa and Bolgatanga have about 80% coverage | Regional averages: Upper East 79.6%, Upper West 69.8% | nb04 |
| Referral hospitals explain Wa and Bolgatanga | A hypothesis; our data cut against it | framing, allocation brief, old deck, old journal |
| Bolgatanga and Wa have tertiary hospitals | Regional (secondary) hospitals; Tamale Teaching Hospital is the only tertiary hospital in the north | allocation brief, old journal |
| Case-proportional allocation is the status quo | Ghana allocates ITNs by population | framing, nb04 |
| Rural Northern is the most under-sampled domain | 10th of 16 by rural clusters; chosen for relevance | nb02 |
| The weighting gap is a design effect | It comes from unequal selection probabilities | claims table C-01 |
| 1.8 times wider, DEFF 3.3, 0.03 points | 2.12 times, DEFF 4.50, 0.09 points (after switching to rural Northern) | README, methodology guide, Theme A guide PDF |
| Allocation map legend: positives per 100k | The map shows nets allocated | `figures/c2_allocation_map.png` |

I checked the hospital-tier and national-strategy facts on 22 September (Tamale Teaching
Hospital's own site, the Ghana Service Provision Assessment 2002, and the PMI Ghana Malaria
Operational Plan FY2017). On 24 and 25 September I confirmed the wording against each source's
own text, and every reference on the deck's References slide against the original.

---

## 5. What I noticed about the data

- The survey file has no parasitaemia column and no district identifier; it resolves only to
  region and cluster. So I could not bootstrap prevalence, as the brief asks, and used net
  ownership instead.
- The published ITN confidence intervals are empty (0 of 76 rows); prevalence intervals exist for
  54 of 76.
- `net_coverage_pct` takes one value per region (67.69, 79.56, 69.76), equal to the survey-weighted
  `has_net`. `has_net` counts any net and the published figures count ITNs, but they agree within
  0.3 points.
- `months_reported`, `year_start` and `year_end` are constant and carry no information.
- 11 districts coded as Northern are now in Savannah (6) or North East (5): in 2019 the old
  Northern Region became three regions. Their 2022 coverage is 79.1% and 62.8%, not 67.7%.
- The raw surveillance workbook records district-level indoor spraying (IRS) and seasonal
  chemoprevention (SMC); the curated file dropped both. 32 of 50 districts had spraying and 24 had
  chemoprevention in 2014-17.
- 39 of 50 districts report more than one confirmed case per resident over 2014-17, and 7 more
  than one per resident per year: repeat episodes, care-seeking across district lines or
  undercounted populations. I treat the rates as relative, not as true infection rates.
- Joining 2014-17 districts to today's boundaries: 43 match directly, 4 by spelling and 3 were
  later split, giving 53 polygons. 207 of today's 260 districts have no data. Bolga East and North
  East Gonja show as gaps although their cases sit inside Bolgatanga and East Gonja.
- The brief says the district file includes rainfall, temperature, elevation and distance to
  water. Ours has none of them, and neither does the data dictionary.
- The data dictionary names geoBoundaries as the boundary source, but our boundary files carry
  OCHA's COD-AB fields.

---

## 6. How I would answer the panel

Short answers that match the corrected analysis. The numbers behind them are in sections 2 and 3.

**Why a negative binomial, not OLS or Poisson?**
Counts are non-negative integers, so OLS has the wrong likelihood. A Poisson forces the variance to
equal the mean; ours is 77,183 times the mean, and with a population offset the dispersion ratio is
still 54,147. The negative binomial adds one dispersion parameter (α = 0.268) and improves AIC by
about 2.4 million.

**Why is a household-level bootstrap wrong for DHS data?**
The survey samples clusters, then households, and households in a cluster are alike. Resampling
households alone gives a rural Northern interval of 7.2 points; resampling clusters gives 15.2. A
design-based calculation agrees: a design effect of about 4.2 to 4.5.

**How do you know your results are not leakage?**
We built each leak deliberately. Preprocessing leakage is real in principle but negligible here.
Target encoding produced a fake R² of 1.00. For space, stratifying is not enough: holding out a
whole region raises the error about four times, so we do not claim the model generalises to regions
it has not seen.

**Why do Bolgatanga and Wa lose nets?**
Our rule moves nets towards Northern Region overall, and within their regions both report more
cases per person than average, which a population rule does not reward. Referral bias may
contribute, but it is a hypothesis: Bolgatanga is only 4th of 13 in its region on cases per person.

**Why does Tamale gain the most?**
It is the most populous district, and our rule treats everyone in a region as equally at risk. It
also reports the fewest cases per person of all 50 districts, so a case-based rule would give it
very little. That trade-off is a value judgement we make openly.

**Isn't your allocation just population within each region?**
Yes. Our coverage data are regional, so the model can only separate regions. We present it as a
universal-coverage allocation, close to how Ghana distributes nets, and show how the regional totals
change under other models.

**Why does the region with the highest coverage get the most nets per person?**
The coverage coefficient is positive, a confounded regional effect, and it outweighs the
coverage-gap term; Upper East also reports the most cases per person. A model with region effects
and coverage only in the gap term would be cleaner. It moves 7,720 nets.

**What if the budget is halved?**
Shares stay the same up to rounding, so every allocation roughly halves. The real sensitivity is the
model choice and the coverage data, not the budget.

**How do you get exactly 50,000 whole nets?**
Hamilton's largest-remainder method: each district gets the whole-number part of its share, then the
leftover nets go to the largest fractional remainders. One known quirk: raising the total can
occasionally cost a district a net (the Alabama paradox).

**What would you do with more time?**
Use today's regions and district-level spraying and chemoprevention, model risk with region effects,
validate by holding out regions, and borrow strength across neighbouring districts with a
small-area model for the survey.

---

## 7. My reflections

1. **The 45.5% came from one random seed. What will I check next time?** Before I quote a number
   now, I re-run it from a clean kernel and repeat any comparison over many seeds.
2. **The referral-hospital story came after we saw the allocation.** I now treat an explanation
   found after the result as a hypothesis, not a finding.
3. **Is allocating by population fair?** I think it is fair for now, because our data cannot tell
   districts in a region apart. But it can under-serve districts whose high rates are real, such
   as Nabdam (761 fewer nets), and it ignores the 207 districts with no data.
4. **How I used AI.** Gemini set up our repository and a methodology guide. Antigravity drafted
   notebooks 01, 03 and 04 and the reports. Claude (Code and chat) reviewed and fixed our work,
   helped with the deck and study aids, and drafted my reflection from this journal. I decided
   what to keep, edited the slides, merged the final deck and presented. My checks caught the
   errors in section 4.
5. **What I still do not understand.** I know a little and am still learning. I am still looking
   into small-area models, which borrow strength from neighbouring districts, and how to remove
   the confounding in our coverage coefficient, and working to understand them better each day.

---

## 8. Our team

Our seats and PBL roles, from our Notion roles table:

| Seat | Person | PBL role | Owns |
|---|---|---|---|
| Cartographer | Eric Sunu (me) | Chairperson | Maps and figures, the fresh-clone check |
| Statistician | Kobina | Steward | Distributions, model fitting, uncertainty |
| Pipeline engineer | Clifford | Secretary | Repo and environment, splits, preprocessing, the leakage audit |
| Analyst | Mubarak | Scribe | Framing, datasheet, allocation rule, ethics, claims table, deck assembly |

In practice the work moved between seats. From our git history: Mubarak built the Theme A
notebook (A1 to A4) with its schema checks and a plain-language guide, wrote the one-command
pipeline runner, added the per-capita check to notebook 02, and prepared the repository for
submission. A teammate merged our analysis pull request (#4), and a teammate suggested writing our
allocation rule as formulas on slide 9. Alongside my maps, I took on the leakage audit, the
allocation, the checks of our numbers and the deck.

To add: what Kobina and Clifford contributed.
