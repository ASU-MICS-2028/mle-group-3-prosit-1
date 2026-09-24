#!/usr/bin/env python3
"""Run the whole analysis end to end, in order, with one command.

    python scripts/run_pipeline.py

Executes the four notebooks in sequence, then re-checks every quoted number
with verify_claims.py. Stops at the first failure and says which cell broke.

Executed copies land in build/ (gitignored) so the committed notebooks keep
their stripped outputs. Pass --inplace to keep outputs in the notebooks
themselves when you want to read them; strip them again before committing.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = [
    ("01_eda.ipynb", "B1  geospatial EDA and data-gap maps"),
    ("02_distributions.ipynb", "A1-A4  distributions, Poisson vs NB, cluster bootstrap"),
    ("03_pipeline_leakage.ipynb", "B2-B4  preprocessing and the leakage audit"),
    ("04_allocation.ipynb", "C  allocation rule, sensitivity, maps"),
]
REQUIRED_IMPORTS = [
    ("numpy", "numpy"), ("pandas", "pandas"), ("scipy", "scipy"),
    ("sklearn", "scikit-learn"), ("statsmodels", "statsmodels"),
    ("matplotlib", "matplotlib"), ("geopandas", "geopandas"),
]
REQUIRED_DATA = [
    "ghana_district_cases.csv",
    "ghana_mis_sample.csv",
    "ghana_region_malaria.csv",
]

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


def say(msg: str, colour: str = "") -> None:
    print(f"{colour}{msg}{RESET}", flush=True)


def check_env() -> bool:
    """Confirm the analysis packages are importable before executing anything."""
    import importlib.util

    missing = [pkg for mod, pkg in REQUIRED_IMPORTS if importlib.util.find_spec(mod) is None]
    if missing:
        say("Missing packages in this interpreter.", RED)
        say(f"  {sys.executable}")
        say(f"  Not importable: {', '.join(missing)}")
        say("  The project pins Python 3.11. Activate the environment first:")
        say("    conda activate prosit1        (or: source .venv/bin/activate)")
        say("    pip install -r requirements.txt")
        if "geopandas" in missing:
            say("  geopandas has no 3.13 wheels; install it with")
            say("    conda install -c conda-forge geopandas=0.14.4", DIM)
        return False
    say(f"Environment ready ({sys.version.split()[0]}).", GREEN)
    return True


def check_data() -> bool:
    """Confirm the course package is in place. Checks filenames only, never rows."""
    data_dir = ROOT / "data"
    missing = [n for n in REQUIRED_DATA if not (data_dir / n).exists()]
    if missing:
        say("Data package not found.", RED)
        say(f"  Missing from {data_dir.relative_to(ROOT)}/: {', '.join(missing)}")
        say("  The package is gitignored by design. Copy it in, then re-run.")
        return False
    boundaries = data_dir / "ghana_boundaries"
    if not boundaries.exists():
        say(f"  Note: {boundaries.name}/ is absent; the map cells in 01 and 04 will fail.", YELLOW)
    say("Data package present.", GREEN)
    return True


def make_kernelspec(tmp: Path) -> str:
    """Point a throwaway kernel at the interpreter running this script.

    Without this, nbconvert launches whichever interpreter the registered
    `python3` kernel happens to name, which is often not the environment the
    pipeline was started in — the notebooks then fail on imports that the
    preflight just confirmed were present.
    """
    name = "prosit1-run"
    spec_dir = tmp / "kernels" / name
    spec_dir.mkdir(parents=True, exist_ok=True)
    (spec_dir / "kernel.json").write_text(json.dumps({
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Prosit 1 pipeline",
        "language": "python",
    }))
    return name


def run_notebook(name: str, blurb: str, inplace: bool, timeout: int,
                 kernel: str, env: dict) -> bool:
    src = ROOT / "notebooks" / name
    if not src.exists():
        say(f"  {name} not found", RED)
        return False

    cmd = [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook",
           "--execute", f"--ExecutePreprocessor.timeout={timeout}",
           f"--ExecutePreprocessor.kernel_name={kernel}"]
    if inplace:
        cmd += ["--inplace", str(src)]
    else:
        out = ROOT / "build" / "executed"
        out.mkdir(parents=True, exist_ok=True)
        cmd += ["--output-dir", str(out), "--output", name, str(src)]

    started = time.monotonic()
    proc = subprocess.run(cmd, cwd=ROOT / "notebooks", capture_output=True, text=True, env=env)
    elapsed = time.monotonic() - started

    if proc.returncode == 0:
        say(f"  ok   {name:26s} {elapsed:6.1f}s   {DIM}{blurb}{RESET}", GREEN)
        return True

    say(f"  FAIL {name:26s} {elapsed:6.1f}s", RED)
    tail = [ln for ln in proc.stderr.splitlines() if ln.strip()][-18:]
    for ln in tail:
        print(f"       {ln}")
    return False


def run_script(rel: str, label: str) -> bool:
    path = ROOT / rel
    if not path.exists():
        say(f"  skip {rel} (not present)", YELLOW)
        return True
    started = time.monotonic()
    proc = subprocess.run([sys.executable, str(path)], cwd=ROOT, capture_output=True, text=True)
    elapsed = time.monotonic() - started
    if proc.returncode == 0:
        say(f"  ok   {Path(rel).name:26s} {elapsed:6.1f}s   {DIM}{label}{RESET}", GREEN)
        return True
    say(f"  FAIL {Path(rel).name:26s} {elapsed:6.1f}s", RED)
    for ln in (proc.stdout + proc.stderr).splitlines()[-18:]:
        print(f"       {ln}")
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the Prosit 1 analysis end to end.")
    ap.add_argument("--inplace", action="store_true",
                    help="keep executed outputs in the notebooks (strip before committing)")
    ap.add_argument("--timeout", type=int, default=1800,
                    help="per-cell timeout in seconds (default 1800)")
    ap.add_argument("--skip-verify", action="store_true", help="skip verify_claims.py")
    ap.add_argument("--deck", action="store_true", help="also rebuild the presentation")
    ap.add_argument("--clean", action="store_true", help="delete build/ first")
    ap.add_argument("--only", metavar="N",
                    help="run just one notebook, by number or name (e.g. --only 02)")
    args = ap.parse_args()

    say("Prosit 1 pipeline", "\033[1m")
    say(f"{DIM}repo: {ROOT}{RESET}")
    print()

    if args.clean:
        shutil.rmtree(ROOT / "build", ignore_errors=True)
        say("Cleared build/", DIM)

    if not check_env() or not check_data():
        return 1
    print()

    selected = NOTEBOOKS
    if args.only:
        selected = [nb for nb in NOTEBOOKS if args.only in nb[0]]
        if not selected:
            say(f"No notebook matches {args.only!r}. Options: "
                + ", ".join(n.split('_')[0] for n, _ in NOTEBOOKS), RED)
            return 1
        args.skip_verify = True

    say("Notebooks, in order" if not args.only else f"Notebook {args.only}")
    started = time.monotonic()
    tmp = Path(tempfile.mkdtemp(prefix="prosit1-kernel-"))
    kernel = make_kernelspec(tmp)
    env = dict(os.environ)
    env["JUPYTER_PATH"] = os.pathsep.join(filter(None, [str(tmp), env.get("JUPYTER_PATH", "")]))
    for name, blurb in selected:
        if not run_notebook(name, blurb, args.inplace, args.timeout, kernel, env):
            shutil.rmtree(tmp, ignore_errors=True)
            print()
            say("Pipeline stopped. Fix the cell above and re-run.", RED)
            return 1
    shutil.rmtree(tmp, ignore_errors=True)
    print()

    if not args.skip_verify:
        say("Verification")
        if not run_script("scripts/verify_claims.py", "independent re-check of quoted numbers"):
            print()
            say("Notebooks ran, but claim verification failed.", RED)
            return 1
        print()

    if args.deck:
        say("Presentation")
        if not run_script("scripts/build_ashesi_deck.py", "rebuild the deck from the template"):
            return 1
        print()

    total = time.monotonic() - started
    say(f"Pipeline complete in {total:.0f}s.", GREEN)
    if not args.inplace:
        say(f"{DIM}Executed notebooks: build/executed/  (gitignored){RESET}")
    say(f"{DIM}Figures refreshed in figures/{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
