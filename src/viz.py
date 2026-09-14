"""Visualization helpers for geographic maps, distributions, and calibration plots.

Ensures standard styling across figures for reports and slides.
"""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt

FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"


def set_theme():
    """Apply consistent styling across all project figures."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["figure.dpi"] = 300


def save_figure(fig: plt.Figure, filename: str, figures_dir: Optional[Path] = None):
    """Save a matplotlib figure to the project figures directory.

    Returns the path where the figure was saved.
    """
    target_dir = figures_dir or FIGURES_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / filename
    fig.savefig(out_path, bbox_inches="tight")
    return out_path
