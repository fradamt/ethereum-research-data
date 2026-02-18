---
source: ethresearch
topic_id: 22241
title: Liveness attack in Ethereum PoS protocol using RANDAO manipulation
author: mart1i1n
date: "2025-04-30"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/liveness-attack-in-ethereum-pos-protocol-using-randao-manipulation/22241
views: 538
likes: 1
posts_count: 4
---

# Liveness attack in Ethereum PoS protocol using RANDAO manipulation

# Abstract

We present a liveness attack on the Ethereum protocol that the adversary can build the canonical chain that includes only blocks from the adversary, which cause liveness failure. In the attack, the adversary can controls the proposer duty of each epoch by carefully constructing RANDAO.

# Details of attack

**Assumption.**

[![](https://ethresear.ch/uploads/default/optimized/3X/c/2/c222147828fbf630af2125c9c8dee4f46eddac82_2_690x114.jpeg)1972×328 69.2 KB](https://ethresear.ch/uploads/default/c222147828fbf630af2125c9c8dee4f46eddac82)

We assume that the epoch of latest justified checkpoint is epoch 0. The proposer in the first slot of epoch 1 and epoch 2 is Byzantine. The stake of adversary is one-third of the total stake. We assume the attestations from Byzantine validators are withheld and never broadcast.

**Epoch 1.**

[![](https://ethresear.ch/uploads/default/optimized/3X/e/a/ea7a88c590e7c87c8f48f1b4e48040e3bd46ae12_2_690x94.jpeg)2068×282 66.7 KB](https://ethresear.ch/uploads/default/ea7a88c590e7c87c8f48f1b4e48040e3bd46ae12)

1. At the first slot of epoch 1, the Byzantine proposer delays its block b_1 for 8 seconds. As a result, the target of the attestations from honest validators in the first slot is not b_1. All Byzantine attestors in the first slot vote for the delayed block b_1. As a result, the delayed block will not be reorganized by an honest validator even the honest reorg mechanism exists. In the rest slots of epoch 1, block b_1 is in the canonical chain. The target of the attestations from honest validators in the rest slots of epoch 1 is block b_1. As a results, the number of attestations from honest validators with the same target and source is least than two-thirds. This means, as the attestations from Byzantine attestors are all withheld, the canonical chain can includes enough attestations to justify epoch 1.
2. The blocks from adversary extends block b_1 and build a private chain. The private chain includes the attestations from honest attestors and Byzantine attestors. Therefore, once the private chain is released, the private chain can update justified epoch to epoch 1.

**Epoch 2.**

[![](https://ethresear.ch/uploads/default/optimized/3X/a/e/aec973c05d7c282cf5a80952dc329134bb98592c_2_690x109.jpeg)1978×315 76.3 KB](https://ethresear.ch/uploads/default/aec973c05d7c282cf5a80952dc329134bb98592c)

1. At the first slot of epoch 2, the adversary conducts the same actions as step 1 in epoch 1. As a result, the canonical chain can not includes enough attestations to justify epoch 2.
2. The blocks from adversary extends the private chain. Comparing with step 2 in epoch 1, the adversary carefully selects blocks from the adversary that extends the private chain. The RANDAO of the private chain at the end of epoch 2 must guarantee that the proposer in the first slot of epoch 4 is adversary. This is easy since there are \lfloor2^{32/3}\rfloor possible RANDAOs and the probability that the proposer in the first slot of epoch 4 is adversary is 1/3.

**Epoch 3.**

[![](https://ethresear.ch/uploads/default/optimized/3X/b/2/b2c13c937763eec8062035bb646a0dcd5252b5f9_2_689x91.jpeg)2388×315 96.8 KB](https://ethresear.ch/uploads/default/b2c13c937763eec8062035bb646a0dcd5252b5f9)

1. The blocks from adversary extends the private chain. The block selection rule is the same as step 2 in epoch 2.
2. At the beginning of the last slot, the adversary released the private chain. As the attestations from the honest attestors in the last slot of epoch 3 is not released, the canonical chain can not includes enough attestations to justify epoch 3. Therefore, the justified epoch in canonical chain is epoch 0. After the private chain is released, the epoch of latest justified checkpoint is updated to 1. According to the filtering rule, the canonical chain is pruned, and the private chain becomes the new canonical chain.

```python
  # The voting source should be either at the same height as the store's justified checkpoint or
  # not more than two epochs ago
  correct_justified = (
      store.justified_checkpoint.epoch == GENESIS_EPOCH
      or voting_source.epoch == store.justified_checkpoint.epoch
      or voting_source.epoch + 2 >= current_epoch
  )
```

**Epoch 4.**

[![](https://ethresear.ch/uploads/default/optimized/3X/f/7/f7ddfd0d3962dda9e333fa74d378dd8feed212ca_2_689x125.jpeg)2388×436 111 KB](https://ethresear.ch/uploads/default/f7ddfd0d3962dda9e333fa74d378dd8feed212ca)

The RANDAO of the private chain at the end of epoch 2 guarantees that the proposer in the first slot of epoch 4 is adversary. The adversary can conducts the same steps as epoch 1.

**Epoch 5.**

[![](https://ethresear.ch/uploads/default/optimized/3X/3/6/36e0f797f19c591638e6bf8deb475664208445a2_2_689x122.jpeg)2388×424 117 KB](https://ethresear.ch/uploads/default/36e0f797f19c591638e6bf8deb475664208445a2)

Same as epoch 4, the RANDAO of the private chain at the end of epoch 3 guarantees that the proposer in the first slot of epoch 5 is adversary. The adversary can conducts the same steps as epoch 2.

**Epoch 6…**

Repeat steps in epochs 3,4,5.

# Analysis

Once the attack starts, the adversary create a canonical chain that only includes the blocks from Byzantine validators. That means, the adversary can choose which transactions can be included in the canonical chain, which violates the liveness property.

# Mitigation

As the liveness attack is one kind of reorganization attack, the attack can be fully prevented using [AA](https://ethereum-magicians.org/t/new-eip-available-attestation-a-reorg-rresilient-solution-for-ethereum/23927), which is a reorg-resilient solution for Ethereum PoS. Our approach is accepted in USENIX Security 2025 ([eprint](https://eprint.iacr.org/2025/097.pdf)).

## Replies

**potuz** (2025-05-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/mart1i1n/48/14503_2.png) mart1i1n:

> As a result, the delayed block will not be reorganized by an honest validator even the honest reorg mechanism exists.

Why is this? under the honest reorg feature, validators do not reorg blocks at the boundary when they propose the first block of the epoch, but they are allowed to reorg the first block of the epoch. So b1 in the above scenario will most definitely be reorged by the chain.

---

**mart1i1n** (2025-06-01):

The proposer of block b_1, which is the first block of epoch 1, will not attempt to reorg the final block of the preceding epoch. The proposer just delays submitting block b_1, leading to the target of attestations in the first slot of epoch 1wrongly.

As you mentioned, this will make block b_1 be reorganized by an honest proposer. However, if the adversary attests to block b_1 and releases b_1 in time, block b_1 will not be reorganized anymore.

---

**mart1i1n** (2025-06-02):

After discussing with [@potuz](/u/potuz), we think the adversary delays its block for 4 seconds and broadcasts the attestations in the first slot immediately can prevent the block from honest reorg.

