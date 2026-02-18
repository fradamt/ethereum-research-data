---
source: ethresearch
topic_id: 18567
title: On Increasing the Block Gas Limit
author: Nero_eth
date: "2024-02-05"
category: Economics
tags: [data-availability]
url: https://ethresear.ch/t/on-increasing-the-block-gas-limit/18567
views: 10586
likes: 48
posts_count: 23
---

# On Increasing the Block Gas Limit

# On Increasing the Block Gas Limit

*by [Toni](https://twitter.com/nero_eth) and [Vitalik](https://twitter.com/VitalikButerin).*

*special thanks to the Starkware team for feedback and data!*

## The TL;DR

- By increasing the block gas limit and the price for nonzero calldata bytes, a smaller and less variable block size can be achieved, making space to add more blobs in the future.
- Increasing the price for nonzero calldata reduces the maximum possible block size. At the same time, the block gas limit could be raised to make more space for regular transactions.
- This further incentivizes the transition to using blobs for data availability, strengthening the multidimensional fee market by reducing competition between calldata and blobs.
- It slows down history growth, which might be preferable in preparing for the Verkle upgrades.

## Rollup-Centric Block Size

Ethereum’s block size hasn’t been changed since [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559).

With a focus on the [rollup-centric roadmap](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698) in the medium, or possible long term future one might argue that the way block space is used hasn’t been optimized for rollups yet. With the introduction of [EIP-4844](https://www.eip4844.com/), we’re taking a big step towards making Ethereum more rollup-friendly. However, the capacity of Beacon blocks and the size of their individual parts have remained mostly unchanged.

[Over the past 12 months](https://etherscan.io/chart/blocksize), the effective block size measured in bytes essentially doubled. This might be a result of more and more rollups starting to use Ethereum for DA and trends like [Inscriptions](https://blockworks.co/news/inscriptions-craze-proves-stark-contrast-between-ethereum-rollups).

See [Appendix 1](#Current-Situation) for the numbers.

**By reducing the maximum size of the EL parts of Beacon blocks, one can make room for more blobs while maintaining the current security levels:**

[![storage_distribution](https://ethresear.ch/uploads/default/original/2X/e/e3d43baa3aafc8a2f9fb9b1b61af7212f4db6855.png)storage_distribution776×207 9.84 KB](https://ethresear.ch/uploads/default/e3d43baa3aafc8a2f9fb9b1b61af7212f4db6855)

## The Goals

- Better separate data from execution. Blobs are designated to serve one specific thing - data. On the other hand, calldata is used for execution and data. Cheap calldata was important to accelerate the adoption of rollups, but its price must be reconsidered under EIP-4844.
- Reduce Beacon block variance and size. The size of Beacon blocks is heavily dependent on the EL payload, which can be maximized in size using calldata. For large Beacon blocks, the EL payload accounts for 99% of their size (see Appendix 2). It’s important to note that it’s not the average block size that is problematic. With 125 KB the median block size is 14.5 times smaller than maximally possible. The aim is to decrease this gap and reduce the avg/max ratio in block sizes.
- Make sure not to harm a specific set of users/applications disproportionally. While data-availability oriented apps can start using blobs, apps that handle big on-chain proofs, which are not just simply data, might be affected more.
- Reduce number of reorged blocks.

[![boxplot](https://ethresear.ch/uploads/default/optimized/2X/9/9ee8dab0b7804e4320a5e9b6ec33ac3225307cf2_2_690x229.png)boxplot1200×400 23.2 KB](https://ethresear.ch/uploads/default/9ee8dab0b7804e4320a5e9b6ec33ac3225307cf2)

> Notable, there were significantly less data points for reorged blocks (368 vs ~129k).

The chart shows the size of reorged vs not-reorged blocks of the last ~16 days (19 Jan - 4 Feb 2024).

- In the last 16 days, blocks that were eventually reorged were ~93% larger (median) than blocks that were eventually finalized.
- The avg. block size of the reorged blocks was 0.155 MB while blocks making it into the canonical chain had around 0.08 MB.



# Design Considerations

As of today, we have been focusing on 5 different designs and want to quickly outline the pros and cons of each of them.

## (1) Increase Calldata to 42

By simply increasing calldata costs to 42.0 gas, we can reduce the maximum possible block size from ~1.78 MB to ~0.68 MB. This makes room to increase the block gas limit, for example to 45 million, giving us a max block size of ~1.02 MB.

[![gas_limit_increase](https://ethresear.ch/uploads/default/optimized/2X/c/c639afe3be1b65f5e6d5f3d4a5ea26f8f69c829d_2_690x229.png)gas_limit_increase1200×400 47.8 KB](https://ethresear.ch/uploads/default/c639afe3be1b65f5e6d5f3d4a5ea26f8f69c829d)

> The area inside the green circle might potentially represent a sweet spot.

### Pros

- Reduces the maximum block size and its variance and makes room for more blobs in the future.
- Increases costs of using calldata for data availability, thus strengthens the multidimensional fee market.
- It’s simple.

### Cons

- Affects apps that are dependent on much calldata, not just for data availability. On-chain STARK proof verification, which is super important to have, could become substantially more expensive for large proofs.



## (2) Increase Calldata to 42 and Decrease Other Costs

Like in the previous example (1), we could make it more expensive to use calldata but cheaper to perform certain arithmetic operations that are common in calldata-heavy proof verification, and that are not on the frontier of “causes of worst-case block time”. This approach is designed to balance out the higher expenses for applications that use a lot of calldata and are unable to switch to using blobs.

Taking Starknet as an example, the main cost drivers are the opcodes `JUMPI`, `PUSH1`, `ADD`, followed by `DUP2`, `PUSH2` and `JUMP`.

[![drawing](https://ethresear.ch/uploads/default/optimized/2X/0/0fcc976322d2d5dbf4ec81e8ac479035fe38384e_2_428x500.png)drawing600×700 37.7 KB](https://ethresear.ch/uploads/default/0fcc976322d2d5dbf4ec81e8ac479035fe38384e)

This leads to a question for client developers: “*Which opcode’s cost could be lowered to save on gas for calldata heavy proof verification?*”

> It is very likely that one will not be able to fully “compensate” affected applications through lowering the costs of specific operations. For example, even if we set ADD, SUB, MUL, MULMOD, which are all part of a STARK proof verification, to 1 gas, we’d only save around 322,624 of a total ~2,596,128 gas spent on EVM operations.

### Pros

- Increases costs of using calldata for data availability which leads to a lower block size variance.
- Reduces the maximum block size.
- Still simple to implement.

### Cons

- Slightly more complex and requires further analysis on potential side-effects.
- Might not fully offset the increase in calldata costs.



## (3) Simple 2D Pricing for Calldata

As proposed in [EIP-4488](https://github.com/ethereum/EIPs/blob/017fa2524e5aeb0bce201777cb31b1c0c1b14d4c/EIPS/eip-4488.md), we could introduce a 2D price mechanism by capping the calldata per block. This reduces the supply of calldata per block, making it a more scarce resource.

EIP-4488 introduces a `BASE_MAX_CALLDATA_PER_BLOCK` and a `CALLDATA_PER_TX_STIPEND`.

- The BASE_MAX_CALLDATA_PER_BLOCK determines the maximum calldata that can be used (in an empty block). For each transaction, the available calldata increases. A transaction’s maximum calldata is the full BASE_MAX_CALLDATA_PER_BLOCK plus its stipend.
- The CALLDATA_PER_TX_STIPEND acts as an additional calldata-usage-bonus per transaction.

Using the values proposed in the EIP, except keeping the calldata costs at 16 gas, the maximum block size would be ~1.332 MB.

### Pros

- Disincentivizes calldata usage for data availability.
- Doesn’t affect standard transactions or token transfers.
- Reduces the maximum block size.

### Cons

- Affects apps that are dependent on much calldata, not just for data availability.
- Increased complexity in analysis and implementation.
- Multi-dimensional resource limit rules for block building.



## (4) Full 2D Pricing for Calldata

By creating a market [similar to EIP-1559](https://ethresear.ch/t/multidimensional-eip-1559/11651) but specifically for calldata, we could completely separate it from other operations, [much like we do with blobs](https://notes.ethereum.org/@vbuterin/proto_danksharding_faq#What-does-the-proto-danksharding-multidimensional-fee-market-look-like). We could set an initial target for calldata usage, for example 125 KB, and then allow it to have up to 1 MB if needed. The price for using calldata would automatically adjust based on how much demand there is. In addition to data used for data availability (blobs), we would introduce a new type of ‘container’ specifically for calldata required for execution.

### Pros

- Disincentivices calldata usage for data availability.
- Clean separation of calldata used for execution and data.

### Cons

- Increased complexity in analysis and implementation.
- Multi-dimensional resource limit rules for block building.



## (5) Increase Calldata With ‘EVM Execution Discount’

Imagine we could provide those that are still requiring large calldata for on-chain computation (e.g. proof verification) with a bonus that compensates them for increased calldata costs.

By introducing a formula like the following, we can reduce block sizes while not disproportionally hurting calldata dependent apps.

`tx.gasused = max(21000 + 42 * calldata, 21000 + 16 * calldata + evm_gas_used)`

- The calldata is high (42 gas) for those that rely more on data availability.
- The calldata is low (16 gas) for those that additionally spend gas on evm computation.
- Spending 26 gas per calldata byte on evm_gas_used enables access to 16 gas calldata.

**This can be visualized as follows:**

[![transaction_dist](https://ethresear.ch/uploads/default/optimized/2X/4/4a56b8b958197506579ca231e0dddf76498fccc4_2_690x345.png)transaction_dist800×400 93.7 KB](https://ethresear.ch/uploads/default/4a56b8b958197506579ca231e0dddf76498fccc4)

- The chart shows all transactions from 01.01.2024 to 31.01.2024.
- The colored areas indicate the minimum evm gas (y-axis) a transaction must spend for every calldata byte (x-axis) to reach the 16 calldata price for different ‘high’ calldata prices of 32, 42 and 68 gas.
- We can see some colored points forming bars at the bottom. These apps are using much calldata but pay relatively low amounts of gas. This can be attributed to DA leveraged through calldata.
- For example, an application that uses 146 KB transactions spending 7 million gas in evm_gas_used will profit from the formula, 21000 + 16 * calldata + evm_gas_used and eventually pay 16 gas per calldata.
- An application that has 200 KB calldata transactions costing 9 million evm gas will pay 21_000 + (16*200*1024) + 9_000_000 = 12_297_800 instead of 21_000 + (42*200*1024) + 9_000_000 = 17_622_600.
- The pure DA consumers would not reach the green area and therefore pay 42 gas per calldata byte.

For the *‘16 vs 42 gas’* variant, the maximum EL block size decreases by 62% to ~0.68 MB.

The area in which the evm gas used “compensates” for the calldata price increase requires to use at least 26 gas for evm operations per calldata byte.

**The interplay between the evm gas usage and its impact on the calldata price and be visualized as follows:**

[![gasmap_legacy2](https://ethresear.ch/uploads/default/optimized/2X/2/248ba1091eed2e71f5fc03c0fb91fbb3f7d22f1c_2_690x280.jpeg)gasmap_legacy21721×700 105 KB](https://ethresear.ch/uploads/default/248ba1091eed2e71f5fc03c0fb91fbb3f7d22f1c)

**Current Situation:**

- There is no special interaction between the evm gas used and a transaction’s gas usage.

**Execution Discount:**

- Constant Before Threshold: The observed constant total gas usage for lower EVM gas usages in the plot indicates transactions where the EVM operations do not yet contribute sufficiently to reach the cheaper calldata rate. In this phase, the total gas cost is primarily determined by the calldata size, priced at the higher rate.
- Increase Beyond Threshold: The increase in total gas usage at higher EVM gas usages reflects transactions crossing the threshold where their EVM operations’ gas cost is sufficient to leverage the cheaper calldata rate. However, because this now includes significant EVM gas usage in the total cost, the overall gas expense rises proportionally to the additional EVM operations conducted.

This means, we reach the 16 gas calldata price by using 26 gas per calldata byte on evm operation. For large calldata users this settles at a ~61% ratio of exec/data. The chart shows this threshold over a range of calldata sizes.

[![calldatapercentage](https://ethresear.ch/uploads/default/optimized/2X/7/7d2d6a6d54fa4d6cb3b942182984631101c187dd_2_690x287.png)calldatapercentage1200×500 35.2 KB](https://ethresear.ch/uploads/default/7d2d6a6d54fa4d6cb3b942182984631101c187dd)

**As long as evm\_gas\_used > 26 \times calldata\_size, one profits from the execution discount formula.**

### Pros

- Disincentivices calldata usage for data availability.
- Reduces blocksize to 0.68 MB, making space for gas limit increases and/or raising the number of blobs.
- Reduces block variance.
- Token transfers or approvals would qualify for the 16 gas calldata. So no effects on regular users.

### Cons

- Slightly increases complexity.
- Introduces some interplay (and potentially side-effects) between calldata size and gas spent on evm gas.



## Summarizing

It makes sense to think about ways to decrease the maximum possible size of Beacon blocks to make room for 4844 blobs, prepare for [Verkle](https://verkle.info/) and reduce the variance in block size. Increasing the calldata price will act as a disincentive to continue using calldata for data availability. Scaling through increasing the blob count comes with less variance in max. size data to handle.

Simply raising the calldata cost to 42 might be too blunt an approach, while creating separate fee markets could add too much complexity. A balanced solution could be to increase the cost of calldata while reducing the cost of some operations, or perhaps moving towards a model that offers incentives for using calldata inside the EVM.

Ultimately, these changes would reduce competition in the traditional fee market and strengthen the multidimensional fee market.

---

# Appendix

## Current Situation

The use of calldata has rapidly increased in the past year - it essentially doubled - which might be attributable to rollups using Ethereum for DA and [Inscriptions](https://blockworks.co/news/inscriptions-craze-proves-stark-contrast-between-ethereum-rollups).

[![calldatasize_over_time](https://ethresear.ch/uploads/default/optimized/2X/4/46cae20b5f4e46c339b3ce7f2df768b1ce8368fa_2_690x250.png)calldatasize_over_time1100×400 90.2 KB](https://ethresear.ch/uploads/default/46cae20b5f4e46c339b3ce7f2df768b1ce8368fa)

The above chart shows the maximum block size observed every 1,000 blocks (to reduce the number of datapoints). We can clearly see a continuous increase with a rising number of positive outliers since April 2023.

The maximum share in size of the EL payload is currently at 69.3% of the total Beacon block + the blobs. By increasing the calldata costs to 42 gas while increasing the block gas limit to ~45 million would effectively reduce the blocksize by 58% while decreasing the share of the maximum possible EL payload to 56 of the total Beacon block incl. blobs.

[![pies](https://ethresear.ch/uploads/default/optimized/2X/3/3979e18625a894d72f4b17f35ef23a69a7ea64c9_2_690x202.png)pies1364×400 47.7 KB](https://ethresear.ch/uploads/default/3979e18625a894d72f4b17f35ef23a69a7ea64c9)

- Reducing the EL payload size opens up the potential to add more blobs without surpassing the current maximum block size (30m limit / 16 gas calldata).
- 6 blobs have a size of 0.75 MB.
- The proposed change would reduce the max. possible block size by 0.76 MB (1.78 - 1.02).

As of today, we see block sizes of up to ~1 MB on a daily basis, with a potential maximum of ~1.78 MB per block.

#### Max Block Size per Day

[![block_size_over_time](https://ethresear.ch/uploads/default/optimized/2X/6/6cdba35ed66fbdb60607654a7e42134f7c95ca39_2_690x229.png)block_size_over_time1200×400 55.6 KB](https://ethresear.ch/uploads/default/6cdba35ed66fbdb60607654a7e42134f7c95ca39)

---

#### EL Payload Share - Average block

- On average, the EL payload accounts for ~20% of the total size of the Beacon block.

[![elpayload_share_avg](https://ethresear.ch/uploads/default/optimized/2X/3/3156e6924912d1829e6782de6f367d4a6e46eeb8_2_690x229.png)elpayload_share_avg1200×400 46.4 KB](https://ethresear.ch/uploads/default/3156e6924912d1829e6782de6f367d4a6e46eeb8)

#### EL Payload Share - Large blocks

- For larger blocks, this share increases to ~99%. Thus, the EL payload is the main contributor to large blocks.
- This chart shows the share of the EL payload compared to the complete Beacon block for big (0.99% quantile) blocks.

[![elpayload_share_99](https://ethresear.ch/uploads/default/optimized/2X/0/0e9a03859c80a5e17222bbd41194a7f928020ad9_2_690x229.png)elpayload_share_991200×400 44.3 KB](https://ethresear.ch/uploads/default/0e9a03859c80a5e17222bbd41194a7f928020ad9)

#### Related links

- EIP-4488 by Vitalik and Ansgar
- On Block Sizes, Gas Limits and Scalability by Toni
- Block size over time by Etherscan
- Rollup Calldata Usage over Time by @niftytable

## Replies

**guthlStarkware** (2024-02-05):

Thanks a lot for reaching out to the team. Love the intiative ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

On a personal note, I see a couple of points I do not understand:

1. How is Verkle Tree impacted by this change since Calldata is not stored in state?
2. You are assigning the raise in calldata to inscriptions and rollups when the rise happened before their launch and does not take into consideration the change triggered by 1559 that block max gas limit varies between 15m and 30m gas. It might be interesting to see if the computation heaviness of the blocks being reorged.
3. 4844 will come out soon and will dramatically reduce avg block size. If your assumptions of block size impacting propagation holds to be true, the analysis you provide could be reinforced or challenged. I would love to see an analysis post 4844 to understand if your claim on reorg holds.

For context, I worked on 2828, 4490 and participated in the initial discussions which led to 4488 and 4844.

---

**Nero_eth** (2024-02-05):

Yeah, good points!

1. You’re right. I was more thinking about  constrasting it to a “naive” block limit increase that causes the general throughput on L1 to increase, which might push nodes to their limits and might require reconsidering opcode pricing.
2. Yeah, I agree. I did some short section in this recent post on the change of 1559 and it looks like it did increase the avg throughput slightly compared to the situation before.
3. The costs will determine where rollups will post their data. If they all switch to using blobs, then the cost for blobspace increases, while L1 gas costs might decrease. In the end there should be enough space on the blob front to not push rollups towards using calldata for DA and thereby compete for resources with regular users.

---

**benaadams** (2024-02-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> It slows down state growth, which might be preferable in preparing for the Verkle upgrades

Unless I’m misunderstanding state growth is completely orthogonal to this, you mean Historical Data growth? (Also addressed via something like eip-4444, since the EL doesn’t really use Historical Data for block processing/validation beyond syncing)

---

**Nero_eth** (2024-02-05):

Yeah right, this was expressed very poorly. And yeah, no direct relation except for syncing.

EDIT. I fixed it in the TLDR points of the text.

---

**kakia89** (2024-02-05):

According to a modeling we did on rollups deciding between using calldata posting strategy vs blob posting strategy ([2310.01155.pdf (arxiv.org)](https://arxiv.org/pdf/2310.01155.pdf)), smaller rollups will use calldata while larger ones will use blobs. Threshold on what is smaller and what is larger is defined in the equilibrium.

Increasing calldata price will force more rollups to use blob posting strategy, which in turn increases blob price in the equilibrium, with the current target number 3. On the positive side, blobs will be fuller.

---

**vbuterin** (2024-02-06):

I think the goal is that we simultaneously reduce max calldata size and increase max blob count, so total max theoretical bytes remains the same (but average-case available bytes increases, because calldata has a very unfavorable worst case / average case ratio whereas with blobs it’s just 2:1)

---

**noamnisan** (2024-02-06):

Maybe the problem (of large call-data) will solve itself once 4844 comes into effect since those who use it now for DA will just move to blobs with no further action necessary?

---

**Nero_eth** (2024-02-06):

I think, without further scaling on the blob front, we might find ourself in a balanced price between using calldata vs blobs and rollups will be able to switch dynamically.

The externalities imposed by those that want their history to be stored in plain forever - of until we get history expiry - are larger than those of blob users, so it makes sense to treat them differently.

Also, if we don’t touch calldata pricing we will always have to deal with the inefficient case that the avg. block has 125 KB while it could potentially have a max of > 2.7 MB. This is a huge discrpancy that is super inefficient.

---

**tripoli** (2024-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> In the last 16 days, blocks that were eventually reorged were ~93% larger (median) than blocks that were eventually finalized.

Are there other factors that influence this? Based on my stats, the winning bid for the median forked mev block arrives about 1200ms later than the median succcessful block, but that would only account for ~10% of the difference. Are blocks from Coinbase / solo stakers / Rocket Pool statistically larger (as they make up an overweight share of forks)?

I’m just wondering about this in the context of monitoring timing games. Maybe block size needs to get factored into the stats as well.

---

**Nero_eth** (2024-02-06):

Yeah good question. Without having looked deeper into it, my feeling is that both variables, timing and size, have great influence on the reorged block rate. Also, the used clients may have great impact.

I cannot think of scenarios in which that Rocketpool Operators or Solo Stakers have more DA transactions in their blocks than others. Why would that be the case? Difficult to say because of the many variables that impact the reorg rate.

---

**tripoli** (2024-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> I cannot think of scenarios in which that Rocketpool Operators or Solo Stakers have more DA transactions in their blocks than others.

The only thing that stands out to me is MEV-Boost prevalence and different building algorithms for self-built vs MEV builders. Are there any good studies of missed/forked blocks? Looks like ~50% are PBS (half of those being Coinbase slots). I wonder if the rest are payload timeouts or were always going to be self-built. Maybe the other 50% are just really big and slow to propagate.

---

**Nero_eth** (2024-02-06):

I have some numbers on that on [timing.pics](https://timing.pics) but yeah, identifying a single cause is challenging due to the numerous influencing factors. Recently, we observed that participants engaging in timing strategies have been missing more slots. Additionally, solo stakers are often among those with the highest slot miss rates, relatively speaking. It’s important to note that the solo staker category, as typically presented on various sites, includes ‘zombie validators’—those who have lost their keys. This contributes to their lower efficiency often seen in stats.

---

**tripoli** (2024-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Yeah good question. Without having looked deeper into it, my feeling is that both variables, timing and size, have great influence on the reorged block rate.

I was curious, so I took a look at the time dependency of the comparative block sizes. It looks to me like there are two definite regimes, with forked blocks very late in the slot not being too much larger than finalized blocks late in the slot, but for earlier blocks the ratio is really high (a max of 250%+ rather than the 93% claimed for the set of all times).

[![forked-block-size-ratio](https://ethresear.ch/uploads/default/optimized/2X/4/4597db025a2ae8d5f4816df169a52b16e8d1bddb_2_690x345.png)forked-block-size-ratio2600×1300 134 KB](https://ethresear.ch/uploads/default/4597db025a2ae8d5f4816df169a52b16e8d1bddb)

---

**Nero_eth** (2024-03-03):

How is the block size defined on the y axis, is that in bytes?

This would be an interesting result that even strenghens the argument of the block size significantly impacting the event of being reorged.

I did some logistic regressions an already got significant results with very low p values, so I’d expect, if one cleans the data set by those transactions that were regored bc they were very late, then we should get event better results.

---

**tripoli** (2024-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> How is the block size defined on the y axis, is that in bytes?

bytes / bytes. It’s the quotient of the median forked block size against the median finalized block size. And agreed re-strengthening the argument.

---

**yyd106** (2024-03-14):

Any update on this? Blobs unlocked a huge potential, and seems the demand of data needs a long time to meet the capacity.

---

**Nero_eth** (2024-03-18):

Yeah, there exists and EIP (EIP-7623) and some analysis on it:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png)
    [Analyzing EIP-7623: Increase Calldata Cost](https://ethresear.ch/t/analyzing-eip-7623-increase-calldata-cost/19002) [Execution Layer Research](/c/execution-layer-research/37)



> EIP-7623: Increase Calldata Cost
>
> EDIT, April 2024: With ongoing analysis, the TOTAL_COST_FLOOR_PER_TOKEN was reduced from 16 to 12 in the current status of the EIP.
>
> EIP-7623 aims to recalibrate the cost of calldata bytes.
> The proposal’s goal is to reduce the maximum possible block size without affecting regular users who are not using Ethereum exclusively for DA. This comes with reducing the variance in block size and makes room for scaling the block gas limit or the blob count.
> With implem…

---

**kevin-hs-sohn** (2024-04-05):

This might be a little bit off-topic, but I’m just curious.

Why can’t we just increase the block gas limit substantially and add an explicit limit on the block size instead?

I thought the major bottleneck of decentralized scaling was the networking overhead in block propagation, not the computation/storage overhead in EVM execution. So as long as we can keep the block size small (e.g., under 2MB), more computations shouldn’t be a problem, theoretically.

(Even this very article is using “maximum possible block size” as a key metric for measuring the consensus overhead that the adjustments may affect, not “computational costs that node operators pay”)

Considering that most of the current blocks only contain ~0.1 MB data, if what I’m saying makes sense, I think we potentially have quite a lot of room to scale the block size in terms of networking costs.

Please correct me if I’m wrong.

(I assume this subject must have been discussed somewhere else before, but I couldn’t find any materials)

cc. [@vbuterin](/u/vbuterin)

---

**MicahZoltu** (2024-04-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/kevin-hs-sohn/48/15901_2.png) kevin-hs-sohn:

> I thought the major bottleneck of decentralized scaling was the networking overhead in block propagation, not the computation/storage overhead in EVM execution.

IMO the biggest problem with Ethereum’s gas limit right now is that it allows for significant state growth over time, and that is driving Ethereum node operation further and further away from consumers.  If you can’t run your own node, then the network is no longer censorship resistant because you are relying on the good will of others to be willing to let you use their node.  You also lose a bit of privacy since you likely need to pay someone to use their node and currently most of the node providers do not allow anonymous purchases (also further encouraging censorship).

---

**kevin-hs-sohn** (2024-04-05):

I’m not sure if storage cost is the major issue here.

Currently, running a full node requires around 1TB SSD, while even 8TB SSD costs around $500, which I don’t think is too expensive even for solo stakers (given that they’re staking 32 ETH)

(assuming we’re talking about the costs in the consensus layer)


*(2 more replies not shown)*
