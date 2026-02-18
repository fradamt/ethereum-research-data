---
source: magicians
topic_id: 7614
title: "EIP Proposal: Increase cost of SSTORE from 20k to X when creating new storage"
author: green
date: "2021-11-29"
category: EIPs > EIPs core
tags: [evm, opcodes, gas]
url: https://ethereum-magicians.org/t/eip-proposal-increase-cost-of-sstore-from-20k-to-x-when-creating-new-storage/7614
views: 2582
likes: 1
posts_count: 4
---

# EIP Proposal: Increase cost of SSTORE from 20k to X when creating new storage

(please change tags if they are improper)

I’m making a draft for a EIP to raise the cost of creating new storage.

I’ve been told EIPs require to be highly technical, but I don’t have that technical knowledge. I also want to have a discussion on if this is feasible or desirable. I will be pasting the unfinished .md I wrote.

Originally, the proposal had `NEW_STORAGE_PRICE` = `30_000`, but I want to see if someone more knowledgeable proposes a different amount. Why not `40_000` instead, what would the consequences be?

It’s implied in the EIP, but the cost of modifying existing storage remains the same.

## Abstract

Increase the cost of the `SSTORE` opcode from `20_000` gas to `NEW_STORAGE_PRICE` gas when the original slot is zero and the resultant slot is non-zero.

## Motivation

The cost of creating a piece of new state increases as state is larger. However, the price for creating every new storage slot has not increased as state became larger.

All resources are merged into the same pricing mechanism. As the price for creating new storage slots is fixed, it has to be changed manually to reflect costs more accurately.

Until a solution to state growth like state expiry is built, a way to slow down the creation of new storage slots will buy additional time.

One of the main reasons for not increasing gas limit is the increase of state. In that regard, because the cost of creating storage is higher than its price, all the users of all the other opcodes are subsidizing the creation of state. If creating state was more precisely priced, raising gas limit would be more feasible, and would benefit the users.

## Specification

| Constant | Value |
| --- | --- |
| FORK_BLOCK | TBD |
| NEW_STORAGE_PRICE | TBD |

For blocks where `block.number >= FORK_BLOCK`, a new gas schedule applies. Make `SSTORE` cost `NEW_STORAGE_PRICE` when a slot is set to non-zero when the original slot is zero. All other costs remain the same.

## Rationale

Unsure of what this means, TODO.

## Backwards Compatibility

Some contracts that depend on hardcoded gas costs may have to be redeployed.

It is a gas schedule change, so transactions from an epoch before `FORK_BLOCK` should be treated with previous gas costs.

## Implementation

TODO

## Security Considerations

Less state growth may encourage miners to increase gas limit per block. This could lead to a return to previous level of state growth, and some new problems such as increased latency, increase in uncle blocks.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**SCBuergel** (2022-04-23):

Could you please provide an analysis and measurement that supports the following statement from the EIP?

> The current pricing was made off a naive approach of benchmarking opcodes in a laptop. Not only it did not consider the long term problem of having the same price for a resource that costs more over time, the benchmark itself was wrong. This price is closer to what the naive original benchmark should have been. It could go higher, but that may be too disruptive.

I would also understand better what exactly this means

> The cost of creating a piece of new state increases as state is larger.

Are you referring to disk space or space in memory while processing? If it’s the former then I guess one should also increase pricing of tx payload as that also gets stored?

---

**green** (2022-07-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/scbuergel/48/14825_2.png) SCBuergel:

> Could you please provide an analysis and measurement that supports the following statement from the EIP?

> The current pricing was made off a naive approach of benchmarking opcodes in a laptop

I got this from a talk by [John Adler](https://twitter.com/jadler0) in Layer Two Amsterdam. [I believe this is the talk](https://youtu.be/_6ctMrlhcO4?t=148).

I’m not sure how to word this properly in the EIP. Since I wrote [EIP-5022](https://github.com/ethereum/EIPs/pull/5022). I will just remove the statement since I’m not able to properly support it.

> Are you referring to disk space or space in memory while processing?

I don’t have deep knowledge on how the EVM works and how expensive is storage, but intuitively, I assumed the following (which may be wrong):

- Disk space, which makes it more expensive for clients to support, and as barriers of entry are higher becomes a centralizing force. The miners prevent this by decreasing the block size, which means that those that are not using storage extensively, are subsidizing this cost that heavy storage users are incurring.
- More storage means that, adding a new piece of storage is more expensive for the data structure to support.
- Reading the state takes more time the more state there is.

> If it’s the former then I guess one should also increase pricing of tx payload as that also gets stored?

Sorry, I’m not sure about this. I guess storage incurs a higher usage?

This EIP shouldn’t be a final solution either. It’s just a hotfix until multidimensional resource pricing is added, so it’s not meant to address all these opcode cost inconsistencies at the same time. It’s mainly meant to temporarily halt abusive state creation.

---

**xinbenlv** (2022-09-22):

I’d love to see some analysis about the reasoning too. Such as why 40K, why not 80K or 100K? Or why not reduce?

In fact if we were able to reduce history [EIP-4444: Bound Historical Data in Execution Clients](https://eips.ethereum.org/EIPS/eip-4444) we might reduce the cost of a SSTORE

