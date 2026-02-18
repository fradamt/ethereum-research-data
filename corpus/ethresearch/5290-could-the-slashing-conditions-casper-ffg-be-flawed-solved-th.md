---
source: ethresearch
topic_id: 5290
title: Could the slashing conditions (casper FFG) be flawed?(Solved, there is no problem)
author: lucian
date: "2019-04-11"
category: Proof-of-Stake > Casper Basics
tags: [slashing-conditions]
url: https://ethresear.ch/t/could-the-slashing-conditions-casper-ffg-be-flawed-solved-there-is-no-problem/5290
views: 2774
likes: 6
posts_count: 15
---

# Could the slashing conditions (casper FFG) be flawed?(Solved, there is no problem)

I wonder if the slashing conditions could be flawed in [paper v4](https://arxiv.org/abs/1710.09437)?

Here is the demonstration(which is a modification of figure 3 in the paper):

[![casper_ffg_conflicting](https://ethresear.ch/uploads/default/optimized/2X/b/bb57023bf62473ffeced2efe6d7e4c53f736c4aa_2_318x375.png)casper_ffg_conflicting849×1001 45.5 KB](https://ethresear.ch/uploads/default/bb57023bf62473ffeced2efe6d7e4c53f736c4aa)

In the figure the purple arcs are supermajority links. a_1, a_2, a_3, b_4, b_5 are justified, and in which a_2, b_4 are finalized while you can see that a_2 and b_4 are conflicting. Less than 1/3 validators violate the slashing conditions.

In the proof of Theorem 1 we didn’t consider the edge case that chain \{a_i\} can overlap the chain \{b_i\}.

To be more specific, In the proof, *“We know that no h(b_i) equals either h(a_m) or h(a_{m+1})”* is not true when b_i is a_m or a_{m+1}. So in the proof, b_{j-1} can be a_{m+1} or a_m(in the figure above, take m=2, j=4, then b_3=b_{j-1}=a_{m+1}=a_3)

Maybe we should add slashing condition that the source and target of a vote are conflicting?

I would like to beg your pardon and please correct my errors if my understanding is wrong.

## Replies

**fubuloubu** (2019-04-11):

The next level after a_1 is a fork, let’s say the left fork is a_i and the right fork is b_i. A fork occurs when the block contents are different, so a_2 \neq b_2 (and a_3 \neq b_3) by definition. Therefore, attesting to b_4 after a_3 is a clear violation leading to the slashing condition.

The block heights could be more clearly defined in this figure, but it’s not wrong.

---

**lucian** (2019-04-11):

I put b_2,b_3 in the figure is for easily explaining the problem in the proof of the theorem, they might not are for representing another fork.

let’s put in another way, forgetting about b_i, replacing b_4, b_5 with a_4,a_5

in the figure,  we get a_1,...,a_5, all of them are justified, and a_2, a_4 are finalized but conflict with each other.

---

**fubuloubu** (2019-04-11):

b_4 is not a descendant of a_3 (i.e. it is not the parent block), therefore attesting to it as if it was would be violating the slashing condition. If a supermajority has finalized a_3, then you cannot attest to b_4 without violating this rule, and thus you wouldn’t pay any more attention to that path, even if it’s longer.

---

**lucian** (2019-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> b_4 is not a descendant of a_3 (i.e. it is not the parent block), therefore attesting to it as if it was would be violating the slashing condition

I can’t see which slashing condition it violates…could you please let me know which one specific it violates?

---

**benjaminbollen** (2019-04-11):

(using the original a_i, b_i from the drawing)

when your node has seen the finalization of a_2 with the justification of a_3, according to the fork selection rule it will not accept a re-org to the conflicting branch which has b_4.

If now the finalized a_3 branch is further extended with new blocks, and this branch is now further justified and finalized, that this can not be done by the validators without hitting a slashing condition eventually:

imagine that a_4 is at the height of b_4 and a_5 is at the height of b_5, then now they can’t vote

-  or  without violating slashing condition I.
-  without violating slashing condition II because the jump over

so important to point out here is that this achieves the objective of the consensus algorithm: as a user with access to the blocks, I can refuse a re-org to b_4, and the validators would cut in their own flesh, because they ve locked themselves out from further finalizing the a-branch without violating the slashing conditions.

---

**fubuloubu** (2019-04-11):

Ah right, so not an explicit violation persay, but locks you into a known condition where you can not continue to complete either side of the fork. To avoid this condition, clients would avoid attesting to b_4 in favor of continuing to build on the a fork to continue the chain (and earn rewards)

---

**lucian** (2019-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminbollen/48/6990_2.png) benjaminbollen:

> (using the original a_i, b_i from the drawing)
>
>
> when your node has seen the finalization of a_2 with the justification of a_3, according to the fork selection rule it will not accept a re-org to the conflicting branch which has b_4.

If with the additional fork selection rule, I agree with you that the consensus is safe. But could the rule be based on the rationale that if there is a finalized checkpoint on fork other than the previous finalized one, then 1/3 validators will lose their deposit? So I think the rule is a reduction, not an additional one.

Anyway the statement of Theorem One is not alway true, since it is only based on the two slashing conditions, and no fork selection rule gets involved.

Regarding the second point that the validators will eventually hit the slashing condition(also reply to @[fubuloubu](https://ethresear.ch/u/fubuloubu)):

We assume that there will be a_6 at height 6 in the figure, the validators can switch back by vote<b_5, a_6> without violate the slashing condition, though it seems nonsense…

---

**schemar** (2019-04-12):

In my opinion the slashing conditions exist to punish bad actors that abuse the fact that there can be, for example, a network partition and we don’t want the validators to finalize competing forks.

In your original example, you suggest that there exist votes that go “cross fork”. However, it is possible to forbid such votes on-chain, regardless of visibility of forks.

If you look at the [vyper implementation of casper](https://github.com/ethereum/casper/blob/e100a6ab43ffcc6852f246293c1101402c85b1f9/casper/contracts/simple_casper.v.py), for example, you will notice that a vote only considers the source epoch, not the specific source block hash, to verify its validity. That is because the source block hash is known based on the source epoch. One fork (where the vote takes place) can only have one source block at the given source epoch.

In short: your suggested vote is not possible based on the implementation and on the nodes’ fork choice rule as pointed out by [@benjaminbollen](/u/benjaminbollen) before:

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminbollen/48/6990_2.png) benjaminbollen:

> when your node has seen the finalization of a2a_2 with the justification of a3a_3, according to the fork selection rule it will not accept a re-org to the conflicting branch which has b4b_4.

---

**lucian** (2019-04-12):

Yes indeed the implementation you referred implicitly forbids the ‘cross fork’ vote.

But the [the official spec of attestation](https://github.com/ethereum/eth2.0-specs/blob/7db21e3f0978a4f972c53d14212dad5338404254/specs/core/0_beacon-chain.md#attestationdata) includes the source hash?

---

**schemar** (2019-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/lucian/48/3339_2.png) lucian:

> But the the official spec of attestation  includes the source hash?

I don’t know why the source hash is required in the vote. The source block is deducible based on the source height and the target hash/height.

Maybe it is required in some edge-cases that I can’t think of right now ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

---

**Alistair** (2019-04-12):

Well this isn’t an issue for full nodes as long as they see that a3/b3 is finalised and don’t follow the b chain as a result. and it requires 2/3 dishonest validators. It means that a light client would need to download at least all the headers to be sure that this does not happen.

But a majority of dishonest validators could also fool a light client by building on an invalid block, which would likely be just as bad an attack, and also hard to prove.

On the other hand, if you wanted to use Casper FFG for a sidechain, then there would be some merit to designing a chain with short proofs-of-invalidity and proofs-of-ancestry. Then you could add slashing conditions for voting on a descendent of an invalid block or doing a vote like a/3/b3->b4.

Proofs of ancestry are useful for other things. We’ve found them useful for GRANDPA, and they might be for Casper CBC. They are also useful for bridges, just like sidechains. So designing a chain to make them short or evenn using (recursive) SNARKs etc., is worth thinking about.

---

**lucian** (2019-04-13):

Sorry I don’t know the meaning of the proof of ancestry and ‘GRADPA’.

Thank you guys for helping me understand how casper will work.

According to what we discussed, we all agree that:

1. if 2/3 of the validators are honest and
2. honest validators don’t switch from a finalized checkpoint to a conflicting one, then the blockchain is safe(i.e., no two finalized checkpoints conflicts each other)
3. we believe the 2/3s are honest.
So the blockchain will be safe.

I have no problem with it. But please allow me to argue something.

1)If we ONLY think about the reasoning in the Theorem One, which is about the  safety(without additional ‘honest action’, since as a mathematical proof, it is supposed to be logical self-contained without any external hypothesis), I would say the two slashing conditions could be not adequate and the proof itself might not be very correct.

2)The philosophy behind the casper I guess is to turn the hypothesis of ‘honest people’ to ‘rational people’(I guess that’s why we call casper is based on the cryptoeconomy), which implies that as soon as the action is to weaken the blockchain and validators will get benefit from the it, the action will get punished, so the expectation of profit of this kind of actions will be negative, preventing rational validators to take it. For example slashing condition one is to prevent the ‘vote with no stake’.

If the ‘cross-fork’ votes get no slashed, rational validators will probably do it if there is for example some kind of double-spending benefits the validators. The cost is zero anyway why not have a try?

On the contrary if we assume 2/3 are honest, I would argue that the two slashing conditions can also be removed since 2/3 are honest.

1. I think the fork rule is based on the rationale that no finalized checkpoint will be reverted unless 1/3 validators’ deposit get slashed, and which is based on the Theorem of the Safety, not based on the honesty.

The reason I insist arguing about this is that as soon as we have some flaw in the logic which we thought is right, someone will use it to attack the blockchain probably.

---

**Alistair** (2019-04-13):

Theorem 1 is correct. However it has an assumption that you might have missed. On page 2 before the table, it says “We require that s be an ancestor of t in the checkpoint tree, otherwise the vote is considered invalid”. The two slashing conditions guarantee safety only if parties only act on valid votes. Unless we knew that b3 was an ancestor of b4, we would ignore the vote b3->b4.

If there are economically important actors who need to act on votes but do not understand ancestry, then yes, we’d need more slashing conditions. One would be to make the vote b3->b4 slashable because the ancestor of b4 at height 3 is not b3. The transaction that points this out would need to include the vote and a “proof-of-ancestry” that shows that “c3 is the ancestor of b4 at height 3”. This is harder to show than the other slashing conditions, but it still might be useful for sidechains, where the most important actor, the main chain or a smart contract on it, is data constrained.

GRANDPA ([1](https://medium.com/polkadot-network/grandpa-block-finality-in-polkadot-an-introduction-part-1-d08a24a021b5),[2](https://github.com/w3f/consensus/blob/af539f50ed6aa569aa0577721cfdcc3d18158b7e/pdf/grandpa.pdf)) is my own take on finality gadgets and has similar issues.

---

**lucian** (2019-04-13):

You are right. Sorry I just neglected that statement.

Thank you for your providing very valuable information.

