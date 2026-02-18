---
source: ethresearch
topic_id: 20907
title: GossipSub Topic Observation (proposed GossipSub 1.3)
author: pop
date: "2024-11-02"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/gossipsub-topic-observation-proposed-gossipsub-1-3/20907
views: 527
likes: 4
posts_count: 12
---

# GossipSub Topic Observation (proposed GossipSub 1.3)

*Authors: [pop](https://github.com/ppopth)*

*tldr; topic observation enables the nodes to get notified when there is a new message in

a topic without actually receiving the actual message.*

This proposal enables you to tell your peers to notify you when there is a new message in the topic without consuming the bandwidth to download the actual message. When you do this, you are called an observing node in that topic.

# Motivation

Topic observation is motivated by the amplification factor on bandwidth consumption due to the mesh degree of GossipSub. When you subscribe to a topic, you would need to download or forward as many copies of messages as the mesh degree. For example, if the mesh degree is 8, you would roughly download or forward 8 copies.

We have `IDONTWANT` implemented in GossipSub 1.2 which will reduce the number of copies you will download or forward, but it doesn’t guarantee exactly how many.

When you observe a topic, you won’t receive any message. You will only get notified when there is a new message. If you want the actual message, you can request the message from the peer that notifies you first, so you will download only one copy. However, the message request part is out-of-scope of this proposal. This proposal only deals with notifications.

# High-level design

[![output](https://ethresear.ch/uploads/default/optimized/3X/b/7/b77e73993faca2c60d123d3700f2e20d3cbf3f24_2_663x500.png)output1280×964 88.4 KB](https://ethresear.ch/uploads/default/b77e73993faca2c60d123d3700f2e20d3cbf3f24)

When you want to observe a topic, you would need to find subscribing nodes in the topic and tell them you want to observe the topic. Later, when there is a new message, those subscribing nodes will notify you.

Let’s see examples in the figure, node 11 is observing the topic. Node 1, 9, and 10 will notify node 11 when there are new messages. Similarly, node 4 and 5 will notify node 12.

Notice that the relationship is unidirectional rather then bidirectional like mesh connections.

You can also tell your subscribing peers when you don’t want to observe the topic anymore. That is when you want to unobserve it.

# Stability

Notice that observing nodes only receive notifications. They neither send notifications nor forward messages. In other words, they only consume, not contribute. So, they are only on the border of the network (as shown in the figure) and don’t provide any stability to the network. It means that there must be enough subscribing nodes in the network to provide stability.

However, the good side of this is that the churn rate of observing nodes doesn’t matter at all. Nodes can observe and unobserve as often as they want.

# Scalability

Currently, when your peers want to observe the topic and tell you to notify, you are obligated to notify them without the option to decline. This has a downside that if too many of your peers want to observe, you will have too much overhead to do the job.

However, the notifications consist only of messages ids which we now assume to be negligible. You may argue that if the number of observing peers is high enough, the total size of notifications will be significant. That’s true, but for the first iteration of the design, we should make this assumption to make the protocol simple.

# Protocol messages

There are two new control messages: `OBSERVE` and `UNOBSERVE`.

You send `OBSERVE` to your peer when you want to observe a topic and have that peer notify you.

You send `UNOBSERVE` to your peer to tell that you don’t observe the topic anymore.

After sending `OBSERVE` to your peer, the peer will send `IHAVE` to you as a notification, when there is a new message in the topic.

However, `IHAVE` in this proposal is different from the previous GossipSub versions. In the previous versions, `IHAVE` is sent only at the heartbeats, while in this version, it can also be sent right after peers receive messages. Previously, you can send `IWANT` after receiving `IHAVE`, but in topic observations, you aren’t expected to send `IWANT`, since `IHAVE` serves only as a notification.

## Replies

**yiannisbot** (2024-11-05):

Interesting idea for sure. My main concern here would be wrt incentives, which you’re slightly touching: why would nodes be subscribing nodes, when they can just rely on others, save bandwidth and be observing nodes?

An alternative would be to adjust the tradeoff between “Eager Push” and “Lazy Pull” in the protocol’s settings (see graphic from an old [blogpost](https://research.protocol.ai/blog/2020/gossipsub-an-attack-resilient-messaging-layer-protocol-for-public-blockchains/)). This could be done by reducing the number of mesh connected nodes and rely more on gossip. But, as you say, gossip comes at the heartbeat which might be too late. But an option to fire gossip together with “just seen/published” messages would be a good middle ground, maybe?

[![gossipsub-tradeoff](https://ethresear.ch/uploads/default/optimized/3X/7/a/7afd0f0fda8da639cbf175627877d25ce8c667c2_2_318x250.png)gossipsub-tradeoff902×709 30.1 KB](https://ethresear.ch/uploads/default/7afd0f0fda8da639cbf175627877d25ce8c667c2)

---

**yiannisbot** (2024-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> When you subscribe to a topic, you would need to download as many copies of messages as the mesh degree. For example, if the mesh degree is 8, you would roughly download 8 copies.

That’s not quite true because the mesh of a node is not fully connected, i.e., not everyone is connected to everyone else. We’ve built a simple model, which concludes that when the mesh degree is `D=8` the number of duplicates to expect is `(D-2)/2 = 3`. See more details in this post: [Number Duplicate Messages in Ethereum's Gossipsub Network](https://ethresear.ch/t/number-duplicate-messages-in-ethereums-gossipsub-network/19921#expected-results-3)

---

**pop** (2024-11-05):

Oh, no. I forgot that. Thank you. However, it receives only D/2 copies, but the overall bandwidth usage is still D (for both upload and download). I will update the wording in the post correspondingly.

---

**pop** (2024-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/yiannisbot/48/14069_2.png) yiannisbot:

> My main concern here would be wrt incentives

No worries about incentives. In Ethereum, we already have a lot of things that honest nodes have to do without incentives. For example,

1. When you attest the blocks, you can just send your attestations to the topic by fan-out instead of subscribing to the topic.
2. Honest nodes are required to aggregate attestations, which they absolutely don’t have incentives to do.

So for anything in Ethereum, feel free to have honest nodes do it without incentives. If we can give incentives, yes it’s good. If not, no worries.

![](https://ethresear.ch/user_avatar/ethresear.ch/yiannisbot/48/14069_2.png) yiannisbot:

> But an option to fire gossip together with “just seen/published” messages would be a good middle ground, maybe?

I don’t know. If I remember correctly, there is some rationale on sending at heartbeats written in [gossipsub spec](https://github.com/libp2p/specs/tree/master/pubsub/gossipsub).

However, in the current GossipSub, IHAVEs are sent to random peers, rather than the peers that want to receive, so there must still be new control messages anyway.

---

**cortze** (2024-11-06):

Interesting idea, yes. Just a few questions:

> Currently, when your peers want to observe the topic and tell you to notify, you are obligated to notify them without the option to decline.

How desirable is this particular solution, in the sense of, how could you ensure this from a P2P perspective, and what would be the penalization for those breaking the enforced “push notification” duties?

Also, would accepting `OBSERVE` messages be somehow tuneable for each particular topic?

You could be forced to supply those targeted `IHAVEs` in topics with a high msg frequency (i.e., attestation subnets), which could make your node waste CPU cycles just for someone’s laziness.

---

**pop** (2024-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/cortze/48/10089_2.png) cortze:

> How desirable is this particular solution, in the sense of, how could you ensure this from a P2P perspective, and what would be the penalization for those breaking the enforced “push notification” duties?

We can de-score them. That’s the best I can think of now and I think that’s enough. Writing the spec on this shouldn’t be a lot of work since we have de-score mechanism already in the libp2p spec.

![](https://ethresear.ch/user_avatar/ethresear.ch/cortze/48/10089_2.png) cortze:

> Also, would accepting OBSERVE messages be somehow tuneable for each particular topic?

Yes, it should be a global configuration for each topic.

---

Both things are minor details that can be put later in the spec. I didn’t put it here because I would like to make the first iteration as simple and as short as possible.

---

**AgeManning** (2024-11-06):

> No worries about incentives. In Ethereum, we already have a lot of things that honest nodes have to do without incentives. For example,
>
>
> When you attest the blocks, you can just send your attestations to the topic by fan-out instead of subscribing to the topic.
> Honest nodes are required to aggregate attestations, which they absolutely don’t have incentives to do.

Just FYI,

For 1. This is not just an honesty requirement. Nodes have to subscribe to subnets based on their peer-id. We can ban nodes that do not do this (this is currently not implemented, but we intend to in the near future, once all clients implement it).

For 2 - Only some are allowed to aggregate. I think validators will want to because they get to choose their own attestation to aggregate. If they didn’t aggregate they might not get their attestation included into a block which is a financial loss. So they are incentivized to aggregate.

I think we should have incentives to perform any extra duties that may consume extra resources.

---

**pop** (2024-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/yiannisbot/48/14069_2.png) yiannisbot:

> My main concern here would be wrt incentives, which you’re slightly touching: why would nodes be subscribing nodes, when they can just rely on others, save bandwidth and be observing nodes?

![](https://ethresear.ch/user_avatar/ethresear.ch/agemanning/48/2204_2.png) AgeManning:

> For 1. This is not just an honesty requirement. Nodes have to subscribe to subnets based on their peer-id. We can ban nodes that do not do this (this is currently not implemented, but we intend to in the near future, once all clients implement it).

So incentivizing this becomes easy then. Just do the same. Let the nodes subscribe to the topic based on their peer-id and ban nodes that do not.

However, incentives are not part of the libp2p GossipSub, but specific to Ethereum.

---

[@AgeManning](/u/agemanning) I would like to give another example because I’m not quite convinced yet.

You can vote for an invalid block without penalties. This will save a lot of CPU because you don’t have to do block validation in the EL. This seems to me that there is no way to penalize this.

---

**AgeManning** (2024-11-08):

Yep, I agree we can make some incentives similar to what we have.

I also think voting for an invalid block will incur a penalty.

Assuming an honest majority, if you vote for an invalid block (unless everyone else in your committee also votes for the same invalid block) your attestation won’t be able to be aggregated (unless you are the aggregator). Even if you are the aggregator your aggregate attestation will likely only contain your signature.

The validator creating the block can only pack so many attestations into that block. As they are rewarded based on the number of signatures they can get in there, they are unlikely to include your sole attestation as they can profit more from including aggregate attestations with more validator signatures.

I might be wrong here, but I think the end result is that it is a lot more likely that your attestation won’t end up in a block and therefore you will not be rewarded. So essentially you are penalized for this strategy.

It might be worth testing this tho.

---

**ufarooqstatus** (2024-11-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> However, IHAVE in this proposal is different from the previous GossipSub versions. In the previous versions, IHAVE is sent only at the heartbeats, while in this version, it can also be sent right after peers receive messages. Previously, you can send IWANT after receiving IHAVE, but in topic observations, you aren’t expected to send IWANT, since IHAVE serves only as a notification.

IMO, IDONTWANT message serves the same purpose. An IDONTWANT is issued to all the peers immediately after receiving a message (above a tunable threshold size).

In this case, it can be sent to “peers + subscribed_peers” (this can eliminate the need for adding a new message)

---

**pop** (2024-11-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/ufarooqstatus/48/18298_2.png) ufarooqstatus:

> In this case, it can be sent to “peers + subscribed_peers” (this can eliminate the need for adding a new message)

IDONTWANT has an incorrect semantic for this case. The observing node will get confused why you tell them you don’t want the message. ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

Subscribing node: I don’t want a message with this msg id.

Observing node: Why tell me?? Tell me when you get a new message, okay?

And then the observing node gets confused.

