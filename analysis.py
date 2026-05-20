"""
Alberta opioid mortality: regression discontinuity in time around COVID-19 onset
================================================================================

Question: Did Alberta's opioid death rate shift at a level higher than the
pre-COVID trend can explain, starting from 2020 Q2?

Method: regression discontinuity in time (RDiT). Fit separate linear trends
to pre- and post-COVID periods. Estimate the jump at the cutoff with 95% CI.

Data: Public Health Agency of Canada, Health Infobase, Substance-Related
Harms Data (downloaded 2026-05-20). Alberta opioid deaths by quarter, 2016 Q1
to most recent available quarter.

Cutoff: 2020 Q2 (first full quarter under public health emergency in Alberta;
PHE declared 2020-03-17).

Limitations are listed in README.md.
"""

import os
import csv
from datetime import date

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ---------------------------------------------------------------------------
# 1. Load
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "SubstanceHarmsData.csv")
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(DATA)

# Keep Alberta, opioid deaths, quarterly, overall (no demographic disagg)
ab = df[
    (df["Region"] == "Alberta")
    & (df["Substance"] == "Opioids")
    & (df["Source"] == "Deaths")
    & (df["Time_Period"] == "By quarter")
    & (df["Specific_Measure"] == "Overall numbers")
    & (df["Disaggregator"].isna())
    & (df["Unit"] == "Number")
].copy()

# Parse year and quarter
ab[["year", "q"]] = ab["Year_Quarter"].str.extract(r"(\d{4})\s*Q(\d)").astype(int)
ab["t"] = ab["year"] + (ab["q"] - 1) / 4.0           # quarter as a continuous time variable
ab["deaths"] = ab["Value"].astype(float)
ab = ab.sort_values("t").reset_index(drop=True)

print(f"Quarters: {len(ab)}   range: {ab['Year_Quarter'].iloc[0]} -> {ab['Year_Quarter'].iloc[-1]}")
print(ab[["Year_Quarter", "deaths"]].to_string(index=False))

# ---------------------------------------------------------------------------
# 2. RDiT specification
# ---------------------------------------------------------------------------
# Cutoff: 2020 Q2 = t=2020.25. PHE declared 2020-03-17 (mid-Q1), but Q1 covers
# almost entirely pre-emergency operating conditions. First full COVID-affected
# quarter is Q2, so treat Q2 as the first post period.
CUTOFF = 2020.25
ab["centered_t"] = ab["t"] - CUTOFF
ab["post"] = (ab["t"] >= CUTOFF).astype(int)
ab["centered_t_post"] = ab["centered_t"] * ab["post"]

X = ab[["centered_t", "post", "centered_t_post"]]
X = sm.add_constant(X)
y = ab["deaths"]

# HAC standard errors with 4-quarter lag (account for quarterly autocorrelation)
model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
print()
print(model.summary())

jump = model.params["post"]
jump_se = model.bse["post"]
jump_ci_low, jump_ci_high = model.conf_int().loc["post"]

print()
print("Jump at 2020 Q2 cutoff:")
print(f"  point estimate: {jump:.1f} additional opioid deaths per quarter")
print(f"  95% CI (HAC):   [{jump_ci_low:.1f}, {jump_ci_high:.1f}]")

# Pre- and post-period mean for context
pre_mean = ab.loc[ab["post"] == 0, "deaths"].mean()
post_mean = ab.loc[ab["post"] == 1, "deaths"].mean()
print(f"  pre-COVID mean (2016 Q1-2020 Q1):  {pre_mean:.0f} deaths/quarter")
print(f"  post-COVID mean (2020 Q2 onward):  {post_mean:.0f} deaths/quarter")
print(f"  raw difference of means:           {post_mean - pre_mean:+.0f}")

# ---------------------------------------------------------------------------
# 3. Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.2))

ax.scatter(ab["t"], ab["deaths"], s=40, color="#2b2b2b", zorder=3, label="Observed quarter")

# Fitted lines
t_pre = np.linspace(ab["t"].min(), CUTOFF, 50)
t_post = np.linspace(CUTOFF, ab["t"].max(), 50)

x_pre = pd.DataFrame({"const": 1.0, "centered_t": t_pre - CUTOFF, "post": 0, "centered_t_post": 0.0})
x_post = pd.DataFrame({"const": 1.0, "centered_t": t_post - CUTOFF, "post": 1, "centered_t_post": t_post - CUTOFF})
y_pre = model.predict(x_pre[["const", "centered_t", "post", "centered_t_post"]])
y_post = model.predict(x_post[["const", "centered_t", "post", "centered_t_post"]])

