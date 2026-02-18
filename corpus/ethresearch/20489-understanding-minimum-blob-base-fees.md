---
source: ethresearch
topic_id: 20489
title: Understanding Minimum Blob Base Fees
author: tripoli
date: "2024-09-25"
category: Layer 2
tags: []
url: https://ethresear.ch/t/understanding-minimum-blob-base-fees/20489
views: 3061
likes: 37
posts_count: 4
---

# Understanding Minimum Blob Base Fees

# Understanding Minimum Blob Base Fees

---

by [Data Always](https://x.com/data_always) - [Flashbots Research](https://www.flashbots.net/)

Special thanks to [Quintus](https://x.com/0xQuintus), [Sarah](https://x.com/sarahalle_), [Christoph](https://ethresear.ch/u/jcschlegel/summary), and [Potuz](https://x.com/potuz_eth) for review and discussions.

### tl;dr

> The myth that blobs pay zero transaction fees is false. Depending on type of data being posted and the state of gas prices, it costs submitters between $0.10 and $3.00 per blob in mainnet execution fees. EIP-7762, the implementation of a ~$0.01 minimum blob base fee, should have a minimal impact on the market, yet vastly reduce the time that the blob market spends in PGAs during surges of demand while blob usage remains below the blob target.

---

Proposals to set a blobspace reserve price are [controversial](https://x.com/EffortCapital/status/1829663405218693624) [in the](https://x.com/ryanberckmans/status/1829878445553402179) [community](https://x.com/0xfoobar/status/1830313459076182183), but this may stem from a [misunderstanding](https://x.com/ryanberckmans/status/1830643363126587454) of how blobs find their way on chain. A common impression is that blobs are currently contributing zero fees to the protocol, but this is misguided and only true when we restrict our analysis to blobspace fees.

Although the blobspace fee market has been slow to reach the targeted level of demand, thus suffering from the [cold-start problem](https://ethresear.ch/t/eip-4844-fee-market-analysis/15078) initially predicted by [Davide Crapis](https://x.com/DavideCrapis) a year before Deneb, blob carrying transactions still pay [mainnet gas fees](https://www.blocknative.com/blog/blobsplaining), both for execution and priority. The current concern, raised by [Max Resnick](https://x.com/MaxResnick1), is that the hard limit of six blobs per block and the slow response time of the blobspace fee market creates the potential for long-lasting priority gas auctions (PGAs) when the network sees periods of high demand. During these PGAs it becomes much harder for L2s to price their transactions, and when coupled with the current strict [blob mempool rules](https://x.com/titanbuilderxyz/status/1809231370243211601), blob inclusion becomes less predictable.

[EIP-7762](https://ethereum-magicians.org/t/eip-7762-increase-min-base-fee-per-blob-gas/20949) aims to minimize future dislocations between the price of blobspace and blob demand until the adoption of L2s pushes us past the cold-start problem. The current configuration, with the minimum blobspace base fee set to 1 wei, requires at least 30 minutes of fully saturated blocks for blobspace fees to reach $0.01 per blob and to begin to influence blob pricing dynamics. Under the current system, when surges of demand arise the network sees a reversion to unpredictable PGAs as L2s fight for timely inclusion.

As an example, on June 20th the network saw its [second blob inversion event](https://www.blocknative.com/blog/june-20th-blob-contention-event-retrospective), stemming from the [LayerZero airdrop](https://www.theblock.co/post/302945/arbitrum-cashed-in-on-layerzero-airdrop-but-the-boost-was-short-lived). It took six hours of excess demand for blobs until the network reached equilibrium.

[![Blobspace Fees During the LayerZero Airdrop](https://ethresear.ch/uploads/default/optimized/3X/5/e/5ed1c53aac66015377915a554d424c352fbeab0e_2_689x337.png)Blobspace Fees During the LayerZero Airdrop2296×1124 170 KB](https://ethresear.ch/uploads/default/5ed1c53aac66015377915a554d424c352fbeab0e)

> Source: https://dune.com/queries/4050212/6819676

---

### The State of Blob Transaction Fees

Six months post-Deneb blobspace usage [remains below the target](https://dune.com/queries/3757544/6319515). As a result, the blobspace base fee has remained low and the majority of blobs have incurred negligible blobspace gas fees. To date, there have only been three weeks where the average cost of blobspace rose above $0.01 per blob: the weeks of March 25 and April 1 during the [blobscription craze](https://www.coindesk.com/tech/2024/03/28/ethereum-hit-by-blobscriptions-in-first-stress-test-of-blockchains-new-data-system/) and the week of June 17th during the LayerZero airdrop.

[![Average Blobspace Fees per Blob](https://ethresear.ch/uploads/default/optimized/3X/5/5/559e1ee7311c976cd4e130f54e920c7e07c9ce8e_2_690x325.png)Average Blobspace Fees per Blob1895×895 49.8 KB](https://ethresear.ch/uploads/default/559e1ee7311c976cd4e130f54e920c7e07c9ce8e)

> Source: https://dune.com/queries/4050128/6819454

In contrast to fees in blobspace, blob carrying transactions (also known as Type-3) are still required to pay gas fees for execution on mainnet. Despite gas prices falling to a multi-year low, the average blob pays between $0.50 to $3.00 in execution fees. When compared to the [price of call data](https://0xpantarhei.substack.com/i/145648175/is-using-blobs-always-more-cost-effective-than-calldata) historically posted by L2s these costs are insignificant and blobs are essentially fully subsidized by the network, yet this small cost is important when framing a minimum base fee for blobs.

[![Average Execution Fees per Blob](https://ethresear.ch/uploads/default/optimized/3X/e/0/e04ba54d1e4aedf3447c63dd1569912eaf3b1fec_2_690x314.png)Average Execution Fees per Blob2017×919 65.7 KB](https://ethresear.ch/uploads/default/e04ba54d1e4aedf3447c63dd1569912eaf3b1fec)

> Source: https://dune.com/queries/4050088/6819431

If we go a step further and segment the execution cost of blob carrying transactions by their blob contents we see that market is highly heterogeneous. Transactions that carry only one blob pay the highest fees per blob, while transactions that carry five or six blobs pay little-to-no fees per blob. In fact these five or six blob carrying transactions pay [significantly lower total fees](https://dune.com/queries/4053870/6841415).

[![Execution Cost per Blob for Blob Carrying Transactions](https://ethresear.ch/uploads/default/optimized/3X/2/d/2d2ed2bc476512d73167911f3d279200c9dc7c49_2_690x296.png)Execution Cost per Blob for Blob Carrying Transactions1895×815 50.7 KB](https://ethresear.ch/uploads/default/2d2ed2bc476512d73167911f3d279200c9dc7c49)

> Source: https://dune.com/queries/4053870/6825747

A large factor in this discrepancy is the variance in blob [submission strategies of different entities](https://dune.com/queries/4062897/6841224): Base, OP Mainnet, and Blast, as well as many smaller L2s, are extremely financially efficient because they post their data to an EOA which requires only 21,000 mainnet gas for execution regardless of blob count, but these transactions are not well suited for fraud proofs. These chains account for the vast majority of transactions that carry five or more blobs, pushing down the perceived price of submitting many blobs in one transaction. By contrast, L2s that post more complex data to better enable fraud proofs, for instance: Arbitrum, StarkNet, Scroll, ZkSync Era, Taiko, and Linea, use [significantly more mainnet gas](https://dune.com/queries/4097909/6900990) and tend to [submit fewer blobs](https://dune.com/queries/4097685/6900477) (often only a single blob) per transaction.

---

Following from the statistics above, if we combine the blobspace and execution fees on a per transaction basis, we see that outside of the brief surges in demand for blobs, which would not have been affected by adding a minimum base fee, the current distribution of fees paid is almost entirely concentrated in execution fees. This demonstrates that the blobspace fee market is currently non-functional and that there is room to raise the minimum cost of blob gas without meaningfully raising the total cost paid by blobs.

[![Blobspace Share of Transaction Fees Paid by Blobs](https://ethresear.ch/uploads/default/optimized/3X/5/4/54a1b2fb5c880dfa45e1d1263db446697dc45501_2_690x325.png)Blobspace Share of Transaction Fees Paid by Blobs1895×895 74.6 KB](https://ethresear.ch/uploads/default/54a1b2fb5c880dfa45e1d1263db446697dc45501)

> Source: https://dune.com/queries/4034097/6792385

By contrast, if we focus on the periods when the blobspace fee market entered price discovery we see that the majority of fee density rapidly transitions into blobspace fees. When the market works, it appears to work well. As such, the most valuable issue to address is the repeated cold-start problem—where the market currently finds itself.

[![Blobspace Share of Transaction Fees Paid by Blobs When Active](https://ethresear.ch/uploads/default/optimized/3X/7/c/7c26bb97930ae40a5902839d4d2f933b87c02fcc_2_690x325.png)Blobspace Share of Transaction Fees Paid by Blobs When Active1895×895 90.5 KB](https://ethresear.ch/uploads/default/7c26bb97930ae40a5902839d4d2f933b87c02fcc)

> Source: https://dune.com/queries/4060561/6837143

When the blobspace fee market is in an execution fee-dominant environment it benefits blob submitters who post less execution data—mostly OP Stack chains. It also complicates the block building process: historically many algorithms were deciding blob inclusion by priority fee per gas, but since the mainnet gas usage of these transactions varied greatly it forced the L2s that submit higher quality proofs to pay higher rates for the entirety of much larger transactions, further amplifying the advantage of submitting less execution data. By moving closer to a blobspace fee-dominant environment we decrease this advantage.

---

### The Impact of a Minimum Fee

At the current value of ether, Max’s [original proposal](https://x.com/MaxResnick1/status/1829736908655624374) opted to price the minimum fee per blob at $0.05 per blob. Supplementing the cost of execution with this new minimum fee, the proposal would have increased the average cost per blob by 2%.

The revised proposal has decreased the minimum blob base fee to 2^25, about 1/5th the originally proposed value or $0.01 per blob under the same assumptions. Since the beginning of July, this implies an average increase in cost of 0.7% for blobs, but due to the dispersion of financial efficiencies amongst blob submitters the percentage changes are not uniform across entities.

| Blob Submitter | Dataset Size | Current Cost per Blob | Proposed Cost | Historic Impact |
| --- | --- | --- | --- | --- |
| Base | 385,077 | $0.0687 | $0.0797 | 16.0% |
| Taiko | 271,786 | $3.0152 | $3.0262 | 0.4% |
| Arbitrum | 178,127 | $1.0099 | $1.0209 | 1.1% |
| OP Mainnet | 106,979 | $0.0830 | $0.0940 | 13.3% |
| Blast | 78,430 | $0.1655 | $0.1765 | 6.6% |
| Scroll | 49,632 | $2.1304 | $2.1414 | 0.5% |
| Linea | 37,856 | $0.5817 | $0.5927 | 1.9% |
| zkSync Era | 11,837 | $2.6971 | $2.7081 | 0.4% |
| Others | 233,494 | $0.6273 | $0.6384 | 1.8% |
| Total | 1,354,218 | $1.5734 | $1.5844 | 0.7% |

> Table: Blob submission statistics by entity from July 1, 2024 to September 17, 2024, assuming a ETH/USD rate of $2,500. Source: https://dune.com/queries/4089576

Modifying the earlier per-transaction breakdown to account for a 2^25 wei minimum blobspace base fee, and only considering transactions where the original blobspace base fee was less than the proposed new minimum, we see that although the profile begins to meaningfully shift, the blob base fee remains a minority component for all affected blob carrying transactions. The highly efficient transactions submitted by Base and OP Mainnet that carry five blobs would see an increase between 10 to 30% depending on the state of L1 gas prices, which should be easily absorbed. Less efficient transactions, particularly those carrying one to three blobs would see total fee increases of less than 10%.

There have been no blob carrying transactions to date where a minimum blob base fee of 2^25 would have accounted for the majority of the cost paid by the transaction.

[![Blobspace Share of Transaction Fees Paid by Blobs with 2^25 Base Fee](https://ethresear.ch/uploads/default/optimized/3X/3/4/347cdc27de8a573c6be2c32f5ffde9279f6dc917_2_690x325.png)Blobspace Share of Transaction Fees Paid by Blobs with 2^25 Base Fee1895×895 86.6 KB](https://ethresear.ch/uploads/default/347cdc27de8a573c6be2c32f5ffde9279f6dc917)

> Source: https://dune.com/queries/4034254/6792625

---

### Blobspace Response Time

Under [EIP-4844](https://github.com/ethereum/EIPs/blob/7ced2f3a283ae9c2af6a4c2e33bba7fffab3e4c3/EIPS/eip-4844.md#helpers), the maximum interblock update to the blobspace base fee is 12.5%. Starting from a price of 1 wei, it takes 148 blocks at max capacity, over 29 minutes with 12 second block times, for the base fee to rise above 2^25 wei. This updating period has been framed as the response time of the protocol, but it still only represents a minimum amount of time. Due to market inefficiencies blocks do not end up full of blobs, vastly increasing the duration of price discovery.

Leading into the LayerZero airdrop on June 20th, the blob base fee was sitting at its minimum value of 1 wei. At its peak, the blob base fee reached [7471 gwei](https://dune.com/queries/4050697/6820492) ($3,450 per blob). Although this level could have theoretically been reached in under 51 minutes, the climb took nearly six hours. Under Max’s proposal this maximum could have theoretically been reached in 21 minutes, but it’s clear that these theoretical values are not accurate approximations.

Rather than focusing on time, the goal of the proposal is to price the minimum blob base fee below, but close to, the inflection point where blobspace fees begin to form a measurable share of total fees paid by blobs. On June 20th, despite the surge in blobs beginning just after 11:00 UTC, it wasn’t until 15:17 UTC that blobspace fees began to contribute 0.1% of total fees paid by blobs, and it wasn’t until 15:41 UTC that a base fee of 2^25 wei (0.0335 gwei) was exceeded.

[![Breakdown of Blob Fees During the LayerZero Airdrop](https://ethresear.ch/uploads/default/optimized/3X/6/2/62d30681b4d36ed46fda6e27a080d10ba6283ca2_2_690x296.png)Breakdown of Blob Fees During the LayerZero Airdrop1895×815 61.3 KB](https://ethresear.ch/uploads/default/62d30681b4d36ed46fda6e27a080d10ba6283ca2)

> Source: https://dune.com/queries/4050166/6819510

By contrast, had the minimum base fee been 2^25 wei during the LayerZero airdrop, the network may have leapfrogged the cold-start problem and minimized the dislocation between price and demand. We might expect the distribution of blob fees to have behaved as follows, with the blob market still taking an hour or longer to normalize.

[![Blob Fee Breakdown During the LayerZero Airdrop (above 2^25 wei base)](https://ethresear.ch/uploads/default/optimized/3X/b/c/bc512855f739910e4b76132ceefbde4cc0ede375_2_690x325.png)Blob Fee Breakdown During the LayerZero Airdrop (above 2^25 wei base)1895×895 70.5 KB](https://ethresear.ch/uploads/default/bc512855f739910e4b76132ceefbde4cc0ede375)

> Source: https://dune.com/queries/4050746/6820583

In summary, raising the minimum blobspace base fee is not a magic bullet, but it should be viewed as a welcome change to the protocol. The market impact from the leading proposal should be minimal, with only the cheapest and lowest quality blobs seeing a price increase larger than 1%, while still remaining significantly cheaper than their competitors.

---

### Open Questions

- Will the blobspace fee market reach an equilibrium before the Pectra hardfork(s)?
- Will we see additional cold-start problems each time the blob limit is increased with future hard forks?
- Will the blob market move towards private mempools?
- How have block building algorithms changed to better handle blobs since the LayerZero airdrop?
- Should revenue from these PGAs be captured by proposers or by the protocol?

## Replies

**roberto-bayardo** (2024-09-25):

I strongly support a higher minimum blob base fees; this will be even more important if we decide to increase the blob target to 4 without increasing the max, as is currently under consideration.

One thing to note is that during the LayerZero spike, Base witnessed significant difficulties landing blob transactions, even with fees set well above what should have been required. We tracked it down to the way geth was handling blob transactions in its transaction pool. We submitted a fix which has been included in the latest release (1.14.9), which is perhaps not rolled out that widely yet. We also observed that FlashBots was not including any blobs in their blocks (also since fixed), though this was probably not a huge factor overall (<5% of blocks IIRC).

I expect the next spike in DA demand should be handled more gracefully. Still, a higher minimum fee would only provide added protection and in my view should be part of PectraA regardless of where we settle on the blob target.

---

**Evan-Kim2028** (2024-09-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> Rather than focusing on time, the goal of the proposal is to price the minimum blob base fee below, but close to, the inflection point where blobspace fees begin to form a measurable share of total fees paid by blobs. On June 20th, despite the surge in blobs beginning just after 11:00 UTC, it wasn’t until 15:17 UTC that blobspace fees began to contribute 0.1% of total fees paid by blobs, and it wasn’t until 15:41 UTC that a base fee of 2^25 wei (0.0335 gwei) was exceeded.
>
>
> Breakdown of Blob Fees During the LayerZero Airdrop1895×815 61.3 KB
>
>
>
> Source: https://dune.com/queries/4050166/6819510

By contrast, had the minimum base fee been 2^25 wei during the LayerZero airdrop, the network may have leapfrogged the cold-start problem and minimized the dislocation between price and demand. We might expect the distribution of blob fees to have behaved as follows, with the blob market still taking an hour or longer to normalize.

[![Blob Fee Breakdown During the LayerZero Airdrop (above 2^25 wei base)](https://ethresear.ch/uploads/default/optimized/3X/b/c/bc512855f739910e4b76132ceefbde4cc0ede375_2_690x325.png)Blob Fee Breakdown During the LayerZero Airdrop (above 2^25 wei base)1895×895 70.5 KB](https://ethresear.ch/uploads/default/bc512855f739910e4b76132ceefbde4cc0ede375)

> Source: https://dune.com/queries/4050746/6820583

Why do these charts have different x-axis time ranges? I am finding it difficult to understand the charts when one starts at 15:41 and the other starts at 11:00. It is visually difficult to see the above 2^25 effect on the blob fee breakdown

---

**0xemperor** (2024-09-27):

Would it be tricky to estimate the total cost of having the blob market in place when 4484 went live vs not? just to quantify it concretely.

Also, do you have any intuition on how a high blob demand event would play out in the existence of this EIP, given we are looking at just 0.01$

Thanks for your work!

