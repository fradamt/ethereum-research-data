---
source: ethresearch
topic_id: 5275
title: "NightShade (was: Whale Fishing): a new NEAR sharding design"
author: AlexAtNear
date: "2019-04-09"
category: Sharding
tags: []
url: https://ethresear.ch/t/nightshade-was-whale-fishing-a-new-near-sharding-design/5275
views: 8031
likes: 4
posts_count: 12
---

# NightShade (was: Whale Fishing): a new NEAR sharding design

Here’s an overview of Near’s latest sharding design. We call it NightShade.

It’s very different from what Near was doing before, it’s more recent and thus not as well thought of yet, so some glaring holes might be present.

The goal of the design is to have a coherent approach with good data availability and atomicity guarantees, and a low chance of invalid state transition even with the adaptive adversary.

## Block production

The first role that exists in NightShade is block producers. There is a limited number of them, and for the simplicity of modeling we say that there are as many block producers as there are shards. Say there’s 100 of both.

Each block producer is assigned to several shards, say 4. Thus, each shard has 4 block producers assigned. Block producers assigned to a particular shard are known, and can somewhat easily be corrupted, by design. The block producers are assigned to the shard for one epoch, which let’s say is approximately one day long. How exactly block producers rotate between epochs is orthogonal to the design.

Instead of modeling the entire system as one beacon chain and several shard chains, we model it as a single blockchain, that we call the main chain, and the blocks in the main chain contain the transactions and the state of the entire system. However, nobody in the system ever observes the full block, instead only the header of the block is distributed, that contains the merkle root of the transactions in the block, and the merkle root of the state before the transactions were applied, as well as some consensus information.

We call the parts of the block that contain the actual transactions applied in each shard in a particular block chunks. Each block has one (or zero) chunk for each shard.

The block producers need to collectively reach the following goals:

1. Collectively produce blocks on the main chain;
2. Prevent forks;
3. Ensure that the state transition function is applied correctly;
4. Ensure that all the chunks are available for some time after the block is produced.

Note that since the block producers can be corrupted adaptively, they alone cannot ensure any of the security properties (2-4 above), and can stall the block production. We will address the security below, and will try to make the stalling economically unreasonable.

The way block production works is relatively simple from here. For each height h of the main chain and each shard exactly one block producer is responsible for producing the chunk for that shard at that height. The four block producers assigned to a particular shard for the epoch take turns producing chunks. Once a block for height h is produced, each block producer downloads the chunks for the all the shards they are assigned to in the epoch, update the local state, and then create a chunk for the shard they are responsible for at the height h+1.

