# Alberta opioid mortality around the COVID-19 onset

**Adilbek Sultanov · independent project · May 2026**

## Background

Alberta has been responding to an opioid crisis since the mid-2010s, when fentanyl emerged in the unregulated drug supply and largely replaced earlier prescription-opioid harms. In 2016 the province recorded 611 apparent opioid-related deaths. In May 2017 the provincial government established a Minister's Opioid Emergency Response Commission under the Public Health Act. By the second half of the decade Alberta's opioid mortality had stabilised at a high level: the quarterly opioid death rate sat around 4 per 100,000 residents from 2016 through early 2020 (roughly 170-200 deaths per quarter), with no sustained upward or downward trend over that four-year period. This is the pre-COVID baseline used in this analysis.

In March 2020 the COVID-19 pandemic intersected with the existing opioid crisis. The World Health Organization characterized COVID-19 as a pandemic on 11 March 2020; Alberta declared a provincial public health emergency on 17 March 2020. Federal data shows opioid mortality rose sharply across Canada from 2020 onward. The size and timing of Alberta's specific shift have not been quantified at this resolution in publicly available analysis.

## Research question

Did Alberta's opioid death rate shift at the COVID-19 cutoff (2020 Q2, the first full quarter under the public health emergency) in a way the pre-COVID period cannot explain? The pre-COVID years give us a model of how the rate behaved (level, trend, seasonality); extrapolating that model forward gives a counterfactual for what we would expect after the cutoff if nothing had changed. The question is whether the observed post-cutoff data are inconsistent with that extrapolation.

## Approach

To answer this I used interrupted time series, also called segmented regression. The method directly tests for a level shift at a known cutoff: it estimates the pre-cutoff trajectory (intercept and slope), the level gap at the cutoff, and any change in trajectory after the cutoff. The pre-period model extrapolated forward serves as the counterfactual. Opioid death counts come from the Public Health Agency of Canada's Health Infobase. Population denominators come from Statistics Canada Table 17-10-0009-01, used to convert counts to a rate per 100,000 so the result is not driven by Alberta's roughly 12 percent population growth over the period. No internal Government of Alberta data is used. Four robustness checks support the main estimate: placebo cutoffs in the pre-period (which generate a reference distribution for how big a "jump" the model finds when nothing has happened), HAC lag sensitivity (so inference does not depend on a single tuning choice), a donut specification (drop the partial-exposure quarter 2020 Q1), and a negative binomial cross-check with a population offset (tests both the linear functional form and the OLS Gaussian assumption against a count model).

## Findings

The level shift at the cutoff is about +5.5 deaths per 100,000 per quarter, with a 95 percent confidence interval of +3.6 to +7.4 and a p-value below 0.001. The pre-COVID slope is essentially zero (p = 0.94), so the jump is not a continuation of an existing trend. The rate moved from approximately 4 per 100,000 pre-COVID to approximately 9.5 immediately post-cutoff, roughly a doubling; the negative binomial cross-check returns a rate ratio of 2.4, consistent with this. At Alberta's average population over the period, the shift translates to roughly 246 additional deaths per quarter evaluated at the cutoff (the cumulative post-period total is larger but is a separate calculation). Placebo cutoffs in the pre-period (seven fake cutoffs in 2018-2019) maxed out at about one third of the real estimate and pointed in the opposite direction; the real shift is far outside the placebo distribution. HAC lag sensitivity is stable across lag choices, the donut estimate moves by less than 3 percent, and the count-model cross-check confirms the rate-ratio interpretation.

## What this identifies, and what it does not

The analysis identifies the level shift at 2020 Q2 that the pre-period trend and seasonality cannot explain. That is what the statistics support directly. I interpret that shift as the total joint effect of the COVID-19 pandemic bundle: virus circulation, the public health emergency response, drug supply chain disruption, harm reduction service capacity, mental health and addiction service capacity, social isolation, and the economic shock. These are downstream consequences of the pandemic, not parallel causes that happened to align. This is an interpretive choice, not a statistical claim: the design cannot separate the channels, and the channels cannot meaningfully be removed from "COVID" without losing the concept itself.

The analysis does not identify which channel caused most of the damage. That is a different question, at the mechanism level, and would need different data: drug-checking composition, service utilization records, fentanyl share of toxicology, and so on. Comparing Alberta to other provinces would not solve this, because every Canadian province faced COVID and its policy response at essentially the same time; the comparison would identify Alberta-specific deviation from the common pattern, not the virus channel alone.

The post-cutoff series has been declining since 2024. This analysis does not formally test that decline; doing so is a natural next step.

## So what

For Mental Health and Addiction work three things follow. First, the post-COVID baseline is materially different from the pre-COVID baseline, and any Recovery Model performance measurement needs to be explicit about which baseline (pre-COVID, post-cutoff peak, or current) it compares to. Second, the post-cutoff trajectory is not flat: it peaked in 2021 Q4 and has been declining since 2024, so a real recovery may already be underway, though that decline is not formally tested here. Third, the realistic next analytical work is decomposition (what share of the shift came from which channel) and heterogeneity (which age groups, zones, and substance types drove it), rather than better identification of "COVID per se," which the structure of the data does not allow.

## Reproducing

Code, data, and full documentation are at [github.com/Adilbek123/alberta-substance-use-trends](https://github.com/Adilbek123/alberta-substance-use-trends). The walkthrough notebook reproduces every step with plain-language commentary on the decisions and trade-offs.
