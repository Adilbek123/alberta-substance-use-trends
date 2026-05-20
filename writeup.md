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

## What this identifies — and what it doesn't

The estimate captures the **total effect of the COVID-19 pandemic** on Alberta opioid mortality — including the bundle of policy and social responses the pandemic produced (border closures and supply-chain disruption in the unregulated drug supply, reduced harm-reduction service capacity, mental-health service disruption, social isolation, the economic shock). These are downstream consequences of COVID, not parallel causes that happened to align. A pandemic without those responses is not a counterfactual that exists in any data.

What the design does not do is decompose that total into its component channels — what share came from supply toxicity, what from service capacity loss, what from isolation, what from the economic shock. That is a mechanism-level question that needs separate work.

A peer-province comparison would not fix this. All provinces faced COVID and its policy response at essentially the same time, so comparing Alberta to BC or Ontario would identify Alberta-specific deviation from the common pandemic pattern, not a clean "COVID-only" channel.

The realistic next steps are mechanism decomposition (supply-side, service-capacity, and outcome signals triangulated), heterogeneity (age, sex, zone, substance type), explicit modelling of the rise-and-decline shape of the post-period, and cumulative excess deaths through end-of-sample.

Repo: [github.com/Adilbek123/alberta-substance-use-trends](https://github.com/Adilbek123/alberta-substance-use-trends).
