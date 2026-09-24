# Group learning journal: Prosit 1

ICS553 Machine Learning Essentials · MICS 2028 · Group 3 · Allocating insecticide-treated
nets (ITNs) in Ghana

For every member of the group. It explains the ideas behind our analysis in plain
language, lists the numbers we can quote and the ones we must stop using, records what went
wrong and how it was found, and helps with the panel and Quiz 1.

- Keep it current: replace a stale section rather than adding one that contradicts it.
- Personal journals go in `reports/journals/<your-name>.md`; a template is in section 8.
- Last updated 2026-09-24, after every notebook was re-run from a clean kernel and each
  number below was checked against the output.

---

## 1. The project in one paragraph

Ghana's malaria programme has a limited delivery of insecticide-treated nets. We advise
where 50,000 of them should go across the 50 districts of the three northern regions (as
they were in 2014-17), and how confident we can be. We have two sources: routine
surveillance (confirmed cases for those 50 districts, 2014-17) and the 2022 DHS household
survey (17,933 households in 618 clusters across all 16 regions, but no district
identifier). Case counts are over-dispersed, so we model them with a negative binomial;
survey intervals must respect the cluster design; and every step must be free of leakage.
Our current rule allocates within each region by population, with regional totals from the
model.

---

## 2. Key ideas in plain English

**Over-dispersion.** A Poisson model forces the variance to equal the mean. Our district
counts have a variance 77,183 times the mean, and even after adjusting for population the
Poisson dispersion ratio is 54,147 (it should be about 1). The negative binomial adds one
dispersion parameter (α = 0.268 with a population offset) and fits far better, so it is our
working model. The a3 figure shows α = 0.395 because it fits without covariates.

**Cluster sampling.** The DHS picks clusters, then households, and households in a cluster
are alike. Resampling households as if independent makes intervals too narrow: for rural
Northern net ownership the naive interval is 7.2 points wide and the cluster bootstrap
15.2, a design effect of about 4.5. A design-based calculation agrees (about 4.2).

**Weights.** Some areas were oversampled on purpose, so unweighted averages mislead:
national net ownership is 70.96% unweighted but 66.77% weighted. That gap is about
selection probabilities, not a design effect.

**Leakage.** Nothing fitted on test data may shape training.
- Preprocessing: fitting a scaler before splitting is a real leak, but its effect here is
  negligible.
- Target encoding: encoding each district by its own case count makes the feature the
  answer (test R² 1.00 against 0.26).
- Spatial: stratifying a split by region keeps every region in training, which is good for
  representation, but neighbours still sit on both sides of the split. Only holding out a
  whole region tests new geography, and it raises the error about four times.
- Temporal: coverage from 2022 cannot explain cases from 2014-17 causally.

**Confidence vs prediction intervals.** A confidence interval for the mean covers the
average count for districts like this one; a prediction interval covers one district's
actual count and is much wider. Our allocation uses the confidence interval for the mean.

**Confounding.** More nets go where malaria is worst, so coverage and cases rise together
across regions: our coverage coefficient is +0.082 per point. That is a region effect, not
evidence that nets increase malaria.

**What our allocation rule does.** Weight = upper confidence bound of expected cases × (1 -
coverage), turned into exactly 50,000 nets by Hamilton's largest-remainder method. Because
coverage is one number per region, the rule gives every district in a region the same nets
per person: 8.5 per 1,000 in Northern, 16.0 in Upper East, 9.2 in Upper West. That is close
to Ghana's own practice of allocating nets by population. The split between regions depends
on the model.

---

## 3. Numbers you can quote

Most rows come from notebook cells. Rows marked *script* come from `scripts/verify_claims.py`,
an independent re-computation that prints aggregates only (run it from the repo root).

