---
source: magicians
topic_id: 11009
title: ERC721 usable extension
author: niceural
date: "2022-09-24"
category: EIPs
tags: [nft, erc721, lending, ticketing, gaming]
url: https://ethereum-magicians.org/t/erc721-usable-extension/11009
views: 573
likes: 0
posts_count: 1
---

# ERC721 usable extension

# Motivation

The newly adopted ERC721 extension, ERC4907, enables an NFT owner to lend their NFT for a period of time. However, the owner cannot limit the number of uses of this NFT.

Version 1.1 of Solana NFT standard Metaplex introduces a  [Uses](https://docs.metaplex.com/programs/token-metadata/using-nfts#the-uses-field) field in the token metadata account. This field enables an NFT to be minted with a set number of uses that cannot be increased. The owner can then delegate the Use authority to other trusted authorities which can decrease the number of Uses left for the token.

This extension could facilitate the expansion of NFT use cases in two industries:

- ticketing: in my home town, you can get 10 entries memberships to the town swimming pool. This model could be reproduced with Usable NFTs by minting NFTs with the Uses field set to 10 uses. The customers would then buy these NFTs, give the swimming pool approval to spend their Uses, and the Uses amount would be decremented each time the customer goes swimming.
- gaming: Usable NFTs representing characters could be minted to be used in an RPG game with a uses field set to 5 corresponding to the number of lives. A player would then buy these NFTs and approve the game to spend their Uses. Each time the player’s character dies in the game, the number of uses is decremented. Once all the lives of the character have been used, the NFT can be automatically burned, or unusable, or transferred back to the game.

# Proposition

Create a ERC721 extension with the following features:

- function getUses(uint tokenId) external view returns ((uint64 expires, uint192 uses));. The returned values correspond to the following:

expires: UNIX timestamp, given by block.timestamp, after which the NFT is unusable
- uses: number of uses left for the token. The token Uses can be decreased by the owner or by an approved authority. If there is no number of Uses restriction on the token, this value is set to max uint192 (2^192 - 1).

`function approveForUsage(address operator) external;`. This function gives an address the right to decrease the number of Uses of a token

A token becomes unusable when `block.timestamp` is passed the `expires` or when the number of Uses is zero. A `_onTokenFullyUsed()` hook can be called when the token is fully used to execute an operation (burn the token, transfer the token to another address, buy more uses, etc)
