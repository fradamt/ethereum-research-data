---
source: magicians
topic_id: 9941
title: How I learned to stop worrying about the DoS and love the chain
author: asn
date: "2022-07-14"
category: Magicians > Primordial Soup
tags: [networking, dos]
url: https://ethereum-magicians.org/t/how-i-learned-to-stop-worrying-about-the-dos-and-love-the-chain/9941
views: 4877
likes: 10
posts_count: 3
---

# How I learned to stop worrying about the DoS and love the chain

This post is about *validator privacy* in the Ethereum proof-of-stake world. Our aim is to protect the identity of block proposers against denial-of-service (DoS) attackers.

With this post, we hope to inform Ethereum validators about the threat of DoS attacks and help them gain resilience against them. We also hope to inform Ethereum consensus client engineers about the solution space around this problem.

## What?

After we move to proof-of-stake, future block proposers [will be known ahead of time](https://eth2book.info/altair/part3/helper/misc#compute_shuffled_index). This allows attackers to DoS those proposers before they get the chance to propose.

A proposer that gets attacked before proposing does not gain block or fee rewards: Given that those rewards represent a big chunk of a validator’s total gains, such attacks can force validators to centralize by joining big validator pools and providers.

## Why?

While DoS attacks against validators might initially seem pointless from an attacker’s perspective, there are actually ways to flip such attacks into monetary gain:

- An attacker opens a short position against ETH and then attacks block proposers while loudly claiming that Ethereum is broken, in an attempt to gain quick profit from the short position.
- An attacker who controls the next proposer in the list is incentivized to attack previous proposers to steal their transaction fees and MEV.
- An attacker can bias Ethereum’s randomness subsystem by DDoSing the right proposer at the right time.

Fortunately, there are ways to defend against such attacks.

## How?

In an attack scenario, the adversary learns the IP address of a validator by [crawling the P2P network](https://ieeexplore.ieee.org/document/9644904) while following that validator’s attestations. After the attacker learns the IP address of a validator, the attacker can start attacking the validator right before it proposes a block.

We present two approaches to solving this problem – a short-term approach that requires manual configuration by the validator’s operator, and a long-term approach that works without any configuration.

### Sentry nodes (short-term)

The most basic practical solution to this problem is to employ a [classic frontend/backend design](https://forum.cosmos.network/t/sentry-node-architecture-overview/454); the [Validator Client](https://docs.ethhub.io/ethereum-roadmap/ethereum-2.0/eth-2.0-client-architecture/) stays in the backend, whereas the frontend uses two separate Beacon Nodes (BN): one for publishing attestations and the other for publishing block proposals. By keeping those two Beacon Nodes independent and disconnected, the *valuable* proposing BN is kept hidden and well protected.

[![multibn.drawio](https://ethereum-magicians.org/uploads/default/optimized/2X/5/57e75d0d3310497f289f01237dca459ec5ead698_2_690x226.png)multibn.drawio1453×478 55.9 KB](https://ethereum-magicians.org/uploads/default/57e75d0d3310497f289f01237dca459ec5ead698)

The obvious drawback of this approach is that the validator’s operator needs to configure this multi-beacon-node setup. They need to maintain separate machines for the beacon nodes and rotate the IP address of the block proposing BN periodically. While this might seem like minimal overhead to a tech-savvy person, it can be troublesome for less technical operators. Furthermore, even for technical operators, it can be hard to create a non-centralized version of this setup that does not rely on popular VPN/VPS providers.

The above setup has to [be](https://github.com/prysmaticlabs/prysm/issues/11048) [built](https://github.com/sigp/lighthouse/pull/3328) into validator clients and exposed as part of their configuration interface. Since The Merge hasn’t happened yet, the attacker incentives are much lower, and hence clients don’t yet support this functionality. As the Merge comes closer, we encourage client teams to support this sentry-node feature to not only protect individual validators but the network as a whole.

#### Vouch

Alternatively, even if a client does not support this functionality, we can build a *dummy BN proxy*, which acts as a regular BN as far as the VC is concerned, but instead transparently routes the requests from the VC to frontend BNs depending on whether they are attestations or proposals. Such an architecture is fully supported by the [current beacon API](https://github.com/ethereum/beacon-APIs).

This is actually close to how the [vouch](https://github.com/attestantio/vouch) project works and it’s currently [possible](https://www.attestant.io/posts/upgrading-attestants-infrastructure-without-missing-a-beat/) to [configure it](https://github.com/attestantio/vouch/blob/master/docs/configuration.md) to support various types of sentry-node architectures.

### Single Secret Leader Election protocols (long-term)

While the sentry node approach is a decent and pragmatic solution to the DoS problem, it also increases the infrastructure complexity and maintenance costs of validators.

For this reason, we plan to eventually enshrine validator privacy into the core Ethereum protocol.

At the moment we are exploring protocols based on [verifiable](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763) [shuffling](https://ethresear.ch/t/simplified-ssle/12315), on [VRFs](https://ethresear.ch/t/secret-non-single-leader-election/11789), and on other [networking](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763#sassafras-25) [approaches](https://ethresear.ch/t/simplified-ssle/12315).

However, most of these approaches involve modifying Ethereum’s consensus layer and that’s a procedure that requires careful security analysis and significant engineering efforts.

Keep checking [our research portal](https://ethresear.ch/) for the latest updates in this line of work.

## Conclusion

We hope this post was informative to you; especially if you happen to be a home staker or plan to become one. In preparation for The Merge, we would suggest you keep in mind the DoS resilience of your validator so that you can keep the Ethereum network safe and sound ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

If you are already protecting your validator from DoS attacks using vouch or any other approach, we would love to learn more in the comments section.

Cheers!

## Replies

**yorickdowne** (2022-07-14):

Note that attesting on CLs A and B and proposing via CLs D and E is not currently supported by Vouch: It only has one `submitter` for everything. The strategies you see are actually selection strategies.

Jim McDonald had this to say about dDoS:

“Regarding DDOS, it isn’t so easy to stop a beacon node from broadcasting a single proposal so it’s more likely that an attack would attempt to overwhelm a node prior to the proposal, either through an eclipse attack or just DDOSing it a slot or two in advance so that the block it produces is ultimately orphaned.  The way that Vouch could avoid that would be to have a node that is on the list of nodes from which it obtains proposal data, but not on the list of submitters.  So there is always a “listen only” node that should be up-to-date when it comes to Vouch creating the proposal.”

This can be done in Vouch thusly:

Assume I have CL nodes A,B,C.

Use A,B for submitters

And A,B,C for all selection strategies

Even if A and B get attacked, C should still have the proposal ready, and keeping a node from actually submitting the thing is non-trivial

---

**mcdee** (2022-08-03):

Note that as of Vouch 1.5.0 it is possible to have separate beacon nodes for submission of different types of information (attestations, proposals, sync committee messages *etc.*), which allows a beacon node to be used purely for broadcasting block proposals if so desired.

It also opens up the opportunity for there to be altruistic “public beacon nodes” that accept block proposals via the REST API from any source and broadcast them (assuming they meet validity requirements, of course), which would make DDoSing a validator very difficulty indeed.

