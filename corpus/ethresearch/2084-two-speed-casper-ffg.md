---
source: ethresearch
topic_id: 2084
title: Two-speed Casper FFG
author: vbuterin
date: "2018-05-29"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/two-speed-casper-ffg/2084
views: 5387
likes: 2
posts_count: 4
---

# Two-speed Casper FFG

Suppose that we have an on-chain Casper FFG cycle, which we absolutely want to confirm, and which we want the chain to be aware of, but this cycle would take a much longer time than we find acceptable because of [overhead/finality time/decentralization tradeoffs](https://medium.com/@VitalikButerin/parametrizing-casper-the-decentralization-finality-time-overhead-tradeoff-3f2011672735). For example, suppose that we have 32 ETH validator slots, with 10,000,000 ETH validating in total; this would entail 312500 validator entries, which at an overhead of 4 tx/sec would take nearly a day to go through.

We can achieve much faster finality time, in the optimistic case, in practice, as follows. In addition to on-chain Casper FFG messages, validators are free to make off-chain Casper FFG messages. There are two layers of checkpoints: *slow checkpoints* (blocks that appear at 1-day intervals) and *fast checkpoints* (blocks that appear at 1-minute intervals). An on-chain Casper FFG message contains a (target epoch, checkpoint hash, source epoch) tuple that can only refer to slow checkpoints and slow epochs (ie. in this example, multiples of 1440). An off-chain Casper FFG message contains such a tuple (target_epoch, checkpoint_hash, slow_checkpoint_hash, source_epoch, slow_source_epoch). The slow_checkpoint_hash is the hash at the start of the slow epoch in which the off-chain Casper FFG message is made. source_epoch is the most recent off-chain-justified epoch, and slow_source_epoch is the most recent on-chain-justified-epoch. A justification chain for off-chain blocks can contain on-chain justifications.

We define new slashing conditions:

- No-contradiction: all votes made within one epoch, including on-chain and off-chain, must use the same slow_checkpoint_hash and slow_source_epoch.
- Restricted no-surround, part 1: if an off-chain vote has source epoch o1, target o2 and an on-chain vote source c1, target c2, then it cannot be the case that o1  C2 and source epoch < C2, where the target is not a descendant of C2. This violates restricted no-surround, part 2.

**Plausible liveness proof**: honest validators can always make an on-chain vote with source epoch equal to the most recent known justified slow checkpoint and a target which is a descendant of the most recent known justified fast checkpoint (these must be compatible, because otherwise the fast checkpoint’s justification chain would either intersect the slow chain’s slow epoch, violating no-contradiction, or skip over it, violating restricted no-surround part 1). Once the target is justified, they can then off-chain or on-chain finalize it.

**Fork choice rule**: build on the chain with the highest known justified epoch (could be justified off-chain).

### Incentivization

A simple way to incentivize publishing off-chain votes would be to allow all on-chain votes to include a CAS of off-chain votes randomly selected validators. Those votes would later be randomly sampled, allowing the CAS provider to submit a merkle proof at which point the CAS provider and vote signer would both be rewarded.

### Light-client verification

Clients could try to download all off-chain messages directly, but this is expensive. They could also use one or more heuristics:

1. Check that there are CASes that sign for enough off-chain votes. Assuming most validators are honest, these are expensive to spoof.
2. Randomly select 500 indices, and download the votes for those indices. Accept a checkpoint as justified if a supermajority of those indices return valid votes that justify the checkpoint.

## Replies

**djrtwo** (2018-05-29):

I think on-chain and off-chain vote messages can have the same fields – `(target epoch, checkpoint hash, source epoch)` – with the condition that only votes referencing slow target epochs and slow source epochs can be included in the chain. This would simplify the protocol to one message type. If we needed a quick check other than checking `target_epoch % SLOW_EPOCH_LENGTH == 0 and source_epoch % SLOW_EPOCH_LENGTH` we could add a `on-chain` bit flag.

The proposed off-chain vote message tuple – `(target_epoch, checkpoint_hash, slow_checkpoint_hash, source_epoch, slow_source_epoch)` – has additional fields `slow_checkpoint_hash` and `slow_source_epoch`, but both of these can be ascertained via the other fields. `slow_checkpoint_hash` is just the hash at the start of the slow epoch that is defined by `target_epoch`/`checkpoint_hash`. `slow_source_epoch` is just the most recent on-chain-justified-epoch which can easily be stored by the contract or protocol (like in the current FFG contract).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> No-contradiction: all votes made within one epoch…

Should read:

> No-contradiction: all votes made within one slow epoch…

---

**djrtwo** (2018-05-29):

I’m trying to understand some potential scenarios. Let’s assume we have the following **actors** and *goals*:

1. Validator: Vote on-chain with the super majority to maximize vote rewards
2. Block producer: Create a block that will be included in the finalized/canonical chain to maximize issuance rewards and/or tx fees
3. Crypto exchange: Confirm (finalize) a user’s deposit quickly so that they can begin trading
4. Smart Contract: Observe that something on chain has been finalized so that a withdrawal (or some other action) can occur

For scenario (1), early finalization off-chain actually would give the validator a chance to submit a vote on-chain for a checkpoint that they were certain would be finalized (if all the validators that participated off-chain participated on-chain for that slow epoch). They would need to follow and participate in the off-chain finalization to get this leg up and any rewards from off-chain finalization

For scenario (2), block producers do not really get any more information to maximize their profits other than just following the fork choice. To ensure that they are building a block on the most likely canonical chain, they would probably follow the off-chain finalization rather than just the probabilistic heuristics.

For scenario (3), a crypto exchange seeking fast finalization times could probably just follow the probabilistic heuristics rather than needing to follow the intensive off-chain voting.

For scenario (4), on-chain finalization to trigger conditionals in contracts would be only on the order of at best a day time interval. Not excellent, but I’m not sure what the scope and requirements of finalization in contracts are atm. Maybe contracts could even peak into the CASes to conclude on probabilistic finalization, but doing this on a per contract basis would be expensive at best.

Maybe the chain should employ some of the heuristics to provide probabilisticly finalized checkpoints on an interval of some fraction of a day to increase the usability of on-chain finalization. Say *every hour, the block could run some of the heuristics to update the likely hood of the off-chain finalization of some recent checkpoint*. Contracts and light-clients could then use this info as they please.

---

**vbuterin** (2018-05-30):

> To ensure that they are building a block on the most likely canonical chain, they would probably follow the off-chain finalization rather than just the probabilistic heuristics.

Unless the heuristics are good enough ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I think we can get them to the point where the gain from downloading every vote is not larger than the gain from personally validating every block and transaction in every shard.

> Smart Contract: Observe that something on chain has been finalized so that a withdrawal (or some other action) can occur

The “default” workflow would be to wait for a slow finality round. But we can have contracts in each shard where validators “bet” on what the state root is, and contracts could use that as a faster data source.

