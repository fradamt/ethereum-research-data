---
source: magicians
topic_id: 241
title: "EIP-908: Reward full nodes and clients for a sustainable network"
author: jamesray1
date: "2018-04-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-908-reward-full-nodes-and-clients-for-a-sustainable-network/241
views: 4075
likes: 2
posts_count: 8
---

# EIP-908: Reward full nodes and clients for a sustainable network

> When each transaction is validated, give a reward to clients for developing the client.

http://eips.ethereum.org/EIPS/eip-908

Changelog

- Update: I made modifications to the proposal, adding a background for the abstract, additional details for the motivation, specification and rationale (while leaving the proposed implementation unchanged), plus references to similar EIPs such as EIP 960 and EIP 1015.
- Update 2: I added more details to how the access list for client addresses could be managed (off-chain or layer 2).
- Update 3: added more details to the spec and rationale with specific reward amounts proposed and more details on how it would work.
- remove a proposal to reward full nodes, leaving just the proposal to reward clients, because Casper FFG will incentivize validation.
- add an attack and solution.

## Replies

**nootropicat** (2018-05-05):

I can see the point in supporting nodes’ uploading capacity (which is imo impossible to do on the protocol level), but the verification itself is already solved by PoS, no? A validator that also signs invalid blocks would get penalized.

Before PoS forcing a new node to accept a false state would require a 51% attack, assuming a simple rule like ‘only download state that’s at least 1 day old’ (no idea if it already exists), which is a failure condition anyway.

PoS also gives a collective incentive to validators to support the network by providing an uploading bandwidth.

Theoretically it’s a free-rideable public good but I would expect most validators to support the network.

---

**jamesray1** (2018-05-07):

OK, Casper FFG does incentivize verification. However, Casper doesn’t incentivize client development.

---

**nootropicat** (2018-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamesray1/48/1548_2.png) jamesray1:

> However, Casper doesn’t incentivize client development.

Yes, but wasn’t getting funds for that the reason behind the ICO and the founders’ share of eth? That sounds like a job for the Ethereum Foundation.

---

**jamesray1** (2018-05-07):

Parity is funded by VCs, not by the Ethereum Foundation. [Drops of Diamond](https://github.com/Drops-of-Diamond/diamond_drops) hasn’t received a grant yet.

---

**jamesray1** (2018-05-07):

Additionally Casper incentivizes validators. It does not incentivize full nodes that are not validators.

---

**jamesray1** (2018-05-18):

I updated the proposal with a significant change, which is to remove a proposal to reward full nodes, leaving just the proposal to reward clients, because Casper FFG will incentivize validation.

---

**jamesray1** (2018-05-19):

I updated the proposal with an attack and solution.

