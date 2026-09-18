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

The project pins Python 3.11. If your machine has it:

```bash
git clone https://github.com/ASU-MICS-2028/mle-group-3-prosit-1.git
cd mle-group-3-prosit-1
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

If it does not (macOS ships 3.13, and `geopandas` has no 3.13 wheels), use conda:

```bash
conda create -n prosit1 python=3.11 -y && conda activate prosit1
pip install -r requirements.txt
python -m ipykernel install --user --name prosit1 --display-name "Python 3.11 (prosit1)"
```

`geopandas` is only needed from Theme B onward. If it fails to build, drop it
and install it later with `conda install -c conda-forge geopandas=0.14.4`.

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

## Current status

| Notebook | Theme | State |
| --- | --- | --- |
| `01_eda.ipynb` | B1 — geospatial EDA, data-gap map | Not started (Week 2 milestone) |
| `02_distributions.ipynb` | A1–A4 — distributions, sampling | **Runs end to end on real data** |
| `03_pipeline_leakage.ipynb` | B2–B4 — preprocessing, leakage audit | Not started |
| `04_allocation.ipynb` | Allocation rule, heatmaps | Not started |

Headline results from Theme A (all reproduce with `RANDOM_SEED = 42`):

- District positive counts are over-dispersed with **variance/mean ≈ 77,200**.
  A fitted Poisson implies sd 442 against an observed 122,882 — about 278x too
  narrow. Over-dispersion survives a log-population offset (Pearson chi2/df
  ≈ 54,100), so the negative binomial is the working model.
- The **cluster bootstrap interval is 1.8x wider** than a naive household
  bootstrap on the same statistic, implying a design effect near 3.3.
- Our survey-weighted estimate of regional net ownership reproduces the DHS
  published figure to **0.03 percentage points**, which validates the weighting
  (though not the interval — see below).

Open decisions are marked in the notebook as **"Your turn"** cells.

---

## Known data issues

Found while running Theme A. All belong in `reports/datasheet.md`; the first two
are discrepancies against the case brief and the data dictionary.

1. **No parasitaemia column and no district identifier** in
   `ghana_mis_sample.csv`. The brief describes both. The finest geography the
   survey supports is region (`hv024`) plus anonymised cluster, so A4 estimates
   net ownership for an under-sampled *region*, not prevalence for a district.
2. **The published ITN confidence intervals are empty.**
   `net_ownership_pct_ci_low/high` and `u5_itn_use_pct_ci_*` are present as
   columns but hold no values (0 of 76 rows). The data dictionary advertises
   them as the reference to check our bootstrap against. Prevalence CIs *are*
   populated (54 of 76), but we cannot bootstrap prevalence — see issue 1. The
   check does not close; we validate the point estimate instead.
3. **`net_coverage_pct` is region-level**, taking one value per region, so it is
   perfectly collinear with a region dummy and cannot enter a model alongside
   one. `src.models.check_design_matrix()` catches this before the fit. Its
   coefficient is a region effect, not a district net effect — do not report it
   as one. It is also measured in 2022 against case counts from 2014–17.
4. **`months_reported`, `year_start` and `year_end` are constant**, so they
   carry no information and are collinear with the intercept. The data
   dictionary flags `months_reported` for gap analysis in B1; that gap signal
   will have to come from somewhere else.
5. **`ghana_region_crosswalk.csv` is not in the course package.** It holds the
   `hv024` to COD `adm1_pcode` mapping that B1 needs to join survey regions to
   boundary polygons. It is public data; source it separately.
6. **District names do not join to the boundary files.** 43 of 50 match COD
   `adm2_name` after normalisation. The 7 that do not are mostly pre-2018
   amalgamated districts since split (Garu-Tempane, Savelugu-Nanton,
   Bunkpurugu-Yunyoo, Kasena-Nankana, Tatale-Sangule) plus two spelling
   variants. The boundaries are 2021 vintage; the surveillance is 2014–17. B1
   needs an explicit name-to-pcode crosswalk, and the unmatched districts are a
   reportable gap.

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

The numbers behind each of those claims are in
`notebooks/02_distributions.ipynb`, and every figure quoted in a report must
cite its notebook section in `reports/claims_table.md`.

---

## Conventions

See `RULES.md` for the full set. The short version:

- Branch per task, one reviewer before merge, never commit to `main` directly.
- Clear notebook outputs before committing.
- Fixed `RANDOM_SEED`, no absolute paths, logic in `src/` not in cells.
- Split before you fit. Nothing is fitted on data that includes the test set.
- Every working session gets a `WORKLOG.md` entry before you push.
