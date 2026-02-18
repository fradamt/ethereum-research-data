---
source: ethresearch
topic_id: 10320
title: Gradual sharding rollout?
author: Polynya
date: "2021-08-13"
category: Economics
tags: []
url: https://ethresear.ch/t/gradual-sharding-rollout/10320
views: 2904
likes: 2
posts_count: 9
---

# Gradual sharding rollout?

A couple of us community members on r/ethfinance (I’m u/Liberosist on Reddit) have been discussing the economic impacts of data shards. Starting with 64 shards made a lot of sense back when the plan was data first, but execution the final goal, and before EIP-1559, rollups, and the rollup-centric roadmap existed. So, are 64 shards still the best starting point? I don’t know, but worth a discussion here.

As per current specifications, the Ethereum network will see a significant positive supply shock with ~18x greater data availability overnight. That is, assuming all transactions on the execution layer is data - realistically the difference will be even greater as there’ll likely be other compute-heavy transactions on the execution layer, limiting space for rollup data; while shards are exclusively data. There are other factors at play - perhaps the execution layer’s block gas limit will be higher than it is now, but you get the idea - it’s an order of magnitude or greater.

Rollups will be well incentivized publish their data to shards immediately, and potentially the shard builder / proposer separation will make this transition even simpler. An order of magnitude is a significant shock, and has the potential to cause short-term instability in already volatile fee markets. With EIP-1559, and shards implementing 1559-like mechanisms, Ethereum’s security is now intrinsically tied to fee markets. Over the long term, I fully believe demand will be induced, an equilibrium will be found in the fee markets, and the additional data availability will be saturated by rollups.

What if… we started off with, as an arbitrary example, 16 shards with 124 kB. This is 1/8th the current specifications, but still a significant 2.25x bump over execution layer’s theoretical max data availability. As this is saturated, more shards and/or larger shards can be deployed incrementally.

I could be missing something technical, but my intuition is that this also means lower technical risk for this new system. I understand the protocol upgrade risk to expand data availability later, of course, so there’s a trade-off there.

Finally, I’ll address that the transition to rollups is quite gradual anyway. We’ve had application-specific rollups slowly gaining adoption over a year and a half now. Both Offchain Labs and Optimism are taking a measured approach starting off with rate limits, and incrementally increasing them over time. Infrastructure (CEX withdrawals/deposits, wallet UX etc.) and building trust will also take time. A gradual sharding rollout will be very much in line with what rollup users are already accustomed to.

## Replies

**kladkogex** (2021-08-13):

Once data shards are available you will be able to do do merge mining on them as well as you will be able to do rollups.

So people that think that data shards will be used by rollups may be surprised. Like we at SKALE could easily do a Layer 1  version of SKL by publishing blocks on ETH data shards.

So far we see very little use of rollups and lots of use for ETH compatible blockchains.   The only roadmap that can realistically be implemented is the one that is implicitly created by users as a result of using something.

Any other roadmap centrally decided can only be perceived ironically because ETH is not a single project anymore, it is an ecosystem of projects where people do whatever they want and users surprisingly use whatever they like.

---

**Polynya** (2021-08-13):

To be fair, this is largely because EVM-compatible rollups are in the process of being rolled out, while EVM-compatible/clone L1s have been around for a while. Arbitrum One has an impressive list of projects deployed on it already - Uniswap, Maker, Chainlink, Aave, USDC, Sushi etc. + hundreds of others - with broad ecosystem support from Etherscan, MetaMask, Infura, Alchemy, Truffle etc. It’s fair to say that it has the greatest developer adoption of any smart contract chain aside from Ethereum itself. The final piece of the puzzle is opening it up to users, and that will happen in a couple of weeks’ time. Other smart contract rollups like Optimistic Ethereum, zkSync 2.0, StarkNet, OMGX, Hermez zkEVM etc. are hard at work too.

Appreciate your perspective, and yes, I fully agree that Ethereum is becoming more of a base layer that different types of chains can be built atop of in different ways. Personally, I prefer rollups as they leverage Ethereum’s security - without relying on a more centralized L1 - and believe this will be the primary avenue in the medium term. But alternative models like validiums & volitions or using it for data availability only as you mention are interesting too. It’s great to see innovation on all fronts.

