---
source: ethresearch
topic_id: 19992
title: "Maximum Viable Security: A New Framing for Ethereum Issuance"
author: xadcv
date: "2024-07-06"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992
views: 5561
likes: 14
posts_count: 5
---

# Maximum Viable Security: A New Framing for Ethereum Issuance

# Maximum Viable Security: A New Framing for Ethereum Issuance

*by [@artofkot](http://x.com/artofkot), [@damcnuta](http://x.com/damcnuta), [@sonyasunkim](http://x.com/sonyasunkim), [@adcv_](http://x.com/adcv_)*

*Appreciate feedback from [@ppclunghe](http://x.com/ppclunghe), [@ks_kulk](https://x.com/ks_kulk), [@lazyleger](http://x.com/lazyleger), [Juan Beccuti](https://cryptecon.org/team-detail-ce/items/juan-beccuti.html), [@entigdd](https://x.com/entigdd), [@stakesaurus](https://x.com/stakesaurus), [@hasufl](http://x.com/hasufl), [@lex_node](http://x.com/lex_node), [@_vshapolapov](https://x.com/_vshapovalov), [@brettpalatiello](http://x.com/brettpalatiello)*

---

**Table of Contents**

- TLDR: Embrace security
- 1. The foundations of the Maximum Viable Security (“MVS”) framework

1.1. Ethereum has a clear goal: build a secure and sovereign distributed system for everyone
- 1.2. A diverse staking economy is key

1.2.1. Stakers
- 1.2.2. Validating entities
- 1.2.3. Entities’ decentralization

[1.3. There is no future-proof safe level of Security](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-13-there-is-no-future-proof-safe-level-of-security-9)
[1.4. Reframing the discourse: expansion over efficiency](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-14-reframing-the-discourse-expansion-over-efficiency-10)

**[2. Analysis of Ethereum Issuance reduction proposal within the MVS framework](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-2-analysis-of-ethereum-issuance-reduction-proposal-within-the-mvs-framework-11)**

- 2.1. The assumption that Ethereum overpays for security is wrong: less issuance may lead to centralization of the validator set

2.1.1 ETF inflows would exacerbate centralization in the context of a 33% stake cap
- 2.1.2 Staked ETH concentration with CEXs doesn’t necessarily have to happen with a higher stake cap
- 2.1.3 MVI effect on the ratio of solo stakers

[2.2. LST dominance and cost-modeling are inadequate arguments for issuance reduction](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-22-lst-dominance-and-cost-modeling-are-inadequate-arguments-for-issuance-reduction-19)

- 2.2.1. Issuance as a cost is a reductive framing
- 2.2.2. Stakers getting higher real vs nominal yield is not significant
- 2.2.3. Reducing LST dominance shouldn’t be a primary objective of Ethereum’s monetary policy

**[3. Putting it all together](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-3-putting-it-all-together-23)**

---

## TLDR: Embrace security

Given Ethereum’s goal of building a secure and sovereign distributed system, we believe viewing Ethereum’s monetary policy through the lens of Minimum Viable Issuance (MVI) is not appropriate. Instead, we propose Maximum Viable Security (MVS) as a new framework for the community to consider in the Ethereum issuance debate. That is,

From: **Minimum Viable Issuance (MVI)** – minimize issuance, without compromising security.

→

To: **Maximum Viable Security (MVS)** – maximize security, without compromising scarcity.

After covering the motivation and foundations behind MVS, we evaluate Ethereum issuance reduction proposals through the MVS lens. We show that issuance reduction can compromise security and neutrality in a direct way, through staked ETH concentration with Centralized Exchanges – and this effect, on balance, far outweighs the advantages of cutting the issuance.

## 1. The foundations of the Maximum Viable Security (“MVS”) framework

### 1.1. Ethereum has a clear goal: build a secure and sovereign distributed system for everyone

> There are many goals of this project; one key goal is to facilitate transactions between consenting individuals who would otherwise have no means to trust one another.
> Source: Ethereum Yellow Paper (link)

The growth of Ethereum’s market capitalization from 0 to $400bn today underscores the market’s confidence in its current and future potential. This value hinges on Ethereum’s ability to validate state changes transparently, securely, and sovereignly.

Security is a crucial part of the value proposition. Without sybil resistance and slashing defense (programmable or social) against 34% double-signing attacks, a settlement layer would not be trusted by participants. A secure validation layer is the most scalable ([link](https://unenumerated.blogspot.com/2017/02/money-blockchains-and-social-scalability.html)) foundation for providing transaction settlement with incorruptible finality.

Sovereignty is equally important – Ethereum should be able to defend against more subtle 51% attacks such as short-range reorgs and censoring ([link](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/attack-and-defense/#attackers-with-50-stake)), and should be able to resist coercion by state actors. If Ethereum loses sovereignty (aka autonomy), it loses its value as a neutral settlement mechanism:

> "Decentralization" is the broad distribution of a system's intrinsic/accepted forms of power, protecting users against arbitrary exercises of power from the recognized legitimate 'authorities' within the system's logic (e.g., validators). "Autonomy" is the system's resistance against extrinsic/unaccepted forms of power, protecting users against all exercises of power from authorities outside the system's logic (e.g., government authorities).
> Source: lex_node (link)

While 34% attacks are costly and 51% attacks are to some extent bounded by reputation and social slashing, a gradual coercion by state actors on independent validators is more feasible, and can even be unintentional. For instance, the European Securities and Markets Authority (ESMA) recently suggested ([link](https://www.esma.europa.eu/press-news/consultations/consultation-technical-standards-specifying-certain-requirements-mica-3rd#responses)) viewing MEV as a form of market manipulation subject to notification requirements from validators. Such regulations could make it impracticable for node operators to continue to function in Europe. In a worst-case outcome, these regulations could propagate to the rest of the world and impose artificial restrictions on how the consensus algorithm works.

High autonomy is therefore maintained through robust decentralization among validators, which includes:

- Client software diversity: running different types of validator software to avoid concentration risk from bugs.
- Node operator diversity: different, independent entities running validator software to prevent individual node operators reaching higher levels of control.
- Geographic and jurisdictional diversity: different levels of base-level infrastructure — such as connectivity to the internet, power supply, law authorities and jurisdictions — that are capable of influencing node operators.

### 1.2. A diverse staking economy is key

#### 1.2.1. Stakers

Stakers fall into three main categories:

1. Retail and Institutions: These participants delegate their staking to Centralized Exchanges (CEXs)
2. On-chain Actors: They delegate their staking to Decentralized Staking Middleware (DSM), such as Liquid Staking Tokens (LSTs) or decentralized pools, as well as Liquid Restaking Token protocols (LRTs) and Centralized Staking Providers (CSPs).
3. Solo Stakers: These users choose not to delegate and run validators independently

#### 1.2.2. Validating entities

[![tg_image_4158519118](https://ethresear.ch/uploads/default/optimized/3X/e/4/e4e64e83cbc59b58fdfe0316e37c8b548dfb52d8_2_690x469.jpeg)tg_image_41585191181920×1307 130 KB](https://ethresear.ch/uploads/default/e4e64e83cbc59b58fdfe0316e37c8b548dfb52d8)

*Note: CSP numbers do not include capital delegated from DSM/LRTs. The above numbers are approximate and for illustration purposes; they are our best estimates from Dune ([1](https://dune.com/hildobby/eth2-staking), [2](https://dune.com/lido/eth-deposits-stats)), as of June 30th 2024.*

A hypothetical scenario where most ETF Ether is staked with custodial services, like Coinbase, suggests that this is where most of future inflows will likely originate. Recent Bitcoin ETFs have seen ~$15b of inflows. Proportionally applied to Ethereum, this could mean about 4m ETH. Notably, 8 out of 11 Bitcoin ETFs use Coinbase as their custodian, a pattern that may repeat with ETH.

#### 1.2.3. Entities’ decentralization

Contributions to decentralization and thus censorship resistance and neutrality can be approximated as follows: Solo Stakers > Decentralized Staking Middleware > Liquid Restaking Protocols > Centralized Staking Providers > CEXs.

- Solo Stakers: Contribute the most to decentralization because each adds an additional validator
- DSM: Efficiently distribute delegated stake among many parties, bonded via reputation (Lido) or collateral (Rocket Pool, Lido’s Community Staking Module). Their impact on Ethereum’s decentralization is measurable and significant, with data on operational diversity publicly available and regularly updated (link). The Herfindahl-Hirschmann Index (HHI) can also provide a useful proxy on the effect on validation concentration (link)

[![dune_hhi](https://ethresear.ch/uploads/default/optimized/3X/b/4/b4d2e88d63be2c26d7397166220ad2752e954a34_2_690x411.png)dune_hhi3602×2150 389 KB](https://ethresear.ch/uploads/default/b4d2e88d63be2c26d7397166220ad2752e954a34)

- Restaking Infrastructure: While not cost-optimized for native staking, these protocols distribute stake among fewer node operators without aggregating it under one entity
- Centralized Staking Providers: Risk aggregating large amounts of stake, but competition among them can bolster decentralization if many can sustain independent businesses
- CEXs: Benefit the most from the power law distribution of AUM, often driving staked ETH concentration. Coinbase, for instance, is the largest node operator with nearly 15% market share.

### 1.3. There is no future-proof safe level of Security

Anders Lowsson suggests ([link](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/)) that Ethereum should reduce its issuance, arguing that “excessive incentives for staking, beyond what is necessary for security, can unfortunately over time turn into perverse subsidies, with many downsides.” However, this raises the question of what constitutes “adequate incentives for staking” and what level of security is truly necessary.

> What exactly is "neutrality"? I see that term being used in handwavy fashion, especially when scaling comes up, and it's hard to know what we mean by "preserving credible neutrality" at the moment. Would be nice to get some info there. :)
> Source: eawosikaa (link)

Today’s global capital markets are valued in the hundreds of trillions of dollars, while Ethereum represents only a tiny fraction of that. For Ethereum to become a neutral settlement layer for the world, its cost of corruption would need to be in the hundreds of billions, if not trillions, of dollars, to capture the value that could be extracted in a possible attack. For context, large value payment systems (excluding retail payments) cleared quadrillions of dollars in value in 2022 ([link](https://data.bis.org/topics/CPMI_FMI/tables-and-dashboards/BIS,CPMI_T9,1.0?view=value&dimensions=REP_CTY%3AUS)). In comparison, over the past 12mos, stablecoin transfer value on Ethereum just about cleared $8tn, or 0.5% ([link](https://www.theblock.co/data/stablecoins/usd-pegged/adjusted-on-chain-volume-of-stablecoins-monthly)). This is consistent with the proportion of market capitalization of Ethereum relative to global capital markets (well under 1% as well).

The slightest risk of insufficient security would stagnate Ethereum’s growth – decentralization and the resulting neutrality is Ethereum’s #1 competitive advantage. No risk should be taken to erode that, and instead, we should seek to strengthen it even further. To answer Emmanuel’s question, in our framing, we would use “neutrality” interchangeably with “sovereignty” and “autonomy”: ability to defend against censorship and coercion attacks ([link](https://nakamoto.com/credible-neutrality/)). Such that the cost of “coercion” is always higher than the benefit from manipulating the state.

Anders’ argument assumes that a 34% double-singing attack is so costly and 51% censorship attack is so unlikely today, that the network can afford to focus on strengthening other layers. If Ethereum were already a major part of the world’s capital markets, this argument might hold more weight, as incremental risks would be smaller. However, reducing today the network’s most crucial features—security and sovereignty—would compromise the network’s ability to grow.

Currently, Ethereum’s social layer serves as the final defense ([link](https://ercwl.medium.com/the-case-for-social-slashing-59277ff4d9c7)) against norm violations that threaten its credible neutrality. However, this social layer is structurally fragile. It requires constant vigilance from the community so that enforcement can occur on a daily basis. Yet, as Ethereum grows, massive new inflows might bypass today’s social layer altogether. If a large bank, say, staked $1tn worth of Ether with a CEX, what chance does a community of open source developers have to enforce social norms? The key question, as Emmanuel points out, is: What is the threshold for security that Ethereum needs today and in the future? The MVI proposal, in our view, fails to address this critical question, focusing instead on the other effects of reducing the security budget.

### 1.4. Reframing the discourse: expansion over efficiency

Ethereum should balance incentives for all stakeholders to ensure the highest level of security. This balance involves weighing long-term sustainability and expansion vs short-term efficiency to create enduring security value.

MVS suggests that instead of asking “how much could we reduce issuance for staking efficiency”, we should be asking “how much network incentivisation do we need to perpetuate decentralization to maintain and expand security”.

Strategically, MVI and MVS represent two different paths for Ethereum’s growth. MVI focuses on minimizing costs, benefiting ETH holders in the short term. MVS, on the other hand, emphasizes building a long-lasting moat around the network, optimizing long-term value creation for all stakeholders, including ETH holders.

Ethereum’s unique appeal lies in its secure, credibly neutral blockspace. Unlike commodity blockspace, which competes on price, secure blockspace competes on features. Similar to the advanced chip industry, where success depends on computational ability rather than price, Ethereum should compete on the magnitude of security it offers. This security creates an enduring competitive advantage, accelerating value creation across the ecosystem.

There is a subtlety in that the market cap of Ethereum is a variable that contributes to security, and so minimizing issuance can be seen as bolstering security. Superficially, there is a reflexive effect, where Ethereum’s security both causes and is driven by its market cap. However, we believe that Ethereum’s security making ETH valuable is the primary causation, and therefore security needs to be prioritized. Below we illustrate diagrammatically the alternative value creation paths for Ethereum contributors deciding between MVS and MVI.

[![tg_image_2418175601](https://ethresear.ch/uploads/default/optimized/3X/1/f/1f2963c356b0018f378fbf4fe73ef79e641aa362_2_530x500.jpeg)tg_image_24181756011357×1280 148 KB](https://ethresear.ch/uploads/default/1f2963c356b0018f378fbf4fe73ef79e641aa362)

## 2. Analysis of Ethereum Issuance reduction proposal within the MVS framework

We posit that, under the MVS framework, Ethereum issuance reduction proposals risk creating downstream effects that would compromise Ethereum’s security value. Overall, we believe that ETH’s moneyness stands to increase with greater security and autonomy, to a degree that far outweighs the downsides of issuance or externalities such as capital gains taxes.

### 2.1. The assumption that Ethereum overpays for security is wrong: less issuance may lead to centralization of the validator set

#### 2.1.1 ETF inflows would exacerbate centralization in the context of a 33% stake cap

Lowering the target stake ratio ([link](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751)) could lead to a concentration of staked ETH with Centralized Exchanges (CEXs), driving capital away from decentralized alternatives.

Consider a scenario where a 33% cap (equivalent to 40.6 million staked ETH) is implemented, and the curve enacts a sharp drop of yield to zero as stake ratio increases from 30% (36.6 million ETH) to 33% (40.6 million ETH). Suppose Ether ETFs are launched in the US, attracting significant capital inflows. If these ETFs use Coinbase as their custodian (as 8 out of 11 BTC ETF issuers do), this could lead to $15 billion in inflows, adding approximately 4.5 million ETH to Coinbase’s custody. The simulated impact on the validation market might look like this; the 40.1m max staked ETH being slightly lower then 40.6 represents the fact that when yield becomes extremely low there is no marginal staker at all on the market.

| Illustrative impact on validation market with a 33% MVI limit | Current composition | Effect in 4 years | Future composition |
| --- | --- | --- | --- |
| ETH staked | 33.1m | +7m | 40.1m |
| ETH held with Coinbase | 17.5m | +4.5m (ETFs) | 22m |
| ETH held & staked with Coinbase | 4.3m | +10m | 14.3m |
| ETH staked on-chain via LSTs/LRTs | 13.7m | -2m | 11.7 |
| ETH staked by other entities | 15.1 | -1m | 14.1 |

1. Market forces and fiduciary duties ensure that CEXs like Coinbase squeeze the maximum amount of profit from staking-as-a-service (for their customers and ETF issuers), and long-term the majority of their holdings are staked.

We model the above impact by assigning a 10m staked ETH inflow to Coinbase. When Coinbase’s stake reaches 7.8 million, total staked ETH will be about 36.6 million, causing rewards to drop sharply. Consequently:

1. Lido stETH and other LST/LRT users, being sophisticated on-chain actors, will seek higher rewards elsewhere. The switching cost of moving capital on-chain is extremely low, so there is no incentive for capital to stay – the capital will leave for higher yields in DeFi.
2. CSPs will exit these protocols since the 5% fee from middleware won’t cover their costs.

We model the above two impacts by assigning a 2 million ETH outflow to LSTs/LRTs and a 1 million ETH outflow to other entities.

1. Meanwhile, CEXs like Coinbase can continue offering staking products because their marginal costs are extremely low, and can even be offset by other business segments. Their customers may remain loyal or lack alternatives due to regulations or unsophisticated nature of the user base. This can happen despite Coinbase having higher fees (25%) compared to better-performing alternatives (5-15%).

In this scenario, Coinbase could control 14.3 million ETH, surpassing the 33% network control threshold independently, while Lido and other DSMs lose market share.

#### 2.1.2 Staked ETH concentration with CEXs doesn’t necessarily have to happen with a higher stake cap

Without the cap, both CEXs and on-chain market segments could coexist without putting pressure on each other due to sufficient demand for staking. LSTs, LRTs and CSPs wouldn’t face the dramatic yield decrease that would occur when Coinbase’s stake reaches 7.8 million ETH. Some might argue that Coinbase would undercut other staking providers by lowering its 25% fee. However, this is uncertain. Coinbase’s customer base seems inelastic, meaning the most profitable strategy might be to maintain or even increase their fees. In addition, even if Coinbase goes after the on-chain market and lowers their fees, the market may not be fully efficient – some people might prefer to stick with LSTs due to their decentralization preference.

In a highly segmented market, margins don’t need to uniformly compress, leaving space for both CEXs/CSPs and LSTs/restaking segments to thrive. LSTs and CEXs serve distinct market segments. For CEXs, the most profitable approach is to charge high fees from retail and institutional clients (e.g., Coinbase’s 25%) without directly competing with LSTs. Targeting stake ratios could stifle the market for on-chain actors but not significantly affect the market for retail and institutional clients.

Thus, in the absence of a stake cap, the coexistence of various staking actors could lead to a more balanced distribution of staked ETH across different market segments.

#### 2.1.3 MVI effect on the ratio of solo stakers

##### The importance of this effect is overrated

Approximately 30 million ETH is delegated, while only 3 million is solo staked. It is evident that delegation dominates as a modality of staking. The key issue is ETH concentration with CEXs, rather than the interaction between solo stakers and LSTs.

| Grouping | Approximate stake | Type |
| --- | --- | --- |
| CEXs | 10m | Delegated |
| LSTs, LRTs, CSPs | 20m | Delegated |
| Solo stakers | 3m | Solo staked |

##### LSTs and CSPs can also contribute to overall network quality

While solo stakers are often seen as the backbone of Ethereum’s network security, the contributions of LSTs and centralized staking providers are undervalued.

There is a lot of nuance to the emergent risks of malicious actors emerging from LSTs such as Lido. There certainly are risks (cf. Mike Neuder’s extensive post on the subject, [link](https://notes.ethereum.org/@mikeneuder/magnitude-and-direction)). However, there are also many benefits to deterministic stake allocation to professional or larger node operators. It’s possible for solo stakers to have different motivations than an LST whose main objective is to decentralize Ethereum validation ([link](https://research.lido.fi/t/lido-dao-vibe-alignment-purpose-mission-vision/)). Some of the most noteworthy examples of malicious proposers, for example, have come from solo validators, such as those involved in the April 3rd, 2023 MEV Boost exploit ([link](https://collective.flashbots.net/t/post-mortem-april-3rd-2023-mev-boost-relay-incident-and-related-timing-issue/)).

Centralized staking providers and LSTs are quantifiably more performant validators than solo stakers. There is significant existing data ([link](http://rated.network/)) today to quantify proposer effectiveness and attester effectiveness, which drive fewer missed slots and attestations, faster block propagation and chain finalization. Overall the network is much more stable and responsive with professional validators than it would otherwise be, but also more decentralized.

##### Issuance reductions would likely decrease the share of solo stakers

Some argue that solo stakers are less elastic with respect to yield, because they are as a cohort more heterogeneous than other validating entities, and hence have a steeper supply curve.

However, our simplified analysis of Ethereum validator economics shows this argument is flawed. Solo stakers in fact have much higher fixed costs, making them much less adaptable to a low issuance rates compared to larger node operators. Specifically,

For solo stakers:

- Staking APR is lower and closer to the Median staking APR (i.e. 2.4% per Rated, link) than scale node operators due to the unpredictability of proposer rewards, tips and MEV
- The costs of running a single validator include hardware (32 GB RAM, 4 TB SSD) and electricity. Home internet plans are sufficient for solo stakers, so broadband cost is assumed to be 0 (no incremental cost).
- In this set up, 100% of solo staker’s total costs are fixed costs. Assuming hardware depreciation of 5 years, profit margins are >90% to solo stakers
- We exclude the need to reserve 32 ETH in capital as collateral, which brings the capital outlay (though not outright investment) significantly higher

Then consider, on the opposite end of the spectrum, a large centralized node operator with 100,000 validators:

- Staking APR is higher and closer to the Average staking APR (i.e. 3.3% per Rated, link) as stake pooling smoothes the unpredictable components of both CL (proposer rewards) and EL (tips + MEV) rewards
- Costs include hardware but also significant operational costs including technical and marketing staff
- Hardware and internet are fixed costs, electricity is a variable cost and staff costs can be seen as a semi-variable cost

Employment footprint can be eventually adjusted should the top line be negatively impacted

Counting half of the maintenance & growth spend as fixed and the other half as variable, we arrive at fixed costs representing 64% of the large node operators’ total costs (i.e. much less than solo stakers). Profit margins are also lower than those of solo stakers

| Assumptions |  |
| --- | --- |
| ETH ($) | 3,500 |
| Average staking APR | 3.3% |
| Median staking APR | 2.4% |
| MVI reduction assumed | 2.0% |

| Illustrative Annual P/L | Current |  |  |  |
| --- | --- | --- | --- | --- |
|  | Solo Staker |  | Large Node Operator |  |
|  | Quantity | $ | Quantity | $ |
| # of validators | 1 | 112,000 | 100,000 | 11,200,000,000 |
| Staking APR |  | 2.4% |  | 3.3% |
| Staking income |  | 2,677 |  | 367,360,000 |
| Commission |  |  | 10% | 36,736,000 |
|  |  |  |  |  |
| Hardware cost |  | 800 |  | 7,750,000 |
| Computer/servers | 1 | 800 | 350 | 7,000,000 |
| Backup servers |  |  | 100 | 750,000 |
|  |  |  |  |  |
| Operational cost |  | 74 |  | 19,794,780 |
| Electricity | 70Wh, $0.12/kWh | 74 | 750Wh/server, $0.12/kWh | 354,780 |
| Internet connection | No incremental cost | 0 | 540GB/month/val @ $0.03/GB | 19,440,000 |
|  |  |  |  |  |
| Maintenance & growth |  | 0 |  | 11,400,000 |
| Technical staff |  | 0 | 70 | 8,400,000 |
| Marketing/admin staff |  | 0 | 30 | 3,000,000 |
| Cybersecurity/miscellaneous |  | 0 |  | 1,000,000 |
|  |  |  |  |  |
| Total cost (assume 5Y hardware depreciation) |  | 234 |  | 32,744,780 |
| o/w fixed cost |  | 100% |  | 64% |
| o/w variable cost |  | 0% |  | 36% |
| Payback period on capex (months) |  | 3.9 |  | 23.3 |
| Annual income/loss |  | 2,443 |  | 3,991,220 |
| Profit margin (excl. ETH at stake) |  | 91.3% |  | 10.9% |

In the event that MVI reduces staking APR for all stakers (e.g. -200bps), the below scenario analysis helps visualize how different stakers may be impacted differently. High level:

- Solo stakers have very limited, if no, way of adjusting their underlying costs. 100% of the reduced staking rewards will fall through to the bottom line, resulting in a dramatic reduction in profit margin. As a result, the payback period on capex (i.e. hardware) multiplies from 3.9 months to 47.2 months in our example, without considering the need to raise 32 ETH to activate a validator to begin with. This raises the question of whether incremental demand from new solo stakers could be sustained in the post-MVI world
- Meanwhile, large node operators have more levers to pull to protect their profits and capex payback periods

As in Scenario 1, node operators can raise their commission
- As in Scenario 2, node operators can raise their commission and reduce variable costs, notably staff costs
- With very minor changes to their structure they can come back to prior levels of profit

| Illustrative Annual P/L | If staking APR reduces by 200bps |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  | Solo Staker |  | Large Node Operator - Scenario 1 |  | Large Node Operator - Scenario 2 |  |
|  | Quantity | $ | Quantity | $ | Quantity | $ |
| # of validators | 1 | 112,000 | 100,000 | 11,200,000,000 | 100,000 | 11,200,000,000 |
| Staking APR |  | 0.4% |  | 1.3% |  | 1.3% |
| Staking income |  | 437 |  | 143,360,000 |  | 143,360,000 |
| Commission |  |  | 25% | 35,840,000 | 25% | 35,840,000 |
|  |  |  |  |  |  |  |
| Hardware cost |  | 800 |  | 7,750,000 |  | 7,750,000 |
| Computer/servers | 1 | 800 | 350 | 7,000,000 | 350 | 7,000,000 |
| Backup servers |  |  | 100 | 750,000 | 100 | 750,000 |
|  |  |  |  |  |  |  |
| Operational cost |  | 74 |  | 19,794,780 |  | 19,794,780 |
| Electricity | 70Wh, $0.12/kWh | 74 |  | 354,780 |  | 354,780 |
| Internet connection | No incremental cost | 0 |  | 19,440,000 |  | 19,440,000 |
|  |  |  |  |  |  |  |
| Maintenance & growth |  | 0 |  | 11,400,000 |  | 10,504,000 |
| Technical staff |  | 0 | 70 | 8,400,000 | 64 | 7,739,789 |
| Marketing/admin staff |  | 0 | 30 | 3,000,000 | 28 | 2,764,211 |
| Cybersecurity/miscellaneous |  | 0 |  | 1,000,000 |  | 1,000,000 |
|  |  |  |  |  |  |  |
| Total cost (assume 5Y hardware depreciation) |  | 234 |  | 32,744,780 |  | 31,848,780 |
| o/w fixed cost |  | 100% |  | 64% |  | 66% |
| o/w variable cost |  | 0% |  | 36% |  | 34% |
| Payback period on capex (months) |  | 47.2 |  | 30.0 |  | 23.3 |
| Annual income/loss |  | 203 |  | 3,095,220 |  | 3,991,220 |
| Profit margin (excl. ETH at stake) |  | 46.5% |  | 8.6% |  | 11.1% |

*Illustrative figures can be found [here](https://docs.google.com/spreadsheets/d/1tr7VJqzJLiywf34_debHa20wfjU5d8db1eYrJWU0i3Q/edit?gid=0#gid=0)*

Due to the presence of a higher proportion of fixed costs, solo stakers (and smaller node operators alike) will show higher sensitivity to changes in staking rewards compared to larger node operators. The corollary is that as MVI reduces staking reward APR, the marginal players may be priced out, leading to a greater centralization of stake. This would exacerbate the already decreasing trend of solo stakers alongside Ethereum’s issuance compression over time.

[![dune_marketshare](https://ethresear.ch/uploads/default/optimized/3X/c/7/c75ca71bdb5bbc1207a30f9439fd1dc937b2aa59_2_690x411.png)dune_marketshare3602×2150 522 KB](https://ethresear.ch/uploads/default/c75ca71bdb5bbc1207a30f9439fd1dc937b2aa59)

*Source: Dune ([link](https://dune.com/queries/3852057/6478867))*

### 2.2. LST dominance and cost-modeling are inadequate arguments for issuance reduction

#### 2.2.1. Issuance as a cost is a reductive framing

“Issuance as a cost” concerns the dilution effect on native ETH holders and the potential welfare loss due to externalities like taxes.

The first component focuses on the direct impact of issuance. It redistributes network ownership from unstaked ETH holders to staked ETH holders. High issuance rates force ETH holders to stake to avoid dilution. This increases Ethereum’s security and neutrality but comes with inconvenience and some risk for native ETH holders – which, under MVS, doesn’t qualify as strongly undesirable. Moreover, the cumulative effect could even be seen as beneficial, to the extent that more stake landing with a distributed set of validators justifies investors’ inconvenience.

The second component addresses additional costs for stakers due to taxes. ETH holders who earn staking rewards may face tax obligations, creating additional sell pressure. However, this concern is specific to certain jurisdictions and points in time. Furthermore, the impact of this sell pressure on Ethereum’s overall functionality is questionable. Assuming 3.5% staking rewards, a $400bn ETH market cap, and 30% average taxes paid by all stakers, we get $4.2bn in annual sell pressure. Given Ethereum’s daily trading volume is in billions, absorbing 1% sell pressure over a year seems immaterial. Furthermore, LSTs such as wstETH may even provide an efficient way to postpone the tax payments, since the tax event might be triggered only when wstETH is sold.

Even though ETH market cap is significant in determining attack costs, the relatively minor effect of sell pressure does not provide enough security benefits to justify reducing issuance. The trade-offs include potential staked ETH concentration, loss of sovereignty, and a more substantial decrease in market cap as a result.

#### 2.2.2. Stakers getting higher real vs nominal yield is not significant

This argument, while mathematically beautiful ([link](https://notes.ethereum.org/@mikeneuder/subsol#3-Scaled-Root-Curve-alternative-issuance)), is not significant in magnitude. It does not affect security and neutrality in any way; in fact, it is not at all clear if there is any benefit to Ethereum in fewer stakers getting higher real yield compared to more stakers getting less real yield. In addition, this analysis assumes concave supply curves with respect to nominal yield, while it is possible that at a higher staking ratio we should adjust our analysis to concave supply curves with respect to real yield.

#### 2.2.3. Reducing LST dominance shouldn’t be a primary objective of Ethereum’s monetary policy

This argument is directly related to security and neutrality, and thus can be analyzed under a security-maximizing framework.

In his article ([link](https://notes.ethereum.org/@mikeneuder/magnitude-and-direction)) Mike Neuder analyzed various directions and magnitudes of possible Lido attacks on Ethereum in the future. While there are several potential attacks, all of them have a corresponding mitigation plan. Dual governance is at the heart of many of those mitigations. DG is a mechanism that allows stETH holders to slow down Lido’s governance and exit from the protocol before any decision is made. This mechanism is in active and final stages of development ([link](https://research.lido.fi/t/dual-governance-design-and-implementation-proposal)).

Another argument for issuance reduction is that stETH risks substituting ETH as the de-facto money and collateral. While there is certainly a possibility that LSTs wind up replacing a lot of ETH functionality in DeFi, it does not diminish the moneyness of ETH – all LSTs are underscored by ETH, and thus derive their value from ETH. In order to execute any of these transactions, users will still need ETH to pay for gas, at the very least. Furthermore, ETH will continue to be bridged to various L2s either way, so at a baseline ETH velocity will already decline with broader adoption of L2s, without compromising its moneyness.

Finally, there are unintended consequences to targeting individual applications in an opinionated manner in order to manipulate the viability of ETH as collateral or as commodity money. The long-term roadmap of Ethereum should not be hostage to short-term tactical considerations, least of all on the application layer. The growth of LSTs has allowed the growth of user activity on Ethereum and has also increased the velocity and usage of Ether itself.

## 3. Putting it all together

MVI, as a framework, ultimately suggests to squeeze as much as possible out of staking, so that stakers’ cost and revenue are more or less at the same low rate. The major problem of this approach is that market forces structurally do not reward decentralization, and ultimately drive stake concentration to CEXs, which are entities with the lowest cost validators and the most inelastic customer base. Thus the downside of MVI is undermining the security and neutrality of Ethereum. In our view, the benefits of MVI, such as decreasing the selling pressure from taxes, do not justify taking this risk on balance.

MVS, on the other hand, suggests evaluating monetary policies primarily through the lens of how it affects security and neutrality, the core value propositions of Ethereum. One of the arguments for issuance reduction, namely to tackle LST dominance, indeed falls into MVS focus. However, the security and neutrality concerns of LST dominance are of second order in nature (“if dual governance doesn’t work”, “LST becomes an additional risk layer for all users”, etc). Meanwhile, stake accumulating in CEXs rather than in LSTs, LRTs or even CSPs creates a very real risk of staked ETH concentration with one single entity. As such, we do not see the case where LST dominance risk outweighs the risk of stake concentration with CEXs.

While we presented the MVS framework, and accordingly evaluated the issuance reduction proposal, the natural question stands: what would be the right issuance policy under the MVS approach? This is an incredibly complex and deep question that we would like to explore in future. Some of the directions that we have in mind include:

- How do we quantifiably measure security? Is there a way for a protocol to see its security? Credit to the contributions from the StakeSure (link) paper in this direction.
- Guided by MVS, rather than focusing on value creation through cost reductions, we should instead consider the value creation by improving security and neutrality. There is a heuristic argument that increasing issuance can improve security through making the network more complex via a more diverse validator set. Is there a way to make this precise? How do we make sure that the extra issued ETH strictly improves security and neutrality?
- Is there a case for a marginal improvement analysis: the more diverse the validator set is, the more complex the network becomes, and improvements to security could have increasing marginal contributions. (Similar to how complexity contributes to entropy and layered security, link)

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/f/1f6daf84bc2dfabd3b7747f049d71b9597079ddb_2_690x389.jpeg)image1626×918 107 KB](https://ethresear.ch/uploads/default/1f6daf84bc2dfabd3b7747f049d71b9597079ddb)

---

*Disclosure: authors are variously affiliated with cyber.fund, Lido DAO, Steakhouse Financial, Progrmd Capital*

## Replies

**aelowsson** (2024-07-07):

Thank you for your contribution to the issuance debate. I will offer some brief remarks on your post, often including links to the [issuance reduction FAQ](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675).

### Section 2

The modeling in [Section 2.1.3](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#issuance-reductions-would-likely-decrease-the-share-of-solo-stakers-18) is very problematic. It is not correct to base a solo staker’s yield on the short-term median and a delegating staker’s yield on the average. The expected staking yield that solo stakers and staking service providers (SSPs) take home is [essentially the same](https://www.reddit.com/r/ethereum/comments/191kke6/comment/kh7egkd). If the idea is to account for variability in staking rewards for solo stakers, a review of the post on properties of issuance level would be fruitful. Figure 9 in [Section 4.2](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-42-effect-of-pooling-14) illustrates how variability in rewards varies with pooling over a year when 29M ETH is staked (based on data of MEV over the preceding year). I reproduce it here and highlight the tiny vertical line segment of the black line, representing only 5 % of 32-ETH stakers over a year. These are the unlucky solo stakers that the text bases its analysis on (note that the expected yield is the same because there are also lucky solo stakers). Over 2-3 years, this vertical line goes away. It would be better to have the expected yield the same for both parties. Variability can still be woven into the argument.

[![Expected yield and short-term median](https://ethresear.ch/uploads/default/optimized/3X/9/6/961dfdfc0f005b0d9ded768ec78c3da79ca233bf_2_690x388.png)Expected yield and short-term median1920×1080 323 KB](https://ethresear.ch/uploads/default/961dfdfc0f005b0d9ded768ec78c3da79ca233bf)

Another remark concerning the model:

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> As in Scenario 1, node operators can raise their commission
> As in Scenario 2, node operators can raise their commission and reduce variable costs, notably staff costs
> With very minor changes to their structure they can come back to prior levels of profit

If this is so simple, why don’t they do it right now? In any case, note that if node operators raise their commision, the gap between how much of the staking yield that befalls the delegator and solo staker increases. From the perspective of retaining a higher proportion of solo stakers, this could be considered as beneficial.

---

Concerning [Section 2.1.1](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-211-etf-inflows-would-exacerbate-centralization-in-the-context-of-a-33-stake-cap-13):

[quote="xadcv, post:1, topic:19992”]

Market forces and fiduciary duties ensure that CEXs like Coinbase squeeze the maximum amount of profit from staking-as-a-service (for their customers and ETF issuers), and long-term the majority of their holdings are staked.

We model the above impact by assigning a 10m staked ETH inflow to Coinbase.

[/quote]

I would expect some actual model here. How do you explain the assigned 10M staked ETH to Coinbase in light of the steady decline among the CEXes in red in the Dune graph in Section 2.1.3 (Coinbase, Kraken, Binance, Bitcoin Suisse)? This decline has taken place even as the staking yield has gradually fallen.

---

[Section 2.1.2](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-212-staked-eth-concentration-with-cexs-doesnt-necessarily-have-to-happen-with-a-higher-stake-cap-14) feels like a restatement of the associated [discussion](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#equilibrium-yield-and-the-broader-composition-of-the-staking-set-27) in the FAQ. While my biggest [concern](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#equilibrium-yield-and-the-proportion-of-solo-stakers-24) is the proportion of solo stakers, [I still think](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#h-4-economic-capping-34) we can cap the stake, just not at 25%.

---

[Section 2.2.1](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-221-issuance-as-a-cost-is-a-reductive-framing-20) “Issuance as a cost is a reductive framing”: does *not* fully address issuance as a cost, rather just taxes.

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> The second component addresses additional costs for stakers due to taxes.

This gives a very incomplete picture of issuance policy. The welfare gain to Ethereum from an issuance reduction is addressed in two parts in the FAQ. The first part that we will focus on here explains how [reduced costs raise welfare](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#h-1-reduced-costs-raise-welfare-6).

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png)[FAQ: Ethereum issuance reduction](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675/1)

> Review Figure 1 (example with more details here), featuring a hypothetical future supply curve  in blue. The supply curve indicates the amount of stake deposited D at various staking yields y. It captures the implied marginal cost of staking. What that means is that every ETH holder is positioned along the supply curve according to how high cost they assign to staking, with their required yield reflecting that cost. Relevant costs include hardware and other resources, upkeep, the acquisition of technical knowledge, illiquidity, trust in third parties and other factors increasing the risk premium, various opportunity costs, taxes, etc. The area above the supply curve indicates the stakers’ surplus (what they actually gain). The area below the supply curve—the supply curve’s integral—indicates the costs assigned to staking (the marginal staker would not stake at a yield below the supply curve).
>
>
> Figure 13133×1864 380 KB
>
>
> Figure 1. Implied cost (blue) and surplus (grey) of staking under a hypothetical future supply curve. A change in issuance policy shifts the equilibrium from the black square to the green circle. The cost reduction (dark blue) leads to aggregate welfare improvement as long as the protocol remains secure and decentralized, and the reduction in surplus (dark grey) simply shifts some utility from stakers to everyone.
>
>
> Two reward curves are shown, with maximum extractable value (MEV) added to the staking yield. In this FAQ, MEV will be 300k ETH/year (close to the average over the last few years) and include priority fees. By maintaining the current reward curve in black, Ethereum compels users to incur higher costs than necessary for securing the network. Adopting the green reward curve 1 eliminates the costs represented by the dark blue area (around 450 000 ETH), thus improving welfare. The issued ETH covered for hardware expenses, taxes, reduced liquidity and risks that users would choose to sidestep under a lower yield. With the green curve, they can, and the benefits are shared by everyone, including remaining stakers. This creates value for all token holders through a reduction in newly minted ETH.

In other words, it is insufficient to only address taxes. Relevant costs include hardware and other resources, upkeep, the acquisition of technical knowledge, illiquidity, trust in third parties and other factors increasing the risk premium, various opportunity costs, taxes, etc. We know the cost that the marginal staker assigns to staking from the equilibrium, and can through assumptions regarding the slope of the supply curve quantify the welfare gain from an issuance reduction using the integral of the inverse supply curve. If we force users to choose between incurring costs as stakers, or to subject themselves to increased dilution under equilibrium, they might in the future simply decide to use another blockchain where the imposed costs are lower.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> #### 2.2.2. Stakers getting higher real vs nominal yield is not significant
>
>
>
> This argument, while mathematically beautiful (link ), is not significant in magnitude. It does not affect security and neutrality in any way; in fact, it is not at all clear if there is any benefit to Ethereum in fewer stakers getting higher real yield compared to more stakers getting less real yield. In addition, this analysis assumes concave supply curves with respect to nominal yield, while it is possible that at a higher staking ratio we should adjust our analysis to concave supply curves with respect to real yield.

Mostly correct. It is unfortunate that several researchers have pushed this angle without careful consideration, but it is not the fundamental argument for a reduction in issuance policy. The fundamental argument, as previously mentioned, is the cost reduction and macro perspective [addressed](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#why-should-ethereum-reduce-its-issuance-4) in the FAQ. In that answer, I outline precisely the topic brought up in Section 2.2.2, highlighting that we must focus on the cost reduction:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png)[FAQ: Ethereum issuance reduction](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675/1)

> When not explicitly highlighting the reduction in costs among those that stop staking as the issuance falls, value may appear to merely shift from one class of users to another in the form of a gain or loss in real/proportional yield. Issued tokens are redistributed among a different quantity of stakers, not creating any new value at the aggregate level. Without a division into cost and surplus, the welfare gain can get lost in translation, especially if it is not otherwise implied by remarking on the outcome among all users at the different equilibria.

Note that to the individual staker, the realization that issuance dilutes them may still be very important. Some stakers may otherwise look only at issuance yield, without considering how the issuance rate increases the inflation rate, ultimately reducing the proportion of all tokens they retain. There is value in highlighting that, even while it is not the reason to reduce issuance. This topic is discussed in a [separate answer in the FAQ](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#can-stakers-profit-from-a-reduced-issuance-and-what-is-the-relevance-and-impact-of-the-realproportional-yield-37), also addressing the influence of the slope of the supply curve, as discussed in Section 2.2.2, in the form of an [isoproportion map](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#the-isoproportion-map-42).

In my original [thread on minimum viable issuance](https://notes.ethereum.org/@anderselowsson/MinimumViableIssuance#Benefits-of-MVI-to-user-utility) I captured both the welfare gain (orange area in the figure from the link) and the benefit to the individual staker and non-staker (attainable change in proportion held, which has later been dubbed “real yield” or “proportional yield”) from an issuance reduction in a single graph. This treatment may have led some researchers to not fully appreciate that two separate issues were being simultaneously uncovered.

---

[Section 2.2.3](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-223-reducing-lst-dominance-shouldnt-be-a-primary-objective-of-ethereums-monetary-policy-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> Finally, there are unintended consequences to targeting individual applications in an opinionated manner in order to manipulate the viability of ETH as collateral or as commodity money. The long-term roadmap of Ethereum should not be hostage to short-term tactical considerations, least of all on the application layer.

It is very hard to understand this statement. Retaining a viable application layer is a key reason for pursuing MVI. A situation where some applications can be “held hostage” by an incumbent LST monopoly is scary. It would only benefit the SSPs at the expense of Ethereum’s users. Quoting from the FAQ:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png)[FAQ: Ethereum issuance reduction](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675/1)

> The macro perspective also extends beyond consensus. If one or a few LSTs overtake as money in the Ethereum ecosystem, they will embed themselves across every layer and application. An economy that is not powered by a trustless asset  is arguably not as resilient, regardless of if the consensus process itself is never threatened. The applications powering the money will gain an outsized influence over the applications using the money, and Ethereum will become a less desirable blockchain to build and develop on.

Francesco’s [tweet](https://x.com/fradamt/status/1760808900792594593) about retaining a trustless asset within Ethereum is particularly astute here.

*I find it surprising  that people seem to be ok with a future where eth is replaced by LSTs (possibly one, possibly custodial). What good is decentralization of staking if there is no trustless asset? Imho the staking economics debate should focus on this point first*

---

### Section 1

Quote from [Section 1.3](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992#h-13-there-is-no-future-proof-safe-level-of-security-9). “There is no future-proof safe level of Security”:

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> Today’s global capital markets are valued in the hundreds of trillions of dollars, while Ethereum represents only a tiny fraction of that. For Ethereum to become a neutral settlement layer for the world, its cost of corruption would need to be in the hundreds of billions, if not trillions, of dollars, to capture the value that could be extracted in a possible attack.

There is value in having a high cost-of-corruption (CoC). However, security needs to be approached holistically. Excessive issuance can render the native token less valuable in the long run, thus reducing the blockchain’s economic security. This is due to the welfare loss associated with compelling users to incur higher costs than necessary for securing the network, as previously discussed. The [perspective](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#what-about-economic-security-more-stake-makes-ethereum-more-secure-right-8) on economic security I outline in the FAQ seems reasonable in this context:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png)[FAQ: Ethereum issuance reduction](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675/1)

> #### What about economic security? More stake makes Ethereum more secure right?
>
>
>
> It is true that up to a certain point, more stake makes Ethereum more secure. But even before reaching this point, the marginal increase in security from adding another validator brings less utility to users than the utility loss stemming from the numerous downsides of excessive issuance (see the previous answer) that negatively affect users, builders, and holders of the ETH token. Ethereum’s economic security will in the long term inherently be linked to the ability of ETH to retain its value. A holistic perspective is therefore important also when considering economic security. This is underscored by reflecting on the early days of Ethereum, when the ETH token was much less valuable. Eight years ago, In May 2016, Vitalik deliberated on  the value that Ethereum can and cannot secure at a stake participation of 30%. At the time, the market cap of the ETH token was roughly 500 times lower than today, and the economic security that Ethereum could offer was therefore limited. Increasing stake participation from 30% to 60% would only increase the value of 1/3 of the stake (the threshold for the ability to delay finality) from $70M to $140M. This highlights that once the proportion staked has risen above insignificant levels, it will ultimately be Ethereum’s role in the world economy, and the ether’s role in the Ethereum economy, that determines the economic security…

I recognize that the post indeed takes a different stand on this topic in Section 1.4 and posits that it is instead increased stake participation that is a key to making ETH valuable. Besides the arguments against this that I have presented in my remarks so far, the argument can also be made that beyond certain levels of stake participation, even short-term security begins to degrade. The social layer may lose its neutrality and credibility as the ultimate arbitrator against attacks from dominant SSPs. This argument can be better understood by first analyzing our different positions on the topic as reflected in this part in the end of Section 1.3:

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> Currently, Ethereum’s social layer serves as the final defense (link) against norm violations that threaten its credible neutrality. However, this social layer is structurally fragile. It requires constant vigilance from the community so that enforcement can occur on a daily basis. Yet, as Ethereum grows, massive new inflows might bypass today’s social layer altogether. If a large bank, say, staked $1tn worth of Ether with a CEX, what chance does a community of open source developers have to enforce social norms? The key question, as Emmanuel points out, is: What is the threshold for security that Ethereum needs today and in the future? The MVI proposal, in our view, fails to address this critical question, focusing instead on the other effects of reducing the security budget.

This paragraph implies that the social layer must impose its will through the validator set. However, what is normally meant by the “final defense” is that the social layer can convene to act one layer above the consensus mechanism, in the event of, for example, a 51% attack. [People](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/attack-and-defense/#people-the-last-line-of-defense) are the last line of defense. In this regard, a proof-of-stake blockchain run by open source developers is certainly not helpless if a large bank were to degrade the consensus mechanism. There are a range of [defensive strategies](https://www.youtube.com/watch?v=1m12zgJ42dI&t=1712s), whose mere existence would presumably scare off any would-be attacker. This leads us to a discussion of the “[macro perspective](https://notes.ethereum.org/@anderselowsson/MinimumViableIssuance#Benefits-of-MVI-from-a-macro-perspective)”. A greater concern is namely what would happen if excessive issuance corrupts the social layer:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png)[FAQ: Ethereum issuance reduction](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675/1)

> An LST exceeding critical thresholds regarding the proportion of stake under its control may compromise the consensus mechanism. Outsized profits from blockspace are here a stratum for cartelization. But if everyone is compelled to stake, an entity or cartel of entities may also gain control over a significant proportion of the total ETH—propelled by network externalities such as the money function of an LST. These externalities are a stratum for cartelization extending outside of the consensus mechanism. The compromised institution also sits one layer above, namely the social layer.
>
>
> It became apparent with The DAO that if the proportion of the total circulating supply affected by an outcome grows sufficiently large, then the social layer may waver on its commitment to the underlying intended consensus process. An LST might grow “too big to fail ” in the eyes of the Ethereum social layer. If the community can no longer effectively intervene in the event of a 51% attack, then Vitalik’s warning system  and Danny’s recourses  may not be effective. Staking becomes so ubiquitous that the social consensus mechanism is overloaded. It is a special and in a way inverted case of issues Vitalik previously warned about.

### Section 3

Finally some notes on the conclusions where I somewhat repeat previous answers.

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> MVI, as a framework, ultimately suggests to squeeze as much as possible out of staking, so that stakers’ cost and revenue are more or less at the same low rate.

The marginal staker will always have the same cost as revenue under equilibrium—it derives no surplus. An important point of MVI is indeed to reduce costs for Ethereum’s users, thus providing a welfare gain to token holders. It follows from the notion of identical cost and revenue that this must involve a reduction in the marginal staker’s revenue.

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> the benefits of MVI, such as decreasing the selling pressure from taxes, do not justify taking this risk on balance.

Highlighting again that taxes are merely a small part of the costs, as explained in my answer relating to Section 2.2.1.

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> There is a heuristic argument that increasing issuance can improve security through making the network more complex via a more diverse validator set. Is there a way to make this precise?

I am not sure what you refer to by making the network more complex, but building a complex money-lego based on LSTs is in my view very problematic and can impute structural risks on Ethereum.

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> How do we make sure that the extra issued ETH strictly improves security and neutrality?

You can’t. The extra issued ETH will just compel users to take on more and more costs in aggregate (loss of liquidity, hardware costs, taxes, etc.).

---

**abcoathup** (2024-07-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> Disclosure: authors are variously affiliated with cyber.fund, Lido DAO, Steakhouse Financial, Progrmd Capital

Suggest putting your disclosure at the top of the post.

---

**xadcv** (2024-07-26):

Thank you for the detailed and considerate response, [@aelowsson](/u/aelowsson) and apologies for taking so long to reply. You make a lot of good points, which we try to summarize and steelman them in the below list. After that we list our comments in order.

1. Solo-staker modeling understates yield advantage: Our modeling of solo staker yield understates their actual performance and we incorrectly compare short-term medians for solo stakers and delegated staker averages
2. Node operators raising commissions could be beneficial to solo stakers: To wit, if node operators could raise their commissions under MVI and remain flat relative to today, why don’t they raise commissions today already?
3. CEX dominance is in decline today and we do not provide a model to support the idea that large inflows of new stake would accrue to them: Our assumption that 10m ETH flows into Coinbase staking is not congruent with the reality that CEX share of staking is in decline
4. Our framing of issuance cost is reductive and only focuses on taxes: it is insufficient to only address taxes, as we know the cost that the marginal staker assigns to staking from the equilibrium, and can quantify the welfare gain from an issuance reduction. If we force users to choose between incurring costs as stakers, or to subject themselves to increased dilution under equilibrium, they might in the future simply decide to use another blockchain where the imposed costs are lower
5. The social layer exerts its influence beyond the staking layer: beyond certain levels of stake participation, even short-term security begins to degrade. The social layer may lose its neutrality and credibility as the ultimate arbitrator against attacks from dominant SSPs
6. Allowing incumbent LSTs to dominate could lead to centralization: it is important to retain ETH as a trustless asset to ensure the ecosystem’s resilience and decentralization, as without it, Ethereum could become less attractive for development

---

## Our comments on the above

### Re 1: Solo-staker modeling understates yield advantage

Empirical data gathered by Rated Network shows the following:

| Realized Rewards Reference Rates |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
| Median | 1D | 7D | 30D | All time |
| Network APR% | 2.38% | 2.37% | 2.39% | 2.41% |
| Consensus Layer APR% | 2.38% | 2.37% | 2.39% | 2.41% |
| Execution Layer APR% | 0% | 0% | 0% | 0% |
|  |  |  |  |  |
| Average | 1D | 7D | 30D | All time |
| Network APR% | 3.35% | 3.39% | 3.37% | 3.43% |
| Consensus Layer APR% | 2.79% | 2.79% | 2.81% | 2.83% |
| Execution Layer APR% | 0.56% | 0.60% | 0.56% | 0.60% |
| Source: Rated |  |  |  |  |

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/7/c7ceb9241b11872f46a9329420fa4668d5c1b5d2_2_690x370.jpeg)image1920×1032 113 KB](https://ethresear.ch/uploads/default/c7ceb9241b11872f46a9329420fa4668d5c1b5d2)

The actual rewards earned by validators have been much lower than the figures shown in your simulated results. According to Rated, the APR earned across the entire active validator set (also known as the “realized rewards reference rate”) has an all-time median of 2.41% and mean of 3.43%. Your model appears to overestimate on both; the median for even a 32 ETH staker is showing ~3.6% while expected yield is 4.1%. In short, your curves would need to shift left if they were to more accurately describe the practical reality of staking.

It would be helpful to understand the assumptions behind your modeling. While some of the difference may be attributed to the increase in the staking ratio (from 29M ETH at the time of your writing to nearly 34M ETH today), we suspect the main cause lies in the difference between theoretical projections and real-world outcomes. As seen in the data from Rated, network effectiveness typically falls short of 100%, with smaller and less professional node operators often underperforming. This trend is reflected in the lower “[RAVER](https://docs.rated.network/methodologies/ethereum/rated-effectiveness-rating)” score for Rocketpool, which likely has a higher proportion of such node operators.

[Source](https://explorer.rated.network/explorer?network=mainnet&view=pool&timeWindow=all&page=1&pageSize=15&poolType=all)

[![unnamed-2](https://ethresear.ch/uploads/default/optimized/3X/b/b/bb61c07b7e9b3d36c16307371da307b18c5e4bf3_2_690x336.png)unnamed-21600×780 176 KB](https://ethresear.ch/uploads/default/bb61c07b7e9b3d36c16307371da307b18c5e4bf3)

We remain more comfortable using the empirically observed median to express the base case for solo and small stakers. This is because of the extreme positive skew of rewards for those participants (particularly proposer and EL rewards), such that averages can be misleading. Some will luck out and win frequent proposer blocks or attractive MEV, while the majority will not.

[Source](https://x.com/sui414/status/1811841295109025904)

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/9/4918c8558f18e0b7804ec1338c762dbd00456e87_2_690x353.png)image1388×712 63.7 KB](https://ethresear.ch/uploads/default/4918c8558f18e0b7804ec1338c762dbd00456e87)

Final remark on the yield variability. We refer to a preliminary [report](https://docs.google.com/document/d/1VQphb5NbeQGI2T3JRsLjeVaohb0ABn8X92huBB665Y4/edit) from one of the cyber•Fund MVI grantees, which shows that empirically, pools earn about 12% higher rewards than solos (*mean*, not median). This can be attributed to solo stakers’ lack of ability to compound, as well as not employing sophisticated strategies such as timing games. While we see the median as a more relevant measure of central tendency for solo stakers and smaller node operators, there is some evidence that even average rewards reaped by this cohort is meaningfully less than those of larger pools.

### Re 2: Node operators raising commissions could be beneficial to solo stakers.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> If this is so simple, why don’t they do it right now? In any case, note that if node operators raise their commision, the gap between how much of the staking yield that befalls the delegator and solo staker increases. From the perspective of retaining a higher proportion of solo stakers, this could be considered as beneficial.

They don’t do it now because there has not been a need to. However, we observe in practice that price elasticity is not equivalent across all channels and all stakers. Less sophisticated stakers, such as those that stake with CEX’s such as Coinbase, are less sensitive to price, instead valuing user experience and convenience more highly. On this segment, Coinbase already charges a 25% commission on staking, a hefty premium to the more common 10% commission charged by other competing staking-as-a-service providers. While the institutional market is price competitive, consolidation as a result of lower margins could make it less competitive for smaller operators, as we described, and force the market into an oligopoly of price-setting large players.

DeFi participants, including solo stakers, are arguably more sophisticated and therefore price-sensitive, prioritizing yield optimization. They may not always stake their 32 ETH, if staking APR declines and better on-chain opportunities exist. Contrast this with less sophisticated holders, such as ETF buyers, who may eventually accept any level of higher commissions on staking for incremental rewards.

In summary, varying sensitivity among staker profiles means that increased commissions by large node operators, in response to lower issuance, may not automatically benefit solo stakers and smaller node operators.

### Re 3: CEX dominance is in decline today and we do not provide a model to support the idea that large inflows of new stake would accrue to them

Tldr: We don’t have an accurate model, but try to think of the impact of an exogenous shock of large amounts of net new stake through inelastic channels (ETFs in particular), which we believe to be more than a realistic possibility.

The difficulty with these is that 1) identifying them in the first place is very hard, as there is no way (in and of itself) to assign a deposit address to an entity purely from on-chain activity, 2) each setup will have different user flows and characteristics that makes it difficult to accurately predict how stake allocation will behave under a steady state and 3) we are trying to forecast an illustrative impact of a large shock in the staking market on the basis of a qualitative assessment that institutional user behavior in certain product categories will be sticky

On 1), every CEX is a private business run for the benefit of its shareholders alone. This is generally a good thing and we should avoid the temptation to take a moralistic view with any choices that companies make, instead think only of incentives and model accordingly.

To witness how, for a private company, pressure to compete more dynamically in the staking market wins over pressure to offer more transparency to the community, we can look to CEX disclosures of ETH staked. For example, even Coinbase, which has been a hugely positive force for our industry, has been able to completely stop reporting information about how much ETH it stakes on behalf of customers without much pushback. Triangulating ETH staked at Coinbase was only possible as long as its investor materials reported the amount in quarterly disclosures, which it stopped doing as of Q4 2023. Not to single them out, as other leading CEXs also do not self-report anything at all.

[Source](https://x.com/hildobby_/status/1710326919898579023)

[![unnamed-4](https://ethresear.ch/uploads/default/optimized/3X/3/4/34d0c9010b7cbdbe503ad236897e5ed784e2b794_2_439x500.jpeg)unnamed-41388×1580 206 KB](https://ethresear.ch/uploads/default/34d0c9010b7cbdbe503ad236897e5ed784e2b794)

[Source](https://x.com/hildobby_/status/1786137965019767014)

[![unnamed-5](https://ethresear.ch/uploads/default/optimized/3X/9/0/905ed3d2504b35597b9610a25cda423180863f48_2_363x500.jpeg)unnamed-51162×1600 129 KB](https://ethresear.ch/uploads/default/905ed3d2504b35597b9610a25cda423180863f48)

So the first question is really whether the balances tracked on Dune are accurately labeled. For the sake of the argument, let’s assume that they are perfectly labeled. However, the point is that, even today, the public does not know for sure how much ETH is staked at Binance, Coinbase or other CEXs.

On 2), user behavior off-chain becomes increasingly difficult to model relative to dynamics that are visible on-chain and should be thought of as an exogenous shock. For example, an ETF issuer that is determined to stake 1m ETH could one day flick a switch and transform the staking landscape in 12s. Indexing on practice seen in European staking ETFs, most issuers opt for 1-3 staking providers. This is the basis for our assessment that, should institutional staking flow along similar lines and opt for less economically attractive but more convenient alternatives (as a result of cross-selling by a custodian), a large majority of net new stake will likely come at the expense of Ethereum’s decentralization.

On 3) Regarding quantities, it may seem like an exaggeration but we are trying to isolate the impact of a large shock. Whether this shock is likely to actually occur is another question we do not have a model on, but early indications from the launch of US-based ETH ETFs suggest that the ETF market in the largest capital market in the world will emerge as quite concentrated in their composition at the very least.

[Source](https://dune.com/queries/3941916/6630442)

[![unnamed-6](https://ethresear.ch/uploads/default/optimized/3X/8/7/874047bf78ef2d796020cbbce3791e47d0c1796c_2_690x322.png)unnamed-61219×570 20.8 KB](https://ethresear.ch/uploads/default/874047bf78ef2d796020cbbce3791e47d0c1796c)

### Re 4: Our framing of issuance cost is reductive and only focuses on taxes

You are completely correct here. Stakers do have additional costs beyond taxes, and if there is less stake there are less costs that Ethereum pays for its security.

To eyeball the cost reduction as a welfare gain (the integral area under the chart), if the average yield between two equilibriums is 0.027, we obtain ~0.027*17mil = 450k ETH < $2bn. For ETH holders, this would represent 450k/(120m-50m) or 0.65% in welfare improvement from lower dilution ($20 in savings per ETH per year). In our view, this is quite a small welfare improvement relative to the corresponding loss in security.

Conversely, using the MVS lens, a relatively minor cost in welfare loss that is more than substantiated by its corresponding increase in security.

[![unnamed-7](https://ethresear.ch/uploads/default/optimized/3X/a/8/a89dd3a4fa6c9316837a44179f00cfaef367758d_2_690x416.jpeg)unnamed-71600×966 177 KB](https://ethresear.ch/uploads/default/a89dd3a4fa6c9316837a44179f00cfaef367758d)

### Re 5: The social layer exerts its influence beyond the staking layer

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> However, what is normally meant by the “final defense” is that the social layer can convene to act one layer above the consensus mechanism, in the event of, for example, a 51% attack.

This is the key consideration that we believe that the Ethereum community needs to spend more time on. Namely, do we want to fully lean into our final defense as the “punishment in the future” (social slashing) – in which case we agree to potentially have 34% and 51% staked ETH concentration; OR do we want to be more proactive, and make deliberate “preventive” measures in order for such stake concentration to not occur – in which case the diversity of the validator set is of utmost importance.

### Re 6: Allowing incumbent LSTs to dominate could lead to centralization

This is probably where our perspectives diverge the most, but in general we agree that the point is rather under-analyzed.

We fully understand and frankly agree with the perspective that for Ethereum to remain a viable platform for applications and development, Ether itself needs to retain a strong degree of moneyness and value as an asset in itself. Where we likely diverge is in our understanding of what that entails and how issuance policy changes could affect it.

We don’t see LSTs and Ether ‘competing’ for moneyness to the same degree or for the same users. Ether’s “moneyness” is far less likely to depend on the emergence of LSTs on the staking layer, than on the roadmap of Ethereum itself - i.e. whether Ethereum continues along a path of being a settlement layer or if it diverges from that vision with the goal to attract more end-users. Furthermore, Ether will always be necessary to some degree as a basic commodity for using Ethereum in the first place. User preferences are also not entirely driven by yield. Despite the objective ‘dilution’ that ETH holders face with respect to issuance whenever it is net positive, ETH holders and users will evaluate the risks of staking as greater than the dilutive effect of staking. This correspondingly reflects in the use of Ether both on-chain and off-chain, where Ether’s basic ‘moneyness’ is not in question. Finally, though it may sound trite, LSTs cannot function without Ether anyway. In summary, Ethereum’s “moneyness” is more likely determined by its roadmap than by its applications, nobody is forced to move into staking today as it is, nor is Ether’s moneyness in question as a result.

In our worldview, it will be very difficult to optimize for a staking layer that does not have some degree of network effects. With the scale that Ethereum has reached today, it may be impossible to achieve an ‘ideal staking economy’ without triggering unintended downstream effects. These could range from a disruption of DeFi economic activity to a rapid centralization of Ethereum validation from net new stake.

If we believe that network effects in staking cannot be prevented, in our view it feels natural to conclude that staking should be democratized and decentralized. LSTs, such as Lido or Rocket Pool, that are aligned with that, are a very practical implementation. It’s not so much a choice of whether staking influences Ethereum governance, we view it more as a choice to whether the power blocks will form in Govspace TradFi or in Ethereum DeFi. To keep a maximally viable security level for Ethereum, we believe the latter is preferable.

---

**aelowsson** (2024-07-30):

Thanks I appreciate the steelmanning of arguments, which is fairly in line with my thinking/writing, and the division into six distinct topics. I will respond to your counterarguments on these topics one by one.

### 1. Solo-staker modeling overstates yield advantage

#### Correct median calculation

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> We remain more comfortable using the empirically observed median to express the base case for solo and small stakers. This is because of the extreme positive skew of rewards for those participants (particularly proposer and EL rewards), such that averages can be misleading. Some will luck out and win frequent proposer blocks or attractive MEV, while the majority will not.

This is an important topic that we shall now go over carefully. The expected yield is the most relevant measure to solo stakers and delegating stakers alike. This is the preferred measure, coupled with a measure of variability over a time frame of one or a few years. A prospective solo staker might also want to know what the median outcome (or any other order statistics) would be over some given time period, perhaps a year or two, or until their hardware investments have reached their depreciation horizon. Order statistics can thus be relevant on a per-validator basis over longer time.

Computing the median across all validators over some minuscule time period, and then averaging these medians over time, fails to capture the probabilistic outcome facing the staker. It is obfuscated by a skewed daily distribution combined with the law of large numbers. Half of the validators will never propose a block during the same day, yet half will still propose within a few months. The signal is destroyed by computing the order statistic (median) at the wrong point across the wrong dimension.

*To check if it is raining, do not extend your hand and measure the median number of fingers impacted by raindrops every millisecond. The result will always be zero; yet it might still rain.*

#### Modeling current conditions

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> The actual rewards earned by validators have been much lower than the figures shown in your simulated results. According to Rated, the APR earned across the entire active validator set (also known as the “realized rewards reference rate”) has an all-time median of 2.41% and mean of 3.43%. Your model appears to overestimate on both.. ..we suspect the main cause lies in the difference between theoretical projections and real-world outcomes.

The figure showed the distribution of yields over a year in accordance with 29M ETH staked and MEV revenue of 2023 (around 300k ETH per year). This was the relevant data at the time of publication in January 2024. The previously linked [specification](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-41-model-13) further stipulates that it captures ideal attestation performance with an approximately similar level of missed sync-committee attestations and block proposals as today. The purpose of showing the figure in my last response was to highlight the technical error in the median calculation. I made no references to exact yield figures because it is not relevant to the question of the correct mathematical process and the shape of the resulting yield distribution.

Thus, the major discrepancy is not theoretical projections relative to real-world outcomes (it was accurate at that specific time point), but how the median is calculated. This is easy to confirm by computing idealized performance at the *current* D = 33.45M ETH but to *exclude* proposal and sync-committee revenue

\frac{54}{64}\frac{cF}{\sqrt{D}}=0.02426.

The result corresponds to the outcome when calculating the median at the wrong point across the wrong dimension (counting the median number of fingers hit by a raindrop every millisecond to determine if it is raining). The marginal difference here between 2.41% (or 2.39%) and 2.426% is mainly attributable to a lower-than-ideal attestation performance.

The benefit of using a simulation is that it becomes possible to analyze how the outcome will change with D and the level of MEV. The associated post leveraged this to show the outcome at for example 50M and 70M ETH staked in [Figures 16-18](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448#h-44-variability-with-fixed-demand-and-varied-supply-16). As evident from those plots, the yield falls when D rises.

The simulation can also be adapted to the current circumstances with D = 33.45M. We could even lower the MEV level to 200k ETH per year as implied by Rated, eventhough this is a bit problematic: Rated seems to define their “all-time” measure to be the last 90 days, making that MEV estimate susceptible to short-term trends (not clear if this was understood in your response). In any case, by reducing the average block MEV in the data used in my previous post so that the yearly figure falls from around 300k ETH to around 200k ETH (linear normalization), these new assumptions can be modeled. For good measure, attestations are set to capture 99% of maximum rewards across the board, bringing the baseline down from 2.426% to 2.402%. The outcome for stakers over one year is shown in the figure.

[![Figure 1](https://ethresear.ch/uploads/default/optimized/3X/1/4/1491d20e10687a6f10bba1cdcc7d0bdff5f32250_2_690x388.png)Figure 11920×1080 352 KB](https://ethresear.ch/uploads/default/1491d20e10687a6f10bba1cdcc7d0bdff5f32250)

I highlight again the tiny vertical line segment of the black line (at 2.402%). This is the small fraction of solo stakers that your analysis is based on. But as evident, the median for solo stakers will over a year already be above 3%. I repeat again that after 2-3 years, there will hardly be any unlucky solo stakers left at the lowest level. This is evident by observing the blue 64-ETH distribution (two years of non-pooled staking for a 32-ETH validator) and the 160-ETH distribution (five years of non-pooled staking).

Concerning the linked report, it seems to rather indicate that solo stakers capture around 97.8% of the average rewards (4.31% relative to 4.41%). This would be unfortunate, but the staking commission would still be a much larger part of rewards. There is then some noisy subgroup data that seems perilous to draw conclusions from. Thus, regardless of whether solo stakers bring in an expected yield of 3.44% or 3.36% currently, they certainly do not bring in a yield of 2.4%, and the median of the distribution will approach the mean with time.

*In conclusion, going forward, we must make sure to not rely on an erroneous median for modeling purposes and to not confuse the argument by invoking misapplied empiricism.*

### 2. Node operators raising commissions could be beneficial to solo stakers

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> ..varying sensitivity among staker profiles means that increased commissions by large node operators, in response to lower issuance, may not automatically benefit solo stakers and smaller node operators.

My contention was that if a reduced APR leads to node operators raising their commission, then the relative difference in revenue between solo stakers and delegating stakers will increase. I then noted that

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> From the perspective of retaining a higher proportion of solo stakers, this could be considered as beneficial.

Thus, while all stakers could lose from lower issuance (this is however not certain, it is a separate topic discussed [here](https://ethresear.ch/t/faq-ethereum-issuance-reduction/19675#can-stakers-profit-from-a-reduced-issuance-and-what-is-the-relevance-and-impact-of-the-realproportional-yield-37)), the benefit discussed was at the protocol level. If node operators greatly raise their commission, then this produces an economic pressure pushing the *proportion* of solo stakers higher. The point is that we cannot ignore the take-home of delegating stakers, because the willingness to delegate stake relative to the willingness to solo stake will also vary with commission rates. So it was an attempt from me to steer the analysis into being more complete by also accounting for this effect.

### 3. CEX dominance is in decline today and we do not provide a model to support the idea that large inflows of new stake would accrue to them

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> Tldr: We don’t have an accurate model, but try to think of the impact of an exogenous shock of large amounts of net new stake through inelastic channels (ETFs in particular), which we believe to be more than a realistic possibility..

My overarching point would be that as Ethereum scales and the technology improves, the value of operating onchain should increase. The trend would then continue, which seems like a reasonable default assumption.

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> ..every CEX is a private business run for the benefit of its shareholders alone. This is generally a good thing and we should avoid the temptation to take a moralistic view with any choices that companies make, instead think only of incentives and model accordingly.
>
>
> To witness how, for a private company, pressure to compete more dynamically in the staking market wins over pressure to offer more transparency to the community, we can look to CEX disclosures of ETH staked. For example, even Coinbase, which has been a hugely positive force for our industry, has been able to completely stop reporting information about how much ETH it stakes on behalf of customers without much pushback.

Most, if not all, SSPs operate with the purpose of deriving profits; CEXes are not materially different in this regard. A CEX might be able to lean into its stronger regulatory oversight to attract stake without making full disclosures, whereas some entity operating under less regulatory scrutiny instead could seek to provide assurances through onchain transparency or leveraging known operator identities in other ways.

We have seen how opaque setups have failed in the past, so full disclosures certainly make for a more attractive service provider. However, being opaque at lower stake participation is more of a threat to beneficial owners than to Ethereum. If Coinbase were to seemingly approach critical thresholds of stake participation (say 25% or 33%) and not be forthright about its stake under management, there would be mounting pressure from the community for greater clarity, and they would make themselves even less attractive. Passing 33% in secret would arguably subject beneficial owners to high risks. The social layer has a wide range of [options available](https://notes.ethereum.org/@djrtwo/risks-of-lsd#Risks-on-Capital-vs-Risks-to-Protocol) that potentially involve loss of funds and/or ejection, say in the event of centralization coupled with contentious forms of consensus participation that could be more benign to Ethereum at lower stake participation.

### 4. Our framing of issuance cost is reductive and only focuses on taxes

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> You are completely correct here. Stakers do have additional costs beyond taxes, and if there is less stake there are less costs that Ethereum pays for its security.
>
>
> To eyeball the cost reduction as a welfare gain (the integral area under the chart), if the average yield between two equilibriums is 0.027, we obtain ~0.027*17mil = 450k ETH
>
> Conversely, using the MVS lens, a relatively minor cost in welfare loss that is more than substantiated by its corresponding increase in security.

Thanks. Yes, that integral bounded by the two equilibria [has been computed](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171#h-21-user-utility-9) to Y'_c = \int_{D_2}^{D_1} f(x)dx\approx 446k ETH (though the supply curve is very hypothetical). The welfare gain is applicable to the entire circulating supply and must be spread out across it:

w=\frac{Y'_c}{S}\approx0.0037,

i.e., 0.37%. The welfare gain corresponds to around 1.5 billion dollars per year, which is no small sum by itself. Yet, it is important to note that this is not a fixed one-time gain. The cost reduction continues to bring a similar welfare gain year over year, and its value is therefore much higher. Comparing with a tech company valued at a p/e ratio of 30, a 1.5 billion gain in profits increases the value of the underlying asset by 45 billion. While the comparison is not perfect, if we are to attach a value to the cost reduction, that figure is probably closer to the mark.

### 5. The social layer exerts its influence beyond the staking layer

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> This is the key consideration that we believe that the Ethereum community needs to spend more time on. Namely, do we want to fully lean into our final defense as the “punishment in the future” (social slashing) – in which case we agree to potentially have 34% and 51% staked ETH concentration; OR do we want to be more proactive, and make deliberate “preventive” measures in order for such stake concentration to not occur – in which case the diversity of the validator set is of utmost importance.

I do not think that the importance of diversity in the validator set is a point of contention. We both want a diverse validator set. The important point is that if an attack requiring social intervention indeed does happen, then if all ETH is tied up in staking, this would be a very fractious process. It is in this light we must understand my response to the post:

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> Yet, as Ethereum grows, massive new inflows might bypass today’s social layer altogether. If a large bank, say, staked $1tn worth of Ether with a CEX, what chance does a community of open source developers have to enforce social norms?

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) aelowsson:

> People  are the last line of defense. In this regard, a proof-of-stake blockchain run by open source developers is certainly not helpless if a large bank were to degrade the consensus mechanism. There are a range of defensive strategies , whose mere existence would presumably scare off any would-be attacker.

Note here the importance of the last part: *whose mere existence would presumably scare off any would-be attacker*. We both wish to avoid any attack happening, but I contend that if the threat of an independent neutral social layer is removed, the risk of the attack happening in the first place increases (and of course the potential consequences as well). Note also that an “attack” must not be an obvious violation, easy to come to social consensus on. It can involve chipping away at the properties that we wish the consensus mechanisms to uphold (e.g., censorship resistance).

### 6. Allowing incumbent LSTs to dominate could lead to centralization

![](https://ethresear.ch/user_avatar/ethresear.ch/xadcv/48/16969_2.png) xadcv:

> We don’t see LSTs and Ether ‘competing’ for moneyness to the same degree or for the same users. Ether’s “moneyness” is far less likely to depend on the emergence of LSTs on the staking layer, than on the roadmap of Ethereum itself - i.e. whether Ethereum continues along a path of being a settlement layer or if it diverges from that vision with the goal to attract more end-users.

The level of the staking yield will directly influence whether or not non-staked ETH remains attractive to the majority of users. Ethereum’s roadmap can influence many things, but it is not necessarily that influential on the risk-adjusted value of holding an LST relative to holding non-staked ETH. We primarily address this with a deliberate issuance policy. I do not actually subscribe to the notion that all ETH will be staked under the current issuance policy. But I certainly subscribe to the notion that the outcome is determined primarily by issuance policy (including MEV burn).

