"""
Alberta opioid mortality: interrupted time series around COVID-19 onset
=======================================================================

Question: Did Alberta's opioid death rate shift at a level higher than the
pre-COVID trend can explain, starting from 2020 Q2?

Method: interrupted time series (ITS) with a level and slope change
(segmented regression). When time is the running variable this is sometimes
called regression discontinuity in time (Hausman and Rapson 2018), but I do
not invoke RD-style local-randomization arguments. Identification rests on
a correctly specified counterfactual trend, not on continuity of potential
outcomes at the cutoff.

Outcome is modelled as a rate per 100k Alberta residents using Statistics
Canada quarterly population estimates, to net out population growth over
the 10-year window. Quarter fixed effects absorb seasonality. HAC standard
errors with small-sample correction. Placebo cutoffs in the pre-period and
a donut robustness check are reported.

Data:
- Public Health Agency of Canada, Health Infobase, Substance-Related Harms
  Data (downloaded 2026-05-20). Alberta opioid deaths by quarter.
- Statistics Canada Table 17-10-0009-01, quarterly population estimates by
  province.

Cutoff: 2020 Q2 (first full quarter under Alberta's public health emergency,
declared 2020-03-17).
"""

import os
from datetime import date

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ---------------------------------------------------------------------------
# 1. Load deaths
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "SubstanceHarmsData.csv")
POP = os.path.join(HERE, "data", "statcan-17100009-population.csv")
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)

ab = df[
    (df["Region"] == "Alberta")
    & (df["Substance"] == "Opioids")
    & (df["Source"] == "Deaths")
    & (df["Time_Period"] == "By quarter")
    & (df["Specific_Measure"] == "Overall numbers")
    & (df["Disaggregator"].isna())
    & (df["Unit"] == "Number")
].copy()

ab[["year", "q"]] = ab["Year_Quarter"].str.extract(r"(\d{4})\s*Q(\d)").astype(int)
ab["t"] = ab["year"] + (ab["q"] - 1) / 4.0           # continuous time (year units)
ab["deaths"] = ab["Value"].astype(float)
ab = ab.sort_values("t").reset_index(drop=True)

assert len(ab) == 39, f"Expected 39 quarters, got {len(ab)}"

# ---------------------------------------------------------------------------
# 2. Load population (StatCan Table 17-10-0009-01)
#    REF_DATE is YYYY-MM. Quarterly snapshots are at Jan/Apr/Jul/Oct.
# ---------------------------------------------------------------------------
pop = pd.read_csv(POP, dtype=str)
pop.columns = [c.strip('﻿"') for c in pop.columns]
pop = pop[pop["GEO"] == "Alberta"].copy()
pop[["pop_year", "pop_month"]] = pop["REF_DATE"].str.split("-", expand=True).astype(int)
pop["VALUE"] = pd.to_numeric(pop["VALUE"], errors="coerce")

# Map quarter -> the snapshot month StatCan publishes (Q1->Jan, Q2->Apr, Q3->Jul, Q4->Oct)
month_to_q = {1: 1, 4: 2, 7: 3, 10: 4}
pop["q"] = pop["pop_month"].map(month_to_q)
pop = pop.dropna(subset=["q"])
pop["q"] = pop["q"].astype(int)
pop = pop[["pop_year", "q", "VALUE"]].rename(columns={"VALUE": "pop"})
pop["t"] = pop["pop_year"] + (pop["q"] - 1) / 4.0

ab = ab.merge(pop[["t", "pop"]], on="t", how="left")
assert ab["pop"].notna().all(), "Missing population for some quarters"

ab["rate"] = ab["deaths"] / ab["pop"] * 1e5  # deaths per 100k Alberta residents

print(f"Quarters: {len(ab)}   range: {ab['Year_Quarter'].iloc[0]} -> {ab['Year_Quarter'].iloc[-1]}")
print(ab[["Year_Quarter", "deaths", "pop", "rate"]].to_string(index=False))

