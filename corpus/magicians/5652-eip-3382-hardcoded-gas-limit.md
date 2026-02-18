---
source: magicians
topic_id: 5652
title: EIP-3382 - Hardcoded Gas limit
author: PhABC
date: "2021-03-15"
category: EIPs
tags: [gas, eth1x, core-eips]
url: https://ethereum-magicians.org/t/eip-3382-hardcoded-gas-limit/5652
views: 3417
likes: 11
posts_count: 7
---

# EIP-3382 - Hardcoded Gas limit

## Simple Summary

Hardcode the block gas limit (known as *block gas target* under [EIP-1559](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1559.md)) to `12,500,000` gas per block.

## Abstract

Ethereum’s block gas limit is currently dictated by block producers and is not enforced when validating blocks in clients. This EIP proposes to hardcode the block gas limit to `12,500,000`.

…


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3382)





###

## Replies

**Agusx1211** (2021-03-15):

As far I know the reason we can’t increase the block size today is a worst-case-scenario block with a ton of SLOADs, this is something that should be addressed in Berlin, and I’ve seen some talks about increasing the gas limit after Berlin because of it.

Maybe this EIP is a good time to do so? If this EIP get’s accepted it would be included probably around London, with [EIP-2929](https://eips.ethereum.org/EIPS/eip-2929) already merged, maybe we can consider a higher value for the initial hardcoded block gas limit?

---

**Hasu** (2021-03-15):

I support this proposal.

The more control miners have over core protocol parameters, the more Ethereum must pay to incentivize their honesty. The main argument for giving miners control over the gas limit is that every update to a hard-coded gas limit requires a hard-fork. But given that Ethereum hard-forks 2-3 times per year anyway, there is no reason not to update it there.

---

**ajsutton** (2021-03-15):

Agreed that it just makes sense to take block size out of the miner control.

I think this is also an important step towards the merge for a couple of reasons:

1. Control of block size will move from miners to stakers and while we’ve seen miners act responsibly and work well with core devs about block sizes, it’s much less known what stakers will do
2. Currently mining pools effectively control the block size but solo staking is much more viable and common than solo mining because rewards are paid smoothly even for a single validator. This may make it very difficult to coordinate desired block size changes in the future.

---

**wjmelements** (2021-03-15):

Strongly opposed to a hardcoded constant. Hard forks are irregular. If this proposal had been implemented in Istanbul, the constant would have been 10m, and the gas price would be much higher than it is currently. This constant, like the difficulty bomb, would need to be micro-managed every hard fork, and, in my observation, core developers are very bad at estimating possible throughput.

But I can support removing it from miner control since they have a propensity toward keeping it far below capacity to manage their operating costs. We could consider instead increasing the gas target when it is often exceeded, as that is evidence that miners could handle a higher limit. A higher uncle rate could signal DoS and push down the gas target.

---

**optimalbrew** (2021-03-16):

> ### Security Considerations
>
>
>
> Rapid changes to the gas limit will likely be more difficult to execute, which could be problematic if an urgent situation arise that required changing the gas limit.

I wonder if there is any asymmetry in the direction of rapid changes that may be needed in urgent situations. If so, then the hard target can be *one-sided*.

---

**elbeem** (2021-04-28):

Isn’t the gas limit already one-sided, in that it is allowed to make blocks with total gas below the limit?

