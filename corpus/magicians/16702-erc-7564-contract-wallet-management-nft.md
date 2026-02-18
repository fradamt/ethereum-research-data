---
source: magicians
topic_id: 16702
title: "ERC-7564: Contract wallet management NFT"
author: wenzhenxiang
date: "2023-11-20"
category: ERCs
tags: [erc, nft, wallet]
url: https://ethereum-magicians.org/t/erc-7564-contract-wallet-management-nft/16702
views: 1294
likes: 0
posts_count: 2
---

# ERC-7564: Contract wallet management NFT

A proposal to manage NFT by the user’s smart contract wallet, which provides a new way to manage assets, utilizes the programmability of the smart contract wallet, and also provides more playability.

EOA wallet has no state and code storage, and the smart contract wallet is different.

AA is a direction of the smart contract wallet, which works around abstract accounts.

The smart contract wallet allows the user’s own account to have state and code, bringing programmability to the wallet. We think there are more directions to expand. For example, NFT asset management, functional expansion of NFT transactions, etc.

The proposal aims to achieve the following goals:

1. Assets are allocated and managed by the wallet itself or plugins. such as approve , which are configured by the user’s contract wallet, rather than controlled by the NFT asset contract, to avoid some existing ERC-721 contract risks.
2. Add the nftTransfer function, the transaction initiated by the non-smart wallet itself or will verify the approves.
3. The user wallet itself supports approve. Add nftApprove,  nftGetApproved, Used to approve specify one asset under the nft contract.
4. add nftSetApprovalForOneAll, nftIsApprovedForOneAll, Used to approve specify all assets under the nft contract.
5. add nftSetApprovalForAllAll, nftIsApprovedForAllAll, Used approve for assets under all nft contracts.
6. The users can choose to add hook function before and after their nftTransfer to increase the user’s more playability
7. The user can choose to implement the nftReceive function

## Replies

**sullof** (2026-01-05):

It sounds useful, but it requires too many additions to the ERC-721 standard. Have you considered the possibility of creating a service via [ERC-7656](https://eips.ethereum.org/EIPS/eip-7656) and just require that the NFT owner approves the service to manage the NFT?

