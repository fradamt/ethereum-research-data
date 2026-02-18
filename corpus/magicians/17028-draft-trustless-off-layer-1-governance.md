---
source: magicians
topic_id: 17028
title: "Draft: Trustless off-layer 1 governance"
author: dkeysil
date: "2023-12-05"
category: ERCs
tags: [layer-2, dao, merkle-proof]
url: https://ethereum-magicians.org/t/draft-trustless-off-layer-1-governance/17028
views: 625
likes: 1
posts_count: 1
---

# Draft: Trustless off-layer 1 governance

Decentralized Autonomous Organizations (DAOs) largely operate on the Ethereum blockchain, where every action incurs a significant ETH expense. This high cost of participation disproportionally affects smaller token holders, limiting their engagement in critical decision-making processes such as proposal surveys. Consequently, power tends to be concentrated among larger token holders, potentially undermining the very essence of decentralization.

With ZK rollups (e.g. Taiko) we get access to the trustless and cryptographically verified block hash from layer 1, so we are able to rebuild `BlockHeader`, get proof from L1 with `eth_getProof`, replace state root in the passed `BlockHeader` and compare it with the L1 block hash stored in the protocol smart contract. This makes it possible to verify any stored data from the L1 blockchain - in our case, it’s the amount of tokens at a specific block number (snapshot block number).

This setup would allow DAO token holders from Ethereum’s Layer 1 to vote with significantly reduced costs, fostering a more inclusive and democratic decision-making process.

Schema of the vote process that requires zero L1 transactions:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/cbf4019da88512a42aac48e21101e42c38ba476c_2_690x388.jpeg)image1200×675 74.7 KB](https://ethereum-magicians.org/uploads/default/cbf4019da88512a42aac48e21101e42c38ba476c)

I think it’s possible to make ERC out of this idea, so I want to ask there for a discussion of this idea and help to make ERC out of it.