[![image](https://lh5.googleusercontent.com/SfnbXnEwJ0J6xXEVqcAWOpKDZMhXl8LpHMnQzcZ6aAcXFuk0adu5P8Fa5guVdew4JnI-zs364hsmmv9-E7464zhzfiK69mKlG1JYlzzsZCXXhSw7TOR7j__gehz1k14zC2a6dV6Y)
1344×802](https://lh5.googleusercontent.com/SfnbXnEwJ0J6xXEVqcAWOpKDZMhXl8LpHMnQzcZ6aAcXFuk0adu5P8Fa5guVdew4JnI-zs364hsmmv9-E7464zhzfiK69mKlG1JYlzzsZCXXhSw7TOR7j__gehz1k14zC2a6dV6Y)

On the figure above each cell shows the shard for which the particular block producer produces a chunk at each height, covering the first 8 block producers with 4 block producers per shard.

## Data Availability

Once a particular block producer created a chunk, they create an erasure-coded version of it with (n, f+1) code where n=3f+1 is the total number of block producers. The block producer then distributes the erasure-coded parts one to each other block producer. This way, for as long as f+1 block producers are online and cooperate, any chunk can be reconstructed. This idea is also inspired by Polkadot design, though we omit the data availability game they have on top of this.

[![image](https://lh4.googleusercontent.com/4PZ1Dr7nHn-UXW7Ila5fKUFM_qEbviWtAZX-_IbNJCkDKRMXytwG4ILUqMYM-v7un5A3O32Bkq6jITu_onPlps_H7U1leh3Zd9VbWEz1RW3sHScYJUf826Dy_l3ED0gGJXkdY7o7)
998×646](https://lh4.googleusercontent.com/4PZ1Dr7nHn-UXW7Ila5fKUFM_qEbviWtAZX-_IbNJCkDKRMXytwG4ILUqMYM-v7un5A3O32Bkq6jITu_onPlps_H7U1leh3Zd9VbWEz1RW3sHScYJUf826Dy_l3ED0gGJXkdY7o7)

Once the chunks are created and distributed, the block producers need to collectively agree on what chunks are available and can be included into the block. This is done in the following way:

## Consensus

The block producers exchange messages with the shards for which they have their parts of the chunks. Assuming for simplicity that no block producer proposed multiple chunks (which is a slashable behavior), a block proposal is a bitmask of the shards for which the chunks to be included. A block proposal is only possible if there are 2f+1 block producers that indicated that they have the parts for such chunks. The reward for the block is quadratic in the number of shards included, and thus the block producers have a certain incentive to wait for more chunks to become available before moving to finalizing the block.

At some point each validator indicates that they wish to proceed to finalizing a block. Once 2f+1 wished to proceed, they collectively use arbitrary BFT consensus, without loss of generality Tendermint, to decide on the block, and collect a BLS signature on it.

## State Validity

To ensure the state validity, we introduce a second role, called Fishermen. Say there’s on the order of 1,000-10,000 fishermen. At the beginning of each epoch each fisherman is randomly assigned to some number of shards, say it is again 4. To get the assignment the fisherman runs a VRF at the beginning of the epoch to randomly sample exactly four shards.

Once the epoch starts, whenever a block is created, the fisherman downloads all the chunks for the shards they are assigned to (conveniently since the chunks are distributed in a form of erasure-coded parts, chunk fetching can be parallelized), and validates them. The fisherman also randomly selects one erasure-coded part for each shard they are not assigned to and fetches it as well.

Once chunks are downloaded and reconstructed, the fisherman validates all the chunks, and creates a message which is either “YAY” if all the parts for all the shards were successfully fetched, and all the chunks in the assigned shards were valid, or “NAY” if at least one action was not successful, with a proof (see about proofs below). The fisherman doesn’t reveal the message immediately, instead it commits to it within 10 blocks after the block being validated was produced, and reveals the message within 10 blocks after that.

[![image](https://lh6.googleusercontent.com/qBJCnoCQjm5FAfoXljJEmt8xzLa0dMw0v0mvrgMWsH2-58MYn2zFvSoRRdC70zjkB22f0CKHXD-C1uZaiC-mMl6yuEaahZ_9kiXTPcB_4QL36tNAR-zCyF1OUwmOftblLjgiXf0_)
1266×708](https://lh6.googleusercontent.com/qBJCnoCQjm5FAfoXljJEmt8xzLa0dMw0v0mvrgMWsH2-58MYn2zFvSoRRdC70zjkB22f0CKHXD-C1uZaiC-mMl6yuEaahZ_9kiXTPcB_4QL36tNAR-zCyF1OUwmOftblLjgiXf0_)

A nice property of this fisherman approach is that on the protocol level there’s someone who’s responsible to fish (so in a sense fisherman here is closer to a concept of a validator), which is different from common approach to fishing in which figuring out incentives for fishermen are not as easy.

The commit reveal scheme makes fishermen accountable. If fisherman A successfully fished, all the fishermen who committed to “YAY” will be slashed (and one must commit to something to get the reward).

Once a fisherman reveals a “NAY” message, they also reveal a proof of the invalid state transition (see below). Every block producer and fisherman needs to validate the proof. If the proof is wrong, the stake of the fisherman who produced it is slashed, and the system continues to operate.

If the proof is correct, every fisherman must reveal their bitmasks within the next 10 blocks, and any fisherman that fails to do so or reveals a bitmask and has the faulty shard assigned to them, but doesn’t reveal a corresponding “NAY” message, gets slashed. In this case the block producer and fishermen assignment is immediately redone. However, since it takes time to download the state for all actors involved, the system for some predefined time continues operation with the current assignments, effectively having lower security for some time (higher chance of adaptive corruption, since the fishermen are revealed).

The aftermath of a successful fishing attempt can be modeled as a fork, but we find it easier to think about it as the continuation of the same chain, but with the state transition of all the blocks from the block with the invalid state transition until the block with the successful fishing nullyfied.

## Aggregating Fisherman Messages

There are two big problems with 1,000+ fishermen attesting in this way to block validity: a) the blocks will need to include more than 1,000 commitments per block, which is rather expensive, and b) the blocks will either need to include 1,000 cheap signatures, or one BLS signature, but validating a 1,000-fold BLS signature is relatively expensive.

To get around this issue the following model is proposed: each fisherman is assigned to one block producer. There are no requirements on the assignment procedure (we compare two different models at the end), in particular the fishermen assigned to a particular block producer are not necessarily assigned to the same shards. The role of the block producer is then to perform the following protocol after each block is produced:

1. Collect commits and reveals from each fisherman;
2. Build a merkle tree of such commits and reveals;
3. For each fisherman, send them a merkle root and the merkle proof of inclusion of that fisherman’s commits and reveals in the tree;
4. Collect a BLS signature part from each fisherman on the merkle tree root;
5. Include the BLS multisig from assigned fishermen and the merkle root into the block.

Ultimately the block producers choose a sample of other block producers to validate the multisigs from their fishermen, and only sign on the final block if for the sample they verified the multisigs were correct. A particular node that replays the block then can only validate the signature on the block from block producers, and assume that unless a very large percentage of the block producers colluded, the signatures from the fishermen were correct (they can still opt to validate the signatures themselves). Fishermen in consecutive blocks also validate a subset of multisigs of fishermen from the previous block, and if such a signature was faked, within few blocks the majority of fishermen will stop signing the blocks.

A block producer can censor messages from a validator, which we analyze below when we talk about approaches to assigning them. Ultimately the only message that we absolutely cannot lost is a message with a fishing attempt. Such a message is the only message that a fisherman can submit through any block producer. If other messages get censored, the fisherman either chooses to work with another block producer, or waits until the rotation, depending on how they are assigned.

## Proofs

**Invalid state transition.** A simple way to model it is to force block producers to include a hash of the state after every consecutive segment of transactions that collectively read or write more than 100Mb of state. Then to prove that there was an invalid state transition the fisherman needs to provide two consecutive state hashes, transactions in between, and 100Mb of data that is affected with the Merkle proofs, which is sufficient to prove that the state transition was applied incorrectly.

**Data unavailability.** To prove that a particular part of erasure coded state is not available, a participant can send a special kind of request to other participants asking if they can fetch the part. If they can, they return the part, otherwise they return a BLS signature part attesting that they also failed to retrieve the part. A BLS multisig with a large percentage of a stake is a meaningful proof that a part is unavailable.

## Fork Choice Rule

Forks shall be unlikely, since the block producers do a BFT consensus on each block. In case a fork occurs, the fork choice rule must favor blocks that have most of the stake from both block producers and fishermen staked on them.

An example fork choice rule that seems to work is to use LMD GHOST that accounts for signatures from both the block producers and fishermen, and slash for signing two conflicting blocks for the same height.

## Approaches to assigning Fishermen to Block Producers

We compare two ways to assign fishermen to block producers, and sampling the block producers.

The first approach is for block producers to choose their fishermen, and the 100 block producers with the highest accumulated stake (the stake of the block producer and all the assigned fishermen) will be the block producers. Such block producers naturally won’t rotate frequently, which creates certain centralization concerns. However, since to become one of the hundred one needs to sign up participants with a lot of accumulated value, it seems reasonable to assume that any honest fisherman with sufficient stake shall be able to convince at least one of the 100 current block producers to include them.

The second approach is for block producers and fishermen to be sampled from a large set of participants wishing to participate in network maintenance, and assign fishermen to block producers randomly.

In the former approach if a block producer doesn’t include fisherman’s messages, or the link between them is slow and the fisherman delays the block production, both the block producer and the fisherman can in their sole discretion break their relationship, and the fisherman can go to another block producer. Since the block producer gets a percentage of rewards from their fishermen, this shall end up in an equilibrium in which each block producer ensured high uptime and good link to their fishermen.

In the latter this property will not hold, but the assignment of fishermen to block producers can be reshuffled relatively frequently, and thus censoring fishermen shall not be a big problem.

## What’s good about it

This approach has several positive properties:

1. Adaptive corruption is extremely complex. To carry out an invalid state transition, the adversary needs to identify the fishermen assigned to a particular shard (for which the only feasible approach appears to be to provide them provable payout exceeding their stakes for YAY-ing an invalid block on another blockchain), and succeed in corrupting each and every one of them, which is significantly more unlikely than corrupting a subset of the validators.
2. For as long as 2f+1 block producers are not intentionally attempting to stall a shard, the data availability story is very good.
3. For as long as at least one fisherman performs their duties, the cross-shard transactions are atomic (in the sense that if an invalid state transition is detected, or the main chain reorgs, it will never be the case that only half of a cross-shard transaction is finalized).

Feedback and brainstorming are highly appreciated!

## Replies

**musalbas** (2019-04-09):

I believe the data availability scheme can be simplified as a sampling-based erasure coding scheme, but where each node in a shard samples a sufficient number of chunks from every other shard, such that if there is an honest majority of nodes in their own shard, they can reconstruct the blocks of the other shards, otherwise the unavailable blocks of other shards will be rejected. I don’t think you need to have a single chain for this; you can also do this with multiple shardchains, where shards download the Merkle roots of other shards. I had a similar idea that was omitted from the fraud proofs paper to use this to complement light clients sampling chunks, so I think it can work, however you still need light clients that aren’t part of shards to sample chunks too, otherwise you’d get a weakened threat model.

This is because while such a scheme prevents a single shard from injecting invalid state if that shard has a dishonest majority, it would still be possible for a network-wide dishonest majority to inject invalid state to the network if they don’t follow the data availability scheme, that every other node will then accept, so light clients should be sampling chunks too. I therefore would be careful with applying concepts from heterogeneous sharded systems to homogeneous sharded systems, considering they have different threat models (heterogeneous systems tend to have weaker “on-chain” threat models than homogeneous systems, but have higher scalability as arbitrary numbers of shards are allowed).

You can also extend this idea further by making it so that consensus nodes in shards sample a number of chunks that is proportional to the amount of stake they have, so that the more stake they have, the most chunks they are expected to download.

> Data unavailability.  To prove that a particular part of erasure coded state is not available, a participant can send a special kind of request to other participants asking if they can fetch the part. If they can, they return the part, otherwise they return a BLS signature part attesting that they also failed to retrieve the part. A BLS multisig with a large percentage of a stake is a meaningful proof that a part is unavailable.

This seems vulnerable to the [fisherman’s dilemma](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding). In general you can’t prove the unavailability of data as not publishing data is not a uniquely attributable fault; however you can prove to yourself the *availability* of data, hence why light clients should be sampling chunks too.

As for the fisherman part of the story, I’m not convinced that the “at least one fisherman should be honest” assumption holds true, unless I’m missing something. You state that fishermen are randomly assigned to shards or chunks from some set of fishermen, so that each chunk has some smaller set of fishermen attached to it. If some of these fishermen are malicious, it thus seems possible that all of the fisherman randomly assigned to a chunk could be malicious. So it seems to me that the assumption would actually be at least one fisherman *per chunk* is honest, rather than one fisherman in the whole system, which is a much less secure assumption. That means in the whole system you’d actually need the majority of fishermen to be honest to have a very low probability of having a chunk that has only malicious fishermen.

IMO if you want to incentivise fraud proof generators/fishermen, a simpler but more effective way to do it would be to allow *anyone* to generate fraud proofs, but require block producers to deposit some amount of coins that could be rewarded to anyone who submits a valid fraud proof of that block within a certain amount of time (similar to Truebit). Either way, I don’t think incentivising fraud proof generators is a big concern considering you only need one honest fraud proof generator in the entire network. I think incentivisation issues in such protocols are usually an issue when you need to make sure that the majority of people behave a certain way, rather than that assuming that there will be one person who will behave in a certain way.

I suppose you could combine the two in some way: you can have some set of nodes that are explicitly responsible for generating fraud proofs for certain shards, and are punished if they don’t, but also allow any third party participant to submit valid fraud proofs (e.g. you don’t need permission to submit a fraud proof)?

---

**AlexAtNear** (2019-04-09):

[@musalbas](/u/musalbas) thanks a lot for feedback!

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> As for the fisherman part of the story, I’m not convinced that the “at least one fisherman should be honest” assumption holds true, unless I’m missing something. You state that fishermen are randomly assigned to shards or chunks from some set of fishermen, so that each chunk has some smaller set of fishermen attached to it. If some of these fishermen are malicious, it thus seems possible that all of the fisherman randomly assigned to a chunk could be malicious. So it seems to me that the assumption would actually be at least one fisherman per chunk is honest, rather than one fisherman in the whole system, which is a much less secure assumption. That means in the whole system you’d actually need the majority of fishermen to be honest to have a very low probability of having a chunk that has only malicious fishermen.

Yes, the assumption is that every shard has at least one honest fisherman assigned to it.

So the parameters need to be chosen to make it not being the case infeasible. I.e. if you assume that the total population of validators has 66% of malicious actors, you assign 100 fishermen per shard, it makes a chance of a single shard to have all fishermen corrupted to be 6e-19, sufficiently unlikely. But if we are close to 66% corrupted we have bigger problems ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Similarly, if you assume it’s 33%, you assign 40 fishermen per shard, and get 5e-20 per shard (that is my example with 1,000 fisherman, 100 shards, and 4 shards per fisherman).

That’s the analysis without the adaptive adversary.

> Either way, I don’t think incentivising fraud proof generators is a big concern considering you only need one honest fraud proof generator in the entire network.

One per shard, not one in the entire network, moreover if you only care about a particular shard (say the contract you use is on shard 2), your security still depends on someone fishing in all the shards, since the invalid state transition might occur in another shard, and then be transferred to shard 2 via a cross-shard communication.

> This seems vulnerable to the fisherman’s dilemma.

Agree, seems like almost any data unavailability proof would be susceptible to it, right? So it is more of an “argument” of unavailability.

> This is because while such a scheme prevents a single shard from injecting invalid state if that shard has a dishonest majority, it would still be possible for a network-wide dishonest majority to inject invalid state to the network if they don’t follow the data availability scheme

50%+ of total stake corrupted can create arbitrary reorgs, against which you can only defend if you are constantly online, so I think defending from invalid state transitions or blocks withholding in such a scenario is not as important.

---

**musalbas** (2019-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexatnear/48/2390_2.png) AlexAtNear:

> So the parameters need to be chosen to make it not being the case infeasible. I.e. if you assume that the total population of validators has 66% of malicious actors, you assign 100 fishermen per shard, it makes a chance of a single shard to have all fishermen corrupted to be 6e-19, sufficiently unlikely. But if we are close to 66% corrupted we have bigger problems

Right, but you can’t make any assumptions about the number of fishermen, just the % of honest fishermen, because these fishermen need to be chosen from a Sybil-resistant set, otherwise they might all be malicious fishermen (e.g. you can’t distinguish 100 fishermen from 1 fisherman pretending to be 100 fishermen.) So if there are only 50 actual fishermen for example, it’s probable that every fisherman will be assigned to every shard. It seems likely given if you look at staking/mining distributions, staking/mining pools control the majority of stake/hash power.

This isn’t a problem per se since the assumption about % of honest actors rather than # of honest actors (except that you’re going to have to assume that these fishermen will actually fish every shard); however if you at least allow anyone to submit a fraud proof you can at least eliminate the Sybil-resistance assumptions at no extra cost, while still having some set of accountable nodes that can be punished if they don’t fish.

> Agree, seems like almost any data unavailability proof would be susceptible to it, right? So it is more of an “argument” of unavailability.

Yes, that’s why you can use a data availability proof system rather than unavailability proof system, and let all nodes sample chunks to prove to themselves that data is available. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> 50%+ of total stake corrupted can create arbitrary reorgs, against which you can only defend if you are constantly online, so I think defending from invalid state transitions or blocks withholding in such a scenario is not as important.

It’s very important because in non-sharded blockchain systems, honest-majority assumptions are indeed used to prevent reorgs that double spend coins. However, they don’t rely on honest-majority assumptions to prevent invalid state transitions, because full nodes validate state transitions. But if you can suddenly create invalid state transitions to do things like the generate lots of money out of thin air, then the benefit of doing a reorg is *much* more profitable. Whereas in non-sharded systems where the worst thing you can do with a reorg is double spend some coins, doing a reorg is not really worth it - but if you can generate lots of money out of thin air - it suddenly becomes a lot more worth it. This IMO is a primary challenge of securing sharded blockchains: preventing injecting invalid state transitions without relying on an honest majority. However if you just added a rule so that nodes that aren’t in shards sample chunks too, then it wouldn’t be a problem. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**AlexAtNear** (2019-04-09):

> because these fishermen need to be chosen from a Sybil-resistant set

Not sure if it was obvious from the description, but fishermen have stakes in the proposed design. So they are sampled from a sybil resistant set.

Also agree that the protocol shall not forbid external fishing. But I find having hidden fishermen that will be slashed if they fail to fish to certainly add extra security. With them we rely on neither the fact that the publicly known validators won’t be corrupted, nor that there’s at least one person per shard voluntarily fishing.

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> This IMO is a primary challenge of securing sharded blockchains: preventing injecting invalid state transitions without relying on an honest majority. However if you just added a rule so that nodes that aren’t in shards sample chunks too, then it wouldn’t be a problem.

I might be forgetting some important part of the fraud proofs construction, but how sampling random fragments helps against invalid state transitions? Seems like the nodes that aren’t in shards will have some certainty that the data is available, but not that the state transition is valid?

---

**zmanian** (2019-04-10):

One idea I have to incentivizing fisherman liveness.

Require the fishermen to generate claim rewards if (VRF(block execution transcript hash)) is below some threshold.

This would incentivize fishermen to actually execute blocks to claim the reward instead of this gameable fake block mechanism.

---

**musalbas** (2019-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexatnear/48/2390_2.png) AlexAtNear:

> I might be forgetting some important part of the fraud proofs construction, but how sampling random fragments helps against invalid state transitions? Seems like the nodes that aren’t in shards will have some certainty that the data is available, but not that the state transition is valid?

Because fishermen can only generate invalid state transition fraud proofs if the data they need to generate them is available. Otherwise a block producer can put an invalid state commitment in a block header (e.g. state root) and tell clients (and other shards) that the shard is in a certain state, but no one can prove that state commitment is invalid. I assume state commitments would be a primary way of knowing the state in a sharded system, since no client is expected to know the state of all shards. Because clients aren’t expected to validate data availability, this would be a perfectly acceptable block according to the block validity rules.

---

**dlubarov** (2019-04-10):

If an honest fisherman was collecting signatures for an unavailability proof, would he collect signatures from the entire fisherman pool, or just his shard?

If it’s just his shard, then the “one honest fisherman per shard” assumption seems insufficient. There would always be an honest fisherman to attempt an unavailability proof, but there might be no honest peers to corroborate it.

If it’s the entire pool, then it seems like performance could degrade to full replication in a worst case scenario, if (potentially malicious) fishermen were building (potentially specious) unavailability proofs for all chunks at the same time.

---

**AlexAtNear** (2019-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/zmanian/48/208_2.png) zmanian:

> Require the fishermen to generate claim rewards if (VRF(block execution transcript hash)) is below some threshold.

Then a dishonest fisherman can monitor the network to see reward claims, extract the execution transcript hash from them, and compute their VRF, right?

I guess not a huge problem if the threshold is configured to have valid claims occur relatively infrequently, making such copy-catting not very profitable.

Cool idea overall, will think more about it

---

**AlexAtNear** (2019-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> Because fishermen can only generate invalid state transition fraud proofs if the data they need to generate them is available. Otherwise a block producer can put an invalid state commitment in a block header (e.g. state root) and tell clients (and other shards) that the shard is in a certain state, but no one can prove that state commitment is invalid. I assume state commitments would be a primary way of knowing the state in a sharded system, since no client is expected to know the state of all shards. Because clients aren’t expected to validate data availability, this would be a perfectly acceptable block according to the block validity rules.

Ok, then I understand it right.

“I assume state commitments would be a primary way of knowing the state in a sharded system” .

So say the full nodes have a dishonest majority, and produce a block with an invalid state transition. In the models that you are thinking of that are resilient to dishonest majority say I’m a light client, and I’m sufficiently convinced that the data is available. What makes me convinced that someone have actually reconstructed the block and ensured the state validity? Without having dedicated fishermen (who can also be corrupted) is the expectation that there’s at least one honest participant sufficiently caring about the health of each shard to validate it?

Also, the dishonest majority can never include the proof of invalid state transition into the block, so such a proof needs to be distributed via some other channel I assume?

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> If an honest fisherman was collecting signatures for an unavailability proof, would he collect signatures from the entire fisherman pool, or just his shard?
>
>
> If it’s just his shard, then the “one honest fisherman per shard” assumption seems insufficient. There would always be an honest fisherman to attempt an unavailability proof, but there might be no honest peers to corroborate it.
>
>
> If it’s the entire pool, then it seems like performance could degrade to full replication in a worst case scenario, if (potentially malicious) fishermen were building (potentially specious) unavailability proofs for all chunks at the same time.

What to do if the data is actually unavailable is not that well thought yet. My current thinking is the following:

A fisherman assigned to a shard must reconstruct a block in such shard. The problem is what to do if they can’t. That immediately implies that more than 1/3 of block producers are not cooperating, and thus collecting any evidence is problematic. The best solution I have is for a fisherman who can’t reconstruct a block to immediately reveal their shards bitmask and resign, with an indication which shard was not reconstructable. Large number of such resignations is an indication of a problem.

The proof of unavailability that I provided in the first post actually doesn’t appear to be very helpful to me anymore, not sure what my initial thinking about it was ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) [@musalbas](/u/musalbas) is right that you can’t proof unavailablity of something.

---

**musalbas** (2019-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexatnear/48/2390_2.png) AlexAtNear:

> What makes me convinced that someone have actually reconstructed the block and ensured the state validity? Without having dedicated fishermen (who can also be corrupted) is the expectation that there’s at least one honest participant sufficiently caring about the health of each shard to validate it?

Yeah, basically light clients gossip shares to full nodes that are trying to reconstruct the block. It’s a bit like BitTorrent or a peer-to-peer filesharing network, you can ask other nodes for missing pieces in a file you’re trying to download.

![](https://ethresear.ch/user_avatar/ethresear.ch/alexatnear/48/2390_2.png) AlexAtNear:

> Also, the dishonest majority can never include the proof of invalid state transition into the block, so such a proof needs to be distributed via some other channel I assume?

The proof would be gossiped via the peer-to-peer network, it doesn’t need to be included on-chain unless you want to use it to slash someone.

---

**zmanian** (2019-04-10):

You are trying to combat the Fishermen senescence problem in your design with `YAY` votes and commit reveal.

I think you can better fix the problem with VRF mining and commit reveal. I think this make me not hate Fishermen as much.

