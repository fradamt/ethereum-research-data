---
source: magicians
topic_id: 16695
title: "ERC-7561: Simple NFT"
author: wenzhenxiang
date: "2023-11-20"
category: ERCs
tags: [erc, nft, token, erc-721]
url: https://ethereum-magicians.org/t/erc-7561-simple-nft/16695
views: 1119
likes: 0
posts_count: 1
---

# ERC-7561: Simple NFT

ERC721 are Ethereum-based standard NFT that can be traded and transferred on the Ethereum network. But the essence of ERC721 is based on the EOA wallet design. EOA wallet has no state and code storage, and the smart contract wallet is different.

Almost all ERCs related to NFT are adding functions, our opinion is the opposite, we think the NFT contract should be simpler, more functions are taken care of by the smart contract wallet.

Our proposal is to design a simpler NFT asset based on the smart contract wallet,

It aims to achieve the following goals:

1. Keep the NFT contract simple, only need to be responsible for the transaction function
2. approve functions are not managed by the NFT contract , approve and getApproved should be configured at the user level instead of controlled by the nft contract, increasing the user’s more playability , while avoiding part of the ERC-721 contract risk.
3. Remove the safeTransferFrom function, and a better way to call the other party’s nft assets is to access the other party’s own contract instead of directly accessing the nft asset contract.
4. Forward compatibility with ERC-721 means that all nft can be compatible with this proposal.

Examples

Judges whether the receiving address is safe (ERC-721, safeTransferForm),

ERC-721 Consecutive Transfer Extension(ERC-2309),

No Intermediary NFT Trading Protoco(ERC-6105),

authorizes the distribution of the user’s own assets (ERC-721, approve, allowance) and many proposals based on ERC-721 extension

The above work should be handled by the user’s smart contract wallet or wallet pulgin, rather than the nft contract itself.

this EIP is forward compatible with ERC-721.
