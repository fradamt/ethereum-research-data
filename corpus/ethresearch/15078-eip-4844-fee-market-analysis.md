---
source: ethresearch
topic_id: 15078
title: EIP-4844 Fee Market Analysis
author: dcrapis
date: "2023-03-16"
category: Economics
tags: [data-availability, layer-2]
url: https://ethresear.ch/t/eip-4844-fee-market-analysis/15078
views: 14452
likes: 45
posts_count: 19
---

# EIP-4844 Fee Market Analysis

*Thanks to Barnabé Monnot, Danny Ryan, and participants to the RIG Open Problem 3 (Rollup Economics) for helpful discussions and feedback.*

EIP-4844 introduces two main components to the Ethereum protocol: (1) a new transaction format for “blob-carrying transactions” and (2) a new *data gas* fee market used to price this type of transactions. This analysis focuses mainly on the **data gas fee market and its key parameters**.

We first discuss the relation between the 4844 and 1559 fee mechanisms and their interaction. Then we present an analysis rooted in a [simulation and backtest with historical data](https://github.com/dcrapis/blockchain-dynamic-pricing/blob/685b837dda64d149bd330e5619cf9682f4e58dc8/eip-4844-sim.ipynb). Finally we discuss potential improvements on current setup.

## 1559 & 4844: a dual market for transactions

The data gas fee mechanism in 4844 is rooted in the 1559 mechanism. It introduces a similar adaptive rule, sustainable target, and block limit structure with minor differences that we summarize in the next section. The most important innovation is the fact that it is the first step towards multi-dimensional resource pricing in Ethereum (Endgame 1559?!). **The blob data resource is unbundled from the *standard gas* metering and gets its own dynamic price based on blob supply/demand**.

However, it is important to note that this is only a partial unbundling of the data resource. Standard transactions are still priced as before, with standard conversions for calldata of 16 gas units per byte and 4 units per empty byte. Only blob transactions use both markets with their EVM operations being priced in standard gas and their blob data being priced in data gas.

We essentially have a **dual market for transactions with standard transactions using the one-dimensional (1559) mechanism and blob transactions using the two-dimensional (1559 x 4844) mechanism**. This distinction is important because users can decide to use any of the two transaction types and there will be relevant interactions between the two markets.

### Data gas accounting & fee update in 4844

We give a summary that clarifies the key features of the 4844 data gas fee market. See relevant sections in the [EIP-4844 Spec](https://eips.ethereum.org/EIPS/eip-4844) for details and [Tim Roughgarden’s EIP-1559 analysis](https://timroughgarden.org/papers/eip1559.pdf) for an extended summary & analysis of the related 1559 mechansim.

Blob-carrying transactions have all fields required by the 1559 mechanism (`max_fee`, `max_priority_fee`, `gas_used`) and also a new field (`max_fee_per_data_gas`) to specify willingness to pay for data gas. This type of transactions can carry up to two blobs of 125kb each and these determine the amount of `data_gas_used` which is measured in bytes. Such a transaction is valid if it passes the 1559 validity conditions & additionally the `max_fee_per_data_gas` is bigger or equal to the prevailing `data_gas_price`. Initially, the `TARGET_DATA_GAS_PER_BLOCK` is set to 250kb (2 blobs) and the `MAX_DATA_GAS_PER_BLOCK` to 500kb.

The data gas price for slot n is computed with a beautiful formula

p^{\text{data}}_n = m \cdot\exp\left(\frac{E_{n-1}}{s}\right),

where m is the `MIN_DATA_GASPRICE`, s is the `DATA_GASPRICE_UPDATE_FRACTION` which corresponds to a maximum update of 12.5% up or down in consecutive blocks, and E_{n-1} is the total excess data gas accumulated to date above the budgeted target data gas.

## Backtesting with actual demand from Arbitrum & Optimism

**Main 5 takeaways:**

1. L2 demand structure is very different from user demand. L2s operate a resource-intensive business on Ethereum: they post transactions via bots at constant cadence, their demand is inelastic, and the L1 cost is their main operating cost.
2. Projected demand for blobs data from L2s is currently 10x lower than the sustainable target and will take 1-2 years to reach that level.
3. Until sustainable target demand is reached, the data gas price will stay close to the minimum (see chart and cold-start section).
4. When sustainable target demand is reached, the data gas price increases exponentially. If the minimu price is 1 this results in a 10 orders of magnitude cost increase for L2s in a matter of hours.
5. We discuss a few potential improvements that involve only minimal changes to the fee market parameters (see “Wat do?” section).

**Let’s dive in…**

We did a backtest using the historical batch-data load of Arbitrum and Optimism (this represents ~98% percent of the total calldata consumed by L2 batches). We chose the day with the highest batch-data load in the first two months of 2023, February 24th.

- Arbitrum posted 1055 consistent batches of ~99kb (600b stdev) every 6.78 blocks on avg, for a total of ~100mb/day
- Optimism posted 2981 variable batches of avg ~31kb (19kb stdev) every 2.37 blocks on avg, for a total of ~93mb/day

### Analysis 1: fee update in practice

Arbitrum demand for data comes at a rate of 14.6kb/block and Optimism demand at 13kb/block (Ethereum blocks). With the current setup of the fee update mechanism, **price discovery effectively does not start until the data demand load is above the block target of ~250kb**, about 10x the current load. To see this you can either assume that batch posters are smart in balancing and coordinating so that no block is above the target and the data price never moves from the initial minimum value of 1 wei, or simply notice that local increases in excess gas will quickly be absorbed so that the data price never goes much above 1.

[![](https://ethresear.ch/uploads/default/optimized/2X/7/7bf816afe78d4730a680859eb42486dddef45fd5_2_689x255.png)1106×409 50.8 KB](https://ethresear.ch/uploads/default/7bf816afe78d4730a680859eb42486dddef45fd5)

> EIP-4844 data gas price dynamics in two backtest scenarios: blob data demand rate is similar to historical (left) and blob data demand rate is 10x historical (right). Both assume same distribution for max_fee_per_data_gas, uniform centered around 50 gwei (see link at the top for full simulation).

When potential demand is above the target, the price gets updated so that the blob transactions with lowest willingness to pay are dropped and balance with the sustainable target is maintained. But how long will it take? From January 2022 to December 2022 the [combined data demand of Ethereum rollups increased 4.4x](https://dune.com/niftytable/rollup-economics), which means that continuing at this rate (or slightly higher considering innovation and 4844 cost reduction), **it will take in the order of 1.5 years for the data price discovery mechanism kick-in and data price to start raising above 1**.

Having such a long time with data price at 1  creates **unreasonable expectations on blob data costs**. Users and apps on L1 may make adjustments to start using blobs, only to be forced back to type 2 transactions once L2 demand (with higher willingness to pay) raises above target. In the worst case, this severe underpricing may lead to [taproot-like usecases](https://read.pourteaux.xyz/p/illegitimate-bitcoin-transactions) that will inject instability in the blob-data market that is undesirable from a rollup-economics perspective (as the next sections clarify).

### Analysis 2: L2 costs

An Arbitrum transaction that posts one batch today consumes about 1.89M gas. Assuming an average fee of 29 gwei and an ETH price of $1500 the cost is about $85 per batch. The gas spent for calldata is about 1.59M and costs $70.

Switching to blobs will consume about 50K gas in precompiles at $2.2 cost, and 125K datagas which at a data price of 1 will cost $2e-10 (basically **free**).

If the datagas price was, say 30 gwei, this would correspond to a data cost of $5.62 per blob, which is still 12x cheaper than the cost incurred for batch calldata today. This seems a **price that rollups would be willing to pay and that is also fair, considering that the eventual sustained load on the system is 12x for calldata vs blobdata**:

*“The sustained load of this EIP is much lower than alternatives that reduce calldata costs […]. This makes it easier to implement a policy that these blobs should be deleted after e.g. 30-60 days, a much shorter delay compared to proposed one-year rotation times for execution payload history.”* ([EIP-4844](https://eips.ethereum.org/EIPS/eip-4844))

Moreover, when starting at a price of 1, once demand hits the target data price will go up multiplicatively every 12s until demand starts dropping; considering that rollup demand is inelastic at such low prices, **their costs will go up by 10 orders of magnitudes in a few hours. The 2022 FED rate hikes are a joke compared to this!**

### Cold-start problem

With the introduction of blobs we are bootstrapping a new market that will allow for price discovery and load balancing for blob data. As is always the case with new markets there is a cold-start problem, an initial phase in which we won’t have a strong market feedback and the fee mechanism will be in stand-by. This is even more relevant in our case because we are starting with a target much higher than current potential demand (even if all rollups were to switch overnight to blobs we will still be in oversupply).

Under the current setup, the analyses above highlighted a few problems:

(1) *cold-start phase will be long (1-1.5 years)*;

(2) *a price of 1 will incentivize spammy applications to use blobs*;

(3) *a price of 1 for an extended period of time will set wrong expectations*: rollups and other apps may make assumptions based on the low prices only to be driven out of the market or seeing their costs raise by orders of magnitude in a matter of hours.

### Wat do?

### Idea 1: set a higher minimum price

The price of 30e9 considered in analysis 2 above is in the order of magnitude of the minimum price of 10e9 that was suggested in the [EIP PR-5862 by Dankrad](https://github.com/ethereum/EIPs/pull/5862). **Setting such a minimum price will set correct expectations, disincentivize spam, and is a fair price at current conditions**. It will make the cold-start phase not shorter but less problematic and it can be easily updated down/removed as the market warms up.

The PR was subsequently closed after pushback based on the argument that if ETH value goes up 1000x that minimum price will be too expensive & we should not make a design decision that will require an update in the future. I believe this is not enough of a good reason to rebut the proposed choice. **We should weigh the benefits from having a higher `MIN_DATA_GASPRICE` during the cold-start phase with the cost of having to update this param in the future**.

Ethereum is not-yet-ossified and there are many design choices that will be upgraded in the coming months/years: from small things like the conversion rates of different opcodes to gas to bigger things like ePBS. Considering the planned changes this one seems rather small.

### Idea 2: set a lower block target for data gas

Another simple idea is to decrease the `TARGET_DATA_GAS_PER_BLOCK` to one blob per block. This is still ~5x higher than current load, it **will not solve spam and wrong-expectations in the cold start phase, but it will cut the cold start phase in half**.

It is a more cautious choice that can/will later be relaxed.

### Idea 3: do nothing

Doing nothing will maintain all the problems with cold-start highlighted above. Playing devils advocate, it is possible that spam use of blobs at low prices will self-correct and make the cold-start phase shorter. But there is uncertainty on if/when this will happen and also higher induced volatility on data gas price for L2 businesses.

### Open question

Should we consider changing the `DATA_GASPRICE_UPDATE_FRACTION` currently corresponding to a maximum multiplier of 12.5% like EIP-1559? This could be a forward-compatible and less controversial change. It will not solve the problems above but, if decreased, could provide more stable prices over time.

## Replies

**roberto-bayardo** (2023-03-17):

Thank you for the analysis and thought provoking discussion!  Some of my thoughts:

This analysis provides a lower bound on demand for blobspace more than an expectation.  If blob space is useful, other applications (or more rollups!) will start taking advantage of it. Cold start could thus be well less than your 1+ year estimate.

I’d love to better understand the impacts of spammy blobs, should they arise. Yes there is some network and storage cost associated with blobs, but with currently proposed parameters, how significant are these compared to all the other costs associated with running a node?

I would say there’s less elasticity in L1 data usage from rollups than other apps, not that the usage is inelastic. Usage is still elastic but the feedback loop might just be longer: if datagas prices spike on the L1, then L2 gas costs also spike, which can reduce tx volume and hence reduce data that needs to be posted to the L1.

This slower feedback loop might support your proposal of changing the DATA_GASPRICE_UPDATE_FRACTION to something more conservative. We already have a max blob limit to protect the network from saturation due to too many blobs, so an aggressive setting of the update fraction isn’t really needed to protect against short term spikes in demand. The max limit will just force pricing to fall back to a first-price like mechanism via 1559 priority fee while the base price adjusts.

---

**timbeiko** (2023-03-20):

FYI we discussed this on the [4844 implementers’ call](https://youtu.be/gdy5svsnFrM?t=405) (conversation starts @ 6:45).

---

**dcrapis** (2023-03-20):

ah, i was not aware it was happening today. would’ve loved to join the discussion. thanks for posting, let me respond here…

---

**dcrapis** (2023-03-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/roberto-bayardo/48/11591_2.png) roberto-bayardo:

> This analysis provides a lower bound on demand for blobspace more than an expectation

Right, I should’ve specified that with the initial price at 1 wei there is going to be much more demand for blobspace (as some other parts of the post argue).

![](https://ethresear.ch/user_avatar/ethresear.ch/roberto-bayardo/48/11591_2.png) roberto-bayardo:

> Usage is still elastic but the feedback loop might just be longer: if datagas prices spike on the L1, then L2 gas costs also spike, which can reduce tx volume and hence reduce data that needs to be posted to the L1.

Yes, that’s exactly what I had in mind. (This is actually a confusion due to the traditional use of the term inelastic in economics, used when elasticity of demand is small.) What I had in mind is that blob transaction demand volume is less elastic than generic transaction demand, not that elasticity is 0.

![](https://ethresear.ch/user_avatar/ethresear.ch/roberto-bayardo/48/11591_2.png) roberto-bayardo:

> This slower feedback loop might support your proposal of changing the DATA_GASPRICE_UPDATE_FRACTION to something more conservative. We already have a max blob limit to protect the network from saturation due to too many blobs, so an aggressive setting of the update fraction isn’t really needed to protect against short term spikes in demand.

Yes, I agree aggressive is not needed and is actually likely not desirable either. Especially because given the fact that demand being discretized into blob of fixed size gives it higher variance  (as [@kakia89](/u/kakia89) from Arbitrum points out in private conversation). We will investigate this further and update here.

---

**dcrapis** (2023-03-20):

Here are my takeaways from listening to the conversation:

There was a thorough discussion on pros/cons of increasing the minimum price.

- It was correctly noted that the “spam” maybe self-correcting as discussed in Idea 3, and that it is not a first-order concern given that we set conservative limit.
- @protolambda mentioned that he is more of a free market maxi but that he doesn’t see any reason in opposing a higher minimum price if well motivated. (Let me add that I agree, the minimum price is simply a feature of market design. I’m just exploring if setting it a bit higher may actually help the market reach the ultimate free market equilibrium more smoothly)

One thing that seemed to be overlooked in the discussion is the second “issue” that this analysis highlights. Beyond the length of the initial cold-start phase where the price will be at 1 wei, **the second “issue” highlighted is that (under current configuration) once demand hits the threshold the price might go up by 10^9x in a few hours**. Setting a higher minimum price would help mitigate this issue too, although there are other things that can help in the same direction as setting a less aggressive exponent (as discussed in previous reply).

---

**dankrad** (2023-03-20):

I’m quite skeptical of this analysis. Simply extrapolating the current usage of L2s, without taking into account that their cost will be massively reduced once blobs are introduced, seems fairly short sighted.

![](https://ethresear.ch/user_avatar/ethresear.ch/dcrapis/48/11293_2.png) dcrapis:

> In the worst case, this severe underpricing may lead to taproot-like usecases  that will inject instability in the blob-data market that is undesirable from a rollup-economics perspective (as the next sections clarify).

It seems to me that you have not made up on the promise to clarify what exact problems this instability will cause?

Either way, I do not expect pricing for rollups to be “stable”. Just like L1, the price of data for L2s will be volatile and based on demand. If there is a massive bull run or a big crises, a lot more transactions tend to be made, and I don’t think L2s will be isolated from that. So they will have to be able to cope with volatility in any case.

> their costs will go up by 10 orders of magnitudes in a few hours. The 2022 FED rate hikes are a joke compared to this!

Well this is wrong on several levels. First the basic cost per blob will never be as low as you seem to assume. At $1 per megabyte, it will be a no-brainer for some people to use Ethereum to share files or to make backups of data they consider important. NFTs will probably be ready to fork $100 per MB easily to store pictures. It’s hard to imagine blob prices ever being at the minimum pricing.

Second, you seem to imply this is some sort of catastrophic event, but it will still be very low prices. It doesn’t hurt me if my transaction costs go from 0.001 cents to 1 cent, both are within the real of “completely unnoticable” for me. So as long as they haven’t made huge mistakes in planning, this should not be a cause for concern.

> a price of 1 for an extended period of time will set wrong expectations: rollups and other apps may make assumptions based on the low prices only to be driven out of the market or seeing their costs raise by orders of magnitude in a matter of hours.

I also contend this, because 4844 is not a permanent solution. With data sharding we are planning to increase the amount of data availability 100-200x or so, and I certainly hope it launches within a timeframe of 1-2 years after 4844. So expecting data prices to be low should be the right bet in the long run, and there are good reasons for establishing this so that people build on secure Ethereum data rather than inventing less secure off-chain DA systems or use validiums etc.

---

**dcrapis** (2023-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Simply extrapolating the current usage of L2s, without taking into account that their cost will be massively reduced once blobs are introduced, seems fairly short sighted.

I mentioned in reply above that it should’ve been pointed out explicitly that the estimate is more of an upper bound. I also mentioned this dynamics in the section “Idea 3: do nothing”.

In any case, I want to remark that the main points that there will be a cold-start phase with low prices (granted, most likely shorter than stated) and that the price could go up very aggressively once demand reaches the target are valid.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Second, you seem to imply this is some sort of catastrophic event, but it will still be very low prices. It doesn’t hurt me if my transaction costs go from 0.001 cents to 1 cent, both are within the real of “completely unnoticable” for me. So as long as they haven’t made huge mistakes in planning, this should not be a cause for concern.

I contend this. I don’t want to sound catastrophic and should’ve probably refrained from the FED joke. I agree that the many order of magnitude increase is only on the data cost part which starts from very low prices. But the total cost may go from, say something like $2 to $10 per blob in a few hours. This seems a relevant impact on the cost structure of rollups.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> With data sharding we are planning to increase the amount of data availability 100-200x or so, and I certainly hope it launches within a timeframe of 1-2 years after 4844. So expecting data prices to be low should be the right bet in the long run, and there are good reasons for establishing this so that people build on secure Ethereum data rather than inventing less secure off-chain DA systems or use validiums etc.

This is a very important point and one where I fully agree. I admittedly did not consider this because I was less aware of expected timeline for data sharding.

---

**dankrad** (2023-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/dcrapis/48/11293_2.png) dcrapis:

> But the total cost may go from, say something like $2 to $10 per blob in a few hours. This seems a relevant impact on the cost structure of rollups.

I think $2 to $10 per blob is very cheap and to me, it seems likely that the equilibrium will be in that order of magnitude when blobs are used for non-rollup purposes, like JPEGs and stuff. You can make pretty nice NFTs at 10 kB/image and that would only cost $.20-$1 per NFT at that blob price.

An EVM rollup with no compression can include around 1000 transactions in a data blob, so at your suggested price it would be $.002 to $.01 per transaction. Rollups with compression will probably be about 10x cheaper than that. For most human-initiated transactions, this will probably be an insignificant cost (the opportunity cost of thinking about and approving a transaction tends to be higher at these costs). I expect costs can probably go 10x higher than that before they significantly impact rollup price structure.

---

**kakia89** (2023-03-24):

Thank you, [@dcrapis](/u/dcrapis), for such an informative discussion. I want to make a suggestion regarding the open question of updating fraction (from now on referred as “the parameter”) modification. The following are few points which justify why lowering is a good idea and also suggesting some ideas to what value it can be lowered:

1. as Davide already mentioned, discrete nature of blobs suggest the variance in the base fee change will be higher, compared to the continuous gas market. Therefore, lowering the parameter is a good idea.
2. as it was pointed out, both Arbitrum and Optimism (biggest rollups) post batches not every block. Therefore, for both of their sequencers, base fee change every time they post is much higher than if they were posting every block. If you consider the sequencers as users, and assume that 12.5% is the right constant updating base fee in the regular gas market, this already suggests we need to have lower parameter and even suggests what it might be. Let x denote the parameter. In the most conservative case, assuming batch posting is happening every third block, we should take (1+x)^3=1.125, which approximately solves x=0.04 (4%). In the average case, assuming batch posting is happening every fifth block, we should take (1+x)^5=1.125, approximately solving x=0.024 (2.4%). In the case of Arbitrum, batch posting is happening every 7 blocks, therefore, equation to solve is (1+x)^7=1.125, resulting in x=0.017 (1.7%).
3. Related to the above, it is always better for the rollup to have slower increasing base fees on the base layer. There are two reasons for this. The first one is rollup user fees, as the rollup data fees are reflected directly in them: for fairness reasons, we do not want rollup users that sent transactions close enough to pay very different fees. The second one is the way how the sequencer is compensated. In particular, ideally, the sequencer is not trusted by the protocol, and either there is some cost smoothening mechanism (as there is a delay between when the sequencer posts and when the protocol knows about the cost) or economic mechanism eliciting information from the sequencer. In both cases, lower parameter makes the compensation scheme easier and fairer.

All the points above suggest that lowering the parameter as much as possible is good, However, we may not want to decrease the parameter arbitrarily, as there are other (technical) requirements of having the target/maximal blob number and they may be violated if the high demand is persisting for long enough (i.e. we want exponential increase of the fee to catch up to lower the demand). There is probably a good explanation why these target and maximal values were chosen. Therefore, this consideration can be used as a lower bound how far the parameter is decreased.

---

**qizhou** (2023-03-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Well this is wrong on several levels. First the basic cost per blob will never be as low as you seem to assume. At $1 per megabyte, it will be a no-brainer for some people to use Ethereum to share files or to make backups of data they consider important. NFTs will probably be ready to fork $100 per MB easily to store pictures. It’s hard to imagine blob prices ever being at the minimum pricing.

Agree.  Currently, a lot of on-chain NFT projects such as Cyberbrokers, Nouns, Moonbirds, Artblocks already paid $10,000 per MB for the images on-chain (quick calculation: 1MB / 32 (sstore bytes) * 20000 (gas per sstore) * 10e9 (gas price) * 1500 (ETH price) ~ 10,000).  I will foresee if the price goes to $100 or $10 per MB, there will be much more demand from NFT projects (e.g., BAYC) to upload and store the data on-chain.  Further, with the reduced cost, there is also a possibility that we can upload the decentralized website contents (e.g., Uniswap/ENS frontend) or social media (mirror.xyz articles) on-chain (see an experiment we done with Vitalik’s blog https://www.reddit.com/r/ethereum/comments/107ok8e/upload_40mb_vitaliks_blog_to_a_smart_contract_on/).  One noticeable feature of this type of applications is that they are not time-sensitive - they can watch and wait until the `data_gasprice` drops to a level and submit the tx with BLOBs, thus potentially reducing the volatility of the price.

One key thing as [@dankrad](/u/dankrad) mentioned is that EIP-4844/Danksharding does not persist the data permanently.  This can be addressed by the proper token (ETH) storage incentive model with the on-chain discounted cash flow model (like Arweave) and proof of storage system (using L1 to verify).  See [EthStorage: Scaling Ethereum Storage via L2 and DA](https://ethresear.ch/t/ethstorage-scaling-ethereum-storage-via-l2-and-da/14223) for more discussion.

---

**dcrapis** (2023-03-28):

Thanks all for a very formative discussion.

It seems now clear that my main concerns with the cold-start phase have been vacated, in particular: incentivization through low prices will likely make cold-start phase relatively short; we are not worried about “spam” because as prices rise the low-value use cases will be priced out & moreover the impact of this on the system is transitory (since data is not persisted); finally, with data sharding capacity will be much higher so setting expectation of low prices is not a worry.

One thing that remains to be further explored in my mind is the question around update fraction param. As [@kakia89](/u/kakia89) points out in the reply above this has interaction with both L2 fees and L2 sequencer compensation/incentives.  We plan to further investigate this and send update here. If you have thoughts about this please chime in the discussion here.

---

**bkellerman** (2023-11-06):

I believe I’ve found a bug in the simulation notebook. It doesn’t change the overall findings, but results in even slightly *less* responsive data prices in this simulation.



      [github.com/dcrapis/blockchain-dynamic-pricing](https://github.com/dcrapis/blockchain-dynamic-pricing/issues/2)












####



        opened 09:21PM - 06 Nov 23 UTC



        [![](https://ethresear.ch/uploads/default/original/2X/6/649a383f9db44b4308f9a23aadc3151a3d946178.jpeg)
          bkellerman](https://github.com/bkellerman)










In `eip-4844-sim.ipynb` in the `build_block_from_data` function, there is a chec[…]()k before adding a blob tx to a block.

```
            if isinstance(tx, BlobTransaction) and utilized_data<=data_limit:
                included_transactions.append(tx)
                utilized += tx.gas_used
                utilized_data += tx.blob_hashes * constants["DATA_GAS_PER_BLOB"]
            elif isinstance(tx, BlobTransaction) and utilized_data>=data_limit:
                continue
            else:
                included_transactions.append(tx)
                utilized += tx.gas_used
```

This will add blobs when `utilized_data=data_limit`, so I suggest this be changed to

```
            if isinstance(tx, BlobTransaction):
                if tx.blob_hashes * constants["DATA_GAS_PER_BLOB"] + utilized_data<=data_limit:
                    included_transactions.append(tx)
                    utilized += tx.gas_used
                    utilized_data += tx.blob_hashes * constants["DATA_GAS_PER_BLOB"]
                elif isinstance(tx, BlobTransaction) and utilized_data>=data_limit:
                    continue
            else:
                included_transactions.append(tx)
                utilized += tx.gas_used
```

This does not appear to result in substantial difference in simulation output or findings.

---

**bkellerman** (2023-11-06):

I finally dug into EIP-4844 and see the base fee update rule is an integral-only version of a [PID Controller](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller)  operating on the data gas price in log space.

I’ll eventually post the derivation in the simulations I’m working on, but it somewhat trivially follows from [@dankrad](/u/dankrad)’s breakdown post.

Since this is an integral controller, the existing PID framework can possibly be applied to this problem.

Some things that come to mind.

-Integral-only controllers have a higher risk of oscillation than PI or PID controllers.

I think the risk of extreme oscillation is usually far-fetched in noisy, market environments.  However, since the majority of blob txs are expected to be consistently and programmatically produced by a small number of profit driven actors(more elastic demand…intelligent batching dependent on L1 fees), I think this risk should be considered when reducing the fraction of the existing mechanism. Would need to simulate this more to understand the risk.

-Proportional term

Adding a proportionate term to consider the *current* excess gas price and not just the history from the integral.  Discussed this briefly with [@barnabe](/u/barnabe) during 1559 research. A conservative P-term could help reduce risk of oscillation, while also making the controller more responsive.  There are well known constraints of the relationship between the strength of the P and I terms which depend upon a model of the process under control(data gas demand in this case). Again, would need to do more simulations of this process model.

One major complaint w/ EIP-1559 is how long it takes for the base fee to return to equilibrium after an impulse.  A P-term could potentially improve this w/ `data_gas_price` but also w/ `basefee` if it’s migrated to this new mechanism.

---

**Evan-Kim2028** (2024-01-05):

how do you get the transaction size calculations (in kb)?

---

**alex-damjanovic** (2024-01-26):

Hello [@bkellerman](/u/bkellerman)

Interesting take.

![](https://ethresear.ch/user_avatar/ethresear.ch/bkellerman/48/12964_2.png) bkellerman:

> Again, would need to do more simulations of this process model.

Do you have a status update on the simulations you were/are working on? If so I would love to take a look and collaborate on this. I feel like this is a feature that could be explored & discussed further.

Cheers

---

**kladkogex** (2024-01-29):

An interesting thing would be to model effect on the ETH mainnet gas price as L2 solutions start to move to EIP-4844

There will probably be a pretty significant deep in gas price

---

**alex-damjanovic** (2024-01-31):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> An interesting thing would be to model effect on the ETH mainnet gas price as L2 solutions start to move to EIP-4844

Is there a way we can see how much L2s influence the current pricing?

---

**bkellerman** (2024-02-07):

[@alex-damjanovic](/u/alex-damjanovic) yes, here is some progress.


      ![](https://ethresear.ch/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/w2s_nSM0SEqz3iEgnf_NSw)



    ![](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd231863ebeb783c60343a8e1e943178c5cb44c7_2_690x362.jpeg)

###

