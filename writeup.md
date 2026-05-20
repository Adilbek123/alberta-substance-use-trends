# Alberta opioid mortality around the COVID-19 onset

**Adilbek Sultanov · independent project · May 2026**

## Background

Alberta has been responding to an opioid crisis since the mid-2010s, when fentanyl emerged in the unregulated drug supply and largely replaced earlier prescription-opioid harms. In 2016 the province recorded 611 apparent opioid-related deaths. In May 2017 the provincial government established a Minister's Opioid Emergency Response Commission under the Public Health Act. By the second half of the decade Alberta's opioid mortality had stabilised at a high level: the quarterly opioid death rate sat around 4 per 100,000 residents from 2016 through early 2020 (roughly 170-200 deaths per quarter), with no sustained upward or downward trend over that four-year period. This is the pre-COVID baseline used in this analysis.

In March 2020 the COVID-19 pandemic intersected with the existing opioid crisis. The World Health Organization characterized COVID-19 as a pandemic on 11 March 2020; Alberta declared a provincial public health emergency on 17 March 2020. Federal data shows opioid mortality rose sharply across Canada from 2020 onward. The size and timing of Alberta's specific shift have not been quantified at this resolution in publicly available analysis.

## Question

Did Alberta's opioid death rate jump at the COVID-19 onset, and is that jump real or noise?

Two things matter here for policy. First, the size of any shift sets the post-COVID baseline against which progress under the Alberta Recovery Model will be measured. Second, whether the shift is real (as opposed to random variation in a noisy series) determines whether it is something that should be acted on. Alberta opioid mortality sat around 4 deaths per 100,000 residents per quarter from 2016 through early 2020, with no sustained rise or fall.

## Approach

The method is an interrupted time series, also called segmented regression. It fits one trend to the pre-COVID years and another to the post-COVID years, measures the gap between them at the cutoff (2020 Q2, the first full quarter under Alberta's public health emergency), and tests whether the gap is meaningfully larger than the natural noise in the data. Opioid death counts come from the Public Health Agency of Canada's Health Infobase. Population denominators come from Statistics Canada Table 17-10-0009-01, used to convert counts to a rate per 100,000. Three robustness checks support the result: placebo cutoffs placed in the pre-period (which should produce no jump if the design is credible), dropping the quarter that straddles the cutoff and refitting, and a cross-check using a count model with a population offset. No internal Government of Alberta data is used.

## Findings

The level shift at the cutoff is about 5.5 deaths per 100,000 per quarter, with a 95 percent confidence interval of 3.6 to 7.4 and a p-value well below 0.001. The pre-COVID rate of about 4 per 100,000 roughly doubled to about 8. At Alberta's average population over the period this corresponds to roughly 240 additional deaths per quarter. The pre-COVID slope is flat, so the jump is not a continuation of an existing trend. The count-model cross-check produces a rate ratio of 2.4, consistent with the rate-based estimate. Placebo cutoffs in 2018 and 2019 produce no comparable jump (the largest is about a third of the real estimate, in the opposite direction). Dropping the quarter that straddles the cutoff moves the estimate by less than 3 percent.

## What this identifies, and what it does not

What the estimate captures is the total effect of the COVID-19 pandemic on Alberta opioid mortality, including the bundle of downstream changes the pandemic brought together: supply chain disruption in the unregulated drug market, reduced harm reduction service capacity, mental health and addiction service disruption, social isolation, and the economic shock. These are downstream consequences of the pandemic, not parallel causes that happened to align. A pandemic without those responses is not a counterfactual that exists in any data.

What the analysis does not do is decompose that total into its component channels. It cannot tell us what share came from supply toxicity versus service capacity versus isolation versus the economic shock. That is a mechanism-level question and needs different data. Comparing Alberta to peer provinces would not fix this, because every Canadian province faced COVID and its policy response at essentially the same time; the comparison would identify Alberta-specific deviation from the common pattern, not a clean virus-only effect.

## So what

For Mental Health and Addiction work three things follow. First, the post-COVID baseline is materially different from the pre-COVID baseline, and any Recovery Model performance measurement needs to be explicit about which baseline it is comparing to. Second, the post-COVID trajectory is not flat: it peaked in 2021 Q4 and has been declining since 2024, so a real recovery is already visible in the data. Third, the realistic next analytical work is decomposition (what share of the shift came from which channel) and heterogeneity (which age groups, zones, and substance types drove it), rather than better identification of "COVID per se," which the structure of the data does not allow.

## Reproducing

Code, data, and full documentation are at [github.com/Adilbek123/alberta-substance-use-trends](https://github.com/Adilbek123/alberta-substance-use-trends). The walkthrough notebook reproduces every step with plain-language commentary on the decisions and trade-offs.
