---
source: ethresearch
topic_id: 19686
title: Gossip IWANT/IHAVE Effectiveness in Ethereum's Gossipsusb network
author: yiannisbot
date: "2024-05-30"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/gossip-iwant-ihave-effectiveness-in-ethereums-gossipsusb-network/19686
views: 4150
likes: 8
posts_count: 8
---

# Gossip IWANT/IHAVE Effectiveness in Ethereum's Gossipsusb network

# Summary & TL;DR

The ProbeLab team (https://probelab.io) is carrying out a study on the performance of Gossipsub in Ethereum’s P2P network. This post is reporting the first of a list of metrics that the team will be diving into, namely, how efficient is Gossipsub’s gossip mechanism. For the purposes of this study, we have built a tool called Hermes ([GitHub - probe-lab/hermes: A Gossipsub listener and tracer.](https://github.com/probe-lab/hermes/)), which acts as a GossipSub listener and tracer. Hermes subscribes to all relevant pubsub topics and traces all protocol interactions. The results reported here are from a 3.5hr trace.

**Study Description:** The purpose of this study is to identify the ratio between the number of `IHAVE` messages sent and the number of `IWANT` messages received from our node. This should be done both in terms of overall messages, but also in terms of `msgIDs`. This metric will give us an overview of the effectiveness of Gossipsub’s gossip mechanism, i.e., how useful the bandwidth consumed by gossip messages really is.

**TL;DR:** **The effectiveness of Gossipsub’s gossip mechanism, i.e., the `IHAVE` and `IWANT` message exchange is not efficient in the Ethereum network.** Message ratios between Sent `IHAVEs` and Received `IWANTs` can reach to more than 1:50 for some topics. Suggested optimisations and things to investigate to improve effectiveness are given at the end of this report.

## Overall Results - Sent IHAVEs vs Received IWANT

The plots below do not differentiate between different topics. They present aggregates over all topics. The ratio of sent `IHAVEs` vs received `IWANTs` does not seem extreme (top plot) with a ratio of less than 1:2, but digging deeper into the number of `msgIDs` carried by those `IHAVE` and `IWANT` messages shows a different picture (middle plot). The ratio itself for all three topics are given in the third (bottom plot), where we see that especially for the beacon_block topic the ratio is close to 1:100 and going a lot higher at times.

[![gossip_control_msgs_sent_ihave_vs_recv_iwant_messages](https://ethresear.ch/uploads/default/optimized/3X/2/7/27e3878da92a987de30755da843003d2390d2852_2_517x309.png)gossip_control_msgs_sent_ihave_vs_recv_iwant_messages1000×600 68 KB](https://ethresear.ch/uploads/default/27e3878da92a987de30755da843003d2390d2852)

[![gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids](https://ethresear.ch/uploads/default/optimized/3X/1/6/169e349eb5bf6f5eae425791f895e9ae32a5a41d_2_517x309.png)gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids1000×600 75.5 KB](https://ethresear.ch/uploads/default/169e349eb5bf6f5eae425791f895e9ae32a5a41d)

[![gossip_control_msgs_ration_of_sent_ihave_vs_recv_iwant_message_ids_all_topics](https://ethresear.ch/uploads/default/optimized/3X/a/3/a37bfd19efcd740d899634ae0d27a92413c2cb2e_2_517x309.png)gossip_control_msgs_ration_of_sent_ihave_vs_recv_iwant_message_ids_all_topics1000×600 76.8 KB](https://ethresear.ch/uploads/default/a37bfd19efcd740d899634ae0d27a92413c2cb2e)

## Per Topic Results - Sent IHAVEs vs Received IWANT

Next, we’re diving into the ratio *per topic* to get a better understanding of the gossip effectiveness for each topic. We’re presenting the overall number as well as the ratio per topic. The ratio of sent `IHAVEs` vs received `IWANTs` is more extreme and reaches an average of close to 1:100 for the `beacon_block` topic, 1:10 for the `beacon_aggregate_and_proof` topic and 1:6 for the `sync_committee_contribution_and_proof` topic.

[![gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids_69ae0e99_beacon_block](https://ethresear.ch/uploads/default/optimized/3X/0/b/0b1d31747dac95b38c72afe9858fb9211ded447c_2_517x309.png)gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids_69ae0e99_beacon_block1000×600 73.5 KB](https://ethresear.ch/uploads/default/0b1d31747dac95b38c72afe9858fb9211ded447c)

[![gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids_69ae0e99_beacon_aggregate_and_proof](https://ethresear.ch/uploads/default/optimized/3X/d/5/d5ac836932182c36c9ef2f0097bc2c27a8b39beb_2_517x309.png)gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids_69ae0e99_beacon_aggregate_and_proof1000×600 56.4 KB](https://ethresear.ch/uploads/default/d5ac836932182c36c9ef2f0097bc2c27a8b39beb)

[![gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids_69ae0e99_sync_committee_contribution_and_proof](https://ethresear.ch/uploads/default/optimized/3X/a/a/aa5d777e133a0cf20446b3e978d7060fbc4a8086_2_517x309.png)gossip_control_msgs_sent_ihave_vs_recv_iwant_message_ids_69ae0e99_sync_committee_contribution_and_proof1000×600 71.1 KB](https://ethresear.ch/uploads/default/aa5d777e133a0cf20446b3e978d7060fbc4a8086)

It is clear that there is an excess of `IHAVE` messages sent compared to the usefulness that these provide in terms of received `IWANT` messages. There’s at least a 10x bandwidth consumption that we could optimise for if we reduced the ratios especially for the `beacon_block` and `beacon_aggregate_and_proof` topics.

The `beacon_aggregate_and_proofs` topic sends hundreds of thousands of `message_ids` over the wire in a minute, with very few `IWANT` messages in return. The ratio of sent `IHAVE` `msgIDs` to the received `IWANT msgIDs` stays around 10 times bigger.

## Overall Results - Received IHAVE vs Sent IWANT

The situation is even more extreme for the case of Received `IHAVE` vs Sent `IWANT` messages in terms of overhead. We include below the overall results only, as well as the ratios per topic. We consider that the ratios are even higher here because our node is rather well-connected (keeps connections to 250 peers) and therefore is more likely to be included in the `GossipFactor` fraction of peers that are chosen to send gossip to (i.e., `IHAVEs`). This in turn means that we must be receiving lots of duplicate `msgIDs` in those `IHAVE` messages. Digging into the number of duplicate messages are subject to a different metric further down in this report.

[![gossip_control_msgs_recv_ihave_vs_sent_iwant_messages](https://ethresear.ch/uploads/default/optimized/3X/e/8/e8bfe2c7e1e5061cc1e6189027c61cb561e5ebff_2_517x309.png)gossip_control_msgs_recv_ihave_vs_sent_iwant_messages1000×600 59.3 KB](https://ethresear.ch/uploads/default/e8bfe2c7e1e5061cc1e6189027c61cb561e5ebff)

[![gossip_control_msgs_recv_ihave_vs_sent_iwant_message_ids](https://ethresear.ch/uploads/default/optimized/3X/d/7/d7221f99eab26664812e8a7b8a5af32da2457f1a_2_517x309.png)gossip_control_msgs_recv_ihave_vs_sent_iwant_message_ids1000×600 76 KB](https://ethresear.ch/uploads/default/d7221f99eab26664812e8a7b8a5af32da2457f1a)

[![gossip_control_msgs_ration_of_recv_ihave_vs_sent_iwant_message_ids_all_topics](https://ethresear.ch/uploads/default/optimized/3X/9/3/93bb45e0850316dea9fa50186848459a21d1d3bd_2_517x309.png)gossip_control_msgs_ration_of_recv_ihave_vs_sent_iwant_message_ids_all_topics1000×600 112 KB](https://ethresear.ch/uploads/default/93bb45e0850316dea9fa50186848459a21d1d3bd)

## Anomalies

Gossipsub messages should always be assigned to a particular topic, as not all peers are subscribed to all topics. Having a topic helps with correctly identifying invalid messages and avoiding overloading of peers with messages they’re not interested in.

We have consistently seen throughout the duration of the experiment both `IHAVE` and `IWANT` messages sent to our node with an empty topic. Both of these are considered anomalies, especially given that the `IWANT` messages we received were for `msgIDs` that we didn’t advertise through an `IHAVE` message earlier.

Digging deeper into the results, we have seen that 49 out of the 55 peers that we received messages with an empty topic were Teku nodes. We have started the following Github issue to surface the anomaly: [Possible Bug on GossipSub implementation that makes sharing `IHAVE` control messages with empty topics · Issue #361 · libp2p/jvm-libp2p · GitHub](https://github.com/libp2p/jvm-libp2p/issues/361), which has been fixed: [Set topicID on outbound IHAVE and ignore inbound IHAVE for unknown topic by StefanBratanov · Pull Request #365 · libp2p/jvm-libp2p · GitHub](https://github.com/libp2p/jvm-libp2p/pull/365).

## Takeaways

- The average effectiveness ratio of the gossip functionality is higher than 1:10 across topics, which is not ideal.
- Messages that are generated less frequently (such as beacon_block topic messages) are primarily propagated through the mesh and less through gossip (IHAVE/IWANT messages), hence the higher ratios, which reach up to 1:100 for this particular topic.
- GossipSub control messages are relevant, but we identify two different use-cases for GossipSub that don’t benefit in the same way from all these control messages:

Big but less frequent messages → more prone to DUPLICATED messages, but with less overhead on the IHAVE control side. The gossiping effectiveness is rather small here.
- Small but very frequent messages → add significant overhead on the bandwidth usage as many more msg_ids are added in each IHAVE message.

## Optimisation Potential

Clearly, having an effectiveness ratio of 1:10 or even less, i.e., consuming >10x more bandwidth for `IHAVE/IWANT` messages than actually needed, is not ideal. Three directions for improvement have been identified, although none of them has been implemented, tested, or simulated.

1. Bloom filters: instead of sending msgIDs in IHAVE/IWANT messages, peers can send a bloom filter of the messages that they have received within the “message window history”.
2. Adjust GossipsubHistoryGossip factor from 3 to 2: This requires some more testing, but it’s a straightforward item to consider. This parameter, set to 3 by default [link], defines for how many heartbeats do we send IHAVE messages for. Sending messages for 3 heartbeats ago obviously increases the number of messages with questionable return (i.e., how many IWANT messages do we receive in return).
3. Adaptive GossipFactor per topic: As per the original go implementation of Gossipsub [link], the GossipFactor affects how many peers we will emit gossip to at each heartbeat. The protocol sends gossip to GossipFactor * (total number of non-mesh peers). Making this a parameter that is adaptive to the ratio of Sent IHAVE vs Received IWANT messages per topic can greatly reduce the overhead seen.

Nodes sharing lots of IHAVE messages with very few IWANT messages in return could reduce the factor (saving bandwidth).
4. Nodes receiving a significant amount of IWANT messages through gossip could actually increase the GossipFactor accordingly to help out the rest of the network.
5. There is further adjustments that can be made if a node detects that a big part of its messages come from IWANT messages that it sends. These could revolve around increasing the mesh size D, or rotating the peers it has in its mesh.

For more details and results on Ethereum’s network head over to https://probelab.io.

## Replies

**Nashatyrev** (2024-06-07):

Thank you for this investigation! Interesting numbers.

Did you have the throughput ratios: what part of the whole topic traffic is consumed by `IHAVE` messages?

From my perspective the `IHAVE/IWANT` serves rather as a fallback mechanism. In good case scenario no `IWANT` messages should be sent ever. However in case of network disruption/attack it would help the network to survive. I think a have some numbers from my simulation which shows that `IHAVE` mechanism would allow the network to live even in case when > 90% of the network nodes are adversaries. Thus `IHAVE` traffic could be useless in good periods but is inevitable to survive during bad periods.

> Bloom filters: instead of sending msgIDs in IHAVE/IWANT messages, peers can send a bloom filter of the messages that they have received within the “message window history”.

That sounds like an interesting idea. That could help to save not just traffic but also the latency as would require just 1 RRT v.s. 1.5 RRT with `IHAVE`.

The only concern here is that if a node misses some message and its bloom gives false positive on that message then no it’s peer would re-transfer that message back as the same bloom would be broadcasted to all peers.

The solution however could be: use different bloom hashes for different peers, thus the probability of false positive for *all* peers would reduce exponentially

---

**pop** (2024-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/nashatyrev/48/6487_2.png) Nashatyrev:

> From my perspective the IHAVE/IWANT serves rather as a fallback mechanism.

I think it’s not just only a fallback mechanism. It also provides shortcuts for nodes if the mesh network is not dense enough. So I disagree that it’s useless in good periods.

In case of the attacks, I agree that it will help a lot because it allows non-mesh peers to receive the messages as well.

---

**yiannisbot** (2024-06-11):

I’d say that in an ideal world (no chance of attack, nodes with enough resources and correctly structured mesh) the gossip part would probably not be needed. But given that’s not the case, it’s helping a lot. The original post didn’t imply removing it at all. We just hinted on optimisation potential.

![](https://ethresear.ch/user_avatar/ethresear.ch/nashatyrev/48/6487_2.png) Nashatyrev:

> Did you have the throughput ratios: what part of the whole topic traffic is consumed by IHAVE messages?

That’s the next metric we’ve been investigating and we’ll publish a similar post in a few days. As a spoiler, I can say that about a quarter of outgoing bandwidth is spent on `IHAVE` messages, which is quite substantial. More to follow on this - I’ll link from here.

![](https://ethresear.ch/user_avatar/ethresear.ch/nashatyrev/48/6487_2.png) Nashatyrev:

> That sounds like an interesting idea.

Glad to hear the bloom filter approach sounds interesting. There’s lots to be investigated before a final design and implementation, but yeah, I agree there are edge cases of false positives that should be avoided.

---

**vyzo** (2024-08-08):

I would like to add some design perspective here: IHAVE/IWANT are mechanisms that ensure robustness to attack and network anomalies.

They really kick in in adversarial conditions – measuring the bandwidth use and “efficiency” in nominal/steady state conditions and declaring them “inefficient” is not quite accurate.

So it is quite expected that they use a bit of bandwidth, it is a trade off between robustness and bandwidth efficiency.

---

**cortze** (2024-09-18):

> IHAVE/IWANT are mechanisms that ensure robustness to attack and network anomalies.

I 100% agree. The intended take of the study isn’t “`IHAVE/IWANT` messages are a waste of resources”. We understand that making a more resilient system requires some extra cost.

> They really kick in in adversarial conditions – measuring the bandwidth use and “efficiency” in nominal/steady state conditions and declaring them “inefficient” is not quite accurate.

The point isn’t whether they are useful or not, no one is questioning it. Most mature networks operate in a “standard” or “honest” mode 99% of the time, but they should be ready for that missing 1%. Plus, we measured that there is indeed message propagation happening over gossips under “standard” conditions.

The point we are trying to make is whether the measured “effectiveness” and “efficiency” (in Ethereum) with the extra cost they imply make sense, or whether they could be optimized by adjusting parameters: i.e., the heartbeat frequency (0,7s of `heartbeat` might be too low for the current number of msgs), or whether some of these parameters should be adjusted for each topic individually (like we do for `peer scores`)

I’m happy to have a chat and discuss further upgrades to GossipSub [@vyzo](/u/vyzo) . Let me know if that would be of interest ![:v:](https://ethresear.ch/images/emoji/facebook_messenger/v.png?v=12)

---

**pop** (2024-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vyzo/48/17361_2.png) vyzo:

> They really kick in in adversarial conditions – measuring the bandwidth use and “efficiency” in nominal/steady state conditions and declaring them “inefficient” is not quite accurate.

Doesn’t IHAVE/IWANT mechanism also serve as a shortcut for the message propagation in the normal/steady state?

Like if the message takes longer than a heartbeat to propagate, IHAVE/IWANT also serves as a shortcut.

---

**yiannisbot** (2024-09-24):

Yup, definitely. What I guess [@vyzo](/u/vyzo) wanted to highlight is that it’s under an attack that gossip is going to save the day, not under steady state.

