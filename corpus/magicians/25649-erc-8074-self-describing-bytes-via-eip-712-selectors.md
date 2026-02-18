---
source: magicians
topic_id: 25649
title: "ERC-8074: Self-Describing Bytes via EIP-712 Selectors"
author: awrichardson
date: "2025-10-02"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8074-self-describing-bytes-via-eip-712-selectors/25649
views: 76
likes: 2
posts_count: 1
---

# ERC-8074: Self-Describing Bytes via EIP-712 Selectors

I have a data encoding proposal based on conventions I’ve adopted in my own projects, and I’d like feedback on formalizing it as an ERC.

---

### Motivation

It is common practice for smart contract methods to include an extensibility parameter of type `bytes`, allowing arbitrary additional data to be passed.

Examples of common methods that include a `bytes data` parameter:

- ERC-721 safeTransferFrom
- ERC-777 send and operatorSend, as well as hook operations tokensToSend and tokensReceived
- ERC-1155 safeTransferFrom and safeBatchTransferFrom

This extra data can be used to encode things such as the reason for the transaction, or additional instructions for how it may be processed. In many practical cases, the `bytes` payload may encode a structured type that must be ABI-decoded before it can be processed. However:

- Different contracts use different, ad-hoc conventions for distinguishing among possible payloads.
- A single contract may need to support multiple encodings.
- In more complex workflows, a payload may be propagated across multiple contracts, each of which may need to parse it differently.

Currently, there is no standardized convention for identifying the “type” of an encoded payload, nor for supporting multiple data items in a single `bytes` parameter.

### Proposal

I propose a standardized mechanism for encoding single or multiple structured payloads into a bytes parameter using type selectors.

#### 1. Single Struct Encoding

- Each struct is prefixed with a 4-byte selector.
- The selector is defined as the first 4 bytes of the keccak256 hash of its EIP-712 type string.

Example: a `TransferNote` payload

```auto
struct TransferNote {
  bytes32 reference; // reference code
  string comment;    // free-form note
  uint256 deadline;  // optional deadline (epoch timestamp)
}
```

Type string:

```auto
TransferNote(bytes32 reference,string comment,uint256 deadline)
```

Type hash:

```auto
keccak256("TransferNote(bytes32 reference,string comment,uint256 deadline)")
= 0xf91f3a243a886588394dfd70af07dce0ca18c55e402d76152d4cb300349c9e9d
```

Selector = first 4 bytes = `0xf91f3a24`

Encoding:

```auto
[0xf91f3a24][abi.encode(reference, comment, deadline)]
```

A contract may then look for a known byte sequence before attempting to decode the data, and can easily distinguish between multiple different payloads that it knows how to accept.

#### 2. Multiple Struct Encoding

Define a canonical wrapper type:

```auto
DataList(bytes[] items)
```

Type hash:

```auto
keccak256("DataList(bytes[] items)")
= 0xae74f986bac701873280ae49be4ba8e9fc2515d9dfe8f4fe347c28b0462fc1b1
```

Selector = first 4 bytes = `0xae74f986`

Encoding:

```auto
[0xae74f986][abi.encode(items)]
```

Each element in the `items` array is itself a single-struct payload (with its own selector).

Any implementing contract/application can look for this well-known sequence, and can then decode the list to be scanned iteratively for any recognized items.

### Benefits

- Provides a lightweight, standardized way to identify structured data payloads.
- Makes extensibility safer and more interoperable.
- Allows scanning through a DataList for relevant payloads without ambiguity.
- Builds on EIP-712 conventions, leveraging existing tooling and libraries.

### Open Questions

- Are there existing standards or conventions that already attempt to solve this problem?
- Would this be a good candidate for a new ERC?
- Should the selector scheme use full type hashes instead of truncated 4-bytes (at the cost of larger payloads), or some other identifier entirely?

---

I would appreciate any references to prior art or related discussions, and thoughts on whether formalizing this would be useful as an ERC.
