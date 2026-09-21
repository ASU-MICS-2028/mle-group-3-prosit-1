# Worklog

Shared record of who did what, when, and with which tools.

**Rules**

- Newest entry at the **top**, directly under this block.
- Append only. Never edit or delete someone else's entry. If an earlier entry
  turned out to be wrong, write a new one correcting it.
- One entry per working session where you changed anything in the repo.
- Write it **before you push**, not at the end of the week.
- If an AI assistant wrote or modified code that ended up in the repo, it goes
  in the `Assistant` field. This is what your individual AI declaration is
  built from.

**Template** — copy this block, fill it in, paste it at the top.

```markdown
## YYYY-MM-DD · HH:MM–HH:MM · Your name

**Branch:** feature/...
**Assistant:** none | Claude / ChatGPT / Copilot / other — and what you used it for
**Did:**
- ...
**Decided:**
- ...
**Blocked / open questions:**
- ...
**Next:**
- ...
```

Field notes:

- **Assistant** — be specific and honest. "Claude, to debug a statsmodels
  convergence error and to draft the docstrings" is useful. "Used AI" is not.
- **Decided** — only real decisions, the kind someone might otherwise reverse
  without knowing. Leave it out if nothing was decided.
- **Blocked** — this is the field that saves the project. Write it even when it
  feels like admitting you're stuck. Especially then.

---

## 2026-09-21 · 22:50–23:25 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Gemini (Gemini 3.8 Flash), to resolve open judgment decisions in `notebooks/02_distributions.ipynb` (Theme A), implement Northern Region domain override, generate `figures/a4_bootstrap_ci_comparison.png`, clear notebook outputs, and update `reports/claims_table.md` and `reports/LEARNING_JOURNAL.md`. No survey rows read or displayed.
**Did:**
- Set notebook owner to Eric Elikplim Sunu in `notebooks/02_distributions.ipynb`.
- Formulated plain-English and technical answer for Section A1 case-count distribution (cell `md12`), noting mass clustering between 40k-300k and right tail outliers (Bolgatanga, Wa).
- Justified and applied manual override in Section A4 (cell `md30` & `cd31`), replacing programmatic Accra selection with Northern Region (`hv024 = 12`, 20 rural clusters, 582 households) to anchor 50 surveillance districts.
- Formulated defensible claim for Section A4.1 (cell `md40`), establishing survey-weighted point estimate reproduction to within 0.09 percentage points of published DHS figure (67.69% vs 67.60%) while clarifying lack of published ITN CI.
- Executed notebook end-to-end to generate `figures/a4_bootstrap_ci_comparison.png` (cluster CI 15.2 pp vs naive 7.2 pp, DEFF = 4.50).
- Stripped notebook outputs cleanly via `jupyter nbconvert --clear-output`.
- Updated `reports/claims_table.md` (claims C-02, C-02b, C-02c, C-03 verified) and `reports/LEARNING_JOURNAL.md`.
**Decided:**
- Locked Northern Region (`hv024 = 12`) as the canonical rural uncertainty domain for Prosit 1, connecting survey uncertainty directly with surveillance districts and capturing DEFF = 4.50.
**Blocked / open questions:**
- Ready to begin Theme B1 geospatial exploration in `notebooks/01_eda.ipynb`.
**Next:**
- Commit Theme A updates to `feature/theme-a`, push to remote, and start Theme B1 (district and regional geospatial mapping).

## 2026-09-21 · 13:20–13:28 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Gemini (Gemini 3.8 Flash), to author `METHODOLOGY_GUIDE.md` translating the NLP 5-pillar learning and engineering methodology into the MLE context (Theme A/B/C/D, zero data leakage, spatial stratification, over-dispersion, cluster bootstrap, learning journal, and oral defense readiness). No survey rows read or displayed.
**Did:**
- Authored `METHODOLOGY_GUIDE.md` codifying the "Explain to a beginner, build like a senior" pedagogy, DHS survey cluster uncertainty, spatial leakage protection, negative binomial modeling, learning journal rituals, and viva defense Q&A.
**Decided:**
- Harmonized collaborative and reflective standards across both MICS 2028 coursework repositories (NLP Prosit 1 and MLE Prosit 1).
**Blocked / open questions:**
- None. Ready to proceed with Theme B tasks.
**Next:**
- Review Theme A decision points and commence Theme B1 spatial analysis.

---

