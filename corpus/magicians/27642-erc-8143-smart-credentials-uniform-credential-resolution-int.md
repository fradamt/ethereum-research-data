---
source: magicians
topic_id: 27642
title: "ERC-8143: Smart Credentials - Uniform Credential Resolution Interface"
author: nxt3d
date: "2026-02-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8143-smart-credentials-uniform-credential-resolution-interface/27642
views: 18
likes: 0
posts_count: 1
---

# ERC-8143: Smart Credentials - Uniform Credential Resolution Interface

We need metadata records about users (including AI agents) that are not controlled by the user. Records like KYC and Proof of Personhood must be managed by secure third parties, but there’s no unified standard for clients to resolve credentials uniformly.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1504)














####


      `master` ← `nxt3d:smart-credentials`




          opened 05:19PM - 31 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/3857985?v=4)
            nxt3d](https://github.com/nxt3d)



          [+103
            -0](https://github.com/ethereum/ERCs/pull/1504/files)







## Summary

This PR adds ERC Smart Credentials, a specification for blockchain[…](https://github.com/ethereum/ERCs/pull/1504)-based credentials that are resolved via smart contracts. Smart Credentials provide a uniform method for resolving credentials for on-chain identities including human users and AI agents, enabling verifiable facts issued by third parties such as KYC, Proof of Personhood (PoP), and reputation systems.

## Motivation

With the rise of AI agents, users on the internet will become increasingly indistinguishable from AI agents. We need provable on-chain identities that allow real human users to prove their humanity, AI agents to prove who controls them, prove what capabilities they have, and to develop reputations and trust based on their work.

Smart credentials meet a long-felt need to be able to have metadata records about users, including AI agents, that are not controlled by the user. Records like KYC and PoP must be managed by secure third parties. This ERC allows credential issuers to create records about users that can be resolved by clients in a uniform way.

## Specification

The specification defines a minimal interface with a single function:

```solidity
interface ISmartCredential {
    function getCredential(string calldata key) external view returns (bytes memory result);
}
```

- Credentials are resolved using [ERC-3668](./eip-3668.md) for off-chain and cross-chain resolution
- Keys MAY use [ERC-8119](./eip-8119.md) parameterized format (e.g., `kyc: 0x123...` or `kyc: Maria Garcia`)
- Interface ID: `0xd091187f`
- Implements [ERC-165](./eip-165.md) for interface detection via `supportsInterface()`

## Key Features

- **Uniform Interface**: Single function makes it easy for clients to resolve credentials
- **Flexible Key Format**: Supports ERC-8119 parameterized keys for flexible credential identification
- **Cross-Chain Support**: Leverages ERC-3668 for cross-chain and off-chain resolution
- **Privacy-Preserving**: Designed to support Zero Knowledge Proofs (ZKPs)
- **Interoperability**: Enables uniform credential resolution across different issuers and clients

## Use Cases

- **Proof of Personhood (PoP)**: Verify that a user is a human and not an AI agent
- **KYC**: Verify a user's identity from a trusted credential issuer
- **Reputation Systems**: Ratings for AI agents based on work and reviews
- **Privacy-Preserving Proofs**: ZKPs that prove facts without revealing underlying data

## Related ERCs

- Implements: [ERC-165](./eip-165.md) (Standard Interface Detection)
- Requires: [ERC-3668](./eip-3668.md) (CCIP-Read)
- Uses: [ERC-8119](./eip-8119.md) (Key Parameters) for flexible key formats
```












ERC-8143 defines Smart Credentials, a minimal interface with a single function:

```solidity
interface ISmartCredential {
    function getCredential(string calldata key) external view returns (bytes memory result);
}
```

**Use cases**: KYC, Proof of Personhood, reputation systems, and privacy-preserving ZKPs.

**Example**:

```javascript
const credentialBytes = await credentialContract.getCredential("kyc: 0x76F1Ff0186DDb9461890bdb3094AF74A5F24a162");
const credential = decodeCredential(credentialBytes, "(string)");
```
