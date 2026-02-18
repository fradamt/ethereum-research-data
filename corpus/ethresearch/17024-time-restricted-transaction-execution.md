---
source: ethresearch
topic_id: 17024
title: Time Restricted Transaction Execution
author: Joseph
date: "2023-10-09"
category: UI/UX
tags: []
url: https://ethresear.ch/t/time-restricted-transaction-execution/17024
views: 1902
likes: 13
posts_count: 9
---

# Time Restricted Transaction Execution

# Time Restricted Transaction Execution

Add a new field `minStartTime` to the transaction signature that replicates the behavior of a `nonce`. When this value is set, it creates a time delay for the transaction in which the block producer cannot include the transaction.

`minStartTime` is a `uint256` epoch timestamp at which the transaction will become valid

Signature layout:

```auto
[nonce, minStartTime, gasPrice, gasLimit, to, value, data]
```

Example logic for transaction exclusion:

```auto
if(msg.minStartTime < block.timestamp)
```

A block observed that includes a `msg.minStartTime` lower than `block.timestamp` of the block the transaction is included in should be rejected by implementing nodes.

Based on some early feedback, I am modifying this proposal with rules for mempool inclusion.

Let’s deem a `minStartTime` of 0 to be a special case that implies the transaction signer does not want to set a future `minStartTime` and can be included in a block immediately.

Using standard inclusion rules for mempool, transactions that have a `nonce` lower than the account’s current nonce will be dropped from mempool. Meaning the user can submit multiple transactions with the first included transaction invalidating the other transactions in mempool.

Mempool inclusion should be restricted to a single transaction with a `msg.minStartTime > 0`. This will prevent having multiple transactions in mempool at the same time. If two transactions arrive with `msg.minStartTime > 0`, the node should select the transaction with the lowest `msg.minStartTime`.

Using heuristics within mempool will be key to prevent transaction with `msg.minStartTime > 0` where the `msg.minStartTime` is set arbitrarily high ex: 10 years. Each transaction should be restricted to `block.timestamp + 1 days`.

## Replies

**Joseph** (2023-10-09):

I just want to assuage anyone’s fears that this could be done at the contract layer, it cannot. A transaction executable as a metatransaction with a `minStartTime` would still be executable before `minStartTime` and would only result in a failed transaction execution when it encountered the revert condition for `minStartTime`.

This user experience improvement would require a protocol change to the signature schema.

---

**kladkogex** (2023-10-09):

It definitely does make sense, and we are considering adding a feature like this to SKALE.

It is much cleaner for the user, because the user has assurance that if a transaction is not executed within a fixed period of time, it will never be executed

---

**MicahZoltu** (2023-10-10):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> the user has assurance that if a transaction is not executed within a fixed period of time, it will never be executed

This sounds like the opposite of what is being proposed here.  This proposal is suggesting that a transaction must be included *after* `timestamp`, not that it must be included *before* `timestamp`.

---

**ariutokintumi** (2023-10-14):

gm [@Joseph](/u/joseph),

I’ve been pondering the use case for time-restricted transaction execution and have identified some potential challenges with the described functionality:

**Problems:**

1. Gas Estimation: Predicting gas for future blocks is inherently uncertain. A transaction intended for execution within a specific timeframe (e.g., within 24 hours as per your statement) might either never get processed due to gas constraints and might requiere a significantly higher gas fee than anticipated. This also assumes the feasibility of a “free mempool exit,” which is currently not achievable.
2. Transaction Replacement Conditions: Introducing a time condition complicates the rules for transaction (nonce) replacement. The new criteria would be: IF “gasPrice + priority fee >= (previous gasPrice + priority fee) * 1.1” AND IF “new time < previous time”.
3. Transaction Selection by Nodes: Nodes prioritize pending transactions based on nonce. Given that multiple valid transactions with the same nonce cannot coexist, the current architecture doesn’t allow for any other selection criteria besides gasPrice.

However, I believe there are existing solutions that can achieve the desired behavior:

**Solutions:**

1. Off-chain Services: Use an off-chain service to send the transaction with the appropriate gas amount at the desired execution time. Several such services are available.
2. Win a hackathon budling a SAFE + oSnap from UMA for this: Configure your SAFE with the oSnap feature for the transaction in question.

I hope this feedback aids in refining your proposal. I’m eager to contribute further insights if needed.

Additionally, [@kladkogex](/u/kladkogex), I find your approach intriguing. The idea of setting a high gas limit to ensure transaction execution or limiting both gas and time is innovative. However, it introduces potential challenges, especially when considering nonce management and transaction replacement. I’d be interested in delving deeper into this topic in a separate discussion.

---

**xinbenlv** (2023-10-16):

Generally in favor of the direction of this proposal.

A somewhat relevant proposal: [EIP-5081: Expirable Trainsaction](https://eips.ethereum.org/EIPS/eip-5081)

---

**DHannum8** (2023-10-17):

Would add GasHawk as a potential solution here as well (Disclaimer CEO)

We have built algorithms that allow us to predict and execute at the lowest base fee over any time interval which saves both users and institutions on fees/TX costs. We also prevent failed and stuck TXs and allow a user or institution to set their time sensitivity.

Would be happy to chat further on this topic!

---

**Piotruscik** (2023-10-31):

Isn’t it already possibile on contract layer by using account abstraction (ERC-4337)? The validating function (validateUserOp) can return:

validUntil is 6-byte timestamp value, or zero for “infinite”. The UserOp is valid only up to this time.

validAfter is 6-byte timestamp. The UserOp is valid only after this time.

---

**jonhubby** (2025-09-03):

The idea of adding a `minStartTime` field makes sense for cases where you want a built-in delay without extra scheduling tools. Using `0` as the “immediate execution” default feels like a clean way to handle backwards compatibility.

Restricting the mempool to just one `minStartTime > 0` transaction seems like a reasonable way to avoid conflicts, and the 1-day cap is a good safeguard against extreme values. For a broader context, this kind of design consideration is similar to how UX patterns are approached in other domains (e.g., [UI/UX design practices](https://ideamaker.agency/ui-ux/)), where clear defaults and limits help prevent confusion or misuse.

