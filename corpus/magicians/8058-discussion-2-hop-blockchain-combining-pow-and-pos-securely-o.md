---
source: magicians
topic_id: 8058
title: "Discussion: 2-hop Blockchain, Combining PoW and PoS Securely on ETH (EIPxxxx)"
author: samsam380
date: "2022-01-21"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/discussion-2-hop-blockchain-combining-pow-and-pos-securely-on-eth-eipxxxx/8058
views: 543
likes: 0
posts_count: 1
---

# Discussion: 2-hop Blockchain, Combining PoW and PoS Securely on ETH (EIPxxxx)

Instead of moving ETH entirely from PoW to PoS Consensus mechanism, would it be possible to merge both PoW and PoS in parallel on 2-hop Blockchain like the one theorized here https://eprint.iacr.org/2016/716.pdf (2-hop Blockchain:

Combining Proof-of-Work and Proof-of-Stake Securely).

“From 1-hop to 2-hop blockchain. Nakamoto’s system is powered by physical computing resources, and the

blockchain is maintained by PoW-miners; there, each winning PoW-miner can extend the blockchain with a

new block. In our design, as argued above, we (intend to) use both physical resources and virtual resources.

That means, in addition to PoW-miners, a new type of players — PoS-holder (stakeholder) — is introduced

in our system. Now a winning PoW-miner cannot extend the blockchain immediately. Instead, the winning

PoW-miner provides a base which enables a PoS-holder to be “selected” to extend the blockchain. In short,

in our system, a PoW-miner and then a PoS-holder jointly extend the blockchain with a new block. If

Nakamoto’s consensus can be viewed as a 1-hop protocol, then ours is a 2-hop protocol.”

Merging PoW and PoS would prevent possibility of another hardfork by PoW miners after ETH moves to PoS, also it supports the PoW miners who had been supporting the network since its infancy, instead of ditching miners entirely wouldn’t it be better to integrate them into a new system where PoS and PoW can work in parallel, supporting each other.

[2016-716.pdf](https://github.com/ethereum/EIPs/files/7867138/2016-716.pdf)