| Claim | Number | Source |
|---|---|---|
| District counts are over-dispersed | Variance/mean 77,183 | nb02 cd09 |
| A Poisson is far too narrow | SD 442 vs 122,882 (278 times) | nb02 cd15 |
| Over-dispersion survives the population offset | Pearson χ²/df 54,147 | nb02 cd25 |
| The negative binomial fits better | α = 0.2677; AIC gap 2,393,669 | nb02 cd25, cd26 |
| Weighting matters | 70.96% unweighted vs 66.77% weighted | nb01 eda_cd05 |
| The cluster design widens intervals | 15.20 vs 7.17 points (2.12 times); DEFF 4.50 at seed 42 | nb02 cd34 |
| The design effect is stable | 4.46 to 5.39 over 20 seeds; 4.18 design-based | script, section A |
| Our weighting reproduces the DHS | 67.69% vs 67.6% published (0.09 points) | nb02 cd39 |
| Target encoding leaks | Test R² 1.0000 vs 0.2618 | nb03 leak_cd06 |
| Holding out a region | RMSE 365,128, about four times a random or stratified split | nb03 leak_cd14 |
| Allocation by region | Northern 24,196, Upper East 18,631, Upper West 7,173 | nb04 alloc_cd07 |
| Nets per 1,000 people | 8.5 / 16.0 / 9.2 | nb04 alloc_cd11 |
| The regional split is model-dependent | A region-effects model moves 7,720 nets | nb04 alloc_cd13 |
| Coverage data error matters | Correcting 11 districts' coverage moves 3,740 nets | nb04 alloc_cd13 |

---

## 4. Numbers and claims to stop using

These appear in our reports or the old deck but are wrong, not reproducible, or
overstated.

| Stop saying | Say instead | Why |
|---|---|---|
| Honest test R² 0.49 | 0.26 | 0.49 does not reproduce from the notebook |
| Random splits understate error by 45.5% | Holding out a region raises error about four times; random and stratified splits agree | 45.5% came from one random seed |
| Region-stratified splits prevent spatial leakage | Stratifying ensures representation; holding out regions tests new geography | Neighbours stay on both sides of a stratified split |
| Preprocessing leakage deflates error by 212 cases | The mechanism is real; here the effect is negligible (44 cases on average over 500 seeds) | 212 was one seed |
| Upper bound of the 95% prediction interval | Upper bound of the 95% confidence interval for the mean | That is what the code computes |
| Depot totals 24,980 / 17,547 / 7,473 | 24,196 / 18,631 / 7,173 | Sums of our own schedule |
| Schedule total 5,263,334 people, 9,781,209 cases | 4,788,809 and 9,781,981 | Column sums of `reports/allocation.md` |
| The interval extends down to 60.1% | The all-Northern cluster interval is 61.4% to 74.0% | No cell produces 60.1% |
| Lower Northern coverage justifies more nets for Northern | Under our model it gives Northern fewer nets | The coverage coefficient is positive |
| Wa and Bolgatanga have about 80% coverage | Upper East 79.6%, Upper West 69.8% (regional averages) | Coverage is regional |
| Referral hospitals inflate Wa and Bolgatanga | This is a hypothesis; our data do not show it | Bolgatanga is 4th of 13 in its region on cases per person |
| Bolgatanga and Wa host tertiary hospitals | They host regional (secondary) hospitals; Tamale Teaching Hospital is the only tertiary hospital in the north (web) | Ghana's health-system tiers |
| Case-proportional allocation is the status quo | Ghana allocates ITNs by population, about one net per two people (web) | National malaria strategy |
| Rural Northern is the most under-sampled region | It was chosen for its link to our districts; it ranks 10th of 16 by rural clusters | nb02 cd29 |
| The weighting gap is a design effect | It comes from unequal selection probabilities | A design effect is a variance ratio |
| 1.8 times wider, DEFF 3.3, 0.03 points | 2.12 times, DEFF 4.50, 0.09 points | The old numbers are from the Greater Accra domain; only `reports/theme_a_guide.pdf` still shows them |

