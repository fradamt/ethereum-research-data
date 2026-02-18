---
source: ethresearch
topic_id: 20345
title: Does multi-block MEV exist? Analysis of 2 years of MEV Data
author: pascalst
date: "2024-08-28"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/does-multi-block-mev-exist-analysis-of-2-years-of-mev-data/20345
views: 1376
likes: 24
posts_count: 4
---

# Does multi-block MEV exist? Analysis of 2 years of MEV Data

# Does multi-block MEV exist? Analysis of 2 years of MEV Data

*by [Pascal Stichler](https://x.com/pascalstichler) ([ephema labs](https://www.ephema.io/))*

*Many thanks to [Toni](https://x.com/nero_eth), [Julian](https://x.com/_julianma), [Danning](https://x.com/sui414), [Chris](https://x.com/cshg0x) and [Marc](https://x.com/marc_nitzsche) for feedback and especially to [Barnabé](https://x.com/barnabemonnot) for nudging the research in the first place and continuous feedback.*

## TL;DR

- We looked at proposer-builder data and MEV-Boost payment data since the merge (September 2022) to identify patterns of multi-block MEV.
- We observe fewer multi-slot sequences of builders than a random Monte Carlo simulation would predict. The longest observed multi-slot sequence is 25 slots.
- Average MEV-Boost payments increase for longer consecutive sequences by the same builder from ~0.05 ETH for single slots to ~0.08 ETH for nine consecutive slots.
- In longer sequences, the payment per slot increases slightly with later slots. This indicates that builders bid higher to get longer sequences or the first slot after a longer sequence.
- There is a weak positive autocorrelation between subsequent MEV-Boost payments. This contradicts the hypothesis that there are generally periods of low and high MEV.
- Comparing builders with periods of low and high base fee volatility shows a low correlation. This indicates that no builder specialization based on base fee volatility has developed yet.

*The detailed results can be found in the Jupyter notebook on [Github](https://github.com/ephema/MEVBoost-Analysis/blob/762b7626c57cc6a1c350059b41e272a70cda49cf/%5Bephema%5D_MEV_Boost_Multi_Slot_MEV_Analysis.ipynb)or [Google Colab](https://colab.research.google.com/drive/1kKM-da6xP7St8puzPuyn1Ndag6a6wsg3?usp=sharing).*

## Background

Multi-block Maximal Extractable Value (MMEV) occurs when one party controls more than one consecutive block. It was first introduced in 2021 by [[1](https://arxiv.org/pdf/2109.04347)] as k-MEV and further elaborated by [[2](https://eprint.iacr.org/2022/445.pdf)]. It is commonly assumed that controlling multiple slots in a sequence allows to capture significantly more MEV than controlling them individually. This derives from MEV accruing superlinearly over time. The [most discussed](https://collective.flashbots.net/t/multi-block-mev/457) multi-block MEV strategies include [TWAP oracle manipulation attacks](https://eprint.iacr.org/2022/445.pdf) on DEXes and producing forced liquidations by price manipulation.

After the merge, [[3](https://arxiv.org/pdf/2303.04430)] have looked into the first four months of data on multi-block MEV and summarized it as *“preliminary and non-conclusive results, indicating [that] builders employ super-linear bidding strategies to secure consecutive block space"*.

With the recent Attester-Proposer-Separation (APS) and pre-confirmation discussions, multi-block MEV has become more of a pressing issue again as it might be prohibitive for some of the proposed designs (For a more in-depth overview, we’ve created a [diagram of recently proposed mechanism designs](https://miro.com/app/board/uXjVK07aBCU=/?share_link_id=220296247588) and also [Mike Neuder](https://x.com/mikeneuder) lately gave a [comprehensive overview](https://www.youtube.com/watch?v=ToVi-zsiE4M)).

## Methodology

In order to get a better understanding of the historical prevalence of multi-block MEV, we decided to look at all slots from the Merge in September ‘22 until May ‘24 (totalling roughly 4.3 million slots) and analyze the corresponding data on validators and builders and on MEV-boost payments (if applicable). The scope was to identify patterns of unusual consecutive slot sequences and accompanying MEV values. [The data](https://mevboost.pics/data.html) has been kindly provided by Toni Wahrstätter and contains information per slot on relay, builder pubkey, proposer pubkey and MEV-Boost value as well as a builder pubkey and validator pubkey mapping. In the labeling of validators for our purposes staking pool providers such as Lido or Rocket Pool are treated as one entity.

MEV-Boost payments are used as a proxy for the MEV per block. We acknowledge that this is only a non-perfect approximation. The ascending MEV-Boost first-price auction by its nature of being public essentially functions like a second price + 1 wei auction (thanks to Julian for pointing this out!). Hence, we strictly speaking only get an estimate of the intrinsic value of the second highest bidder. However, as [[4](https://arxiv.org/pdf/2405.01329)] have observed more than 88% of MEV-Boost auctions were competitive and [[5](https://arxiv.org/pdf/2407.13931)] concluded that the average profit margin per top three builder is between 1% and 5.4%, further indicating a competitive market between the top builders. Based on this, despite the limitations we deem it feasible to use the MEV-Boost payments as an approximation for the generated MEV per block.

To establish a baseline of expected multi-slot sequences, a Monte Carlo simulation was conducted. In this simulation, builders were randomly assigned to each slot within the specified time period, based on their observed daily market share during that period. The frequency of consecutive slots, ranging in length from 1 to 25 (the longest observed sequence in the empirical data), was recorded. This procedure was repeated 100 times, and the average was taken. We decided to use daily market shares for the main analysis as in the investigated time period market shares have strongly shifted [4]. For comparison we also ran the analysis on monthly and overall market shares.

Further, base fee volatility data has been included to cross-check effects of low and high-volatility periods. Previous research (e.g. [[6](https://arxiv.org/pdf/2305.19150)] & [[7](https://arxiv.org/pdf/2401.01622)]) has focused on token price volatility effects based on CEX-prices. As we are interested in low- and high-MEV environments, we deem base fee volatility for our use case more fitting, as it is driven by empty or full blocks which are at least partially a result of the prevalence of MEV opportunities.

## Empirical Findings

### Finding 1: Fewer multi-slot sequences exist than assumed by random distribution

**[![](https://ethresear.ch/uploads/default/optimized/3X/b/6/b6ab4921507e70c619d5121b5abf611e67e2138f_2_533x426.png)1000×800 25.1 KB](https://ethresear.ch/uploads/default/b6ab4921507e70c619d5121b5abf611e67e2138f)**

*Figure 1: Comparison of statistically expected vs. observed multi-slot sequences (note that slots > 25 have been summarized in slot 25 for brevity)*

Firstly, the prevalence of multi-slot sequences with the same builder proposing the block was investigated to determine if they are more common than would be expected by chance.

Comparing the results of the Monte Carlo simulation as a baseline in expected distribution (blue) with the observed distribution (orange), it can be seen that significantly fewer multi-slot sequences occur than expected (Figure 1). The longest observed sequence was 25 slots and the longest sequence with the same validator (Lido) and builder (BeaverBuild) was 11 consecutive slots on March 4th, 2024 (more details with descriptive statistics in the [notebook](https://colab.research.google.com/drive/1kKM-da6xP7St8puzPuyn1Ndag6a6wsg3#scrollTo=5bje4mIWzELq)). Running the same simulation on monthly or total market shares in the time period, the observation shifts to having more longer sequences than expected, however we attribute this to the statistical effect of changing market shares. A detailed analysis can be run in the [notebook](https://colab.research.google.com/drive/1kKM-da6xP7St8puzPuyn1Ndag6a6wsg3#scrollTo=mz4CTqCQInTv) or be provided upon request.

In the next step, to understand this in a more-fine-grained manner, the values are compared for each of the top 10 builders based on market shares. Therefore, for each builder, the difference between expected and observed occurrences of multi-slot sequences are plotted with the size of the bubble indicating the delta in Figure 2. The expected occurrences are based on the results of the Monte Carlo simulation. Red bubbles indicate a positive deviation (more observed slots than expected), while blue indicates a negative deviation. Green dots indicate values in line with the expectation. In Figure 2 it is shown in absolute numbers, in the [notebook](https://colab.research.google.com/drive/1kKM-da6xP7St8puzPuyn1Ndag6a6wsg3#scrollTo=cd07f078-f646-450c-b610-9e91012111f2&line=3&uniqifier=1) it can also be seen on a relative scale.

**[![](https://ethresear.ch/uploads/default/optimized/3X/e/9/e94454973c4bf844c96e0a1735409a130a0983dd_2_628x419.png)1200×800 99.7 KB](https://ethresear.ch/uploads/default/e94454973c4bf844c96e0a1735409a130a0983dd)**

*Image 2: Deviations between expected (Monte Carlo simulation) and observed multi-slot frequencies per builder*

It can be observed in the relative as well as in the absolute deviation that for the top builders there are more single slot sequences than expected with the exception of ETH-Builder, f1b and Blocknative. For multi-slot sequences with two or more slots, almost all top 10 builders have less than expected. This shows that the trend is not limited to singular entities but derives more from the general market structure.

### Finding 2: Payments for multi-slot sequences are higher on average than for single slots

To understand if multi-slot sequences are valuable, we looked into MEV-Boost payments and compared single-slot to multi-slot sequences (Figure 3).

**[![](https://ethresear.ch/uploads/default/original/3X/b/5/b570ac276a9b9dc76883e6e89489c8792b0186e3.png)630×460 23.1 KB](https://ethresear.ch/uploads/default/b570ac276a9b9dc76883e6e89489c8792b0186e3)**

*Figure 3: Average MEV-Boost payments per Sequence Length*

It can be observed that in accordance with previous work of [3], we observe higher average MEV payouts for longer consecutive sequences (from about 0.05 ETH for single slot sequences to around 0.08 ETH for sequences with nine consecutive slots). Note that the gray numbers in Figure 3 provide the sample size for each slot length. So it can be observed that the longer the sequence, almost linearly the average MEV-boost payment per slot in the sequence rises. At this stage of the research we can only speculate why this is the case. It could be driven by a higher value in longer consecutive sequences, but also by alternative effects. For example, Julian rightfully pointed out it could also be driven by an increasing intrinsic value for the second highest-bidder due to accumulating MEV in private order flow and the intrinsic valuation of the winning bidder remains constant. Or as Danning suggested, it might be driven by certain types of proprietary order flow (e.g. CEX-DEX arbitrage) being more valuable in certain time periods (e.g. volatile periods) leading to more consecutive sequences as well as higher MEV-Boost payments on average. For a more comprehensive answer and a more in-depth understanding, an analysis on the true block value (builder profits plus proposer payments) and potentially on individual tx level is necessary. We leave this open for future research.

This trend also holds when plotting the average payments for each individual builder. The results on this are shown in the [notebook](https://colab.research.google.com/drive/1kKM-da6xP7St8puzPuyn1Ndag6a6wsg3#scrollTo=e673f535-1bad-41aa-b617-fcdeee234f01&line=3&uniqifier=1).

### Finding 3: Per Slot Payments also increase with longer sequences

Supplementary to the absolute average payment, we also looked into the payment per slot position in longer sequences (Figure 4). E.g. how much was on average paid for the third position in a longer sequence.

**[![](https://ethresear.ch/uploads/default/original/3X/3/9/3910c4ca760a17b0ae0a9ec76bb90d27155b5e42.png)592×460 19.3 KB](https://ethresear.ch/uploads/default/3910c4ca760a17b0ae0a9ec76bb90d27155b5e42)**

*Figure 4: Average MEV-Boost payments per Sequence Position*

Also in the payment per slot analysis a similar trend can be observed, however less prevalent. This suggests that there is slight value in longer sequences, however builders are not willing to bid significantly more for longer consecutive sequences or the first slot after a longer sequence.

This indicates for us that, at least so far, multi-slot strategies are not applied systematically. In this case, we expect builders would need to pay significantly higher values for later slots to ensure to capture the MEV opportunity prepared earlier.

### Finding 4: Low auto-correlation between consecutive MEV-Boost payments

**[![](https://ethresear.ch/uploads/default/optimized/3X/9/d/9db050ae9f5aa540ea6f3c5b6270dee27e111380_2_533x321.png)1165×701 77 KB](https://ethresear.ch/uploads/default/9db050ae9f5aa540ea6f3c5b6270dee27e111380)**

*Figure 5: Auto-correlation of MEV-Boost Payments*

We examined auto-correlation in the MEV boost payments to understand if historical MEV data allows us to forecast future MEV and to see if there are low- and high-MEV periods (Figure 5).

Overall, it can be observed that within the first few slots the correlation strongly decreases until an offset of 2 to 3 slots (we tested for Pearson Correlation Coefficient, Spearman’s Rank Correlation Coefficient and Kendall’s Rank Correlation Coefficient). Based on this we can conclude that not more than one to three slots in advance the MEV value can be moderately predicted based on historical data.

Further interesting observations can be made. As expected, the Spearman and Kendall correlation coefficients are significantly higher than the Pearson correlation coefficient, underlining that the data is not following a normal distribution but being skewed and having large outliers. Additionally, it is interesting to note that for the Pearson correlation coefficient, the complete data set and the top 50% quantile dataset behave similarly, which is not the case for the Spearman and Kendall coefficients. This might be an indicator that the rank ordering for the lower 50% quantile can be more reliably predicted, further underlying that high MEV values are volatile and spiky, hence difficult to predict.

### Finding 5: No indication of builder specialization on low- or high base fee volatility environment

Previous research (e.g. [6] & [7]) has found that certain builders specialize in low- or high token price volatility environments, with volatility being measured on CEX-price changes. Further, [5] observe that different builders have different strategies with some focusing on high-value blocks while others on gaining market share in low-MEV blocks.

Complementary, to determine whether low or high base fee volatility impacts (multi-block) MEV, we analyzed changes in base fee data to identify periods of high volatility. The base fee fluctuations are driven by whether the gas usage in the previous block was below or above the gas target, as defined by [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559). To identify high volatility environments, we employed two methods: (i) a more naive approach that calculated price changes per slot, classifying the highest and lowest (negative) 10% of these changes as high volatility periods, with the remaining 80 % of slots being categorized as low volatility. Consequently, high volatility blocks occur following a block with either minimal or significant MEV and/or priority tips. (ii) Secondly, the Garman-Klass volatility [[8](https://arxiv.org/pdf/0807.3492)] was calculated on an epoch basis, with slots in the top 20% of GK values designated as high volatility. This approach allows us to examine longer periods characterized by minimal or significant MEV and/or priority tips.

Initial correlation analysis shows only a low correlation between low and high volatile periods and the respective builders ([Cramér’s V](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V) for the naive approach 0.0664 and for the Garman-Klass 0.0772). This indicates that there seems to be no builder specialization based on the volatility environment of the base fee. So, it can be observed that in contrast to token price volatility for base price volatility there seems to not have a specialization of builders developed (yet). Further research is needed to elaborate on this first finding.

## Limitations

The research presented here is intended as an initial exploratory analysis of the data rather than a comprehensive study. It is important to note several limitations that affect the scope and conclusions of this analysis. Firstly, it is limited by the considered data set being publicly available MEV-Boost payments data. This leaves out roughly 10 % of non-MEV-Boost facilitated blocks and it does not reflect potential private off-chain agreements. Additionally, the data was partially incomplete and in other parts contained duplicate information (see the [notebook](https://colab.research.google.com/drive/1kKM-da6xP7St8puzPuyn1Ndag6a6wsg3#scrollTo=0d986969-2492-49ac-ad92-8ff78e2a7fe1&line=2&uniqifier=1) for details). Further, missed slots have been excluded so far, a more detailed analysis in the future might focus on the particular effects missed slots have on the subsequent MEV. Lastly, as outlined in the methodology section, using MEV-Boost payments is only a proxy for captured MEV and the competitive metric used in [4] is only partially applicable for our use case.

As outlined in section Finding 2 it currently can only be speculated about the causation of the increasing average MEV-Boost payouts. Furthermore, running the analysis on the true block value (proposer payment plus builder profits) might generate further insights and solidify the research findings.

On the frequency analysis, the approach contains somewhat a chicken and egg-problem. The Monte Carlo simulation is run on market shares, while the market shares potentially derive from multi-slot sequences. We see a daily time window as an appropriate balance between precision and the need to filter out isolated effects, although this can be critically challenged.

## Conclusions

Analyzing block meta-data since the merge, we observe that multi-slot sequences occur less frequently than statistically expected. Further, we observe that the average payments for longer multi-slot sequences increase with the sequence length. Similarly, the payments per slot position in longer sequences also slightly rise. This might indicate that there is generally value in longer consecutive sequences. However, considering the only slight increase in value and the fewer observed multi-slot sequences than expected we so far see no indication of deliberate multi-slot MEV strategies being deployed. Also on individual builder level we currently don’t observe strong deviations from expected distributions. This may also stem from the fact that in the current PBS mechanism, with MEV-Boost operating as a just-in-time (JIT) block auction, creating multi-block MEV opportunities carries inherent risk. This risk arises as creating these opportunities typically requires an upfront investment, and the opportunity might be captured by a competing builder in the next slot, assuming no off-chain collusion between the proposer and builder. This element of risk is a critical factor that could be eliminated by some of the proposed changes to the mechanism (e.g. some APS designs), making it an essential consideration when defining future mechanisms.

## References

[1] Babel K, Daian P, Kelkar M, Juels A. Clockwork finance: Automated analysis of economic security in smart contracts. *In 2023 IEEE Symposium on Security and Privacy (SP)* 2023 May 21 (pp. 2499-2516). IEEE.

[2] Mackinga T, Nadahalli T, Wattenhofer R. Twap oracle attacks: Easier done than said?. *In 2022 IEEE International Conference on Blockchain and Cryptocurrency (ICBC)* 2022 May 2 (pp. 1-8). IEEE.

[3] Jensen JR, von Wachter V, Ross O. Multi-block MEV. arXiv preprint arXiv:2303.04430. 2023 Mar 8.

[4] Yang S, Nayak K, Zhang F. Decentralization of Ethereum’s Builder Market. arXiv preprint arXiv:2405.01329. 2024 May 2.

[5] Öz B, Sui D, Thiery T, Matthes F. Who Wins Ethereum Block Building Auctions and Why?. arXiv preprint arXiv:2407.13931. 2024 Jul 18.

[6] Gupta T, Pai MM, Resnick M. The centralizing effects of private order flow on proposer-builder separation. arXiv preprint arXiv:2305.19150. 2023 May 30.

[7] Heimbach L, Pahari V, Schertenleib E. Non-atomic arbitrage in decentralized finance. arXiv preprint arXiv:2401.01622. 2024 Jan 3.

[8] Meilijson I. The Garman-Klass volatility estimator revisited. arXiv preprint arXiv:0807.3492. 2008 Jul 22.

## Replies

**The-CTra1n** (2024-08-28):

Hypothesis on why you are seeing less multi-block builder sequences than expected randomly: private orderflow.

It’s related to the same reason we see non-0 MEV-Boost bids at the start of a slot. Only the winner drains their “orderflow pot” at the end of a slot, giving other builders who still have private orders to execute, a clear advantage in the next slot. [I wrote a thread on this hypothesis!](https://x.com/ConorMcMenamin9/status/1816418107931361538)

---

**pascalst** (2024-08-28):

Thanks for the input, interesting point! I guess it comes a bit down to how much of the private order flow is exclusive (non-available to the currently winning builder). Did you see any data on that?

---

**The-CTra1n** (2024-08-29):

Exclusivity of the private orderflow is key to the hypothesis. If everyone has the same private orderflow, then my theory falls apart. I’d say that’s incredibly unlikely though, even among the top 3 builders. At the very least, their own transactions would be private and exclusive. I think that’s enough for the phenomenon to exist, *assuming* each of the builders have non-identical private valuations for MEV opportunities (which I think we can assume without too much controversy).

