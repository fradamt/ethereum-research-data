---
source: ethresearch
topic_id: 21320
title: "Understanding Based Rollups: PGA Challenges, Total Anarchy, and Potential Solutions"
author: DavideRezzoli
date: "2024-12-23"
category: Economics
tags: [mev, based-sequencing]
url: https://ethresear.ch/t/understanding-based-rollups-pga-challenges-total-anarchy-and-potential-solutions/21320
views: 1656
likes: 18
posts_count: 7
---

# Understanding Based Rollups: PGA Challenges, Total Anarchy, and Potential Solutions

Many thanks to [@linoscope](/u/linoscope), [@donnoh](/u/donnoh), [@Brecht](/u/brecht), [@sui414](/u/sui414), [@pascalst](/u/pascalst),and [@cshg](/u/cshg) for their valuable feedback and comments.

### How to Lose $200K every Two Weeks

tl;dr In this post, we analyze the economics of based rollups using [total anarchy](https://vitalik.eth.limo/general/2021/01/05/rollup.html) as a method of sequencing blocks. Focusing on the only live based rollup, Taiko, we highlight the inefficiencies of total anarchy. Specifically, we identify a critical inefficiency in L2 block building that resembles a priority gas auction (PGA), where competing proposers rush to include transactions before Taiko Labs’ proposer. This results in L2 blocks with redundant transactions being posted on-chain on L1, reducing the value of Taiko’s blocks and increasing its economic costs. As a result, Taiko Labs often incurs expenses to prove blocks with few or no profitable transactions.

Through a two-week analysis of block data, we observe that the market is dominated by four major proposers (including Taiko Labs). Our findings indicate that Taiko Labs faces significant losses due to consistently losing the PGA. Over this period, Taiko Labs lost approximately 83.9 ETH, which, at an average Ethereum price of $3,112, translates to a total loss of roughly $261,096 in just two weeks. This underscores the urgent need for better proposer incentives and mechanisms to mitigate these inefficiencies.

## Introduction

[Based rollups](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016) aim to enhance Ethereum scalability by integrating L2 operations with L1 for improved data availability and security. They leverage L1 for sequencing and settlement, avoiding the need for centralized sequencers, which promotes decentralization.

However, the total anarchy model used for sequencing in Taiko introduces significant inefficiencies. In this model, where block posting lacks hierarchy or coordination, any user can act as an L2 proposer and post blocks without restriction, promoting maximum permissionless participation. While this approach aligns with decentralization principles, it also introduces systemic challenges.

Vitalik described total anarchy as:

> “Total anarchy: anyone can submit a batch at any time. This is the simplest approach, but it has some important drawbacks. Particularly, there is a risk that multiple participants will generate and attempt to submit batches in parallel, and only one of those batches can be successfully included. This leads to a large amount of wasted effort in generating proofs and/or wasted gas in publishing batches to chain.”

These drawbacks materialize in Taiko, where multiple L2 blocks are submitted for the same L1 slot, resulting in redundant transactions. Redundant blocks consume valuable L1 space, inflate fees, and diminish economic efficiency.

## Inefficiency Caused by Redundant Transactions

In rollups using total anarchy, redundant transactions occur when multiple L2 blocks containing the same transactions are published to L1. These blocks may be submitted within the same L1 slot or across different slots. In such cases, both blocks are submitted to L1, consuming valuable blob space and incurring L1 fees for the L2 proposer. The first block processed on L1 is executed to determine the updated L2 state. Any redundant transactions in the second block, already included in the first, are invalidated, as their state transitions have already been applied. Unique transactions in the second block remain valid and still affect the L2 state.

The proposer of the second block faces significant economic inefficiencies. They incur the full cost of posting and proving the block but only earn rewards for valid, non-redundant transactions. This dynamic discourages proposers from submitting redundant blocks. Additionally, posting two blocks to the same L1 slot reduces the effective throughput of the network by occupying valuable block space with redundant data blobs, increasing congestion and costs.

## Taiko’s Architecture and the Economics of redundant Blocks

Taiko exemplifies a based rollup using total anarchy as its sequencing design, prioritizing simplicity and decentralization. In this model, anyone can collect transactions from the L2 mempool, build a bundle (which becomes the L2 block when proposed by the L1 proposer), and submit it to L1 alongside data blobs containing transaction payloads. These blocks may include transactions or remain empty (containing only a single [anchor transaction](https://github.com/taikoxyz/taiko-mono/blob/73944585586686ad1ce5548ce59e9ea583c4b2ee/packages/protocol/docs/how_taiko_proves_blocks.md)) to ensure chain continuity during low-demand periods. After block submission, proposers must generate and post a [validity proof](https://docs.taiko.xyz/core-concepts/multi-proofs/) to confirm the block’s correctness, which incurs additional L1 transaction costs.

[![Simplified Overview of Taiko Architecture](https://ethresear.ch/uploads/default/optimized/3X/9/7/974d90ba9f6cfa9aa8610ffbbda26f098bb69ec4_2_597x500.png)Simplified Overview of Taiko Architecture799×669 38.2 KB](https://ethresear.ch/uploads/default/974d90ba9f6cfa9aa8610ffbbda26f098bb69ec4)

Even empty blocks must be proven to maintain the chain’s liveness and avoid slashing penalties. This requirement places a significant economic burden on fallback proposers like Taiko Labs during periods of low activity. When Taiko Labs includes profitable transactions, higher-bidding competitors often outpace it in the PGA environment, resulting in diminished rewards and economic challenges.

## Priority Gas Auction Dynamics in Taiko

PGAs presents a recurring challenge in Taiko Labs’ operation. Competing searchers exploit Taiko Labs’ open block submission process by outbidding its proposer, using higher fees to ensure their block is executed first. Driven by economic incentives, these proposers monitor pending blocks and submit their own for the same L1 slot, offering higher transaction fees to secure inclusion.

When multiple blocks overlap in content, the first valid block determines the network’s state. Redundant transactions between Taiko Labs’ block and an earlier block are excluded, forcing Taiko Labs to bear the cost of proposing and proving blocks without proportional rewards. This creates a situation where Taiko Labs incurs the full cost of sequencing blocks but receives minimal or no profit, further straining the network’s economic sustainability.

These inefficiencies are especially pronounced during high-demand periods, when the PGA environment is most competitive. However, during low-demand periods, the Taiko Labs proposer is forced to maintain liveness by posting and proving blocks that may contain some transactions but are not full. While these blocks may offer some rewards, in most cases they cannot cover the L1 costs, making them unprofitable. As a result, PGAs not only redirect rewards to more sophisticated proposers but also undermine the incentives necessary to maintain the network’s liveness, placing a disproportionate economic burden on fallback proposers like Taiko Labs.

---

## Analysis

### Methodology

For this analysis, we evaluate proposer profitability by comparing their earnings with the costs incurred. The block rewards from L2 blocks represent the earnings, while the L1 publication costs and proving costs are considered the losses. For Taiko Labs proposer, the base fee associated with each block is included in its earnings.

1. Taiko Proposer Net Profit:
\text{(L2 Priority Fees + Base Fee)−(L1 Publication Costs + Proving Costs)}
2. Other Proposers Net Profit:
\text{L2 Priority Fees − (L1 Publication Costs + Proving Costs)}

The analysis is based on blocks created between November 7, 2024, and November 22, 2024, covering Block IDs 538304 to 593793. This represents 9.34% of all blocks on the Taiko chain since genesis at the time of writing. This dataset provides insights into the economic performance of proposers who processed more than 500 blocks during this period.

## Analysis of Proposer Rewards, Costs, and Profitability

The graph below presents an overview of rewards, costs, and profits for major proposers, highlighting the economic dynamics within the system. Taiko Labs, as the primary fallback proposer, is used as the baseline for evaluating profitability.

[![Proposer Profit Breakdown](https://ethresear.ch/uploads/default/optimized/3X/7/b/7bc9a1c1eb53c6ecdf340c2cc4aba7c3013f8ce3_2_690x339.png)Proposer Profit Breakdown5952×2927 321 KB](https://ethresear.ch/uploads/default/7bc9a1c1eb53c6ecdf340c2cc4aba7c3013f8ce3)

### Key Observations

1. Taiko Labs’ Proposer (0x000000633b68f5D8D3a86593ebB815b4663BCBe0)

Net Profit: -83.9 ETH (approximately $261,096 at $3,112/ETH).
2. Taiko Labs frequently incurs economic losses due to its fallback role in maintaining liveness and being outbid in the PGA environment by competitors, most notably Proposer A (0x41F2F55571f9e8e3Ba511Adc48879Bd67626A2b6) and Proposer B (0x66CC9a0EB519E9E1dE68F6cF0aa1AA1EFE3723d5). By offering higher fees and securing earlier blocks, these proposers reduce Taiko Labs’ ability to capture profitable transactions. The result is often blocks filled with only an anchor transaction, leaving Taiko Labs to incur the proving costs without receiving commensurate rewards.
3. Most Profitable Proposer A (0x41F2F55571f9e8e3Ba511Adc48879Bd67626A2b6)

Net Profit: 26.0 ETH (approximately $80,912 at $3,112/ETH).
4. This proposer routinely outbids the Taiko Labs proposer, capturing the majority of profitable transactions by winning the PGA race and extracting more value.
5. Second most profitable Proposer B (0x66CC9a0EB519E9E1dE68F6cF0aa1AA1EFE3723d5)

Net Profit: 17.5 ETH (approximately $54,460 at $3,112/ETH).
6. This proposer also strategically outbids Taiko Labs, securing profitable transactions and achieving substantial net gains. While slightly less profitable than Proposer A, Proposer B still efficiently balances rewards and costs.
7. Third most profitable proposer C (0x9a5Cc6E3A3325CDc19fC76926CC9666c80139C09)

Net Profit: 6.6 ETH (approximately $20.540 at $3,112/ETH).
8. Although Proposer C posts a similar number of blocks as Proposer B, it earns only about half the profit. This discrepancy likely arises from less sophisticated bidding strategies, reducing overall profitability.
9. Small-Scale Proposers

Smaller-scale proposers exhibit lower overall activity. However, they often manage to remain profitable or near break even due to proportionally lower costs, benefiting from a more cautious approach within the PGA landscape.

## Taiko Labs Proposer Outbid by Other Proposers

In this section, we analyzed instances where the two top-earning proposers outbid Taiko Labs. This happens when a proposer submits a block faster than Taiko Labs and secures its execution on L1 first.

[![Taiko Labs' outbid by Proposer A](https://ethresear.ch/uploads/default/optimized/3X/5/0/50a742b5560fab5e602e388d92cb56deeb2c9503_2_690x379.jpeg)Taiko Labs' outbid by Proposer A1920×1055 138 KB](https://ethresear.ch/uploads/default/50a742b5560fab5e602e388d92cb56deeb2c9503)

This graph illustrates each instance where Proposer A outpaced the Taiko proposer in posting a block.

- Y-Axis: Represents the reward associated with each block (sum of L2 transaction fees).
- X-Axis: Represents the size of the posted block.
- Timeframe: Over the two-week period analyzed, this occurred 4,621 times.

In our analysis, we examined instances where blocks proposed by Proposer A were immediately followed by blocks proposed by Taiko Labs’ proposer.

### Profitability Comparison:

- Proposer A:

In blue on the graph, we observe all 4,285 profitable blocks proposed (92.7% profitability), while the not profitable blocks are shown in ligthblue.

**Taiko Proposer**:

- In red, the graph shows that the Taiko Labs proposer achieved only 103 profitable blocks (2.2% profitability with 4,518 blocks resulting in 97.8% of blocks being unprofitable), with the not profitable blocks shown in pink.

**Economic Impact on Taiko**:

- The total loss incurred by the Taiko Labs proposer, as a result of consistently being outbid by Proposer A, amounted to 18.37 ETH.

[![Taiko Labs' outbid by Proposer B](https://ethresear.ch/uploads/default/optimized/3X/5/0/501b07200c8900a91698255208b55d19c17cfe5b_2_690x382.jpeg)Taiko Labs' outbid by Proposer B1920×1064 139 KB](https://ethresear.ch/uploads/default/501b07200c8900a91698255208b55d19c17cfe5b)

Similarly, we analyzed cases where blocks proposed by Proposer B preceded those proposed by the Taiko Labs proposer. This occurred 4,870 times during the observation period.

### Profitability Comparison:

- Proposer B:

Proposed 4,333 profitable blocks (89.0% profitability) in blue, with not profitable blocks shown in lightblue.

**Taiko Proposer**:

- Achieved 132 profitable blocks (2.7% profitability with 4,738 blocks resulting in 97.3% of blocks being unprofitable) in red, with not profitable blocks in pink.

**Economic Impact on Taiko:**

- The total loss incurred by the Taiko Labs proposer in these cases was 18.25 ETH.

## Transaction Distribution Analysis

To further investigate proposer behavior, we analyzed the distribution of transactions per block using a Kernel Density Estimation (KDE) graph. This visualizes how proposers allocate transactions across blocks, highlighting differences in their strategies.

[![Transactions Count KDE](https://ethresear.ch/uploads/default/optimized/3X/c/1/c1f84ba433380ab8db6697db10931ae41ee3cc82_2_690x366.jpeg)Transactions Count KDE1920×1020 103 KB](https://ethresear.ch/uploads/default/c1f84ba433380ab8db6697db10931ae41ee3cc82)

### Key Observations

1. Taiko Labs’ Behavior (0x000000633b68f5D8D3a86593ebB815b4663BCBe0):

Low-Transaction Blocks (1500 Transactions): Around 24.1% of Taiko Labs’ blocks exceed this threshold, showing occasional success in capturing profitable opportunities.
3. Taiko Labs’ fallback role and the penalties from redundant blocks lead to significant economic inefficiencies.
4. Profit-Focused Proposers:

Proposers A and B focus almost exclusively on high-transaction blocks, with over 46–58% of their blocks exceeding 1500 transactions.
5. Both proposers frequently outbid Taiko Labs by submitting blocks with higher transaction fees, diminishing Taiko Labs’ reward opportunities.

## Analysis of Block Profitability by Major Proposers

We continue our analysis by evaluating the number of profitable blocks proposed by each proposer and examining the distribution of these results in Taiko.

[![Proposers profitability (1)](https://ethresear.ch/uploads/default/optimized/3X/3/3/335eb1a96c26e44b06d690a109360dd007713761_2_690x359.png)Proposers profitability (1)4453×2317 266 KB](https://ethresear.ch/uploads/default/335eb1a96c26e44b06d690a109360dd007713761)

This graph illustrates the profitability of blocks published by major proposers (processing more than 500 blocks) during the analyzed period. It categorizes blocks into two groups: profitable blocks (green) and unprofitable blocks (red), highlighting the proportion of each for individual proposers.

### Key Observations

1. Taiko Proposer (0x000000633b68f5D8D3a86593ebB815b4663BCBe0)

Profitable Blocks: 19.1%
2. Unprofitable Blocks: 80.9%
3. The majority of Taiko Labs’ blocks are unprofitable, reflecting its role in maintaining liveness, even if that requires posting unprofitable blocks. This outcome supports the hypothesis that Taiko Labs is consistently outbid in the PGA environment on profitable blocks, leaving it to act as a fallback proposer during periods of lower profitability.
4. Proposer A (0x41F2F55571f9e8e3Ba511Adc48879Bd67626A2b6)

Profitable Blocks: 93.4%
5. Unprofitable Blocks: 6.6%
6. This proposer maintains a highly efficient operation, focusing almost exclusively on profitable blocks, which suggests selective block proposal during high-demand periods.
7. Proposer B (0x66CC9a0EB519E9E1dE68F6cF0aa1AA1EFE3723d5)

Profitable Blocks: 89.8%
8. Unprofitable Blocks: 10.2%
9. Another highly efficient proposer, demonstrating strong profitability, likely by focusing on full blocks.
10. Mixed Strategy Proposer (0x9a5Cc6E3A3325CDc19fC76926CC9666c80139C09)

Profitable Blocks: 69.8%
11. Unprofitable Blocks: 30.2%
12. This proposer might not be as sophisticated as the other proposers, occasionally posting unprofitable blocks.
13. Smaller Proposers (e.g., 0x2802E30d61d5ac0879c4F0c2825201a3D9C250Ef)

Profitable Blocks: 96.8%
14. Unprofitable Blocks: 3.2%
15. This proposer began operations later in the analyzed period, starting at block 580181. Despite its smaller scale, it demonstrates a highly sophisticated strategy, focusing exclusively on profitable opportunities and avoiding unprofitable blocks entirely. This could indicate that it is one of the most advanced actors, strategically entering only when conditions are favorable.

## Insights

This analysis reveals how competing proposers, driven by their own economic interests, create challenges for Taiko Labs. A critical issue arises when Taiko Labs posts blocks on L1 with low-priority fees, enabling more sophisticated actors to outbid them in the PGA environment. Our findings indicate that over 80% of Taiko Labs’ posted blocks were unprofitable, and being outbid occurred in more than half of the blocks proposed by Taiko. This highlights the economic inefficiencies Taiko Labs faces as it strives to maintain network liveness in an environment where competing proposers exploit its fallback role.

---

## Possible Solutions

Using total anarchy for sequencing requires guarantees of execution to prevent redundant transactions. This approach can be challenging because, from the L1 perspective, transactions are executing correctly.

One potential solution is to add the L2 block ID field in the L2 block proposal function, causing the block proposal to revert if the target is missed due to competition from other proposers. While this still incurs a transaction cost for proposing, it avoids the expense of proving the block. Taiko Labs could potentially use revert protection to prevent conflicting blocks from getting on-chain. By doing this, they could avoid wasting transaction fees. However, it’s worth noting that revert protection introduces a trust assumption on the builder. Another problem might be when you have blocks with the same ID that don’t have redundant transactions.

Another possible solution is [execution preconfirmations](https://ethresear.ch/t/based-preconfirmations/17353). However, ensuring execution guarantees on the L2 side adds complexity to the preconfirmation process. Having a single preconfer can provide guarantees that they will not publish conflicting blocks for the same slot, as doing so could result in slashing penalties. This mechanism can significantly reduce redundant submissions and lower L1 fee wastage. However, it also introduces execution complexity, posing challenges that must be addressed to ensure efficient implementation.

The solution that might be the easiest to implement involves the use of execution tickets. [Execution Tickets](https://ethresear.ch/t/execution-tickets/17944), or others leader election mechanisms like based preconfirmation, provide a deterministic system to elect a single block proposer per slot. This approach minimizes conflicts and redundancy by ensuring that only one proposer is responsible for block submission at any given time.

Execution tickets have several advantages. By eliminating redundant block submissions, they reduce wasted resources and align proposer incentives with the system’s overall efficiency. However, implementing such a system introduces challenges to ensure fair and reliable leader election.

---

### Discussion and Conclusion

While total anarchy encourages permissionless participation, it struggles to meet the efficiency demands of based rollups due to redundant blocks and the competitive PGA environment. Taiko serves as a compelling case study, illustrating the economic costs associated with inefficient block space utilization on L1.

Potential solutions such as execution preconfirmations could address these inefficiencies but add system complexity. Alternatively, introducing a leader election mechanism could reduce redundant blocks by adding structure, though it might also introduce centralization risks. A balanced approach could retain permissionless participation while penalizing harmful behavior, aligning decentralization with practical efficiency.

---

### Future Work

1. Profitability Analysis: Investigate whether Taiko Labs has ever been profitable or if competing proposers were consistently capturing the profits instead.
2. Proof Costs: Evaluate the impact of off-chain proof generation costs on net profitability.
3. Proposer Behavior: Study proposer strategies in detail. Initial decoding of a few L1 blobs revealed no instances of proposers directly copying Taiko Labs’ proposer blobs, but further analysis is needed to confirm patterns.

### Acknowledgments

I would like to express my sincere gratitude to [Flashbots](https://www.flashbots.net) for awarding the grant that made this work possible and for supporting my ongoing research on this topic. I also extend my thanks to the [PBS Foundation](https://pbsfoundation.notion.site) for their initial support of this research.

## FAQ:

### How does Taiko Labs post blocks on L1?

Currently, the Taiko proposer operates openly by observing the public L2 mempool and publishing their blocks on the L1 mempool. Since everything is done publicly, outpacing the Taiko Labs sequencer by submitting blocks faster is relatively straightforward, provided you can generate the proof for the blocks you publish or find a prover willing to generate the proof on your behalf.

### Data Collection?

To collect data, we listened to events from the contract responsible for proving and proposing: 0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a. From these events, we extracted the Taiko block ID in which the L1 block was recorded and the L1 transaction hash.

Using the transaction hash, it was straightforward to check the transaction fees associated with each transaction via RPCs. For L2 transaction fees and the L2 base fee, we used the L2 block ID and calculated the results based on the block reward. While this method might not be the fastest, acquiring data for Taiko has proven to be challenging and relatively slow.

In future posts, we aim to find a faster way to collect data for all chains.

### Encrypted Mempool as a Solution?

An encrypted mempool wouldn’t solve the problem, as blocks with redundant transactions would still occur. Over time, this could lead to a monopoly where the most competitive and sophisticated searcher consistently posts blocks faster than others.

### Are Proposer A and Proposer B Outbidding Each Other?

We found only 57 occurrences where these two proposers published blocks in immediate succession, indicating that direct PGA-style competition between them is relatively rare. Proposer A published first in 31 instances, making all of those blocks 100% profitable for Proposer A but only 54.8% profitable for Proposer B. Conversely, Proposer B published before Proposer A in 26 instances, and in those cases, both proposers’ blocks were profitable 80.8% of the time. Further analysis will be conducted for other proposers in a subsequent post.

### How Can I Identify Blocks Impacted by Outbidding?

You can view it by simply checking [TaikoScan](https://taikoscan.io/blocks). Often, when blocks are empty or contain fewer than 100 transactions, it suggests the proposer was outbid in the PGA environment. Even blocks with a higher number of transactions might have been affected; in such cases, comparing the block’s costs to its rewards is the only way to confirm. For a more in-depth analysis, decoding the blob is the most reliable approach.

### Was Taiko Labs ever profitable?

To answer this question definitively, further analysis is needed. However, the intuition suggests that Taiko Labs becomes profitable under specific conditions. For other proposers, profitability occurs when  \text{L2  Priority Fees − (L1 Publication Costs + Proving Costs) > 0}. If this condition is not met, they avoid publishing blocks that would result in a loss.

In contrast, the Taiko Labs proposer earns an additional Base Fee, making its profitability condition:

\text{(L2  Priority Fees + Base Fee) − (L1 Publication Costs + Proving Costs) > 0}

When this condition holds, Taiko Labs is profitable, as the Base Fee offsets the publication and proving costs that would otherwise make the block unprofitable for other proposers.

## Replies

**namayama** (2024-12-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/daviderezzoli/48/16233_2.png) DavideRezzoli:

> Specifically, we identify a critical inefficiency in L2 block building…

Actually, in the rare occurences of overlapping blocks, [both proposers usually remain profitable](https://ethresear.ch/t/understanding-based-rollups-pga-challenges-total-anarchy-and-potential-solutions/21320#p-51915-are-proposer-a-and-proposer-b-outbidding-each-other-26). This is even more efficient than expected, as it implies competing proposers are complementing eachother.

Taiko Labs intentionally losing funds is unrelated to the based rollup architecture.

Another solution to regular cadence during low-activity would be to create a block subsidy by issuing debt.

---

**Phillip-Kemper** (2024-12-26):

nice work, what I am wondering.

normally sequencing is about the ordering of transactions.

what happens if 2 blocks within the same slots order redundant transactions differently? also what happens if a TX is reverted due to different ordering in the first L2 block of a slot? does this make the 2nd L2 Block invalid or did they never correspond their txns together with a state root or similar anyway?

either way it seems like total anarchy is a little bit overkill and I would prefer total regulated anarchy e.g by adding L2 block id.

---

**alex-damjanovic** (2025-01-02):

Excellent work! Quite an enjoying read.

![](https://ethresear.ch/user_avatar/ethresear.ch/daviderezzoli/48/16233_2.png) DavideRezzoli:

> To answer this question definitively, further analysis is needed. However, the intuition suggests that Taiko Labs becomes profitable under specific conditions. For other proposers, profitability occurs when \text{L2 Priority Fees − (L1 Publication Costs + Proving Costs) > 0}L2 Priority Fees − (L1 Publication Costs + Proving Costs) > 0\text{L2 Priority Fees − (L1 Publication Costs + Proving Costs) > 0}.

Just to check: Isn’t the L2 block proposer getting 75% of the base fee when it’s not TaikoLabs proposer? Source: [Economics | Docs](https://docs.taiko.xyz/taiko-protocol/economics)

---

**DavideRezzoli** (2025-01-03):

Thanks for the comments! Both blocks get on chain, but the sequencer for the first block will receive the L2 priority fees as a reward, while the second one, containing the same transactions, will not get any reward since the transaction are invalidated. To better understand, you can check the blobs and see what’s inside them. Here is a code written by [Mateusz](https://0xmatradomski) to check the blobs [Taiko blob decoder](https://github.com/mateuszradomski/takio-decode-blob)

---

**DavideRezzoli** (2025-01-03):

Hey Alex, thanks for the comments! I followed this [post](https://taiko.mirror.xyz/PhlvGdIaY3-ZQ1DqI9uM5LxrWGWLAzLI84rkxhvPKmM) from Junger, a researcher at Taiko Labs to better understand the role of the base fee. Over the last few weeks, I’ve been reading the Taiko-mono repository, and what you mentioned is correct; the proposer is receiving a portion of the base fee, which can be set, with 75% being the maximum amount. I need to check if this was always the case or if it changed during the on-take hard fork. Anyway, thanks for the feedback! I’ll do some digging and include it in the next post.

---

**vid** (2025-08-14):

Very good work!

What’s the latest status on this problem? Has it been fixed or improved, and if so, how?

