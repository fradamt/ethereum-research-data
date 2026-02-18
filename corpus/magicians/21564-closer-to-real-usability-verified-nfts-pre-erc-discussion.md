---
source: magicians
topic_id: 21564
title: "Closer to real usability: Verified NFTs pre-ERC discussion"
author: tms1337
date: "2024-11-03"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/closer-to-real-usability-verified-nfts-pre-erc-discussion/21564
views: 82
likes: 6
posts_count: 5
---

# Closer to real usability: Verified NFTs pre-ERC discussion

# Discussion on Verified NFTs with Encrypted UIDs

Hello everyone,

I’m excited to share an idea I’ve been working on regarding verified NFTs that incorporate encrypted storage for their unique identifiers (UIDs). I plan to open an ERC and draft a PR for this standard, but I wanted to discuss the concept here first to gather initial feedback before submitting a more polished version.

## The Concept

The core idea is to create a standard for NFTs where each token’s UID is encrypted. Only those who have been given the decryption key can access the UID, providing an extra layer of security and privacy. I have resolved most of the technicalities, but I want to avoid introducing bias into the conversation too early, so some details from my initial plan are left out for now.

### Key Features:

1. Privacy: Only authorized users can access the UIDs, keeping ownership details secure.
2. Verification: The ownership and authenticity of the NFT can still be verified on-chain, ensuring the integrity of the asset.
3. Interoperability: This standard would align with existing NFT protocols (like ERC721 and ERC1155), making it easy to integrate.
4. Original Creator Verification: We want to ensure that the original creator can be verified via a digital signature, similar to how an artist or author certifies their work. This adds an additional layer of trust and authenticity.

## Implementation Details

- Encryption Method: The UIDs would be encrypted using a robust algorithm (e.g., AES) to ensure security.
- Key Management: We’ll implement a secure method for distributing the decryption keys to authorized users, possibly leveraging existing wallet infrastructure.
- On-Chain Verification: The NFT’s smart contract would include functions for verifying ownership while maintaining the privacy of the UID.

## Potential Use Cases

- Digital Art: Artists can protect their identities and proprietary information while still allowing collectors to verify ownership.
- Gaming: Players can have privacy regarding their in-game assets, making it harder for malicious actors to exploit their information.
- Collectibles: Collectors can feel more secure in their purchases, knowing that their ownership details are not publicly accessible.

## Seeking Feedback

I’d love to hear your thoughts on this idea! What do you think about the implementation challenges? Are there existing projects that might be similar, and how do you envision this impacting the NFT landscape?

Looking forward to your insights!

## Replies

**hellohanchen** (2024-11-03):

Very interesting idea.

I have a not quite similar but idea that can leverage this solution: using it on testament.

From technical perspective, what if the UID is leaked through social engineering but not crypto hacking, will the owner lost the value of the NFT in anyway?

---

**tms1337** (2024-11-03):

Agree that this is edge case but can not think of failproof solution, since dealing with digital data once either UID or plain text leaks, it is forever leaked.

Yet will think about potential solutions, either partial or full if even possible.

That said, still we could make it so that at least we know which key leaked I think, will update on this (is part of initial thoughts on this).

cc [@hellohanchen](/u/hellohanchen)

---

**cypherpepe** (2024-11-03):

How does the proposed standard plan to ensure compatibility between encrypted UID NFTs and existing protocols (e.g., ERC721, ERC1155) to maintain functionality and ease of use?

---

**tms1337** (2024-11-04):

Hey @cypher_frog,

You’re totally right to think about compatibility with existing standards like ERC721 and ERC1155—it’s a big priority for this idea.

Your further input appreaciated ofc.

Here’s how we’re thinking about it:

### Current UID Format

In ERC721 and ERC1155 standards, each token has a unique identifier (UID), typically a `uint256` value, which tracks ownership and metadata, ensuring each token’s uniqueness.

### Encrypted UID Format

With encryption, the UID would be stored in a secure, encrypted format, likely as a `bytes` array. This ensures that only those with the decryption key can access the original UID, adding a layer of privacy.

### Reconciling Formats for Compatibility

To maintain compatibility with existing systems:

1. Hashing for Consistency: We can hash the encrypted UID (e.g., using SHA-256) to create a fixed-size output, which we use as a proxy UID. This hashed value can fit within the existing uint256 format required by ERC721 and ERC1155.
2. Mapping Encrypted to Proxy UIDs: The smart contract can hold a mapping linking the proxy UID (hashed value) to the actual encrypted UID. This lets us use the proxy UID in standard operations while preserving the original encrypted UID.

### Implementation Steps

- Hashing: During minting, we’d encrypt the UID and then hash it to generate the proxy UID.
- Storage: Maintain a mapping in the contract from proxy UID to encrypted UID.
- Standard Functions: Functions like ownerOf and balanceOf would operate on the proxy UID, ensuring compatibility with existing interfaces.

This approach keeps encrypted UID NFTs compatible with ERC721 and ERC1155 protocols while preserving functionality and usability. Looking forward to your thoughts!

