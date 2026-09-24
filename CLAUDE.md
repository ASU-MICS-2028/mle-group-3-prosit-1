# Project context

Coursework project: recommending how to allocate a limited delivery of
insecticide-treated nets across Ghana's districts, with honest uncertainty.
ICS553, group of four, three-week deadline. Graded on statistical rigour (25%),
pipeline and leakage handling (25%), equity and ethics (20%), framing (15%) and
communication (15%).

We are students. Prefer explaining the reasoning over producing finished code
we can't defend — a panel will ask us to justify any number on any slide.

## Absolute constraints

- **Never read, print, echo, or otherwise surface rows from `data/`.** It holds
  licensed household health data. You may read `data_dictionary.md`, inspect
  column names and dtypes, and report aggregate counts. Do not display record
  contents, not even `.head()` output, and not to diagnose a parsing error.
- **Never write to `data/`** or suggest committing anything from it. If you see
  a data file staged in git, stop and say so.
- Do not add a data file path to any example, test fixture, or docstring in a
  way that would end up in the repo.

## The leakage rule, which this project is graded on

Split first, fit second. No imputer, scaler, or encoder is ever fitted on data
that includes the test set. Use `Pipeline` + `ColumnTransformer` so the
structure enforces it rather than our memory.

Two things that look fine and are not:

- **Target encoding** uses the outcome to build a feature. Don't suggest it as
  a default. It appears in this repo only inside the deliberately-broken
  comparison in the leakage audit, clearly labelled.
- **Random row-wise splits leak through geography.** Districts are spatially
  autocorrelated — a district and its neighbour share rainfall, elevation and
  transmission conditions. Stratify splits by region so every region is in
  training, and flag `train_test_split` called without a stratification
  argument. Stratifying does not stop this leak, though: neighbours still land
  on both sides. To test generalisation to new geography, hold out whole
  regions with `split_data(..., hold_out=region)`.

`src/io.py` owns the one split function. Import it; never write a second one.

## Statistical conventions

- Count data here is over-dispersed. Poisson is fitted to demonstrate its
  failure, not as a candidate model. Negative binomial is the working model.
- Confidence intervals for survey-derived quantities come from a **cluster**
  bootstrap: resample clusters with replacement, then households within the
  drawn clusters. A household-level bootstrap is wrong here and produces
  intervals that are too narrow. If we ask for "a bootstrap", assume cluster
  unless we say otherwise.
- `RANDOM_SEED` is defined once and passed explicitly to every split, bootstrap
  and model. No unseeded randomness.

## Code conventions

- Python 3.11. `black` and `ruff`, no style debates.
- No absolute paths, ever. `Path(__file__).parent` and relatives only — the
  repo must run from a fresh clone on a machine that has never seen it.
- Analysis logic lives in `src/`. Notebooks read like a narrative: import,
  call, plot, comment. A cell longer than ~20 lines belongs in a module.
- Notebook outputs are stripped before commit.
- Every statistic that reaches a report cites a source.

## Working style we want from you

- When you make a modelling choice, write the one-sentence justification into
  the notebook next to it. The rubric rewards the reasoning, not the output.
- Prefer the simple approach the brief allows. Mean or median imputation is
  explicitly fine. Don't reach for a sophisticated method we'd have to defend.
- If something we ask for would introduce a leak, say so before doing it.
- Don't silently work around a discrepancy between the data and the data
  dictionary. Surface it — a documented discrepancy is a finding we can report.

## Housekeeping

After a working session that changed the repo, remind us to add a `WORKLOG.md`
entry at the top: branch, which assistant was used and for what, what changed,
decisions made, blockers. It is the evidence for our individual AI-use
declarations, which are required to pass.

Full team rules are in `RULES.md`.
