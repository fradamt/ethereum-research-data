---
source: magicians
topic_id: 21587
title: "EIP-7808: Reserve Tx-Type Range for RIPs"
author: CarlBeek
date: "2024-11-05"
category: EIPs > EIPs Meta
tags: []
url: https://ethereum-magicians.org/t/eip-7808-reserve-tx-type-range-for-rips/21587
views: 131
likes: 3
posts_count: 5
---

# EIP-7808: Reserve Tx-Type Range for RIPs

This post is for discussion of [EIP 78xx](https://github.com/ethereum/EIPs/pull/9020) wherein the [transaction-type](https://eips.ethereum.org/EIPS/eip-2718) range from `0x40` to `0x7f` are reserved for use by the RIP process similar to how [EIP-7587](https://eips.ethereum.org/EIPS/eip-7587) did for precompile addresses.

## Replies

**protolambda** (2024-12-19):

OP-Stack uses 0x7E for deposit txs from L1 into L2.

See [specs/specs/protocol/deposits.md at main · ethereum-optimism/specs · GitHub](https://github.com/ethereum-optimism/specs/blob/main/specs/protocol/deposits.md#the-deposited-transaction-type)

This type falls into this range.

Will there be a registry of L2 tx type usage?

Also, I believe other L2 stacks use custom tx types already as well. Arbitrum has 7 if I remember correctly.

---

**prasincs** (2025-04-04):

Where is this defined? I followed the specs but when I looked at `ethereum-optimism/op-geth/blob/optimism/core/types/transaction.go#L47-L52` it’s same as go-ethereum.

whereas Arbitrum defines it here `OffchainLabs/go-ethereum/blob/084f63827520569955a905596878d90d42b734a7/core/types/transaction.go#L46-L60`

(sorry new account can’t link)

we can probably go through all major go-ethereum forks for the file and find if the range has any overlaps?

---

**shemnon** (2025-04-05):

EIP editors are not going to like this suggestion, but I think we should keep an open “living” RIP/RRC to enumerate chain specific TX Types, precompile addresses, etc.  This should be *somewhere* and it it was a RIP/RRC there is some weight of “this is the official registry.”

TX types may become the most conflicted.

Also, we should preserve some for multi-byte TX types.

---

**prasincs** (2025-04-28):

I like this idea, it’s very hard to build a scalable indexer across the ecosystem if we have to make custom rules. Having an official registry would help to ensure that we at least have the diffs recorded.

