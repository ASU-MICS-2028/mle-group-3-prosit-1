# Team rules — Prosit 1 (ITN allocation)

Read this before your first commit. It exists so five people can work on one
repository for ten days without breaking each other's work.

If you disagree with a rule, raise it in the group chat and change it here.
Don't quietly ignore it.

---

## 1. Data handling

These are not style preferences. Breaking them can fail the submission.

- **The survey file never leaves this machine.** `data/` is in `.gitignore`.
  Never commit it, never attach it to a message, never upload it to a
  generative AI tool. This is stated in the case brief.
- **AI tools get the schema, not the rows.** You may paste `data_dictionary.md`,
  column names, dtypes, error messages, and your own code. You may not paste
  records, even a single head() output from the household survey.
- **District-level aggregates are fine to discuss.** The restriction is on the
  licensed household microdata.
- **Every number in the report cites a source.** If you can't say where a figure
  came from, it doesn't go in.

---

## 2. Repository layout

```
.
├── data/                  # gitignored. Never committed.
│   └── .gitkeep
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_distributions.ipynb
│   ├── 03_pipeline_leakage.ipynb
│   └── 04_allocation.ipynb
├── src/
│   ├── io.py              # loading, column contracts
│   ├── features.py        # transformers, encoders
│   ├── models.py          # Poisson / NB fitting
│   ├── uncertainty.py     # bootstrap
│   └── viz.py             # map and plot helpers
├── figures/               # exported PNG/SVG for slides
├── reports/
│   ├── datasheet.md
│   ├── leakage_audit.md
│   └── claims_table.md
├── WORKLOG.md
├── RULES.md
├── requirements.txt
└── README.md
```

One notebook per theme, one owner per notebook. Two people editing the same
`.ipynb` produces a merge conflict that is genuinely painful to resolve.

---

## 3. Git

- **Branch per task.** `feature/nb-fit`, `feature/gap-map`, `fix/split-strata`.
  Never commit directly to `main`.
- **Pull before you start working.** Every session, every time.
- **Small commits with real messages.** `fit negative binomial, add dispersion
  readout` — not `update`, not `stuff`.
- **One reviewer before merge.** It can be a two-minute look. The point is that
  a second person has seen every line that reaches `main`.
- **Clear notebook outputs before committing.** Run
  `jupyter nbconvert --clear-output --inplace notebooks/*.ipynb` or install
  `nbstripout`. Committed outputs create conflicts on every single merge and
  can leak data into git history.

---

## 4. Code conventions

- **Python 3.11.** Pin everything in `requirements.txt` with exact versions.
- **Formatting:** `black` for code, `ruff` for linting. Run both before you push.
  No debates about style; the tool decides.
- **`snake_case`** for variables and functions, `UPPER_CASE` for constants.
- **No magic numbers.** `RANDOM_SEED = 42` at the top of every module that
  randomises. Pass it explicitly to every split, bootstrap and model.
- **No absolute paths.** `Path(__file__).parent / "data"`, never
  `/home/kwame/Desktop/...`. This is the single most common reason a fresh
  clone fails.
- **Logic lives in `src/`, not in notebooks.** A notebook should read like a
  narrative: import, call, plot, comment. If a cell is longer than about
  twenty lines, it belongs in a module.
- **Docstrings on anything in `src/`.** One line on what it does, one on what it
  returns. That's enough.

---

## 5. Pipeline discipline

The two rules the grading rubric actually tests:

1. **Split first, fit second.** Nothing — no imputer, no scaler, no encoder —
   is fitted on data that includes the test set. Use
   `Pipeline` + `ColumnTransformer` so this is enforced by structure rather
   than by memory.
2. **Every modelling choice gets a sentence of justification** in the notebook
   next to it. "We stratified by region because rural districts are
   under-sampled and a random split can leave some regions absent from
   training."

---

## 6. Working with AI assistants

Everyone will use an assistant. That's allowed and the course expects it to be
declared. These rules keep it honest and keep the work coherent.

- **You own every line you commit.** If you can't explain a block to the panel,
  don't commit it. The panel asks.
- **Log the session.** Every time an assistant writes or changes code that ends
  up in the repo, add a `WORKLOG.md` entry before you push. This is not
  optional — see section 7.
- **Never paste survey rows into a prompt.** See section 1.
- **Prefer asking for an explanation over asking for a file.** "Why is my
  negative binomial dispersion parameter negative" teaches you something.
  "Write my notebook" does not, and it shows.
- **Keep your AI declaration notes as you go.** You each need one for the
  individual reflection. Reconstructing it on the last night is miserable and
  usually inaccurate.
- **Assistants disagree with each other.** If two people get contradictory
  advice on the same question, bring it to the group rather than letting two
  incompatible approaches land in `main`.

---

## 7. The worklog

`WORKLOG.md` is a single shared file. Every working session gets an entry,
whether or not an AI was involved.

**Why it exists.** Three reasons, in order of importance. It is the evidence
for your individual AI declarations. It stops two people silently solving the
same problem two different ways. And it gives the scribe the raw material for
the report without having to interview everybody.

**The rule:** append an entry at the end of any session where you changed
something in the repo. Newest entries go at the **top**. Do it before you
push, not at the end of the week.

**Append only.** Never edit or delete someone else's entry. If something was
wrong, write a new entry saying so.

Format and an example are in `WORKLOG.md` itself.

---

## 8. Meetings

- **Ten minutes, start of every working session.** What I did, what I'm doing,
  what's blocking me. That's it.
- **The secretary writes decisions down as they happen.** A decision that isn't
  written down gets re-argued three days later.
- **Blocked for more than two hours? Say so.** Silent struggling is the most
  expensive thing on a ten-day project.

---

## 9. Definition of done

A task is not done when the code runs on your laptop. It is done when:

- [ ] it runs from a clean kernel, top to bottom
- [ ] no absolute paths, no manual steps, no "just run this cell first"
- [ ] a second person has reviewed it
- [ ] every number it produces is traceable to a cell
- [ ] `WORKLOG.md` has the entry
- [ ] it's merged to `main`
