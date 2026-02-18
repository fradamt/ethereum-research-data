---
source: magicians
topic_id: 905
title: Fix block reward at 2 ETH per block (EIP-1277)
author: MicahZoltu
date: "2018-07-31"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/fix-block-reward-at-2-eth-per-block-eip-1277/905
views: 872
likes: 2
posts_count: 8
---

# Fix block reward at 2 ETH per block (EIP-1277)

Discussion for EIP-1277

## Simple Summary

Changes the block reward to be a fixed amount per block of 2 ETH.

## Abstract

As of `FORK_BLOCK_NUMBER`, set the block reward to 2 ETH and the Uncle and Nephew reward following the same formula as before.

## Motivation

There has been an expectation of block reward reduction up to now as a side effect of the ice age.  If the Ice Age is removed or delayed, there will be an increase in block reward per time.  This change makes the most sense on a chain that removes or delays the Ice Age, but it can be implemented on a chain in isolation.

## Specification

```auto
new_block_reward = 2_000_000_000_000_000_000 if block.number >= FORK_BLOCK_NUMBER else block.reward
```

(2E18 attoeth, or 2,000,000,000,000,000,000 attoeth, or 2 ETH).

If an uncle is included in a block for `block.number >= FORK_BLOCK_NUMBER` such that `block.number - uncle.number = k`, the uncle reward is

```auto
new_uncle_reward = (8 - k) * new_block_reward / 8
```

This is the existing pre-fork formula for uncle rewards, simply adjusted with `new_block_reward`.

The nephew reward for `block.number >= FORK_BLOCK_NUMBER` is

```auto
new_nephew_reward = new_block_reward / 32
```

This is the existing pre-fork formula for nephew rewards, simply adjusted with `new_block_reward`.

## Rationale

This change will keep ETH issuance per day stable with pre-fork values in the face of a permanent decrease in blocks per day down to 15 seconds per block.

If there is a desire to keep ETH issuance per day stable in the face of decreasing blocks per day then this EIP is not a good solution and another EIP should be implemented that adjusts the block reward formula to be a function of time rather than a function of block number.

## Backwards Compatibility

This EIP is not forward compatible and introduces backwards incompatibilities in the block, uncle and nephew reward structure. Therefore, it should be included in a scheduled hardfork at a certain block number.

## Test Cases

Test cases shall be created once the specification is to be accepted by the developers or implemented by the clients.

## Implementation

None yet.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**tjayrush** (2018-08-01):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> There has been an expectation of block reward reduction up to now as a side effect of the ice age.

Just to be overly pedantic. It’s not clear how a side effect can be an expected behavior. According to Google, a side effect is “a secondary, typically undesirable effect…”.

Of course, removing (or delaying) the ice age would result in an increase in the block reward over time. But if the decrease in number of blocks per time period is a side effect of growing difficulty then restoring the original issuance per time period can be looked at as a remedy to the problem of the side effect.

I actually support lowering the issuance, but the decision should be based on data. Is it possible to know how many attacks (of the type we’re trying to secure against) occur over a given time period? Have there even been any attacks? Is there a guestimate of how much the network (as a whole) is paying per time period for security. Can we estimate (even to an order of magnitude) how much security we need? Why 2.0 ether per block. Why not 2.5? Why not 2.75?

I’ve seen a lot of discussion that the block reward should be lowered and/or raised, but almost no objective information about what the current situation looks like.

---

**MicahZoltu** (2018-08-02):

Ah, my understanding of the Ice Age was that its primary purpose was to force upgrades by making the network become unusable over time.  It had a secondary effect (possibly desired, but not the primary goal) of reducing block reward over time.  I’m amenable to changing the wording to something else.  Perhaps “There has been an expectation of block reward reduction up to now as a secondary effect of the ice age.”?

---

**MicahZoltu** (2018-08-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tjayrush/48/23_2.png) tjayrush:

> I’ve seen a lot of discussion that the block reward should be lowered and/or raised, but almost no objective information about what the current situation looks like.

This, unfortunately, is because calculating the needed security is *really hard* especially on Ethereum due to smart contracts.  The needed economic security is a function of value transferred over time.  The more value that is moved between parties per unit of time, the higher the economic incentive to attack the system is.  The block reward serves as a mechanism to give economic disincentive to attacks against these value transfers by making it more valuable to miners to mine the longest chain than to risk mining a forked chain in an attempt to steal some of that value.

The lower the block reward, the more confirmations necessary to be confident that an off-chain value transfer actually occurred.

The problem is that we do not have a good mechanism for calculating the value transfer per minute of Ethereum, so we don’t actually have a good measure of how much security we need.  I believe many people have a “gut feeling” about what that number is, but since the data is hard to acquire no one has hard data.

---

**tjayrush** (2018-08-03):

What information exactly would you need to calculate “value transfer per minute”. It doesn’t seem like there are that many variables. Per-block reward, transaction fees, uncle rewards, price in some basket of fiats averaged from multiple sources.

Also, is there some way to make a judgement on how (or even if) anyone is ‘attacking’ the chain? Maybe it’s not possible to even distinguish between an attack and someone just following a different chain for a while. What data would you need to get a feel for that?

Can QuickBlocks help with any of this? QuickBlocks watches every block and does whatever it does with it, but perhaps I can modify it to do some other junk to collect data to make some informed “non-gut-feeling” decisions.

---

**tjayrush** (2018-08-03):

This article appears to have some data to consider: https://medium.com/@eric.conner/a-case-for-ethereum-block-reward-reduction-in-constantinople-eip-1234-25732431fc77.

Looking at the first chart, I see the issuance plummeting just before the difficulty bomb was diffused. It doesn’t make sense to me to claim that the expected issuance pattern anticipates the rising difficulty. The bomb (the plummet) is clearly a wild shift in the issuance and the delay of the bomb at the hard fork is a discontinuity.

I’m not saying the issuance shouldn’t be lower (I think it probably should be), I’m just saying that lowering it to keep it in line with the expected issuance if you build the difficulty bomb into “expected issuance” seems hard to support. At the rate the issuance was declining, if the fork was two weeks later, then by that argument, the new issuance should have been 1 ETH. If the fork was two weeks earlier, it should have been 4 ETH.

---

**MicahZoltu** (2018-08-03):

I personally don’t believe that comparing to other chains is necessary or meaningful.  Nor do I believe that market cap, inflation, etc. are relevant.  What matters is whether or not miners are being paid enough to behave in the way we desire or if they are underpaid, thus financially motivated to behave in undesirable ways (like attempting non-51% double spends).

The reason it is difficult to calculate this is because you need to not only track how much ETH changes hands per minute, but also tokens, and any other asset that holds non-zero value (which is basically everything on-chain).  In theory, you can filter these by “value transfers where one party is providing something off-chain”.  This means that you can ignore almost all Augur trading transactions, or ERC20 to ERC20 trades on on-chain exchanges like 0x, IDEX or EtherDelta.

However, even ignoring the filtering, it is hard to get a number to even start with since changing contract ownership is an example of a value transfer.

---

**tjayrush** (2018-08-03):

I wonder if there’s some way to do sampling (https://en.wikipedia.org/wiki/Sampling_(statistics)).

If we could collect together the right list of things to sample, we might be able to gain some insight.

My goal (to the extent there is one) is to be able to make decisions with a bit more rigor. Switching from 3 ETH to 2 ETH (or 5 to 3, for that matter) seems remarkably “rough-hewn” for a system with 18 decimal place accuracy.

