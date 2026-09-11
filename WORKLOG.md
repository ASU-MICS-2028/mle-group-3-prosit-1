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
