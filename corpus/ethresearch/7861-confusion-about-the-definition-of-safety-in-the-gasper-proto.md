---
source: ethresearch
topic_id: 7861
title: Confusion about the definition of safety in the Gasper protocol
author: newptcai
date: "2020-08-18"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/confusion-about-the-definition-of-safety-in-the-gasper-protocol/7861
views: 1972
likes: 4
posts_count: 9
---

# Confusion about the definition of safety in the Gasper protocol

I am reading the Gapser paper [here](https://arxiv.org/abs/2003.03052), it defines *safety* as

> safety, if the set of finalized blocks F(G) for any view G can never contain two conflicting
> blocks. A consequence of having safety is that any validator view G’s finalized blocks
> F (G) can be “completed” into a unique subchain of F (view(NW)) that starts at the genesis
> block and ends at the last finalized block, which we call the finalized chain.

What I don’t get is, it seems trivial to have no conflicting blocks. Given a view (here it means a tree of blocks), just choose any chain to be the finalized blocks, then there is no conflict anymore.  How can this be considered as having achieved “safety”?

## Replies

**thor314** (2020-08-18):

Coauthor here. I’m not entirely certain I understand your question, so I’m going to try to give a short passage clarifying any misunderstandings.

A validator does not choose a chain of blocks to be finalized. A block is “justified” if it has 2/3 attestation weight, and “finalized” if it is justified, and immediately follows another justified block. Thus finalization is a way of understanding permanency of a block in a blockchain. We want to prove that it’s impossible to have a situation where the chain comes to a situation where two conflicting blocks are finalized (or else we don’t really have a consensus protocol). We give a proof in section 4 roughly as follows:

If two conflicting blocks were to be finalized, that would mean:

1. the chain has forked
2. two thirds of validators have attested to each of the conflicting blocks
3. therefore at least one third of validators attested to each block, meaning the chain is 1/3-slashable.

This gets us most of the way to “safety”.

---

**newptcai** (2020-08-19):

Hi thank you very much for your clarification.

Though I wanted to point out, if you interpret the definition of *safety* in the quoted passage rigorously/mathematically, then it is rather trivial to achieve it.

A view is just a tree. Finalized blocks is just a subset of nodes (blocks) in the tree. Whatever tree/view G you are given, simply let F(G) return only the root node. This silly protocol will guarantee you never have conflicts in F(G).

If you insist that F(G) grows as G grows, then you can simply take the path from the root to the leaf with the highest timestamp as F(G), then there is also no conflicts in F(G).

I suspect that you actually also want to insist that if two views G and G' satisfy G \subseteq G' , then F(G) \subseteq F(G'). This makes the definition more interesting and harder to achieve.  This will also make the statement “A consequence of having …” in that paragraph valid. However, this is missing in the definition.

---

**newptcai** (2020-08-19):

Another definition that confuses me is this

> Definition 4.4. Given a block B, we define view(B), the view of B, to be the view consisting of
> B and all its ancestors in the dependency graph. We define ffgview(B), the FFG view of B, to be view(LEBB(B)).

First of all, this is the first time the term *dependency graph* is mentioned anywhere in the paper. I suppose you meant the graph formed by the dependency relationship of messages. And by block B, you actually meant to say the message that proposes the block B.

Then it’s *ambiguous* what do you mean by ancestors here. Does that mean messages that *message* B depends on, or any *accepted* messages with a timestamp earlier than B's timestamp (slot number)?

In particular, it seems view(B) must include attestation messages that will be needed to decide the last justified pair. But then the paragraph afterwards does not make sense anymore

> The definition view(B) is “agnostic of the viewer” in which any view that accepted B can compute an identical view(B), so we do not need to supply a validator (or NW) into the argument.

Each validator receives messages with different delays. So the attestation messages before B may or may not have arrived. How can each validator have the same view(B)?

---

**thor314** (2020-08-20):

In S4.5 we define finalization: (B_k,j) is finalized in G if (B_k,j) = \max_{k}B_k \in view(G) such that [![Screen Shot 2020-08-20 at 3.04.33 PM](https://ethresear.ch/uploads/default/optimized/2X/3/31df3783ad95a3376947ef2d9dc5efc4e99bfba1_2_690x116.png)Screen Shot 2020-08-20 at 3.04.33 PM1146×194 14 KB](https://ethresear.ch/uploads/default/31df3783ad95a3376947ef2d9dc5efc4e99bfba1)

By that logic, your statement about F(G)\subseteq F(G') is implied.

Concerning Defn 4.4; dependencies are described in S2.2, with Example 2.2 giving further context. In definition 4.2, we state that “For dependencies, B depends on P (B) and all attestations in newattests(B)”.

Although we don’t give a definition for dependency graph (and you’re right we probably should have!), the definition of dependency graph reasonably follows definiton 4.2.

---

**newptcai** (2020-08-20):

[@thor314](/u/thor314) I agree. But this should be part of the *definition* of *safety* up front. Otherwise, it’s a very a weak requirement.

It’s a bit like defining *safe car* as *any car made of metal*, but then argue/prove that you have a *car* is factually *safe*, because it has all the safety measures.

---

**newptcai** (2020-08-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/thor314/48/11146_2.png) thor314:

> Concerning Defn 4.4; dependencies are described in S2.2, with Example 2.2 giving further context. In definition 4.2, we state that “For dependencies, BB depends on P (B) and all attestations in newattests(B)”.

Then `view(B)` cannot be viewer agnostic, right? The set of messages newattests(B) must depend on which validator/viewer we are talking about.

---

**thor314** (2020-08-20):

We generally avoid talking about a view of a block. Views are described from the perspective of a validator or the network. When we do use view(B), as we do in section 4, we explicitly mean the ancestors of the block, and its message dependencies.

---

**newptcai** (2020-08-20):

[@thor314](/u/thor314) Thanks, I think I now understand the definition of `view(B)` now.

Though I do suggest that when you emphasize that when we talk about `view(B)`, we are talking about the message `P(B)` and what it dependent messages are. This will make this section much clearer.

