---
source: magicians
topic_id: 10543
title: "EIP (ERC) Proposal: NFT Breeding Standard"
author: hieroph4nt
date: "2022-08-27"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-erc-proposal-nft-breeding-standard/10543
views: 460
likes: 0
posts_count: 1
---

# EIP (ERC) Proposal: NFT Breeding Standard

Based on what we are developing at [Breedchain.xyz](https://breedchain.xyz), this is a proposal of a standard to interact with breeding of ERC 721/1155-based tokens.

***Breeding occurs after confirmation of ownership of a pair of ERC 721/1155 tokens of a same collection, generating a third token (offspring).***

This EIP proposal promotes collection-agnostic contracts that support breeding of multiple NFT collections and the option to charge specific minting fees for different collections.

**Token functions proposed are:**

breedCount - Retrieves the breed count of a certain NFT;

breedLimit - Retrieves the breeding limit of a certain NFT collection;

getParenthood - Retrieves X’s id and Y’s id (and their native NFT contract address) of a certain token;

breedPrice - Retrieves the standard ETH price to breed of a certain NFT collection;

breedPriceToken - Retrieves the price to breed of a certain NFT collection, in a specific ERC-20 token;

breed - Breeds an NFT.

**Examples of possible descentralized applications built on top of this standard are:**

- Browser plugins and explorer to show breeding count of NFTs
- NFT rarity and property explorers
- Breeding cost and limit calculators
- Breeding integrations with NFT marketplaces
- Gamified breeding experiences
- Etc

**Functions’ parameters can be found in detail here: https://docs.breedchain.xyz/for-developers#token-functions**

**In what regards metadata, apart from the specific attributes native to each of the supported collections, we add some standard attributes specific to our BREED collection:**

- Parenthood information - who are the parents, X and Y, of the BREED)
- Parenthood contract information - from which contract the parent NFTs belong
- Original contract information - from which contract the lineage started
- Generation - the more a lineage breeds, the higher the generation (example: children of original NFTs of an original collection are part of the 1st generation, whereas their children will be members of the 2nd generation etc )

If feedback is positive, a more detailed EIP draft will be designed. Thanks for your attention.