# ---------------------------------------------------------------------------
# 3. Main specification: segmented regression on rate per 100k, with
#    quarter fixed effects to absorb seasonality.
# ---------------------------------------------------------------------------
CUTOFF = 2020.25  # 2020 Q2
ab["centered_t"] = ab["t"] - CUTOFF
ab["post"] = (ab["t"] >= CUTOFF).astype(int)
ab["centered_t_post"] = ab["centered_t"] * ab["post"]


def fit_seg(data, dv, hac_lags=3):
    """Segmented regression with quarter dummies (Q4 reference), HAC SE."""
    formula = f"{dv} ~ centered_t + post + centered_t_post + C(q)"
    return smf.ols(formula, data=data).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": hac_lags, "use_correction": True},
    )


main = fit_seg(ab, dv="rate", hac_lags=3)
print("\n========== Main spec: rate per 100k, segmented + quarter FE ==========")
print(main.summary())

jump = main.params["post"]
jump_se = main.bse["post"]
ci_low, ci_high = main.conf_int().loc["post"]
print(f"\nLevel shift at 2020 Q2 cutoff: {jump:+.2f} deaths per 100k per quarter "
      f"[95% CI {ci_low:+.2f}, {ci_high:+.2f}], p = {main.pvalues['post']:.4f}")

# For interpretability, also report at average population
mean_pop = ab["pop"].mean()
print(f"At mean Alberta population ({mean_pop:,.0f}), this corresponds to roughly "
      f"{jump * mean_pop / 1e5:+.0f} additional deaths per quarter "
      f"[{ci_low * mean_pop / 1e5:+.0f}, {ci_high * mean_pop / 1e5:+.0f}].")

pre_mean = ab.loc[ab["post"] == 0, "rate"].mean()
post_mean = ab.loc[ab["post"] == 1, "rate"].mean()
print(f"\nPre-COVID  mean rate (2016 Q1 – 2020 Q1): {pre_mean:.2f} per 100k per quarter")
print(f"Post-COVID mean rate (2020 Q2 onward):     {post_mean:.2f}")

# ---------------------------------------------------------------------------
# 4. Robustness — HAC lag sensitivity
# ---------------------------------------------------------------------------
print("\n========== HAC lag sensitivity (rate spec) ==========")
hac_table = []
for L in [1, 2, 3, 4, 6]:
    m = fit_seg(ab, dv="rate", hac_lags=L)
    p = m.params["post"]
    se = m.bse["post"]
    lo, hi = m.conf_int().loc["post"]
    hac_table.append((L, p, se, lo, hi, m.pvalues["post"]))
    print(f"  maxlags={L}: jump={p:+.2f}, SE={se:.2f}, 95% CI [{lo:+.2f}, {hi:+.2f}], p={m.pvalues['post']:.4f}")

# ---------------------------------------------------------------------------
# 5. Robustness — donut (drop transitional 2020 Q1)
# ---------------------------------------------------------------------------
ab_donut = ab[ab["Year_Quarter"] != "2020 Q1"].copy()
donut = fit_seg(ab_donut, dv="rate", hac_lags=3)
print("\n========== Donut robustness (drop 2020 Q1) ==========")
print(f"  jump: {donut.params['post']:+.2f}  "
      f"[95% CI {donut.conf_int().loc['post', 0]:+.2f}, "
      f"{donut.conf_int().loc['post', 1]:+.2f}]")