---

**benjaminion** (2021-08-13):

I quite like this proposal, but unfortunately I don’t think it would be as simple as just reducing the `INITIAL_ACTIVE_SHARDS` constant. Fairly soon, we shall be running at capacity with 64 committees per slot on the beacon chain. As per (the converse of) the comment in the [sharding spec](https://github.com/ethereum/eth2.0-specs/blob/dd58c702d1459e0c1393d8a392b4e98a6b5d9ec9/specs/sharding/beacon-chain.md#get_active_shard_count), the number of committees puts a lower bound on the number of shards.

```auto
def get_active_shard_count(state: BeaconState, epoch: Epoch) -> uint64:
    """
    Return the number of active shards.
    Note that this puts an upper bound on the number of committees per slot.
    """
    return INITIAL_ACTIVE_SHARDS
```

So, setting the shard count to 16 would mean that we could have a maximum of 16 committees per slot, which would mean some material changes to the beacon chain spec, and to committee dynamics. This would be a significant change, engendering a degree of risk as ever.

---

**Polynya** (2021-08-13):

Thanks for the explanation, understood! So, INITIAL_ACTIVE_SHARDS remains at 64. Would it be possible to reduce the MAX_SAMPLES_PER_BLOB and TARGET_SAMPLES_PER_BLOB? Using the same arbitrary numbers above as examples, target 31 kB instead of 248 kB. The end result would be the same from an economic perspective. I’m not a software developer, so apologies if I’m misunderstanding the specs, but I’m sure you’ll know what I mean.

---

**benjaminion** (2021-08-14):

Yes, that would work. It is equivalent to miners voting to change block ~~size~~gas limit in the Eth1 protocol as they currently do. Only we seem to be baking the shard blob size into the protocol for Eth2, which is simpler and safer, but would require a hard fork to modify. So it’s a trade-off of risks as usual.

---

**Polynya** (2021-08-15):

Thinking about these trade-offs, I’ve had another thought - something like a longer-term 1559. Keep the MAX_SAMPLES_PER_BLOB and TARGET_SAMPLES_PER_BLOB as is, but add in a further variable - let’s say, INITIALTARGET_SAMPLES_PER_BLOB.

So, as per the above examples, we start with ~31 kB instead of 248 kB (of course, “initalmax” will be ~62 kB, or whatever MAX:TARGET ratios are chosen - the short-term 1559-like mechanism will follow these targets), but the protocol gradually increments this to the final target of 256 kB based on block fullness (slot fullness?). Again, some arbitrary examples, if the 7-day moving average is ~95% of initial target of 31 kB, increment by +5% every 24 hours. This continues till the target of ~248 kB is reached. Potentially, this could also be two-way like 1559, i.e. if blocks are less than ~50% as per a 7 day MA, then increment by -5% per day till the initialtarget is reached, but this may not be required. There’s probably a simpler way to achieve the same goal. We know that ~248 kB is a “safe target”, and to push past this final target, we’ll need hard forks to either add more shards and increase the shard blob target size.

Something like this could: a) have a smoother supply increment curve, mitigating positive supply shocks described above; and b) keep the system safe and secure without requiring validator voting or further hard forks, until we’re prepared to lift the ceiling past 64/248. Of course, it adds complexity - which is the trade-off. A much simpler alternative solution could also be a naïve linear increment hardcoded, e.g. start at initialtarget, increment by +3% every 24 hours (arbitrary examples, again) till the target is reached.

---

**kladkogex** (2021-08-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/polynya/48/6945_2.png) Polynya:

> it has the greatest developer adoption of any smart contract chain

Well … respectfully disagree.  One can deploy anything on anything but the question is whether people will use.

Binance smart chain has like 1000 times more use.

---

**Polynya** (2021-08-23):

I do not wish to go off-topic here, and I agree that Arbitrum needs to prove itself when it opens to the public in a week’s time. However, I just want to clarify that I was specifically talking about developer adoption, not user adoption. Many of the top DeFi dApps like Uniswap or Maker have not deployed to Binance Smart Chain, but have embraced Arbitrum One, for example.

