---
source: ethresearch
topic_id: 23353
title: Unrealized manipulating attack
author: Mediabs2022
date: "2025-10-27"
category: Security
tags: []
url: https://ethresear.ch/t/unrealized-manipulating-attack/23353
views: 251
likes: 4
posts_count: 7
---

# Unrealized manipulating attack

# Unrealized manipulation attack

Building on the 3 kinds of one-epoch inactivation attack in [1] and collusive Byzantine strategies, we propose six new Unrealized manipulation attack strategies. These attacks exploit collusion among adversaries to keep the honest chain inactive, and then use a single adversarial block with sufficient votes to connect to an unrealized block and reorganize the honest blocks on the chain, causing losses to honest validators. The specific strategy below illustrates the idea:

### Strategy 1

[![un-1-exante+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/a/6/a65bbab4b111b4717bd95306aa81e4135e639beb_2_690x191.png)un-1-exante+sandwich.png1986×552 46.8 KB](https://ethresear.ch/uploads/default/a65bbab4b111b4717bd95306aa81e4135e639beb)

1. During epochs e and e\!+\!1, except for slot t and slot t\!+\!32, all Byzantine votes are collusively sent only to the final Byzantine proposer v_k in epoch e\!+\!1. This proposer does not continue to extend the current honest chain; instead, it sets the parent to be the first block in epoch e that contains 1/3 voting weight (the block proposed at slot t\!+\!18), and withholds releasing b_k.
2. Launch a sly-ex-ante attack against the honest validators in epoch e, and perform a single sly-sandwich attack against the honest validators in epoch e\!+\!1.
3. In epoch e\!+\!2, the Byzantine proposer at slot t\!+\!64 proposes b_{k2} with parent b_k, and releases b_k and b_{k2} simultaneously within the first 4 seconds so as to justify cp_e and roll back the honest branch.

### Strategy 2

[![un-2-exante+4s.png](https://ethresear.ch/uploads/default/optimized/3X/a/a/aaf3a0ef7877db9866595ef1c9aeba41bf3d9d2a_2_690x198.png)un-2-exante+4s.png1980×570 55.6 KB](https://ethresear.ch/uploads/default/aaf3a0ef7877db9866595ef1c9aeba41bf3d9d2a)

1. During epochs e and e+1, except for slot t, all Byzantine votes are collusively sent only to the final Byzantine proposer v_k in epoch e+1. This proposer does not continue to extend the current honest chain; instead, it sets the parent to be the first block in epoch e that contains 1/3 voting weight (the block proposed at slot t+18), and withholds releasing b_k.
2. Launch a sly-ex-ante attack against the honest validators in epoch e, and perform one sly-1/3-slot-withhold attack against the honest validators in epoch e+1.
3. In epoch e+2, the Byzantine proposer at slot t+64 proposes b_{k2} with parent b_k, and releases b_k and b_{k2} simultaneously within the first 4 seconds so as to justify cp_e and roll back the honest branch.

### Strategy 3

[![un-3-sandwich+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/3/4/34d078175aba24f1b91001e2cfaf9b4a75dc5354_2_690x173.png)un-3-sandwich+sandwich.png1896×477 48.9 KB](https://ethresear.ch/uploads/default/34d078175aba24f1b91001e2cfaf9b4a75dc5354)

1. During epochs e and e+1, except for slot t+32, all Byzantine votes are collusively sent only to the final Byzantine proposer v_k in epoch e+1. This proposer does not continue to extend the current honest chain; instead, it sets the parent to be the first block in epoch e that contains 1/3 voting weight (the block proposed at slot t+18), and withholds releasing b_k.
2. Launch a sly-sandwich attack against the honest validators in epoch e, and also launch a sly-sandwich attack against the honest validators in epoch e+1.
3. In epoch e+2, the Byzantine proposer at slot t+64 proposes b_{k2} with parent b_k, and releases b_k and b_{k2} simultaneously within the first 4 seconds so as to justify cp_e and roll back the honest branch.

### Strategy 4

[![un-4-sandwich+4s.png](https://ethresear.ch/uploads/default/optimized/3X/7/1/71d4cd38b8d6e025a562cbe5980fcd3cef38cbf2_2_690x165.png)un-4-sandwich+4s.png2016×484 51.9 KB](https://ethresear.ch/uploads/default/71d4cd38b8d6e025a562cbe5980fcd3cef38cbf2)

1. During epochs e and e+1, all Byzantine votes are collusively sent only to the final Byzantine proposer v_k in epoch e+1. This proposer does not continue to extend the current honest chain; instead, it sets the parent to be the first block in epoch e that contains 1/3 voting weight (the block proposed at slot t+18), and withholds releasing b_k.
2. Launch a sly-sandwich attack against the honest validators in epoch e, and launch a sly-1/3-slot-withhold attack against the honest validators in epoch e+1.
3. In epoch e+2, the Byzantine proposer at slot t+64 proposes b_{k2} with parent b_k, and releases b_k and b_{k2} simultaneously within the first 4 seconds so as to justify cp_e and roll back the honest branch.

### Strategy 5

[![un-5-4s+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/9/9/9946a206d5d106676d5c16d075fe9f99cfc32147_2_690x219.png)un-5-4s+sandwich.png1560×497 39.8 KB](https://ethresear.ch/uploads/default/9946a206d5d106676d5c16d075fe9f99cfc32147)

1. During epochs e and e+1, except for slot t+32, all Byzantine votes are collusively sent only to the Byzantine proposer v_k in the last slot of epoch e+1. This proposer does not continue to extend the current honest chain; instead, it sets the parent to be the first block in epoch e that contains 1/3 voting weight (the block proposed at slot t+18), and withholds releasing b_k.
2. Launch a sly-1/3-slot-withhold attack against the honest validators in epoch e, and launch a sly-sandwich attack against the honest validators in epoch e+1.
3. In epoch e+2, the Byzantine proposer at slot t+64 proposes b_{k2} with parent b_k, and releases b_k and b_{k2} simultaneously within the first 4 seconds so as to justify cp_e and roll back the honest branch.

### Strategy 6

[![un-6-4s+4s.png](https://ethresear.ch/uploads/default/optimized/3X/a/6/a6102700556c8f23a2768e0004e5c99b3099a6ae_2_690x180.png)un-6-4s+4s.png1496×392 35 KB](https://ethresear.ch/uploads/default/a6102700556c8f23a2768e0004e5c99b3099a6ae)

1. During epochs e and e+1, all Byzantine votes are collusively sent only to the Byzantine proposer v_k in the last slot of epoch e+1. This proposer does not continue to extend the current honest chain; instead, it sets the parent to be the first block in epoch e that contains 1/3 voting weight (the block proposed at slot t+18), and withholds releasing b_k.
2. Launch a sly-1/3-slot-withhold attack against the honest validators in epoch e, and also launch a sly-1/3-slot-withhold attack against the honest validators in epoch e+1.
3. In epoch e+2, the Byzantine proposer at slot t+64 proposes b_{k2} with parent b_k, and releases b_k and b_{k2} simultaneously within the first 4 seconds so as to justify cp_e and roll back the honest branch.

# Attack Extension Strategies

In fact, the six attack strategies we described above are only the most basic “take-what-you-get” strategies. In real attack scenarios, we can further leverage the three kinds of one-epoch inactivation attack in [1] to keep additional epochs inactive, thereby amplifying the attack. For example, for the six strategies above, if the proposer at slot t+64 is Byzantine; or if the proposer at slot t+64 is honest while the proposers at slots t+63 and t+62 are both Byzantine; or if the proposer at slot t+64 is honest while the proposers at slots t+63 and t+65 are Byzantine, then the adversaries can proceed to launch a third-stage one-epoch inactivation attack that causes epoch e+2 to become inactive. Immediately afterwards, the Byzantine proposer in the last slot of epoch e+2 can set as parent the first block in epoch e that contains \frac{1}{3} of the voting weight, thereby rolling back an additional epoch of honest blocks and attestations…

By the way, for all the attack strategies above, if b_{k2} is the block of the first slot then it is unnecessary to launch a one-epoch inactivation attack against epoch e+1. If b_{k2} is a later block, then that one-epoch inactivation attack must be carried out.

# References

[[1]Fang, Y. (2025, October 27). One-Epoch Inactivation and Pistol Attacks. Ethresear.Ch. https://ethresear.ch/t/one-epoch-inactivation-and-pistol-attacks/23351](https://ethresear.ch/t/one-epoch-inactivation-and-pistol-attacks/23351)

## Replies

**Tuoeth** (2025-11-09):

Hello, thank you for your efforts. I would like to ask the following questions:

1. Why should the byzantine votes be sent to the last Byzantine proposer in epoch e+1?
2. I think once b_k is released, it can already justify the checkpoint of epoch e. Why is b_{k2} still needed?

---

**Mediabs2022** (2025-11-09):

Thank you very much for your questions. First, b_k can be sent to any Byzantine proposer in epoch e+1 that is not involved in the one-epoch inactivation attack, and it can be released before the unrealized justified slot of the next epoch.

Second, if b_k is released with a delay, then b_{k2} is not necessary to justify cp_e. Thanks again.

---

**nagyabi** (2025-11-12):

Hello, thank you for the post and your work. Just to clarify, cp_e refers to bi2, right? If yes, it means that the 2 branches from slot t+18 share a justified checkpoint, and the LMD-Ghost would prefer the honest branch, right? How is the adversarial branch favored once bk2 is proposed? To my understanding the only difference between the adversarial and honest branch (starting from slot t+18) is that we could justify cp_e. Thank you!

---

**Mediabs2022** (2025-11-12):

Thank you for your question. First, on the honest chain, cp_e is exactly b_{i2}. Second, after discussing with [@Tuoeth](/u/tuoeth), if b_k is released with a delay until epoch e+2, then cp_e can be justified directly during epoch e+2 without requiring b_{k2}.

---

**seresistvanandras** (2025-11-12):

for some reason [@nagyabi](/u/nagyabi) cannot answer directly within 24 hours, so I send his message instead:

“I understand that cp_e is justified because we accumulated 2/3 of the votes. I refered to Strategy 1, how does justifying cp_e help us forking out the blocks between slot t+19 and t+62?“

---

**Mediabs2022** (2025-11-13):

Thanks for your question. Even if b_{i2} is shared by two branches, during `filter_block_tree` LMD-GHOST will first recursively check whether each branch satisfies:

```auto
correct_justified = (
    store.justified_checkpoint.epoch == GENESIS_EPOCH
    or voting_source.epoch == store.justified_checkpoint.epoch
    or voting_source.epoch + 2 >= current_epoch
)
```

In this attack scenario, the honest branch cannot justify b_{i2} due to two epochs of inactivity. Its `voting_source.epoch` is epoch e−1, while `current_epoch` is epoch e+2. Therefore it does not meet the `correct_justified` condition. As a result, the honest branch is filtered out **before** weight aggregation and thus is not considered by LMD-GHOST.

In fact, the reorg slots is not necessarily confined to slot [t+19, t+62]. The block b_k can be delayed and released as late as just before the unrealized justified state of cp_e+2, yielding a maximum attack window of slot [t+17, t+85].

