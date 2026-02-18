---
source: magicians
topic_id: 2783
title: "EIP-1559: Fee market change for ETH 1.0 chain"
author: econoar
date: "2019-03-01"
category: EIPs
tags: [gas, eip-1559]
url: https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783
views: 126920
likes: 345
posts_count: 389
---

# EIP-1559: Fee market change for ETH 1.0 chain

Hi Everyone! ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=9)

I really think we should start discussion around this EIP. The current first auction fee market works but is extremely inefficient and a large UX barrier for adoption. This proposal introduces a fixed fee concept through the use of a MINFEE. Users can pay a premium over this if they want but in general it greatly simplifies the UX.

One great benefit of this EIP is because the MINFEE is burned and must be paid in Eth, we are making sure economic abstraction does not occur on the protocol level which is extremely important for long term Eth value.

One note I’ll make is while the current EIP mentions Eth 1.0, we should also consider it in the Eth 2.0 implementations.

I’d like for this to be considered for the Istanbul fork. What are general thoughts and concerns around this?

**Links**

[EIP-1559](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md)

[Ethresear.ch Post w/ Vitalik’s Paper](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838)

## Replies

**jpitts** (2019-03-01):

Thanks for bringing this up, I think it should get a lot more attention in light of the many efforts in the community to lower the barriers to entry for users.

---

**tvanepps** (2019-03-02):

On board with trying to get this into Istanbul and beyond. Let me know what can been done to help.

---

**arne9131** (2019-03-02):

In storage price section, you described the solution of charging timely rent fees. Do users need to pay expensive timely storage fees due to price fluctuation? Is there a more predictable way to know the cost?

Say, users can occupy storage proportional to the amount of ether they hold in their accounts. If I have 100 ether and total supply is 1000, I would be able to occupy 10% of the storage without any rent fees. If my balance reduces the occupied storage can be poked by other users.

---

**vbuterin** (2019-03-04):

> Do users need to pay expensive timely storage fees due to price fluctuation?

