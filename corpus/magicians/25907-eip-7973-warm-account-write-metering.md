---
source: magicians
topic_id: 25907
title: "EIP-7973: Warm Account Write Metering"
author: charles-cooper
date: "2025-10-21"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-7973-warm-account-write-metering/25907
views: 44
likes: 1
posts_count: 2
---

# EIP-7973: Warm Account Write Metering

discussions thread for [EIP-7973: Warm Account Write Metering](https://eips.ethereum.org/EIPS/eip-7973) (original PR: [Add EIP: Warm Account Write Metering by charles-cooper · Pull Request #9900 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9900))

## Replies

**jochem-brouwer** (2025-11-19):

Hiya! Some feedback:

From the abstract:

> Namely, if one of the account fields (nonce , value , codehash ) is changed more than once in a transaction, the later writes are cheaper, since the state root update only happens once.

I think `storage_root` should also be part of this? If you first storage update and then send ETH to it then you also want this “discount”. (Maybe also use `code_hash` instead of `codehash`?)

From the specification section:

`GAS_STORAGE_UPDATE`: I don’t know what this constant is. I’m not sure what it would be in the current EVM.

I did not check the SSTORE code but this seems to be mostly EIP-2200 code. I think a “diff” here might be more helpful? This would show the original EIP-2200 code and then the changes to it (to point out what actually changes).

> On the account-updating opcodes CREATE , CREATE2 , and *CALL , instead of charging GAS_CALL_VALUE :

I think `SENDALL` needs to be added here.

> For compatibility with EIP-7928 and parallel execution, if the accessed account shows updates in the Block-Level Access List (BAL) in a transaction indexed before the current transaction, then the values to compare against are taken from this entry instead of the account trie.

I’m not entirely sure what this means or what changes here. I think the point made here is to take the “original” storage values as they would be before this transaction. Also I think the point here made is that the “changed accounts” are cleared after each transaction?

The EIP states that we charge cold write cost if the storage items are the same as at the start of the transaction. So, if account A calls B (with value) this charges cold gas. Now B will send the amount just sent back to A. A, will now again call B (with value). By the current definition this means that we charge cold gas again. Is this correct?

