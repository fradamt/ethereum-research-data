---
source: ethresearch
topic_id: 22652
title: Impact of IDONTWANT in the number of duplicates
author: cortze
date: "2025-06-20"
category: Networking
tags: []
url: https://ethresear.ch/t/impact-of-idontwant-in-the-number-of-duplicates/22652
views: 170
likes: 4
posts_count: 1
---

# Impact of IDONTWANT in the number of duplicates

# Introduction

This work is a follow-up study of the original one we carried out on the number of duplicate messages, before the `IDONTWANT` message primitive was adopted:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/yiannisbot/48/14069_2.png)

      [Number Duplicate Messages in Ethereum's Gossipsub Network](https://ethresear.ch/t/number-duplicate-messages-in-ethereums-gossipsub-network/19921/1) [Networking](/c/networking/27)




> Summary & TL;DR
> The ProbeLab team (probelab.io) is carrying out a study on the performance of Gossipsub in Ethereum’s P2P network. Following from our previous post on the “Gossipsub Network Dynamicity through GRAFTs and PRUNEs” in this post we investigate the number of messages and duplicated messages seen by our node, per topic. There is no public data on the overhead that broadcasting messages and control data over the network imply on each participating node.
> For the purposes of this study, …

# Methodology

The data used to generate the following study was collected using our GossipSup listener hermes located in Sydney, Australia on `27/05/2025`.

> NOTE: We’ve also analysed the numbers from a second hermes node, located in California, US, to verify that numbers don’t differ much, which was indeed the case.

# Adoption of IDONTWANTs

`IDONTWANT` messages have been part of the libp2p gossipsub  [spec](https://github.com/libp2p/specs/blob/e4e6eb75348d116958fc00fb68de48a4d44225be/pubsub/gossipsub/gossipsub-v1.2.md) for a while, but not all implementations supported them. In that sense, the Pectra upgrade wasn’t just a synchronous update to the Ethereum protocol—it also brought a significant increase in peers supporting the new control messages.

As of May 27th, from our weekly reports, we can observe that the majority of the network supports `IDONTWANT` (part of the `meshsub/1.2.0` release). Only about 5% (roughly 400 nodes) are missing from the total [discovered nodes](https://pages.probelab.io/ethereum/discv5/2025-22/#agent-distribution).

[![image](https://ethresear.ch/uploads/default/optimized/3X/8/7/878a12fab6221367f98d8ba3357105b3407ec8ff_2_597x500.png)image714×597 70.5 KB](https://ethresear.ch/uploads/default/878a12fab6221367f98d8ba3357105b3407ec8ff)

# Current level of duplicates

From our [previous report](https://www.notion.so/Reporting-GossipSub-message-arrivals-and-duplicates-78b477c7a279422ab518a0178ea6d67a?pvs=21) when referring to the `beacon_blocks` topic, we found the following:

> there are almost no recorded messages without duplicates (1%-2%).
> 54% of the messages report the expected 3  duplicates from the mesh
> Taking a look at the tail of the CDF (shown in the dropdown plot further down), there are a few messages that were received up to 34 or 40 times.

Compared to these previous results, our current findings show that there’s a **small but clear reduction of duplicates** in topics with “large enough” messages (exceeding the [1Kb msg size](https://github.com/libp2p/go-libp2p-pubsub/blob/3f89e4331c981a6b60206b762a10d015c04875a8/gossipsub.go#L75)), i.e., the `beacon_block` and `beacon_blobs` topics:

- There is an increase in the number of blocks with no duplicates from 2% (previously) to 9% after the addition of IDONTWANT.
- In the following graphs, we see a reduction of the mean, which now stays at 2 duplicates, instead of 3 previously. There are only 5% of the messages exceeding 4 duplicates.
- There’s a clear reduction in the tail of duplicates - we previously measured up to 34 or 40 duplicates in some edge cases, while now, the tail stops at 6-8 copies.

Before the IDONTWANTs:

[![image](https://ethresear.ch/uploads/default/optimized/3X/e/d/ed32bde99b26723d014caa6cd3b1b065fc876638_2_517x309.png)image1000×600 66.9 KB](https://ethresear.ch/uploads/default/ed32bde99b26723d014caa6cd3b1b065fc876638)

After the IDONTWANTs:

[![image](https://ethresear.ch/uploads/default/original/3X/7/b/7b5d9efb66cafbe46affb18117bc2399781aa9b5.png)image582×347 44.9 KB](https://ethresear.ch/uploads/default/7b5d9efb66cafbe46affb18117bc2399781aa9b5)

Overall, what we see is that 98% of the duplicates arrive within the first second after receiving the first message, with 79% arriving within half a second, which extends for another 400ms until the last duplicate arrives.

[![image](https://ethresear.ch/uploads/default/original/3X/3/b/3b7d09abbb99a841e2eed23bc0b5babd0fda47a2.png)image582×360 46 KB](https://ethresear.ch/uploads/default/3b7d09abbb99a841e2eed23bc0b5babd0fda47a2)

# Correlation between message size and number of duplicates

The following graph shows the time differences between the message arrival and the first duplicate per topic. In the figure, we can appreciate a clear difference between the two types of topics. The `beacon_block` generally has smaller messages than the `blob_sidecar` one, or at least the `blob_sidecar` topic is less stable in terms of message size (check the block size distribution further down).

Time to first duplicate:

[![image](https://ethresear.ch/uploads/default/original/3X/e/5/e5b433128610ce865f0a0c04742f9b2647bcde5d.png)image581×355 57.4 KB](https://ethresear.ch/uploads/default/e5b433128610ce865f0a0c04742f9b2647bcde5d)

Certainly, the next graph shows the CDF of the message size, where we see that beacon blocks are generally smaller than the sidecars.

[![image](https://ethresear.ch/uploads/default/original/3X/6/c/6cb825b7442cdf9524ef49b5a810acad913c45ef.png)image580×358 61.5 KB](https://ethresear.ch/uploads/default/6cb825b7442cdf9524ef49b5a810acad913c45ef)

There is, therefore, a small correlation between the size of the message and the number of duplicates. When looking at the following CDF chart, we see that larger messages do tend to get a higher number of copies, as they generally take a larger time to get transmitted over the wire.

[![image](https://ethresear.ch/uploads/default/original/3X/3/7/374c80c293b2ddadb07f8e289f75264fe29efa0c.png)image580×360 41.4 KB](https://ethresear.ch/uploads/default/374c80c293b2ddadb07f8e289f75264fe29efa0c)

> NOTE: the size_range belongs to the range X to X+19 in KB
> Example: size_range 0 includes [0kb, 20kb)

# Number of IDONTWANTs

## Methodology

The data used for this report comes from a single peer located in Australia, which is known to be out of the core of the network, with higher latency and lower bandwidth. However, checking with the results from a node based in the US, we found very similar results.

We aim to check if the `IDONTWANT` messages are actually getting sent, and the timing of sending these messages. These are both relevant points to see if there are any bottlenecks at the implementation level.

## Results Summary

There is a clear reduction of duplicates, yet it is lower than we expected → we assumed that most of the duplicates would come through the mesh propagation ([[D-2](https://ethresear.ch/t/gossipsub-network-diameter-estimate/21561)]([Gossipsub Network Diameter Estimate](https://ethresear.ch/t/gossipsub-network-diameter-estimate/21561)))

However, we didn’t measure any sign of sent `IDONTWANT` messages on topics with messages below the threshold (1KB).

Interestingly, the following graph shows that our control node sent a similar number of `IDONTWANT` messages as the number of duplicates that we receive. Which could be an indicator of `IDONTWANT` not being as effective as we would expect.

One possible explanation is that we send `IDONTWANTs` on time to our mesh peers. However, we still receive the messages that we have just sent `IDONTWANTs` for, which indicates that the message was already on the wire.

[![image](https://ethresear.ch/uploads/default/original/3X/c/3/c35f8c47e81c3afa8eaa46363ff44e6872bb63f7.png)image582×350 44.9 KB](https://ethresear.ch/uploads/default/c35f8c47e81c3afa8eaa46363ff44e6872bb63f7)

## When do duplicates arrive

Given the correlation between the number of sent `IDONTWANT` messages and the received duplicates, it is still unclear whether the `IDONTWANTs` are useful. The node could be sending the control messages with a small, but enough, delay from the arrival of the message. Thus, the following chart shows the time difference between the sending of `IDONTWANT` messages and the arrival of the first message. The figure shows that there is, indeed, no delay between the arrival of the message and the `IDONTWANT` notifications. The graph even shows some cases where control notification was sent before we were able to track the “delivery” of the message.

> NOTE: We do see negative times as we read the message arrival by the Deliver notification, not when we received the message over the RPC.

[![image](https://ethresear.ch/uploads/default/original/3X/b/4/b4b45e4c2497129c6353d4a135767a5b810780e4.png)image580×358 31.2 KB](https://ethresear.ch/uploads/default/b4b45e4c2497129c6353d4a135767a5b810780e4)

## What triggers duplicates after IDONTWANT messages

As mentioned above, interestingly, we still see duplicates that arrive after notifying the remote peer with an `IDONTWANT`.

The following chart shows the time difference between the notification of an `IDONTWANT` message and the received duplicate from the same peer. Where we can see that some implementations or versions don’t stop transmitting messages after receiving an `IDONTWANT` (rust-libp2p has ongoing work to address this issue, see [GH issue](https://github.com/libp2p/rust-libp2p/issues/5751) and [GH PR](https://github.com/sigp/rust-libp2p/pull/570)).

It’s worth noting that there is ongoing work to fix the case when a published RPC is queued and an `IDONTWANT` message arrives ([issue](https://github.com/libp2p/go-libp2p-pubsub/issues/611)). We believe this will help reduce the number of duplicates significantly.

[![image](https://ethresear.ch/uploads/default/original/3X/b/a/bac538cfaea89f6c262fb7e1de5fe31a083906f2.png)image592×359 65.7 KB](https://ethresear.ch/uploads/default/bac538cfaea89f6c262fb7e1de5fe31a083906f2)

To provide some numbers on how frequent this case is, we have:

- 30,607 unique message IDs (blocks and blobs)
- 63,735 duplicated messages
- 144,524 sent IDONTWANTs
- 25,201 sent IWANTs
- 14,255 message IDs where we sent both IWANTs and IDONTWANTs
- out of 63,735 total duplicates, 44,875 are from peers that got notified via IDONTWANT messages (~70% of duplicates)

sequence of events from the same peer that produced duplicates:

(44,875): msg_arrival > sent_idontwant > recv_duplicate

(`18`) `sent_iwant` > `msg_arrival` > `sent_idontwant` > `recv_duplicate`

- very few in relation to the total number of sent control messages
- In the overlap between IDONTWANTs and IWANTs, at least the go implementation doesn’t seem to be notifying remote IWANT-notified peers to stop the diffusion

# Number of IWANTs

When looking at the number of `IWANT` messages sent by the `hermes` instance on the topics, what we see is that quite a few duplicates come as a reply to the `IWANTs` that we sent out.

[![image](https://ethresear.ch/uploads/default/original/3X/d/9/d9e1b765a1d08940af7ac9b613ba5b54bd736380.png)image580×358 42.9 KB](https://ethresear.ch/uploads/default/d9e1b765a1d08940af7ac9b613ba5b54bd736380)

Looking at when these messages were sent, we see that for around 60% of the (25,201) sent `IWANTs` were shared just 4 ms before the arrival of the block. Therefore, producing one duplicate message per sent `IWANT`. Clearly, this means that our node was almost done receiving the message when it sent the `IWANT` message out, which resulted in a duplicate.

[![image](https://ethresear.ch/uploads/default/original/3X/8/d/8d7bbc473ef6b4778e221cb4e17b969df4415a26.png)image580×358 37.4 KB](https://ethresear.ch/uploads/default/8d7bbc473ef6b4778e221cb4e17b969df4415a26)

The following graph shows that the full download of block and sidecar messages through IWANTs takes between 500ms and 1.5 seconds.

[![image](https://ethresear.ch/uploads/default/original/3X/c/9/c91258c1ce0d6f6fd1bd668426fced0760492cb8.png)image575×351 61.9 KB](https://ethresear.ch/uploads/default/c91258c1ce0d6f6fd1bd668426fced0760492cb8)

# Summary

We see all the events summarised in the following chart, which is displayed as a relative time to the arrival of the message at the node we collect results from. That is, `0` is the point in time when our node received the message.

[![image](https://ethresear.ch/uploads/default/original/3X/0/e/0e3ff9e04d336f09922b48db1ed69438b56c512f.png)image592×359 63.8 KB](https://ethresear.ch/uploads/default/0e3ff9e04d336f09922b48db1ed69438b56c512f)

To provide some numbers of the events and their frequency, here is a summary:

- 30,607 unique message IDs (blocks and blobs)
- 63,735 duplicated messages
- 144,524 sent IDONTWANTs
- 25,201 sent IWANTs
- 14,255 message IDs where we sent both IWANTs and IDONTWANTs
- 44,875 duplicates from peers that got notified via IDONTWANT messages (~70% of duplicates) → msg_arrival > sent_idontwant > recv_duplicate
- 18,540 duplicates from peers that requested the message through an IWANT (~29% of duplicates) → sent_iwant > msg_arrival  > recv_duplicate (no sent IDONTWANT to cancel the IWANT)

(18) sent_iwant > msg_arrival > sent_idontwant

very few cases when we tried to cancel the sent IWANT with an IDONTWANT → expected result at the go implementation, but defined by the spec.
- 12 of those 18 cases, we received a duplicate

# Our recommendations

- Overall, IDONTWANTs improve the situation significantly, but become ineffective when:

The msg_id was already requested through an IWANT, in which case we don’t send an IDONTWANT message
- The message is already in the pipe, and it doesn’t get cancelled

That said, there is still room for improvement in handling the control messages:

- Limit the number of IWANT messages sent as discussed at this issue and in Devcon SEA. As discussed earlier, we’ve seen that the node sends many redundant IWANT messages for a single message ID
- Delay the first IWANT message to avoid 60% of the distribution that was requested 10ms before the first message arrival, which we know would produce redundant copies.

Cancel the reply of IWANT upon receipt of IDONTWANT, even if the message is already in transmission/on the wire.

This doesn’t seem to be the case for all the implementations (certainly not for Go).
- There is already a check for the messages we are about to publish (link). But many duplicates arrived after the sequence: msg_arrival -> sent_idontwant -> recv_duplicate
