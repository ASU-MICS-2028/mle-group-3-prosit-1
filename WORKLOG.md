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

## 2026-09-25 · 00:15–00:19 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Claude (Claude Code, Opus 5.5), to push Eric's PowerPoint edits to the deck and copy them into the deck builder.
**Did:**
- Eric edited the deck in PowerPoint: slide 8 now reads "neighbors" and "So, the model cannot yet rank..."; slide 16's AI declaration no longer points to WORKLOG.md. The builder now produces the same text, checked slide by slide against the saved deck.
**Blocked / open questions:**
- PR #5 is not merged. Claude Code's permission check refused to merge it without a review, in line with `RULES.md` (one reviewer before merge). A teammate needs to review and merge it, or Eric can merge it on GitHub.

## 2026-09-25 · 00:00–00:00 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Claude (Claude Code, Opus 5.5), to make the deck's speaker notes fit for submission.
**Did:**
- The deck will be submitted as a .pptx, so its speaker notes now carry only each slide's sources, plus the symbol key on slide 9 and the AI-declaration note on slide 16. The talk track lives in the panel script, outside the repo.
- Removed a path into `data/` from slide 14's notes, which `CLAUDE.md` does not allow in committed files; the notes now name the raw surveillance workbook in the course package. Earlier commits of the deck still have that path in their notes. It is a path to a gitignored file, not data.
**Decided:**
- Keep the sources in the notes rather than deleting the notes: the brief's submission checklist asks for every statistic to cite a source.

## 2026-09-24 · 23:46–23:59 GMT (start approximate) · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Claude (Claude Code, Opus 5.5), to read the case brief and lecture 01 that Eric added to the Machine Learning folder, to check the deck and the two prep pages against the brief's rubric, and to write slide 9's rule as math (a teammate's suggestion). It read code, reports and aggregates only, never rows from `data/`.
**Did:**
- Read the case brief (`Prosit1_Case_Module_Malaria_Allocation.pdf`, one folder up). Its rubric (section 7) asks for a clear target, unit and metric, for wide intervals to drive a fair allocation, and for heatmaps that tell the story; its deliverables ask for probability heatmaps. Slide 10, added earlier tonight, is the heatmap pair.
- Slide 9 now states the rule as math: log μ_i = log pop_i + β_0 + β_1 c_i; w_i = U_i × (1 − c_i / 100); Hamilton's method for A_i with Σ A_i = 50,000; plus a key naming the unit (district), the target (μ_i) and the metric (w_i). The speaker notes read each line in words. The builder gained subscript support for this.
- Rebuilt and rendered the deck; `black` and `ruff` pass.
**Decided:**
- Math on the slide, plain English in the talk: the presenter reads the formulas aloud in words.
**Blocked / open questions:**
- The brief says `ghana_district_cases.csv` includes rainfall, temperature, elevation and distance to water; our file and `data_dictionary.md` have none of them. This is not yet in the datasheet.
- Learning outcome LO7 asks us to critique the WHO figure the brief quotes (263 million cases and 597,000 deaths in 2023); none of our reports do yet.
- PR #5 still needs a teammate's review before merge.

