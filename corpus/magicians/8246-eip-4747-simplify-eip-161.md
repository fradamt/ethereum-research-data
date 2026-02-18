---
source: magicians
topic_id: 8246
title: "EIP-4747: Simplify EIP-161"
author: petertdavies
date: "2022-02-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-4747-simplify-eip-161/8246
views: 2268
likes: 1
posts_count: 4
---

# EIP-4747: Simplify EIP-161

[Pull Request](https://github.com/ethereum/EIPs/pull/4747)

## Background

Empty accounts (defined as having no nonce, no balance, no code and no storage) exist as a consequence of design flaws in early versions of the EVM. After an unknown attacker created large numbers of them during the Shanghai DOS attacks, EIP-161 both banned the creation of new empty accounts and provided that the old ones would be deleted if they were “touched”.

Vitalik Buterin then [bulk touched](https://etherscan.io/address/0xb992592df1b30ce37ffba6f7167e58bfbdfe4b91) all the accounts created by the Shanghai DOS attacker, but neglected to deal with 196 that had been created by accident.

These remaining empty accounts were largely forgotten about, but their continued existance raised the threat of consensus issues with this obscure corner of the protocol. This is best illustrated by [this comment](https://github.com/ethereum/go-ethereum/blob/fb3a6528cfa49f623570575c4fe9e8a716cfcdf7/core/vm/evm.go#L346) in the Geth source code, which incorrectly stated that `STATICCALL`s and empty accounts can never interact on Mainnet. Additionally there were edge cases involving empty accounts with storage, that I have been unable to find a test for.

I deleted every single remaining empty account in [block 14,049,881](https://etherscan.io/tx/0xf955834bfa097458a9cf6b719705a443d32e7f43f20b9b0294098c205b4bcc3d/). This makes all the edge cases that never happened impossible, retroactively vindicates the Geth comment.

However, the Ethereum specification and testsuite still requires implementors to implement EIP-161 state clearing with all the impossible edgecases even where it is irrelevant. As an extreme, a post-merge only client would have to implement state-clearing solely to pass the Ethereum testsuite. The EIP removes as much of this technical debt as possible.

## Technical validation

The EIP requires that certain facts about Mainnet be validated in order to be equivalent to EIP-161. 1 and 2 can be validated by dumping the state at the start of Byzantium to get the list of all 196 accounts that existed post-Byzantium and checking that they were deleted in the transactions named in the EIP.

3 is slightly more complicated. EIP-161 is usually implemented by marking an account as “touched” and then checking if it is still empty at the end of the transaction. Condition 3 can be checked by testing that the “if still empty” never fails during a sync to the start of Byzantium.

I have performed these checks by informally modifying the [akula](https://github.com/akula-bft/akula/) client, but something more rigorous will be needed before the EIP becomes final.

## Replies

**petertdavies** (2022-02-09):

[@axic](/u/axic) on github:

> This EIP is focused on Mainnet, and can not be used as-is on testnets, because
>
>
> these blocks, if they do exists on a testnet, are containing different transactions
> testnets may have other accounts in inconsistent states

I have added the words “on Mainnet” in a couple of places to clarify this. As explained in the “Other Networks” section, the only testnet that ever had empty accounts is Ropsten. All the others are too new.

Ropsten’s empty accounts were created at genesis and cleared early in its history in entirely straightforward ways, so the EIP applies vanilla to it without having to list special cases. I checked Ropsten by scrolling Etherscan for a bit rather that checking with a sync, so I am less sure than I am for Mainnet though.

---

**axic** (2022-11-12):

> A client may assume that STATICCALLs to empty accounts never occur and that CALLs to empty accounts in STATICCALL contexts never occur.

A `CALL` within a `STATICCALL` context is failing in any case. What is the change/clarification here?

---

**rmeissner** (2022-11-14):

Only if the CALL would change state (e.g. trabsfer eth or update the storage), right?

