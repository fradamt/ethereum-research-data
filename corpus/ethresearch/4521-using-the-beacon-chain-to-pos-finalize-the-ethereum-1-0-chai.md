---
source: ethresearch
topic_id: 4521
title: Using the Beacon chain to POS-finalize the Ethereum 1.0 chain
author: josojo
date: "2018-12-09"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/using-the-beacon-chain-to-pos-finalize-the-ethereum-1-0-chain/4521
views: 7735
likes: 9
posts_count: 11
---

# Using the Beacon chain to POS-finalize the Ethereum 1.0 chain

Initially, the plan for Ethereum was to use a Casper staking mechanism on top of the pow Ethereum chain.

This plan was abandoned because we wanted to focus on developing the Beacon chain. Now, reading the new Beacon chain spec, I think that only small changes would be needed to use the Beacon chain for introducing  POS-finalization also on top of our current pow Ethereum 1.0 chain.

We could use the  Casper staking mechanism of the Beacon chain to POS-finalize the Beacon chain **AND the Ethereum 1.0 chain**. This would give the Ethereum 1.0 chain more security, while we are developing proper shards for our Beacon chain in the coming years.

In this thread, I would like to discuss the technical feasibility of POS introduction.

**Current eth2.0 spec:**

In the current eth2.0-specs, we have a one-way connection between the Beacon chain and our current Ethereum 1.0 chain.

Basically, the Beacon state is aware of the last processed receipt root of the Ethereum 1.0 chain:  `processed_pow_receipt_root` and possible new candidates of pow receipts: `candidate_pow_receipt_roots`. The Beacon chain needs to be aware of them, in order to make sure that the deposits into to Beacon chain are credited.

If half of the block proposers of the Beacon chain voted for one ‘candidate_pow_receipt_roots’, this candidate will be incorporated and all deposits will be credited:

> Set  state.processed_pow_receipt_root = x.receipt_root  if  x.votes * 2 > POW_RECEIPT_ROOT_VOTING_PERIOD  for some  x  in  state.candidate_pow_receipt_root

**Idea:**

In the Beacon chain, we are referencing to “old” Ethereum 1.0 blocks. If blocks of the Beacon chain are finalized, then also the old Ethereum 1.0 blocks from within the references, would be finalized. That means that no reorgs deeper than the last finalized Ethereum 1.0 block is allowed.

**Specification details:**

