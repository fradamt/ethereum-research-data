---
source: ethresearch
topic_id: 20463
title: Privacy Problems in the P2P Network and What They Tell Us
author: liobaheimbach
date: "2024-09-20"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/privacy-problems-in-the-p2p-network-and-what-they-tell-us/20463
views: 920
likes: 8
posts_count: 1
---

# Privacy Problems in the P2P Network and What They Tell Us

Authors: [Lioba Heimbach](https://liobaheimba.ch/), [Yann Vonlanthen](https://yannvonlanthen.com/), Juan Villacis, [Lucianna Kiffer](https://luciannakiffer.com/), [Roger Wattenhofer](https://disco.ethz.ch/)

Preprint: [[2409.04366] Deanonymizing Ethereum Validators: The P2P Network Has a Privacy Issue](https://arxiv.org/abs/2409.04366)

## TL;DR

The messages exchanged in the Ethereum P2P network allow a silent observer to deanonymize validators in the network, i.e., map a validator to an IP address of a node in the network. Our deanonymization technique is simple, cost-effective, and capable of identifying over 15% of Ethereum’s validators with only three days of data. This post discusses the technique, its implications, and potential mitigations to protect validators’ privacy in the P2P network.

## Background

Ethereum’s P2P network is what allows validators to exchange important messages like blocks and attestations, which keeps the blockchain running. With over a million validators, it’s not practical for each one to send a vote (attestation) to every node for every block, especially to keep Ethereum accessible to solo stakers. To make things manageable, voting (i.e., attestations by validators) is divided in two main ways:

**Time Division Across Slots**: Validators only need to vote once per epoch (i.e., once every 32 slots), in a random slot. Thus, only a fraction are voting in a given slot.

**Network Division Across Committees**: Validators are split into 64 *committees*. Within each committee, a set of validators is assigned as *aggregators* that collect and combine attestations into a single aggregate. This division of attestations into committees is further mirrored in the network layer, which is also divided into 64 attestation *subnets (overlay sub-networks)*. Each committee is assigned to one of these 64 subnets, and the corresponding attestations are broadcast only within the respective subnet. These subnets are also referred to as *topics* in the context of GossipSub,  the underlying P2P implementation used by Ethereum.

**Attestation Propagation in GossipSub:** When a validator signs an attestation, it gets published to its specified subnet by sending it to a subset of peers that are part of the subnet. The node hosting a validator does not need to be subscribed to this specific subnet, since their committee changes every epoch. Instead, each node in the network subscribes to two subnets by default, and participates in propagating attestations only in these two subnets - these are known as *backbone duties*. Additionally, each node maintains a connection with at least one peer in each subnet so that their own attestations can be sent to the correct subnet in one hop.

## Deanonymization Approach

Given the background on Ethereum node behavior, we describe how an ideal peer (a peer who gives us perfect information) would behave. Let us assume we are connected to a peer running V validators who is a backbone in two subnets. The peer’s validators will attest V times per epoch. Let us assume we receive perfect information from this peer, meaning they forward all attestations they hear about in their two backbones to us. In each epoch, we will receive V attestations from our peer for their validators, and N\cdot \frac{2}{64} for all other N  validators.

**Observation:** An ideal peer will only send us an attestation in a subnet they are not a backbone of if they are the signer of the attestation.

Thus, in this scenario, we receive all attestations for the V validators of the peer and can distinguish them as the only attestations we do not receive from the two backbones of the peer. Thus, linking validators to peers in this scenario is trivial.

### Case Study

In practice, however, network message data is not perfect. To showcase this, we plot the attestations received from an example peer across time and subnets. On this peer, we will identify four validators associated with the peer; their respective attestations are highlighted in red, blue, yellow, and green, while the remaining attestations are shown in pink. Notice that the attestations from these four validators, who happen to have consecutive identifiers, appear equally distributed across subnets. In contrast, the vast majority of attestations come from the two subnets where the peer acts as a backbone (subnets 12 and 13 for the sample peer). Thus, we can locate validators on our peers by observing how the attestations belonging to a validator, which we receive from the peer, are distributed across subnets.

Additionally, and this is where the imperfect information comes into play, the validators hosted on the peer are occasionally tasked with being aggregators in a subnet approximately every 30 epochs per validator. During these times, they temporarily become a backbone (smaller pink horizontal strips) for these subnets and receive attestations from multiple validators belonging to the subnet.

[![casestudy](https://ethresear.ch/uploads/default/optimized/3X/8/c/8c8f040874963de5a0c732cf369fb3fde4802d4a_2_690x388.png)casestudy1708×962 68.1 KB](https://ethresear.ch/uploads/default/8c8f040874963de5a0c732cf369fb3fde4802d4a)

### Heuristics

Based on the above observations and other network behaviors which lead to imperfect information such as temporary disconnects, we develop a set of heuristics to link a validator with a node. We verify our results  (see [pre-print](https://arxiv.org/abs/2409.04366) for more details).

### Comparison to Other Approaches

We are aware of three existing approaches to deanonymize peers in the P2P network that, similarly to us, only rely on observing messages.

A [research post](https://ethresear.ch/t/packetology-validator-privacy/7547) explores mapping validators to peers by observing which peer consistently first broadcasts a block. There also exists a [medium post](https://medium.com/hoprnet/proof-of-stake-validator-sniping-research-8670c4a88a1c) that discusses using attestation arrival times in a similar fashion. The presented analysis is based on data collected on the Gnosis Beacon Chain. Finally, in parallel to our work, a further [research post](https://ethresear.ch/t/estimating-validator-decentralization-using-p2p-data/19920) discussed using dynamic subscriptions to deanonymize validators in the P2P network.

We believe that compared to these approaches our method requires significantly less data or concurrent network connections (in the case of timing analyses). Further, it is less prone to noise  in comparison to those approaches based on arrival times and also works if a node hosts more than 62 validators (this is the limit of the approach based on dynamic subscriptions). Thus, we suspect it to be able to more precisely deanonymize a larger proportion of the network in less time.

## Measurement Results

By deploying our logging client across four nodes over a period of three days, we were able to deanonymize more than **15% of Ethereum’s validators** in the P2P network. Our nodes were located in Frankfurt (FR), Seoul (SO), Virginia (VA), and Zurich (ZH). By deploying a greater number of nodes and running the measurement for longer, we presume this figure would increase.

With the data we collected, we can also make additional observations about the geographic decentralization and hosting of validators, as well as the behavior of staking pools.

### Geographic Decentralization

We show the distribution of validators across countries in the following figure both overall and  separately for the four nodes we ran. We locate the largest proportion (around 14%) in the Netherlands. Further, 71.53% of the validators we locate are in Europe, 11.95% are in North America, 11.52% are in Asia, 4.90% are in Oceania, 0.06% are in Africa and 0.03% are in South America.

Additionally, we notice geographical biases, e.g., the SO node’s high relative proportion of deanonymizations in Australia and South Korea. Thus, we presume that the skew towards Europe could be a result of us running two out of the four nodes in Europe.

[![country_validators](https://ethresear.ch/uploads/default/original/3X/f/4/f45fb3a3f65719354e1dc95150461dccb139b567.png)country_validators693×219 5.28 KB](https://ethresear.ch/uploads/default/f45fb3a3f65719354e1dc95150461dccb139b567)

### Cloud Hosting

We perform a similar analysis to understand how peers are run - if they run hosted on cloud providers or through residential ISP (likely home stakers). Overall, around 90% of the validators we locate are run through cloud providers, with the other 10% belonging to residential ISPs. We plot the distribution across organizations and find that  eight out of the ten largest organizations are cloud providers. Further, we locate the largest number of validators in Amazon data centers, i.e., 19.80% of the validators we locate.

[![org_validators](https://ethresear.ch/uploads/default/original/3X/b/d/bdf51bb01378fcc59ecf23b602ee18f3e0dd65fd.png)org_validators693×219 5.26 KB](https://ethresear.ch/uploads/default/bdf51bb01378fcc59ecf23b602ee18f3e0dd65fd)

### Staking Pools

We also take a deeper look at the practices of the  five largest staking pools (Lido, Coinbase, [Ether.Fi](http://Ether.Fi), Binance, and Kraken). On average, we observe 678 validators on a given peer for staking pools, with the largest node running 19,263 validators (!).

> Additionally, many staking pools utilize node operators and many of the node operators run validators for various staking pools. This creates a dependency between the staking pools. In particular, we find five instances of validators from two different staking pools that utilize the same node operators being located on the same machine.

## Security Implications

**Taking Out Previous Block Proposers**: One security issue that’s been discussed is the incentive for the proposer of slot n+1 to prevent the proposer of slot n from publishing a block. If successful, the slot n+1 proposer can include both the missed transactions and new ones in their block, earning more in fees. Since proposers are known in advance (about six minutes), an attacker could deanonymize the proposer for slot n and launch a temporary DoS or BGP hijack attack, preventing them from submitting their block. Importantly, this attack only needs to last for four seconds - the window for making a block proposal.

**Breaking Liveness and Safety**: Extending this attack, an attacker could continuously target the upcoming proposers to stop the network’s progress. If more than one-third of block proposals are missed, Ethereum’s finality gadget won’t be able to finalize blocks, halting the network. Even worse, safety could be compromised as many Ethereum light clients assume the chain head is finalized. By breaking network synchrony through DoS or network partitioning, attackers could cause serious issues.

## Mitigations

To mitigate these security risks one can either improve privacy in the P2P network or protect against potential attacks. We discuss both avenues.

### Providing anonymity

**Increase Subnet Participation**: Validators could subscribe to more subnets than the default, making it harder for adversaries to link specific attestations to validators. This increases the communication overhead on the network, potentially undermining Ethereum’s goal of enabling solo stakers to run validators with minimal resources. However, given the increase of the [MAX_EFFECTIVE_BALANCE](https://ethresear.ch/t/increase-the-max-effective-balance-a-modest-proposal/15801) in the upcoming hardfork there might be room for a slight increase in the number of P2P messages.

**Run Validators Across Multiple Nodes**: Validators could distribute their attestation broadcasts across multiple nodes, making it harder to deanonymize them. While this increases operational costs, it can enhance privacy by spreading validator responsibilities across different IP addresses.

**Private Peering Agreements**: Both Lighthouse and Prysm clients allow validators to set up private peering agreements, where a group of trusted peers helps relay gossip messages. While this improves performance and reliability, it also provides some privacy, making it harder to trace validators to a single IP. Instead, an attacker would have to target multiple peers in the agreement. However, finding trusted peers can be costly and difficult, especially for smaller stakers.

**Anonymous Gossiping**: Protocols like Dandelion and Tor have been proposed to enhance anonymity. Dandelion, for example, sends messages through a single node first (the “stem” phase) before broadcasting to the network (the “fluff” phase), which helps conceal the message origin. However, these methods introduce delays and might not be fast enough for the Ethereum P2P network.

### Defending Against DoS

**Network Layer Defenses**: The libp2p framework used for the Ethereum P2P layer already includes some defenses like limiting the number of connections, rate-limiting incoming traffic, and auto-adjusting firewalls. However, these aren’t foolproof, and manual intervention might still be needed during attacks.

**Secret Leader Election**: Another potential defense against DoS attacks is keeping the identity of block producers secret until they propose blocks. This idea, called **secret leader election**, avoids other issues and looks promising. Some proposals have been made for Ethereum, but they’re still in the early design phase as far as we are aware.