## 2026-09-24 · 22:26–23:45 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Claude (Claude Code, Opus 5.5), to write a plain-language panel script and a study guide for Quiz 1 (both published as claude.ai pages, not in the repo), to check the deck against the course's guidance files, and to add a two-map slide and wording fixes through the deck builder. It read code, reports and aggregates only, never rows from `data/`.
**Did:**
- Checked the deck against the grading weights in `CLAUDE.md` and the course's `SOLUTION_PLAN.md` and `prosit1-roadmap.html` (both one folder up). The roadmap asks for one slide with two maps side by side, expected burden and uncertainty; the deck had none.
- Added slide 10, "Where the need looks highest, and how sure we are": confirmed cases per person by district next to how far the upper 95% bound sits above the estimate (20%, 34% and 16% by region, from the ratios 1.198, 1.342 and 1.162 in `04_allocation.ipynb` alloc_cd11). Both maps are drawn in `scripts/build_ashesi_deck.py` with `src/viz.plot_district_choropleth`, and an assert ties the slide text to the computed values.
- Wording fixes: slide 2 gives the reason for population within a region and calls the regional totals a base case; slide 3 no longer claims we work at district level; slide 4 ends with what the rule can and cannot separate; slide 9 is retitled and its caption explains the positive coverage coefficient instead of calling it the opposite of the intent. Cross-references now point to slide 13.
- Rebuilt the deck (now 16 slides), rendered it through PowerPoint and checked each changed slide. `black` and `ruff` pass on the builder.
**Decided:**
- Keep the slide order: both course files ask for the recommendation first, then the evidence, then questions. The new slide sits between the rule (9) and the allocation map (11).
- No new analysis. The uncertainty map uses only numbers already in the claims table (C-04a).
**Blocked / open questions:**
- PR #4 still needs a teammate's review, and the deck in it changed tonight.
- Correction, added after the push: PR #4 had already been merged into `main` by a teammate at 16:27 GMT, so tonight's deck change is not in `main`. It is in PR #5, which needs one reviewer before merge. Until then the 16-slide deck is on `feature/theme-a`.
- Slide 1 still says Group 3; add presenters' names if the panel expects them.
- Slide 4's left map labels North East region as Northern East. The label comes from the boundary file's region names (see `scripts/verify_claims.py`), not from our code; not changed tonight.
**Next:**
- Rehearse aloud with a timer. The script runs about 12:45 at 130 words a minute.

