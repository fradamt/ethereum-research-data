---
source: magicians
topic_id: 15106
title: "EIP-7361: Metadata Hash extension with Decentralized Validation"
author: pugakn
date: "2023-07-18"
category: EIPs
tags: [erc, erc-721, metadata]
url: https://ethereum-magicians.org/t/eip-7361-metadata-hash-extension-with-decentralized-validation/15106
views: 645
likes: 3
posts_count: 4
---

# EIP-7361: Metadata Hash extension with Decentralized Validation

Hi, I’m proposing this EIP, this is my first time submitting one, so any comments or thoughts are welcome!

https://github.com/ethereum/EIPs/pull/7361

## Abstract

The proposed extension pairs a tokenId with a metadataHash to facilitate secure off-chain metadata storage and a mechanism for consistency checks. The proposal addresses potential challenges related to metadata reconstruction, off-chain storage security, owner/operator dependence, and data privacy.

## Motivation

The ERC-721 standard requires a more secure and efficient way to handle metadata, particularly when large or sensitive. By introducing a method to pair each tokenId with a metadataHash, and providing a decentralized mechanism for metadata consistency validation, we can enhance data security and reduce on-chain storage needs.

## Specification

**MetadataHash**

This function returns a cryptographic, collision-resistant hash of the metadata for a given tokenId.

```solidity
function metadataHash(uint256 tokenId) external view returns (bytes32);
```

**SetMetadataHash**

This function sets the metadataHash for a given tokenId. This function is only callable by the contract owner or an approved operator. The function also emits a MetadataHashSet event.

```solidity
function setMetadataHash(uint256 tokenId, bytes32 hash) external;
```

**MetadataHashValidator**

This function allows any user to validate the consistency of the metadata against its hash. This function facilitates decentralization and reduces dependence on the token’s owner or approved operator.

```solidity
function metadataHashValidator(uint256 tokenId, bytes metadata) external view returns (bool);
```

**Event**

This event is emitted when the metadataHash of a tokenId is set or updated.

```solidity
event MetadataHashSet(uint256 indexed tokenId, bytes32 metadataHash);
```

## Rationale

The proposal introduces functions for unique hash value generation for each tokenId, secure metadata hash setting by contract owner or operator, and metadata consistency validation by any user. These mechanisms enhance data security and promote decentralization.

## Backwards Compatibility

This EIP is fully backward compatible as it extends the existing ERC-721 standard. The base functionality of ERC-721 tokens is not modified or impacted.

## Test Cases

Test cases will be added where the new functions and event are tested to ensure they function as expected.

## Reference Implementation

A reference implementation will be provided when this EIP moves to the “Final” stage.

## Security Considerations

This EIP improves the integrity of off-chain metadata and the overall security of the ERC-721 token standard. However, the quality of this security depends on the implementation of hash functions, the safety of off-chain storage, and the proper use of the MetadataHashValidator function. It’s recommended for token owners, operators, and users to follow best practices in these areas.

**Data Privacy Considerations**

The privacy of off-chain metadata should be ensured through appropriate data protection measures during storage and transmission. The hash function should be selected so that reverse-engineering the metadata from the hash is computationally unfeasible.

This proposal should encourage community discussion around improving the handling and security of metadata in the ERC-721 standard. It aims to address multiple concerns and strikes a balance between on-chain and off-chain storage, security, and the decentralization of validation.

## Replies

**sullof** (2023-07-20):

Your point is valid and this proposal does open up the opportunity for developers to store metadata on mutable servers while still ensuring its integrity. The downside is the high cost associated with it on chains like Ethereum mainnet.

Have you considered using a Merkle tree structure?

By storing only the root of the Merkle tree in the smart contract, users could verify whether the hash of the metadata (possibly obtained via keccak256(JSON.stringify(metadata))) is included in the Merkle tree providing the proof. This proof could be stored on IPFS, Arweave or even provided by a trusted authority or the project itself (as long as the root is not updatable).

BTW, I just read this

https://twitter.com/onnnnnnnion/status/1681771176664907776

---

**pugakn** (2023-07-21):

Oh, thanks! [@sullof](/u/sullof) The Merkle proof idea sounds very interesting. It makes sense for ETH mainnet because yeah the gas cost of minting would be almost double, although for other chains maybe it would be overcomplicated for developers because they would need to create and maintain the Merkle tree and proofs, also it would be technically less secure because you would always need to rely on a “trusted” source to generate and store the tree and proofs; I’ve never done that so not sure if it is actually that overcomplicated though.

Maybe we could make both standards that are optimized for different use cases/chains. What do you think?

---

**pugakn** (2023-07-21):

Oh the contract from that tweet is pretty great to save gas.

- Open metadata contract combined with this EIP would cost almost the same gas as the current contract’s mints with tokenURI but with the benefits of this EIP
- Open metadata contract combined with the Merkle proofs would cost very little gas with the addition of the security and privacy capabilities.

