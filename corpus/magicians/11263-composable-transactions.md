---
source: magicians
topic_id: 11263
title: Composable Transactions
author: bernardo
date: "2022-10-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/composable-transactions/11263
views: 1335
likes: 4
posts_count: 5
---

# Composable Transactions

[![ComposableTransactions](https://ethereum-magicians.org/uploads/default/original/2X/c/caa7f38399e657bc1237740fa9cf8bde13826846.png)ComposableTransactions512×446 46 KB](https://ethereum-magicians.org/uploads/default/caa7f38399e657bc1237740fa9cf8bde13826846)

Normal transactions can make only a single call to a smart contract. This means that when we need to call a function many times, or interact with different smart contracts, we need a separate transaction for each smart contract interaction.

Composable Transactions bring the ability to **make many calls in a single transaction**, either to the same or to different smart contracts.

Even more than just calls, this feature allows **a variety of commands** to be executed, including storing the result of a call into a (temporary) variable, conversion of the value, math operations, and assertion (reverts the whole transaction if evaluates to `false`)

## Characteristics

1. Multiple calls
2. Atomicity
3. Sequential execution
4. Act on current state
5. Scripting
6. No blind signing

### Atomicity

If any of the calls fail, the entire transaction is aborted.

This means that either all calls succeed or none of them.

### Sequential Execution

Execute a series of contract calls with the guarantee that they happen sequentially with no external action occurring between them.

### Act on current state

Do actions using the current values from contracts and account states by making queries to contracts and using the returned value on the same transaction.

This is useful when another transaction arrives first and changes the contract state.

### Scripting

Instead of just a list of calls, it is possible to process the returned values and act according to them.

The language supports data conversion and manipulation, assertion, conditional execution, and more.

### No Blind Signing

The transaction can be reviewed even on hardware wallets before approval or rejection

The user can check each command and its arguments

The scripts contain the function signature (human readable). The function selector is computed at execution time

## Use Cases

**1)** Purchase airplane tickets and hotel reservation from different contracts, only if both succeed. If some of the purchases fail, the other is reverted (the user does not want one of them if the other is not acquired)

**2)** Swap token and buy something with it. If the purchase fails, the user does not want that intermediary token

**3)** Transferring token (fungible and/or non-fungible) to multiple recipients at the same time

**4)** Transferring different tokens (fungible and/or non-fungible) to one recipient in a single transaction

**5)** Mint many non-fungible tokens (NFTs) in a single transaction

**6)** Trustless swap (or purchase): check if the purchased token was received, otherwise revert the transaction

**7)** Swap tokens using a split route. Check the minimum output in the transaction itself and revert if not satisfied

**8)** Swap to an exact amount of the output token when using a multi-hop route, by querying a contract for the right amount to send in the same transaction

**9)** Approve contract B to use contract A (token) and then call a function on contract B that handles the resources on contract A (eg: approve and swap, approve and add liquidity) on a single transaction

**10)** Approve, use resource, and remove approval on a single transaction, with the guarantee that no other operation would happen in between while the resource/token is approved to contract B

**It also allows** (by creating compatible smart contracts):

**11)** Swap tokens **without approval**

**12)** Add liquidity to a pool (2 tokens) in a single transaction **without approval**

**13)** Multisig wallet users and DAO users can create and vote on an entire script of commands

## Implementation

### Client Side

As most clients use web-browsers, the scripts are built in JSON format, like this one:

```javascript
[
["call","","transfer(address,uint256)","",""],
["call","","transfer(address,uint256)","",""],
["call","","transfer(address,uint256)","",""]
]
```

As this format is not efficiently processed by EVM code, it is then converted to binary format using a small library on the browser (or another environment)

The converted script in binary format is then included in the transaction as the payload

The transaction is marked with a special “type” to differentiate from normal transactions.

The current test implementation uses this method:

- recipient address := signer address
- amount := 0
- payload := binary script

But it can have some other method, like a explicit type (MULTICALL or SCRIPT …)

### Execution Side

The execution client can identify these transactions and process them accordingly

The current implementation uses a smart contract to parse and execute the binary script / commands

There is no reference to this contract on the transaction

The execution client calls a function on this contract passing the binary script as argument.

The call is made using the CALLCODE opcode (0xF2) executed as the caller account.

The binary format is engineered to minimize gas usage when processed

### Usage by Contracts

As the script executor is a smart contract, other contracts can also interface with it using the DELEGATECALL opcode (0xF4) and passing the script as argument.

One use would be by MultiSig wallets and DAOs, in which scripts can be stored, reviewed, voted, and only executed when/if approved.

## Other resources

- Scripts
- Complete list of commands
- Example Scripts for Specific Use Cases
- Human-readable display of amounts
- Display on hardware wallets
- Templates

## Other discussion places

As the goal is to implement a single (or very similar) specification that can be used on most EVM-compatible blockchains (to make dApps simpler) there are separate discussions with different teams from other blockchain projects and we have also [a common channel](https://discord.com/channels/1022349347540697128/1022349347993686017) in which anyone can come together to share thoughts for cross-chain compatibility

## Replies

**bernardo** (2022-10-09):

Related proposals:

[“Rich transactions” via EVM bytecode execution from externally owned accounts](https://ethereum-magicians.org/t/rich-transactions-via-evm-bytecode-execution-from-externally-owned-accounts/4025)

[Native Batched Transactions](https://ethereum-magicians.org/t/eip-native-batched-transactions/4337)

[EIP-2733: Transaction Package](https://ethereum-magicians.org/t/eip-2733-transaction-package/4365)

---

**unenunciate** (2022-10-09):

While they don’t work with EOAs, 4337 user operations already achieve this.

---

**dadabit** (2022-10-15):

Wouldn’t be easier and straightforward deploying an orchestrator contract to make a single entry point to trigger many transactions?

---

**bernardo** (2022-10-16):

1. What do you mean by “orchestrator contract”? Something like the existing multicall contracts? How to call it under the EOA? Notice that the changes on the executor are exactly for that purpose, using the CALLCODE opcode.
2. By “make a single entry point to trigger many transactions” do you mean to trigger many calls from the sent transaction?

Notice also that our approach goes beyond just contract calls. The supported operations allow a range of new use cases, that are not possible with just a list of contract calls

