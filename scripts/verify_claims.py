"""Independent verification of Prosit 1 claims.

Prints aggregates, model outputs and derived comparisons only. Never prints a
raw record from data/. Usage, from the repo root: .venv/bin/python scripts/verify_claims.py
"""

import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
COPY, REAL = (Path(a) for a in (sys.argv[1:3] + [".", "."])[:2])
sys.path.insert(0, str(COPY))
from src import io, models, uncertainty as unc  # noqa: E402

SEED = io.RANDOM_SEED
d = io.load_district_cases()
mis = io.load_mis_sample()
reg = io.load_region_malaria()
pub22 = (
    reg.query("survey_year == 2022")
    .dropna(subset=["hv024_16region"])
    .groupby("hv024_16region")["net_ownership_pct"]
    .first()
)


def hdr(s):
    print("\n" + "=" * 8, s)


# ---------------------------------------------------------------- D. dictionary
hdr("D. Data dictionary claims (aggregates only)")
print(
    f"households {len(mis):,} | clusters {mis.cluster.nunique()} | regions {mis.region.nunique()}"
)
print(
    "has_net==0:",
    int((mis.has_net == 0).sum()),
    "| num_nets==0:",
    int((mis.num_nets == 0).sum()),
    "| has_net vs num_nets>0 disagreements:",
    int(((mis.num_nets > 0).astype(int) != mis.has_net).sum()),
)
cl = mis.groupby("cluster").num_nets.sum()
print(f"per-cluster total nets variance/mean: {cl.var() / cl.mean():.2f}")
print(
    "district count by region_code:",
    d.region_code.value_counts().sort_index().to_dict(),
)
recomputed = d.positive_cases / d.mean_population * 1e5
print(
    f"max |positive_per_100k - cases/pop*1e5| = {(d.positive_per_100k - recomputed).abs().max():.6f}"
)
for r in [12, 13, 14, 15, 16]:
    sub = mis[mis.region == r]
    fc = d.loc[d.region_code == r, "net_coverage_pct"].unique().round(2).tolist()
    print(
        f"hv024={r}: survey-weighted has_net {unc.weighted_proportion(sub, 'has_net'):.2f}"
        f" | published ITN ownership {pub22.get(float(r), float('nan'))}"
        f" | district-file coverage {fc} | {len(sub)} hh, {sub.cluster.nunique()} clusters"
    )
rural = mis[mis.residence == "rural"]
rc = rural.groupby("region").cluster.nunique().sort_values(kind="stable")
print(
    f"rural-cluster rank of Northern (1 = fewest): {list(rc.index).index(12) + 1} of {len(rc)};"
    f" rural clusters per region sorted: {rc.tolist()}"
)

# ---------------------------------------------------------------- A. Theme A
hdr("A. Theme A cross-checks")
north = mis[mis.region == 12]
print(
    f"all-Northern weighted has_net = {unc.weighted_proportion(north, 'has_net'):.4f}"
    f" vs published {pub22[12.0]}"
)
domain = rural[rural.region == 12]
own = lambda df: unc.weighted_proportion(df, "has_net")  # noqa: E731


def linearised_width(df, psu):
    """Taylor-linearised 95% CI width (pp) for a weighted proportion, one stratum."""
    w, y = df.sample_weight.to_numpy(float), df.has_net.to_numpy(float)
    p = (w * y).sum() / w.sum()
    z = pd.Series(w * (y - p) / w.sum()).groupby(psu).sum()
    c = len(z)
    return 2 * 1.96 * np.sqrt(c / (c - 1) * ((z - z.mean()) ** 2).sum()) * 100


