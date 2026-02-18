---
source: ethresearch
topic_id: 21713
title: Improving DAS performance with GossipSub Batch Publishing
author: cskiraly
date: "2025-02-10"
category: Networking
tags: [data-availability, p2p]
url: https://ethresear.ch/t/improving-das-performance-with-gossipsub-batch-publishing/21713
views: 893
likes: 13
posts_count: 11
---

# Improving DAS performance with GossipSub Batch Publishing

*Author: [@cskiraly](/u/cskiraly)*

*This research was conducted by the [Codex Research Team](https://codex.storage): [@cskiraly](/u/cskiraly), [@leobago](/u/leobago) and [@dryajov](/u/dryajov)*

## TL;DR

- We can achieve significantly lower latencies in DAS by applying chunk/peer scheduling techniques compared to using “standard” GossipSub.
- If the main bandwidth constraint is the publisher’s uplink, individual segments will get diffused in the system shortly after sending out their first copy. Hence, first copies should be prioritized.
- Batch publishing is a way to introduce this prioritization in GossipSub.
- Beyond GossipSub, similar chunk/peer scheduling techniques are beneficial in other protocols designed for DAS as well.

## Intro

There are cases where an application should send out multiple messages over GossipSub simultaneously. A typical example of this is the use of GossipSub in [PeerDAS](https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541) and [FullDAS](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529), where a larger block of data is erasure coded and **split up into multiple segments** (columns, rows, or cells), and each of these is published on different “column topics” (or row/column topics) as individual messages.

While these messages could be sent out sequentially, publishing them one-by-one as it is done in implementations today, the notion of these belonging to the same “**batch**” allows for more advanced **scheduling**, resulting in substantial performance gains.

While we have mentioned and used such scheduling in our [simulators](https://github.com/codex-storage/das-research) and [presentations](https://app.devcon.org/schedule/EVSLDH) in the past, we’ve not yet provided a dedicated writeup. So here it comes.

## The Problem

The problem with typical GossipSub implementations is that an **ordering of messages** is enforced by the publish API. When a message is published, it is **immediately sent** (queued for sending) to all selected neighbours on the relative topic. In case of **limited available uplink bandwidth** the end result is that the “first” message will propagate fast, while the “last” messages will face long queuing times and thus start diffusion very late, **breaking the “diffusion balance”** between messages with otherwise equivalent priority.

Intuitively, it is clear that the entirety of the data cannot be diffused in the system before at least one copy of each segment is sent out by the publisher (for the sake of simplicity we disregard the effect of erasure coding and on-the-fly repair for now). If some parts are sent out multiple times over a limited capacity link, the diffusion of other parts will be unavoidably delayed. Hence, we need **better control over the ordering of message sending**.

## Proposed Solution: Batch Publishing

We can use chunk and peer **scheduling** techniques **to balance the diffusion of segments**. Our technique is not new, it is clearly inspired by literature and best practices on efficient p2p distribution (see e.g. rarest first chunk scheduling policies in Bittorrent, or [some other literature related to chunk/peer scheduling](https://scholar.google.it/citations?view_op=view_citation&citation_for_view=74GVAjAAAAAJ:Se3iqnhoufwC)).

We have used such scheduling techniques since the beginning of our DAS simulations. In fact, scheduling is important independent of whether GossipSub or some other custom pub-sub protocol is used, but here we focus on the GossipSub aspect.

While chunk and peer scheduling can be quite complex, here we describe a simple strategy that improves performance considerably. The main intent is to make sure a first copy of each message in the batch is sent out to the network before second, third, etc. copies are sent out. In other words, we **interleave the publishing of messages**. This allows p2p redistribution to happen as fast as possible, distributing load over the network in a timely manner.

We propose the introduction of the notion of “**batch publishing**” to describe and handle such a scenario. The role of batch publishing is to explicitly inform the underlying protocol stack that a group of messages belongs together, allowing the stack to optimize publishing priorities according to this information. Various implementations are possible at the API level (passing all messages in one call, passing a special iterator, etc.), and various scheduling techniques can be implemented underneath.

Once batch publishing is available at the API level, the implementation of a scheduling policy is relatively simple. A prototype implementation of a simple interleaved strategy is available in nim-libp2p, which we use for results presented below.

## Simulations

We use the [Nim version of our DAS Simulator](https://github.com/cskiraly/das-simulator-nim), with a modified nim-libp2p GossipSub stack [implementing batch publish](https://github.com/cskiraly/nim-libp2p/tree/batch-publish). The simulator is based on the Shadow Network Simulator framework.

Our scenario for the performance comparison is a homogeneous PeerDAS-like (although largely simplified) scenario:

- blobs: 128KB erasure coded to 256KB
- blob count: 8
- columns count: 128
- custody: 16
- Number of nodes: 1000 (ideally we should use 10000, but we need a bigger simulation server for that and 1000 is still indicative of performance gains)
- network latency between nodes: 50ms
- GossipSub degree: 8
- Uplink and downlink bandwidth limit: between 10 Mbps and 100 Mbps

[![average time to custody with/without Batch Publishing](https://ethresear.ch/uploads/default/original/3X/a/0/a07f751963ddd98a7ea665e2299e7f3ce85b912a.png)average time to custody with/without Batch Publishing640×480 22.7 KB](https://ethresear.ch/uploads/default/a07f751963ddd98a7ea665e2299e7f3ce85b912a)

The above summary figure shows average **time to custody** as a function of the available (symmetric) network bandwidth, with traditional (sequential) and with batch publishing. We take the time to custody (when all 16 columns have arrived) of every one of the 999 nodes, and average these values.

As expected, there is a tremendous advantage to batch publishing when available bandwidth is low, and there is notable advantage even at higher bandwidth.

To understand better what happens in the network, we also show detailed figures for both the traditional and batch publishing cases. Because of the level of detail, we should focus on a specific bandwidth: we **select the 20 Mpbs scenario**. These are dense figures with many overlapping curves, and we need some explanation:

- per message propagation: shows a curve for each individual message (we have 128 of these), with each curve showing the percentage of diffusion in the network of the message as a function of time. The percentage of diffusion is measured among those nodes that subscribed to the specific column.
- per peer custody progress: shows a curve for each peer (999 curves), with each curve showing the percentage of custody columns arrived. 100% means all 16 columns have arrived.

[![sequential, per message propagation](https://ethresear.ch/uploads/default/original/3X/e/d/ed13b0e0cf055eb9778296c8fd8cb7b41fca2842.png)sequential, per message propagation484×500 52.6 KB](https://ethresear.ch/uploads/default/ed13b0e0cf055eb9778296c8fd8cb7b41fca2842)

[![batched, per message propagation](https://ethresear.ch/uploads/default/original/3X/5/e/5e87974ecb62d4c87191ee49a7a294fbfc2e21ac.png)batched, per message propagation484×500 87.8 KB](https://ethresear.ch/uploads/default/5e87974ecb62d4c87191ee49a7a294fbfc2e21ac)

[![sequential; per peer custody progress](https://ethresear.ch/uploads/default/original/3X/d/8/d8104783b88c6bdd9aa985976d4dc9ab69456298.png)sequential; per peer custody progress484×500 35.7 KB](https://ethresear.ch/uploads/default/d8104783b88c6bdd9aa985976d4dc9ab69456298)

[![batched; per peer custody progress](https://ethresear.ch/uploads/default/original/3X/9/0/90f38fe24c84f805f97472454bf4a40da0859fc8.png)batched; per peer custody progress484×500 30 KB](https://ethresear.ch/uploads/default/90f38fe24c84f805f97472454bf4a40da0859fc8)

Note that the x-axis has a **different scale** for the sequential and for the batch case.

As **first copies** of messages leave the publisher, **curves start** at the bottom of the per message plot. Clearly, this happens much earlier with batching. Once the first copy is out, the network has plenty of bandwidth and p2p multiplicative effect to diffuse individual messages, leading to 100% diffusion for the given message in a short time.

The per peer plot instead shows us how **custody progress is uniform among peers in the batched case**. At any quantile (horizontal cut on the figure) the time difference between the best and worst peer is not more than 400ms. Only at the last diffusion step (from 15 columns in custody to all 16 columns in custody) the plot widens. Note that we have already introduced techniques to “cut” this tail of the distribution in our [LossyDAS post](https://ethresear.ch/t/lossydas-lossy-incremental-and-diagonal-sampling-for-data-availability/18963), and similar techniques could be used here as well.

If instead we look at the case of the sequential strategy, we see that the difference between the custody progress of individual peers is much bigger: several seconds.

Further experiments will be conducted with different parameters and with heterogeneous scenarios, but we expect baching to provide significant benefits also in other cases.

## Sounds Great, but How Many Blobs?

The previous simulation was run with 8 blobs. In the figure below we vary the number of blobs from 3 to 64, and plot the average time to custody as a function of available network bandwidth. This is still a homogeneous network scenario, but indicative of what to expect (also note that this is plotted from single runs at the moment, so curves are not smooth).

[![image](https://ethresear.ch/uploads/default/optimized/3X/7/0/70cbc866cae44655f979b7e6cdb0908be369cd24_2_690x320.png)image1076×500 65.2 KB](https://ethresear.ch/uploads/default/70cbc866cae44655f979b7e6cdb0908be369cd24)

The results seem promising, showing that Batch Publishing could really help in increasing the blob count in PeerDAS.

Further experiments will be conducted with different parameters and with heterogeneous scenarios, but we expect batching to provide significant benefits also in other cases.

## Discussion

Batch publishing is only one of the techniques we prepare to improve the performance of DAS. We have mentioned several other possibilities in our [FullDAS writeup](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529#the-dispersal-protocol-18) and [presentations](https://app.devcon.org/schedule/EVSLDH), and plan to provide details on more in the future.

Similar effects to batch publishing can be achieved by so called “staggered sending” which was studied by Tanguy and [@Nashatyrev](/u/nashatyrev) in the past. We think the notion of batching provides a better semantics and allows better scheduling than staggered send.

When considering possible scheduling strategies, there are many ways to complicate ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) the above described simple interleaving:

- Message order randomisation: the order of messages in the batch could be randomly shuffled between iterations. This has the advantage of removing even more bias from the distribution.
- Per-message peer order randomisation: Regarding the first, second, etc. copies of a single message, we can randomise the order of mesh peers. This is to make sure load is distributed evenly among peers. Of course randomisation is not the only possible strategy, just the simplest one. Different peers can be mesh neighbours in multiple topics. Counter-based strategies can provide more even distribution; weighted random strategies can be used if there is more information (peer score, latency, bandwidth estimate, etc.) about peers.
- Feedback based adjustment: in cases of low uplink bandwidth, it can easily happen that by the time the batch publisher starts to send out second copies, most messages are already diffused in the network. Feedback about the diffusion state of individual messages (e.g. through IHAVE messages) might also start to come in. Such feedback can be used to prioritise the seeding of 2nd, 3rd, etc. copies of one message over another. We note that such feedback cannot be trusted, so care should be taken when adapting the sending schedule. As an alternative, a hidden trusted “buddy” node could also be used to observe the diffusion state.

As mentioned before, batching and chunk/peer scheduling can be used not just with GossipSub, but also with other pub-sub protocols where multiple copies are sent out. This is true for UDP-based protocols, and even if we use erasure coding. A notable exception to this is the use of fountain codes or random linear network coding, where there are no replicas. In that case peer scheduling might still be important, but chunk scheduling is not directly applicable.

The goal of Batch Publishing is to **reduce the impact of  a bandwidth bottleneck at the publisher**, allowing for **better home staking**. It significantly improves latency even if available bandwidth is higher. Other techniqes under development such as [Distributed Blob Building](https://blog.sigmaprime.io/peerdas-distributed-blob-building.html) are complimentary to our technique.

## References

[1] Original PeerDAS post



    ![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png)

      [PeerDAS -- a simpler DAS approach using battle-tested p2p components](https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541) [Networking](/c/networking/27)




> PeerDAS
> This is an sketch representing the general direction of PeerDAS. This is being circulated at an early stage for feedback before further discussion refinement.
> This set of ideas came out of conversations with Dankrad, Vitalik, members of Codex, RIG, ARG, and Consensus R&D. Directionally, pieces of this type of approach have also been under discussion in various avenues for the past couple of years, e.g. Proto’s PeerDHT
> The intent of a PeerDAS design is to reuse well known, battle-teste…

[2] Our FullDAS post



    ![](https://ethresear.ch/user_avatar/ethresear.ch/cskiraly/48/13102_2.png)

      [FullDAS: towards massive scalability with 32MB blocks and beyond](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529) [Sharding](/c/sharding/6)




> Author: Csaba Kiraly, in collaboration with Leonardo Bautista-Gomez and Dmitriy Ryajov, from the Codex.storage research team.
> Note: this document describes the current state of our thinking, result of a collaborative effort and numerous discussions with other teams. It would not had been possible without the contribution and ideas of @dankrad , @djrtwo , @fradamt , @AgeManning , @Nashatyrev , @matt , @pop , and @Echo .
> TL;DR
>
> Danksharding was planned for 32MB blocks, but our current networking…

[3] DEVCON SEA Talk on Scalability

https://app.devcon.org/schedule/EVSLDH

[4] libp2p Day 2024 Bangkok Talk

  [![image](https://ethresear.ch/uploads/default/original/3X/c/2/c2785ba1fc4d29dfedfdc57ee2b84c4981c117ca.jpeg)](https://www.youtube.com/watch?v=sI_Qr1vHUk4)

[5] Batch Publishing prototype implementation


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/cskiraly/nim-libp2p/tree/batch-publish)





###



[batch-publish](https://github.com/cskiraly/nim-libp2p/tree/batch-publish)



libp2p implementation in Nim. Contribute to cskiraly/nim-libp2p development by creating an account on GitHub.

## Replies

**Nashatyrev** (2025-02-11):

Great writeup! This totally makes sense to me and the gain numbers are really impressive!

Just one question: so the staggered sending was not involved here? You were just submitting all the batch chunks (columns) to all the peers at once (but shuffled instead of ordered) and then just rely on OS network stack to schedule them?

---

**Nashatyrev** (2025-02-11):

Submitted a feature request for Teku: [[GossipSub] Implement Batch publishing · Issue #9096 · Consensys/teku · GitHub](https://github.com/Consensys/teku/issues/9096)

---

**cskiraly** (2025-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/nashatyrev/48/6487_2.png) Nashatyrev:

> Great writeup! This totally makes sense to me and the gain numbers are really impressive!
>
>
> Just one question: so the staggered sending was not involved here? You were just submitting all the batch chunks (columns) to all the peers at once (but shuffled instead of ordered) and then just rely on OS network stack to schedule them?

No staggered sending here. Just comparision between the baseline behaviour and batch publishing. I think the staggered implementation is on another branch in the repo, but with some effort we can make a comparison.

One thing to note is that here I’m really just modifying the publish behavior. Scheduling can also be applied in forwarding, but on forwarding I’m preparing a separate writeup.

Scheduling is partly done by the OS stack, but part of the buffers are still at the libp2p level.

---

**Nashatyrev** (2025-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/cskiraly/48/13102_2.png) cskiraly:

> One thing to note is that here I’m really just modifying the publish behavior.

I see. Is the `floodPublish` option was turned off for your experiments?

> Scheduling can also be applied in forwarding, but on forwarding I’m preparing a separate writeup.

Oh interesting! Staying tuned!

---

**cskiraly** (2025-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/nashatyrev/48/6487_2.png) Nashatyrev:

> I see. Is the floodPublish option was turned off for your experiments?

Yes, that was off. I’m making the publisher node subscribe to each topic. Anyway, with floodPublish it would be the same, just pushing to a different subset of nodes … but I did not yet implement that part ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I have to organize the code a little bit into meaningful patches, then I will release that as well.

One thing I am checking is whether the numbers are different during a longer experiment, because TCP slow-start might influence my numbers.

---

**pop** (2025-03-05):

Do you have a plan to merge your branch into the nim-libp2p upstream repo?

Since this only involves the publisher, when nimbus becomes the publisher we can learn the real metrics from the mainnet directly instead of learning them from the simulations.

Or maybe you don’t need to merge it. You can just have some validators run the patched code and learn the real metrics when they become proposers.

---

**cskiraly** (2025-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> Do you have a plan to merge your branch into the nim-libp2p upstream repo?

Eventually yes, but in its current state it is a functional PoC implementation with a few TODOs left in. In the meantime, I post a better link to the code that only shows the relevant patches (last two):


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [GitHub](https://github.com/cskiraly/nim-libp2p/compare/5072423709a6569035912a5746c3d6ab9570bee0...cskiraly:nim-libp2p:batch-publish)



    ![](https://ethresear.ch/uploads/default/optimized/3X/4/1/41eff9ee98cf22e68a5c2877f008259a22dc3666_2_690x345.png)

###



libp2p implementation in Nim. Contribute to cskiraly/nim-libp2p development by creating an account on GitHub.










![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> Since this only involves the publisher, when nimbus becomes the publisher we can learn the real metrics from the mainnet directly instead of learning them from the simulations.
>
>
> Or maybe you don’t need to merge it. You can just have some validators run the patched code and learn the real metrics when they become proposers.

Learning from mainnet is difficult, because data collection is limited and it depends on the actual bandwidth limits of the specific node and many other factors. That’s the exact reason we are validating these in simulation, using a simulator that uses the real libp2p code and gives us relatively high levels of realism, while we can explore the parameter space and collect fine-grained data on the diffusion process.

Having said that, I’m convinced we will see the positive effect on mainnet once it gets deployed.

---

**pawanjay176** (2025-03-07):

Great writeup. We’ll be implementing this in rust-libp2p soon and try to test it out.

> Scheduling can also be applied in forwarding

I’m curious how you are thinking about this. On the consensus layer, if the message passes gossip validation, we accept it at the application which immediately triggers a forward on libp2p. Batch forwarding here would imply that we wait around to get a few messages before doing the actual forwarding which would slow down propagation.

---

**potuz** (2025-03-07):

Nice write-up! Just wanted to call to attention that this is compatible with our RLNC proposal and we have indeed implemented batch broadcasting in our RLNC branch in Prysm.

---

**cskiraly** (2025-04-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/pawanjay176/48/2699_2.png) pawanjay176:

> Great writeup. We’ll be implementing this in rust-libp2p soon and try to test it out.
>
>
>
> Scheduling can also be applied in forwarding

I’m curious how you are thinking about this. On the consensus layer, if the message passes gossip validation, we accept it at the application which immediately triggers a forward on libp2p. Batch forwarding here would imply that we wait around to get a few messages before doing the actual forwarding which would slow down propagation.

The main thing to notice is that you should **know about the “batch” in the forwarding node** for this. **In DAS** this is relatively **simple** if we do the correct message IDs, i.e. **IDs based on the block hash and X,Y positions**.

Once you know the messages belong to the same batch, you can schedule between them. Such scheduling is important when your uplink bandwidth is limited, so you can’t just push out messages, you really just queue them for sending. In that case, ordering this queue (these queues for various peers) wisely can make a difference.

