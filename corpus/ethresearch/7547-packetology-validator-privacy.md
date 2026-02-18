---
source: ethresearch
topic_id: 7547
title: "Packetology: Validator Privacy"
author: jrhea
date: "2020-06-16"
category: Networking
tags: []
url: https://ethresear.ch/t/packetology-validator-privacy/7547
views: 7706
likes: 26
posts_count: 13
---

# Packetology: Validator Privacy

*Special thanks to [TXRX research team](https://twitter.com/txrxresearch), [@AgeManning](/u/agemanning), [@protolambda](/u/protolambda), [@djrtwo](/u/djrtwo), [@benjaminion](/u/benjaminion), [@5chdn](/u/5chdn)*

The Eth2 community has long speculated that validator privacy will be an issue.  For background, refer to this issue [@jannikluhn](/u/jannikluhn) opened on validator privacy almost 2 years ago:

- Brainstorming about validator privacy · Issue #5 · ethresearch/p2p · GitHub

[@liochon](/u/liochon)  suggests the following solution here:

- Cryptographic sortition: possible solution with zk-snark

and [@JustinDrake](/u/justindrake) improves on it:

- Low-overhead secret single-leader election

Despite all this, Eth2 still doesn’t provide privacy preserving (alliteration ![:white_check_mark:](https://ethresear.ch/images/emoji/facebook_messenger/white_check_mark.png?v=14)) options for validators.  To be fair, no one has demonstrated a method of exposing validator IP addresses.  As a result, the problem has been somewhat limited to the existential realm.  With the Phase 0 launch growing closer, I have been giving the following question a fair amount of thought:

> What is the simplest way to deanonymize validators?

This post is dedicated to exploring this question.

## Data Collection

The data for the following analysis was collected on the Witti Testnet from Wednesday, June 10, 2020 through Thursday, June 11 by a single [network agent](https://github.com/prrkl/imp) designed specifically to crawl and collect data on the eth2 network. The network agent uses Sigma Prime’s implementation of [discv5](https://github.com/sigp/discv5) and the gossipsub implementation they contributed to [rust-libp2p](https://github.com/libp2p/rust-libp2p).

The data collection was done in two phases.  First, the network agent crawled the Witti testnet in order to locate most/all of the testnet nodes.  In order to optimize the DHT crawl, some minor modifications were made to Discv5 params:

- MAX_FINDNODE_REQUESTS: 7
- MAX_NODES_PER_BUCKET: 1024

**Crawl Summary**

- total node count: 134
- validating node count: 78
- non-validating node count: 56

> Note: the ENR attnets field was used to determine if a node hosts validators

Next, nodes discovered during the crawl were used to select peers and begin logging gossip messages. Minor modifications were made to gossipsub params:

- mesh_n_high: set to the estimated number of validating nodes
- mesh_n_low: set to 1/3 of the estimated number of validating nodes
- mesh_n: set to 2/3 of the estimated number of validating nodes
- gossip_lazy: set to 0

In addition, the gossipsub LRU cache was remove to enable the logging of duplicate messages.

> Note: Blocks were the only gossip messages logged.

**Gossip Summary**

- Starting slot: 105787
- Ending slot: 112867
- Number of slots: 7080
- Number of peers: 17
- Number of peers validating: 11
- Number of peers not validating: 6

Data from the DHT crawl was joined with Gossip data to create a dataset with the following fields:

[![](https://ethresear.ch/uploads/default/original/2X/6/62e6ca2175aff61995bd61da63ced6b8afb541fb.png)508×239 6.81 KB](https://ethresear.ch/uploads/default/62e6ca2175aff61995bd61da63ced6b8afb541fb)

## Data Analysis

Given the data collected, do you think it is possible to determine (with a high degree of confidence) the ip address associated with any of the active validators?

Let’s start by looking for peers that always notify the agent first with respect to blocks created by particular proposer indexes.

[![](https://ethresear.ch/uploads/default/original/2X/b/b334344b34efce8c9390f3385c5974c7f6972875.png)962×347 29.7 KB](https://ethresear.ch/uploads/default/b334344b34efce8c9390f3385c5974c7f6972875)

Our peers change and anomalies happen so it’s probably okay if a particular peer isn’t ALWAYS the first.  Next, we need to transform peer_id into a categorical variable that can be included in a visual analysis.

[![](https://ethresear.ch/uploads/default/original/2X/9/9ae7ba0f58c2922ade8e196de24cfeb7d83a343f.png)509×479 34.7 KB](https://ethresear.ch/uploads/default/9ae7ba0f58c2922ade8e196de24cfeb7d83a343f)

As you can see, peer_id can be conveniently mapped to a categorical variable peer_id_cat.  This makes it easier to plot (and even use in models). Since we are paying attention to what peer is first to deliver a block, it’s probably a good idea to track what peers are active and when.

[![](https://ethresear.ch/uploads/default/optimized/2X/3/30ec2e2d7e3849e96856e2ecb2decc4cff7cad58_2_690x443.png)700×450 14.1 KB](https://ethresear.ch/uploads/default/30ec2e2d7e3849e96856e2ecb2decc4cff7cad58)

This gantt chart gives us a rough idea when/if the peer is still actively sending the agent blocks.

Now we are ready to look at some different views of proposer index vs. the first peer id notify the agent of the corresponding blocks.

[![](https://ethresear.ch/uploads/default/optimized/2X/d/dbff6ded3ab5a8efc775695c0351bc0d60f1bec6_2_690x336.png)1003×489 124 KB](https://ethresear.ch/uploads/default/dbff6ded3ab5a8efc775695c0351bc0d60f1bec6)

Notice how there seems to be a large consecutive sequence of proposer indexes associated with a single peer id?  If I deposited a bunch of eth in order to activate 128 validators, then wouldn’t they have consecutive indexes in the validator registry?  How convenient…for me. Let’s zoom in.

[![](https://ethresear.ch/uploads/default/optimized/2X/1/1a7a462ebc2bea957a22395a060d405bfad56401_2_690x336.png)1003×489 17.1 KB](https://ethresear.ch/uploads/default/1a7a462ebc2bea957a22395a060d405bfad56401)

Just like before, the x-axis is proposer index, but this time the y-axis represents peer-id.  The more times a proposer is selected and the same peer notifies the agent, then the fatter the line.  If many different peers have been the first to notify the agent, then it will just look like the walls are melting (aka noise).

#### Finale

[![](https://ethresear.ch/uploads/default/optimized/2X/3/383b98f770d26a3acc0a5f954134c3596d6cdbd7_2_586x500.png)786×670 189 KB](https://ethresear.ch/uploads/default/383b98f770d26a3acc0a5f954134c3596d6cdbd7)

The diagram above outlines my thought process.  No models.  Just plots. This only scratches the surface of what’s possible.

#### Denouement

I was looking at the plots above and realized that I should probably verify my guess with known validator indices.  Remember peer-id: `16Uiu2HAmK3aw5p4Uw7RYRFeUcL4u1pg3u6JN8MnyT5wRshNLvHqU` (aka peer_id_cat = 6)?  I looked up the associated IP, saw it was in Berlin and assumed it was Afri. He was generous enough to share the public keys of his 384 validators so that I could validate my methodology.

If Afri has 384 validators, then why was I only able to predict 128?  Simple.  The agent wasn’t peered with Afri’s other validating nodes so the data didn’t provide strong signal.  This indicates that this methodology provides some resistance to false positives.

## Suggestion(s)

Batched deposits resulting in consecutive validator indices running on the same node is a dead giveaway.  This can be easily exploited. **At a minimum, we should suggest some best practices for splitting keys across nodes.**

## Future Work

- follow-up post on DHT analysis
- follow-up post on Gossip analysis
- derive a model to output ip address and probability for a given validator index
- look at other network messages besides just blocks
- take a closer look at the relationship between message_size and arrival time variance.

## Replies

**Mikerah** (2020-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> At a minimum, we should suggest some best practices for splitting keys across nodes.

I don’t think this would actually help with anything, from a privacy perspective. If an adversary takes into account on-chain activity, in addition to any network layer info, I’m pretty sure they can easily map on-chain and network layer identities together.

---

**jrhea** (2020-06-17):

Sure, it’s an arms race - most measures have countermeasures.  What I am saying is that if nothing else changes…I suggest not activating batches of validators all at once and assigning them to the same node.

---

**arnetheduck** (2020-06-18):

A little of this came up during initial talks about networking design and some steps were taken to maintain basic information hygiene and leave the door open for future solutions:

- in gossip, the initial design was to include signatures / keys of the originator of a message - the thought was that this should be used to identify spammers, but more careful thought revealed that spam is best handled locally between neighbors and not with a global identity (even if its tempting to take that shortcut), thus clients should now be running with signatures disabled so that the origin of a message is less obvious as it gets propagated through the network (this feature still exists in libp2p, so care must be taken to keep it disabled)
- libp2p-level peer id’s themselves can be cycled by clients - of course, this doesn’t help when ip’s are static, but again, it helps maintain basic hygiene such that the cost of analysis goes up without any real loss in performance
- the protocol has been design in such a way that there are no strong ties between validator identity and network identity - this means for example that it remains possible to cycle a validator identity between beacon nodes - this will of course only work on the beefiest beacon nodes that can support a sufficient number of attestation subnets such that it’s less obvious from the subscription pattern where the validator is attached. I’d like to think that the core issue here is that we still assume trust between beacon node and validator client.

---

**jrhea** (2020-06-18):

> libp2p-level peer id’s themselves can be cycled by clients - of course, this doesn’t help when ip’s are static, but again, it helps maintain basic hygiene such that the cost of analysis goes up without any real loss in performance

Tracking cycled peerid’s is trivial to overcome.  I already track ENRs as they change.  Furthermore, if peer reputation is tracked by peerid then cycling peerid’s to confuse attackers also puts a burden on the client.

> the protocol has been design in such a way that there are no strong ties between validator identity and network identity - this will of course only work on the beefiest beacon nodes that can support a sufficient number of attestation subnets such

Sure, this will definitely work.  We could also wall off validating nodes with other nodes and cycle those ips.

We could even use Cloudflare to protect us from denial of service attacks, but relying on large scale sophisticated setups just encourages centralization and is a disappointing outcome.  ETH2 protected by Cloudflare is not a great message.

---

**djrtwo** (2020-06-18):

As noted, the fact that nodes leak information about their validators is not a new discovery. The sending of 1 to 2 messages per epoch per validator leaks info and would allow for trivially de-anonymizing nodes wrt validators unless operators are using more sophisticated measures.

As [@arnetheduck](/u/arnetheduck) noted, a design goal for early phases is to not tightly couple a validator ID to the node and thus allow for any level of sophistication, obfuscation, load balancing, etc when creating a setup that is sufficient for your validation needs.

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> At a minimum, we should suggest some best practices for splitting keys across nodes.

Agree with [@Mikerah](/u/mikerah) here, on mainnet, the obvious place to look for de-anonymizing nodes wrt validators is going to be consensus messages being broadcast to gossip and originating from various nodes. Splitting validators won’t really obfuscate this very much and would just result in more nodes that you need to secure.

IMO, the biggest concern for this type of de-anonymization is strategic DoS-ing of validators at particular slots depending on their assigned role (e.g. DoS the next beacon block proposer). If someone were pursuing this avenue of attack (assuming they’ve successfully de-anonymized all nodes), they would look at the current proposer shuffling and attempt to DoS each proposer at each consecutive slot. If they prevented *all* block proposals for an epoch, the attacker could impose a liveness failure (inducing the network to not be able to justify/finalize an epoch).  If instead, they were only able to prevent a significant but *not all* proposals, there is enough room for an epoch’s worth of attestations (in most cases) even if 50% of proposals fail. We can make this number better (at the cost of bigger/more expensive blocks by increasing `MAX_ATTESTATIONS` to 256).

There is a wealth of tools, strategies, best practices, and other mitigations for DoS protection that need to be explored and made readily accessible to home/hobbyist stakers (those, in my estimation that are at highest risk to being strategically DoS’d). For Phase 0 launch, hardening of nodes (rather than the protocol) is my suggestion. At the same time I do suggest we continue to dig into single secret leader election and other protocol hardening techniques.

---

**Mikerah** (2020-06-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> For Phase 0 launch, hardening of nodes (rather than the protocol) is my suggestion. At the same time I do suggest we continue to dig into single secret leader election and other protocol hardening techniques.

I would suggest that the [sentry node architecture](https://forum.cosmos.network/t/sentry-node-architecture-overview/454) is looked into for this purposes (I was suppose to write about this a few months ago but I got caught up in other things). That way, we can at least have decent DoS resistance without relying on validator privacy yet.

---

**jrhea** (2020-06-18):

> Agree with @Mikerah here, on mainnet, the obvious place to look for de-anonymizing nodes wrt validators is going to be consensus messages being broadcast to gossip and originating from various nodes. Splitting validators won’t really obfuscate this very much and would just result in more nodes that you need to secure.

In afri’s case, he had 3 nodes and 384 validators.  He activated all 384 validators in batch and they were added to consecutive validator registry indexes. Then he took the first 128 validators and put them on node 1, the second 128 validators and put them on node 2 and the third 128 validators on node 3.  If instead, he slowly activated them allowed other people to mix their validators into the registry and maybe shuffled what validators he assigned to one of his 3 nodes…then I wouldn’t have been able to deanonymize them by eyeballing it.  All 3 nodes were on the same ip anyways adding more nodes wouldn’t have helped him.

> There is a wealth of tools, strategies, best practices, and other mitigations for DoS protection that need to be explored and made readily accessible to home/hobbyist staker.

Ya good point.  If u want to defeat this particular exploit follow my advice and don’t batch activate a bunch of validators and assign them to the same node.  At least shuffle them and if u can let a few more activations mix in.  Can it be defeated? Yes, but if nothing else changes in the protocol (like automatically queuing up new validators for mixing), then it’s better than nothing.

Then again, it’s just a suggestion.  It’s not really a solution to the core problem.

---

**jrhea** (2020-06-18):

> I would suggest that the sentry node architecture  is looked into for this purposes (I was suppose to write about this a few months ago but I got caught up in other things)

So u r suggesting this as a stopgap and not necessarily a permanent solution, right?  Seems reasonable, but I hope it doesn’t discourage research into validator privacy.  If u do the writeup, it would be interesting to hear your take on how to integrate it into eth2

---

**Mikerah** (2020-06-18):

I don’t think employing the sentry node architecture should affect research into validator privacy but many other chains such as Cosmos, Oasis and Polkadot are deploying this architecture for the main purpose of DoS resistance.

As for whether this is a stopgap or a permanent solution, that would depend on the needs of validators. I don’t see why it this architecture couldn’t be combined with other protocols and techniques for validator privacy and thus become a more permanent solution.

---

**jgm** (2020-06-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> At the same time I do suggest we continue to dig into single secret leader election and other protocol hardening techniques.

Perhaps only tangentially related to the topic, but can we use this method (or something similar) to select aggregators as well?  Seems like aggregators could be DOSed similarly to proposers.

---

**protolambda** (2020-06-18):

[@jgm](/u/jgm) I think aggregators are already selected privately at random based on a signature. Some ratio of the subnet gets to play the aggregator, and submit an attestation aggregate to the global net, along with a proof.

See: https://github.com/ethereum/eth2.0-specs/blob/520ad97c3e8a5a6694709a145bb0578366899bda/specs/phase0/validator.md#aggregation-selection

---

**Mikerah** (2020-07-29):

Another idea I had recently for a short-term but not complete solution would be to limit who can query a node for its bucket table during discovery. There are protocols such as Brahms that were considered for using in eth2 but due to the lack of support for querying metadata, they were no longer considered. If there’s a DHT design that can support private querying of metadata and limits a node from just being able to query a validator, then it has only partially solved the problem described in this post.

