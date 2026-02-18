---
source: ethresearch
topic_id: 21901
title: Coordinated dampening of untrusted gossip
author: bowaggoner
date: "2025-03-08"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/coordinated-dampening-of-untrusted-gossip/21901
views: 187
likes: 0
posts_count: 2
---

# Coordinated dampening of untrusted gossip

**Disclaimer.** I’ll admit up front that I have a lot to learn about the peer-to-peer layer; I’d love pointers to deeper resources beyond e.g. the [ethereum.org](http://ethereum.org) [documentation about the networking layer](https://ethereum.org/en/developers/docs/networking-layer/).

**Background.** In my understanding, the P2P protocol needs to very carefully limit messages propogated, to avoid DOS. Therefore, nodes employ a variety of rules and also heuristics to decide when to pass on gossip. However, we do need to often allow messages to make it across the entire network, even some messages that seem wrong or untrusted to the current node (I am thinking of the Holesky Pectra deployment failure, where we need the minority chain members to be able to reach each other).

So, we would like each untrustworthy message to either be treated in one of two ways:

1. Essentially do not propogate at all; reject.
2. Propogate to essentially every node on the network, with as little communication as possible.

For example, for each message, we can flip a coin with weight depending on how overloaded the network currently is and how trustworthy the message is, and propogate the message only if the coin comes up heads.

**Problem.** The key point is that if each node tries to employ such a filtering method independently, we will (I think) fail to achieve a balance between (1) and (2) above. If each node randomly rejects, then messages will generally die out after a few hops, not reaching the entire network. If that is not true (i.e. random rejection probabilities are low), then most messages will reach the entire network, but that means we’re vulnerable to DOS.

**Proposal.** We can use a coordination mechanism where instead of nodes independently flipping a coin, they coordinate to all flip the same coin. If the coin is heads, every node spreads this untrustworthy message (according to a reasonable gossip protocol; I’m not saying they have to blast it to all their peers). If the coin is tails, every honest node agrees not to spread this message.

How do we flip a coin all together? We can do something like hash the message along with the header of the most recent block on the chain, and propogate the message if the last bit is 1. Since most of the network will agree on the most recent block, this will have pretty good coordination properties.

**Extension.** Suppose that nodes want to coordinate, but each node wants to use its own heuristics for trustworthiness of a message and make its own decisions about how often to propogate in general. We can ask each node to compute a score for each message between 0 and 2^{64} based on trustworthiness and willingness to propogate. A node then uses the last 64 bits of the coordinated hash mentioned above to determine a threshold between 0 and 2^{64} - 1. If the message’s score is above my personal threshold, then I propagate the message. This system will still have the property that it propogates generally trustworthy messages much more than untrustworthy ones, but it sometimes allows seemingly-untrustworthy messages to spread.

**Note.** A similar technique can be used for other P2P decisions, such as whether to respond to requests from a new, untrusted node. Also, this technique can be pictured as, or modified to work as, a type of proof-of-work HashCash defense mechanism against DOS attacks.

**Questions.** Are ideas like this already out there? Is it a reasonable or potentially useful idea? Is there something important about the P2P layer that I don’t seem to understand?

## Replies

**bowaggoner** (2025-03-09):

Here’s a simple mathematical model and impossibility/possibility result. You can tell me if this is a bad model of P2P and gossip.

For simplicity, abstract away trusted messages; suppose that trusted communication is occurring in the background at a manageable level. Focus on untrusted messages. Suppose that every message is a “broadcast”, meaning that it is intended to reach every node in the network. Suppose for simplicity that when nodes receive a broadcast for the first time, they must either decide to immediately propagate it to all neighbors, or else to never propagate it. This decision is called **filtering.** In this simple setting, filtering is simply a binary decision: with some probability p, broadcast the untrusted message, and otherwise do not.

There are n+3 nodes in the network. n of the nodes, u_1,\dots,u_n, are the *honest majority*. There are two *honest minority* nodes v_1,v_2. And there is one *malicious* node v_3. The honest majority nodes cannot distinguish between messages sent by the honest minority and the malicious node.

Say the system is **well-connected** if there is some constant q_{c} > 0 independent of n such that, with probability at least q_c, a broadcast from v_1 reaches v_2.

Say the system is **DOS-resistant** if there is some constant q_{d} < 1 independent of n such that, with probability at most q_d, a broadcast from v_3 reaches every node in the graph.

Say the system is **anonymous** if every honest node uses the same filtering probability p.

**Theorem 1.** If majority nodes filter independently, then there is no system that is anonymous, well-connected, and DOS-resistant.

*Proof.* Consider these two structures:

![graph-structures-2](https://ethresear.ch/uploads/default/original/3X/a/8/a8b6802740f22b32c5e7aea0e9ce1d53fc8f96a6.svg)

In both cases, the probability of getting the honest message through equals the probability of getting a malicious message to every node. Using anonymity, in the top case, the probability is p^n because we need every u_i to broadcast. In the bottom case, it is p^2 because we just need u_1 and u_n to broadcast.

To be well-connected, we need p^2 \geq q_c > 0, which implies p > \sqrt{q_c}, a constant. To be DOS-resistant, we need p^n \leq q_d < 1, which implies p \leq (q_d)^{1/n}, which goes to zero as n \to \infty. There is no choice of p that satisfies both.

Of course, the example is contrived, but in reality, we can’t assume too much knowledge of the graph structure, especially if we want to reach minority nodes that may be somewhat isolated. Even with some knowledge of the graph structure, tuning p correctly may still be very difficult or impossible.

---

**Theorem 2.** With access to shared randomness r, there is a filtering strategy that is anonymous, well-connected, and DOS-resistant. Furthermore, for any constant \alpha \in [0,1], there is such a strategy that sets q_c = q_d = \alpha, regardless of graph size and structure.

*Proof.* As discussed in the post, for each message m at time tick t, a node can compute x = h(r,m,t) for some hash function h without any communication with other neighbors. All honest majority nodes will compute the same value x. We can suppose that h(r,m,t) is uniformly random in [0,1] for all m and t. A node then propogates the message if and only if x \leq \alpha. Then every message has a probability of exactly \alpha of being spread to the entire network, and probability 1-\alpha of being spread only to the node(s) that initially received it.

---

Let me know if this makes sense and if it sounds useful. We can also extend this with a HashCash proof of work idea so that spreading a message to the entire network requires any given level of proof of work.