# ---------------------------------------------------------------------------
# 6. Robustness — placebo cutoffs in the pre-period
#    Fit the same model on pre-cutoff data only, using a fake cutoff.
#    A credible design should produce small / non-significant jumps here.
# ---------------------------------------------------------------------------
print("\n========== Placebo cutoffs (using only 2016 Q1 – 2020 Q1 data) ==========")
pre_only = ab[ab["t"] < CUTOFF].copy()
placebo_results = []
for fake_t in [2018.0, 2018.25, 2018.50, 2018.75, 2019.0, 2019.25, 2019.50]:
    d = pre_only.copy()
    d["centered_t"] = d["t"] - fake_t
    d["post"] = (d["t"] >= fake_t).astype(int)
    d["centered_t_post"] = d["centered_t"] * d["post"]
    if d["post"].sum() < 3 or (d["post"] == 0).sum() < 3:
        continue
    m = smf.ols("rate ~ centered_t + post + centered_t_post + C(q)", data=d).fit(
        cov_type="HAC", cov_kwds={"maxlags": 2, "use_correction": True}
    )
    p_est = m.params["post"]
    p_pval = m.pvalues["post"]
    placebo_results.append((fake_t, p_est, p_pval))
    label = f"{int(fake_t)} Q{int(round((fake_t % 1) * 4)) + 1}"
    print(f"  Fake cutoff {label}: jump={p_est:+.3f} per 100k, p={p_pval:.3f}")

# Real estimate vs placebo distribution
print(f"\nReal estimate at 2020 Q2: {jump:+.2f} per 100k.")
print(f"Largest placebo jump (absolute): "
      f"{max(abs(p[1]) for p in placebo_results):.3f} per 100k.")

# ---------------------------------------------------------------------------
# 7. Negative binomial cross-check on raw counts with log population offset
# ---------------------------------------------------------------------------
print("\n========== NB GLM cross-check (counts with log-pop offset) ==========")
nb = smf.glm(
    "deaths ~ centered_t + post + centered_t_post + C(q)",
    data=ab,
    family=sm.families.NegativeBinomial(),
    offset=np.log(ab["pop"]),
).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
print(f"  post coef (log rate ratio): {nb.params['post']:.4f}")
print(f"  rate ratio: exp(post) = {np.exp(nb.params['post']):.3f}  "
      f"i.e. post-period rate is {(np.exp(nb.params['post']) - 1) * 100:+.1f}% relative to pre-period at cutoff")
print(f"  95% CI: [{np.exp(nb.conf_int().loc['post', 0]):.3f}, "
      f"{np.exp(nb.conf_int().loc['post', 1]):.3f}]")

# ---------------------------------------------------------------------------
# 8. Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 5.5))

ax.scatter(ab["t"], ab["rate"], s=40, color="#2b2b2b", zorder=3, label="Observed quarter")

# Predict at each observed point — model includes quarter FE so fitted values
# carry the seasonal pattern.
ab["fit"] = main.predict(ab)

t_pre = ab[ab["post"] == 0].sort_values("t")
t_post = ab[ab["post"] == 1].sort_values("t")
ax.plot(t_pre["t"], t_pre["fit"], color="#1f6fb4", linewidth=2.2, label="Pre-COVID fit (incl. seasonality)")
ax.plot(t_post["t"], t_post["fit"], color="#c0392b", linewidth=2.2, label="Post-COVID fit (incl. seasonality)")
ax.axvline(CUTOFF, color="#7f7f7f", linestyle="--", linewidth=1, alpha=0.7)
ax.text(CUTOFF + 0.08, ab["rate"].max() * 0.97,
        "Public health emergency\n(2020 Q2)",
        fontsize=9, color="#555", va="top")

