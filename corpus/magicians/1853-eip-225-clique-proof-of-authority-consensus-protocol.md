---
source: magicians
topic_id: 1853
title: "EIP-225: Clique proof-of-authority consensus protocol"
author: karalabe
date: "2018-11-09"
category: EIPs
tags: [consensus-protocols, poa]
url: https://ethereum-magicians.org/t/eip-225-clique-proof-of-authority-consensus-protocol/1853
views: 5633
likes: 6
posts_count: 2
---

# EIP-225: Clique proof-of-authority consensus protocol

**This thread is a continuation of https://github.com/ethereum/EIPs/issues/225 (happening on GitHub until now) so it can survive long term even after the EIP is accepted and it’s issue closed.**

---

# Background

Ethereum’s first official testnet was Morden. It ran from July 2015 to about November 2016, when due to the accumulated junk and some testnet consensus issues between Geth and Parity, it was finally laid to rest in favor of a testnet reboot.

Ropsten was thus born, clearing out all the junk and starting with a clean slate. This ran well until the end of February 2017, when malicious actors decided to abuse the low PoW and gradually inflate the block gas limits to 9 billion (from the normal 4.7 million), at which point sending in gigantic transactions crippling the entire network. Even before that, attackers attempted multiple extremely long reorgs, causing network splits between different clients, and even different versions.

The root cause of these attacks is that a PoW network is only as secure as the computing capacity placed behind it. Restarting a new testnet from zero wouldn’t solve anything, since the attacker can mount the same attack over and over again. The Parity team decided to go with an emergency solution of rolling back a significant number of blocks, and enacting a soft-fork rule that disallows gas limits above a certain threshold.

While this solution may work in the short term:

- It’s not elegant: Ethereum supposed to have dynamic block limits
- It’s not portable: other clients need to implement new fork logic themselves
- It’s not compatible with sync modes: fast and light clients are both out of luck
- It’s just prolonging the attacks: junk can still be steadily pushed in ad infinitum

Parity’s solution although not perfect, is nonetheless workable. I’d like to propose a longer term alternative solution, which is more involved, yet should be simple enough to allow rolling out in a reasonable amount of time.

## Standardized proof-of-authority

As reasoned above, proof-of-work cannot work securely in a network with no value. Ethereum has its long term goal of proof-of-stake based on Casper, but that is heavy research so we cannot rely on that any time soon to fix today’s problems. One solution however is easy enough to implement, yet effective enough to fix the testnet properly, namely a proof-of-authority scheme.

*Note, Parity does have an [implementation of PoA](https://github.com/ethcore/parity/wiki/Consensus-Engines#authority-round), though it seems more complex than needed and without much documentation on the protocol, it’s hard to see how it could play along with other clients. I welcome feedback from them on this proposal from their experience.*

The main design goals of the PoA protocol described here is that it should be very simple to implement and embed into any existing Ethereum client, while at the same time allow using existing sync technologies (fast, light, warp) without needing client developers to add custom logic to critical software.

---

For the actual spec, please see https://eips.ethereum.org/EIPS/eip-225 (once it’s merged).

## Replies

**boris** (2018-11-09):

[@karalabe](/u/karalabe) thank you for sharing here – this seems very relevant.

