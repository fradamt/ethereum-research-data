---
source: ethresearch
topic_id: 21893
title: Doubling the blob count with Gossipsub v2.0
author: pop
date: "2025-03-07"
category: Networking
tags: [data-availability, p2p, scaling]
url: https://ethresear.ch/t/doubling-the-blob-count-with-gossipsub-v2-0/21893
views: 1977
likes: 26
posts_count: 13
---

# Doubling the blob count with Gossipsub v2.0

Authors: [Pop](https://github.com/ppopth), [Nishant](https://github.com/nisdas), [Chirag](https://github.com/chirag-parmar)

*tldr; with gossipsub v2.0, we can double the blob count from whatever is specified in Pectra*

*Gossipsub v2.0 spec: [here](https://github.com/libp2p/specs/pull/653)*

# Introduction

Gossipsub is a pubsub protocol over lib2p which is based on randomized topic meshes. The general message propagation strategy is to broadcast any message to a subset of its peers. This subset is referred to as the ‘mesh’. By controlling the outbound degree of each peer you are also able to control the amplification factor in the network.

By selecting a high enough degree you can achieve a robust network with minimum latency. This allows messages to be dispersed resiliently across a network in a short amount of time.

The mesh that is selected is random and is constantly maintained via gossip control messages to ensure that the quality of peers stays consistent and doesn’t deteriorate. Gossip Metadata is emitted during every heartbeat to allow peers who might have missed certain messages due to downstream message loss to be able to recover and retrieve them.

Each peer has a memory of all seen messages in the network over a period of time. This allows nodes to drop duplicates and prevents them from being further disseminated.Also having memory of messages which were propagated allows peers to make scoring decisions on their mesh peers. This allows them to prune lousy peers from the mesh and graft new ones in.

# Problem With Gossipsub Today

As demonstrated above gossipsub has some very desirable characteristics as a pubsub protocol. However, while you have a resilient network with minimal latency (assuming a high enough degree), Gossipsub as of its current design brings about a high level of amplification.

The tradeoff of the current design is if a network requires messages to be propagated with minimal latency it requires a large amount of amplification. This is problematic in networks which need to propagate large messages, as the amplification done is significant. If many of these large messages start being propagated in a network it would affect the general decentralization and scalability of the network.

For networks such as those Gossipsub v1.2 introduced a new control message called `IDONTWANT`. This control message allows a peer to tell its mesh peers not to propagate a message matching a particular message ID. The main goal of this is to prevent duplicates from being sent and reduce amplification in the network as a whole.

While this does help in reducing duplicates it ultimately relies on remote peers being able to act on the control message in time. If they do not, the message still ends up being forwarded wasting bandwidth on both the sender and the receiver. So how can we improve on this?

# Our Solution

We enshrine a lazy-pull mechanism adjacent to the original eager-push mechanism in v2 of GossipSub. With lazy-pull we only broadcast the message ids instead of the entire message. We do so by introducing two new control messages IANNOUNCE and INEED which carry a single message id within them.

In essence, an announcement of the message is made using IANNOUNCE and a request for the announced message is made using INEED. A node waits for the actual message as a response to INEED for a configured timeout.

If the timeout expires it tries to get the message from another peer (an individual node only sends INEEDs sequentially). When the timeout occurs, the node will also down-score the peer to prevent malicious peers from ignoring INEEDs and never sending back the message.

With such a lazy-pull mechanism we drop the number of duplicates to nearly zero, but, by trading off latency. To minimize the effect of increased latency we introduce the concept of an announcing degree. The announcing degree indicates the number of mesh peers chosen by a node at random for lazy-pull from within its mesh. Because this splits the mesh into two, `D_announce <= D` always.

Before forwarding the message to each mesh peer, the node will toss a coin to decide whether to send the message lazily with the probability of `D_announce/D` or otherwise send the message eagerly, so expectedly the node sends the message lazily to `D_announce` of its mesh peers and eagerly to `D-D_announce` of its mesh peers.

The formal [spec](https://github.com/libp2p/specs/pull/653) with its simplicity accommodates for future strategies minimizing the latency effects of a lazy pull mechanism. However, in this post we explore the concept of D_announce and some other strategies through simulations.

# Simulation Setup

> We used the implementation of Gossipsub v2.0 of go-libp2p as shown in this PR and used Shadow as a simulator.

We ran simulations with 1,000 nodes, 20% of which have the bandwidth of 1Gbps/1Gpbs and 80% of which have 50Mbps/50Mbps. The publisher always has 1Gbps/1Gbps in order to get consistent simulation results.

The latency between each pair of nodes are consistent with the real-world geographic locations which we adopt from the simulation tool [Ethshadow](https://github.com/ethereum/ethshadow). We decided to spend effort to make them as close to the real world as possible because we know that the round-trip time caused by IANNOUNCE/INEED has a significant impact on the result and it’s heavily dependent on geolocations.

Firstly we simulate the network of a single publisher publishing a single message with different message sizes. Secondly we simulate the network of a single publisher publishing multiples message with different numbers of messages where each has a size of 128KB.

Then we repeat what we mentioned with `D_announce=0,7,8` and with `D=8` and the timeout of 1 second. We ran `D_announce=7` to see if it will help when we add some randomness. In the cases of `D_announce=7,8`, we also change the heartbeat interval from the default CL value of 0.7s to 1.5s to reduce the number of duplicates from IHAVE/IWANT.

# Results

### Multiple messages

Firstly, we look at the simulations when a single publisher publishes multiple messages simultaneously.

[![cdf_num_0](https://ethresear.ch/uploads/default/optimized/3X/8/6/86a3bbcc31923069a7e6ec45b71dda564919cf54_2_666x500.png)cdf_num_0800×600 57.4 KB](https://ethresear.ch/uploads/default/86a3bbcc31923069a7e6ec45b71dda564919cf54)

[![cdf_num_7](https://ethresear.ch/uploads/default/optimized/3X/6/1/61e48a4732dc73e96f143e5c7f1dcc13fb81c000_2_666x500.png)cdf_num_7800×600 50 KB](https://ethresear.ch/uploads/default/61e48a4732dc73e96f143e5c7f1dcc13fb81c000)

[![cdf_num_8](https://ethresear.ch/uploads/default/optimized/3X/0/f/0f162f4c21ac992b42628c4166436348b63c7ae0_2_666x500.png)cdf_num_8800×600 51.5 KB](https://ethresear.ch/uploads/default/0f162f4c21ac992b42628c4166436348b63c7ae0)

You can see from the result that with `D_announce=0`, you can publish 16 messages with the deadline of 4 seconds while with `D_announce=7,8`, you can publish 32 messages. So we conclude that **we can double whatever the blob count is in Pectra**.

Also note that `D_announce=7` is also much better than `D_announce=8` because with the latter, the propagation can be delayed by the round-trip time from each hop. With the former, each node expectedly sends the message eagerly to one random peer to allow the message to propagate faster.

### Single message

Even if publishing a single message doesn’t matter much for Ethereum, we should still consider it because Gossipsub is a general-purpose pubsub protocol and publishing a single message is the most popular use case.

[![cdf_sizes_0](https://ethresear.ch/uploads/default/optimized/3X/3/5/35f1f0aad681b89951b06c1aae20247eb7bea93f_2_666x500.png)cdf_sizes_0800×600 65.4 KB](https://ethresear.ch/uploads/default/35f1f0aad681b89951b06c1aae20247eb7bea93f)

[![cdf_sizes_7](https://ethresear.ch/uploads/default/optimized/3X/2/9/29e14d9f9233ca7afadba5aff64e2ef5197e915f_2_666x500.png)cdf_sizes_7800×600 64.9 KB](https://ethresear.ch/uploads/default/29e14d9f9233ca7afadba5aff64e2ef5197e915f)

[![cdf_sizes_8](https://ethresear.ch/uploads/default/optimized/3X/4/5/4508f71f73daea504bebb6f63f6bdf8601dc4f1f_2_666x500.png)cdf_sizes_8800×600 64.4 KB](https://ethresear.ch/uploads/default/4508f71f73daea504bebb6f63f6bdf8601dc4f1f)

You can see from the result that we don’t gain any improvement from v2. Our hypothesis is that even if the bandwidth consumption is reduced, sometimes the links are idle because of the round-trip time.

### Duplicates

Let’s look at the average number of duplicates per message for the case of multiple messages.

|  | 1 msg | 2 msgs | 4 msgs | 8 msgs | 16 msgs | 32 msgs | 64 msgs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D_announce=0 | 4.515 | 5.492 | 5.658 | 5.686 | 6.161 | 7.394 | 9.232 |
| D_announce=7 | 0.598 | 0.565 | 0.586 | 1.259 | 0.767 | 1.482 | 2.244 |
| D_announce=8 | 0.192 | 0.804 | 0.179 | 0.395 | 0.769 | 0.673 | 1.236 |

You can see that the number has improved so much that further bandwidth optimisation probably would not benefit much.

We also noticed that almost all of the remaining duplicates are due to IHAVE/IWANT which we think we should reconsider how important it really is.

Now look at the average number of duplicates for the case of a single message.

|  | 128KB | 256KB | 512KB | 1024KB | 2048KB | 4096KB | 8192KB |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D_announce=0 | 4.515 | 4.749 | 5.122 | 5.832 | 8.909 | 11.022 | 12.990 |
| D_announce=7 | 0.598 | 2.284 | 1.163 | 2.506 | 4.078 | 6.971 | 9.275 |
| D_announce=8 | 0.192 | 1.777 | 1.087 | 1.950 | 3.762 | 5.927 | 8.692 |

The numbers look good for 128KB to 1024KB, but they did not improve much for larger messages. That is because larger messages take more time to send between peers and then INEED timeout is more likely to occur. It results in sending many INEEDs and then leads to receiving more duplicates.

# Concerns

The major concern of Gossipsub v2 is that we introduces a new parameter called INEED timeout, which is the time a node will wait for a message after sending INEED.

Setting the timeout is tricky. We don’t want malicious actors to ignore INEEDs or delay sending messages. We should set the timeout in a way that all honest nodes are able to follow most of the time.

When you down-score a peer after the timeout occurs, you also have to make sure that you don’t down-score too much. Otherwise, you will kick out honest peers too quickly when they occasionally trigger the timeout. A possible alternative would be to ignore `IANNOUNCE` messages from peers who have repeatedly ignored or responded too late to `INEED` messages previously rather than down-score them.

Currently we set the timeout to 1 second because even if you have three consecutive peers triggering the timeout, you would still be able to receive the messages within the deadline of 4 seconds or even better IHAVE/IWANT will sometimes help you get the message before the deadline. The simulation result also suggests that timeouts by honest nodes don’t make you miss the deadline.

# Acknowledgements

Thank [Vyzo](https://github.com/vyzo) for valuable comments on [AnnounceSub](https://github.com/libp2p/specs/pull/652) which was a predecessor of GossipSub v2.0.

# Further research

- Reconsider how important IHAVE/IWANT is. Can we remove it completely or we reduce its effect instead, such as by increasing the heartbeat interval, etc?
- Simulate the network with 5%, 10%, 20% of malicious nodes in the network, where malicious nodes mean nodes that ignore INEEDs.
- Define exactly how much a node should down-score a peer after a timeout occurs.
- Perhaps we don’t need the timeout for INEED, but it’s better to down-score peers based on how late they reply back the message.
- Integrate with Codex’s batch publishing and see the result.

# Resources

- Gossipsub v2.0 spec: Gossipsub v2.0 spec: Lower or zero duplicates by lazy mesh propagation by ppopth · Pull Request #653 · libp2p/specs · GitHub
- Gossipsub v2.0 implementation in go-libp2p-pubsub: Gossipsub v2.0 by ppopth · Pull Request #587 · libp2p/go-libp2p-pubsub · GitHub
- If you would like to re-run the simulation, you can use the following repo: GitHub - ppopth/pubsub-shadow

## Replies

**djrtwo** (2025-03-07):

This is great! I agree that having a protocol that can better balance between push vs pull, especially depending on message type, is really valuable.

On that note, I would suggest that `D_announce` is a per-topic configuration variable. For example, `attnets` probably has a different value that would be optimal.

(And if we go that route, maybe `D` should be configurable per message type/topic. I don’t believe it already is, right?)

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> Also note that D_announce=7 is also much better than D_announce=8 because with the latter, the propagation can be delayed by the round-trip time from each hop

Did you try this for other values of `D_announce`? Seeing a curve showing the relationship between values from 0 to D would be valuable

Funny to see that `0` is strictly worse (under these non-adversarial conditions). This is because duplicates are just wasting local/global bandwidth? Assuming we were hitting peak load locally or globally, you’d expect `0` to be strictly better. Maybe it’s worth running an experiment with all 1Gbps (or even 10Gbps) nodes to show that when bandwidth is not saturated, that push is faster. This would help us validate the hypothesis of why pull is faster for more bandwidth bound networks.

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> So we conclude that we can double whatever the blob count is in Pectra.

I’m concerned that this isn’t adequately capturing adversarial network conditions or poor mesh constructions. It does look very promising! But, I could imagine attack cases could degrade worse under this model.

Does shadow model any of the attack conditions that Testground did in the original [gossipsubv1.1](https://github.com/libp2p/specs/blob/6d38f88f7b2d16b0e4489298bcd0737a6d704f7e/pubsub/gossipsub/gossipsub-v1.1.md) parameter additions? For example, the “Covert Flash Attack” might more seriously disrupt a mesh that is being less opportunistic about push. that said, the gossip meta-data (IWANT/IHAVE) might still be sufficient to protect. Nonetheless, I do think that we should model some set of relevant p2p attack vectors when adding a significant change to the gossip protocol – the v1.1 set of attacks as a good basis.

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> Reconsider how important IHAVE/IWANT is. Can we remove it completely or we reduce its effect instead, such as by increasing the heartbeat interval, etc?

What is the relationship you see here? Yes, IHAVE/IWANT is similarly announcing for `pull` opportunities, but the major difference is that IHAVE/IWANT is to a *wider set* of peers than your mesh degree, D, and thus helps ensure distribution of messages even under adversarial p2p network conditions. Given that IANNOUNCE/INEED is upon the same set D, then it’s usage does not serve the same resilience purpose as IWANT/IHAVE (ensuring that if the narrow degree D is corrupted/disrupted, that the network can still communicate)

I do agree that revisiting IWANT/IHAVE, it’s timing, and load should be under consideration. I guess, you probably want IANNOUNCE/INEED to happen in quicker time frames than IWANT/IHAVE heartbeat to ensure that IWANT/IHAVE doesn’t become dominant wrt message broadcast.

---

Another idea is for `D_announce` to potentially be dynamic locally based on observations – e.g. how many duplicates normally getting, how far into the slot normally receiving message, etc – and for local adjustments to tune the network as a whole. Can of worms but might have some promising avenues

---

**nisdas** (2025-03-08):

> On that note, I would suggest that D_announce is a per-topic configuration variable. For example, attnets probably has a different value that would be optimal.
>
>
> (And if we go that route, maybe D should be configurable per message type/topic. I don’t believe it already is, right?)

Yeah, this would be a natural next step for us. We didn’t include it in the initial specification because we wanted to be able to complete the simulations in a reasonable amount of time without implementing per topic parameters.  v2 would be a good time to introduce this into the spec.

> Funny to see that 0 is strictly worse (under these non-adversarial conditions). This is because duplicates are just wasting local/global bandwidth? Assuming we were hitting peak load locally or globally, you’d expect 0 to be strictly better. Maybe it’s worth running an experiment with all 1Gbps (or even 10Gbps) nodes to show that when bandwidth is not saturated, that push is faster. This would help us validate the hypothesis of why pull is faster for more bandwidth bound networks.

For large messages, sending out so many messages at the same time saturates the uplink bandwidth which is why it shows an improved performance even against `0` in our simulations. Its the same reason why [batch publishing](https://ethresear.ch/t/improving-das-performance-with-gossipsub-batch-publishing/21713) has much better results.

I agree on validating this with new simulations with all the nodes having much higher bandwidth to eliminate uplink saturation. Alternatively we can also drop the message size ( 1kb) and run the simulation to show that `0` is strictly better in the absence of congestion

> I’m concerned that this isn’t adequately capturing adversarial network conditions or poor mesh constructions. It does look very promising! But, I could imagine attack cases could degrade worse under this model.
>
>
> Does shadow model any of the attack conditions that Testground did in the original gossipsubv1.1 parameter additions? For example, the “Covert Flash Attack” might more seriously disrupt a mesh that is being less opportunistic about push. that said, the gossip meta-data (IWANT/IHAVE) might still be sufficient to protect. Nonetheless, I do think that we should model some set of relevant p2p attack vectors when adding a significant change to the gossip protocol – the v1.1 set of attacks as a good basis

We haven’t started simulations yet with a malicious majority yet, but it is definitely something we will cover soon. The worst thing a mesh peer can do is to not respond back to an `INEED` message within the timeout, so this can push up the latency by quite a bit in the event of an attack. There are heuristics that can be used to handle such events(very similar to unfulfilled promises with gossipsub v1.1). Ex: If the mesh peer is non-responsive beyond a threshold it is ignored and pruned from the mesh. It does need to be balanced with not being too harsh on slower peers.

> I do agree that revisiting IWANT/IHAVE, it’s timing, and load should be under consideration. I guess, you probably want IANNOUNCE/INEED to happen in quicker time frames than IWANT/IHAVE heartbeat to ensure that IWANT/IHAVE doesn’t become dominant wrt message broadcast.

Yeap, we just do not want `IWANT/IHAVE` to interfere with mesh announcements. A peer could be already receiving the message from a mesh peer and request it at the same time from a non-mesh peer which would lead to a duplicate.

---

**CPerezz** (2025-03-08):

Hey really interesting work! Specially because is a lot less complex than other proposed alternative solutions.

I had some questions:

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> We do so by introducing two new control messages IANNOUNCE and INEED which carry a single message id within them.

1. The packet utilization % of IANNOUNCE/INEED is (i assume really low). We are spending network resources propogating and replying for almost empty packets.

I was wondering if we can take profit of these and already perform some sort of TLS-Handshake or similar. Such that we can establish a connection with Err Correcting Codes or similar properties. This is [an idea that appears in other protocols such as PQ-DNSSEC](https://eprint.iacr.org/2025/003)

This would be useful if we’re planning to send much bigger data structs cross the network with more reliance.

1. I agree that setting the timeout is a complex task. Specially for the tradeoff of filtering bad-behaved peers from somehow slow peers.

One possible solution I can imagine is to have a series of timeout tiers. And record in our Peer buckets locally the tier at which a peer is at.

This should work as follows:

- We always start with our most restrictive (hence demanding) timeout for every peer.
- For any peer that goes over the timeout:

If we receive the data but later, we adjust the timer to the next tier without a penalization to the peerscore.
- If we don’t ever receive the data, we ask again and adjust the peerscore to the next tier.

If a peer is at the less-demanding timeout, and still misses, then we demote the peerscore accordingly; **This simply means that the peer has bad connection towards us or by itself, or it’s actually misbehaving.**

*It’s still worth to consider improving timeout requirements on situations where peers are at less demanding timeout tiers but we aren’t satisfied on the long run and want to still search for better peers.*

Finally, a question that comes to me is if you’ve thought about rate-limiting IWANT/IHAVE. Since although they are tiny packets, take actual kernel time to process specially if someone floods the network. This might not be severely relevant. But still worth simulating.

To conclude. Nice post and nice idea! Would love to help if there’s anything I can do to move this forward (any tasks left or deign to consider/ideas to run by etc…). It seems super simple and with few considerations to do. And the upside of it is clearly nice.

---

**AgeManning** (2025-03-09):

Nice! The simulations look promising!

We have been thinking about some improvements also, I’ll try write them up in a separate post to avoid cluttering this.

An older version of attempting to improve the eager/lazy ratio of message propagation we attempted was called “episub”. The idea was very similar to this, where we sent IHAVE’s to a subset of our mesh instead of forwarding the messages directly. However the number of peers we did this to was dynamic.

The main complication of episub, was the choice of which peers to lazy send to vs which to eagerly send to. I built a system based on measuring statistics of duplicates and message latency to make the decision. Ultimately, I didn’t push for it too hard because the decision on which peers to do it for was complex. Specifically, there were a few constants around the statistics that users would need to decide, and ultimately I think an automatic version would have been better. I also tested a version of this, where all but 2 mesh peers propagated lazily, and the results showed a worse result than if we just forwarded the message directly, which is the opposite result of what is shown here. (i.e I’d expect the latency to be small when you propagate everything without 2 round trips for each message). The caveat here being it was only for 50 nodes, as it used testground which couldn’t scale at the time. I see in these simulations that we are hitting upload bandwidth thresholds, which we weren’t testing in our simulations. On this point it might be worth running simulations where the upload bandwidth isn’t saturated.

The suggestion in this post is to randomly select peers, removing the complications we faced in episub all together (which is a good idea, I think). I’ve been thinking about this a bit and I want to propose a general/generic version of this, where we abstract both gossipsub scoring (which imo is currently broken) and the mesh choice into “modules” that we can experiment with.

One of the main things lacking in gossipsub today, I think is what I’ve seen referred to as “Peer Selection/Sampling”. Fundamentally, it’s just some algorithm, that decides which peers we eagerly push to (mesh), which we lazily push to (IANNOUCNE in this proposal, or IWANT in episub) and which just get occasional IWANTs (for security from censorship).

In this proposal, the Peer Sampling algorithm would have a static mesh size, randomize peers in that mesh between eager and lazy and all others exist outside.

There could be many forms of this “Peer Selection/Sampling” algorithm. The statistics based approach (which tries to minimize duplicates/latency) would encompass the episub thing we attempted a while ago.

The main point here, is that I think we could have this generic algorithm, provided we don’t introduce new control messages to split between eager/lazy methods.

In episub, we would send IHAVE’s directly instead of forwarding the messages. Is it possible that this proposal can be implemented using the current control messages? Is it vital that we have IANNOUNCE/INEED for this and not just use the IHAVE/IWANT methods. I think doing this would allow us to experiment with a wide range of “Peer Sampling/Selection” algorithms without having to modify the spec each time (also scoring methods).

---

**nisdas** (2025-03-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Funny to see that 0 is strictly worse (under these non-adversarial conditions). This is because duplicates are just wasting local/global bandwidth? Assuming we were hitting peak load locally or globally, you’d expect 0 to be strictly better. Maybe it’s worth running an experiment with all 1Gbps (or even 10Gbps) nodes to show that when bandwidth is not saturated, that push is faster. This would help us validate the hypothesis of why pull is faster for more bandwidth bound networks.

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/c/cc15d8e93f3c9ff63501d2e56d690e31aa86916b_2_333x250.jpeg)image800×600 58.6 KB](https://ethresear.ch/uploads/default/cc15d8e93f3c9ff63501d2e56d690e31aa86916b)

[![image](https://ethresear.ch/uploads/default/optimized/3X/7/a/7a0be131e79a48e338d4157579b19a6d169e9952_2_333x250.jpeg)image800×600 64.2 KB](https://ethresear.ch/uploads/default/7a0be131e79a48e338d4157579b19a6d169e9952)

[![image](https://ethresear.ch/uploads/default/optimized/3X/e/6/e6f87a9edfb21204e9a9ab368d9ac9223131db25_2_333x250.jpeg)image800×600 67.1 KB](https://ethresear.ch/uploads/default/e6f87a9edfb21204e9a9ab368d9ac9223131db25)

[![image](https://ethresear.ch/uploads/default/optimized/3X/0/5/05b084c7a5c4a881917a28fbc4b335914447489e_2_333x250.jpeg)image800×600 62.1 KB](https://ethresear.ch/uploads/default/05b084c7a5c4a881917a28fbc4b335914447489e)

[![image](https://ethresear.ch/uploads/default/optimized/3X/d/a/dacc96e576e4d5bfa6acfb2ae228c6e964573f20_2_333x250.jpeg)image800×600 66.5 KB](https://ethresear.ch/uploads/default/dacc96e576e4d5bfa6acfb2ae228c6e964573f20)

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/6/b65bb1a40a82ce0f6cbeaf49c8e4bb2a11cdf254_2_333x250.jpeg)image800×600 68.4 KB](https://ethresear.ch/uploads/default/b65bb1a40a82ce0f6cbeaf49c8e4bb2a11cdf254)

We re-ran simulations with much lower message sizes. The first 3 charts show the message arrival times with a size of 1kb. As it can be seen here `D_announce=0` has significantly lower latency vs `D_announce=8`. It takes roughly a fourth of the time to reach the whole network compared to `D_announce=8` . It does show in the absence of congestion, only pushing is strictly better.

If you look at the next 3 charts, we ran the simulation with progressively larger message sizes from 1kb to 128 kb with a single message broadcasted each time. For `D_announce=0` , you can see that message arrival times cluster together until 64kb and 128kb, There is a non-trivial jump when sending out messages with 64 kb and finally a much bigger jump at 128kb indicating congestion. For `D_announce=7` and `D_announce=8` , at a message size of 128kb the latency is equivalent to that of `D_announce=0` . Inferring from these results, at a size of 128kb the network is congested.

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> I was wondering if we can take profit of these and already perform some sort of TLS-Handshake or similar. Such that we can establish a connection with Err Correcting Codes or similar properties. This is an idea that appears in other protocols such as PQ-DNSSEC

For gossipsub, we have long-lived streams with all the peers we are connected to. So there is no need to perform any handshake when sending `IANNOUNCE/INEED` messages.

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> This should work as follows:
>
>
> We always start with our most restrictive (hence demanding) timeout for every peer.
> For any peer that goes over the timeout:
>
> If we receive the data but later, we adjust the timer to the next tier without a penalization to the peerscore.
> If we don’t ever receive the data, we ask again and adjust the peerscore to the next tier.
>
>
> If a peer is at the less-demanding timeout, and still misses, then we demote the peerscore accordingly; This simply means that the peer has bad connection towards us or by itself, or it’s actually misbehaving.

Yeah, this is one way we could handle timeouts and progressively make it larger. However waiting for larger timeouts isn’t helpful when the first/smaller one already failed.  It would be better to penalize for repeat failures in responding to `INEED` messages in time as the timeout bounds the worst case latency for a single node in receiving a particular message.

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> The main complication of episub, was the choice of which peers to lazy send to vs which to eagerly send to. I built a system based on measuring statistics of duplicates and message latency to make the decision. Ultimately, I didn’t push for it too hard because the decision on which peers to do it for was complex. Specifically, there were a few constants around the statistics that users would need to decide, and ultimately I think an automatic version would have been better. I also tested a version of this, where all but 2 mesh peers propagated lazily, and the results showed a worse result than if we just forwarded the message directly, which is the opposite result of what is shown here. (i.e I’d expect the latency to be small when you propagate everything without 2 round trips for each message). The caveat here being it was only for 50 nodes, as it used testground which couldn’t scale at the time. I see in these simulations that we are hitting upload bandwidth thresholds, which we weren’t testing in our simulations. On this point it might be worth running simulations where the upload bandwidth isn’t saturated.

Yeah, we wanted to primarily keep the peer selection logic simple rather than do bandwidth estimation of peers, etc. So each message you just randomly choose `D_announce` peers to send the announcements to. On the episub simulations having different outcomes, the charts I linked above should explain why. In the absence of any network congestion, you would always have lower latency with an announcement degree of 0. However our main goal was to optimize for larger messages and when the network is congested which is the case now in Ethereum mainnet. There should still some benefit to have a low announcement degree for smaller messages if it is tolerable to have slightly higher latency with a smaller amount of duplicates. We can try with `D_announce = 1 , 2` and see how the results are for smaller messages.

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> One of the main things lacking in gossipsub today, I think is what I’ve seen referred to as “Peer Selection/Sampling”. Fundamentally, it’s just some algorithm, that decides which peers we eagerly push to (mesh), which we lazily push to (IANNOUCNE in this proposal, or IWANT in episub) and which just get occasional IWANTs (for security from censorship).
>
>
> In this proposal, the Peer Sampling algorithm would have a static mesh size, randomize peers in that mesh between eager and lazy and all others exist outside.
>
>
> There could be many forms of this “Peer Selection/Sampling” algorithm. The statistics based approach (which tries to minimize duplicates/latency) would encompass the episub thing we attempted a while ago.

Yeah, this would be very helpful for the testing of current and future designs if we can agree on how we want peer selection to be abstracted. For now to keep it straightforward we just have the mesh, since involving non-mesh peers might interfere with IHAVE/IWANT.

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> In episub, we would send IHAVE’s directly instead of forwarding the messages. Is it possible that this proposal can be implemented using the current control messages? Is it vital that we have IANNOUNCE/INEED for this and not just use the IHAVE/IWANT methods. I think doing this would allow us to experiment with a wide range of “Peer Sampling/Selection” algorithms without having to modify the spec each time (also scoring methods).

The main reason we had it as a separate control message is to delineate the difference of purpose between the two. The former is for non-mesh peers who will send back any requested IWANTs periodically but not on the critical or fast path. For announcements, these need to be responded back to immediately and within the defined timeout. You could have it as IHAVE/IWANT messgaes but then gossip routers will need to modify how how their current IHAVE/IWANT pipelines to handle this new usecase.

---

**AgeManning** (2025-03-10):

Thanks for the response!

![](https://ethresear.ch/user_avatar/ethresear.ch/nisdas/48/250_2.png) nisdas:

> However our main goal was to optimize for larger messages and when the network is congested which is the case now in Ethereum mainnet.

Is this known? We tried to measure bandwidth saturation on a number of peers for implementing staggered sending, and although the network is rather “bursty” the nodes we were looking at never really saturated their bandwidth, at least in block propagation. These were real nodes with 50/mb connections.

I’d just want to be cautious of implementing a solution that improves on a bandwidth saturated scenario but regresses on a non-bandwidth saturated scenario.

![](https://ethresear.ch/user_avatar/ethresear.ch/nisdas/48/250_2.png) nisdas:

> The main reason we had it as a separate control message is to delineate the difference of purpose between the two. The former is for non-mesh peers who will send back any requested IWANTs periodically but not on the critical or fast path. For announcements, these need to be responded back to immediately and within the defined timeout. You could have it as IHAVE/IWANT messgaes but then gossip routers will need to modify how how their current IHAVE/IWANT pipelines to handle this new usecase.

I didn’t follow this. You said that “non-mesh peers will send back any requested IWANTs periodically but not on the critical or fast path”.

Does this imply that the current implementation upon recieving an IWANT doesn’t send back the message instantly, rather periodically? This isn’t the current specification, which says we should respond instantly ([specs/pubsub/gossipsub/gossipsub-v1.0.md at 6d38f88f7b2d16b0e4489298bcd0737a6d704f7e · libp2p/specs · GitHub](https://github.com/libp2p/specs/blob/6d38f88f7b2d16b0e4489298bcd0737a6d704f7e/pubsub/gossipsub/gossipsub-v1.0.md#message-processing))

For IWANTs, I think currently they should be responded to immediately and they also have a predefined timeout (the promises). I dont think any modification needs to happen with current routers (at least not with rust-libp2p) because we already do this.

---

**nisdas** (2025-03-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> Is this known? We tried to measure bandwidth saturation on a number of peers for implementing staggered sending, and although the network is rather “bursty” the nodes we were looking at never really saturated their bandwidth, at least in block propagation. These were real nodes with 50/mb connections.

For our case we have been looking at not just block propagation but blob propagation too. Since they happen at the same time, they compete with each other. This is what I have for mainnet right now:


      ![](https://ethresear.ch/uploads/default/original/3X/c/9/c956f5798311e726d7366baeea406deada8ec6ef.png)

      [The Lab by ethPandaOps](https://lab.ethpandaops.io/beacon/timings/blocks?network=mainnet&timeWindow=last_30_days)



    ![](https://ethresear.ch/uploads/default/optimized/3X/e/4/e4e9aafe662ef5beec1300fbd334038160914296_2_690x360.png)

###



Platform for exploring Ethereum data and network statistics.










At higher blob counts, there is a noticeable increase in block arrival times.

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> I’d just want to be cautious of implementing a solution that improves on a bandwidth saturated scenario but regresses on a non-bandwidth saturated scenario.

Yeah, so we definitely do not intend for all topics to have the same announcement degrees. It would be a per-topic tunable parameter.

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> Does this imply that the current implementation upon recieving an IWANT doesn’t send back the message instantly, rather periodically? This isn’t the current specification, which says we should respond instantly (specs/pubsub/gossipsub/gossipsub-v1.0.md at 6d38f88f7b2d16b0e4489298bcd0737a6d704f7e · libp2p/specs · GitHub)
>
>
> For IWANTs, I think currently they should be responded to immediately and they also have a predefined timeout (the promises). I dont think any modification needs to happen with current routers (at least not with rust-libp2p) because we already do this.

We will send it back immediately but the IHAVEs that we receive would be processed along IHAVEs from non-mesh peers if we use the same pipelines. At least in `go-libp2p-pubsub` we have a separate priority queue on handling `IDONTWANT` messages since we want these processed as soon as possible.We would need to prioritize IHAVEs from mesh peers into a new pipeline rather than be blocked by non-mesh peers, since its important we respond to them as soon as possible.

---

**chirag-parmar** (2025-03-10):

If I can chime-in, one of the benefits of introducing new control messages is also to conceptually “modularize” the network. IHAVEs/IWANTs would serve their purpose of providing resiliency to the network(outside the mesh) while IANNOUNCEs/INEEDs would serve their purpose of reducing the number of duplicates using lazy pull (inside the mesh). Could we maybe introduce two more for eager push mesh route optimisation using “Peer Selection”?

This would allow the statistics component to be abstracted out which can then also be implementation specific. We can also make these new control messages agnostic of which end is initiating the exchange to allow more degrees of control (maybe SELECT/UNSELECT).

---

**fradamt** (2025-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> I’d just want to be cautious of implementing a solution that improves on a bandwidth saturated scenario but regresses on a non-bandwidth saturated scenario.

Something worth noting here is that in some sense we *want* the network to be saturated (at least during the critical time of block and blob propagation). If not, why not increase the blob count (or block size, assuming other constraints don’t prevent that) until it is?

Besides, I think the issue of congestion is likely going to become a more important question in the future, because PeerDAS creates a bandwidth asymmetry between the smallest and biggest nodes (in terms of validator count). Right now it’s “just” 16x, but could even become as high as 64x if we decrease the column size. At some point, even high bandwidth nodes might be saturated in the critical path, or they could even be the ones to saturate first. And at that point, there’s not going to be extra bandwidth available in the network like there is today if it’s only low bandwidth nodes that saturate their connection.

---

**pop** (2025-04-03):

We did some additional analysis and modelled malicious behaviour where a certain percentage of nodes send IANNOUNCEs but do not reply to INEEDs. In an announce-only network, this would increase the latency of the message and disrupt the normal function of the chain. However, even in the case of D_announce = D we still have IWANT/IHAVE providing resiliency to the network, and the results below support the hypothesis.

> The graphs below plot the latency of a message for a random graph network of 1000 nodes with mesh degree D = 8. The publishing node publishes 16 messages of size 128KB simultaneously for varying degrees of announcement and percentages of malicious nodes in the network.

[![cdf_malicious_0](https://ethresear.ch/uploads/default/optimized/3X/3/4/34d0dc468c38db182ae79007251f4ac8e1690059_2_666x500.png)cdf_malicious_0800×600 59.3 KB](https://ethresear.ch/uploads/default/34d0dc468c38db182ae79007251f4ac8e1690059)

[![cdf_malicious_7](https://ethresear.ch/uploads/default/optimized/3X/4/e/4e5d6cd6ca095d39be547ef00ec53b4bd7e84c1e_2_666x500.png)cdf_malicious_7800×600 65.4 KB](https://ethresear.ch/uploads/default/4e5d6cd6ca095d39be547ef00ec53b4bd7e84c1e)

[![cdf_malicious_8](https://ethresear.ch/uploads/default/optimized/3X/f/d/fde7765e210c5f073a56120379c3aaac20da8a7a_2_666x500.png)cdf_malicious_8800×600 69.9 KB](https://ethresear.ch/uploads/default/fde7765e210c5f073a56120379c3aaac20da8a7a)

Furthermore, we observe that D_announce = D-1 performs better than D_announce = D and this demonstrates the need for mixed strategies in GossipSub v2 for optimal resiliency and performance.

---

**CPerezz** (2025-04-05):

Is this the major expected form of missbehavior/malicious behavior you expect we could see in the network for gossipsubv2?? Or this is just one of them?

---

**pop** (2025-04-08):

I would say it’s the most concerned one for me.

