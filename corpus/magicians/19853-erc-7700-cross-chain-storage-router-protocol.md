---
source: magicians
topic_id: 19853
title: "ERC-7700: Cross-chain Storage Router Protocol"
author: sshmatrix
date: "2024-04-30"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7700-cross-chain-storage-router-protocol/19853
views: 975
likes: 1
posts_count: 1
---

# ERC-7700: Cross-chain Storage Router Protocol

The following proposal is a superior version of [EIP-5559: Cross-Chain Write Deferral Protocol](https://ethereum-magicians.org/t/eip-5559-cross-chain-write-deferral-protocol/10576), aka *CCIP-Write*, replacing Ethereum L1 storage with L2 chains and cryptographically secure databases with an aim to cut gas costs and further privacy while retaining the secure aspects of on-chain storage. Methods in this document specifically target security and cost-effectiveness of write deferrals in context of databases. The cross-chain data written with these methods can be retrieved by generic EIP-3668-compliant contracts completing the cross-chain data life cycle.

**ERC Link:** [ERC-7700](https://github.com/namesys-eth/ERCs/blob/ccipWrite/ERCS/erc-7700.md)

**PR Link:** [Add ERC: Cross-chain Storage Router Protocol by sshmatrix · Pull Request #404 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/404)

**Note:** This proposal is a standalone ERC, amended from what was originally intended as a PR to [EIP-5559](https://ethereum-magicians.org/t/erc-5559-cross-chain-write-deferral-protocol/19664)