In the paper (page 14 of https://github.com/ethereum/research/raw/master/papers/pricing/ethpricing.pdf) I show how under full-blocks conditions, cryptocurrency price fluctuation is lower than txfee fluctuation, so denominating things as fixed fees denominated in cryptocurrency actually leads to *more* (fiat-denominated) price predictability than a market with bidding and a gas limit.

---

**fubuloubu** (2019-03-04):

One thought: if the “base fee” portion of the txn fee paid is burned, and the only portion that a miner/validator earns would be the “tip” above and beyond what is paid for the base fee, this means that we are net reducing the economic rewards that miner/validators earn (this should be obvious).

If we reduce the issuance reward portion of what miner/validators earn (as is planned for future block reward reductions in PoW and the rewards system in PoS), this reduces the incentive for the miner/validators to actually include transactions in a block (since they are getting paid regardless via inflation), meaning the total congestion goes down until txns with “tips” are included.

This may basically revert to the current auction-based fee model over time.

---

**econoar** (2019-03-04):

Yes, users will still have to pay some type of premium over the base but since we’re adjusting capacity based on demand, it’s assumed this premium will become constant over time and not be up/down like today. It essentially will settle on a fixed fee for miners.

---

**fubuloubu** (2019-03-04):

Not sure I follow. If the transactions included end up optimizing for the “tip” added to a transaction, then how have we not re-created the existing fee market, but worse because of this burning requirement?

---

**fubuloubu** (2019-03-04):

Also, a question on design mechanics (cross-posting here):

---

I think an applications of Controls Theory concepts is very interesting here. In order for it to work though, you have to identify a few things in the system: what are we optimizing for? what are our “control variables” (things we can control in the protocol)? what are our sensory inputs we can read (things we can observe)? how do we want to model the system we are controlling (the “plant”)?

There are tons of very interesting things that can be done, very simply and very effectively (especially since we have a TON of data to analyze about the current system), but applying controls theory works best when you go through the exercise of defining the system in the framework.

It might be good to start by modeling the existing system using a Controls Theory model (State Space or “classical”)

https://github.com/ethereum/EIPs/issues/1559#issuecomment-469340447

---

TL;DR: Marketplace design is an interesting application of Controls Theory

---

**econoar** (2019-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> then how have we not re-created the existing fee market, but worse because of this burning requirement?

The key is that base fee floats with demand and therefore is constantly moving the base cost to the user up and down based on block capacity. That is the hardest part of pricing today and what causes the inefficiencies.

It is extremely likely that just basefee plus some small tip will get you in the next block using this model. The market will settle on what this small tip “is” but I’d expect that to be a universal number and not one bid on.

---

**fubuloubu** (2019-03-04):

Ah, I see. So the key innovation here is to account for the variability in the fee paid by accounting for it within the block structure… and have that variability be burned. The remainder is theorized to be a large constant value corresponding to what the miner/validators wish to earn from rewards for processing transaction fees.

There may be some variability in the “tips” portion of the fee, but that should roughly correspond to the “speed” at which a user desires inclusion.

Can you walk us through an example such as front-running where the structure of the current fee market plays a large role?

---

**Daffy** (2019-03-04):

This is a GREAT solution to attrack new users and to take the frustation away from the current users!

---

**ciontude** (2019-03-04):

I find this proposal to be both very complex / hard to understand, and also to raise some issues with ecosystem security / inflation (Making inflation and ecosystem security much more difficult to approximate and evaluate).  In particular, any idea that involved the burning of fees would make EIP 960 impossible under any inflationary system like Eth 2.0

As an alternative proposal, how about leveraging miners own self-interests against eachother.  Ideally this approach becomes a drop in replacement when miners -> stakers.

To accomplish this, compare the minfee used/charged by a given block versus the <X=24> hour rolling average of minfees from blocks.  If the minfee of the block in question is lower than the X hour rolling average, apply a bonus of 0-5% to the miner’s reward depending on the size of the decrease.  If the minfee of the block in question is higher than the 24-hour rolling average (AKA, either demand is spiking or a miner is attempting to increase their own minfee ala the graph in Vitalik’s paper), apply a penalty of 0-5% to the miner’s reward depending on the size of the decrease.

In this way, miners are incentivized to take action that benefits the long-term ecosystem (Lower fees, more adoption, but not unconstrained spam) without changing the way gaslimits can be adjusted in response to raw increased adoption & demand.  Miners who proactively reduce fees gain small benefit; Miners who attempt to push the minimum fee up to earn more profit pay a penalty, and should only do so when the demand is truly sufficient to justify the penalty.  Miners maintaining the status quo see no change.

To prevent abuse / exploitation, these steps and penalties/rewards can be capped, i.e., preventing miners from doing 4 bonus “down” fee steps for a 5% bonus each time followed by a very large 20% “up” step to counterbalance for a single 5% penalty.

---

**ciontude** (2019-03-04):

Doesn’t this system also put the onus on developers to hardfork to adjust the maximum blocksize when actual adoption of the ecosystem requires scaling blocks up to maintain reasonable fees for extant usecases?

How is TARGET_GASUSED adjusted?  Is there no more visibility into it between miners?

---

**veox** (2019-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/econoar/48/1641_2.png) econoar:

> It is extremely likely that just basefee plus some small tip will get you in the next block using this model.

I think this statement mis-frames the inclusion criteria. Here’s a mirror image:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> It is extremely unlikely that a transaction will be included until basefee falls so low that the tip is significant.

I still fail to see how “just `basefee` plus some small `tip`” would translate to lower net-wide fee variance (when comparing periods of low/high demand for gas). And, more importantly, that average `basefee+tip` would ever be lower than the current average `fee`. As [@fubuloubu](/u/fubuloubu) wrote:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> If the transactions included end up optimizing for the “tip” added to a transaction, then how have we not re-created the existing fee market, but worse because of this burning requirement?

(I’ve heard this being mentioned at the rumour mill, that “~~EIP-1559~~ issue 1559 === cheaper transactions”; not in this thread yet.)

---

The trade-off for the miner is currently between `block_reward+fees` and `ommer_block_reward`.

In the proposed scheme, it would be between `block_reward+tips` and `ommer_block_reward`.

Miners include transactions in blocks based on the marginal profit increase they would get, offset by the chance that the block would become an ommer. Currently, fees rarely make 5% of base block reward. (This was <3% before the most recent issuance reduction; sorry I can’t link a chart: the numbers are from anecdotal personal observation.)

Let’s generously assume that the average fees per block are, in fact, 5% of the base block reward (that is, they are 0.1 ETH and 2.0 ETH, respectively). So, miners have to weigh this 5% extra gain at probability `P` against a 12.5% loss (at best! 25% for 2-block-old ommer) at probability `1-P`. The profitability condition is:

```auto
0.05 * P >  0.125 * (1 - P)
       P >~ 0.714
0.05 * P >  0.25 * (1 - P)
       P >~ 0.833
...
   F * P > U * (1 - P)  # F: extra profit percentage when getting Fees
       P > U / (F + U)  # U: loss percentage due to becoming Uncle
```

Back to what I started with: I fail to see how lowering user-born fees (and by necessity lowering `F`, since `F` is the `tips` part in `basefees+tips`, and ostensibly `basefees+tips < fees`…) will result in anything but the miners becoming reluctant to include transactions.

It’s reasonable to expect the opposite: average `basefees+tips` under this proposal will be higher than average current `fees`.

(There! It’s out of the way now.)

---

The scheme further breaks down in times of “congestion”; that being a descriptor for increased average uncle rate: an ever-larger proportion of hashing power contributing to “security of the chain”, but not (i.e.: at the expense of) transaction throughput.

During congestion, when relatively many ommer solutions are available, miners:

- routinely have the option to include ommer references in their blocks - because, hey, they keep popping up!; and
- are increasingly pressed to drop transactions altogether - because “no compute” is much faster to process than the “much compute” blocks from the competition (ones that would do well to get out of the way and become ommers…).

Transactions are now in competition with uncles; in particular, the highly-priced transactions (that tend to catch the eye and prompt *“congestion!.. congestion!..”*). If they can’t “outbid” the inclusion of an uncle (adjusted for the risk of the block itself becoming an ommer!), then it is not rational for miners to include transactions instead of ommers.

This is not specific to the proposed scheme, but is also the state of affairs currently (and manifested mildly in late 2017 and early 2018, I believe).

As noted in the [github issue 1559 summary](https://github.com/ethereum/EIPs/issues/1559#issue-377994505):

> If a transaction sender highly values urgency during conditions of congestion, they are free to instead set a much higher premium and effectively bid in the traditional first-price-auction style.

In other words, during congestion, the proposed scheme devolves (at best!) to the current auction mechanism. All good here, except the “at best” part: see previous section.

---

Somewhat OT: I am against lowering user-born transaction fees wholesale, until a “state fees” portion is introduced to them.

Any scheme that claims to lower user-born fees needs to consider that state expansion gets *this* much faster when user-born fees are *that* much lower. The cost is now born by someone else than the users, but they are not gone.

That said, I do appreciate burning a portion of ether, as a means to balance (counter-act) newly-minted ether.

---

Finally: having both a `gasprice_tip` (per-gas-unit, in shannons) and `cap` (per-whole-tx, in ether), where

- gasprice_tip * gas_limit <= cap;
- basefee <= gasprice_tip * gas_limit;
- basefee <= cap.

… will be a nightmare for UX; and will most likely devolve into `basefee <= cap` as far as wallet interfaces are concerned, with `gasprice_tip` abstracted away as a percentage of `cap`…

---

**vbuterin** (2019-03-05):

> If the transactions included end up optimizing for the “tip” added to a transaction, then how have we not re-created the existing fee market, but worse because of this burning requirement?

Currently, a miner has two reasons NOT to include a transaction:

1. Opportunity cost (ie. other transactions)
2. Increased uncle rate risk

(2) is predictable, (1) is unpredictable. This proposal brings (1) out of the equation, so we should expect miners to be satisfied by a constant level of `tip` even as `basefee` fluctuates.

> will result in anything but the miners becoming reluctant to include transactions.

We can actually calculate the size of this the marginal uncle rate risk (ie. increase in change your block becomes an uncle from including an additional 1 million gas in a block).

The thing we would do before is run a linear regression of gas usage vs uncle rate data [here](https://www.etherchain.org/correlations) to see what the marginal risk of being uncled is if you add more than 1 million gas. Unfortunately, this is temporarily complicated because we recently upgraded network block propagation, and there’s still relatively little data post-change. So what we can do is use the formula `U = (k1 + k2 * G) / T` where `U` is uncle rate, `T` is block time and `G` is gas usage of a block (see [Decker and Wattenhofer 2013](http://www.gsd.inesc-id.pt/~ler/docencia/rcs1314/papers/P2P2013_041.pdf) for some of the arguments that lead to this). We have a natural experiment in Constantinople bringing `T` down, so we can use [block](https://etherscan.io/chart/blocks), [uncle](https://etherscan.io/chart/uncles) and [gas usage](https://www.etherchain.org/charts/blockGasUsage) before and after the fork. Before we had 220 uncles and 4200 blocks per day, so `U_pre = 0.0523`, after we have 500 uncles and 6400 blocks per day, so `U_post = 0.078`. Block time = 86400 / blocks per day, so we get `T_pre = 20.57` and `T_post = 13.5`. `G_pre = 7.5m`, `G_post = 6.2m` (see [here](https://www.etherchain.org/charts/blockGasUsage)). So we get:

```
0.078 = (k1 + k2 * 6.2m) / 13.5
0.0523 = (k1 + k2 * 7.5m) / 20.57
```

[Solving](https://www.wolframalpha.com/input/?i=solve+(k1+%2B+k2+*+6200000)+%2F+13.5+%3D+0.078,++(k1+%2B+k2+*+7500000)+%2F+20.57+%3D+0.0523) the linear system gives:

```
k1 = 0.944
k2 = 0.0175 * 10**-6
```

To get an incremental uncle rate per million gas, you would need to divide `k2` by the block time (13.5) so you get 0.0013 per million gas. Another way to see how `k2` is tiny is that a 2/3x reduction in block time leads to a 3/2x increase in uncle rate, showing that “base” (ie. not usage-dependent) uncle rate by itself explains almost all of the uncle rate.

If you enter `x=AVG_BLOCK_UTIL` and `y=UNCLE_RATE` in [etherchain’s correlation utility](https://www.etherchain.org/correlations)  and set the date to Jan 16 (first Constantinople attempt, which is what forced everyone to update), you can see the line doesn’t slope up quickly at all.

Note that as an absolute upper limit, marginal uncle rate risk is 0.01 per million gas, because that’s what it would be if *all* of the current uncle rate were explainable by the `k2 * G` term. So we have two estimates for marginal uncle rate risk: 0.0013 per million (aggressive) and 0.01 per million (maximally conservative).

We can compute the expected loss to a miner of including a transaction via `U' * (R_B - R_U)` (marginal uncle rate risk * block reward minus uncle reward). The [average uncle reward](https://etherscan.io/uncles) is ~1.67 (note that this means that most uncles are getting the full 7/8 reward; a year ago this was *not* true, which is part of why a year ago many miners were not including blocks). So `R_B = 2`, `R_U = 1.67` and `U' = 0.0013` per million gas, so expected loss per million gas is 0.000433 ETH (or 0.433 gwei per gas). Under conservative estimates this goes up to 3.33 gwei per gas.

**TLDR: the disincentive that miners have against including txs is currently already quite low, somewhere between 0.4 and 3.3 gwei, which is only a small portion of transaction fees seen today.**

---

**vbuterin** (2019-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> In other words, during congestion, the proposed scheme devolves (at best!) to the current auction mechanism.

This actually depends on how long you’re willing to wait. If you absolutely need a tx included in the next block, then yes in sudden demand spikes it can temporarily degrade to a first price auction, but if you’re willing to wait ~10 blocks, then it works like an ascending price auction (ie. it’s efficient).

---

**veox** (2019-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> The thing we would do before is run a linear regression of gas usage vs uncle rate data

Quick note: ideally, we’d run that with gas usage from the uncle blocks, not the “canonical” blocks that included the uncles. Etherchain’s correlations page provides the latter.

This works with the assumption that blocks become uncles not because of the particular transaction inclusion strategy used to construct them, but because of other factors, which can be summed up as “random luck” (the worst there is ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)).

It’s probably hard to prove one way or another with real historic ommers (which are not guaranteed to be available), so IMO this is an OK assumption to roll with (until proven otherwise, e.g. by intentionally seeking out missing ommers over `devp2p` ASAP, and comparing them to the nephews *as classes*).

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> the disincentive that miners have against including txs is currently already quite low, somewhere between 0.4 and 3.3 gwei, which is only a small portion of transaction fees seen today.

That is 0.4 to 3.3 gwei per gas, and it is *not* insignificant. (In fact, this is the gas price range I most often use…)

Gitcoin’s [gas history breakdown](https://gitcoin.co/gas/history?breakdown=weekly) shows “gas price needed to confirm within 3 hours” to fall most of the time *within* that range, and “gas price need to confirm within 1 minute” skipping off of the 3.5 mark (or so).

Even using [Etherscan’s average gas price chart](https://etherscan.io/chart/gasprice) (which shows y-day’s as 13.5 shannon), the difference is only around one order of magnitude. This, I feel, is not a good chart/metric to use; what is needed here is a breakdown by gas price ranges over time; something like [Johoe’s Bitcoin Mempool charts](https://jochen-hoenicke.de/queue/#0,24h), but for Ethereum main-line blocks. *Then* we could see how much of the gas used falls into the 0.4-3.3 gas price range (or, more prudently, recalculate this gas price range for each time period in question), where miners are taking an ever-more-guaranteed risk, “out of the kindness of their heart”.

---

P.S. I’ve gotten OT, I think. Sorry for that.

---

**vbuterin** (2019-03-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> That is 0.4 to 3.3 gwei per gas, and it is not insignificant. (In fact, this is the gas price range I most often use…)

Oh I agree it’s not insignificant! But what you need to keep in mind is that, in an economic sense, the BASEFEE and the TIP are **NOT** additive. To see why, imagine that following two facts are true:

- The fee level at which there is 8 million gas of demand per block is, in some particular span of time, 5 gwei
- Miners value the cost of including 1 gas worth of transactions at 1 gwei

Clearly, no miner will accept a transaction with a tip of less than 1 gwei, and let’s say there’s a bit of monopoly power added on top so miners on average only accept transactions with tips of 1.5 gwei. Suppose the BASEFEE starts off at 1 gwei. Users would have to pay only 2.5 gwei total, so demand is higher than 8 million; hence, blocks are more than 50% full, and the BASEFEE rises. Eventually, when the BASEFEE reaches 3.5 gwei (NOT 5 gwei!), users have to pay 5 gwei total, and at that point demand is equal to 8 million, so the BASEFEE reaches an equilibrium.

The one special case is the case where the equilibrium fee is less than the tip that miners demand. In this case, the BASEFEE would fall to zero and blocks would just be less than 50% full until demand rises again. But notice that in this situation, the current system would have the same consequence.

---

**tvanepps** (2019-04-02):

Hey Vitalik - will you or [@econoar](/u/econoar) be able to present this at the Berlin Istanbul / 1.x meeting the 17th and 18th? Trying to get either of you confirmed if you will be presenting remote.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)
    [Istanbul & ETH1x Roadmap Planning Meeting - April 17th & 18th in Berlin](https://ethereum-magicians.org/t/istanbul-eth1x-roadmap-planning-meeting-april-17th-18th-in-berlin/2899) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)



> The discussion that started in January has resulted in a meeting being planned for April 17th & 18th in Berlin.
> The dates are confirmed so please feel free to book travel. There may be a reception on the evening of the 16th or other shoulder events, but nothing else is confirmed.
> The goals are:
>
> discuss process & timing of Istanbul hardfork – EIP233 improvements, security, testing
> discuss various multi-hardfork plans such as state fees, eWASM, EVM evolution
> presentations from technical expert…

---

**vbuterin** (2019-04-02):

I will unfortunately have to present remotely; it’s too close to EthCapetown for me to fly in personally. But will be very happy to do be around on call for as long as needed.


*(368 more replies not shown)*
