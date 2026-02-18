---
source: magicians
topic_id: 4337
title: EIP-? Native Batched Transactions
author: PhABC
date: "2020-06-04"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-native-batched-transactions/4337
views: 1898
likes: 2
posts_count: 5
---

# EIP-? Native Batched Transactions

There have been many discussions about how to improve the UX when it comes to EOA, such has integrating [native transaction delegation](https://github.com/ethereum/EIPs/issues/1035), [rich transactions](https://ethereum-magicians.org/t/rich-transactions-via-evm-bytecode-execution-from-externally-owned-accounts/4025) and more.

Another approach would be to allow EOA to execute atomic batch transactions, where only one nonce and one signature would be provided for a given batch of transactions. This would allow users to do things like Approve + call (for ERC20) in a single batch, or buy an asset in one dex to send it elsewhere after.  This is a pattern that is common in smart contract wallets and has proved very powerful when it comes to UX and cost optimisation.

To support this, the transaction object passed to `eth_sendTransaction` could be changed from:

```auto
export type Transaction = {
  from: string;
  to: string;
  gas?: number;
  gasPrice?: number;
  value?: number;
  data:  string;
  nonce?: number;
}
```

to something like this:

```auto
export type Transaction = {
  from: string;
  to: string | string[];
  gas?: number | number[];
  gasPrice?: number | number[];
  value?: number  | number[];
  data:  string | string[];
  nonce?: number;
}
```

If arrays are provided, they all must of of same length. Could also use default values for the optional fields. There is always a single nonce and a single signature, which ensures that all calls are executed within a transaction, providing atomicity. Nodes can then execute sequentially the calls provided in a given transaction.

That’s about it! I was curious if there was already an EIP for this and what other people thought of this approach.

## Replies

**kohshiba** (2020-06-06):

This is interesting. My concern is that it easily runs out of gas and go beyond the gas limit. We need to approach this issue.

---

**Arachnid** (2020-06-07):

What are the advantages over my proposed scheme? From my perspective, it seems more involved (insofar as it requires changes to a consensus data structure) and less flexible.

---

**PhABC** (2020-06-08):

[@Arachnid](/u/arachnid)

> What are the advantages over my proposed scheme? From my perspective, it seems more involved (insofar as it requires changes to a consensus data structure) and less flexible.

To me, the main advantages would be

1. Less security considerations (no need to worry/debate if EOA should have a state, etc.)
2. Easier for clients to benefit from since they don’t need to write contracts code to do complex txs, just just put in an array the transactions they want to execute.
3. Cheaper calls for most use cases (my guess), since you don’t need to pass contract code, just calldata for each tx.

It is indeed less expressive than rich-transactions, but I don’t see them as mutually exclusive proposals.

---

**anna-carroll** (2023-10-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/phabc/48/81_2.png) PhABC:

> This would allow users to do things like Approve + call (for ERC20) in a single batch, or buy an asset in one dex to send it elsewhere after. This is a pattern that is common in smart contract wallets and has proved very powerful when it comes to UX and cost optimisation.

Came here to say I think this proposal is cool for these exact reasons.

Batching calls from EOAs is obviously a problem that has motivated other ERCs like

- ERC-677 - ERC20-specific and insufficient because of deep liquidity in normal ERC-20s
- EIP-6357 - insufficient because it’s often desirable to batch calls to different contracts

And probably many more.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> it seems more involved (insofar as it requires changes to a consensus data structure)

Would this be easier to implement after [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718) was included in Berlin?