ax.plot(t_pre, y_pre, color="#1f6fb4", linewidth=2.2, label="Pre-COVID trend")
ax.plot(t_post, y_post, color="#c0392b", linewidth=2.2, label="Post-COVID trend")
ax.axvline(CUTOFF, color="#7f7f7f", linestyle="--", linewidth=1, alpha=0.7)
ax.text(CUTOFF + 0.05, ab["deaths"].max() * 0.97,
        "Public health emergency\n(2020 Q2)",
        fontsize=9, color="#555")

ax.set_title("Alberta opioid deaths per quarter, 2016-present", fontsize=13, pad=12)
ax.set_xlabel("Quarter")
ax.set_ylabel("Opioid-related deaths")
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
ax.grid(True, axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper left", frameon=False)

footer = (
    f"Source: Public Health Agency of Canada, Health Infobase substance-related harms data. "
    f"Cutoff = 2020 Q2.\n"
    f"Estimated jump at cutoff (HAC SE, 4-quarter lag): "
    f"{jump:+.0f} deaths/quarter [95% CI {jump_ci_low:+.0f}, {jump_ci_high:+.0f}]."
)
fig.text(0.02, -0.02, footer, fontsize=8, color="#555", ha="left")

fig.tight_layout()
fig.savefig(os.path.join(OUT, "rdit_opioid_deaths.png"), dpi=180, bbox_inches="tight")
print(f"\nSaved chart: output/rdit_opioid_deaths.png")

# ---------------------------------------------------------------------------
# 4. Robustness: drop transitional Q (2020 Q1) — donut RDiT
# ---------------------------------------------------------------------------
# PHE declared 2020-03-17 cuts Q1 ~80/20 pre/during. Drop Q1 2020 as the
# "donut" and re-fit to check whether the jump estimate is sensitive to its
# inclusion.
ab_donut = ab[ab["Year_Quarter"] != "2020 Q1"].copy()
ab_donut["centered_t"] = ab_donut["t"] - CUTOFF
ab_donut["post"] = (ab_donut["t"] >= CUTOFF).astype(int)
ab_donut["centered_t_post"] = ab_donut["centered_t"] * ab_donut["post"]

Xd = sm.add_constant(ab_donut[["centered_t", "post", "centered_t_post"]])
yd = ab_donut["deaths"]
model_donut = sm.OLS(yd, Xd).fit(cov_type="HAC", cov_kwds={"maxlags": 4})

print()
print("Robustness check: donut RDiT (drop 2020 Q1)")
print(f"  Jump estimate: {model_donut.params['post']:+.1f} "
      f"[95% CI {model_donut.conf_int().loc['post', 0]:+.1f}, "
      f"{model_donut.conf_int().loc['post', 1]:+.1f}]")

# Save results JSON-ish text for README
with open(os.path.join(OUT, "results.txt"), "w") as f:
    f.write(f"Alberta opioid deaths RDiT results — run {date.today()}\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Quarters in sample: {len(ab)} ({ab['Year_Quarter'].iloc[0]} – {ab['Year_Quarter'].iloc[-1]})\n")
    f.write(f"Cutoff: 2020 Q2\n\n")
    f.write(f"Main specification (full sample, HAC SE 4-lag):\n")
    f.write(f"  jump at cutoff: {jump:+.1f} deaths/quarter\n")
    f.write(f"  95% CI:         [{jump_ci_low:+.1f}, {jump_ci_high:+.1f}]\n")
    f.write(f"  p-value:        {model.pvalues['post']:.4f}\n\n")
    f.write(f"Donut robustness (drop 2020 Q1):\n")
    f.write(f"  jump at cutoff: {model_donut.params['post']:+.1f}\n")
    f.write(f"  95% CI:         [{model_donut.conf_int().loc['post', 0]:+.1f}, "
            f"{model_donut.conf_int().loc['post', 1]:+.1f}]\n\n")
    f.write(f"Pre-COVID mean:   {pre_mean:.0f} deaths/quarter\n")
    f.write(f"Post-COVID mean:  {post_mean:.0f} deaths/quarter\n")
    f.write(f"Difference:       {post_mean - pre_mean:+.0f}\n")

print(f"Saved results: output/results.txt")
print("\nDone.")
