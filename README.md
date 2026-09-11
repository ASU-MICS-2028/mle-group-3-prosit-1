# Prosit 1 — Data-driven allocation of insecticide-treated nets in Ghana

ICS553 Machine Learning Essentials · MICS 2028 · Group 3

**The question.** Where should Ghana's limited supply of insecticide-treated
nets go, and how confident can we be in the district-level malaria estimates
behind that decision?

We are acting as an analytics consultancy advising the National Malaria
Elimination Programme's allocation committee. The deliverable is a defensible
ranking of districts, with an honest account of what we don't know.

---

## ⚠️ Data rules — read before your first commit

The household survey (`ghana_mis_sample.csv`) is **licensed health data**.

- `data/` is gitignored. Never commit its contents.
- Never paste survey rows into any AI assistant — not one row, not to debug a
  parsing error. Share column names, dtypes and the error message instead.
- District-level aggregates are fine to discuss and share.

If a data file is ever committed by accident, **stop and tell the group**. It
stays in git history after deletion and removing it properly means rewriting
history for everyone.

---

## Setup

```bash
git clone https://github.com/ASU-MICS-2028/mle-group-3-prosit-1.git
cd mle-group-3-prosit-1
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Place the course data package in `data/`. Then confirm it is ignored:

```bash
git status   # no CSVs should appear
```

Run the notebooks in numerical order. Everything must work from a fresh clone
with no manual steps.

---

## Layout

```
data/         gitignored — never committed
notebooks/    01_eda, 02_distributions, 03_pipeline_leakage, 04_allocation
src/          shared logic: io, features, models, uncertainty, viz
figures/      exported figures for the deck
reports/      datasheet, leakage audit, allocation, claims table
```

One notebook per theme, one owner per notebook. Two people editing the same
`.ipynb` produces merge conflicts that are painful to resolve by hand.

---

## Who owns what

| Seat | Owns |
| --- | --- |
| Statistician | Distributions, model fitting, uncertainty |
| Pipeline engineer | Repo and environment, splits, preprocessing, leakage audit |
| Cartographer | Maps and figures, fresh-clone reproducibility check |
| Analyst | Framing, datasheet, allocation rule, ethics, claims table |

On top of these, each person holds one PBL role: chairperson, secretary,
scribe, steward. Rotate both for Prosit 2.

Full role detail, task board and decisions log live in the team Notion hub.

---

## What we are producing

1. **A reproducible notebook pipeline** — cleaning through to the leakage audit.
2. **A resource allocation proposal** — 15-minute presentation to a mock
   Ministry of Health panel, with probability heatmaps.
3. **One individual reflection per person**, including the AI-use declaration.
   Required to pass.

---

## The analysis in one paragraph

District case counts are over-dispersed, so a Poisson under-fits the
high-burden tail and a negative binomial fits better. The household survey is a
cluster sample, so confidence intervals must come from a bootstrap that
resamples clusters rather than households — resampling households pretends the
design was simple random sampling and produces intervals that are too narrow.
Under-sampled rural and border districts therefore carry wide intervals, and
our allocation rule uses that uncertainty rather than ranking on the point
estimate alone.

---

## Conventions

See `RULES.md` for the full set. The short version:

- Branch per task, one reviewer before merge, never commit to `main` directly.
- Clear notebook outputs before committing.
- Fixed `RANDOM_SEED`, no absolute paths, logic in `src/` not in cells.
- Split before you fit. Nothing is fitted on data that includes the test set.
- Every working session gets a `WORKLOG.md` entry before you push.
