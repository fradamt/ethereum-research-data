---
source: ethresearch
topic_id: 10799
title: Bridging NFTs across layers
author: psinelnikov
date: "2021-09-20"
category: Layer 2
tags: []
url: https://ethresear.ch/t/bridging-nfts-across-layers/10799
views: 17190
likes: 14
posts_count: 11
---

# Bridging NFTs across layers

Thank you to [@vbuterin](/u/vbuterin) for his initial post kick-starting this topic: [Cross-rollup NFT wrapper and migration ideas](https://ethresear.ch/t/cross-rollup-nft-wrapper-and-migration-ideas/10507)

# Problem

A problem faced within the Ethereum blockchain as well as Layer 2s is the segmentation of assets, especially NFTs. When an NFT is created on a Layer 2, the NFT is stuck on that layer. This leads to the problem of NFT silos, where NFT assets on Layer 2 cannot be withdrawn to Layer 1. Having a way to create and transfer NFTs across multiple layers is important in order to introduce NFT applications to Layer 2s.

# Solution

Create a way to easily transfer NFTs across layers and reduce the gas requirements by minting the NFTs on Layer 2. This lets the user decide when they would like to withdraw their NFTs to Layer 1.

# Overview Diagram

[![NFT Metis-Initialization - Smart Contracts](https://ethresear.ch/uploads/default/optimized/2X/7/7902ea6a682ac628322d0bf43184b23fcd9685f8_2_501x500.jpeg)NFT Metis-Initialization - Smart Contracts798×796 33.1 KB](https://ethresear.ch/uploads/default/7902ea6a682ac628322d0bf43184b23fcd9685f8)

## Initializing the NFT Contracts

1. The Owner will provision the L1_NFT_Collection with the deployed L2_NFT_Collection, specifying:

- Address of the L2_NFT_Collection
- Chain ID of the L2_NFT_Collection
- Location of the NFT, mapping of the Chain ID by the NFT ID
- Range of Allocated NFTs, e.g. #1-100, 60-61, etc.

Range is a unit of 1000 NFTs.. rangeid 0 means NFT #0 to NFT #999.

### Data Structure

```auto
mapping(chainid => address) addresses;
mapping(rangeid => chainid) range_loc;
```

## Claiming the NFT on Layer 2

1. The User will claim the NFT, specifying the NFT ID. The L2_NFT_Collection contract on Layer 2 will verify the ID assignment (i.e. this Layer 2 owns the NFT) and mints the NFT on this rollup accordingly. Users can freely transfer NFTs within the rollup as normal.

## Withdrawing an NFT

1. The User sends a transaction to the L2_NFT_Collection smart contract, initiating the withdrawal to a target recipient on Layer 1.
2. The NFT gets deposited into the L2_Deposit contract, which locks the NFT for later retrieval if necessary.
3. The Locked NFT triggers a cross-message to the L1_NFT_Collection which allows the designated recipient to mint/withdraw the NFT on Layer 1.

- A new record in L1_NFT_Collection will be added to update the chain ownership of this particular NFT, data structure: mapping(id=>chainid) nft_loc; nft_loc always overrides range_loc. To determine the actual chain ownership of a NFT, the logic should check nft_loc first then range_loc if nft_loc[id] returns 0.
- If the NFT was already previously minted on Layer 1 before, i.e. it is not the first time this NFT has been withdrawn to Layer 1, the user would get that NFT with the updated metadata, with its nft_loc updated.

1. The recipient will claim the NFT, specifying the NFT ID.

## (Re)depositing the NFT on Layer 2

1. The User sends a transaction to the L1_NFT_Collection smart contract, initiating the transition to a target recipient on a target Layer 2 rollup.
2. The NFT gets deposited into the L1_Deposit contract, which locks the NFT for later retrieval if necessary.
3. The Locked NFT triggers a cross-message to the L2_NFT_Collection, which allows the user to mint/claim an existing NFT on Layer 2 by the NFT ID.

- If the NFT was already created and was deposited to the target rollup, the user would recieve the NFT with the updated metadata.
- L1_NFT_Collection will have nft_loc updated to reflect the updated chain ownership of the NFT.

# Sequence Diagrams

## Provisioning

[![NFT Owner Sequence](https://ethresear.ch/uploads/default/optimized/2X/7/7433ba110be4749bfd03e7e0bdbd1c16dde22052_2_690x270.jpeg)NFT Owner Sequence776×304 27.6 KB](https://ethresear.ch/uploads/default/7433ba110be4749bfd03e7e0bdbd1c16dde22052)

## Layer 1 => Layer 2

[![NFT Sequence - L1 to L2](https://ethresear.ch/uploads/default/optimized/2X/7/71d6af2af34c861cdd94dd4201b61c798d591c60_2_690x263.jpeg)NFT Sequence - L1 to L21684×644 91.3 KB](https://ethresear.ch/uploads/default/71d6af2af34c861cdd94dd4201b61c798d591c60)

## Layer 2 => Layer 1

[![NFT Sequence - L2 to L1](https://ethresear.ch/uploads/default/optimized/2X/5/5c69dcd0310566bddd5ec9279489704d639a459f_2_690x263.jpeg)NFT Sequence - L2 to L11684×642 89.6 KB](https://ethresear.ch/uploads/default/5c69dcd0310566bddd5ec9279489704d639a459f)

# Pros & Cons

## Pros

- Allows any user to claim an NFT on another Layer 2.
- The User can withdraw the NFT on Layer 2 and have the equivalent NFT created on Layer 1 with no chance of duplication.
- The User has the option to transfer their created NFT at any time from Layer 1 to Layer 2 and vice versa.
- Allows one NFT project to extend to multiple rollups.
- Easy and low cost initial setup.

## Cons

- The Owner has to create an equivalent NFT contract on the supported layers.
- NFTs can only move from Layer 2 to the coordinator chain (Layer 1 in this case) and back, they cannot move from Layer 2 to Layer 2 directly.
- Higher cost when moving NFTs among rollups because involvement of two Layer 1 transactions (withdraw and deposit)
- Technical complexity to connect both Layers

# Extensions

## Using a rollup to track the chain ownership to reduce the transaction cost

A rollup can be used to manage the chain ownership. In this way, the transaction cost can be greatly reduced. Layer 1 in this case can be treated the same as other rollups to some extent.

## Replies

**abcoathup** (2021-09-21):

I assume you have already seen VB’s [Cross-rollup NFT wrapper and migration ideas](https://ethresear.ch/t/cross-rollup-nft-wrapper-and-migration-ideas/10507)

---

**vbuterin** (2021-09-21):

The core ideas seem quite similar to what I wrote in [Cross-rollup NFT wrapper and migration ideas](https://ethresear.ch/t/cross-rollup-nft-wrapper-and-migration-ideas/10507) !

Allowing NFTs to be issued in any domain (L1 or an L2 rollup) by pre-allocating some indices to each domain is an excellent idea and definitely needed to prevent confusion from multi-allocation.

![](https://ethresear.ch/user_avatar/ethresear.ch/psinelnikov/48/9314_2.png) psinelnikov:

> The Locked NFT triggers a cross-message to the L1_NFT_Collection which allows the designated recipient to mint/withdraw the NFT on Layer 1.

The main challenge with using cross-messages *directly* is that many of these rollups are optimistic rollups which have a 1 week withdrawal delay. This is okay for some exceptional situations (eg. a particular rollup is shutting down completely due to some governance operation, and everyone is getting their assets out), but it’s really inconvenient for normal use. Hence why my proposals make wrapper NFTs accessible *instantly*, and not just after a week-long wait.

Another issue is that I think it’s not just L1 ↔ L2 transfers that we should be thinking about, but also L2 ↔ L2 transfers (eg. Optimism ↔ Arbitrum). These L2 ↔ L2 transfers should not require directly touching L1.

---

**psinelnikov** (2021-09-21):

Hi [@vbuterin](/u/vbuterin) thank you for your response. I re-read your post regarding [Cross-rollup NFT wrapper and migration ideas](https://ethresear.ch/t/cross-rollup-nft-wrapper-and-migration-ideas/10507). This implementation is similar to Extension 2, but instead of having a single contract manage all NFTs, where all potentially withdrawn NFTs are pre-created. This implementation instead uses a single NFT-collection contract, where the individual who created the contract owns the NFTs and can set the amount to be allocated on each individual layer. This has the added benefit of allowing each NFT to be tracked and located from the Layer 1 contract, with the assumption that the NFT stays on that layer and is not deposited to another contract outside of the architecture. This allows other users/contracts to see where the NFT is officially located using the Layer 1 contract.

I agree that there is a significant trade-off in the wait time for the transition between layers. Any type of messaging across chain would have to be put in that waiting period. I personally think that the event of transitioning an NFT from a Layer 2 is rare, but necessary to have. The initial idea is to have the ability for NFT projects to support multiple allocations on multiple layers, while still retaining the ability to make a withdrawal to Layer 1/2. Thank you for your thoughts and discussion points related to this design.

---

**RezaNourmohammadi** (2021-10-30):

Did u think about illiquid NFTs? What if we have a locked NFT collection on L1 with a specific period of time due to some reason like staking, liquidity minning?

---

**psinelnikov** (2021-11-01):

When dealing with a locking mechanism, the NFT that is locked would be stored in a contract account, only to be unlocked and released after certain conditions are met. Each contract can implement its own logic, but the core principle is that the contract will manage the logic. The same applies to the NFT collection. In this case, there will be contract bridges that are built that allow to lock, unlock, or mint those NFTs in those specific collections. You can use the NFTs that are created from this process in any contract that accepts NFTs, including staking, liquidity mining, and any other uses that NFTs have. In this case, if the NFT is not present on the current layer, it is locked within the LX_Deposit contract.

Let me know if that answers your question.

---

**RezaNourmohammadi** (2021-11-02):

thanks for your message, So, based on this it’s not possible for such an NFT collection that is locked on Layer_1 and unlocked on Layer_2? Also, it’s not an advantage, because you can do it and it would be a solution for the liquidity problem on Layer_2!

---

**mave99a** (2022-03-03):

Since the current ERC721/1155 NFT only store very few meta data on-chain and the data are stored off-chain (e.g. IPFS or S3), I think the only problem we need to take care of is the ID of NFT ?

If we use a decentralized unique ID for NFT rather than use incremental numbers like most of today’s ERC721 NFT, the problem is solved.  The W3C DID, or IPFS’s IPLD DID ([IPID DID Method](https://did-ipid.github.io/ipid-did-method/)) are perfect for this?

Then any NFT is essentially something stored off-chain (anywhere) with a verifiable unique ID, and then the blockchain is simply recording the ownership of such ID. A rollup alike solution should solve this problem easily.

Some of the existing NFT  might be tough to across layers by design.

---

**psinelnikov** (2022-03-10):

What you are describing is the data storage of the NFT, it can be stored anywhere and it is not on-chain. The reference to the storage is on-chain, in this case, it is the URI of the NFT metadata.

The ID of the NFT is defined in both the [EIP-721](https://eips.ethereum.org/EIPS/eip-721) and the [EIP-1155](https://eips.ethereum.org/EIPS/eip-1155) standards as a `uint256`. This means that a DID cannot be used, as it is a `string` type.

Even then, this is not a problem in the current design, as the contract on one layer is essentially a copy of the contract present on another layer. In this case, the bridged NFT on any layer should have the same ID and reference the same URI as the original NFT.

---

**austin-king** (2024-02-05):

Hi all, I just proposed an ERC that empowers NFTs to expand across rollups without ceding sovereignty to an interoperability protocol in a manner identical to xERC20. The work was partially inspired by this thread so I wanted to link it here in case anybody in this thread is still actively interested in this topic and wants to give their input.

I can’t include links in this post but it is available under the title “ERC-7611: Sovereign Bridged NFTs” in the Ethereum Magicians forum.

---

**KhaTruong123** (2024-02-06):

Interesting! One use case I’d like to leverage is tokenisation of real world asset. This approach can help to bring NFTs across chains but probably we need to consider Regulatory Considerations on the deployed smart contracts