lin_cl = linearised_width(domain, domain.cluster.to_numpy())
lin_srs = linearised_width(domain, np.arange(len(domain)))
print(
    f"rural Northern, design-based (linearised) CI width: cluster {lin_cl:.2f} pp,"
    f" SRS {lin_srs:.2f} pp, DEFF {(lin_cl / lin_srs) ** 2:.2f}"
)
rng = np.random.default_rng(SEED)
pos = {
    c: np.flatnonzero(domain.cluster.to_numpy() == c) for c in domain.cluster.unique()
}
keys = np.array(list(pos))
one_stage = [
    own(domain.take(np.concatenate([pos[c] for c in rng.choice(keys, keys.size)])))
    for _ in range(2000)
]
lo, hi = np.percentile(one_stage, [2.5, 97.5])
print(
    f"cluster-only (one-stage) bootstrap width: {hi - lo:.2f} pp  (two-stage in repo: 15.20)"
)
deffs, ratios = [], []
for s in range(20):
    t = unc.compare_bootstraps(domain, own, "x", n_bootstraps=2000, random_seed=s)
    deffs.append(t.attrs["design_effect"])
    ratios.append(t.ci_width.iloc[1] / t.ci_width.iloc[0])
print(
    f"two-stage vs naive over 20 seeds: DEFF min {min(deffs):.2f} / median {np.median(deffs):.2f}"
    f" / max {max(deffs):.2f}; width ratio {min(ratios):.2f} to {max(ratios):.2f}"
)

# ---------------------------------------------------------------- B. leakage
hdr("B. Leakage audit")
X = d[["mean_population", "net_coverage_pct"]]
y = d.positive_cases.to_numpy()
strata = d.region_code


def pipe():
    return Pipeline([("scaler", StandardScaler()), ("model", Ridge(alpha=1.0))])


def rmse(m, Xt, yt):
    return float(np.sqrt(mean_squared_error(yt, m.predict(Xt))))


a = train_test_split(X, y, test_size=0.2, random_state=SEED, shuffle=True)
b = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=strata)
pa, pb = pipe().fit(a[0], a[2]), pipe().fit(b[0], b[2])
print(
    f"seed 42: random-split R2 {r2_score(a[3], pa.predict(a[1])):.4f},"
    f" stratified-split R2 {r2_score(b[3], pb.predict(b[1])):.4f}  (reports quote 0.4905)"
)
top5 = set(np.argsort(-y)[:5])
print(
    "seed 42: top-5 highest-count districts in test set: random split",
    len(top5 & set(a[1].index)),
    "| stratified split",
    len(top5 & set(b[1].index)),
)
rows = []
Xs = StandardScaler().fit_transform(X)
for s in range(500):
    a = train_test_split(X, y, test_size=0.2, random_state=s, shuffle=True)
    b = train_test_split(X, y, test_size=0.2, random_state=s, stratify=strata)
    c = train_test_split(Xs, y, test_size=0.2, random_state=s, stratify=strata)
    r_rand = rmse(pipe().fit(a[0], a[2]), a[1], a[3])
    r_strat = rmse(pipe().fit(b[0], b[2]), b[1], b[3])
    r_leaky = rmse(Ridge(alpha=1.0).fit(c[0], c[2]), c[1], c[3])
    rows.append((r_rand, r_strat, r_strat - r_leaky, (r_strat - r_leaky) / r_strat))
sw = pd.DataFrame(rows, columns=["rand", "strat", "pre_delta", "pre_rel"])


def q(s):
    return f"median {s.median():,.0f} [5%-95%: {s.quantile(.05):,.0f} to {s.quantile(.95):,.0f}]"


print("500 seeds, random-split test RMSE    :", q(sw.rand))
print("500 seeds, stratified-split test RMSE:", q(sw.strat))
print(
    f"share of seeds where random RMSE < stratified RMSE: {(sw.rand < sw.strat).mean():.2f}"
)
print(
    f"preprocessing leak (clean - leaky RMSE): mean {sw.pre_delta.mean():,.1f}, sd {sw.pre_delta.std():,.1f},"
    f" range {sw.pre_delta.min():,.1f} to {sw.pre_delta.max():,.1f}; median |rel| {sw.pre_rel.abs().median():.4%};"
    f" share of seeds where leaky looks better: {(sw.pre_delta > 0).mean():.2f}"
)
preds = np.empty_like(y, dtype=float)
for r in sorted(d.region_code.unique()):
    tr, te = d.region_code != r, d.region_code == r
    m = pipe().fit(X[tr], y[tr])
    preds[te.to_numpy()] = m.predict(X[te])
    print(f"leave-one-region-out, held out {r}: RMSE {rmse(m, X[te], y[te]):,.0f}")
