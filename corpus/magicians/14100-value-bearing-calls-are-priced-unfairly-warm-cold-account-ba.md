---
source: magicians
topic_id: 14100
title: "Value-bearing CALLs are priced unfairly: Warm/Cold Account Balances Proposal"
author: Philogy
date: "2023-05-02"
category: EIPs
tags: [evm, gas]
url: https://ethereum-magicians.org/t/value-bearing-calls-are-priced-unfairly-warm-cold-account-balances-proposal/14100
views: 1136
likes: 4
posts_count: 3
---

# Value-bearing CALLs are priced unfairly: Warm/Cold Account Balances Proposal

## Intro

Every `CALL` within a transaction which sends ETH in the EVM (`value > 0`) costs 6700 more than the equivalent valueless `CALL` would. Intuitively the basic reasoning seems to be that:

> Sending value along with a call incurs some additional overhead because it modifies the recipient’s balance and therefore requires an update of the node and the state trie.

However similar to warm/cold storage reads it seems that for clients this added overhead is constant in practice, in the sense that multiple value-sending `CALL`s to/from the same addresses within a transaction will only require 1 state-trie-node update per account. The unique overhead for a balance change is even less if the account’s state-trie-node already needs to be updated for other reasons like. a storage root change or code change.

## Overview

I’d like to open the discussion around the introduction of a new EIP that’ll introduce cold/warm gas cost dynamics for account balances similar to that of storage slots or accounts themself.

## Motivation

The 6700 gas value-bearing-`CALL` stipend places quite a heavy burden on smart contract wallets such as those working with the [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337) standard as they have to execute multiple payable-`CALL`s per transaction and do so to accounts who’s balance is already being changed in the transaction.

Pricing `CALL` more fairly will make smart contract wallets cheaper and more accessible.

## Rough Proposal

- In every transaction maintain a new set of addresses called warm_account_balances
- At the start of every transaction the from address is added to the warm_account_balances set, the transaction’s to address is also added if the transaction’s value is non-zero
- Whenever a CALL with value > 0 is made:

If both the caller and call-target are already in warm_account_balances no added cost instead of +6,700
- If only one of two are in warm_account_balances add +3,350 to the cost of the CALL
- If neither are in the warm_account_balances set add the existing +6,700 cost
- Add any address that’s part of the call and not in warm_account_balances to the set

If a `CALL` that added addresses to the `warm_account_balances` reverts remove the added addresses from the set

This logic could be made more complex to account for storage root changes and reduce `CALL`s cost there as well but for the sake of implementation simplicity it may be best to leave it like this.

## Feedback & Discussion

Is there some overlooked complexity and overhead that needs to be done upon every value-bearing call? Should it really cost an added +6,700 gas (for reference that’s equivalent to a cold storage slot change +1,700) when it’s just a trie-node update too?

## Replies

**Philogy** (2023-06-06):

I’m deprecating this discussion as EIP-7069 (currently being considered for inclusion in Cancun) fixes this issue by simply not charging more gas for sending ETH via `CALL2`: [EIP-7069: Revamped CALL instructions](https://ethereum-magicians.org/t/eip-7069-revamped-call-instructions/14432)

---

**dror** (2023-06-07):

I agree that value treatment is expensive and different from other storage modifications.

That’s one of the reasons ERC-4337 introduced “deposit”: an account (and paymaster) have a deposit in the EntryPoint contract. sending value to the EntryPoint is equivalent to `depositTo()`. The cost of moving funds out of the deposit (and refund back there the excess at the end) is much lower than sending value back and forth

My suggestion for fixing this issue: make the pricing of value closer to SSTORE rules.

I’m not sure it can be completely the same (e.g. the simple “transfer” costs 21000, regardless of current value zero/nonzero, while SSTORE costs anything between 5000 to 26000 …)