See here for the more recent [proposal](https://ethresear.ch/t/using-the-beacon-chain-to-pos-finalize-the-ethereum-1-0-chain/4521/10).

**
Old initial idea**

Only slight details of the current eth2.0 -spec beacon chain would need to be changed. These changes are:

- The Beacon chain state should be aware of the last POS-finalized block of the Ethereum 1.0 chain.
- New Beacon chain blocks are only processed by the Beacon chain clients if the new Beacon block also refers to an Ethereum 1.0 block, which is a child of the POS-finalized block. More specifically, each new Beacon block in the cycle x should refer to the Ethereum 1.0 block, which was minted during the Beacon cycle x-50 (that should be roughly 4x6x50 blocks in the past) and has the highest timestamp and is a child of the last finalized block.
- At the end of each Beacon cycle, any new finalization on the Beacon chain, where the old justified block and the new justified block both reference to Ethereum 1.0 blocks on the same branch ( new justified block must refer to a child block of the referred block in the old justified block),  will also set a finalization of the Ethereum 1.0 chain. The Ethereum 1.0 block, which was referenced in the new finalized Beacon block, will be the new finalized block.
If we are getting a new finalization on the Beacon chain, where the old justified block and the new justified block do not reference to blocks on the same branch, we will not do any finalization of Ethereum 1.0 blocks in this cycle.

Deposits from the Ethereum 1.0 chain into the Beacon chain would be handled similarly as in the current spec, only the point of time would be different: It would happen, if there is a new finalized Ethereum 1.0 block.

Alternatively, one could also dedicate one shard id to the Ethereum 1.0 chain and use crosslinks for the finalization of the Ethereum 1.0 chain.

The changes for the Ethereum 1.0 chain clients would be also very minor. We would just need to make them aware of the happening of the Beacon chain and do not allow any reorgs deeper than the finalized block.

## Replies

**MaverickChow** (2018-12-10):

One thing I am still unsure is whether ETH from address of Ethereum 1.0 in cold storage will need to be transferred to a new address of Ethereum 2.0 to remain valid.

---

**benjaminion** (2018-12-10):

Something along these lines was in the beacon chain spec until about two months ago: see [this version](https://github.com/ethereum/eth2.0-specs/blob/a2ad4bf6d5916b37e53dd2e7e65cdbb199f333f3/specs/casper_sharding_v2.1.md#pow-main-chain-changes) from October 3rd, second bullet point:

> PoW Main chain clients will implement a method, prioritize(block_hash, value). If the block is available and has been verified, this method sets its score to the given value, and recursively adjusts the scores of all descendants. This allows the PoS beacon chain’s finality gadget to also implicitly finalize PoW main chain blocks. Note that implementing this into the PoW client is a change to the PoW fork choice rule so is a sort of fork.

I can’t find the commit that removed it, but it’s presumably because it doesn’t belong in the beacon chain spec, rather an EIP somewhere.

---

**josojo** (2018-12-10):

[@benjaminion](/u/benjaminion)  thanks for this info.

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminion/48/612_2.png) benjaminion:

> I can’t find the commit that removed it, but it’s presumably because it doesn’t belong in the beacon chain spec, rather an EIP somewhere.

Yeah, this makes sense. I can understand the effort to keep the Beacon chain spec as pure as possible.

However, it would be great, if someone could shed some light into what exactly is planned regarding the finalization of the Ethereum 1.0 chain. We, as the community, would like to understand and give feedback on these solutions.

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> One thing I am still unsure is whether ETH from address of Ethereum 1.0 in cold storage will need to be transferred to a new address of Ethereum 2.0 to remain valid.

I think the Ethereum 1.0 chain will stay alive for quite a long time. So we do not have to be worried about transferring any eth soon. And in this transfer process, it will not make a difference whether the ETH is in cold storage or not.

---

**MihailoBjelic** (2018-12-14):

Interesting idea, thanks for posting.

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> The changes for the Ethereum 1.0 chain clients would be also very minor. We would just need to make them aware of the happening of the Beacon chain and do not allow any reorgs deeper than the finalized block.

Are these changes really minor?

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> It is meant to be a start for a discussion, as this could speed up the introduction of POS and thereby reduce inflation.
> I have several friends, which are concerned that the funding of their research/development can no longer be provided, in this context of crashing markets and high inflation.

IMHO reduced inflation can do very little to recover prices, there’s an extremely week correlation between these two things, at least ATM.

---

**DennisPeterson** (2018-12-15):

I agree that issuance isn’t a major factor for the price, but another consideration is that if we can use the beacon chain to reduce issuance on the PoW chain without losing security, we reduce our climate impact significantly.

---

**MihailoBjelic** (2018-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/dennispeterson/48/1675_2.png) DennisPeterson:

> another consideration is that if we can use the beacon chain to reduce issuance on the PoW chain without losing security, we reduce our climate impact significantly

This is true, of course.

---

**AlexeyAkhunov** (2018-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/dennispeterson/48/1675_2.png) DennisPeterson:

> if we can use the beacon chain to reduce issuance on the PoW chain without losing security, we reduce our climate impact significantly.

True. Another consideration - with finality gadget like that, would it be possible to not play whack-a-mole game with ASIC manufacturers? Or is it still going to be a problem?

---

**josojo** (2018-12-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> The changes for the Ethereum 1.0 chain clients would be also very minor. We would just need to make them aware of the happening of the Beacon chain and do not allow any reorgs deeper than the finalized block.

Are these changes really minor?

I would really call these changes minor. It’s even just a soft fork if block rewards would not be touched. If the code for the Beacon chain is finished, then it’s just modifying the fork choice rules.

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> if we can use the beacon chain to reduce issuance on the PoW chain without losing security, we reduce our climate impact significantly.

True. Another consideration - with finality gadget like that, would it be possible to not play whack-a-mole game with ASIC manufacturers? Or is it still going to be a problem?

Good question.

If there is much less money to be made from mining, then also, in general, the market demand for newer chips is lower. Hence, it will be less profitable to develop new and more efficient hardware. But it’s hard to say, whether it will be still profitable enough for people to develop specialized chips.

I think the main benefit of switching to POS is the increased security for the Ethereum 1.0 chain. Look at the charts, the hash rate has already halved itself: [here](https://etherscan.io/chart/hashrate). And at the latest with the next hard fork, there is plenty of cheap hardware available. This decreased the theoretical-attack costs for POW chains.

With POS, we could increase the theoretical attack costs again.

---

**josojo** (2018-12-26):

Here is a much more educated proposal:

**Introduction:**

The attestation concepts for the shards from the ETH 2.0 spec can be used straightforward for an Ethereum 1.0 finalization. The main challenges are coming from the fact, that POW blocks are coming fairly irregularly compared to the POS blocks and the synchronization with the beacon “heartbeats” is not enforced.

**Concept:**

We define that the rotating attestation committee of the shard 0 will be responsible for the POS validation of the Ethereum 1.0 chain. All other shards 1-1023 will be used as real Ethereum 2.0 shards.

The attestation committee of this shard 0 will, exactly like the others, vote on cross-links for the shard and attestations for the Beacon chain.

We want to call an Ethereum 1.0 block `cross-linked` if the attestation committee generates a cross-link for this block, (i.e. 2/3 of the attestation committee voted for this block).

We also want to call an Ethereum 1.0 block `finalized`, if the block is `cross-linked` and the cross-link is included into a finalized Beacon chain block.

The beacon chain usually justifies/finalizes an `epoch_boundary_block`. We will call an Ethereum 1.0 block, `epoch_boundary_block`, if it is a most recent block in the POW chain before the Beacon-chain ‘epoch_boundary_block’ (We will compare it based on block timestamps). This will give us exactly one Ethereum 1.0 epoch_boundary_block per epoch of a beacon chain.

The honest majority of the attestation committee of the shard 0, will only attest to `epoch_boundary_blocks` of the Ethereum 1.0 chain. The votes of the committee do not touch the Ethereum 1.0 chain, they will just be posted into the Beacon chain, exactly as for the usual shard construction.

In order to have a smooth attestation process, the committee would vote on the `epoch_boundary_block` of the epoch e, if the Beacon chain is in the epoch e+1. This delay of one epoch (64*5sec), will give the Ethereum POW chain some time for stabilization.

Fork-choice rule for Ethereum 1.0:

Clients of Ethereum 1.0 would need to be aware of the leading Beacon chain block. From this leading Beacon chain block, they would read the leading `cross-linked` block for the shard 0. From this cross-linked block, they determine the tip of the chain exactly as today: the longest chain.

Because the Beacon chain will never reorg deeper than the last finalized block, also the Ethereum 1.0 chain will never reorg deeper than the last `finalized` Ethereum 1.0 block.

**Analysis**

Since we assume an honest 2/3 majority in the Beacon chain, we will have also an honest  2/3 majority in the attestation committee of shard 0 (with striking likelihood). Since the committee is honest they will not do any attestations of cross-links, which will cause deeper, unjustified reorgs, neither will they support special privately mined chains. Hence, the protocol is safe and add security compared to the normal POW security.

Also, since the attestation happens with a delay of one epoch (5-6 min), they will not be able to influence the tips of the POW chain and not be able to give some advantage to some miners.

**Implementations:**

Beacon chain:

In order to realize the above-mentioned concept, there are no changes required to the Beacon chain(phase 0) at all, (only phase 1 as described in “shard 0 client” later)

Ethereum 1.0 chain:

For the Ethereum 1.0 chain, only the fork-choice rule is affected. No other changes are required. For the fork-choice rule the Ethereum 1.0 client would have to talk to a Beacon chain client. Based on the data from the Beacon chain, the client would calculate the `epoch_boundary_blocks`, the `cross-linked` blocks and the `cross-linked-finalized` blocks. With this information, the new fork choice rule will be easy to follow.

Shard 0 client:

The shard 0 client implementation would contain logic for the attestation committee of shard 0. That means that this client would have to

- be aware of the Beacon chain and the Ethereum 1.0 chain,
- calculate the epoch_boundary_blocks, the cross-linked blocks and the cross-linked-finalized blocks
- based on these blocks send out the attestation for the right epoch_boundary_block of the Ethereum 1.0 chain for the validators at the right slots.

And that’s it already! Hope to get some feedback and questions.

---

**DennisPeterson** (2019-03-17):

Since `BeaconBlockBody` includes `eth1_data` which has a blockhash, how is it even possible for the beacon chain to have finality if Eth1 doesn’t share in that finality? If a finalized beacon block points to an Eth1 block that reverts, what then?

Edit: someone on gitter told me the beacon chain will pull from blocks far behind current, to minimize the chance of this happening until 1.0 has finality. If there’s a major attack so it does happen, the beacon chain will be manually adjusted. (Thanks DR.)

