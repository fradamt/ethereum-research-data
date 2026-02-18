---
source: magicians
topic_id: 14127
title: "Smart contract properties and metadata: what structure to use when?"
author: MidnightLightning
date: "2023-05-04"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/smart-contract-properties-and-metadata-what-structure-to-use-when/14127
views: 465
likes: 0
posts_count: 1
---

# Smart contract properties and metadata: what structure to use when?

Thinking through the different ways smart contracts present properties/metadata about themselves, I realized there’s a few different styles/standards:

# ERC20-style

The `symbol`, `name`, and `decimals` properties of an [ERC20 token](https://eips.ethereum.org/EIPS/eip-20) are revealed as functions that are just their names (i.e. not `getSymbol`), and return a string.

- Pros: Can be static strings, can be read by other smart contracts
- Cons: Cannot be extended (must choose all the properties at the deploy of the contract)

# ENS-style

[ERC634](https://eips.ethereum.org/EIPS/eip-634) defines a `text(bytes32 node, string key) view returns (string text)` function. This allows any `key` to be input and receive a value back.

- Pros: Infinitely expandable, can be read by other smart contracts
- Cons: No built-in iteration/enumeration, need Events to know what custom properties have been set

# JSON

The [ERC72 Metadata](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md) standard indicates a JSON structure that could be returned from the `tokenURI` function.

- Pros: Relatively human-friendly to read
- Cons: No native builder in solidity, other smart contracts cannot use this data

---

In my experience, the “ERC20-style” is good for simple implementations that will only have a fixed set of properties (and in general, don’t put a `get` prefix on the name of the function when building this style).

For future-proofing, and allowing user customization, the “ERC634-style” seems strongest. However, it seems many projects gravitate toward the JSON-style output. For contracts that want to generate that JSON on-chain, it becomes more complicated, and the result cannot be read by other smart contracts.

Instead of JSON, why not something even easier for solidity to do (CSV or other text-delimited style)? Or why not more compact format (Protocol Buffers, or EVM ABI-encoded format)?

ERC634 could be aided by multi-call functions:

```auto
function text(bytes32 node, string[] keys) view returns (string[] values)
```

To return multiple values for a single node), and optional “enumeration” extension (like ERC721, to iterate by index through the key/value pairs for a node:

```auto
function textOfNodeByIndex(bytes32 node, uint256 index) view returns (string key, string value)
```

Or a “get all” function:

```auto
function textsOfNode(bytes32 node) view returns (string[] key, string[] value)
```

---

These example “metadata” structures have been built into other standards. Should there be an EIP for generalized property storage? Or an overall “best practices” set of guidelines contract authors should generally adhere to (similar to how Java programming typically has “getters” and “setters” on classes, that by convention start with “get” and “set”)?