ax.set_title("Alberta opioid deaths per 100,000 residents, 2016-present", fontsize=13, pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("Deaths per 100,000 per quarter")
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
ax.grid(True, axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper left", frameon=False)

footer = (
    f"Sources: PHAC Health Infobase substance-related harms data; StatCan Table 17-10-0009-01.\n"
    f"Level shift at 2020 Q2 (segmented regression with quarter FE, HAC SE 3-lag, small-sample correction): "
    f"{jump:+.2f} per 100k [95% CI {ci_low:+.2f}, {ci_high:+.2f}]."
)
fig.text(0.02, -0.02, footer, fontsize=8, color="#555", ha="left")

fig.tight_layout()
fig.savefig(os.path.join(OUT, "rdit_opioid_deaths.png"), dpi=180, bbox_inches="tight")
print(f"\nSaved chart: output/rdit_opioid_deaths.png")

# ---------------------------------------------------------------------------
# 9. Save results
# ---------------------------------------------------------------------------
with open(os.path.join(OUT, "results.txt"), "w") as f:
    f.write(f"Alberta opioid deaths — segmented regression / ITS results\n")
    f.write(f"Run date: {date.today()}\n")
    f.write("=" * 64 + "\n\n")
    f.write(f"Sample: {len(ab)} quarters ({ab['Year_Quarter'].iloc[0]} – {ab['Year_Quarter'].iloc[-1]})\n")
    f.write(f"Cutoff: 2020 Q2\n")
    f.write(f"Outcome: opioid deaths per 100,000 Alberta residents per quarter\n\n")

    f.write("Main spec (rate per 100k, segmented regression with quarter FE,\n")
    f.write("  HAC SE 3-lag, small-sample correction):\n")
    f.write(f"  level shift (post): {jump:+.2f} per 100k\n")
    f.write(f"  95% CI:             [{ci_low:+.2f}, {ci_high:+.2f}]\n")
    f.write(f"  p-value:            {main.pvalues['post']:.4f}\n")
    f.write(f"  pre-COVID slope:    {main.params['centered_t']:+.3f} per 100k/quarter "
            f"(p = {main.pvalues['centered_t']:.3f})\n")
    f.write(f"  At mean AB pop ({mean_pop:,.0f}) this is ~{jump * mean_pop / 1e5:+.0f} deaths/quarter\n\n")

    f.write("HAC lag sensitivity:\n")
    for L, p, se, lo, hi, pv in hac_table:
        f.write(f"  maxlags={L}: jump={p:+.2f}, SE={se:.2f}, 95% CI [{lo:+.2f}, {hi:+.2f}], p={pv:.4f}\n")
    f.write("\n")

    f.write("Donut robustness (drop transitional 2020 Q1):\n")
    f.write(f"  jump: {donut.params['post']:+.2f}  "
            f"[95% CI {donut.conf_int().loc['post', 0]:+.2f}, "
            f"{donut.conf_int().loc['post', 1]:+.2f}]\n\n")

    f.write("Placebo cutoffs (fit using only 2016 Q1 – 2020 Q1 data):\n")
    for fake_t, est, pval in placebo_results:
        label = f"{int(fake_t)} Q{int(round((fake_t % 1) * 4)) + 1}"
        f.write(f"  {label}: jump={est:+.3f} per 100k, p={pval:.3f}\n")
    f.write(f"  Real cutoff (2020 Q2):   jump={jump:+.2f} per 100k, p={main.pvalues['post']:.4f}\n")
    f.write(f"  Largest placebo |jump|:  {max(abs(p[1]) for p in placebo_results):.3f}\n\n")

    f.write("Negative binomial cross-check (counts, log-pop offset, quarter FE):\n")
    f.write(f"  post coef (log rate ratio): {nb.params['post']:.4f}\n")
    f.write(f"  rate ratio: {np.exp(nb.params['post']):.3f} "
            f"(95% CI [{np.exp(nb.conf_int().loc['post', 0]):.3f}, "
            f"{np.exp(nb.conf_int().loc['post', 1]):.3f}])\n")
    f.write(f"  → post-cutoff rate is {(np.exp(nb.params['post']) - 1) * 100:+.1f}% of pre-cutoff at cutoff\n\n")

    f.write(f"Pre-COVID mean rate:  {pre_mean:.2f} per 100k/quarter\n")
    f.write(f"Post-COVID mean rate: {post_mean:.2f} per 100k/quarter\n")

print("Saved results: output/results.txt")
print("\nDone.")
