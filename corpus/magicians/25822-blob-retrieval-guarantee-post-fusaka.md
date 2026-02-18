---
source: magicians
topic_id: 25822
title: Blob retrieval guarantee post Fusaka
author: koenmtb1
date: "2025-10-15"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/blob-retrieval-guarantee-post-fusaka/25822
views: 528
likes: 30
posts_count: 13
---

# Blob retrieval guarantee post Fusaka

On behalf of [Aztec](https://aztec.network/), I’d like to bring up a point around blob retrieval.

There’s been a lot of focus on the consensus client side on giving guarantees that blobs are stored. But we’re actually running into a problem with our implementation on how to retrieve blobs.

Prior to Fusaka each decentralised sequencer on the Aztec network required a “regular” consensus client endpoint.

The Aztec node was configured to retrieve blobs from the consensus client, for which it had access to the latest 3 weeks worth depending on consensus client pruning settings.

In the new design given that blobs are split up in 128 columns we will require the sequencer operators to run an L1 consensus “supernode” to make sure the Aztec node has access to all the data. (or atleast 64 columns to allow for reconstruction, but most consensus clients don’t currently support manually setting the # of columns it wants)

This comes with very high resource requirements, especially on the networking side of things. Basically from our perspective making it close to impossible for home stakers to run the entire stack at home. (assumptions made based on numbers published by [ethPandaOps here](https://ethpandaops.io/posts/fusaka-bandwidth-estimation/)) A full home staking stack requiring an Ethereum consensus and execution client and the Aztec node.

For our roadmap we would like to get an understanding on potential paths for us to go down. We see some possible solutions on the Ethereum consensus client side, see below. But is blob retrieval something that was thought about from the L2 consumption perspective?

Thoughts on solutions

- Lite Supernodes → A super node that just retrieves enough columns to reconstruct (or all columns to lower compute requirements and delay), but is excluded from having to seed all columns to peers (beyond the 4 minimum). This would mean the consensus client would behave exactly like it used to pre-Fusaka. (easiest, similar to an already suggested idea)
- Tagging blobs → Being able to tag blobs and configure consensus clients to force it to pro-actively retrieve only the full data for the blobs with a certain tag. (harder, might require protocol changes)
- Separate tooling → Develop and support separate tooling to do blob retrieval. We could in that case integrate this natively in to our node.

## Replies

**thegaram33** (2025-10-16):

We also ran into this issue at Scroll, though to a lesser extent since our node support multiple blob data sources (beacon node, AWS S3 snapshot, Blobscan API, BlockNative API).

Given that consensus clients will prune blobs after a while anyway, I think all L2s need some kind of blob archival mechanism. This can be in-protocol (e.g. require a proof of long-term storage from Filecoin when submitting the blob to Ethereum), or out-of-protocol (e.g. AWS S3 blob snapshot).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/koenmtb1/48/16226_2.png) koenmtb1:

> Tagging blobs → Being able to tag blobs and configure consensus clients to force it to pro-actively retrieve only the full data for the blobs with a certain tag. (harder, might require protocol changes)

I like the idea of configuring the consensus client to store specific blobs, maybe even for long-term storage (exclude from pruning). A simple rule like *“store all blobs where the blob tx sender/receiver is address X”* would probably cover most rollups today.

---

**koenmtb1** (2025-10-16):

Thanks for the weigh-in!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thegaram33/48/13347_2.png) thegaram33:

> I think all L2s need some kind of blob archival mechanism. This can be in-protocol (e.g. require a proof of long-term storage from Filecoin when submitting the blob to Ethereum), or out-of-protocol (e.g. AWS S3 blob snapshot).

Just adding that this is not preferred for our decentralisation goals. Ideally there would be a system allowing users to retrieve their own blobs directly from a consensus client to reduce centralisation risk.

Using something like Filecoin goes against the point of using Ethereum for DA in our opinion.

---

**thegaram33** (2025-10-16):

> Ideally there would be a system allowing users to retrieve their own blobs directly from a consensus client

Yes, but unfortunately this does not work for historical sync because Ethereum does not guarantee long-term storage of blobs.

As long as blobs can be validated against L1 data (e.g. by comparing blob hashes), then any source to obtain the blob data is fine. I think the ideal UX is a centralized fast default (blob snapshot in the cloud) with a decentralized fallback (e.g. L2 nodes share the data with each other).

---

**koenmtb1** (2025-10-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thegaram33/48/13347_2.png) thegaram33:

> Yes, but unfortunately this does not work for historical sync because Ethereum does not guarantee long-term storage of blobs.

Totally! We have a (decentralised) snapshot system for that. I was more referring to blobs within the 4096 epochs data custody period that we require for live operation.

---

**bbusa** (2025-10-16):

Could you explain a little how does a decentralized sequencer work?

Do each sequencer have to publish all blobs to L1?

How many blobs per slot do you plan to publish to L1?

Generally download bandwidth is not a problem for home stakers, locally built blocks which require high upload speed is the most critical path.

As far as I understand aztec sequencers would only need to download 128 columns but not actually upload a huge amount of data.

You reference that today people only have to run a “standard” node. That standard node is a “supernode” as currently everyone custody every blob on the network.

---

**MicahZoltu** (2025-10-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbusa/48/8136_2.png) bbusa:

> Generally download bandwidth is not a problem for home stakers, locally built blocks which require high upload speed is the most critical path.

[Fusaka bandwidth estimation | ethPandaOps](https://ethpandaops.io/posts/fusaka-bandwidth-estimation/) says:

> receive spikes to ~400 Mb/s, transmit to ~300 Mb/s. However, ignoring the spikes, the baselines data usage seems to be around 100 Mb/s. The higher blob count clearly amplifies bandwidth requirements for supernodes.

100 Mb/s is already more than many home stakers/sequencers have access to.  Even if we assume that the user has 100Mb/s they can dedicate *just* to following head of Ethereum (after accounting for anything else on the connection also using the internet), those 400Mb/s spikes are going to end up smoothed over several seconds due to saturation, and it is unclear how frequent those spikes will be.

The baseline I like to use is StarLink, because that is available in many parts of the world even when wired internet isn’t available or local quality is very low.  I believe that means ~50Mbps, and that connection likely also is serving other household users for things like video streaming and such, so really 10Mbps should be the target for “home participants” in any system.

---

**cskiraly** (2025-10-17):

There are a few things to note here:

1. Spikes are only happening if you have the bandwidth for them. If not, it is smoothed out by the network. It is a side-effect of testing with high bandwidth nodes, NOT a requirement.
2. How the network behaves when you don’t have the bandwidth for spikes and spikes are smoothed out is something to study separately. For this we have run tests with bandwidth restrictions, but there is still more space for testing. We are doing such tests and we will do these more intensively as we go towards higher blob counts.
3. For lower blob counts bandwidth requirement is definitely not in the hundreds of Mbps range. E.g., 10blobs/12sec is less then 1 blob/sec. Even if you would subscribe to all 128 column subnets, that’s less than 256 KB/s of data. Even if you add overhead, you are not going into the hundreds of Mbps space, you are in the single digit Mbps space.
4. GossipSub is adapting to available bandwidth to some extent already, and we are working on making it adapt more (see push-pull phase transition, lazy push, partial messages, etc.)
5. if one does not have the bandwidth, it should be perfectly fine to subscribe to 64 column only, and use CPU power to decode the blobs.
6. if one also doesn’t have the bandwidth to subscribe to 64 columns, subscribing to less and retrieving only the relevant blobs, filtering on the sender address, would also be fine. However, in the CL, in the current version we don’t have row topics or row-based ReqResp to support this well. These are part of the FullDAS design, but not in current PeerDAS. But we can work on adding them.
7. as a middle-ground, and without row-topics or partial messages, one could also think of requesting all the column of only the blocks that have relevant blob transactions. I don’t think we need this, as we have partial messages close to being finalized already.

---

**qzhodl** (2025-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/koenmtb1/48/16226_2.png) koenmtb1:

> This comes with very high resource requirements, especially on the networking side of things. Basically from our perspective making it close to impossible for home stakers to run the entire stack at home. (assumptions made based on numbers published by ethPandaOps here) A full home staking stack requiring an Ethereum consensus and execution client and the Aztec node.

[@thegaram33](/u/thegaram33) [@koenmtb1](/u/koenmtb1)

EthStorage, a decentralized storage Layer 2, provides long-term blob storage and retrieval for L2s.

In short, the L2 sequencer posts blobs via blob-carrying transactions to its batch inbox contract, which can then call the EthStorage contract to pay storage fees. A decentralized network of EthStorage nodes permanently stores these blobs while submitting on-chain proofs of storage. Later, L2 nodes can retrieve the blobs through the standard Beacon API via an EthStorage node.

Here’s a tutorial on integrating it with an OP Stack chain if you’d like to dive deeper: [OP Stack Tutorial | EthStorage](https://docs.ethstorage.io/rollup-guide/op-stack-tutorial)

---

**MicahZoltu** (2025-10-17):

Is low bandwidth a test scenario that is actively tested/exercised?  e.g., 10Mbps throttled connection, to see how things perform for each of the node types?

If not, I feel like that would go a long way to alleviating the concern that people (rightfully) have that Ethereum core devs keep cranking up the system requirements without thinking much about all of the home users.  If that data is available and the path well tested, I think it would be worthwhile to make it readily available and listed more visibly so people aren’t scared by the appearance of rapidly increasing node requirements.

---

**cskiraly** (2025-10-17):

Yes, it is actively tested. Partly we are still ramping up on this, but there is both large scale testing and small scale testing. For small scale, I’ve developed these tools:

- GitHub - cskiraly/ethereum-kurtosis-tc: Control network resources in Ethereum Kurtosis tests
- GitHub - cskiraly/ethereum-fork-testing: Run local test networks reproducing various scenarios around a hard fork

I’ve yet to publish some test results. Also note that we’ve introduced DAS, GossipSub improvements (and working on partial diffusion in the mempool) exactly to avoid cranking up system requirements. Of course there is no free lunch, but we can do a lot to keep home users happy and bandwidth requirements reasonable.

---

**koenmtb1** (2025-10-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbusa/48/8136_2.png) bbusa:

> Do each sequencer have to publish all blobs to L1?

The currently selected block proposer (selected at random from an epoch committee, which is selected at random from the entire active validator set) publishes the blobs for that block to the L1.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbusa/48/8136_2.png) bbusa:

> How many blobs per slot do you plan to publish to L1?

We currently have a maximum of 3 per block (36s on testnet), it’s up to the proposer to suggest how many it needs to publish all data.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbusa/48/8136_2.png) bbusa:

> As far as I understand aztec sequencers would only need to download 128 columns but not actually upload a huge amount of data.

Correct, or alternatively just 64 would allow the consensus client to reconstruct the blobs.

Download data isn’t as much of a concern. According to the ethPandaOps article the baseline download for a supernode is about 50 Mbps, which is acceptable to us. The problem lies in the upload requirement and spikes.

---

**Alambda** (2025-10-22):

Real talk. But dont think it will last.

