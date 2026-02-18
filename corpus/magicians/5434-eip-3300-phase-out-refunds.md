---
source: magicians
topic_id: 5434
title: "EIP-3300: Phase out refunds"
author: wjmelements
date: "2021-02-27"
category: EIPs
tags: [evm, council-of-prague, refund, selfdestruct, eip-3300]
url: https://ethereum-magicians.org/t/eip-3300-phase-out-refunds/5434
views: 3236
likes: 1
posts_count: 9
---

# EIP-3300: Phase out refunds

https://github.com/ethereum/EIPs/pull/3300

## Replies

**timbeiko** (2021-02-27):

Cross-posting a few comments from the [Eth R&D discord](https://discord.com/channels/595666850260713488/812719315136675850/815299124353957978):

> @shemnon: I think a gradual incentive to clear out the inventory is better than a deadline and the preceding fire sale. I expect we would see more state cleanup in the gradual scenario.

> @timbeiko: Generally agree, although 1m blocks (~1y) seems very long, especially given the “advance warning” w.r.t. this actually hitting mainnet. IMO if we’re planning to, say, have another upgrade around Q4/Q1, we should aim to have the refund at 0 by then, and then we can maybe simplify a lot of code on the next fork.
> So, in other words, ~1 year from today seems fine, but not ~1 year from London hitting mainnet

---

**shemnon** (2021-02-27):

Would a 50 block step be an option then?  Puts the phase out to ~1MM blocks.

---

**wjmelements** (2021-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> So, in other words, ~1 year from today seems fine, but not ~1 year from London hitting mainnet

The longer it goes the more cleanup we can expect. I would suggest 64 over 50 for a rounder number, but if they must be removed by the following major upgrade, 1,900,000 is a reasonable timetable. For 64 it would be 1,216,000 blocks, about 7 months. There were 1,789,000 blocks (282 days) between Constantinople and Istanbul, and Istanbul/Muir has gone for almost 3,000,000.

For theoretically larger intra-tx refunds such as the 19800 specified by EIP-1283, I would not suggest to wait the full decay period since the refund was not stored between transactions. For that case it would be sufficient to go forward with an upgrade that replaces the remaining intra-tx refund with some negative-gas mechanic.

From Github:

> GasTokens are effectively an exploit

As a speedrunning enthusiast I wouldn’t categorize any feature being used in a way the developers are [aware of and call a net-positive](https://ethresear.ch/t/use-of-https-gastoken-io-positive-or-negative-for-the-network/2790/2) as an exploit.

> It’s not our fault that certain people hoarded them against this advice. And most certainly it shouldn’t lead to stretching out selfdestruct phase out.

I wouldn’t say we’ve been hoarding them. We use hundreds to tens of thousands per week depending on congestion, and the amount we hold is reasonable for our business. We have to hedge against the gas price volatility and insure against the worst-case. It’s easy to criticize us if you don’t participate in PGAs or need to use the network in peak congestion, but refund usage is not optional, and our gas reserve is rational. If refund removal cannot be delayed for whatever reason, core devs might prefer the cleanup-and-compensation alternative I am currently writing up, tho that will be more work for them.

---

**MicahZoltu** (2021-03-02):

What is the argument for 17 moths over 5 months?  (where 5 months is starting from now until expected London HF, and 12 months is that plus a 1 year decrease)

---

**wjmelements** (2021-03-02):

They’re more likely to be freed under the phase-out plan because as their intrinsic value drops it will be cheaper to buy the liquid refunds than to mint them, and they will still be burned in congestion. I don’t think 5 months would be enough time to burn even half of them, especially without the diminishing efficiency.

This is also fairer to refund holders, especially illiquid refund holders who can’t just dump on some poor AMM LP.

On a 5 month schedule I would suggest cleanup and compensation, where all of the refund contracts are replaced by EIP similar to the DAO fork, and refund holders receive freshly minted ETH at some fair gas price, perhaps totaling several thousand ETH. But the real cost of this would be developer time.

---

**MicahZoltu** (2021-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> On a 5 month schedule I would suggest cleanup and compensation, where all of the refund contracts are replaced by EIP similar to the DAO fork, and refund holders receive freshly minted ETH at some fair gas price, perhaps totaling several thousand ETH. But the real cost of this would be developer time.

I’m *personally* not a huge fan of taxing Ethereum holders in order to pay people who spent the last 12 months bloating the blockchain.  I would be fine with an irregular state change that wiped out the obviously worthless state though (CHI tokens and Gas tokens specifically).

If we implement something like [Resurrection-conflict-minimized state bounding, take 2 - Execution Layer Research - Ethereum Research](https://ethresear.ch/t/resurrection-conflict-minimized-state-bounding-take-2/8739) then the CHI and Gas tokens will eventually fade into cold state and be pruned, so the situation will clean itself up naturally long term (if we go that route).

---

**wjmelements** (2021-03-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I’m personally not a huge fan of taxing Ethereum holders in order to pay people who spent the last 12 months bloating the blockchain. I would be fine with an irregular state change that wiped out the obviously worthless state though (CHI tokens and Gas tokens specifically).

Holders aren’t necessarily minters, especially in the liquid case, but neither are doing anything wrong. It’s evil and possibly illegal to destroy their assets without compensation. Also the “bloat” is small relative to the total storage, has been in steep decline for months, and can be reduced further by taking advantage of its uniformity.

---

**wjmelements** (2021-03-04):

I currently prefer [EIP-3322](https://ethereum-magicians.org/t/eip-3322-efficient-gas-storage/5470) to this because refunds encourage healthy state management. Most of the concerns with refunds can be solved by introducing a more-efficient alternative.

