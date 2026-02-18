---
source: ethresearch
topic_id: 5388
title: Interest in escrow protocol extensions?
author: marckr
date: "2019-04-30"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/interest-in-escrow-protocol-extensions/5388
views: 1529
likes: 1
posts_count: 2
---

# Interest in escrow protocol extensions?

[![swap](https://ethresear.ch/uploads/default/optimized/2X/1/1a16e6226aa2be5cb205ad5403265fc964e53a51_2_690x335.png)swap2406×1170 269 KB](https://ethresear.ch/uploads/default/1a16e6226aa2be5cb205ad5403265fc964e53a51)

From [Escrow protocols for cryptocurrencies: How to buy physical goods using Bitcoin](http://www.jbonneau.com/doc/GBGN17-FC-physical_escrow.pdf)

I am most interested in 5.4 Escrow Encrypt-and-Swap and 6.3 Group Encrypt-and-Swap. I have dropped away from cryptography for a bit, but this certainly comes up at an economic layer as well. I have no evidence aside from some hacker texts regarding infeasibility of sMPC that have colored the way I think about cryptography since.

Ring signatures and Threshold Signatures are practically dual, but seem an enduring theoretical key. What is the state of the art for automatic PKI signing? Proxy wallets of some sort? I am interested in how to make as much automated as possible, especially on the cryptographic layer.

Transitive trust is the issue that glares as the main problem within this direction of thinking and one of the gravest concerns within the space. I have 3 ETH in my Kovan wallet, so I am ready to rumble.

Have any of you read this paper? I am trying to figure out a bit of a knowledge share, how to discuss fruitfully with the knowledge base this community has.

## Replies

**pablo-chacon** (2025-11-29):

This thread hits on something I’ve been thinking about from a slightly different angle: how Non-Fungible Tokens can model real-world rights such as delivery, access, ownership, without trying to “put the object” on-chain.

One thing I’ve found compelling is that the NFT itself represents ownership of a solid object, it also holds metadata that makes fraud practically useless. If someone tries to spoof the NFT (copy it, fake transfer, etc), the metadata won’t match the original intent (e.g., pickup/dropoff locations, hash-locked route, access credentials). The fraud is detectable by design, not by policy.

In traditional systems (say, land registries like Lantmäteriet in Sweden), the assumption is that trusted parties submit clean data. But people still game that, and when fraud happens, it’s always after the fact. With protocol-enforced NFT lifecycles, the rules of custody and settlement are encoded up front and can’t be bypassed by social engineering.

I see this as especially useful in physical delivery, title deeds, ticketing, and any domain where what’s being transferred is unique, physical, and needs to be claimed. If the NFT lifecycle is deterministic and the metadata is authenticated off-chain, then even without direct GPS or KYC, you still get strong guarantees around state transitions and payout conditions.

Curious if others have used NFT state machines + metadata integrity to sidestep transitive trust in IRL workflows. I think it’s a good foundation for physical-world protocols that needs to be trustless without heavy cryptography overhead.

