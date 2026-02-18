---
source: ethresearch
topic_id: 961
title: Ethereum fundamental research topics
author: eswak
date: "2018-01-30"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/ethereum-fundamental-research-topics/961
views: 2390
likes: 3
posts_count: 11
---

# Ethereum fundamental research topics

Hello members of the Ethereum Research community,

I’m a Computer Science Master 2 student in France with good academic results and I’ll soon be applying for a public research grant.

I’m fairly interested in the Ethereum protocol, and would love to help the community. This mix of computer science, mathematics and economy sounds perfect to me.

I can basically shape my own PhD subject but I need to submit an application with references and intended research topics.

What are the currently active research topics that surround the Ethereum protocol ? I’m particularly interested in game theory and decision making.

I won’t have any difficulty to justify use-cases but I’m looking for keywords and recent publications that could provide me some insights on what are the underlying active fundamental research fields.

Paper links/references and why they are relevant to the Ethereum protocol would be very helpful.

## Replies

**kladkogex** (2018-01-30):

You need to research how to securely transfer Ethereum back and forth between the main chain and Ethereum shards (other independent chains).

And also how to make a secure contract calls from one independent chain to another - this is a problem that no-one knows how to solve!

---

**tawarien** (2018-01-31):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> You need to research how to securely transfer Ethereum back and forth between the main chain and Ethereum shards (other independent chains).

I thought in case of shards the plan was to produce receipts that contain the Ether and then can be consumed by another transaction on the target shard to release the Ether. Is their a discussion about the problems with this approach some where or is this approach no longer under discussion

---

**kladkogex** (2018-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> I thought in case of shards the plan was to produce receipts that contain the Ether and then can be consumed by another transaction on the target shard to release the Ether

I guess it is good plan at a high level and there are many ways to implement this, the question is how to translate this into mathematics and prove security in some model.

---

**vbuterin** (2018-01-31):

If block A2 in shard A consumes a receipt created in block B1 in shard B, then B1 becomes a logical parent of A2; that is, we should consider both A2’s actual parent in shard A, and B1, as dependencies of A2. A chain (really, DAG) where A2 consumes a receipt, but the source of the receipt is not part of the chain/DAG, or it or any of its own ancestors is invalid, is an invalid chain.

Now that we’ve shown that all cross-shard transactions in a valid chain are secure by definition, we move on to the real challenge: checking that the chain we are in is valid. A super-full-node can do this easily, though there is still a challenge in making an *online* algorithm for determining the head of each shard chain (that is, if, *right now*, A2 is in the main chain of shard A and B1 is in the main chain of shard B, that’s good, but what if suddenly B has a large reorg and B1 is no longer in the main chain? How do you invalidate all of B1’s dependencies?). Vlad’s fork choice rule touches on some of these questions but there are other ways to do it as well.

The second challenge is, how can a not-super-full node determine reliably if the entire chain is valid? This starts getting into questions of “collaborative validation” and “almost-fully-validating light client” theory where things like fraud proofs, [data availability proofs](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding) and similar fancy stuff come into play; it is possible but you do need a couple of additional assumptions (bound on network latency, honest client minority, etc).

---

**kladkogex** (2018-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If block A2 in shard A consumes a receipt created in block B1 in shard B, then B1 becomes a logical parent of A2; that is, we should consider both A2’s actual parent in shard A, and B1, as dependencies of A2

You could arguably have a mechanism, where a receipt would be  signed by Casper validators for the Shard A using some kind of a threshold signature, so security would be based on security of 2/ 3  validators for the shard A. In this case you would have to wait until the receipt is finalized by the validators,  but arguably then you would not need to care about any reorgs … ?

Or I am totally wrong ?)

---

**vbuterin** (2018-01-31):

Yeah, this is the simplest approach: wait for finality of B1 before allowing it to be a dependency of A2, so that reorgs are simply not an issue. But we should be able to make cross-chain messages happen faster than finality…

---

**bradleat** (2018-02-01):

These messages have to be revertable or removed from the side chain if the parent chain reverts.

It seems to me that if chain A is dependent on chain B, chain A cannot have any final state changes based on chain B’s receipts until chain A reaches finality.

I guess you’d have to do chain A and B’s finality at the same time. Especially if B can also be dependant on A in the same period.

---

**kladkogex** (2018-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/bradleat/48/527_2.png) bradleat:

> It seems to me that if chain A is dependent on chain B, chain A cannot have any final state changes based on chain B’s receipts until chain A reaches finality.
>
>
> I guess you’d have to do chain A and B’s finality at the same time. Especially if B can also be dependant on A in the same period.

Thats a good point, It seems to me too that  marrying Casper validators and sharding is a touchy subject.

Mathematical proofs in the Casper whitepaper assume a single chain …  If there are  two chains submitting receipts to each other,  you kind of couple Casper validators on different chains, so you have to consider interactions between them,  which opens up Pandora box a bit …  All of proofs become mathematically vague …  Essentially if you Casper-finalize a block on one chain, if may include yet Casper-unfinalized receipts from another chain.   So it becomes kind of a Byzantine agreement problem where sets of validators on each chain need to finalize in some kind of atomic sync.

Seems like a simple deadlock can arise, where a Casper-unfinalized receipt from chain B is submitted to chain A, and Casper validators on chain A finalize it,  but later Casper validators on chain B decide to finalize a competing B-chain.  There is no way to unfinalize a receipt on chain A, so the entire system would deadlock and stall.

It seems that the only way to avoid this deadlock is to only submit Casper-finalized receipts across  chains …

---

**vbuterin** (2018-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/bradleat/48/527_2.png) bradleat:

> It seems to me that if chain A is dependent on chain B, chain A cannot have any final state changes based on chain B’s receipts until chain A reaches finality.

Correct. Though there is one loophole: it’s theoretically possible to design a system where **transactions** on chain A can be finalized quickly, even if the **post-state roots** is not finalized until chain B finalizes. Basically, the transactions on chain A would be quickly frozen in stone, but then the consensus could flip back and forth on whether final state reflects the execution of chain A plus one branch of chain B or chain A plus the other branch of chain B. This has the benefit that anything in the state of chain A that does not have chain B in its dependency cone can “finalize” much faster than the complete state root.

I know that Vlad has spent a lot of time thinking through ideas like this.

---

**jamesray1** (2018-04-19):

Well this is a very belated reply, but there’s a wiki [here](https://github.com/ethereum/wiki/wiki/Sharding-introduction-and-implementations) which tries to list or summarise everything happening with sharding at the moment. It includes an independent researcher and a couple of compendiums on research.

