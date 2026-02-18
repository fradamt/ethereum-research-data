---
source: magicians
topic_id: 8958
title: "EIP-5018: Directory Standard"
author: qizhou
date: "2022-04-18"
category: EIPs
tags: [data, storage]
url: https://ethereum-magicians.org/t/eip-5018-directory-standard/8958
views: 2296
likes: 1
posts_count: 5
---

# EIP-5018: Directory Standard

---

## eip: 5018
title: Directory Standard
description: A standard interface for filesystem directories.
author: Qi Zhou ()
discussions-to: TBD
status: Draft
type: Standards Track
category: ERC
created: 2022-04-18

## Abstract

The following standard allows for the implementation of a standard API for filesystem directories within smart contracts.

This standard provides basic functionality to read/write binary objects for any size, as well as allow reading/writing chunks of the object if the object is too large to fit in a single transaction.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5018/files)














####


      `master` ← `qizhou:qizhou-dir`




          opened 07:30PM - 18 Apr 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/e/ec489df73b8873547715c8a2f21986ca2b83d33c.jpeg)
            qizhou](https://github.com/qizhou)



          [+159
            -0](https://github.com/ethereum/EIPs/pull/5018/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/5018)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**SamWilsn** (2022-05-20):

I have a couple non-formatting related comments:

- What makes this EIP filesystem-like? It seems like it’s really a key-value store?
- What data structure do you envision backing this interface?
- Why use chunk ids instead of byte ranges?

---

**qizhou** (2022-05-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What makes this EIP filesystem-like? It seems like it’s really a key-value store?

Thanks for the comment. I agree that the current interface is quite similar to a key-value store.  The reason is that we want a filesystem-like smart contract with **minimal necessary** interfaces that can host a decentralized website:

1. chunked-based functions are needed because we want to support reading a large BLOB, which cannot be fit in a single tx;
2. ls (list directory contents) may not be needed in the minimal version as most websites do not offer it to users;
3. sub-directory can be achieved by allowing “/”'s in the filename, e.g., “/a/b/c/d”, so we may not need an explicit interface of sub-directory.

Note that, a key-value store may not have 1. Moreover, if the applications do need 2 or 3, we can create the extension EIPs to include the features (similar to the extensions to ERC-20/ERC-721).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> What data structure do you envision backing this interface?

Thanks for the comment.  Current EVM supports two types of storage.

1. local contract storage via SLOAD/SSTORE; and
2. contract-code-based via CREATE/CREATE2/EXTCODECOPY.

The first storage is efficient for 32-bytes operations, but if the data is large with dynamic size, using contract-code-based storage can be more efficient in both gas and IO.  The following is a table of the gas for different storage (note that the gas for put only accounts for the the-first-time put):

|  | OPCODE | 1k | 4k | 8k | 12k |
| --- | --- | --- | --- | --- | --- |
| Local contract (get) | SLOAD | 96212 | 310514 | 596473 | 882688 |
| Local contract | SSTORE | 771051 | 2949132 | 5853295 | 8757522 |
| Code-based storage | EXTCODECOPY | 30502 (1/3.15x) | 38987 (1/7.96x) | 50525 (1/11.8x) | 62319 (1 / 14.1x) |
| Code-based storage | CREATE | 387383 (1/ 2x) | 1128673 (1/2.61x) | 2117788 (1/2.76x) | 3104698 (1 / 2.82x) |

We have implemented both types of storage following the standards and the code can be found here [GitHub - ethstorage/evm-large-storage-bak](https://github.com/web3q/evm-large-storage), where

- For local contract storage, we use keccak256(filename || chunkId) as the key, and the value is an optimized version of solidity bytes storage
- For contract-code-based storage, we use keccak256(filename || chunkId) as the key, and the value is a contract, whose code contains the corresponding chunk data.

Furthermore, the code is deployed to Rinkeby to store ENS and Uniswap homepages, and works very well:

- ENS Homepage: https://galileo.web3q.io/ensdomains.eth:4/ @ 0x9e081Df45E0D167636DB9C61C7ce719A58d82E3b
- Uniswap Homepage: https://galileo.web3q.io/uniswaps.eth:4/ @ 0xC100d49e8F3d621E4438E82E4f95CF505b3E2a28

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Why use chunk ids instead of byte ranges?

A good design question!  To support large BLOB, we can definitely do bytes ranges as UNIX read/write do.  However, this seems to be complicated in some cases such as read-modify-write - if a write overrides multiple physical storages (e.g., storage slots or contract code), the contract needs to read existing data/override the data/rewrite the data.  Using chunk ids, we can simplify the logic and let the off-chain application determine how to use them (and do read-modify-write off-chain).  What do you think?

---

**talentlessguy** (2025-06-07):

So as of now EIP-5018 does not support nested directories?

---

**qizhou** (2025-11-06):

No, for simplicity, the standard only supports flat directory, where you can support subdirectory by introducing app-level directory separator character like ‘/’

