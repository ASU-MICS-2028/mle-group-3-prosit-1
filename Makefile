# Prosit 1 — one command runs the whole analysis.
#
#   make            run the pipeline end to end
#   make pipeline   same thing, named
#   make deck       run the pipeline and rebuild the presentation
#   make verify     re-check quoted numbers without re-running notebooks
#   make lint       black + ruff over src/ and scripts/
#   make strip      strip notebook outputs before committing
#   make clean      remove build/ and caches

PY := python3

.DEFAULT_GOAL := pipeline
.PHONY: pipeline deck verify lint strip clean setup

pipeline:
	$(PY) scripts/run_pipeline.py

deck:
	$(PY) scripts/run_pipeline.py --deck

verify:
	$(PY) scripts/verify_claims.py

lint:
	black src/ scripts/ && ruff check src/ scripts/

strip:
	jupyter nbconvert --clear-output --inplace notebooks/*.ipynb

clean:
	rm -rf build/ .ruff_cache/
	find . -name __pycache__ -type d -prune -exec rm -rf {} +

setup:
	$(PY) -m pip install -r requirements.txt
