---
source: ethresearch
topic_id: 21056
title: "RFC: Using this.balance as a Storage-Free Deactivation Mechanism Post-Cancun"
author: Zergity
date: "2024-11-21"
category: Security
tags: []
url: https://ethresear.ch/t/rfc-using-this-balance-as-a-storage-free-deactivation-mechanism-post-cancun/21056
views: 215
likes: 1
posts_count: 6
---

# RFC: Using this.balance as a Storage-Free Deactivation Mechanism Post-Cancun

### RFC: Using this.balance as a Storage-Free Deactivation Mechanism Post-Cancun

After the Cancun upgrade and the changes introduced by EIP-6780, the ability to deactivate and reactivate a contract dynamically has become more challenging, particularly in scenarios where querying storage for every transaction is not desirable. I am proposing a minimalistic mechanism for activating and deactivating a contract (specifically a router contract) using the built-in `this.balance` variable as a control flag.

### Use Case

The router contract in question:

- Holds user approvals but no tokens or significant business logic.
- Does not hold ETH in its normal operation.
- Needs a reliable, storage-free way to toggle between an active and inactive state.

This is particularly useful in cases where:

- A bug is identified in the contract, and users need to be prevented from interacting with it until it is fixed.
- There’s a need to deactivate the router swiftly without requiring manual revocation of user approvals.

### Proposed Mechanism

The mechanism relies solely on the contract’s ETH balance (`this.balance`) to toggle its state. The logic is as follows:

1. State Definition:

- Deactivated: this.balance == 0. The contract rejects all interactions.
- Activated: this.balance == 1 wei. The contract functions normally.

1. State Transitions:

- Activate the Contract: The activate() function (restricted to an immutable DEACTIVATOR address) sends 1 wei to the contract, setting it to an active state.
- Deactivate the Contract: The deactivate() function (also restricted) transfers all ETH in the contract back to the DEACTIVATOR, setting the balance to zero.

1. Key Features:

- The router has no receive function, ensuring that ETH cannot be accidentally or maliciously sent to it.
- All state transitions rely exclusively on the ETH balance, eliminating the need to query or store custom state variables.

### Benefits

1. No Storage Reads: State checking relies on this.balance, avoiding the gas cost of reading from storage.
2. Efficient State Transitions: Activating or deactivating involves only minimal ETH transfers.
3. Safety: The absence of a receive function ensures the router cannot accidentally accumulate ETH.

### Why This Is Useful

This mechanism provides a lightweight way to handle router deactivation, especially in scenarios where:

- Bugs in router contracts force users to manually revoke approvals.
- State querying for every transaction is undesirable due to gas costs or complexity.

Using the contract’s ETH balance as a toggle avoids the need for storage variables while enabling quick and efficient state changes. This approach could benefit other contract designs requiring similar activation/deactivation mechanisms in a storage-free context.

## Replies

**abcoathup** (2024-11-22):

You can still send funds to a contract, allowing this mechanism to be manipulated

From: [Introduction to Smart Contracts — Solidity 0.8.28 documentation](https://docs.soliditylang.org/en/v0.8.28/introduction-to-smart-contracts.html#deactivate-and-self-destruct)

> From EVM >= Cancun onwards, selfdestruct will only send all Ether in the account to the given recipient and not destroy the contract.

---

**Zergity** (2024-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/abcoathup/48/5778_2.png) abcoathup:

> You can still send funds to a contract, allowing this mechanism to be manipulated

Not without `receive` or `fallback`:

> If neither a receive Ether nor a payable fallback function is present, the contract cannot receive Ether through a transaction that does not represent a payable function call and throws an exception.

https://docs.soliditylang.org/en/latest/contracts.html#receive-ether-function

---

**abcoathup** (2024-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/zergity/48/5716_2.png) Zergity:

> Not without receive or fallback:

A contract can receive Ether without a receive function as a destination of a selfdestruct.  See the documentation warning.

> A contract without a receive Ether function can receive Ether as a recipient of a coinbase transaction (aka miner block reward) or as a destination of a selfdestruct.
>
>
> A contract cannot react to such Ether transfers and thus also cannot reject them. This is a design choice of the EVM and Solidity cannot work around it.

From: [Contracts — Solidity 0.8.29 documentation](https://docs.soliditylang.org/en/latest/contracts.html#receive-ether-function)

---

**Zergity** (2024-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/abcoathup/48/5778_2.png) abcoathup:

> A contract without a receive Ether function can receive Ether as a recipient of a coinbase transaction (aka miner block reward) or as a destination of a selfdestruct.
>
>
> A contract cannot react to such Ether transfers and thus also cannot reject them. This is a design choice of the EVM and Solidity cannot work around it.

Oh shoot! Thanks for pointing that out.

---

**Zergity** (2024-11-25):

### Update: Fixing the SELFDESTRUCT and Miner Coinbase Problem

Thanks, [@abcoathup](/u/abcoathup) for pointing out the possible attack: ETH can still be sent to the contract using `SELFDESTRUCT` or as part of a miner’s coinbase transaction. This would mess up the balance-based activation logic since the contract could end up with an unexpected balance.

Here’s the fix:

Change the state to:

- Active: balance == 0
- Deactivated: balance > 0

Add an `s_deactivated` flag that is only checked when the `balance > 0`. In this case:

- If s_deactivated == true: revert the transaction with Deactivated reason.
- If s_deactivated == false: transfer the this.balance to DEACTIVATOR to ensure the balance is consistent with the s_deactivated flag. And continue with the transaction as normal.