print(f"leave-one-region-out pooled RMSE: {np.sqrt(np.mean((preds - y) ** 2)):,.0f}")

# ---------------------------------------------------------------- C. allocation
hdr("C. Allocation")
off = np.log(d.mean_population.clip(lower=1)).to_numpy()
nb = models.fit_negative_binomial_mle(
    "positive_cases ~ net_coverage_pct", d, offset=off
)
al = models.compute_allocation(d, nb, total_nets=50000, offset=off)
print(
    f"NB coefficient on net_coverage_pct = {nb.params['net_coverage_pct']:+.4f}"
    f" (p = {nb.pvalues['net_coverage_pct']:.2g}): higher coverage predicts MORE cases"
    if nb.params["net_coverage_pct"] > 0
    else f"NB coefficient on net_coverage_pct = {nb.params['net_coverage_pct']:+.4f}"
)
pat = re.compile(
    r"\|\s*\d+\s*\|\s*([^|]+?)\s*\|[^|]+\|\s*([\d,]+)\s*\|\s*([\d.]+)%\s*\|\s*([\d,]+)\s*\|"
    r"\s*([\d,]+)\s*\|\s*\*\*([\d,]+)\*\*\s*\|\s*([+\-−]?[\d,]+)\s*\|"
)
num = lambda s: int(s.replace(",", "").replace("−", "-"))  # noqa: E731
md = [
    pat.match(line)
    for line in (REAL / "reports/allocation.md").read_text().splitlines()
]
md = [m.groups() for m in md if m]
byname = al.set_index("district")
bad = 0
for name, popu, cov, cases, naive, eq, delta in md:
    r = byname.loc[name]
    got = (
        round(r.mean_population),
        round(r.net_coverage_pct, 1),
        int(r.positive_cases),
        int(r.naive_allocation),
        int(r.equitable_allocation),
        int(r.delta),
    )
    want = (num(popu), float(cov), num(cases), num(naive), num(eq), num(delta))
    if got != want:
        bad += 1
        print("  MISMATCH", name, "report", want, "recomputed", got)
print(f"allocation.md schedule: {len(md)} rows parsed, {bad} mismatching rows")
tot = al.groupby("region_code")[["naive_allocation", "equitable_allocation"]].sum()
print(
    "region totals (naive, equitable):",
    {k: tuple(v) for k, v in tot.iterrows()},
    "| depot figures in allocation.md/deck: 12->24,980  15->17,547  16->7,473",
)
al["per1000"] = al.equitable_allocation / al.mean_population * 1000
al["burden"] = (
    al.positive_cases / al.mean_population
)  # cumulative positives per person, 2014-17
al["delta_pc"] = al.delta / al.mean_population
al["ub_ratio"] = al.pred_ci_upper / al.predicted_cases
for r, g in al.groupby("region_code"):
    print(
        f"region {r}: equitable nets/1000 pop {g.per1000.min():.3f} to {g.per1000.max():.3f};"
        f" Spearman(alloc, pop) {spearmanr(g.equitable_allocation, g.mean_population)[0]:.3f};"
        f" upper/predicted ratio {g.ub_ratio.min():.4f} to {g.ub_ratio.max():.4f};"
        f" Spearman(delta per capita, burden) {spearmanr(g.delta_pc, g.burden)[0]:.3f}"
    )
rank = al.burden.rank().astype(int)
t = al.set_index("district")
print(
    f"Tamale burden rank among 50 (1 = lowest cases per person): {int(rank[al.district == 'Tamale'].iloc[0])};"
    f" Tamale burden / Northern median = {t.loc['Tamale', 'burden'] / al[al.region_code == 12].burden.median():.2f}"
)
for name, rc_ in [("Bolgatanga", 15), ("Wa", 16), ("Nabdam", 15), ("Bole", 12)]:
    g = al[al.region_code == rc_]
    print(
        f"{name}: burden / own-region median = {t.loc[name, 'burden'] / g.burden.median():.2f};"
        f" burden rank within region (1 = highest) = {int(g.burden.rank(ascending=False)[g.district == name].iloc[0])} of {len(g)}"
    )
