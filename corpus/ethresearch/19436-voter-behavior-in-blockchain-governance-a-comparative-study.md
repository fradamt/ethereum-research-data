---
source: ethresearch
topic_id: 19436
title: "Voter Behavior in Blockchain Governance: A Comparative Study of Curve Finance and Polkadot"
author: dengwx11
date: "2024-05-02"
category: Economics
tags: [governance]
url: https://ethresear.ch/t/voter-behavior-in-blockchain-governance-a-comparative-study-of-curve-finance-and-polkadot/19436
views: 2609
likes: 0
posts_count: 1
---

# Voter Behavior in Blockchain Governance: A Comparative Study of Curve Finance and Polkadot

by [Wenxuan Deng](https://twitter.com/dengwx11), [Tanisha Katara](https://www.linkedin.com/in/tanishakatara/), [David Hamoui](https://www.linkedin.com/in/davidhamoui/) and [Mateusz Rzeszowski](https://twitter.com/matrzeszowski)

**Acknowledgments**

Additional thanks to [Peter Liem](https://twitter.com/p_petertherock) for his assistance with data fetching.

Also blogged here: [polygon mirror](https://polygon-governance.mirror.xyz/_BeDt5MvxFQ26ElodFtzHoLi725EFLp_IlliUYtg_HA); [Voter Behavior in Blockchain Governance: A Comparative Study of Curve Finance and Polkadot - HackMD](https://hackmd.io/QkqNJuSjQKSolPWfcEnceA?view)

## Abstract

As the first comprehensive examination of voter behavior in Web3, the following research explores two significant blockchain ecosystems, Curve Finance and Polkadot, using a novel quantitative methodology to decompose and highlight governance patterns.

The presented analysis shows, among other findings, a significant influence of market conditions on voter tendencies, diverse patterns relating to voting power accumulation, and a potential effect of financial incentives on voter participation.

As such, this research seeks to provide value to the growing field of blockchain-based governance frameworks in dealing with fundamental issues, such as low stakeholder activity, the impact of shifting market conditions, and various complexities at the intersection of economics and political science.

## 1. Introduction

Blockchain enables decentralized decision making[1]. The information once hidden is now displayed publicly in any block explorer[2]; what used to be the domain of a few now can be accessed permissionlessly[3]; what was perceived as status quo is now challenged with every executed transaction[4].

These qualities are revolutionary, but the decision-making of distributed networks is largely undocumented still. Consequently, this paper serves as an attempt to analyze and compare two blockchain-based governance systems quantitatively: Curve Finance[5] and Polkadot[6].

Firstly, in order to lay a common ground of understanding, we describe the relevant governance systems. Secondly, we explain the motivation for selecting Curve Finance and Polkadot as part of our analysis. Lastly, in each of the systems, we analytically deep dive into the voter personas, voter turnout, proposals and voter behavior in different market conditions.

### 1.1 Curve Finance and Polkadot

As the fields of tokenomics[7] and governance rapidly evolve, two protocols have emerged as particularly influential. Curve Finance pioneered[8] the vote escrow token model[9], introducing gauge voting[10] to decentralized finance (DeFi)[11]. Meanwhile, Polkadot’s governance system has been notable[12] for its innovative approach to quorums[13] and governance lockers[14]. These protocols consequently stand out as significant pioneers in decentralized governance innovation, including novel concepts such as governance conviction[15].

Governance conviction, also referred to as lockup-based voting multipliers or vote escrow[16], is a mechanism used in decentralized governance models[17] to enhance the influence or voting power of token holders based on the duration for which they are willing to lock up their tokens in a smart contract. This type of system operates under the assumption that the longer a participant commits their tokens for, the more conviction they demonstrate towards the decisions being made within the network and the more incentive alignment they display. As a consequence of the process, their voting power is multiplied by a factor corresponding to the lockup period. This aims to incentivize longer-term commitment and stability within the governance process, aligning participants’ interests with the long-term health and success of the platform.

Let’s now briefly go over both projects and how their governance works in practice.

**1.1.1 Curve Finance**[18] is a protocol allowing for seamless exchange of ERC-20 tokens at a low cost. This is achieved through the use of liquidity pools[19], which are tokens locked in smart contracts to facilitate trades. Curve Finance offers rewards[20] to those who contribute, creating a mutually beneficial relationship where users can easily exchange tokens while liquidity providers receive rewards.

To vote, CRV token holders must possess veCRV. veCRV[21] represents CRV tokens that are locked for a certain period ([Table 1](#table1)). Users can lock their CRV for a minimum of  one week and a maximum of four years.[22]

**1.1.1.1 Governance Proposals** - To distinct proposals were noted: gauge proposals and non-gauge proposals. Gauges and gauge weights determine how much token rewards the suppliers to a liquidity pool get. Therefore, a gauge proposal will have explicit financial consequences for some or all token holders. Non-gauge proposals, on the other hand, may or may not have financial consequences and may pertain to high-level maintenance and regular upgrades in the network. The impact of proposal types on voter behavior will be discussed more in this research paper.

**1.1.1.2 Community Voting** - A proposer must have a minimum voting power of 2500 vote-escrowed CRV (veCRV)[23] to create a proposal. A voter’s voting power linearly decreases overtime until it reaches zero at the time of the unlock.

**1.1.2 Polkadot**[24] is a protocol which uses a nominated Proof of Stake (PoS)[25] consensus algorithm and aims to connect blockchains, also known as parachains[26], to enable seamless communication, and intermediary-free communication within its network. Fundamentally, parachains are independent PoS blockchains with their own functionalities and tokens. What binds these parachains is the relay chain[27], which is responsible for achieving consensus and ensuring that transactions are executed.

Note: This study analyzes data from Polkadot’s Governance V1[6], rather than the more recent Open Governance system[28]. This choice was made to ensure comparability in terms of the data size, data type and temporal alignment of the voter samples with those from Curve Finance.

**1.1.2.1 Governance Proposals** - Similarly to Curve Finance, two types of proposals can be distinguished in Polkadot: treasury proposals[29] and non-treasury proposals. According to Polkadot’s Governance V1, when a stakeholder wishes to propose spending from the treasury, they must reserve a deposit of at least 5% of the proposed spending[29]. A treasury proposal will have explicit financial consequences for the protocol, subject to governance, while non-treasury proposals may or may not have financial consequences and pertain to high-level maintenance and regular upgrades in the network. The manner in how the proposal types impact voter behavior will be tackled in the  “Governance Proposals Breakdown” section of this research paper.

**1.1.2.2 Community Voting** - To vote on proposals, DOT token holders must lock their tokens. The longer the DOT is locked, the more voting power is assigned. The voting power of a DOT holder in Polkadot is calculated as DOT tokens held multiplied by the relevant multiplier ([Table 2](#table2)), which increases as the locking period increases. The multipliers range from 0.1x for zero days to 6x for two hundred and twenty-four days.[30]

For instance, if Bobby has 100 tokens and locks them for 14 days, her/his voting power per the ([Table 2](#table2)) is (Dot Tokens Held) * 2 (14-day multiplier) = 200. Therefore, Bobby will have the voting power of 200 tokens.

### 1.2 Curve Finance and Polkadot Case Selection

Curve Finance and Polkadot serve as significant examples of decentralized governance and are distinct in their purposes and functionalities. At the same time, due to the need for upgradeable contracts and changeable system parameters[30][31], both projects incorporate governance structures, delegating system maintenance responsibilities to their respective communities, as proxied by token in order to facilitate for secure and decentralized decision-making. Both of those governance systems utilize permissionless on-chain execution, which means that the decision-making is directly translated into canonical code, without the need for an external authority or intermediary to apply the changes that tokenholders vote on.

Importantly, in both Polkadot’s and Curve’s cases, we can distinguish between proposals with explicit and direct financial consequences (financial proposals) and those where the financial consequence is implicit and delayed (technical proposals). Curve’s gauge proposals and Polkadot’s treasury proposals can be both considered financial proposals since they explicitly impact the allocation of financial resources shared by all tokenholders, i.e., as it concerns deciding reward structures for pools in Curve, and the distribution of Polkadot’s treasury funds. On the other hand, technical proposals, i.e., non-gauge and non-treasury, impact the protocols, relate to maintenance and upgrades, and may not directly affect the allocation of financial resources shared by tokenholders.

There is one notable difference between the two governance systems in terms of the specifics of their token lock-up mechanisms. Curve Finance employs a governance mechanism that encourages participants to actively engage in decision-making processes by allowing them to gain financial rewards[20] for locking their tokens. On the other hand, Polkadot doesn’t financially incentivize the locking up of tokens for voting (Democracy locker).

The above makes the case for a comparative study of the two systems. In the following parts, we analyze voter turnouts ([Section 2](#2)) and break down governance proposals by type ([Section 3](#3)). Then, we establish voter personas and seek to understand them in each system ([Section 4](#4)). Finally, we analyze voter behavior and seek to identify the governing principles and patterns of these complex environments ([Section 5](#5)). To do so, we break down the types of market conditions and consequent variations in voter behavior.

## 2. Voter Turnout Analysis

The below data comes from a comprehensive analysis on voter turnout for governance proposals. The calculation of voter turnout metrics is based on the number of veCRV tokens and DOT tokens used for voting over time, relative to the total veCRV and DOT tokens locked over the same period.

**2.1 Curve Finance:** On average, 65% of the circulating CRV is locked as veCRV. The below graph shows the monthly average number of veCRV tokens used for voting on gauge proposals and non gauge proposals over time. The red line shows the monthly average CRV locked as veCRV over time.

While there is no significant difference in the veCRV used for voting on gauge proposals and for non gauge proposals, it is interesting to note that out of the 65% locked, an average of 38% tokens have been used for voting. This highlights that although a significant proportion of CRV is locked, a relatively low percentage is used for voting. Further investigation is required to determine the exact factors contributing to the low percentage of utilized tokens.

[![crv_turnout](https://ethresear.ch/uploads/default/optimized/3X/b/5/b5ca495402eba76079ef1ae2e3a6201676e86217_2_690x202.png)crv_turnout1428×420 42.1 KB](https://ethresear.ch/uploads/default/b5ca495402eba76079ef1ae2e3a6201676e86217)

**2.2 Polkadot:** On average, 54.5% of the circulating DOT is locked into multiple Polkadot lockers. The below graph shows the monthly average number of locked DOT tokens used for voting on treasury proposals and non treasury proposals over time. The red line shows the monthly average amount of DOT locked over time. In stark contrast to Curve Finance, out of these locked tokens, only 0.11% has been used for voting.

This highlights a significant disparity in voter engagement between the two blockchain ecosystems, with DOT showing a much lower level of voter engagement than CRV. While no direct  connection can be drawn, the low percentage of utilized tokens for voting in DOT could be attributed to several factors, such as a lack of financial incentives dedicated to token lockups.

[![dot_turnout](https://ethresear.ch/uploads/default/optimized/3X/0/9/09bf469fb6b10415f3bbdd8919dab25c4e91905b_2_690x204.png)dot_turnout1432×424 28.3 KB](https://ethresear.ch/uploads/default/09bf469fb6b10415f3bbdd8919dab25c4e91905b)

The voter turnout metrics shed light on the extent to which token holders actively engage in voting in both the ecosystems. This sets the stage for a deeper exploration into the nature of governance proposals and their implications on decision-making dynamics within the Curve Finance and Polkadot communities. By examining the types and frequencies of proposals submitted in governance, we can gain further insights into the priorities and interests driving the respective ecosystems’ governance mechanisms.

## 3. Governance Proposals Breakdown

Governance proposals play a crucial role in decision-making within any community. Our analysis of two ecosystems, Curve Finance and Polkadot, reveals that financial proposals make up a significant portion of all proposals. Gauge proposals constitute approximately 70% of all proposals in Curve Finance, while treasury proposals make up approximately 80% of all proposals in Polkadot.

[![crv_cumu_prop_num](https://ethresear.ch/uploads/default/optimized/3X/9/f/9f65fd9cc73df566bd1b3796a96d61ae737a365a_2_690x406.png)crv_cumu_prop_num763×450 38.6 KB](https://ethresear.ch/uploads/default/9f65fd9cc73df566bd1b3796a96d61ae737a365a)

[![dot_cumu_ref_num](https://ethresear.ch/uploads/default/optimized/3X/3/5/35b67cad4c367dc4f4c3268906521b452a2cc5c7_2_690x318.png)dot_cumu_ref_num1300×600 70.5 KB](https://ethresear.ch/uploads/default/35b67cad4c367dc4f4c3268906521b452a2cc5c7)

Interestingly, in Curve Finance, we found that most proposals are initiated by individuals associated with the [Curve.fi](http://Curve.fi) team ([Table 3](#table3)), particularly two wallets linked to its founder, Michael Egorov[32]. The top wallet, identified as the [Curve.fi](http://Curve.fi) deployer on the Arkham data platform[33], is notably active in both gauge and non-gauge proposal submissions. See the appendix for ([Table 3](#table3)) of top Curve Finance proposers, ranked in order of participation.

No similar pattern could be observed in Polkadot with the most referenda submitted by a single author amounting to only 6% of the total proposals.

Having provided an analysis of various proposals and consequent patterns, we move into the voter-centric part of the paper.

## 4. Voter Personas and Respective Patterns

The following research categorizes voter persona and analyzes their behavior towards the governance systems.

Voter personas are categorized based on the size of their token holdings, and the hierarchy is defined as follows: the top 1% is labeled as Whales, the next 5% as Sharks, the next 10% as Dolphins, the next 20% as Fish, and the remaining 64% as Shrimps.



| Token Holdings | Voter Persona |
| --- | --- |
| Top 1% | Whales |
| 5% | Sharks |
| 10% | Dolphins |
| 20% | Fish |
| Remaining 64% | Shrimps |

**4.1 Curve Finance:** In the context of Curve Finance governance, over 58% of token holders choose to lock their tokens for the longest duration, i.e. four years. However, an intriguing trend surfaces among the different cohorts of holders.

In the graph below, the x-axis displays the initial lock-up windows, which range from 7 days to 4 years, and the y-axis displays the percentage of each of the voter personas who have locked their tokens. The more significant holders, i.e., Whales, Sharks, and Dolphins, show mild hesitation to commit for more extended lock periods. Conversely, they slightly prefer shorter commitments, particularly those under six months. Although the margin is slim, it is a telling divergence.

It hints that larger holders may not need to lock up their tokens for extended periods to wield significant voting power. For them, the flexibility not to lock in for an extended time could be a strategic move to mitigate risk and maintain liquidity options.

[![crv_shark_and_shrimp_dotplot](https://ethresear.ch/uploads/default/optimized/3X/b/1/b1c30bac016ddab4cd9accb8232ffc6b72a406aa_2_375x500.png)crv_shark_and_shrimp_dotplot600×800 31.8 KB](https://ethresear.ch/uploads/default/b1c30bac016ddab4cd9accb8232ffc6b72a406aa)

**4.2 Polkadot:** In the Polkadot ecosystem, analysis yields a similar, yet valuable, correlation to Curve Finance. 4% of DOT holders initially choose to lock their tokens for a maximum of 224 days (roughly seven months). Holders with more significant positions prefer shorter lock-up periods, and this pattern is glaringly apparent. Particularly striking in the Polkadot ecosystem is that about 93% of Whales and 98% of Sharks tend to lock up their tokens for 14 days or less. Contrastingly, shrimp holders display markedly different behavior, with approximately 30% opting for an 8-week lock-up and about 5% committing to a 32-week lock-up.

[![dot_shark_and_shrimp_dotplot](https://ethresear.ch/uploads/default/optimized/3X/9/5/957fc95c9dade9db90e4b1116fe2e631d9f3b6a7_2_375x500.png)dot_shark_and_shrimp_dotplot600×800 31.2 KB](https://ethresear.ch/uploads/default/957fc95c9dade9db90e4b1116fe2e631d9f3b6a7)

Among different holder categories, from Whales to Shrimps, there is an incremental increase in the preference for longer lock-ups as we move down the scale of holdings. The distinctions and preferences between prominent and smallholders are consistent within each protocol.

However, there is a significant difference between the two protocols. As shown in the pie charts below, in Curve Finance, 67.2% of voters across all groups opt for a four-year lock-up, while in Polkadot, only 4% of the users choose the most extended lock-up window of 224 days. Even among the most minor stakeholders, the Shrimps, less than 5% chose the most prolonged lock-up period of 32 weeks.

This divergence could be attributed to the fundamental differences in the underlying rewards and incentives of Curve Finance and Polkadot. Curve’s gauge weight voting system[34] incentivizes users to boost their voting power by locking their tokens for extended periods. This may indicate that sustained rewards are crucial in incentivizing token holders to stay longer.

[![crv_piechart](https://ethresear.ch/uploads/default/optimized/3X/a/d/ad4e411543cfef1a3570feaedf97c885a91ad181_2_511x500.png)crv_piechart733×717 33 KB](https://ethresear.ch/uploads/default/ad4e411543cfef1a3570feaedf97c885a91ad181)

[![dot_piechart](https://ethresear.ch/uploads/default/optimized/3X/f/b/fb9c1553283566ce16f0c4076202d83ab22487a6_2_497x500.png)dot_piechart708×711 32.7 KB](https://ethresear.ch/uploads/default/fb9c1553283566ce16f0c4076202d83ab22487a6)

With this understanding of voter personas and their lock-up behaviors, we now dive into how they accumulate voting power in different market conditions.

## 5. Voting Power Accumulation Patterns in Different Market Conditions

The study of voting power accumulation patterns and the associated dynamics between voters and their locked-up tokens are of great importance in understanding how voters use their tokens in upward and downward market conditions.

Fundamentally, the two primary ways in which voters can augment their voting power (VP) are by purchasing additional tokens and locking them up, or by extending their lock-up period for already-owned tokens, resulting in an increased multiplier. VP calculation is derived from the multiplication of token balance and a multiplier based on the lock-up period.

**Voting Power (VP) = token balance * multiplier based on lockup time**

However, analyzing the behavior of voters in response to changes in token prices and market conditions presents a significant challenge - it’s hard to determine whether voter behavior is influenced by changes in token locked amounts and lock-up duration or whether they are affected by the daily routines of the average Externally Owned Account (EOA) wallet.

To overcome this challenge, a reliable quantitative methodology has been developed to simplify this complex analysis. The approach we present is based on a decomposition of the changes in voting power into its constituent factors. By quantifying the changes in voting power (\Delta vp) over time, an analysis of the two constituent factors, changes in balance (\Delta b) and changes in conviction (\Delta c), can be made.

The change in voting power between two consecutive time points, t and t-1, can be derived through arithmetic calculations as follows:

![image](https://ethresear.ch/uploads/default/original/3X/2/4/24c7a0daa9f98d910a6b49ded7cef9789868a70f.png)

This equation can be expanded as:

[![image](https://ethresear.ch/uploads/default/original/3X/f/d/fd0c1ec82b641fef7cc14e5a229f8fece3897b0e.png)image785×107 3.91 KB](https://ethresear.ch/uploads/default/fd0c1ec82b641fef7cc14e5a229f8fece3897b0e)

Here, b(t) and c(t) represent the balance and conviction at time t, respectively. The terms \Delta b and \Delta c denote the changes in balance and conviction from time t-1 to t.

For this study, each timestamp where a new transaction occurs on the blockchain is considered a discrete-time point. This approach captures the dynamic nature of voting power changes with high granularity. To represent the changes in voting power across different voters and time points, a matrix formulation is used. The matrix of changes in voting power (\Delta VP) is defined as follows:

![image](https://ethresear.ch/uploads/default/original/3X/9/4/94595d89b00fa0170bf67b4c30629f6540180d37.png)

Here, T+1 represents the total number of time points, while W indicates the number of voters. The changes in voting power can be represented using the following formula:

![image](https://ethresear.ch/uploads/default/original/3X/1/1/110d27df9e76e720b17c0f7043a488be63d81b53.png)

The formula can be represented in matrix form as:

[![image](https://ethresear.ch/uploads/default/original/3X/8/b/8be96fafed33f43a6b1d92ef7ac076c5c191602e.png)image798×324 10.8 KB](https://ethresear.ch/uploads/default/8be96fafed33f43a6b1d92ef7ac076c5c191602e)

The matrix \Delta VP represents the change in voting power for each voter at each timestamp, while B represents the balance of each voter at time t, \Delta C represents the change in conviction between t and t-1 for each voter, and C(t-1) represents the conviction of each voter at time t-1. The matrices \Delta B and \Delta C represent the changes in balance and conviction, respectively, for each voter between t and t-1. The symbol \odot represents the element-wise multiplication of matrices.

If \Delta vp_{t, i} is non-zero, the voting power of voter i's wallet has been altered at time point t. A non-zero change in VP due to a change in conviction occurs because b \cdot \Delta c is non-zero. Conversely, a change in balance results in a non-zero value because c(t-1) \cdot \Delta b is non-zero. Typically, these two terms hold non-zero values simultaneously if the user changes the lock-up window and balance in the same transaction.

The crux of the analysis then becomes determining whether the term B \odot C or C(t-1) \odot \Delta B is more dominant in influencing \Delta VP. To this end, we define two metrics:

1. Balance Impact: This is quantified as the L1 norm of |C(t-1) \odot \Delta B|_1.
2. Conviction Impact: This is quantified as the L1 norm of |B \odot \Delta C|_1.

Here, the notation ||_1 denotes the L1 norm, which essentially sums up the absolute values of all elements in the matrix.

In summary, this methodology for governance conviction provides a more in-depth and comprehensive approach to analyzing voting power accumulation patterns in different market conditions. Through the matrix formulation, the changes in voting power across different voters and time points can be represented and analyzed with high granularity, providing valuable insights into voter behavior dynamics.

### 5.1 Accounting for Market Conditions in Curve and Polkadot

In this study, we aim to assess the impact of market conditions on how voters accumulate voting power. To achieve this, we analyze upward and downward trends in the market by employing a combination of short-term and long-term moving averages, namely the 7-day moving average (MA7) and the 30-day moving average (MA30). We define an upward trend when the MA7 exceeds the MA30 and a downward trend when the MA7 falls below the MA30.

It is crucial to acknowledge that token behavior is circumstantial, and varying market conditions may elicit different responses from holders with varying stakes, thereby exhibiting diverse behavior patterns. Therefore, we adopt a nuanced approach, which considers these factors to provide a precise understanding of how balance and conviction impact the ebb and flow of voting power within the Curve Finance and Polkadot governance systems.

[![crv_price](https://ethresear.ch/uploads/default/original/3X/0/7/07a995daf9cb9eb9aadcc576d83b39e7257db50b.png)crv_price635×387 48.5 KB](https://ethresear.ch/uploads/default/07a995daf9cb9eb9aadcc576d83b39e7257db50b)

[![dot_price](https://ethresear.ch/uploads/default/original/3X/c/a/ca393687212f545f9764f88da9c2ea9b776a93c2.png)dot_price650×388 39.7 KB](https://ethresear.ch/uploads/default/ca393687212f545f9764f88da9c2ea9b776a93c2)

The charts presented above illustrate how the MA7-MA30 differential correlates with the token price. Our analysis leverages these definitions to explore how market trends affect Shrimp voter behavior, specifically the influence of the token price and lock-up duration on the dynamic voting power within the governance frameworks of Curve Finance and Polkadot. Since the sample size for Whales, Sharks, Dolphins and Fish is insignificant, we choose to exclusively analyze the Shrimp voter group. Having said that, it’s useful to note that for all the aforementioned groups, similar tendencies can be distinguished to the ones presented below.

### 5.2 Findings: Voting Power Accumulation in Curve Finance and Polkadot

**5.2.1 Curve Finance:** In the case of Curve Finance, we encountered a challenge when studying Shrimp voters due to their number exceeding 12,000 and the high computational complexity of our method. As a result, we adopted a sampling strategy, randomly selecting 2000 Shrimp voters in each experiment, and repeated this process 500 times. We calculated the log ratio of conviction impact to balance impact in each experiment and grouped the results by upward and downward market trends. The grouped histograms below show distinct patterns.

[![crv_vp_accu](https://ethresear.ch/uploads/default/original/3X/d/5/d536727595a832550e07d0d6945f5ee56a64682e.png)crv_vp_accu1200×600 10.2 KB](https://ethresear.ch/uploads/default/d536727595a832550e07d0d6945f5ee56a64682e)

During downward trends, the log ratio values were mainly concentrated between 0 and 0.5, displaying a distribution similar to a normal distribution. This suggests that Shrimp behavior is more uniform in downward markets, and most log ratios exceeding 0 indicate a tendency among Shrimp to increase their lock-up duration to alter their voting power.

During upward trends, the scenario was notably more complex, as three peaks around -0.3, 0.5, and 1 indicate that Shrimp behavior is inconsistent during upward markets. However, most Shrimps preferred increasing their lock-up window, a tendency that was even more pronounced than during downward trends.

**5.2.3 Polkadot:** When analyzing Polkadot’s market trends, we observed a deviation from the typical pattern observed in Curve Finance. Instead of a normal distribution, there was a noticeable long tail in the data. Upon closer inspection, we discovered a fascinating insight: a particular group of Shrimp voters in Polkadot had a strong inclination towards raising their lock-up window rather than increasing their balance during bullish market conditions. This behavior was particularly prominent and suggestive of a unique pattern among this subset of voters.

[![dot_vp_accu](https://ethresear.ch/uploads/default/original/3X/f/0/f08029351ce5b605f8ceb52b4074c5c8b7c9ef1c.png)dot_vp_accu1200×600 10.4 KB](https://ethresear.ch/uploads/default/f08029351ce5b605f8ceb52b4074c5c8b7c9ef1c)

## 6. Conclusion

The research focused on identifying key trends in voter behavior by examining voter personas, types of governance proposals, and patterns of voting power accumulation.

1. There is a noticeable correlation between financial incentives at the token lock-up level in Curve Finance and the absence of such incentives in Polkadot, which may directly affect voter turnout - relatively high in Curve Finance than in Polkadot.
2. The analysis indicates that financial proposals, specifically Curve Finance- gauge proposals and Polkadot’s treasury proposals, constitute the majority of proposals in both systems and are central to all significant voting activities.
3. The study defines and analyzes various voter personas and shows interesting patterns,  the most crucial of them being that Whales, Sharks, and Dolphins, prefer shorter lock-up periods, while the majority of low-staked holders, referred to as Shrimps, opt for longer lock-up durations.
4. In Curve Finance, most voters choose the longest available lock-up period. This behavior contrasts sharply with that of Polkadot voters, underscoring the potential influence of financial incentives on long-term voter alignment with the protocol.
5. A new methodology is introduced to analyze voter behavior under various market conditions. The results indicate that market trends significantly influence voter behavior. For instance, during market upswings, shrimps in both governance systems have differing preferences, utilizing both adjustments to their lock-up durations and increasing their token holdings to maximize voting power. During market downturns, on the other hand, there is a pronounced tendency among the shrimp voter group to extend their lock-up periods. While the sample size for other voter personas is too small to establish the above trends with confidence, similar tendencies could be seen in preliminary analysis of those sets as well.

This research contributes to our understanding of decentralized governance within blockchain ecosystems and aims to provide insights that could help in the design and optimization of governance mechanisms. Continued research in this field is vital to enhancing the scalability and effectiveness of decentralized decision-making as the blockchain landscape continues to evolve.

## References

[1]: Beck, Roman; Müller-Bloch, Christoph; and King, John Leslie (2018) “Governance in the Blockchain Economy: A Framework and Research Agenda,” Journal of the Association for Information Systems, 19(10),.

[2]: [Etherscan.Io](http://Etherscan.Io). n.d. “Ethereum (ETH) Blockchain Explorer.” Ethereum (ETH) Blockchain Explorer. https://etherscan.io/.

[3]: S. Wang, W. Ding, J. Li, Y. Yuan, L. Ouyang and F. -Y. Wang, “Decentralized Autonomous Organizations: Concept, Model, and Applications,” in IEEE Transactions on Computational Social Systems, vol. 6, no. 5, pp. 870-878, Oct. 2019, doi: 10.1109/TCSS.2019.2938190.,

[4]: “Zuwu on X: ‘Hey @Opensea Why Does It Appear @Natechastain Has a Few Secret Wallets That Appears to Buy Your Front Page Drops Before They Are Listed, Then Sells Them Shortly After the Front-page-hype Spike for Profits, and Then Tumbles Them Back to His Main Wallet With His Punk on It?’ / X.” n.d. X (Formerly Twitter). https://twitter.com/0xZuwu/status/1437921263394115584.

[5]: CurveFi. n.d. “Understanding Curve (V1) - Curve Resources.” https://resources.curve.fi/base-features/understanding-curve/.

[6]: “Governance V1 · Polkadot Wiki.” 2024. May 1, 2024. [Polkadot OpenGov - Polkadot Wiki](https://wiki.polkadot.network/docs/learn/learn-governance).

[7]: Lin William Cong, Ye Li, Neng Wang, Tokenomics: Dynamic Adoption and Valuation, The Review of Financial Studies, Volume 34, Issue 3, March 2021, Pages 1105–1155, https://doi.org/10.1093/rfs/hhaa089

[8]: Curve DAO. n.d. “Curve DAO.” https://classic.curve.fi/files/CurveDAO.pdf.

[9]: “WTF Are veTokens on Bankless.” n.d. [WTF are veTokens - by Ben Giove - Bankless](https://www.bankless.com/wtf-are-vetokens).

[10]: CurveFi. n.d. “Gauge Weights - Curve Resources.” [Gauge weights - Curve Resources](https://resources.curve.fi/reward-gauges/gauge-weights/).

[11]: Zetzsche, Dirk Andreas and Arner, Douglas W. and Buckley, Ross P., Decentralized Finance (DeFi) (September 30, 2020). Journal of Financial Regulation, 2020, 6, 172–203, Available at SSRN: https://ssrn.com/abstract=3539194 or http://dx.doi.org/10.2139/ssrn.3539194

[12]: CryptoDaily. 2024. “Polkadot’s Uniquely Decentralized Community Governance Model Accelerates Ecosystem Traction.” Crypto Daily, March 5, 2024. [Polkadot’s Uniquely Decentralized Community Governance Model Accelerates Ecosystem Traction - Crypto Daily](https://cryptodaily.co.uk/2024/03/polkadots-uniquely-decentralized-community-governance-model-accelerates-ecosystem-traction).

[13]: “Governance V1 · Polkadot Wiki.” 2024. May 1, 2024. [Polkadot OpenGov - Polkadot Wiki](https://wiki.polkadot.network/docs/learn/learn-governance#adaptive-quorum-biasing).

[14]: “Introduction to Polkadot OpenGov · Polkadot Wiki.” 2024. April 3, 2024. [Polkadot OpenGov - Polkadot Wiki](https://wiki.polkadot.network/docs/learn-polkadot-opengov#voluntary-locking-conviction-voting).

[15]: Emmett, Jeff. 2022. “Conviction Voting: A Novel Continuous Decision Making Alternative to Governance.” Medium, April 22, 2022. https://blog.giveth.io/conviction-voting-a-novel-continuous-decision-making-alternative-to-governance-aa746cfb9475.

[16]: CoinMarketCap. 2023. “What Is Vote Escrow?” CoinMarketCap Academy. April 5, 2023. [What Is Vote Escrow? | CoinMarketCap](https://coinmarketcap.com/academy/article/what-is-vote-escrow).

[17]: “Blockchain Voting Is Overrated Among Uninformed People but Underrated Among Informed People.” 2021. May 25, 2021. [Blockchain voting is overrated among uninformed people but underrated among informed people](https://vitalik.eth.limo/general/2021/05/25/voting2.html).

[18]: “[Curve.finance](http://curve.fi/compound.%E2%80%9D) n.d. Curve Finance. https://classic.curve.fi/.

[19]: CurveFi. n.d. “Understanding Curve Pools - Curve Resources.” https://resources.curve.fi/lp/understanding-curve-pools/.

[20]: CurveFi. n.d. “Boosting Your CRV Rewards - Curve Resources.” [Boosting your CRV rewards - Curve Resources](https://resources.curve.fi/reward-gauges/boosting-your-crv-rewards/).

[21]: CurveFi. n.d. “Overview - Curve Resources.” [Overview - Curve Resources](https://resources.curve.fi/vecrv/overview/).

[22]: CurveFi. n.d. “Locking CRV - Curve Resources.” [How to Lock CRV - Curve Resources](https://resources.curve.fi/vecrv/locking-your-crv/).

[23]: CurveFi. n.d. “Creating a DAO Proposal - Curve Resources.” https://resources.curve.fi/governance/proposals/creating-a-dao-proposal/?h=2500.

[24]: “Polkadot: Web3 Interoperability | Decentralized Blockchain.” n.d. Polkadot Network. https://polkadot.network/.

[25]: “Polkadot Launch Phases · Polkadot Wiki.” 2024. May 1, 2024. [Polkadot](https://wiki.polkadot.network/docs/learn/learn-launch#nominated-proof-of-stake).

[26]: “Polkadot’s Parachains · Polkadot Wiki.” n.d. [Parachains | Polkadot Developer Docs](https://wiki.polkadot.network/docs/learn-parachains-index).

[27]: “Architecture · Polkadot Wiki.” 2024. April 3, 2024. [Architecture - Polkadot Wiki](https://wiki.polkadot.network/docs/learn-architecture#relay-chain).

[28]: “Polkadot OpenGov · Polkadot Wiki.” n.d. https://wiki.polkadot.network/docs/learn-polkadot-opengov-index.

[29]: “Governance V1 Treasury · Polkadot Wiki.” 2024. May 1, 2024. [Treasury - Polkadot Wiki](https://wiki.polkadot.network/docs/learn/learn-treasury).

[30]: “Polkadot Parameters · Polkadot Wiki.” 2024. March 11, 2024. [Infrastructure | Polkadot Developer Docs](https://wiki.polkadot.network/docs/maintain-polkadot-parameters#governance).

[31]: “[Curve.fi](http://Curve.fi) Governance.” n.d. [Curve.Fi](http://Curve.Fi) Governance. https://gov.curve.fi/.

[32]: “Michael Egorov (@Newmichwill) / X.” n.d. X (Formerly Twitter). [https://twitter.com/newmichwill?ref_src=twsrc^google|twcamp^serp|twgr^author](https://twitter.com/newmichwill?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor).

[33]: “Arkham | Deanonymizing the Blockchain.” n.d. https://www.arkhamintelligence.com/.

[34]: CurveFi. n.d. “Understanding Gauges - Curve Resources.” https://resources.curve.fi/reward-gauges/understanding-gauges/.

## Appendix

Table 1: veCRV amount by lock-up period

| 1 CRV is locked for | The user is assigned |
| --- | --- |
| one week | 0 veCRV |
| one month | 0.02 veCRV |
| six months | 0.13 veCRV |
| one year | 0.25 veCRV |
| two years | 0.5 veCRV |
| three years | 0.75 veCRV |
| four years | 1 veCRV |

Table 2: DOT conviction multiplier by democracy lock

| 1 DOT is locked for | Multiplier |
| --- | --- |
| zero days | 0.1 |
| seven days | 1 |
| fourteen days | 2 |
| twenty eight days | 3 |
| fifty six days | 4 |
| one hundred and twelve days | 5 |
| two hundred and twenty four days | 6 |

Table 3: Top Proposal Address Labels on [Curve.fi](http://Curve.fi)

| Rank | Proposer Address | Count | ID on Arkham |
| --- | --- | --- | --- |
| 1 | 0xbabe61887f1de2713c6f97e567623453d3c79f67 | 55 | Curve.fi Deployer |
| 2 | 0x745748bcfd8f9c2de519a71d789be8a63dd7d66c | 28 | @skellet0r (Curve.fi) |
| 3 | 0x7a16ff8270133f063aab6c9977183d9e72835428 | 28 | Michael Egorov (Curve.fi) |
| 4 | 0x0000000000e189dd664b9ab08a33c4839953852c | 22 | Charlie Watkins (Curve.fi) |
| 5 | 0x71f718d3e4d1449d1502a6a7595eb84ebccb1683 | 22 |  |
| 6 | 0x947b7742c403f20e5faccdac5e092c943e7d0277 | 22 | Convex Finance Deployer |
| 7 | 0x34d6dbd097f6b739c59d7467779549aea60e1f84 | 17 |  |
| 8 | 0xa1992346630fa9539bc31438a8981c646c6698f1 | 14 |  |
| 9 | 0xf7bd34dd44b92fb2f9c3d2e31aaad06570a853a6 | 13 |  |
| 10 | 0x52f541764e6e90eebc5c21ff570de0e2d63766b6 | 13 | Stake Dao: Curve yCRV Voter |
