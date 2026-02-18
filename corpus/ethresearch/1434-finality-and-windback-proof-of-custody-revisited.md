---
source: ethresearch
topic_id: 1434
title: Finality and Windback - Proof of Custody Revisited
author: MaxC
date: "2018-03-19"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/finality-and-windback-proof-of-custody-revisited/1434
views: 2810
likes: 2
posts_count: 3
---

# Finality and Windback - Proof of Custody Revisited

**TL;DR** - If there is a way to finalise state execution on each shard,  we could  use proofs of custody to ensure collators check the availability for a period of wind-back shards.  Since cross-shard transactions are likely to require finalised state execution, it may be worth revisiting proofs of custody. The basic idea is to push availability checking to the state execution level as well.

Proofs of custody may be used even without finalised state execution-- so long as the slashing penalty is not too severe and collators lock funds on the appropriate shard chains – or alternatively we can simply use snarks/starks for fraud proofs.

A reminder of proof of custody schemes, similar to [Justin’s](https://ethresear.ch/t/enforcing-windback-validity-and-availability-and-a-proof-of-custody/949), but with extra padding:

1. When assigned to a shard, each collator commits to the SMC the hash of a random secret s.
2. Before adding a new header to the SMC, the collator computes \text{hash}[b||s]  for the last 25 blocks b, and includes the block numbers in the header. This is the challenge.
3. The collator reveals s, through  a transaction to the SMC, which enables people to verify the challenge.

**Slashing Conditions:**

If we discover a block for which \text{hash}[b||s] disagrees with the value in the collators header, we slash the collator. The question is how (I assume no starks for fraud proofs for security assumptions, **although I think starks would be a great solution**, since they could just be used for fraud proofs which there would be few of, given the incentive structure):

**With no execution-finalisation**, the collator posts a bond of X eth to the shard chain he is creating a header for, which he cannot spend for 50 blocks. In the event of an incorrect header, the executors adjust the collator’s balance to 0.

To preserve transaction ordering: each proposer can hash his proposals in the order given. If this hash does not match up with the ordering given by the collator, the collator gets slashed as above.

If any node discovers s before the block header is added to the SMC, they can submit s to the SMC to steal the collator’s deposit. This discourages outsourcing availability checking.

If there were a way of finalising  state execution, then collators could also be slashed at the SMC level for a higher deposit as soon as a fraud proof was generated (merkle state root with a special symbol for fraud F stored under the validator in a finalised block). The question is how finalisation occurs.

This scheme may create perverse incentives with executors blackmailing collators, but if we take the truebit philosophy seriously and 10% of executors are honest, and false claims are punished,  then it would be possible to push data availaibility checking to the execution layer.

## Replies

**MaxC** (2018-03-19):

Benefit of this method is checking whether a collator has checked for data availability can be done pretty much deterministically by anyone.

---

**jamesray1** (2018-04-10):

Interesting, so this proposal would abstract data availability checking, so you just have data! You would of course then need to have a spec and test suite for the execution layer to make sure that this scheme is followed for any EVM abstraction so that custom EVMs know what to make and how to test. A note for others: this scheme would work similar to [Truebit](https://people.cs.uchicago.edu/~teutsch/papers/truebit.pdf)’s interactive verification.

