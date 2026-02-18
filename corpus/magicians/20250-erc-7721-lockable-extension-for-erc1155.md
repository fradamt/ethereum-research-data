---
source: magicians
topic_id: 20250
title: "ERC-7721: Lockable Extension for ERC1155"
author: piyushchittara
date: "2024-06-09"
category: ERCs
tags: [erc, nft, token, erc1155, lockability]
url: https://ethereum-magicians.org/t/erc-7721-lockable-extension-for-erc1155/20250
views: 572
likes: 0
posts_count: 1
---

# ERC-7721: Lockable Extension for ERC1155

This feature enables a multiverse of NFT liquidity options like peer-to-peer escrow-less rentals, loans, buy now pay later, staking, etc. Inspired by [ERC7066](https://ethereum-magicians.org/t/eip-7066-lockable-extension-for-erc721/14425/1) locking on ERC721, this proposal enables locking on ERC1155.

Complying with the need for enhanced security and control over tokenized assets, this extension enables token owners to lock individual NFTs with `tokenId`, ensuring that only approved users can withdraw predetermined amounts of locked tokens. Thus, offering a safer approach by allowing token owners to specify approved token IDs (setApprovalForId) to set an amount for withdrawal along with the default function of (setApprovalForAll)

[EIP](https://github.com/ethereum/ERCs/blob/d46b6302b8d3672e5d79a01f93c5e4bb97192166/ERCS/eip-locakable1155.md)

[ERC Pull Request](https://github.com/ethereum/ERCs/pull/466)

Please let us know your thoughts on this proposal and if our motivation seems useful! ![:crossed_fingers:](https://ethereum-magicians.org/images/emoji/twitter/crossed_fingers.png?v=12)