print(f"Spearman(delta, burden) across all 50: {spearmanr(al.delta, al.burden)[0]:.3f}")


def moved(a1, a2):
    return int(
        np.abs(
            a1.equitable_allocation.to_numpy() - a2.equitable_allocation.to_numpy()
        ).sum()
        // 2
    )


def region_totals(a1, col="region_code"):
    return a1.groupby(col).equitable_allocation.sum().to_dict()


# sensitivity 1: point estimate instead of upper bound
pt = al.copy()
w = pt.predicted_cases * pt.unmet_need_gap
raw = w / w.sum() * 50000
seats = np.floor(raw).astype(int)
seats[np.argsort(-(raw - seats).to_numpy())[: 50000 - seats.sum()]] += 1
pt["equitable_allocation"] = seats
print(
    f"[sens] point estimate instead of CI upper bound: {moved(al, pt)} nets move; totals {region_totals(pt)}"
)

# sensitivity 2: region dummies instead of a coverage slope
nb_r = models.fit_negative_binomial_mle(
    "positive_cases ~ C(region_code)", d, offset=off
)
al_r = models.compute_allocation(d, nb_r, total_nets=50000, offset=off)
print(
    f"[sens] C(region_code) model instead of coverage slope: {moved(al, al_r)} nets move; totals {region_totals(al_r)}"
)

# sensitivity 3: current (post-2019) region of each district, from the COD boundaries
import geopandas as gpd  # noqa: E402

adm2 = gpd.read_file(COPY / "data/ghana_boundaries/gha_admin2.geojson")


def norm(s):
    s = re.sub(r"\b(Municipal|Metropolitan|District)\b", "", s, flags=re.I)
    return re.sub(r"[^a-zA-Z]", "", s).lower()


aliases = {
    "sagnarigu": "sagnerigu",
    "gushiegu": "gushegu",
    "tatalesangule": "tatalesanguli",
    "kasenanankana": "kasenanankanaeast",
    "garutempane": "garu",
    "savelugunanton": "savelugu",
    "bunkpuruguyunyoo": "bunkpurugunakpanduri",
}
lookup = {norm(n): a for n, a in zip(adm2.adm2_name, adm2.adm1_name)}
d2 = d.copy()
d2["current_adm1"] = [
    lookup.get(aliases.get(norm(x), norm(x)), "UNMATCHED") for x in d2.district
]
print(
    "[sens] districts by (region_code, current adm1):",
    d2.groupby(["region_code", "current_adm1"]).size().to_dict(),
)
moved_names = d2[(d2.region_code == 12) & (d2.current_adm1 != "Northern")]
print(
    "[sens] region_code 12 districts now outside Northern:",
    moved_names.groupby("current_adm1").district.apply(list).to_dict(),
)
cov13 = unc.weighted_proportion(mis[mis.region == 13], "has_net")
cov14 = unc.weighted_proportion(mis[mis.region == 14], "has_net")
d2.loc[d2.current_adm1 == "Savannah", "net_coverage_pct"] = cov13
d2.loc[d2.current_adm1 == "Northern East", "net_coverage_pct"] = cov14
nb_c = models.fit_negative_binomial_mle(
    "positive_cases ~ net_coverage_pct", d2, offset=off
)
al_c = models.compute_allocation(d2, nb_c, total_nets=50000, offset=off)
al_c["current_adm1"] = d2.current_adm1.to_numpy()
al2 = al.assign(current_adm1=d2.current_adm1.to_numpy())
print(
    f"[sens] coverage corrected for current region (Savannah {cov13:.1f}%, North East {cov14:.1f}%):"
    f" {moved(al, al_c)} nets move"
)
print(
    "        totals by current region, as reported:", region_totals(al2, "current_adm1")
)
print(
    "        totals by current region, corrected  :",
    region_totals(al_c, "current_adm1"),
)

