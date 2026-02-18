---
source: ethresearch
topic_id: 21712
title: Opinion Article Scoring System
author: murraci
date: "2025-02-10"
category: Applications
tags: []
url: https://ethresear.ch/t/opinion-article-scoring-system/21712
views: 140
likes: 0
posts_count: 1
---

# Opinion Article Scoring System

Here I propose a system for scoring media opinion articles. It is part prediction markets - as there is a small amount of money involved - and part forecasting science mechanism design. Journalists that publish an article on the platform must do so with an accompanying stake. Readers (whether human or AI) that wish to pass judgment on the merits of the main opinion must pay a small fee/tip for the right to do so. The overall aggregated reader score dictates how much of the stake (and tips) the writer receives. The remainder is sent to the protocol’s global funding pool meaning the protocol takes the other side. Readers are scored by a separate mechanism where honest responses are a Nash equilibrium. They are incentivised to participate as star performers are eligible for monthly rebates from the protocol. Many readers won’t be well calibrated and many might tip without participating in the forecasting competition/market simply because they like the article. They will subsidise the insightful bettors.

### Brief summary of the relevant forecasting literature

Most opinion piece articles involve unverifiable predictions. However, we can settle markets without a resolving exogenous event or ground truth using [peer-prediction](https://www.nature.com/articles/nature21054) based mechanisms. This enables us to create and settle markets for questions that won’t have answers for some time or for counterfactual type questions. Individuals can be scored for being both [well-calibrated and honest](https://www.science.org/doi/10.1126/science.1102081) ensuring incentive compatibility and the avoidance of a Keynesian Beauty Contest. Aggregated forecasts work best when good [track records are upweighted and the aggregate is extremised](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/are-markets-more-accurate-than-polls-the-surprising-informational-value-of-just-asking/B78F61BC84B1C48F809E6D408903E66D). A track record shows good general forecasting ability whereas a divergence between what one forecasts themselves and what they predict the crowd will forecast (their meta prediction) is a strong signal of [domain-specific expertise](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0232058#:~:text=A%20common%20approach%20to%20improving,a%20large%20collection%20of%20500).

Based on this literature I present an opinion article scoring mechanism based on the meta-probability weighting with a track record upweighter added as Bayesian Truth Serum scores will be tracked in protocol. This enables us to account for both types of expertise and extremise the aggregate. Prelec et al’s BTS mechanism is itself adapted for continuous probabilities and made robust to small sample sizes. We will still probably require a minimum of 10 respondents to score any article and reader. We expect a high prevalence of AI agents on the system to compete for the protocol payouts so this shouldn’t be a problem.

# Agent Reports

There are n agents, indexed by i = 1, \dots, n. Each agent i reports:

- A primary report p_i \in [0,1].
- A meta‐prediction m_i \in [0,1], which represents agent i's guess of the group average \bar{p}

*In english, respondents are asked:*

*1. What do you think the chances are that this opinion is correct?*

*2. What do you think the average answer will be for question 1?*

# 1. Article Score

### Domain Specific Expertise (MPW Divergence)

For each respondent i, let

D_i = |p_i - m_i|

where:

- p_i is the respondent’s probability that the main opinion is correct, and
- m_i is the respondent’s meta‐prediction of the group’s average probability.

**Rationale:** The idea is that if a respondent’s own opinion differs significantly from what they expect the crowd to believe, that divergence is taken as an indicator of potential domain-specific insight.

### Track Record

Each respondent’s historical performance is expressed as a percentile rank PR_i (with values between 0 and 1, where 0.5 represents the median performance). This is then incorporated via a multiplier:

TR_i = 1 + \beta \,(PR_i - 0.5)

Here, \beta is a variable parameter that we can calibrate. For example, with \beta = 1, a respondent with a perfect track record (PR_i = 1) would have M_i = 1.5 while one with the lowest rank (PR_i = 0) would have M_i = 0.5.

**Rationale:** The track record multiplier adjusts the influence of the divergence component based on past performance. Those with a good track record *and* a high divergence will be heavily upweighted as they are showing two valuable signals.

### Combined Weight

For each respondent, combine the divergence and track record components multiplicatively:

w'_i = D_i \times TR_i = |p_i - m_i| \times [1 + \beta \,(PR_i - 0.5)]

### Normalisation of Weights

To ensure that all weights sum to 1, normalize the unnormalized weights:

w_i = \frac{w'_i}{\sum_{j} w'_j} = \frac{|p_i - m_i| \times [1 + \beta \,(PR_i - 0.5)]}{\sum_{j} |p_j - m_j| \times [1 + \beta \,(PR_j - 0.5)]}

**Rationale:** Normalisation makes the weights comparable and ensures that the final aggregated score is a true weighted average of the respondents’ probabilities. This step rescales the combined scores so that no matter how large or small the individual components are, the final influence each respondent has is relative to the overall group.

### Final Aggregated Score

**Formula:** The final score S for the opinion article is calculated as:

S = \sum_{i} w_i \, p_i

# 2. Individual Scores

Respondents/bettors are scored via a BTS system where accuracy and honesty are a the optimal strategies. Specifically they are rewarded for accurately predicting what the crowd will forecast and how surprisingly common their own honest answer is. The latter is known as their information score, the former is their prediction score.

### 2.1. Information Score

- Kernel Aggregator We collect each agent’s primary report p_i \in [0,1]. Define a dynamic‐bandwidth, offset‐augmented Epanechnikov kernel density:

\hat{f}(x) = \frac{1}{n\,h(n)}\sum_{j=1}^n K\!\left(\frac{x - p_j}{h(n)}\right) + \alpha(n),

where:

h(n) = C\,n^{-\frac{1}{5}}, \quad \alpha(n) = \frac{\alpha_0}{n^\gamma}, \quad K(u) = \begin{cases}
\frac{3}{4}(1 - u^2), & |u|<1,\\
0, & \text{otherwise}.
\end{cases}

- Log‐Score Each agent i gets an information score by comparing \hat{f}(p_i) with the group’s average log density:

S_i^{\mathrm{info}} = \ln[\hat{f}(p_i)] - \frac{1}{n}\sum_{k=1}^n \ln[\hat{f}(p_k)].

**Rationale**

1. No Arbitrary Bins Traditional BTS (for discrete categories) must count occurrences in bins. For continuous “probabilities,” that discretisation is unnatural and can produce perverse outcomes. A kernel density smoothly estimates frequencies without artificial cut‐offs.
2. Epanechnikov Kernel Has bounded support |u|0 everywhere, so no agent ever encounters \ln(0)\to -\infty. The dynamic bandwith and pseudo-count ensure ‘robustness’ a low n.
5. Log‐Score (Difference) Subtracting the average log ensures a zero‐sum distribution of “surprise,” rewarding reports that turn out “unexpectedly common.”

### 2.1 Prediction Score

- Regularised Group Average Instead of a raw mean of the primary reports, use:

\bar{p}^{\star} = \frac{\alpha_{\mathrm{B}} + \sum_{j=1}^n p_j}{n + 2\,\alpha_{\mathrm{B}}},

where \alpha_{\mathrm{B}}>0 is small. This keeps \bar{p}^{\star}\in(0,1), never exactly 0 or 1 at small n.

- Brier Score Each agent i provides a meta‐prediction m_i\in[0,1]. Their prediction score is:

S_i^{\mathrm{pred}} = 1 - (m_i - \bar{p}^{\star})^2.

High scores (up to 1) reward accurate guesses of the group’s average.

**Rationale**

1. Continuous Probability Setting We’re asking each agent for a probability in [0,1]. A Brier‐type rule is strictly proper for a real‐valued outcome.
2. Avoiding Log Blow‐Ups Log scoring for a fraction can go -\infty if that fraction is exactly 0 or 1. The Brier rule remains finite in all cases.
3. Weighted (Regularised) Average By adding a small pseudo‐count \alpha_{\mathrm{B}}, extreme outcomes (0 or 1) are impossible at small n. This lowers variance and improves stability.

### Final Combined Score

Each agent i receives:

S_i = S_i^{\mathrm{info}} + S_i^{\mathrm{pred}}

This yields a **Continuous Probability BTS** that (hopefully!) remains:

- Strictly Proper (honest reporting is optimal),
- Robust (no infinite log penalties, no forced bins),
- Adaptive (dynamic smoothing for small vs. large n).

In other words, we solve the problem of **domain mismatch** between classical (categorical) BTS and new (probabilistic) questions by abandoning bins in favor of a **kernel** approach, along with a **Brier** rule suited to real‐valued [0,1] predictions.

# Discussion

This is an *attempt* to recreate the BTS Nash equilibrium but it might be broken. Certainly if the dynamic kernels aren’t calibrated correctly. We’ll need to perform simulations.

For the article score the combination of both multipliers will have to be carefully calibrated. Too much weight could be given to forecasters with a strong track record and a large divergence.

I’m currently thinking that fee/tip/bet sizes should scale with how much one diverges from what they predict the crowd average will be. This increases risk:reward under BTS so it makes sense that the financial cost should mirror this. So there’ll be some mininum bet and the more you diverge the more it’ll cost you to try and achieve a high score.

Any thoughts and criticisms welcome.