## 2026-09-18 · 09:15–12:20 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Gemini (Gemini 3.8 Flash), to synchronize remote git changes, checkout `feature/theme-a`, populate `data/` from parent data package, install Python 3.11 via Homebrew, build `.venv`, install pinned requirements, register `prosit1` Jupyter kernel, and create `reports/LEARNING_JOURNAL.md` adopting the NLP reflective structure. No survey rows read or displayed.
**Did:**
- Fast-forwarded local `main` to `origin/main` (incorporating PR #2).
- Checked out and tracked `feature/theme-a` containing Theme A analysis by Tijani.
- Placed course data files from parent `../data/` into `data/` and verified git status remains clean via `.gitignore`.
- Installed `python@3.11` via Homebrew, created `.venv`, and installed all pinned requirements from `requirements.txt`.
- Registered Jupyter kernel `Python 3.11 (prosit1)`.
- Verified clean module imports across all `src/` modules.
- Created `reports/LEARNING_JOURNAL.md` documenting plain-English conceptual guides, empirical logs, data caveats, and viva defense answers.
**Decided:**
- Maintained a dedicated reflective learning journal (`reports/LEARNING_JOURNAL.md`) following the pattern of the NLP project to document intuition and viva readiness.
**Blocked / open questions:**
- Review the 4 "Your turn" open decisions in `notebooks/02_distributions.ipynb` before proceeding to Theme B.
**Next:**
- Review the "Your turn" cells in notebook 02, verify outputs, and begin Theme B1 (geospatial mapping in `01_eda.ipynb`).

## 2026-09-14 · 21:05–21:30 GMT · Eric Elikplim Sunu

**Branch:** feature/repo-setup
**Assistant:** Gemini (Gemini 3.8 Flash), to scaffold repository structure (`src/`, `notebooks/`, `reports/`, `figures/`), create `requirements.txt` with pinned versions, add `*.docx` and `*.xlsx` to `.gitignore`, and create stubs for pipeline modules and reports. No survey records or data files read.
**Did:**
- Added `*.docx` and `*.xlsx` to `.gitignore` to keep data dictionary source files and routine spreadsheets untracked.
- Created `requirements.txt` with pinned dependencies for Python 3.11 (numpy, pandas, scipy, scikit-learn, statsmodels, geopandas, matplotlib, seaborn, black, ruff, nbstripout, openpyxl).
- Scaffolded `src/` modules (`__init__.py`, `io.py`, `features.py`, `models.py`, `uncertainty.py`, `viz.py`).
- Implemented `src/io.py` with data loaders and the single authoritative `split_data()` function enforcing region stratification.
- Scaffolded notebook templates in `notebooks/` (`01_eda.ipynb`, `02_distributions.ipynb`, `03_pipeline_leakage.ipynb`, `04_allocation.ipynb`).
- Scaffolded report templates in `reports/` (`datasheet.md`, `leakage_audit.md`, `claims_table.md`).
- Added `.gitkeep` files in `data/` and `figures/`.
**Decided:**
- Preprocessing and feature engineering pipelines in `src/features.py` use `ColumnTransformer` and `Pipeline` exclusively to structurally prevent data leakage.
- Uncertainty estimation in `src/uncertainty.py` is configured as a two-stage cluster bootstrap (clusters sampled with replacement, then households sampled with replacement) to respect DHS survey design.
**Blocked / open questions:**
- Local system has Python 3.14 by default; Python 3.11 formula is available in Homebrew (`python@3.11`) and needs to be installed or set up in a virtual environment for testing.
**Next:**
- Review git staging, commit changes on `feature/repo-setup`, push and open a pull request into `main`.

## 2026-09-11 · 10:49–11:25 GMT · Eric Elikplim Sunu

**Branch:** feature/repo-setup
**Assistant:** Claude (Claude Code), to review README, RULES, CLAUDE.md and
data_dictionary.md for inconsistencies, and to write `.gitignore`. It read the
dictionary only, never files in `data/`.
**Did:**
- Added `.gitignore`: `data/*`, plus `*.csv` and `*.dta` anywhere, venv,
  caches, notebook checkpoints, `.DS_Store`
- Committed README, RULES, WORKLOG, CLAUDE.md and data_dictionary.md
**Decided:**
- `data_dictionary.md` is the canonical dictionary. The `.docx` stays out of
  git: same content, but it is missing the weighted vs unweighted bullet.
**Blocked / open questions:**
- The repo is public on GitHub. Confirm with the instructor that this is
  intended. Any data file committed by accident would be public immediately.
- Framing: the household survey has no district column. District data exists
  only for 50 districts in the three old northern regions (2014-17 routine
  surveillance). Proposal to discuss: allocate across the 16 regions from the
  2022 survey, then rank districts within the north. The README analysis
  paragraph (district intervals from the cluster bootstrap) needs revising
  either way.
- Dictionary discrepancies to verify when the data lands (aggregates only):
  the 26 old Northern districts all get region code 12, but some are now in
  Savannah or North East; `positive_per_100k` is not divided by
  `months_reported`; `has_net`/`num_nets` may count any net while the region
  file reports ITNs; the survey file is DHS 2022, not an MIS.
- No region population data in the package (DHS weights are normalised, so
  they cannot give totals). No strata column either.
- Not in the repo: the case brief (tasks A4, B1, B4, net supply size) and the
  `data_prep/` scripts.
**Next:**
- `requirements.txt` (the example entry below says it exists; it does not
  yet), `src/__init__.py` and module stubs, `data/.gitkeep`, `nbstripout`
- Open a PR for this branch and get one reviewer

## 2026-09-11 · 16:00–16:40 · [example entry — replace with your own]

**Branch:** main
**Assistant:** Claude, to draft the repo structure and this worklog format
**Did:**
- Created the repository, added `.gitignore` with `data/` excluded
- Set up `requirements.txt` with pinned versions
- Added `RULES.md` and this file
**Decided:**
- District ranking will use expected cases per capita, adjusted downward where
  the confidence interval is wide. Reason: the rubric rewards letting
  uncertainty drive a fair allocation rather than ranking on the mean alone.
- One notebook per theme, one owner per notebook, to avoid `.ipynb` merge
  conflicts.
**Blocked / open questions:**
- Real dataset not yet released. If it hasn't landed by Monday 09:00 we build
  against a synthetic stand-in with the same schema.
**Next:**
- Everyone clones and confirms `requirements.txt` installs cleanly on their
  machine before Monday.
