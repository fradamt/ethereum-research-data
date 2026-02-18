---
source: magicians
topic_id: 9851
title: "ERC-5202: Standard Factory Contract Format"
author: charles-cooper
date: "2022-07-05"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/erc-5202-standard-factory-contract-format/9851
views: 2363
likes: 1
posts_count: 6
---

# ERC-5202: Standard Factory Contract Format

An ERC standard for factory contracts. Please see the EIP text at [ERC-5202: Blueprint contract format](https://eips.ethereum.org/EIPS/eip-5202)

## Replies

**SamWilsn** (2023-04-18):

I believe the EOF team was working on something similar to remove `codecopy`. Maybe [@matt](/u/matt) knows more?

Edit: saw your note in rationale.

---

**SamWilsn** (2023-04-18):

Why have both the version field and reserve a length for continuation? If you ever need a longer data region with the current scheme, you’d need to write a new EIP defining the length encoding anyway, right?

---

**charles-cooper** (2023-04-27):

The main reason is we already needed 2 bits to describe the length encoding, and did not have anything to do with the last value (since needing 3 bytes to describe a contract’s length is already de facto an invalid contract per EIP 170). If it’s clearer to think about it this way, the wording of the current spec in its most narrow reading just says that version `0b000000` combined with length encoding bits of `0b11`  results in an invalid ERC-5202 contract.

We could loosen the restriction on the length encoding bits, although I don’t really see the purpose since I don’t think the EIP 170 restriction will be lifted any time soon, and it forces a specific interpretation of `0b11` even though there is not currently a use for it. In other words, the way the EIP is written, it leaves it ambiguous whether in the future `0b11` would mean 3 bytes for the length or if it will be used as a continuation marker - and I think the flexibility is better.

---

**axic** (2023-05-19):

If you want to ensure that arbitrary contracts are not mistaken as “blueprints”, you could think about introducing a checksum.

Since users of blueprints must `extcodecopy` the entire account, they already have to bear copy and memory expansion costs. Because of this, you could do something simple, like storing the truncated one byte keccak256 hash of the blueprint contract at the end of it:

```auto
// blueprint_offset is the memory location to where the entire contract was copied to
// blueprint_size is the total size of the copied contract

// store checksum byte at the end
let checksum_byte = mload(add(blueprint_offset, blueprint_size))
let checksum = keccak256(blueprint_offset, sub(blueprint_size, 1))
if iszero(eq(checksum_byte, and(checksum, 0xff))) { revert(0, 0) }
```

---

**axic** (2023-05-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I believe the EOF team was working on something similar to remove codecopy. Maybe @matt knows more?

There have been some discussions/ideas about having a “creator account” functionality with EOF, which basically means the (init)code used would come from an external account. i.e. it would replace this functionality within the EOF paradigm.