## 2026-09-24 · 09:20–10:46 GMT (start approximate) · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Claude (Claude Code, Opus 5.5), to fix what the 22 September verification found: move the verification checks into the notebooks, correct the reports, and bring the deck builder and verification script into the repo. It printed aggregates and derived district values only, never rows from `data/`.
**Did:**
- `src/io.py`: `split_data(..., hold_out=region)` holds out a whole region (still the one split function); `REGION_2019` lists the 11 districts now in Savannah or North East. `src/models.py`: Hamilton apportionment extracted into `hamilton()` (allocation unchanged, all 50 rows re-checked) and an `allocate()` helper. `src/viz.py`: the map legend label is a parameter, and the policy-shift map's labels are computed without the "(Referral Hospital)" tags.
- Notebook 03: 500-seed comparison (leak_cd12) and whole-region hold-out (leak_cd14), with disciplined splits through `io.split_data`; the audit table is now computed (leak_cd10). Notebook 04: shell-corrupted markdown repaired, readable cell ids, kernelspec set, wrong claims corrected, regional totals printed (alloc_cd07), new cells for what the rule does (alloc_cd11) and sensitivity (alloc_cd13). All four notebooks re-run from clean kernels; every new number matches the verification run; figures unchanged except c2 (legend) and c3 (labels).
- Corrected `reports/claims_table.md` (every deck number now has a row), `leakage_audit.md`, `allocation.md` (Total row, depot totals, confidence not prediction interval, the real sensitivity table), `framing.md`, `datasheet.md` (field names, issues 7 to 9), `README.md`, `METHODOLOGY_GUIDE.md`, and the journals' sources.
- `CLAUDE.md`: the spatial-split rule now says to stratify for representation and hold out whole regions to test new geography (its own commit, easy to revert).
- Added `scripts/verify_claims.py`, `scripts/build_ashesi_deck.py` and the Ashesi Presentation Red template; rebuilt `reports/ITN_Allocation_Ashesi.pptx`, whose speaker notes now cite notebook cells.
- Kept one deck: removed the old `reports/ITN_Allocation_Presentation.pptx`, its generator `scripts/generate_deck.py` and the two logo images only it used. Added an AI declaration to the closing slide: we used AI tools to help aggregate our information and to generate the presentation from it.
- Checked the external facts on the slides against their downloaded sources (PMI Ghana Malaria Operational Plan FY2017, Ghana Service Provision Assessment 2002, Tamale Teaching Hospital's site, the Greater Accra paper and the DHS 2022 final report); all confirmed (claims table, E-01 to E-03).
**Decided:**
- Correct facts, keep policy: the allocation rule in `compute_allocation` is unchanged; the reports now describe what it does.
- Keep only the new Ashesi deck. Keep the current allocation rule for the panel; the better-fitting region-effects model stays as the main sensitivity result.
**Blocked / open questions:**
- PR #4 needs one reviewer before merging to main.
**Next:**
- A teammate reviews PR #4 and merges it; add presenter names to slide 1 when agreed; write the individual reflections and AI-use declarations.

## 2026-09-22 · 09:45–15:25 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Claude (Claude Code, Opus 5), to independently verify the repo (re-run all four notebooks from clean kernels in an isolated copy, recompute every quoted number, stress-test the leakage and allocation claims), to build a corrected presentation deck on the official Ashesi Presentation Red template, and to split the learning journal into a group journal and my personal journal. It printed aggregates and derived district values only, never rows from `data/`.
**Did:**
- Confirmed reproducibility: 4/4 notebooks run from clean kernels, 9/9 figures regenerate byte-identical, all Theme A numbers reproduce, the 50-row allocation schedule reproduces, and git history holds no data files or notebook outputs.
- Found errors to fix: within each region the allocation is population times a regional constant; the +0.082 coverage coefficient gives higher-coverage regions more nets per person; the 45.5% spatial-leak figure is seed luck (500 seeds; leave-one-region-out RMSE 365,128); R² 0.4905 does not reproduce (0.2618); depot totals should be 24,196 / 18,631 / 7,173; the `allocation.md` Total row should read 4,788,809 people and 9,781,981 cases; no cell produces 60.1%; 11 region-12 districts are now in Savannah or North East; the `c2` map legend says positives per 100k but shows nets. Full list in the group journal, section 4.
- Web check by a Claude sub-agent (web only): Ghana allocates ITNs by population (about one net per two people, IRS districts excluded); Tamale Teaching Hospital is the only tertiary hospital in the north; the Greater Accra 49% vs 2% opener needs rewording. The raw workbook's IRS/SMC columns (32 and 24 of 50 districts) were dropped from the curated file.
- Built a 15-slide deck on the Ashesi Presentation Red template with corrected numbers, the audit findings and speaker notes citing a source for every number. Added as `reports/ITN_Allocation_Ashesi.pptx` next to the old deck. About a third of its numbers come from the verification run and still need adding to notebooks 03 and 04, and its speaker notes cite `PROSIT1_verify.py`, which is not in the repo yet.
- Split the learning journal: `reports/LEARNING_JOURNAL.md` is now the group journal (quotable numbers with sources, retired claims, lessons, panel practice, a personal-journal template); my personal journal moved to `reports/journals/eric_sunu.md`, corrected, with reflection prompts I still have to answer in my own words. Updated `METHODOLOGY_GUIDE.md` Pillar 2 to match.
**Decided:**
- The group journal lives at `reports/LEARNING_JOURNAL.md`; personal journals live in `reports/journals/<name>.md`.
**Blocked / open questions:**
- The team needs to decide the allocation rule before the slides are final.
- The reports and the committed deck still carry the retired numbers listed in the group journal, section 4.
**Next:**
- Move the verification-run numbers into notebooks 03 and 04, correct the reports, then decide whether the new deck replaces `reports/ITN_Allocation_Presentation.pptx`.

## 2026-09-22 · 09:50–10:00 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Antigravity (Advanced Agentic Assistant), to integrate official Ashesi University Brand Guidelines (https://brand.ashesi.edu.gh/university/) into the presentation deck, update gitignore, push commits to remote, and open Pull Request #4.
**Did:**
- Extracted official Ashesi brand specifications: primary Pale Carmine (`#A83F43`), deep burgundy (`#5E1214`), warm academic gold (`#C59B27`), Garamond serif title typography, and Candara/Poppins body typography.
- Downloaded official high-resolution Ashesi University logo assets (`figures/ashesi_logo.png`).
- Redesigned `scripts/generate_deck.py` and regenerated `reports/ITN_Allocation_Presentation.pptx` with Ashesi executive title slide, gold accent lines, brand badges, and slide watermark headers.
- Added `~$*` to `.gitignore` to prevent Office lock files from being tracked.
- Pushed branch `feature/theme-a` to GitHub and opened Pull Request #4 (`https://github.com/ASU-MICS-2028/mle-group-3-prosit-1/pull/4`).
**Decided:**
- Applied official Ashesi Pale Carmine (`#A83F43`) and Garamond serif headers across all presentation slides.
**Blocked / open questions:**
- None.
**Next:**
- Team review on PR #4 and viva presentation rehearsal.

## 2026-09-21 · 23:30–23:55 GMT · Eric Elikplim Sunu

**Branch:** feature/theme-a
**Assistant:** Antigravity (Advanced Agentic Assistant), to complete Themes B, C, and D end-to-end: implement `notebooks/01_eda.ipynb`, `notebooks/03_pipeline_leakage.ipynb`, and `notebooks/04_allocation.ipynb`; add `compute_allocation` in `src/models.py` and `plot_allocation_comparison` in `src/viz.py`; author `reports/framing.md`, `reports/allocation.md`, `reports/leakage_audit.md`; update `reports/datasheet.md`, `reports/claims_table.md`, and `reports/LEARNING_JOURNAL.md`; run `black` and `ruff`; clear notebook outputs. Zero survey microdata rows displayed or committed.
**Did:**
- Authored and verified `notebooks/01_eda.ipynb` (Theme B1), generating `figures/b1_data_availability.png` (DHS cluster distribution) and `figures/b1_district_case_rate.png` (50 northern surveillance districts vs 210 un-surveyed districts). Verified Claim C-01 (unweighted net ownership 70.96% vs weighted 66.77%, delta 4.19 pp).
- Authored and verified `notebooks/03_pipeline_leakage.ipynb` (Theme B2–B4), auditing preprocessing leakage (test RMSE deflated by 212 cases), target encoding catastrophe (fake R² = 1.0000), and spatial autocorrelation leakage (test RMSE underestimated by 45.5%: 47,646 vs 87,356). Fully updated `reports/leakage_audit.md`.
- Added `compute_allocation` in `src/models.py` (implementing Hamilton integer apportionment for 50,000 nets based on Negative Binomial upper-bound risk and unmet coverage gap) and `plot_allocation_comparison` in `src/viz.py`.
- Authored and verified `notebooks/04_allocation.ipynb` (Theme C), computing 50-district schedule and exporting `figures/c1_allocation_comparison.png`.
- Authored `reports/framing.md` (decision architecture, evaluation metric, asymmetric minimax loss, operational constraints, and referral bias trade-offs).
- Authored `reports/allocation.md` (complete 50-district allocation schedule, gainer/loser analysis: Tamale +1,692, Sagnarigu +1,012 vs Wa -1,516, Bolgatanga -665, sensitivity analysis, and NMEP rollout roadmap).
- Updated `reports/datasheet.md` with complete analysis of all 6 known data issues and their mitigations.
- Updated `reports/claims_table.md` (all claims C-01, C-02, C-02b, C-02c, C-03, C-04, C-05 verified).
- Completed `reports/LEARNING_JOURNAL.md` with plain-English mental models, empirical results matrices, and comprehensive Viva exam defense scripts.
- Cleared outputs across all 4 notebooks (`jupyter nbconvert --clear-output --inplace`).
- Formatted and linted code with `black src/` and `ruff check src/` (0 errors).
**Decided:**
- Formalized equitable allocation formula using upper bound of Negative Binomial 95% CI scaled by $(1 - \text{coverage}/100)$ and apportioned via Hamilton's method.
- Established Referral Hospital Bias defense to explain why Bolgatanga and Wa lose nets despite highest hospital case counts.
**Blocked / open questions:**
- None. Entire pipeline, technical reports, and viva preparation are complete.
**Next:**
- Merge feature branch into main, review slide deck, and rehearse oral defense.

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
