---
source: magicians
topic_id: 2868
title: Reduce the cost of transaction data
author: Recmo
date: "2019-03-06"
category: EIPs
tags: [gas, eip, scaling, istanbul]
url: https://ethereum-magicians.org/t/reduce-the-cost-of-transaction-data/2868
views: 2034
likes: 3
posts_count: 3
---

# Reduce the cost of transaction data

Layer two scaling solution store data out of storage, but they often have a need to bring it in a transaction for security purposes (fraud proofs, data availability, etc.). When data is brought on-chain, this also often includes large merkle proofs relating it back to concise on-chain state.

Currently the cost of updating storage is ~ 5000 gas. The cost of verifying a single Merkle tree of depth 32 is ~70 000 gas. It is cheaper to skip L2 scaling and just store on chain.

Examples of applications that are currently constrained by transaction data cost:

- FunFair
- Rollup
- StarkDEX
- DutchX
- Truebit

Final implementation is a trivial update of costs, but before that we need to extensively research what would be an appropriate gas cost and it’s impact on the network.

Mentions:

- Remco’s talk in Stanford https://www.youtube.com/watch?v=dHZiWFWCGNM&feature=youtu.be&t=68
- Vitalik’s talk in Tapei https://youtu.be/mOm47gBMfg8?t=755

## Replies

**axic** (2019-06-03):

This is now being addressed in [EIP-2028: Calldata gas cost reduction](https://ethereum-magicians.org/t/eip-2028-calldata-gas-cost-reduction/3280/4)

Perhaps this topic can be set to locked to avoid proliferation on duplicate topics?

---

**jpitts** (2019-06-24):

I will lock it.

[@Recmo](/u/recmo), PM me in this forum if you would like to keep the conversation going here for some reason…

