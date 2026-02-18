---
source: magicians
topic_id: 23884
title: "EIP-7938: Exponential Gas Limit Increase via Default Client Voting Behavior"
author: dankrad
date: "2025-04-27"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7938-exponential-gas-limit-increase-via-default-client-voting-behavior/23884
views: 4145
likes: 58
posts_count: 30
---

# EIP-7938: Exponential Gas Limit Increase via Default Client Voting Behavior

Discussion topic for [EIP-7938](https://eips.ethereum.org/EIPS/eip-7938)

## Replies

**totmacher** (2025-04-27):

Is the intention here to force driving towards an end goal of gas limit related delivery, kind of like how Muir glacier would make the difficulty bomb adjustment?

---

**benaadams** (2025-04-28):

Is the change schedule too fast? (Not target)

If block size increases every epoch (6.4 mins); will it constantly be front running demand and not letting it adjust and catch up causing a continuous precipitous gas price drop?

For example would it be better to make the increase every 30 days (monthly) or 90 days (quarterly)

---

**MicahZoltu** (2025-04-28):

It feels like this should be a function of epoch time, not a function of number of epochs alone.  There have been discussions of decreasing block times and depending on how that is implemented, that could result in a change in epoch length.  If this algorithm is a function of epoch count alone, then it could end up accelerating towards its target too quickly.

---

**MicahZoltu** (2025-04-28):

If the network can handle X gas per block today, then gas limits should be set to that.  We should not assume that future handling of gas is a given and we should only increase the gas limit *after* clients can handle such an increase.  We should not be increasing the gas limit optimistically based on an assumption that things will get better in the future.

---

If my math is correct, a 100x increase in gas limit would increase the worst case scenario of state growth to 14TB/year (up from 140GB/year).  As gas prices decrease (due to abundance of space), the probability of people using Ethereum primarily for storage may go up, so we may trend towards worst case scenario as storage is often more valuable than computation once both are sufficiently cheap.  Math listed below so others can double check my numbers.

This level of state growth is unsustainable, even if we assume users are running nodes on dedicated custom build hardware.  There are things in the works like Portal Network to try to reduce the state growth problem, but none are in production yet so we cannot yet rely on them for addressing this problem.

```auto
gas_per_block = 3,600,000,000
blocks_per_minute = 5
gas_per_year = 9,460,800,000,000,000
gas_per_slot = 20,000
bytes_per_slot = 32
bytes_per_year = 15,137,280,000,000
terabytes_per_year = 14
```

---

**CPerezz** (2025-04-28):

One of the things I thought would be interesting and useful for this proposal is to bump-up state growth rates in [Surge’s Perfnet](https://github.com/NethermindEth/surge) and see how it actually handles it. Thus, we can anticipate when clients will need to “upgrade hardware” (SSD → NVME M.2 (PCIE)) or when implementations simply can’t handle the state anymore and break. Thus allowing us to fix it in advance.

This would increase the certainty on state-growth metrics and expectations for the next 4 years.

And allow us to regulate gar_limit growth rates according to our predictions if needed.

I’m already working on an integration of the tool within [spamoor](https://github.com/ethpandaops/tooling-wishlist/blob/master/open-ideas/state-growth-spammer.md) so that we have something easy to use to take such measurements.

---

**TimDaub** (2025-04-28):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/7/78578175254abf6b18704288df9f07f8dde60325_2_690x381.jpeg)image2148×1188 138 KB](https://ethereum-magicians.org/uploads/default/78578175254abf6b18704288df9f07f8dde60325)

EIP doesn’t include a motivation on why we should increase the gas limit. Can you please add this to the EIP?

As for the motivation to reject the EIP, since it is lacking a motivation to counter: Gas pricing would tell us that the L1 isn’t used fully and so why would we want a speculative gas limit increase?

---

**eccentricexit** (2025-04-28):

Hit the nail on the head.

Not to mention that compared to blobs, bumping gas limits is a contentious change and has a much lower bang for the buck.

---

**dankrad** (2025-04-28):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> It feels like this should be a function of epoch time, not a function of number of epochs alone. There have been discussions of decreasing block times and depending on how that is implemented, that could result in a change in epoch length. If this algorithm is a function of epoch count alone, then it could end up accelerating towards its target too quickly.

If we change the slot time, we would also have to change the gas limit (as what we are really targeting is a gas limit per unit of time, not block). I think it’s ok to update this schedule with such a change.

---

**0xBreadguy** (2025-04-28):

It’s a signal towards application builders that there is a future which encompasses scale to handle their growth.

Teams have left mainnet to this point because they were told “mainnet isn’t your home.”

Low gas prices on mainnet today should not be used as an excuse to not push to make the chain more inhabitable for applications and users.

---

**dankrad** (2025-04-28):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> If the network can handle X gas per block today, then gas limits should be set to that. We should not assume that future handling of gas is a given and we should only increase the gas limit after clients can handle such an increase.

There is no exact, hard limit of how much the network can handle. There is currently no reason to believe what is proposed here poses direct safety issues: https://x.com/notnotstorm/status/1915439259630317995

The purpose of having a schedule is to give applications predictability, and make us solve performance issues as a priority. A lot of what needs to be done is performance engineering; you cannot do this well without understanding what the end goal is.

We also have a strong pipeline of changes that will make this a reality. I think we should commit with the end goal in mind, rather what we have been doing so far, which has led to stagnation of the Ethereum network (e.g. still no DA scaling today, more than 5 years after the rollup-centric roadmap became the goal). I think it’s time to shake things up a little.

---

**TimDaub** (2025-04-28):

As long as these arguments are not included in the EIP you are just hallucinating what you personally feel are the motivations for Dankrad to propose the EIP. Not meant as an offense ofc, but this is just structurally what can be observed.

Btw. I also don’t think it is enough for [@dankrad](/u/dankrad) himself to state in the comments here or elsewhere what his motivation is for submitting. This has to be part of the EIP IMO. Otherwise Twitter etc. is going to front run the EIP with strawmans

---

**dankrad** (2025-04-30):

Writing more about the reasons for this EIP. To be upfront, it is unconventional. I do think it is time for being unconventional, because the current way of doing things is likely to make Ethereum irrelevant over the next 5-10 years.

Key considerations why I think we should commit to this gas limit change schedule:

1. Strategic: Things happening on one layer (composability and UX-wise) is much more strategically important than previously thought.
2. Technical: Validity proving Ethereum L1 at 1-block latency will become possible this year, and DAS with PeerDAS will also become reality
3. Execution: Working backwards from a goal tends to have better outcomes than making incremental changes as they become possible.

## 1. Strategic

Ethereum L1 needs to be the economic center of Ethereum. There are a number of reasons for this:

- Ethereum L1 will probably always drive fee revenue, as the moat for DA is much lower
- If L1 is unimportant and loses its attraction of liquidity and DeFi, there will also be less of a reason for L2s to even remain attached to Ethereum
- The Ethereum ecosystem does compete with other ecosystems, who are eager to get its market share. Fragmenting L1 liquidity across a number of different L2s is a very good way to lose this battle

## 2. Technical

In the last year, proving Ethereum L1 blocks became first possible, and is now cheap (typical proof cost per block is a few cents: https://ethproofs.org/). Within this year, we will have proving within a single slot delay, and all teams expect order of magnitude improvements to continue for at least a few years.

This means that for the first time, we will have the ability to significantly scale the L1 so that a lot of activity can continue to happen on it. Not just just do 10x the scale, we can do 100x to 1000x the current scale while keeping Ethereum’s most important properties:

- Verifiability (it is very easy to check that the current continuation of the blockchain is according to the rules)
- Censorship resistance (we can guarantee that any paying transaction will get included)

Ethereum’s current node architecture is a copy of Bitcoin’s from 2009. We will need to update the Ethereum node types for the 2020s and 2030s. Some roles (full nodes, attesting, FOCIL) are likely to be even lighter than they are today, while others (building, proving) will become more beefy; however, all the “beefy” node types come with an 1-out-of-n honesty assumption, making sure that they can always be easily replaced.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/6/68b979e3cd6c80355442d61c13f1b6327b93f16d_2_690x397.jpeg)image1738×1001 151 KB](https://ethereum-magicians.org/uploads/default/68b979e3cd6c80355442d61c13f1b6327b93f16d)

Barnabe discusses his vision for different node types more on this call (https://www.youtube.com/live/m5HFO4DYckQ?si=4fD0Z7PkJM-4pBpX).  The key to maintaining security and keeping Ethereum unstoppable that all node types can still be run from home in some places.

## 3. Execution

In the past, we have been very reluctant to do certain things:

- Commit to timelines
- Plan actively for the future, several forks ahead
- Execute efficiently

Committing to a scaling timeline makes it clear what the goal is, and lets us plan backward from the goal:

- Most critical upgrades for Glamsterdam:

Delayed Execution
- Shorter slot times
- Aggressive history expiry

L1 scaling upgrades over the next 2 years:

- Block-level access lists + parallel execution
- Network-level erasure coding for execution blocks

Rollout of full zkEVM

- Optional (this year) and then enshrined zkEVM proving (ca. 2 years)
- Execution payload in blobs (to use DAS) (might be combined with network level erasure coding)
- FOCIL to ensure continued censorship resistance

In addition to hard forks, scaling the EL 100x will require performance engineering. Having a concrete goal in mind will let us prioritize this work as well as the concrete upgrades as needed. A database for a 5x scaled EL might look very different from one that is scaled to 100x. The mempool certainly does. A lot of decisions become much easier if we know where we want to go.

The same goes for application developers. Ethereum L1 is currently still the home for DeFi – this might not be true for much longer if we don’t start strongly supporting applications. An important step in this direction is giving them dependable scaling timelines.

## Doesn’t that make us like a Datacenter chain or Solana?

I think it is irrelevant whether some superficial aspects of Ethereum look more like Solana or not. The core value proposition of Ethereum is not the home staker, it is verifiability and censorship resistance. While the future world looks significantly different from now, I would argue it’s not clearly better or worse in those aspects, just a different set of tradeoffs. 99%+ of users today do not run their own node but use their wallet’s default RPC. Having ZK verifiability will actually make it easier (obviously it’s still going to be hard work getting it integrated into wallets). FOCIL or MCP can probably bring us better censorship resistance than we have today.

Another question might be – are we playing Solana’s game? Why should we IBRL, aren’t we certain to lose this?

I think it is not so certain we will lose this game. Ethereum L1 so far has the most liquidity of all chains. Why is it still here?

- Existing DeFi moat
- IBRL is not the only thing that matters
At least as far as scaling is concerned, I do believe that at 100x the current scale, Ethereum L1 can support a very large range of value transaction that competing with it simply on scaling terms is not and interesting game to play anymore. On shorter block times, I think we are unlikely to go below ca. 1s to change proposers, but there are other options to improve UX (preconirmations) and DEX performance (MCPs).

Uniquely, Ethereum has a huge moat in DeFi liquidity, and those applications benefit significantly from being colocated. What we need to do is support these applications and making Ethereum the best home to them.

## Conclusion

Due to these updates to the strategic and technical environments, I think by far the best strategy for Ethereum from here is, in addition to supporting L2s via blob scaling and UX/interop improvements, to significantly scale the L1. The endgame is scaling 100x-1000x. We need to commit to it as soon as possible, both because builders and applications need predictability, and because we need to prioritize properly so that it can actually get executed.

---

**MicahZoltu** (2025-04-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> If L1 is unimportant and loses its attraction of liquidity and DeFi, there will also be less of a reason for L2s to even remain attached to Ethereum

Why do we want/need L2s to be attracted to Ethereum?  What is the problem if some L2s decide to build on Polkadot, Celestia, Solana, etc.?  What harm is caused to Ethereum in such a world where that happens sometimes (but not all the time)?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> The Ethereum ecosystem does compete with other ecosystems

I would like to see this reasoned out more thoroughly.  Why does Ethereum need to compete with other ecosystems?  What axis does it need to compete on?  All of them, or is a particular niche sufficient?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> Technical

This section talks about why you think we can get away with a gas increase, but it doesn’t really speak to the motivation for why we need an increase, or more importantly why we need a gas increase right now.  When you integrate all of this into the EIP’s motivation, I recommend leaving this part out or changing it significantly.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> Committing to a scaling timeline makes it clear what the goal is, and lets us plan backward from the goal:

We can have a goal and work towards it without also counting our chickens before they hatch.  We can say that we want to increase gas limits, and outline a roadmap that will enable us to do so, but wait to actually raise the gas limits until such time as those roadmap items are complete.  If the goal of this strategy is to try to force our future hands, then I think that should be stated very clearly in the motivation section without beating around the bush.

---

**green** (2025-04-30):

I was writing a reply on this thread with other ideas of how to “Increase the Gas Limit”, but ended up using it as the response of a different thread. Still related though: [Formalizing decentralization goals in the context of larger L1 gaslimits and 2020s-era tech - #18 by green](https://ethereum-magicians.org/t/formalizing-decentralization-goals-in-the-context-of-larger-l1-gaslimits-and-2020s-era-tech/23942/18)

---

**Giulio2002** (2025-04-30):

I’m glad this is no longer a taboo topic and that we can discuss it seriously.

I agree with almost everything you’ve said: Ethereum does have competitors, and it needs to make strategic decisions to maintain its status as the world computer. I also believe Ethereum wasn’t built around home stakers—they were simply a “nice” side effect of The Merge. However, maintaining that narrative is costly, so dropping home stakers seems like the right compromise.

That said, a 100× improvement strikes me as unrealistic. A 10–20× gain (around 300 TPS) feels more attainable. The challenges are largely engineering-driven: so far, only Erigon has been engineered to handle state growth without breaking RPCs or write throughput. To hit 100×, you’d first need to shift engineering priorities across many teams (including ours—we do have performance gaps in some areas, though I’m comfortable with them given our core goals). Second, you’d require multi-order-of-magnitude “L1 scaling” upgrades, and we have no history of handling more than a single order of magnitude. That said, I could certainly be proven wrong.

I need to do some research in how you plan to achieve a 100x still. Nonetheless, I think it is doable on perhaps a larger time horizon (say 6 years)

---

**Sirmoremoney** (2025-05-01):

You dropped this Sir ![:crown:](https://ethereum-magicians.org/images/emoji/twitter/crown.png?v=12)

As correctly pointed out, if ethereum remains anticompetitive, we will be the Nokia of blockchains in 1-2 years.

It is already happening. We completely lose our relevance if we don’t dramatically change.

I also appreciate the top-down approach to scaling the L1. Setting the goal to scale 100-1000x then planning and executing to make it happen.

---

**Stoff81** (2025-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/giulio2002/48/11035_2.png) Giulio2002:

> I’m glad this is no longer a taboo topic and that we can discuss it seriously.

Why has it been taboo till now? What are the “downsides” of increasing gas limit. Is it just state size?

So this proposal is looking to add state size (ie node HDs) to drive better economic incentives generated from fees. These fees are captured by node operators.

---

**Ariiellus** (2025-05-01):

Today home stakers (soon home builders) can run on 2TB but many people recommend starting with 4TB.

This means that home stakers could be affected pretty soon?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> gas limit would increase the worst case scenario of state growth to 14TB/year (up from 140GB/year).

Or will they need to prune their nodes constantly in order to not run out of storage? (increasing bad UX for NO). Also, this will impact in the minimum bandwidth necessary.

I’m agree on L1 being the economic center on Ethereum but this proposal feels that is leaving some aspects out of the table and seeing only one side of the moon.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dankrad/48/2962_2.png) dankrad:

> Fragmenting L1 liquidity across a number of different L2s is a very good way to lose this battle

If the goal is to get back to mainnet and drop the rollup-centric roadmap, then why keep pushing the intents framework / interoperability efforts? Let’s not start a new battle front inside our barracks.

Solving the L1/L2 liquidity fragmentation UI/UX will increase the MOAT for eth eco.

---

**MicahZoltu** (2025-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ariiellus/48/15146_2.png) Ariiellus:

> they need to prune their nodes constantly in order to not run out of storage?

The upper limit of 14TB/year I quoted was actual state, assuming you are running completely pruned with no overhead.

In reality it is quite unlikely that 100% of gas is spent on storage, but on the flip side there is also a significant amount of overhead beyond the raw state (like old state if you don’t prune instantly, the supporting data structures, indexes, etc.)

---

**Pmatt328** (2025-05-02):

As home staker, I totally and fully support this!

we are late but better starting now that never


*(9 more replies not shown)*
