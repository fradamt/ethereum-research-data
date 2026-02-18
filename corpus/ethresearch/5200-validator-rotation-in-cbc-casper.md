---
source: ethresearch
topic_id: 5200
title: Validator rotation in CBC Casper
author: nrryuya
date: "2019-03-25"
category: Proof-of-Stake
tags: [validator-rotation, cbc-casper]
url: https://ethresear.ch/t/validator-rotation-in-cbc-casper/5200
views: 2673
likes: 5
posts_count: 7
---

# Validator rotation in CBC Casper

How to realize validator rotation in CBC Casper is an open question.

In this post, I present a modification of CBC Casper for validator rotation.

The more formal version of this proposal is [here](https://scrapbox.io/layerx/Casper_CBC:_General_validator_rotation).

### Prerequisite

The latest CBC Casper paper with [the draft of Section7 by Nate Rush](https://github.com/cbc-casper/cbc-casper-paper/pull/13) (The compiled version is [here](https://drive.google.com/file/d/1lGg0RDZ7BW7DnuJKP_YWaYe5VN2TPEw2).)

I reuse definitions and lemmas in the original paper.

### Overview

- Replace weight in CBC parameters with weights \mathcal{W}, which is a set of all possible weight.
- Define a function to calculate a weight from a consensus value (block)

E.g. Calculate a weight from the information (e.g. entry/exit transactions, slashing transactions, etc.) included in the chain until its parent block

\mathrm{Weight}: \mathcal{C} \rightarrow \mathcal{W}

- Modify the fork choice rule (estimator)  to use  \mathrm{Weight} so that the result is deterministic regardless of validator rotation.

E.g. Modify LMD GHOST to score a block b by \mathrm{Weight}(b) in the “best children selection”.
- This is originally proposed in the previous draft of Casper TFG paper.

Validators make a decision on a chain if all blocks in the chain are decided to win best children selection in GHOST at its height for any future states where there are t equivocations or less by \mathrm{Weight}(b).

- To detect this finality, we use clique oracle for the best children properties.

Validators decide on a chain if there are cliques for any blocks in the chain.
- We weight a clique agreeing on a block b by \mathrm{Weight}(b).

From these, the protocol has safety i.e. validators do not decide on conflicting blocks if there are t equivocations or less by \mathrm{Weight}(b) for any b they decided on.
For liveness, we allow validators to exit by a bounded ratio every time a block is supported by a certain size of a clique (*on-chain finalized*).

- Any exited validator’s weight is set to 0. They can not create a valid message by his public key.
- For any block b, validators who have a non-zero weight in \mathrm{Weight}(b) can exit up to \alpha by weight.

Hence the 1 - \alpha weight (by ratio) can contribute to the clique agreeing on the block
- For plausible liveness, fault tolerance is
An *on-chain finalized block* is defined as a block which is supported by a clique larger than or equal to (2 - \alpha)/3 (by ratio).

- This is the maximal threshold which does not break plausible liveness.
- Strictly speaking, we need to subtract 1 unit from this threshold.

The blockchain can include an exit transaction if and only if it does not make the exiting weight exceed \alpha for the oldest non-on-chain-finalized block.

Any validator can go offline when her exit transaction is included in a block and the block gets finalized subjectively by t such that t < (1 - 2\alpha)/3.

N.B. Proofs of these claims are WIP.

## Replies

**vbuterin** (2019-03-31):

> E.g. Modify LMD GHOST to score a block b by Weight(b) in the “best children selection”.

To be clear, this means that if a block b has children c_1 ... c_n, we use the weights in b to choose between c_1 ... c_n, and then if we choose c_i with children d_1 .... d_n we use the weights in c_i to choose one of them, and so on and so forth, correct?

> For liveness, we allow validators to exit by a bounded ratio every time a block is supported by a certain size of a clique ( on-chain finalized ).

So this basically means “enshrine a specific finality oracle in-protocol and allow some bounded quantity of exits every time a finality event happens”, correct?

If we don’t want to enshrine a specific finality oracle, what do you think of our current proposed approach of simply having a bounded exit rate of N per period, so the weak subjectivity bound (which is already a synchrony assumption) becomes a more explicit synchrony assumption?

---

**nrryuya** (2019-04-01):

> To be clear, this means that…

Yes!

> So this basically means “enshrine a specific finality oracle in-protocol and allow some bounded quantity of exits every time a finality event happens”, correct?

Yes!

> If we don’t want to enshrine a specific finality oracle, what do you think of our current proposed approach of simply having a bounded exit rate of N per period, so the weak subjectivity bound (which is already a synchrony assumption) becomes a more explicit synchrony assumption?

I guess you mean the one in [the proposal](https://github.com/ethereum/eth2.0-specs/issues/701) of CBCification of beacon chain?

Then, how are weights used in GHOST decided there?

---

**nrryuya** (2019-04-01):

The *on-chain finalization* in my proposal might incentivize forming a cartel of 1/3 weight by ratio to stop validator rotation, although the finality of a block is still subjective.

---

**vbuterin** (2019-04-01):

> Then, how are weights used in GHOST decided there?

Exactly the way that you suggest: you choose between children of a block B by using the weights in the state of the block B.

> The  on-chain finalization  in my proposal might incentivize forming a cartel of 1/3 weight by ratio to stop validator rotation, although the finality of a block is still subjective.

Right, this is what we are trying to prevent by making validator rotation be time-based only.

---

**nrryuya** (2019-04-01):

> Exactly the way that you suggest: you choose between children of a block B by using the weights in the state of the block B.

Then, I think it’s OK ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

Do you have any idea to recover if the protocol gets stuck? (inactivity leak?)

What I wanted to do here is to keep the fault tolerance as much as possible after some temporal liveness failure i.e. a situation in which small messages are generated to contribute to clique for blocks over a few epochs but a large number of validators (e.g. maximum allowed) exited. Adding in-protocol finality threshold (only for entry & exit) is a simple but dirty way for this.

Instead, I think we can have such an advantage by making the exit rate dynamic using some formula which depends on the progress of consensus.

How do you think?

---

**adiasg** (2019-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/nrryuya/48/1552_2.png) nrryuya:

> E.g. Modify LMD GHOST to score a block b by Weight(b) in the “best children selection”.

It becomes very costly to execute this in each step of the fork choice. Some clever tricks mentioned here (“Dynamic validator sets”, [What CBCifying the beacon chain might look like · Issue #433 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/eth2.0-specs/issues/433)) can be used to increase fork choice efficiency!

