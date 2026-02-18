---
source: magicians
topic_id: 20997
title: Security concerns when deploying contracts with the same account on different chains
author: elmariachi
date: "2024-09-08"
category: Uncategorized
tags: [security, contract-deployment]
url: https://ethereum-magicians.org/t/security-concerns-when-deploying-contracts-with-the-same-account-on-different-chains/20997
views: 81
likes: 1
posts_count: 2
---

# Security concerns when deploying contracts with the same account on different chains

using the plain old CREATE opcode, when I’m deploying contracts, the contract addresses depend on the account’s current nonce.

When I’m using the same account / EOA to deploy contracts on different chains, there might exist completely unrelated contracts on different chains.

Regardless of the UX implications (multichain explorers, eg tenderly would display unrelated transactions across chains), might that lead to security related issues? Could eg someone find  a transaction casted for one contract on the L1 and replay that on an L2 (since the contract addresses are the same?)

## Replies

**ryley-o** (2024-09-16):

In general, [EIP-155](https://eips.ethereum.org/EIPS/eip-155) prevents replay attacks on different chains.

Of course, for the few transactions that sign in a pre-EIP-155 format, yes, there will always be some amount of cross-chain replay attack vulnerability. Those transactions are typically very intentional, however, and are not part of the typical UX.

