---
source: magicians
topic_id: 25656
title: "ERC-8041: Fixed-Supply Agent NFT Collections"
author: nxt3d
date: "2025-10-03"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8041-fixed-supply-agent-nft-collections/25656
views: 620
likes: 5
posts_count: 3
---

# ERC-8041: Fixed-Supply Agent NFT Collections

This standard introduces an interface for creating fixed-supply collections of ERC-8004 Agent NFTs with mint number tracking and onchain collection metadata.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1237)














####


      `master` ← `nxt3d:onchain-metadata`




          opened 12:13PM - 03 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/3857985?v=4)
            nxt3d](https://github.com/nxt3d)



          [+263
            -0](https://github.com/ethereum/ERCs/pull/1237/files)







## Add ERC-8041: Fixed-Supply Agent NFT Collections

### Summary
This PR intr[…](https://github.com/ethereum/ERCs/pull/1237)oduces ERC-8041, a standard for creating fixed-supply collections of ERC-8004 Agent NFTs with mint number tracking.

### Motivation
While ERC-8004 provides unlimited minting for AI Agent identities, many use cases require limited collections (e.g., "Genesis 100", "Season 1"). ERC-8041 addresses this need by defining a standard interface for fixed-supply collections.

### Key Features
- **Fixed Supply Limits**: Define maximum number of agents per collection
- **Mint Number Tracking**: Permanent tracking of each agent's position (e.g., "5 of 1000")
- **Onchain Collection Metadata**: Links agents to their collections via the `"agent-collection"` metadata key
- **Time-Gated Releases**: Collections can activate at specific block numbers

### Technical Details
Core interface includes:
- `getAgentMintNumber(uint256 agentId)` - Returns agent's position in collection
- `getCollectionDetails()` - Returns supply info and collection status
- Events: `CollectionCreated`, `AgentMinted`

### Compatibility
- **Requires**: ERC-8004
- **Compatible with**: ERC-721

---

### Note on Direction Change
This ERC represents a strategic shift in approach. Originally, ERC-8041 was planned as a standalone contract-level metadata standard. We've pivoted to instead leverage the existing Onchain Metadata functionality of ERC-8004, focusing on a specific application (fixed-supply agent collections) rather than the underlying metadata infrastructure.

This decision prioritizes implementation speed by repurposing the existing ERC number rather than submitting a new proposal and going through the numbering process again. This allows immediate adoption of onchain metadata capabilities using ERC-8004 registries with the `agent-collection` metadata key. A future ERC will standardize the Onchain Metadata interface itself.












### Summary

This PR introduces an interface for creating fixed-supply collections of ERC-8004 Agent NFTs with mint number tracking and onchain collection metadata.

While ERC-8004 provides an unlimited mint registry for AI Agent identities, many use cases require limited collections (e.g., “Genesis 100”, “Season 1”). ERC-8041 addresses this need by defining a standard interface for fixed-supply collections that leverage ERC-8004’s existing onchain metadata capabilities.

The ERC defines:

- getAgentMintNumber(tokenId) - Returns an agent’s permanent position in the collection (e.g., “#5 of 1000”)
- getCollectionSupply() - Returns current supply; collection configuration (max supply, start block, status) is communicated via CollectionUpdated events
- Collection metadata stored via ERC-8004’s onchain metadata using the “agent-collection” key
- Required events: CollectionUpdated and AgentMinted

I hope this proposal sparks discussion on fixed-supply agent collections, and I’d love feedback from anyone working on NFT infrastructure, AI agent registries, or collection management systems.

## Replies

**SamWilsn** (2026-01-13):

Is it wise to specify `startBlock` as the only minting criteria? Is it possible implementations might use other criteria for the minting process? If so, you might want to avoid enshrining `startBlock` explicitly.

---

**nxt3d** (2026-01-14):

I moved it to an event parameter. I could see taking it out altogether as well. However, it might be useful to keep if there’s a consistent pattern of new projects using it to advertise the block number when the collection will be open for minting?