# sensitivity 4: the allocation.md claim about lower Northern coverage
for cov in (61.4, 74.0):
    d3 = d.copy()
    d3.loc[d3.region_code == 12, "net_coverage_pct"] = cov
    nb3 = models.fit_negative_binomial_mle(
        "positive_cases ~ net_coverage_pct", d3, offset=off
    )
    a3 = models.compute_allocation(d3, nb3, total_nets=50000, offset=off)
    print(
        f"[sens] Northern coverage set to {cov}% (cluster-bootstrap bound): Northern total"
        f" {int(a3[a3.region_code == 12].equitable_allocation.sum()):,} (as reported: 24,196)"
    )

# ---------------------------------------------------------------- E. deck numbers
hdr("E. Numbers used in the Ashesi deck")
tot_row = [
    line
    for line in (REAL / "reports/allocation.md").read_text().splitlines()
    if "**Total**" in line
]
print("allocation.md Total row:", tot_row[0][:160] if tot_row else "not found")
print(
    f"column sums: population {round(d.mean_population.sum()):,}, positive cases {int(d.positive_cases.sum()):,}"
)
pop = al.groupby("region_code").mean_population.sum()
eq = al.groupby("region_code").equitable_allocation.sum()
print("nets per 1,000 by region:", (eq / pop * 1000).round(2).to_dict())
g5 = (
    al.sort_values("delta", ascending=False)
    .head(5)[["district", "delta"]]
    .values.tolist()
)
l5 = al.sort_values("delta").head(5)[["district", "delta"]].values.tolist()
print("top 5 gainers:", g5)
print("top 5 losers :", l5)
print(
    "smallest allocation:",
    al.loc[
        al.equitable_allocation.idxmin(), ["district", "equitable_allocation"]
    ].tolist(),
)


def by_code(a1):
    s = a1.groupby("region_code").equitable_allocation.sum()
    return [int(s.get(12, 0)), int(s.get(15, 0)), int(s.get(16, 0))]


print("[table] as proposed          :", by_code(al), "moved 0")
print("[table] point estimate       :", by_code(pt), "moved", moved(al, pt))
print("[table] region-effects model :", by_code(al_r), "moved", moved(al, al_r))
print("[table] coverage corrected   :", by_code(al_c), "moved", moved(al, al_c))
for cov in (61.4, 74.0):
    d3 = d.copy()
    d3.loc[d3.region_code == 12, "net_coverage_pct"] = cov
    nb3 = models.fit_negative_binomial_mle(
        "positive_cases ~ net_coverage_pct", d3, offset=off
    )
    a3 = models.compute_allocation(d3, nb3, total_nets=50000, offset=off)
    print(f"[table] Northern coverage {cov}:", by_code(a3), "moved", moved(al, a3))
print(f"AIC coverage-slope {nb.aic:.1f} vs region-effects {nb_r.aic:.1f}")
per_person = d.positive_cases / d.mean_population  # cumulative 2014-17
print(
    f"districts with >1 confirmed positive per resident over 2014-17: {int((per_person > 1).sum())} of 50;"
    f" >1 per resident per year: {int((per_person > 4).sum())}"
)
print(
    "median cases per resident per year by region:",
    (per_person / 4).groupby(d.region_code).median().round(2).to_dict(),
)
print(
    "median test positivity by region:",
    (d.positive_cases / d.tested_cases)
    .groupby(d.region_code)
    .median()
    .round(3)
    .to_dict(),
)
xl = pd.ExcelFile(COPY / "data/raw/northern-ghana-districts-routine-data-2014-17.xlsx")
irs = smc = 0
for sheet in xl.sheet_names:
    raw = xl.parse(sheet)
    dcol = "District" if "District" in raw.columns else "Districts"
    irs += int(
        raw.groupby(dcol)["IRS Status"].apply(lambda v: (v == "IRS").any()).sum()
    )
    smc += int(
        raw.groupby(dcol)["SMC Status"].apply(lambda v: (v == "SMC").any()).sum()
    )
print(
    f"raw workbook: districts with IRS in any month {irs} of 50, with SMC in any month {smc} of 50"
)
