---
source: magicians
topic_id: 3904
title: Membership proof in a Merkle Tree with Peer Secret
author: axe
date: "2020-01-07"
category: Web > Wallets
tags: [wallet, ux, social-recovery]
url: https://ethereum-magicians.org/t/membership-proof-in-a-merkle-tree-with-peer-secret/3904
views: 1124
likes: 0
posts_count: 2
---

# Membership proof in a Merkle Tree with Peer Secret

Starting a new topic to discuss the implementation of a pseudo anonymous membership proof in a Social Recovery Process. see: [ERC2429](https://github.com/ethereum/EIPs/pull/2429)

Problem: In a recovery the peers will have theirs addresses link to the user in recovery. Privacy and accounts correlations is something all users should be aware and as possible the system should have mechanism to help in privacy matters.

To mitigate this problem in the context of ERC2429, I think will be beneficiary to include a extension as how the Merkle tree is build.

One solution is to generate new Accounts for each recovery contract, mitigating the potencial link between accounts. But this solution put more pressure on the peer, that will have to manage more keys. As the recovery process is something unusually done, there is a probability of keys getting lost.

The proposed solution is something like a barebone HD Wallet strategy.

- The user setting a Recovery contract has to generate a peer_Hash (ERC2429).
- The peer uses this peer_hash with their private key.
- Following something like NewPublicKey = PrivateKey * Secret * G
- When is needed a recovery process, the user will give the Secret again to the peer that have a capacity of regenerate the member account.

Cheers

There is no way to enforce this solution in the context of ERC2429.

p.s - [gist](https://gist.github.com/ngmachado/be1428791256eefca99d16040b134a19)

## Replies

**axe** (2020-01-23):

This solution was dropped in favour a more capable solution of privacy.

