---
source: ethresearch
topic_id: 22266
title: "Understanding Based Rollups: PGA Challenges, Total Anarchy, and Potential Solutions Part 2"
author: DavideRezzoli
date: "2025-05-05"
category: Economics
tags: [mev, based-sequencing]
url: https://ethresear.ch/t/understanding-based-rollups-pga-challenges-total-anarchy-and-potential-solutions-part-2/22266
views: 559
likes: 4
posts_count: 2
---

# Understanding Based Rollups: PGA Challenges, Total Anarchy, and Potential Solutions Part 2

Many thanks to [@sui414](https://ethresear.ch/u/sui414), [@linoscope](https://ethresear.ch/u/linoscope), [@Brecht](https://ethresear.ch/u/brecht), [@sui414](https://ethresear.ch/u/sui414), [@pascalst](https://ethresear.ch/u/pascalst), [@cshg](https://ethresear.ch/u/cshg), [@dataalways](https://ethresear.ch/u/tripoli/summary) and [@](https://ethresear.ch/u/awmacp/summary)[awmacp](https://ethresear.ch/u/awmacp/summary) for their valuable feedback and comments.

In the [initial part](https://ethresear.ch/t/understanding-based-rollups-pga-challenges-total-anarchy-and-potential-solutions/21320) of this research, we conducted a thorough analysis of Taiko Labs’ operational dynamics within its total anarchy model. We identified and quantified the significant economic losses Taiko Labs faces due to consistently losing the PGAs when attempting to post L2 blocks on L1. This analysis revealed that the competitive proposer landscape, redundant transaction submissions, economic disincentives, inefficient resource allocation, and misaligned incentive structures collectively contribute to Taiko Labs’ financial challenges.

In this research, we formalize the concept of efficiency in Taiko sequencing and other based rollups that adopt a total anarchy approach to block production. We study and summarize the profiles and behaviors of all active sequencers in the Taiko network, analyzing their profitability, strategies, and coordination mechanisms. This includes identifying different sequencing styles, such as off-chain agreements, private mempool usage, and revert protection, as well as quantifying earnings and block contributions over time.

Efficiency, in the context of blockchain and L2 rollups, encompasses several dimensions that collectively determine how well resources are allocated and utilized within the system. Economic efficiency relates to minimizing the cost of block production while maximizing transaction fee revenue, ensuring that the network operates in a cost-effective manner. Computational efficiency focuses on reducing redundant computations and wasted resources, particularly those incurred by sequencers that fail to secure block inclusion. Throughput efficiency considers how effectively block space is utilized, prioritizing the inclusion of high value transactions to enhance overall network capacity. Incentive alignment plays a critical role in shaping sequencer behavior, as misaligned incentives can lead to inefficient competition and excessive resource expenditure. Lastly, welfare efficiency examines whether transaction selection benefits not just individual sequencers but the network as a whole, ensuring that high-value transactions are included while unnecessary costs are minimized. These dimensions provide a framework for assessing the effectiveness of Taiko’s sequencing process and highlight the structural inefficiencies introduced by its total anarchy model.

We interchangeably use *proposer* and *sequencer* to refer to the entity submitting the blob transaction to L1. When referring to a proposer from L1, we use *L1 proposer*.

### Efficiency in Taiko

In Taiko’s total anarchy model, Pareto efficiency evaluates whether sequencers maximize system utility without unnecessary trade-offs. A clear example of inefficiency occurs when two sequencers post L2 blocks on L1 containing the same transactions. Both expend significant resources, such as gas fees in PGAs, but only one block gives rewards, leaving the other effort economically wasteful.

This redundancy arises because Taiko operates without centralized coordination, allowing any sequencer to propose blocks in a fully permissionless manner. Given that inclusion on L1 is competitive, multiple sequencers independently attempt to post blocks that maximize their individual rewards. Since all rational sequencers prioritize transactions with the highest tips, they often construct nearly identical blocks, leading to repeated submissions of the same transactions. In Taiko, both blocks are accepted; however, duplicate transactions in the second block are filtered out upon inclusion. As a result, only the first sequencer to successfully publish their block receives rewards, while others still incur gas costs but gain nothing in return.

This results in resource inefficiency, as gas spent by non rewarded sequencers adds no economic value. These resources could be better allocated to include unique transactions or optimize proposals.

### Consider the following scenario:

The Taiko mempool contains x transactions, denoted as T = \{t_1, t_2, \dots, t_x\}, where each transaction t_i is characterized by a tip tip(t_i), representing its economic value. We assume that transaction tips represent the economic utility of inclusion for users. In reality, users may engage in strategic bidding, misestimate their willingness to pay, or face constraints that cause misalignment between tips and true utility. However, for simplicity, we assume that tips directly correspond to user utility.

Without loss of generality, we assume tip(t_1) \geq tip(t_2) \geq \dots \geq tip(t_x), i.e., transactions are ordered by decreasing tip values.

Each sequencer S_j can construct a block B_k, subject to the block gas limit G_{\text{max}}, which restricts the number of transactions in B_k to at most y, such that |B_k| \leq y. The set of transactions selected by sequencer S_j for their block B_k is B_k = \{t_1, t_2, \dots, t_y\}.

Sequencers are rational and prioritize transactions that maximize their utility U(B_k), defined as:

U(B_k) = \sum_{t \in B_k} tip(t) - C(B_k)

where C(B_k) represents the cost incurred by sequencer S_j to propose and prove the block B_k. Rational sequencers independently select the same top y transactions: B_1 = B_2 = \dots = B_n = T_y, where T_y = \{t_1, t_2, \dots, t_y\} represents the set of transactions with the highest tips.

In this case:

1. The accepted block B_w (where $w \in W$the set of winning sequencers) contributes utility to the system:

U_{\text{system}} = \sum_{t \in T_y} tip(t)

1. The empty blocks represent wasted gas and computational effort. The total wasted cost

C_{\text{wasted}} = \sum_{j \neq W} C(B_j)

where W represents the set of sequencers whose blocks are accepted. If only one block is accepted, then W = \{w\}, and the sum applies to all non-winning sequencers.

1. Transactions not included in T_y are excluded, defined as:

T_{\text{remaining}} = T \setminus T_y = \{t_{y+1}, t_{y+2}, \dots, t_x\}

1. The utility loss due to these excluded transactions is:

U_{\text{excluded}} = \sum_{t \in T_{\text{remaining}}} tip(t)

This scenario illustrates Pareto inefficiency. While the accepted block contributes to system utility, the gas costs and efforts of other sequencers add no value. Additionally, if two different sequencers publish for the same L1 data, they consume blob space without generating additional utility. Furthermore, transactions in T_{\text{remaining}}, which could enhance utility, are excluded due to redundant competition. These inefficiencies highlight the need for improved coordination mechanisms to optimize resource allocation within Taiko’s total anarchy model.

Beyond Pareto efficiency, ****welfare efficiency looks at whether transaction selection benefits the network as a whole. In an ideal system, resources would be allocated to maximize overall value while keeping unnecessary costs low. However, in Taiko’s current design, sequencer competition introduces inefficiencies that go beyond individual losses. High-value transactions can be excluded simply because multiple sequencers prioritize the same set of transactions, leading to redundant submissions that waste valuable blob space. This misalignment between individual incentives and broader network welfare suggests that better coordination mechanisms are needed.

### Market Share by Proposer

In the next part, we analyze the proposer market share. We excluded the Taiko Labs proposer, as its role is solely to ensure the liveness of the chain. We can see that Proposer F was the dominant proposer from the start of the analysis until early November. We also observe that there are now five active proposers, with Proposers A and B building most of the blocks. Proposers D and E are also active, each reaching around 10% to 20% of the total blocks.

[![Market Share by Proposer](https://ethresear.ch/uploads/default/optimized/3X/f/4/f40923b9166779bbdd6857b4bebb8ebda7a2564b_2_690x345.png)Market Share by Proposer1200×600 154 KB](https://ethresear.ch/uploads/default/f40923b9166779bbdd6857b4bebb8ebda7a2564b)

### How do sequencer currently operate in the Taiko Ecosystem

In our previous research, we highlighted the earnings of sequencers that outcompete Taiko Labs’ sequencer. In this section, we analyze their behavior.

There are two distinct cases in which the two most profitable sequencers are proposing. We observe that they alternate sequencing periods to avoid interfering with each other while keeping the priority fee unchanged. This behavior is most likely an off-chain agreement between the proposers from the data analyzed we think the active proposers excluding Proposer E and Taiko Labs have an off-chain agreement.

The following plot illustrates the gas prices (priority fees) for the proposing transactions on L1 on December 21st and 22nd. Notably, both sequencers maintain a fixed priority fee over time. Sequencer A (0x41F2F55571f9e8e3Ba511Adc48879Bd67626A2b6) proposed 153 blocks on the 21st and 184 on the 22nd, consistently paying a priority fee gas price of 3.78 Gwei for each proposing transaction. Similarly, Sequencer B (0x66CC9a0EB519E9E1dE68F6cF0aa1AA1EFE3723d5) maintained a fixed gas price of 3.79 Gwei for 155 blocks on the 21st and 166 on the 22nd.

[![December 21-22 Max Priority Fee Gas price](https://ethresear.ch/uploads/default/optimized/3X/a/7/a7536ea2bc6415cd13b7ae80a94458b3c0ca3e3f_2_665x499.jpeg)December 21-22 Max Priority Fee Gas price1280×961 91.9 KB](https://ethresear.ch/uploads/default/a7536ea2bc6415cd13b7ae80a94458b3c0ca3e3f)

In the second case, sequencers submit their transactions, and if they are not accepted within a given time, they increase the priority fee. This behavior is [implemented](https://github.com/taikoxyz/simple-taiko-node/blob/2fa21d1c0cfe1c49416d6f7fc7f086c459c86cc4/.env.sample#L102) in the standard Taiko sequencer, which is based on the Optimism sequencer’s code implementation.

When a block is profitable, sequencers send a blob transaction. If the transaction is not accepted, they send another transaction with the same nonce but higher priority fee to improve inclusion chances.

The logic for bumping transactions is already present in the [Taiko codebase](https://github.com/taikoxyz/optimism/blob/1b90c0522ace1939b54d1d9404a8ef2de5edfa5c/op-service/txmgr/txmgr.go). We do not believe that sequencers actively monitor the mempool before bumping their transactions.

In the following plot, we show a day where the three main sequencers are actively proposing blocks. From 00:00 to 10:00, it is visible how the three different proposers increase their priority fees to ensure their blocks are included before their competitors.

### Multiple proposers operating during the same day

The graph below illustrates the activity of four different proposers, Proposer A, Proposer B, Proposer D, Proposer E and Taiko Labs proposer between midnight and 10 AM.

Some proposers submit private blob transactions directly to the builder, while others send their transactions through the public mempool.

A key observation is that Proposers D and E do not utilize the bump function, maintaining a constant priority fee throughout. In contrast, Proposers A and B adjust their strategy: when their transactions are not included, they increase their priority fee in an attempt to secure inclusion in the next block.

[![February 4th Max Priority Fee Gas Price by Proposers](https://ethresear.ch/uploads/default/optimized/3X/d/e/de87fa16060152d1d6e1f74534e8150bdfec4d84_2_690x365.png)February 4th Max Priority Fee Gas Price by Proposers1512×800 86.7 KB](https://ethresear.ch/uploads/default/de87fa16060152d1d6e1f74534e8150bdfec4d84)

### Why Public Mempool and Not Simply Revert Protection?

A public mempool introduces uncertainty because it can lead to empty blocks being included on-chain. Losing the Priority Gas Auction (PGA) may result in an unprofitable block getting finalized.

As mentioned in the previous post, a more reliable approach would be revert protection, ensuring that the block being created has an ID that matches the current Taiko head +1. If it doesn’t match, the transaction simply reverts.

Revert protection is [offered](https://docs.flashbots.net/flashbots-protect/overview) by builders, who simulate transactions to verify their validity. If a transaction is invalid, it is discarded at no cost however, not all builders support revert protection, for example Beaver, which constructs more than [40% of blocks](https://relayscan.io/overview?t=7d), does not offer it. While this mechanism is not currently enforceable on-chain, efforts are underway to enable it, for example, [EIP-7640: Transaction Revert Protection](https://ethereum-magicians.org/t/eip-7640-transaction-revert-protection/19000) by Joseph Poon.

### Profitability of Each Proposer per Block

In the next graph, we show the profitability of each block starting from February 4th. We also include the Taiko proposer to indicate whether a block was profitable or not. The data shows that all proposers generally build profitable blocks. However, when two blocks compete for the same slot, they may produce unprofitable blocks, except for Taiko proposers, who consistently build unprofitable blocks.

[![February 4th Profitability of Blocks by Proposers](https://ethresear.ch/uploads/default/optimized/3X/c/4/c48fe7a8e79427332a66d58b1b6e80d297299ab0_2_690x365.png)February 4th Profitability of Blocks by Proposers1512×800 93.1 KB](https://ethresear.ch/uploads/default/c48fe7a8e79427332a66d58b1b6e80d297299ab0)

### Proposer Earnings per Block

In the next graph, we observe the earnings for each block. Notably, Proposer E does not produce any unprofitable blocks, while other proposers mostly generate profitable blocks, with only a few instances of unprofitable ones.

We also observe that Taiko predominantly builds unprofitable blocks, an issue that could be easily avoided by sending their blob privately and using revert protection.

One challenge is that [Beaver](https://beaverbuild.org/) occasionally builds multiple blocks on the L1, which could cause the Taiko chain to halt since they do not accept blobs privately. However, this issue can be easily mitigated: if a Taiko proposer notices they haven’t built a block within a certain timeframe, they could simply force the transaction into the L1 mempool.

[![February 4th Profitability of Blocks by Proposers](https://ethresear.ch/uploads/default/optimized/3X/d/1/d19c22036f0ebeaba7859679d6f2d2e1d36b52c5_2_690x365.png)February 4th Profitability of Blocks by Proposers1512×800 160 KB](https://ethresear.ch/uploads/default/d19c22036f0ebeaba7859679d6f2d2e1d36b52c5)

## Analysis of Proposer Rewards, Costs, and Profitability

The table below presents data on sequencer earnings and behaviors, focusing on whether they post blobs to the mempool and use revert protection. The analysis includes only those who have published more than 5,000 blocks, covering the period from Genesis to Block 915,000 (May 25, 2024 – March 1, 2025).

This extends the dataset from Part 1 of our research, offering a broader view of proposer strategies and outcomes over a longer time frame.

The [net profit](https://docs.taiko.xyz/taiko-alethia-protocol/economics) is calculated as:

\text {NetProfit = Reward + 75%} \times \text {BaseFee - ProposingCost - ProvingCost}

| Name | Earnings | Proposed Block Shares (%) | Style of Proposing | Positive-Earning-Block Shares (%) | Revert Protection |
| --- | --- | --- | --- | --- | --- |
| Proposer A | 106.1 ETH | 5.65% | Off-chain Agreement | 95.74% | No |
| Proposer B | 93.8 ETH | 5.03% | Off-chain Agreement | 92.80% | No |
| Proposer C | 27.3 ETH | 1.80% | Off-chain Agreement | 79.83% | No |
| Proposer D | 25.3 ETH | 1.60% | Off-chain Agreement | 84.25% | No |
| Proposer E | 10.3 ETH | 0.69% | No Agreement | 99.80% | Yes (Flashbots Protect) |
| Taiko Labs Proposer | -2061.8 ETH | 78.88% | Off-chain Agreement | 14.50% | No |

Among the six active proposers, Taiko Labs stands out with a significant net loss of 1,891.9 ETH. This outcome likely reflects a strategic choice to prioritize liveness and block inclusion even when profitability is low. In contrast, Proposer A leads in profitability with 87.1 ETH earned. Most participants rely on off-chain coordination and public mempool access, which exposes them to competition and potential inefficiencies. Proposer E is the only one using revert protection and a private flow, likely aiming to minimize failed transactions and optimize for consistent returns.

### Average Profit Per Proposer

In the graph below, we show the average daily profit per proposer over the period from November 1st to February 25th. Proposers A, B, and D were active from the start, while Proposer E joined on January 5th. We can observe that Proposer E became the most profitable proposer for a period, even though they were building significantly fewer blocks compared to the others. This is likely due to faster block construction, as Proposer E does not build on Beaver but instead uses Beaver Builder.

[![AvgProfit](https://ethresear.ch/uploads/default/optimized/3X/2/1/21b5c10aa2b213ccae805c632c4b74c6980ea3e8_2_690x414.png)AvgProfit1512×909 133 KB](https://ethresear.ch/uploads/default/21b5c10aa2b213ccae805c632c4b74c6980ea3e8)

### Preconfirmations as a Coordination Mechanism in L2 Rollups

Preconfirmations (preconfs) introduce a structured approach to L2 sequencing, reducing redundant computation, lowering gas costs, and mitigating Priority Gas Auctions (PGA) and frontrunning risks. By allowing a designated preconfirmer to commit to transaction inclusion before finalization, preconfirmations create predictability in execution while preventing inefficiencies caused by uncoordinated sequencing.

In this model, L2 users submit transactions to a preconfirmer, who aggregates them and submits the batch as a Type-3 blob transaction (EIP-4844). This mechanism provides inclusion guarantees, minimizing reordering risks and transaction delays.

### Challenges and Centralization Risks

Despite their benefits, preconfirmations introduce centralization risks, particularly if a small number of proposers dominate L2 block production. Suppose the first available preconfirmer in the lookahead is in the 30th slot. In that case, they effectively control transaction ordering across multiple blocks, enabling multi-block MEV extraction. This could lead to:

- Exclusive MEV strategies: Preconfirmer could reorder transactions across multiple slots to optimize arbitrage, sandwiching, or liquidation timing.
- Reduced sequencing diversity: Large validators or staking pools could consistently preconfirm blocks, sidelining smaller participants.
- Higher capital barriers: Collateral requirements for preconfirmers may exclude solo stakers, reinforcing centralization.
- Liveness risk: A preconfirmer controlling many slots could halt the chain.

These risks and potential mitigations will be explored in a future post.

### Pricing and Economic Trade-offs

Preconfirming transactions means [forfeiting potential MEV revenue](https://research.lido.fi/t/estimating-the-revenue-from-independent-sub-slot-auction-preconfirmations/8801), making pricing a key research question. Proposers need sufficient incentives to commit to transaction order ahead of time. Possible models include:

- User-paid preconfirmation fees to compensate for lost MEV.
- Preconfirmation slot auctions, allowing multiple parties to bid for sequencing rights.
- Dynamic pricing mechanisms, adjusting based on network demand and proposer competition.

Ongoing discussions in the research community ([CTra1n,](https://collective.flashbots.net/t/value-capturing-based-rollups-with-based-preconfirmations/2884) [Charlie Noyes](https://x.com/_charlienoyes/status/1887589138116788242),[Alex Nezlobin](https://x.com/0x94305/status/1802806221059268657)) explore optimal fee structures for preconfirmation markets.

### Conclusion

Taiko’s total anarchy model presents fundamental inefficiencies in proposer competition, leading to redundant transaction submissions, wasted gas costs, and systemic exclusion of valid transactions. The alternating behavior of top sequencers, coupled with priority fee stabilization, suggests a move toward implicit coordination, if not explicit agreements.

Preconfirmations offer a potential path forward, but they come with risks of centralization and MEV monopolization. Future developments in execution ticket markets and alternative proposer coordination mechanisms will be critical in determining the long-term sustainability of based rollups like Taiko.

Further research should focus on pricing models for preconfs, evaluating alternative auction designs, and formalizing economic trade-offs to ensure a decentralized and efficient block-building ecosystem.

## Replies

**jvranek** (2025-05-06):

Thanks for the post! I think the concerns about preconfs are worth discussing but the framing here oversimplifies / misses some nuances (and it’s important to note that many equally apply to centralized sequencers) - also here’s a curated list of some preconf research ([Awesome Based Preconfirmations | Fabric Docs](https://eth-fabric.github.io/website/education/awesome-based-preconfs))!

> “Suppose the first available preconfirmer in the lookahead is in the 30th slot…”

This is valid but assumes low adoption of preconfers.

> “Preconfirmer could reorder transactions across multiple slots to optimize arbitrage, sandwiching, or liquidation timing.”

Execution preconfs are designed so that transactions are bound to a specific output state and cannot be reordered without slashing.

> “Large validators or staking pools could consistently preconfirm blocks, sidelining smaller participants.”

While larger operators will naturally have more opportunities, the mechanism is permissionless. This is no different than how block proposing works today, the existence of staking pools doesn’t preclude solo stakers from proposing L1 blocks.

> “Collateral requirements for preconfirmers may exclude solo stakers, reinforcing centralization.”

Most preconfirmation designs only require minimal collateral (rough conensus around 1 ETH) and is compatible with collateral reuse (e.g., via restaking protocols) to further reduces the barrier to entry. Supporting solo stakers has been a top priority in protocol design!

> “A preconfirmer controlling many slots could halt the chain.”

Classical rollups already delay posting to L1 for gas costs without halting the chain. Preconfers who attempt to censor would be forgoing revenue, and forced inclusion mechanisms remain as a backstop.

