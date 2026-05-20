# Alberta opioid mortality and COVID-19: regression discontinuity in time

A short personal analysis of how Alberta's opioid death rate shifted around
the COVID-19 onset, using federal data and a regression discontinuity in
time (RDiT) specification.

This is a learning project I built in an afternoon to refresh my hands-on
work with time-series policy data. It is not affiliated with my employer
and does not use any internal data.

## Question

Did Alberta's opioid death rate shift at a level higher than the pre-COVID
trend can explain, starting from 2020 Q2?

## Data

Public Health Agency of Canada, Health Infobase, Substance-Related Harms
Data (`SubstanceHarmsData.csv`). Downloaded 2026-05-20 from
[health-infobase.canada.ca](https://health-infobase.canada.ca/substance-related-harms/opioids-stimulants/).

I use a single slice: Alberta, opioids, deaths, quarterly counts,
overall (no demographic disaggregation). 39 quarters, 2016 Q1 to 2025 Q3.

The full raw file is included under `data/` for reproducibility.

## Method

Regression discontinuity in time around the 2020 Q2 cutoff:

```
deaths_t  =  α  +  β1·(t − cutoff)  +  β2·post  +  β3·(t − cutoff)·post  +  ε
```

- `post = 1` if `t ≥ 2020 Q2`, else `0`.
- `cutoff = 2020 Q2` (first full quarter under the public health emergency
  declared 2020-03-17).
- HAC standard errors (Newey-West, 4-quarter lag) to handle autocorrelation.
- Robustness: I also re-fit dropping 2020 Q1 (the transitional quarter that
  straddles the cutoff) — a "donut" specification.

`β2` is the discontinuity at the cutoff, i.e. the level shift in opioid
deaths attributable to the pre/post change after accounting for the existing
trend.

## Findings

| Quantity | Estimate |
| --- | --- |
| Pre-COVID mean (2016 Q1 – 2020 Q1) | 173 deaths / quarter |
| Post-COVID mean (2020 Q2 onward) | 369 deaths / quarter |
| Jump at cutoff (main spec, HAC SE) | **+235 deaths / quarter** [95% CI +165, +306], p < 0.001 |
| Jump at cutoff (donut spec, drop 2020 Q1) | +230 [95% CI +163, +298] |
| Pre-COVID slope | +2.3 deaths / quarter (not significant, p = 0.76) |

The pre-COVID period is roughly flat, so the jump is not part of an
existing trend. The donut robustness check moves the estimate by less than
2%.

The post-cutoff period also looks like it peaked in 2021 Q4 and has been
trending down since 2024. The RDiT here measures the level shift at the
cutoff, not the longer dynamics.

![RDiT chart](output/rdit_opioid_deaths.png)

## Limitations (important)

- **Not a causal identification of COVID-19 itself.** RDiT requires that no
  other major changes happened sharply at the same cutoff that affected
  the outcome through other channels. In March 2020 many things moved at
  once: supply chains for unregulated drugs, harm-reduction service
  availability, employment, housing, and mental health service capacity.
  The estimate captures the bundled effect of "the world before March 2020
  vs after," not a clean COVID-only effect.
- **Single cutoff, no donor pool.** A stronger design would use other
  provinces with different pandemic-response timing as comparators
  (difference-in-discontinuities), or a synthetic control. I did not build
  that here.
- **No demographic stratification.** Alberta-level totals mask substantial
  age, sex, and zone heterogeneity that any real Ministry analysis would
  surface.
- **No fentanyl decomposition.** A natural follow-up is to break the post-
  COVID jump into the share driven by composition change in the unregulated
  supply (fentanyl share, carfentanil emergence) vs uptake of
  pharmaceutical opioids.
- **Reporting lag and revisions.** Health Infobase notes the data is
  subject to revision; the most recent quarters may move.

## What I would do next

1. Add other provinces and run a difference-in-discontinuities to net out
   the common COVID shock from the Alberta-specific level.
2. Decompose the post-cutoff total into substance type (fentanyl /
   carfentanil / other opioids) using the `Type of opioids` rows in the
   same dataset.
3. Add EMS responses and ED visits as parallel outcomes — these have
   different reporting lag and different selection into the data, and
   triangulating across them strengthens the inference.
4. Stratify by age and sex to identify which cohorts drove the post-COVID
   level shift.

## Reproducing

```
pip install pandas statsmodels matplotlib numpy
python analysis.py
```

Output goes to `output/rdit_opioid_deaths.png` and `output/results.txt`.

## License

Code: MIT. Data: redistributed under the Public Health Agency of Canada's
open data terms.
