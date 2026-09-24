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


def plot_district_choropleth(
    adm0_path: Path,
    adm1_path: Path,
    adm2_path: Path,
    case_df: pd.DataFrame,
    value_col: str = "positive_per_100k",
    title: str = "Malaria Surveillance Coverage & Case Rate across Ghana Districts",
    legend_label: str = "Cumulative Positives per 100k (2014–17)",
) -> Tuple[plt.Figure, plt.Axes]:
    """Map Ghana's 260 districts, shading the 50 northern surveillance districts.

    Set legend_label to match value_col when it is not the case rate.
    """
    import geopandas as gpd
    import re

    adm1 = gpd.read_file(adm1_path)
    adm2 = gpd.read_file(adm2_path)

    def norm(s):
        s = re.sub(r"\b(Municipal|Metropolitan|District)\b", "", s, flags=re.I)
        return re.sub(r"[^a-zA-Z]", "", s).lower()

    aliases = {
        "sagnarigu": "sagnerigu",
        "gushiegu": "gushegu",
        "tatalesangule": "tatalesanguli",
        "kasenanankana": "kasenanankanaeast",
    }

    adm_norm_map = {norm(name): idx for idx, name in enumerate(adm2["adm2_name"])}

    adm2_plot = adm2.copy()
    adm2_plot[value_col] = np.nan

    for _, row in case_df.iterrows():
        k = norm(str(row["district"]))
        k = aliases.get(k, k)
        val = row[value_col]
        if k in adm_norm_map:
            adm2_plot.loc[adm_norm_map[k], value_col] = val
        elif k == "garutempane":
            for sub in ["garu", "tempane"]:
                if sub in adm_norm_map:
                    adm2_plot.loc[adm_norm_map[sub], value_col] = val
        elif k == "savelugunanton":
            for sub in ["savelugu", "nanton"]:
                if sub in adm_norm_map:
                    adm2_plot.loc[adm_norm_map[sub], value_col] = val
        elif k == "bunkpuruguyunyoo":
            for sub in ["bunkpurugunakpanduri", "yunyoonasuan"]:
                if sub in adm_norm_map:
                    adm2_plot.loc[adm_norm_map[sub], value_col] = val

    fig, ax = plt.subplots(figsize=(8, 10))
    adm2_plot[adm2_plot[value_col].isna()].plot(
        ax=ax, color="#E8ECEF", edgecolor="#B0BEC5", linewidth=0.5
    )
    adm2_plot[adm2_plot[value_col].notna()].plot(
        column=value_col,
        ax=ax,
        cmap="YlOrRd",
        edgecolor="#37474F",
        linewidth=0.8,
        legend=True,
        legend_kwds={
            "label": legend_label,
            "orientation": "horizontal",
            "shrink": 0.7,
            "pad": 0.05,
        },
    )
    adm1.boundary.plot(ax=ax, color="#263238", linewidth=1.2)
    ax.set_title(title, fontsize=12, pad=15)
    ax.set_axis_off()
    return fig, ax


def plot_region_choropleth(
    adm1_path: Path,
    region_stats: pd.DataFrame,
    value_col: str = "n_clusters",
    title: str = "National Survey Data Coverage: DHS Clusters per Region (2022)",
) -> Tuple[plt.Figure, plt.Axes]:
    """Map Ghana's 16 regions shaded by a regional survey metric."""
    import geopandas as gpd
    import re

    adm1 = gpd.read_file(adm1_path)

    def clean_reg(s):
        s = re.sub(r"\(.*?\)", "", str(s))
        s = re.sub(r"[^a-zA-Z]", "", s).lower()
        if s == "northerneast":
            s = "northeast"
        return s

    adm1["join_key"] = adm1["adm1_name"].apply(clean_reg)
    region_stats["join_key"] = region_stats["region_name"].apply(clean_reg)

    adm1_merged = adm1.merge(region_stats, on="join_key", how="left")

    fig, ax = plt.subplots(figsize=(8, 10))
    adm1_merged.plot(
        column=value_col,
        ax=ax,
        cmap="Blues",
        edgecolor="#263238",
        linewidth=1.2,
        legend=True,
        legend_kwds={
            "label": "DHS 2022 Survey Clusters Sampled per Region",
            "orientation": "horizontal",
            "shrink": 0.7,
            "pad": 0.05,
        },
    )

    for _, row in adm1_merged.iterrows():
        pt = row["geometry"].representative_point()
        val = int(row[value_col]) if pd.notna(row[value_col]) else 0
        ax.text(
            pt.x,
            pt.y,
            f"{row['adm1_name']}\n({val})",
            fontsize=7,
            ha="center",
            va="center",
            weight="bold",
            color="#1A237E",
        )

    ax.set_title(title, fontsize=12, pad=15)
    ax.set_axis_off()
    return fig, ax


