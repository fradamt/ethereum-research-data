---
source: magicians
topic_id: 10576
title: "EIP-5559: Cross Chain Write Deferral Protocol"
author: paulio
date: "2022-08-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5559-cross-chain-write-deferral-protocol/10576
views: 2822
likes: 3
posts_count: 13
---

# EIP-5559: Cross Chain Write Deferral Protocol

This EIP proposes a new mechanism in which smart contracts can defer various mutations to be handled off chain. Created in conjection with the ENS team, the purpose of this EIP is to standardize a method in which these deferred mutations can be authorized, verified, and executed. One core use case for the Cross Chain Write Deferral Protocol is adding decentralized write support to an off-chain ENS resolver.

[EIP Link](https://eips.ethereum.org/EIPS/eip-5559)

## Replies

**Pandapip1** (2022-08-31):

This is a personal recommendation of mine, but I would highly recommend making the revert reason more succinct due to deployment costs. See [EIP-5289: Ethereum Notary Interface](https://eips.ethereum.org/EIPS/eip-5289) as an example.

---

**paulio** (2022-09-01):

Does it have that large of an impact on deployment costs?

We had originally started with a JSON formatted string for OffChain reversions, but normalized that for ease of implementation.

Let me check this out.

---

**Pandapip1** (2022-09-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/paulio/48/6978_2.png) paulio:

> Does it have that large of an impact on deployment costs?

1kB of data currently costs about $7.50 to store.

---

**paulio** (2022-09-08):

Let me do a parallel implement using the string based encoding to get a more accurate comparison of gas costs associated with deploying the contract.

One of the reasons behind the use of objects in the reversion was to normalize the format of the response to make it easy to decode on the clientside and integrate into wallets. String encoding this would require a more complex encoding function. That function could be pushed to an external library, but increases the overall complexity of the code. Thoughts?

---

**Pandapip1** (2022-09-08):

Seems like an interesting idea. I was thinking more along the lines of [Add EIP-5568: Required Action Signals Using Revert Reasons by Pandapip1 · Pull Request #5568 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5568). Not sure how feasible that is.

---

**paulio** (2022-09-08):

Are you suggesting to remove the reversion error and to just revert the encoded values directly?

---

**Pandapip1** (2022-09-08):

Sort of. Once EIP-5568 is merged, I suggest you use that instead ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12). If you don’t want to wait for it, I suggest you do revert *a form of* the encoded values directly (not the actual values, otherwise it wouldn’t be distinguishable).

---

**doublespending** (2022-10-11):

```auto
A deferred mutation can be handled in as little as two steps. However, in some cases the mutation might be deferred multiple times.

Querying or sending a transaction to the contract
Querying or sending a transaction to the handler using the parameters provided in step 1
```

1. Query L1 contract to write data may confuse users. However, send a transaction to the L1 contract should pay a gas fee.
2. In the view of client, how can it know to use query or send a transaction to the L1 contract.

---

**doublespending** (2022-10-11):

In the case of  `Data Stored in an L2 & an Off-Chain Database`, query L2 contract is better because data is in off-chain database not in L2.

I think `StorageHandledByL2(chainId, contractAddress)` should tell the client query or send a transaction to L2 contract in the next step.

---

**paulio** (2022-10-13):

I guess the correct way  to phrase it would be to say “send a transaction” and in some cases that transaction will fail (in preflighting) but it is always intended to be a write

In the case of `StorageHandledByL2` we want it to support both:

- the data being stored in the L2 (the mutation occures there)
- the data being deferred to an off-chain database

---

**sshmatrix** (2024-04-15):

A superseding version of this has been [proposed here](https://ethereum-magicians.org/t/cross-chain-write-deferral-protocol/19664).

---

**pikonha** (2024-07-11):

Overall, this is a great proposal! However, I have a suggestion for improvement.

During the implementation of a Resolver that follows this EIP, I encountered the following scenario:

I needed to implement a `multicall` function with the following signature:  `function multicall(bytes[] calldata datas) external returns (bytes[] memory)`

I faced challenges with encoding the `Parameter` struct from the `bytes[]` type. Eventually, I encoded the entire `msg.data` into a string to fit the `Parameter.value` specification (string). This approach worked as expected, but it left me questioning why we need a key-value (string:string) mapping for the given parameters when we could simply return its `bytes` format along with the function signature.

Therefore, I propose the following change:

Current structure:

```solidity
struct messageData {
    bytes4 functionSelector;
    address sender;
    parameter[] parameters;
    uint256 expirationTimestamp;
}

struct parameter {
    string name;
    string value;
}
```

Proposed structure:

```solidity
struct messageData {
    bytes callData;
    address sender;
    uint256 expirationTimestamp;
}
```

With this new structure, the function being called and its arguments are ABI encoded, which avoids the need for type casting to string.

