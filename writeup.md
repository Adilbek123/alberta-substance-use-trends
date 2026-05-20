# Alberta opioid mortality around the COVID-19 onset

**Adilbek Sultanov · independent project · May 2026**

## Headline

Alberta's opioid death rate roughly doubled when COVID-19 hit in 2020 Q2 — from about 4 to about 8 deaths per 100,000 residents per quarter — and stayed at the higher level for years. The shift is sharp, large, and survives every robustness check applied to it. The most honest reading is that the pandemic and the bundle of changes it brought together (supply, services, isolation, economic shock) shifted opioid mortality; the analysis cannot, and does not try to, separate the virus channel from everything else COVID-19 produced.

## Background

Before COVID-19, Alberta's opioid death rate had been flat for five years at roughly 4 per 100,000 per quarter. In March 2020 the province declared a public health emergency, and federal data shows opioid mortality rose sharply across Canada from that point. The Ministry of Mental Health and Addiction is now transforming Alberta's system to the Recovery Model. Understanding the size and shape of the post-COVID shift is a prerequisite for measuring progress against that baseline.

## Question

Did Alberta's opioid death rate shift at a level higher than the pre-COVID trend can explain, starting from 2020 Q2 (the first full quarter under the public health emergency)?

## Approach

This is an interrupted time series. The model fits one trend to the pre-COVID period and one to the post-COVID period, and measures the level gap between them at the cutoff. The outcome is a rate per 100,000 residents (to keep population growth from contaminating the result), with quarter-of-year adjustments to absorb seasonal patterns. Three robustness checks support the headline: placebo cutoffs placed in the pre-period (no jump found), dropping the transitional quarter (estimate unchanged), and a count-model cross-check (consistent rate-ratio result).

## Data

Two public sources. Quarterly opioid deaths in Alberta come from the Public Health Agency of Canada's Health Infobase, downloaded 20 May 2026 and covering 2016 Q1 through 2025 Q3. Population denominators come from Statistics Canada Table 17-10-0009-01. No internal Government of Alberta data is used.

## Findings

The level shift at the cutoff is about 5.5 deaths per 100,000 per quarter — roughly a doubling of the pre-COVID rate — with a 95 percent confidence interval of [3.6, 7.4] and a p-value well under 0.001. At Alberta's average population over the period that translates to roughly 240 additional deaths per quarter. The pre-COVID slope is flat, so the jump is not a continuation of an existing trend. The count-model cross-check returns a rate ratio of 2.4, meaning the post-COVID rate is about 2.4× the pre-COVID rate at the cutoff. Placebo cutoffs in 2018 and 2019 produce no comparable jump (largest about a third of the real estimate, in the opposite direction). Dropping the quarter that straddles the cutoff moves the estimate by less than 3 percent.

## What this identifies — and what it does not

What the estimate captures is the **total effect of the COVID-19 pandemic on Alberta opioid mortality**, including supply chain disruption in the unregulated drug supply, reduced harm reduction service capacity, mental health service disruption, social isolation, and the economic shock. These are downstream consequences of the pandemic, not parallel causes that happened to align. A pandemic without those responses is not a counterfactual that exists in any data.

What the analysis does not do is decompose that total into its component channels. It cannot tell us what share came from supply toxicity versus service capacity versus isolation versus the economic shock. A peer-province comparison would not fix this, because every province faced COVID and its policy response at essentially the same time — the comparison would identify Alberta-specific deviation, not a clean "virus-only" channel.

## So what

For the Ministry of Mental Health and Addiction, three things follow. First, the post-COVID baseline is materially different from the pre-COVID baseline, and any measure of progress under the Recovery Model needs to account for that. Second, the trajectory is not flat: the post-COVID period peaked in 2021 Q4 and has been declining since 2024, so a single average masks a real recovery already underway. Third, the realistic next analytical steps are decomposition (what share of the shift came from which channel) and heterogeneity (which age groups, zones, and substance types drove it) — not better identification of "COVID per se", which the data structure does not allow.

## Reproducing

Code, data, and full documentation are at [github.com/Adilbek123/alberta-substance-use-trends](https://github.com/Adilbek123/alberta-substance-use-trends). The walkthrough notebook (`walkthrough.ipynb`) reproduces each step with plain-language commentary on the decisions and trade-offs.