(web): from a web check on 2026-09-22 (Tamale Teaching Hospital's own site; the Ghana
Service Provision Assessment 2002; the PMI Ghana Malaria Operational Plan FY2017). Open the
source before quoting it.

---

## 5. Data caveats

- The survey has no parasitaemia column and no district identifier; it resolves only to
  region and cluster.
- The published ITN confidence intervals are empty (0 of 76 rows).
- `net_coverage_pct` is one value per region (67.69, 79.56, 69.76) and measured in 2022,
  five to eight years after the cases.
- 11 districts coded as Northern are now in Savannah (6) or North East (5), where 2022
  coverage is 79.1% and 62.8%, not 67.7%.
- The raw surveillance workbook records indoor spraying (IRS) and seasonal chemoprevention
  (SMC) by district and month; the curated file dropped them. 32 of 50 districts had
  spraying and 24 had chemoprevention in 2014-17.
- 39 of 50 districts report more than one confirmed case per resident over 2014-17, which
  suggests repeat episodes, care-seeking across districts or undercounted populations.
- 207 of today's 260 districts have no surveillance data in our package.

---

## 6. Lessons for the rest of the course

1. One random seed is an anecdote. Report the spread over seeds before calling a difference
   real.
2. Every number in prose should be printed by a cell. Hand-typed numbers drifted in this
   project (the R², the depot totals, the 60.1%).
3. Stratify to keep every group in training; hold groups out to test generalisation. They
   answer different questions.
4. Check a coefficient's sign before building on it. A positive coverage coefficient was
   the warning sign here.
5. An explanation written after seeing a result is a hypothesis. Show the evidence for and
   against it.
6. Check the vintage of codes and boundaries. Ghana's regions changed in 2019; our district
   file did not.
7. Do not drop columns silently. The spraying and chemoprevention status was in the raw
   workbook all along.
8. Re-run from a clean kernel before quoting anything, and update the claims table in the
   same commit.

---

## 7. Panel and Quiz 1 practice

**Why a negative binomial and not a Poisson?** The variance is 77,183 times the mean, and
the dispersion ratio is still 54,147 after a population offset; a Poisson cannot fit that.
The negative binomial adds one dispersion parameter.

**Why resample clusters, not households?** Households in a cluster are alike, so treating
them as independent overstates what we know. The cluster interval is 2.12 times wider.

**What does a design effect of 4.5 mean?** The survey carries the information of a simple
random sample about a quarter its size.

**What does the 0.09-point match with the DHS validate?** Our weighting and coding, not our
interval: the published ITN intervals are empty.

**Does stratifying by region stop spatial leakage?** No. It keeps each region represented,
but only holding out a whole region tests new geography.

**Why does Tamale gain the most nets?** It is the most populous district, and within a
region the rule treats everyone as equally at risk, even though Tamale reports the fewest
cases per person.

**Why do Bolgatanga and Wa lose nets?** The rule moves nets towards Northern Region overall,
and both districts report more cases per person than their regional averages. Referral bias
is a possible extra reason, not a finding.

**What is the weakest part of the analysis?** The split between regions: coverage is one
2022 number per region, its coefficient is confounded, and a better-fitting model moves
7,720 nets.

**How do you get exactly 50,000 nets?** Hamilton's largest-remainder method: whole-number
parts first, then the leftovers to the largest remainders.

**What would you do with more time?** Use today's regions and district-level spraying and
chemoprevention, model risk with region effects, validate by holding out regions, and
borrow strength across neighbouring districts with a small-area model.

---

## 8. Template for your personal journal

Copy this into `reports/journals/<your-name>.md` and write it in your own words; it feeds
your individual reflection and AI-use declaration.

```markdown
# Learning journal: <your name>

Role: <seat and PBL role> · Last updated: <date>

## What I worked on

## Concepts I can now explain in my own words

## One thing that went wrong, and how it was found

## How I used AI assistants, and what I checked (for my declaration)

## Questions I still have
```
