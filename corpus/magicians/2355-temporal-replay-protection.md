---
source: magicians
topic_id: 2355
title: Temporal Replay Protection
author: holiman
date: "2019-01-08"
category: EIPs
tags: [security, dust-removal, replay-protection]
url: https://ethereum-magicians.org/t/temporal-replay-protection/2355
views: 3479
likes: 9
posts_count: 8
---

# Temporal Replay Protection

This EIP would add temporal replay protection: https://github.com/ethereum/EIPs/pull/1681

We already have cross-chain replay protection, thus ‘temporal’ to signify that we’re talking about replay over time.

The main driver for my EIP is to make dust account removal possible, but there are also other scenarios where it could be useful: during ICO (either the tx makes it through within two hours or just remove it) and to make it easier for nodes to clean up/maintain transaction queues.

EDIT: Linked to the PR instead of a the version in a specific commit-hash

## Replies

**ligi** (2019-01-08):

Really like this EIP - much cleaner than e.g. replacing a transaction with a higher gas price when the tx is not wanted anymore.

Just a small nit:

> Note: this EIP does not introduce any maximum valid-until date, so it would still be possible to create transactions with near infinite validity.

actually it introduces a maximum (max uint64) - so perhaps change to:

> Note: this EIP does not introduce any maximum valid-until date apart from the maximum of uint64, so it would still be possible to create transactions with near infinite validity.

so there is no more room to nit-pick.

Thanks for the initiative with this EIP! Can’t wait for the HF introducing this feature.

---

**Amxx** (2019-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Just a small nit:
>
>
>
> Note: this EIP does not introduce any maximum valid-until date, so it would still be possible to create transactions with near infinite validity.

actually it introduces a maximum (max uint64) - so perhaps change to:

> Note: this EIP does not introduce any maximum valid-until date apart from the maximum of uint64, so it would still be possible to create transactions with near infinite validity.

Another possibility is to consider that valid-until 0 is equivalent to valid forever. This is what I call the “check only if value is set” approach.

---

**ligi** (2019-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Another possibility is to consider that valid-until 0 is equivalent to valid forever. This is what I call the “check only if value is set” approach.

I do not think this is needed and it would introduce a bit more complexity in code. So I would signal not to do it this way. I think the approach of [@holiman](/u/holiman) is completely fine there my comment was just to get the wording a bit more precise so there is no more nit-picking possible.

---

**holiman** (2019-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> I do not think this is needed and it would introduce a bit more complexity in code

I’d agree about that. I pushed some changes to the EIP, to give credit to an earlier EIP (by [@Arachnid](/u/arachnid))  which was basically the same, but used blocknumber instead of `time`. I also added some reasoning about that choice.

---

**Arctek** (2019-12-27):

With a few trading protocols now supporting a deadline in their smart contracts (Uniswap V2, 0x v3), having this would be great for preventing charging users for transactions that will fail past a deadline.

It should also help out in terms of transactions that needlessly sit in the pending pool by fault of user error.

If a transaction is signed for a particular valid-until date, does that make any subsequent transaction with a higher valid-until date invalid?

---

**kladkogex** (2019-12-30):

This is super important for fast ETH-compatible networks like us at SKALE, and we will implement it on our network sometime in 2020.

It has to be the time stamp and not the block number, since for asynchronous consensus there is no fixed, so the block number becomes meaninless.

---

**MicahZoltu** (2020-06-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I pushed some changes to the EIP, to give credit to an earlier EIP (by @Arachnid) which was basically the same, but used blocknumber instead of time .

I don’t personally think this is appropriate content for an EIP.  EIPs are all CC0 so there is no legal theater necessity to give credit, and the referenced EIP is still a draft (looks like dead in the water) and therefore subject to a complete rewrite that makes it no longer at all related to what this EIP does.  If it were a final EIP then I would have no problem with that addition.

