---
source: magicians
topic_id: 13823
title: UNFT - NFT owns NFT by Clopr
author: PotionBoss
date: "2023-04-14"
category: EIPs
tags: [nft, erc-721]
url: https://ethereum-magicians.org/t/unft-nft-owns-nft-by-clopr/13823
views: 986
likes: 1
posts_count: 2
---

# UNFT - NFT owns NFT by Clopr

EIP: TBD

Title: UNFT - Underlying Non-Fungible Tokens Owning NFTs

Author: Clopr ([cloprnft.com](http://cloprnft.com)) - Antoine & Baptiste

Type: Standards Track

Category: ERC

Status: Draft

Created: 2023-04-18

Requires: TBD

Replaces: TBD

Superseded-by: TBD

Resolution: TBD

## Abstract

This proposal introduces a new type of Non-Fungible Token (NFT) known as UNFT, which enables NFTs to own other NFTs. With the UNFT, when an NFT such as a StoryNFT (SNFT) is owned by a UNFT and the UNFT is sold to a new owner, the SNFT is automatically transferred to the new owner’s wallet. This approach provides a more seamless and intuitive way to manage ownership and transfer of NFTs that own other NFTs, eliminating the need for manual claiming of assets.

## Motivation

Currently, if an ERC-721 NFT owns another ERC-721 NFT such as a StoryNFT (SNFT), the owned asset is not automatically transferred to the new owner’s wallet when the owning NFT is sold. This is because the ERC-721 code is not designed to allow NFTs to naturally own other NFTs. To solve this issue, CloprNFT proposes the creation of a new type of NFT called UNFT, which enables NFTs to own other NFTs and transfer ownership of both assets in a single transaction.

By automating the process on-chain, when an NFT is transferred, its underlying assets (NFTs) will follow accordingly. Additionally, with UNFTs, marketplaces can reflect the assets owned by NFTs in the same way hard-coded attributes are. This will enable a smoother process for NFT ownership and transfer, without the need for manual asset claiming.

Solving issues on offers when dealing with UNFT:

- Issue 1: Solving offers made on full CloprBottle NFTs - Consume StoryPotion (emptying the CloprBottle NFT) before accepting an offer.
- Issue 2: Solving UNFT offers - Burn Story NFT before accepting an offer on a UNFT
- The two current issues do not apply if the UNFT or CloprBottle NFT is directly purchased.
- Opportunity for Clopr marketplace with special conditions such as the requirement of owning certain SNFTs in order for the sale to be considered valid.

## Specification

The UNFT is a new type of ERC-721-compatible NFT that allows for ownership of other ERC-721-compatible NFTs. It includes new fields in its smart contract to represent the owned NFT (Code: Work in progress), which can be any type of NFT such as a StoryNFT. When a UNFT is transferred to a new owner, the owned NFT is automatically transferred to the new owner’s wallet along with the UNFT. This enables a simpler and more natural way of tracking and transferring ownership of multiple NFTs owned by a UNFT.

## Rationale

The UNFT was developed to address a critical challenge in NFT ownership and transfer. The current ERC-721 standard does not provide a natural way for an NFT to own another NFT. This means that if an ERC-721 NFT owns another ERC-721 NFT, such as a StoryNFT, the owned asset is not automatically transferred to the new owner’s wallet when the owning NFT is sold. To solve this problem, we propose the creation of UNFTs, which allow NFTs to own other NFTs and transfer ownership of both assets (or more) in a single transaction.

By allowing the UNFT smart contract to gain ownership of other owned NFTs, we enable a more straightforward way of tracking and transferring ownership of all NFTs owned by a UNFT. With the UNFT, NFT ownership becomes more natural, and transferring ownership of NFTs that own other NFTs becomes seamless. This innovation brings significant benefits to the NFT ecosystem, making it easier for collectors and investors to manage, transfer and make use of their NFT holdings.

## Backward Compatibility

The UNFT is fully backward compatible with existing ERC-721 NFTs, meaning that existing NFTs can own UNFTs and vice versa. However, existing NFTs (not UNFTs) that own other NFTs will need to manually claim any SNFT or other NFT that they own when transferred to a new wallet. It’s important to note that not claiming an asset owned by an NFT does not affect ownership, as it is secured on-chain anyway. This is where the innovation of UNFT lies - providing a smoother process for UNFT owners to have their UNFT assets reflected automatically on marketplaces, in the same way that attributes are reflected. Additionally, when a UNFT is transferred, any associated SNFTs or others will follow along naturally with the UNFT, making the ownership transfer process more streamlined.

## Test Cases

To test the functionality of UNFT, Clopr is deploying CloprHouse - a decentralized application (dApp) that enables NFTs and UNFTs to consume potions to create an NFT that is owned by the NFT or UNFT consuming the potion. This dApp can only be used by owners of the CloprBottle NFT that can be filled with potions. The first potion available is called StoryPotion, which creates a StoryNFT upon consumption. The StoryNFT is then linked to the NFT or directly integrated into the smart contract of a UNFT, and it will forever remain the property of the UNFT, even if the NFT is transferred to a new owner. At launch, only NFTs will be able to consume potions, so the management of NFT transfers owned by NFTs and reflecting them on marketplaces will be done mechanically with APIs, claiming mechanisms, and event listeners. With this proposal, UNFTs of the future will be able to naturally integrate their NFTs, allowing them to be owned and managed the same way as hard-coded attributes.

## Security Considerations

The SNFT, as an asset, is owned by an NFT or UNFT rather than a wallet, making it different from a soulbond token. The ownership of the owned NFT is linked to the UNFT, and it cannot be sold or transferred independently. When a UNFT is sold, the ownership of its owned NFT is also transferred to the new owner. Thus, the owner of the UNFT also gains ownership of the UNFT’s owned NFT, and the previous owner loses ownership of both assets.

## References

- ERC-721: Non-Fungible Token Standard
- OpenZeppelin: Implementing ERC721 Token Standards on Ethereum
- WhitePaper
- (TBD)

Clopr is launching an innovative dApp called the CloprHouse. The CloprHouse enables owners of the exclusive CloprBottle NFT to harness the power of minting NFTs owned by their NFTs. Through the CloprHouse, the CloprBottle NFT becomes refillable with various potions, with StoryPotion being the first potion available for use.

[![spaces_PkoqObPq3fmTeXwI82aA_uploads_ZiiuN2cI8WRoebVcFHDZ_NftOwnsNFT](https://ethereum-magicians.org/uploads/default/original/2X/b/b19fe5444c85fe45f7e1ae58e8577457068ca059.webp)spaces_PkoqObPq3fmTeXwI82aA_uploads_ZiiuN2cI8WRoebVcFHDZ_NftOwnsNFT1056×754 33.1 KB](https://ethereum-magicians.org/uploads/default/b19fe5444c85fe45f7e1ae58e8577457068ca059)

## Replies

**Mani-T** (2023-08-09):

Ensuring that UNFTs can interact with other NFTs, wallets, marketplaces, and applications, the security and robustness is crucial, as any vulnerabilities could lead to potential exploits.

