# Alberta opioid deaths around COVID-19 — one-page brief

*Personal learning project, ~3 hours. Not affiliated with my employer.*

## The question

Did Alberta's opioid death rate shift at a level higher than the pre-COVID trend can explain, starting from 2020 Q2 (the first full quarter under Alberta's public health emergency)?

## What I did

Pulled federal public data (PHAC Health Infobase substance-related harms data, downloaded 2026-05-20) on Alberta opioid deaths by quarter, 2016 Q1 to 2025 Q3. Normalised to a rate per 100,000 Alberta residents using Statistics Canada quarterly population estimates so the result is not driven by population growth.

Fit a segmented regression — interrupted time series with a level and slope change around 2020 Q2, quarter fixed effects to absorb seasonality, Newey-West HAC standard errors with small-sample correction.

Ran four robustness checks: HAC lag sensitivity (L = 1, 2, 3, 4, 6), a donut spec (drop transitional 2020 Q1), seven placebo cutoffs in the pre-period, and a negative binomial GLM cross-check with a log-population offset.

## What I found

| | Pre-COVID (2016 Q1 – 2020 Q1) | Post-COVID (2020 Q2 onward) |
| --- | --- | --- |
| Mean deaths per 100k per quarter | 4.05 | 7.99 |

The level shift at the cutoff is **+5.50 deaths per 100k per quarter** (95% CI +3.60, +7.39, p < 0.001). At mean Alberta population that is about +246 deaths per quarter. The negative binomial cross-check gives a rate ratio of 2.43 (95% CI 1.80, 3.26) — post-cutoff rate is roughly 2.4× the pre-cutoff rate.

Pre-period slope is flat (−0.02, p = 0.94), so the jump is not part of an existing trend. Donut robustness moves the estimate by less than 3%. All seven placebo cutoffs in the pre-period give jumps in the opposite direction with absolute values at most one third the real estimate.

## What this is — and isn't

The design identifies a sharp, large, robust break in the data at 2020 Q2. It does **not** identify COVID-19 as the cause. Several things shifted at that cutoff at the same time: the virus itself, public health emergency response, supply chain for the unregulated drug supply, harm reduction service capacity, mental health services, social isolation, and an economic shock. Any of these could explain part of the break.

To net out COVID specifically from the policy-and-supply bundle, a difference-in-discontinuities using other provinces with different pandemic-response timing would be the next step. Stratification by age, sex, and zone, and a substance-type decomposition (fentanyl, carfentanil, other), would also sharpen the picture.

Repo: [github.com/Adilbek123/alberta-substance-use-trends](https://github.com/Adilbek123/alberta-substance-use-trends).