def plot_allocation_comparison(
    df: pd.DataFrame,
    n_top: int = 5,
    title: str = "ITN Policy Shift: Equitable (Need-Weighted) vs. Naive Allocation",
) -> Tuple[plt.Figure, plt.Axes]:
    """Horizontal bar plot showing top gainers and losers in ITN allocation."""
    gainers = df.sort_values(by="delta", ascending=False).head(n_top)
    losers = df.sort_values(by="delta", ascending=True).head(n_top)
    subset = pd.concat([losers, gainers]).sort_values(by="delta")

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#C44E52" if d < 0 else "#4C72B0" for d in subset["delta"]]
    bars = ax.barh(subset["district"], subset["delta"], color=colors, height=0.6)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.7)

    for bar, delta in zip(bars, subset["delta"]):
        offset = 35 if delta >= 0 else -35
        ha = "left" if delta >= 0 else "right"
        ax.annotate(
            f"{delta:+d}",
            xy=(delta, bar.get_y() + bar.get_height() / 2),
            xytext=(offset, 0),
            textcoords="offset points",
            va="center",
            ha=ha,
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xlabel("Change in Net Allocation (Equitable - Naive)")
    ax.set_title(title, fontsize=12, pad=12)
    ax.margins(x=0.2)
    return fig, ax


def plot_policy_shift_map(
    adm1_path: Path,
    adm2_path: Path,
    alloc_df: pd.DataFrame,
    title: str = "Policy Shift: ITN Reallocation (Equitable - Naive) Across Northern Ghana",
) -> Tuple[plt.Figure, plt.Axes]:
    """Choropleth of Northern Ghana highlighting net reallocations (Gainers in blue, Losers in red)."""
    import re
    import geopandas as gpd
    from matplotlib.colors import TwoSlopeNorm

    adm1 = gpd.read_file(adm1_path)
    adm2 = gpd.read_file(adm2_path)

    northern_regions = ["Northern", "Upper East", "Upper West"]
    adm1_north = adm1[adm1["adm1_name"].isin(northern_regions)].copy()

    def norm(s):
        s = re.sub(r"\b(Municipal|Metropolitan|District)\b", "", s, flags=re.I)
        return re.sub(r"[^a-zA-Z]", "", s).lower()

    aliases = {
        "sagnarigu": "sagnerigu",
        "gushiegu": "gushegu",
        "tatalesangule": "tatalesanguli",
        "kasenanankana": "kasenanankanaeast",
    }

    adm_norm_map = {norm(name): idx for idx, name in enumerate(adm2["adm2_name"])}
    adm2_plot = adm2.copy()
    adm2_plot["delta"] = np.nan

    for _, row in alloc_df.iterrows():
        k = norm(str(row["district"]))
        k = aliases.get(k, k)
        val = row["delta"]
        if k in adm_norm_map:
            adm2_plot.loc[adm_norm_map[k], "delta"] = val
        elif k == "garutempane":
            for sub in ["garu", "tempane"]:
                if sub in adm_norm_map:
                    adm2_plot.loc[adm_norm_map[sub], "delta"] = val
        elif k == "savelugunanton":
            for sub in ["savelugu", "nanton"]:
                if sub in adm_norm_map:
                    adm2_plot.loc[adm_norm_map[sub], "delta"] = val
        elif k == "bunkpuruguyunyoo":
            for sub in ["bunkpurugunakpanduri", "yunyoonasuan"]:
                if sub in adm_norm_map:
                    adm2_plot.loc[adm_norm_map[sub], "delta"] = val

    adm2_north = adm2_plot[adm2_plot["delta"].notna()].copy()

    fig, ax = plt.subplots(figsize=(10, 8))
    norm_scale = TwoSlopeNorm(
        vmin=alloc_df["delta"].min(), vcenter=0, vmax=alloc_df["delta"].max()
    )

    adm2_north.plot(
        column="delta",
        ax=ax,
        cmap="RdYlBu",
        norm=norm_scale,
        edgecolor="#263238",
        linewidth=0.7,
        legend=True,
        legend_kwds={
            "label": "Net Reallocation (Equitable - Naive): Red = Reduced, Blue = Increased",
            "orientation": "horizontal",
            "shrink": 0.65,
            "pad": 0.05,
        },
    )
    adm1_north.boundary.plot(ax=ax, color="#1A237E", linewidth=1.5)

    # Label the largest gains and losses with their computed change; Tamale's label
    # goes below so it does not sit under its neighbour Sagnarigu's.
    deltas = alloc_df.set_index("district")["delta"]
    for dist_name in ["Tamale", "Sagnarigu", "Bolgatanga", "Wa"]:
        k = norm(dist_name)
        k = aliases.get(k, k)
        if k in adm_norm_map:
            geom = adm2.loc[adm_norm_map[k], "geometry"]
            pt = geom.centroid
            ax.annotate(
                f"{dist_name}\n{deltas[dist_name]:+,}",
                xy=(pt.x, pt.y),
                xytext=(0, -34 if dist_name == "Tamale" else 22),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                fontweight="bold",
                bbox=dict(
                    boxstyle="round,pad=0.2",
                    facecolor="white",
                    alpha=0.85,
                    edgecolor="gray",
                ),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"),
            )

    ax.set_title(title, fontsize=12, pad=15)
    ax.set_axis_off()
    return fig, ax
