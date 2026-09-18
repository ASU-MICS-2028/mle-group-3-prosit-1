"""Plot helpers, so notebook cells stay short and figures share one style."""

from pathlib import Path
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"


def set_theme():
    """Apply consistent styling across all project figures."""
    plt.style.use(
        "seaborn-v0_8-whitegrid"
        if "seaborn-v0_8-whitegrid" in plt.style.available
        else "default"
    )
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["figure.dpi"] = 110  # save_figure re-renders at 300


def save_figure(
    fig: plt.Figure, filename: str, figures_dir: Optional[Path] = None
) -> Path:
    """Save a figure into figures/ at print resolution. Returns the path."""
    target_dir = figures_dir or FIGURES_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / filename
    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    return out_path


def plot_count_distribution(
    y: pd.Series, bins: int = 15, title: str = "", xlabel: str = "count"
) -> Tuple[plt.Figure, plt.Axes, np.ndarray]:
    """Histogram of a count response with the mean marked.

    Also returns the bin edges, so a fitted pmf can be overlaid on the same bins.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    counts, edges, _ = ax.hist(
        y, bins=bins, color="#4C72B0", edgecolor="white", alpha=0.85
    )
    ax.axvline(
        float(np.mean(y)),
        color="#C44E52",
        linestyle="--",
        label=f"mean = {np.mean(y):,.0f}",
    )
    ax.set_xlabel(xlabel)
    ax.set_ylabel("number of districts")
    ax.set_title(title)
    ax.legend()
    return fig, ax, edges


def overlay_expected(
    ax: plt.Axes, edges: np.ndarray, expected: np.ndarray, label: str, color: str
):
    """Draw a fitted model's expected bin counts as a step line over a histogram."""
    centres = (edges[:-1] + edges[1:]) / 2
    ax.plot(
        centres,
        expected,
        marker="o",
        markersize=4,
        color=color,
        label=label,
        linewidth=1.8,
    )
    ax.legend()
    return ax


def plot_ci_comparison(
    table: pd.DataFrame, title: str = ""
) -> Tuple[plt.Figure, plt.Axes]:
    """Interval plot comparing bootstrap methods. Takes `compare_bootstraps` output."""
    fig, ax = plt.subplots(figsize=(7, 2.4 + 0.5 * len(table)))
    for i, row in enumerate(table.itertuples()):
        ax.plot([row.ci_low, row.ci_high], [i, i], linewidth=3, color="#4C72B0")
        ax.plot(row.estimate, i, "o", color="#C44E52", zorder=3)
        ax.annotate(
            f"width {row.ci_width:.1f} pp",
            xy=(row.ci_high, i),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            fontsize=9,
        )
    ax.set_yticks(range(len(table)))
    ax.set_yticklabels(table["method"])
    ax.set_xlabel("estimate (%)")
    ax.set_title(title)
    ax.margins(x=0.18)
    return fig, ax
