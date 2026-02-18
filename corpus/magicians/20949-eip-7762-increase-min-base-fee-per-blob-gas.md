---
source: magicians
topic_id: 20949
title: "EIP-7762: Increase MIN_BASE_FEE_PER_BLOB_GAS"
author: MaxResnick
date: "2024-09-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7762-increase-min-base-fee-per-blob-gas/20949
views: 1275
likes: 14
posts_count: 10
---

# EIP-7762: Increase MIN_BASE_FEE_PER_BLOB_GAS

Discussion topic for EIP-7762 <[link to EIP](https://github.com/ethereum/EIPs/pull/8849)>

#### Update Log

2024-09-02: initial draft

https://github.com/ethereum/EIPs/pull/8849/commits/9d588a70c26108432d3c63b959af3ad3981475c2

#### External Reviews

[Data Always](https://ethresear.ch/t/understanding-minimum-blob-base-fees/20489)

[Robert Bayardo of Base](https://x.com/roberto_bayardo/status/1838986334683513330)

#### Outstanding Issues

None as of 2024-09-03

## Replies

**davidecrapis.eth** (2024-09-05):

The motivation for setting the parameter considered in the EIP draft is wrong imo:

> To set the parameter apropriately, one aproach is to look at the cost of simple transfers when base fees are low. The cost of a simple transfer when the base fee is 1 GWEI is ~5 cents USD at today’s prices (2,445.77$ ETH/USDC). We can try to peg the minimum price of a blob to that.

We should connect the logic to the reason we are increasing the minimum which is less arbitrary. Eg, can we simulate a pareto frontier between the following?

- fraction of time that min fee is active (based on historical data)
- time for blob fee to reach X gwei

---

**ryanberckmans** (2024-09-11):

> We should connect the logic to the reason we are increasing the minimum which is less arbitrary.

Makes sense.

If I understand correctly

1. Selling blobs for free during a lack of congestion is not a problem at all. It’s actually great, as blobs being free minimizes L2 cost and helps to maximize investment in Ethereum’s network effects.
2. The reason for this EIP is to fix the blob gas market from being non-responsive during the initial stages of sustained congestion due to the number of consecutive congested blocks it takes for a 1 wei base fee to grow to become non de minimis.
3. This EIP’s strategy is to increase the minimum blob base fee, which seems reasonable.
4. In terms of opportunity cost of this EIP’s strategy, it can be useful to enumerate any alternative approaches. One alternative could be to ramp up the base fee much faster below a threshold, but this is more complex. Raising the minimum base fee is the (perhaps provably) simplest approach, so let’s start there. But we don’t want blobs to be unnecessarily expensive without congestion, so we need a method to determine the new minimum base fee. Max gives one method (5 cent method). Here is another possible method:

Assuming the current blob base fee is 1 wei and then the sudden onset of sustained congestion

- Today, how many blocks with 6 blobs does it take for the base fee to ramp up from 1 wei to become non de minimis?
- How many blocks do we want it to take?
- What new minimum base fee is implied by how many blocks we want it to take?
- For illustrative purposes, given our proposed new minimum blob base fee, what would be the DA cost component of a rollup transaction for a simple transfer or swap? What if the price of ETH rises to $50k? With ETH at $50k, is DA still effectively free for end-users if blobs are not congested (this seems like a good goal)?

---

**Nerolation** (2024-09-12):

I do see the short-term advantages of 7762, though, I think there is also value in not touching the protocol for fine-tuning things.

Also, it’s debatable how much of a problem this really is.

Having the blob basefee min at the lowest possible point is more neutral than some arbitrary number that potentially needs to be adjusted in the future.

While the intentions are right, I am for leaving the mechanism as-is.

---

**benaadams** (2024-09-12):

wei is used for decimal precision; the min price should never have been set at 1 wei as there is no decimal precision left (1 wei being the smallest amount)

If blob fees are meant to go up by +12.5% of 1 wei; what is that? 0 wei because it cannot be expressed; so instead the math needs to be fudged to 2 wei (+100%)

The fairest of fair launch tokens would never be launched at a 1 wei price because Uniswap and all dexes would choke on the maths.

For a low price something more in the 1 gwei or lowest of low 0.1 gwei is more sensible; because at least the price deltas are calculatable without fudges

---

**Nerolation** (2024-09-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png) benaadams:

> If blob fees are meant to go up by +12.5% of 1 wei; what is that? 0 wei because it cannot be expressed; so instead the math needs to be fudged to 2 wei (+100%)

This is not a problem because excess blob gas can grow infinitely (bc it’s cumulating). When it reaches 2,313,024 excess gas, then the base fee doubles (e.g. from 1 wei to 2 wei) such that the transition from 1 wei → 2 wei takes 6 blocks having 6 blobs.

---

**benaadams** (2024-09-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> such that the transition from 1 wei → 2 wei takes 6 blocks having 6 blobs.

Which demonstrates the issue; that it takes 6 over target blocks to increase the fee by 1 wei

---

**prestonvanloon** (2024-09-12):

I share this view point. Modifying the min base fee per blob gas seems short sighted and setting the floor to the minimum value rather than an arbitrary value is more credibly neutral. Additionally, this only matters when blob demand is too low for price discovery.

The argument that 1wei is too small of a unit to instantly react to blob demand may be valid. However, it only holds true when the price is less than 6 wei.

Do we need to modify the protocol for these edge cases? I think it is not worth it.

If there is strong interest in moving forward on this, it would be worthwhile to review the arguments from geth reducing their min tip requirements. [miner: lower default min miner tip from 1 gwei to 0.001 gwei by karalabe · Pull Request #29895 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/pull/29895). Block producers should be rewarded something, but in the case of transactions (also blobs in this context) that something is much less than this EIP’s proposal.

*Disclaimer: I am employed by a company that buys blob space. I do not care if blob buyers or my employer pays more for blob space. I care about a neutral protocol.*

---

**hiddenintheworld** (2024-10-09):

1. How about taking Time-Weighted Average Price (TWAP) model or some linear model as a reference instead of setting a hard threshold of +12.5% for adjusting the blob base fee is better. TWAP model would smooth out volatility and adjust quicker for gradual adjustments and avoiding sudden fee spikes.
@benaadams @Nerolation
2. L2 solutions like rollups heavily rely on DA, it’s crucial to keep DA costs low. It is better to propose a way so for transfer with less blobs like basic transfers or those using rollups, even with a higher base fee, we can ensure that fewer blobs are used at a lower cost for simpler transfers, maintaining affordability while scaling Ethereum efficiently.
@ryanberckmans

---

**eawosika** (2024-12-04):

Hi all! Recently published a high-level explanation of EIP-7762 for those interested: [EIP-7762 & EIP-7691: Making Ethereum Blobs Great Again](https://research.2077.xyz/eip-7762-eip-7691-making-ethereum-blobs-great-again). The article explores provides context surrounding the existing blob pricing mechanism and discusses the rationale for tweaking the pricing formula to make the blobspace market more efficient. All comments and feedback are welcome.

