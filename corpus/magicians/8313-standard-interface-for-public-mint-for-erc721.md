---
source: magicians
topic_id: 8313
title: Standard Interface for Public Mint for ERC721
author: caffeinum
date: "2022-02-15"
category: Magicians > Primordial Soup
tags: [nft, token, eip]
url: https://ethereum-magicians.org/t/standard-interface-for-public-mint-for-erc721/8313
views: 1475
likes: 8
posts_count: 4
---

# Standard Interface for Public Mint for ERC721

Most of the NFTs collections that launch today host primary mint on their website first, and then secondary trading happen on marketplaces. While the latter is straightforward – send ETH from user1 to user2, call `safeTransferFrom`; the former is very different from project to project.

The proposal is to form a standard interface for public minting a collection. This could open rooms for bots, trading strategies, cross-chain integrations etc. Even marketplaces could add a button to a collection page that says “Mint primary”!

The simplest interface could look like:

```solidity
interface NFTPublicMint {
  function mint(uint256 quantity, bytes data) payable;
  function mint(uint256 quantity, address to, bytes data) payable;

  function totalSupply() returns (uint256);
  function getPrice() returns (uint256);
}
```

The objections to this implementation include:

- lacking tokenURI, royaltyRecipient etc
- not possible to use in situations where more granular control is required (dutch auction, merkle-tree whitelist)

In Buildship, I am already working on a `MetaverseNFT` reference implementation + Factory pattern to deploy cheap copies of self-owned 10k+ collections. While I won’t benefit from this standard much, I am in a position to implement it for all of our creators.

I will invite some stakeholders that I have in mind to post their usecase in the thread.

P.S. See the initial discussion here in NFT Standards ring: [Telegram](https://t.me/c/1426798277/2626)

## Replies

**ohld** (2022-02-15):

Hey! CTO of Via protocol here. With one of our products, we implement cross-chain NFT mint. For example, we can accept ETH on Ethereum as payment and mint NFT on Polygon using our own liquidity.

To achieve this we implemented our `mintAndSend` contract: In one method it calls `.mint` and `.safeTransferFrom` of NFT mint contract.

The problem is that different NFT collection contracts have different `.mint` methods with different **names** ([example](https://polygonscan.com/address/0xd558bf191abfe28ca37885605c7754e77f9df0ef)) and even different set of parameters ([example](https://polygonscan.com/address/0xbC1fE0f3B02CE5FF516F14AC7b79Dd6397A54b9c#code)).

So we are forced to deploy a separate ‘wrapper contract’ to unify the minting interface of the NFT collection mint contract. The Standard Interface would solve a lot of problems here.

---

**fmc** (2022-02-16):

gm!

[@caffeinum](/u/caffeinum)

I love the idea of the standardization of interfaces. Communication between different contracts is a very important part to make eth ecosystem bloom IMO.

While I do not see minting interface as a part of ERC-721 standard, it can be useful as a part of some future standard of a minter contract.

I think that future launches of projects using NFTs as a part of their ecosystem can launch at several launchpads simultaneously and such an interface can ease that process.

[@ohld](/u/ohld)

I believe that mint first and `safeTransferFrom` after is not the best pattern since `_mint` already has `to` param. That’s why I believe all the NFT minting contracts should allow minting to another wallet, not just `msg.sender`.

---

**ohld** (2022-03-16):

Thanks for the reply. Not all NFT mint contracts have to param or public access to this param. That’s why the open standard is somehow what we need.

