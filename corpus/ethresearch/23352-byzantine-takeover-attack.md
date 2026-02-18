---
source: ethresearch
topic_id: 23352
title: Byzantine takeover attack
author: Mediabs2022
date: "2025-10-27"
category: Consensus
tags: []
url: https://ethresear.ch/t/byzantine-takeover-attack/23352
views: 148
likes: 3
posts_count: 1
---

# Byzantine takeover attack

# Byzantine takeover attack

The **Byzantine takeover attack** is an attack in which Byzantine validators collude to construct a private branch that contains only Byzantine-produced blocks and, upon release, cause that branch to become the canonical chain. This attack enables the Byzantine validators to perform on-chain transactions, produce proofs, and package blocks arbitrarily on the attacker-controlled branch. Once the initial attack conditions are satisfied, the adversary can enumerate Randaos to make the attack recur with probability approaching 1 within the collusive environment, effectively driving the beacon chain toward a takeover state. The takeover attack can be instantiated using different one-epoch inactivation attack primitives [1], yielding six concrete attack strategies.

### Strategy 1

As shown in the figure, validators at slots t-1, t-2, and t collude to launch a sly-ex-ante attack. Validators at slots t+31 and t+33 collude to launch a sly-sandwich attack.

In epochs e, e+1, and e+2, all Byzantine attestors also only collusively send their votes to the Byzantine proposers in the current or next epoch. All Byzantine proposers locally store these blocks and delay their release; during the last slots of epochs e+1 and e+2 they repeatedly enumerate and try candidate RANDAO values to choose the most favorable RANDAO for assigning duties in epochs e+3 and e+4. Each Byzantine proposer may choose to miss certain slots to avoid updating the RANDAO[2]. In this way, the number of RANDAOs that RANDAO-grinding can enumerate in each of these two epochs is 2^{32/3 - 1} = 2^{9} = 512.

Because Byzantine validators control roughly 1/3 of the stake, each enumerated RANDAO gives a 1/3 probability that the first slot of epoch e+3 or e+4 will be assigned to a Byzantine proposer. Therefore, the probability that the first slot in epoch e+3 (and similarly e+4) is assigned to a Byzantine proposer is approximately

1 - \left(\tfrac{2}{3}\right)^{512} \approx 100\%.

Moreover, Byzantine proposers must include roughly 1/3 of the honest votes from epoch e in their attack chain to ensure that, after release, the attack chain can justify cp_e. To maximize honest incentive loss, the attacker may choose not to include the honest votes from epochs e+1 and e+2 in the attack chain.

In a single attack instance, the attack chain is released during the final slot of epoch e+2, specifically in the final 4 seconds before that slot ends, so as to ensure that honest votes cast will vote for the attack chain’s head block and thus will not allow epoch e+2 to be re-justified by honest voters in epoch e+3. Prior to release, the attacker has locally enumerated and selected the most favorable RANDAO combination; upon release the attack chain can justify cp_e and reorg the honest chain into the new canonical chain, and the attacker can ensure the attack recurs with near 100% probability.

[![takeover-1-exante+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/9/5/95b6b6d04dda0123bdc357b44ec081c8079b739e_2_690x139.png)takeover-1-exante+sandwich.png1943×393 39.6 KB](https://ethresear.ch/uploads/default/95b6b6d04dda0123bdc357b44ec081c8079b739e)

As shown in the figure, RANDAO grinding can ensure that the first slot of both epoch e+3 and epoch e+4 are assigned to Byzantine proposers. These proposers can then extend the canonical chain and, in the corresponding epochs, execute sly-1/3-slot-withhold attacks. The remaining Byzantine behavior in epochs e+3, e+4, and e+5 is similar to that in epochs e, e+1, and e+2; by the same RANDAO-grinding technique, the attacker can ensure the first slot of epochs e+6 and e+7 are Byzantine-proposer slots. Releasing the attack chain during the final 4 seconds of the last slot of epoch e+5 will make the chain the new canonical chain.

By repeating the Byzantine strategies in epochs e+3, e+4, and e+5 in this cyclic manner, the attack can continue to recur indefinitely.

[![takeover-1-exante+sandwich-2.png](https://ethresear.ch/uploads/default/optimized/3X/3/f/3f7f992607ec196c91dc4f0512bd13b486e1400f_2_690x303.png)takeover-1-exante+sandwich-2.png920×405 24.1 KB](https://ethresear.ch/uploads/default/3f7f992607ec196c91dc4f0512bd13b486e1400f)

### Strategy 2

As shown in the figure, validators at slots t-1, t-2, and t collude to launch a sly-ex-ante attack. Validators at slots t+32 collude to launch a sly-1/3-slot-withhold attack.

In epochs e, e+1, and e+2, all Byzantine attestors collusively send their votes only to the Byzantine proposers in the current or next epoch. All Byzantine proposers locally store these blocks and delay their release; during the last slots of epochs e+1 and e+2 they repeatedly enumerate and try candidate RANDAO values to choose the most favorable RANDAO for assigning duties in epochs e+3 and e+4. Each Byzantine proposer may choose to miss certain slots to avoid updating the RANDAO[2]. In this way, the numbers of RANDAOs that RANDAO-grinding can enumerate in these two epochs are 2^{32/3 - 1} = 2^{9} = 512 and 2^{32/3} = 2^{10} = 1024, respectively.

Because Byzantine validators control roughly 1/3 of the stake, each enumerated RANDAO gives a 1/3 probability that the first slot of epoch e+3 or e+4 will be assigned to a Byzantine proposer. Therefore, the probabilities that the first slot in epoch e+3 and epoch e+4 are assigned to a Byzantine proposer are approximately 1 - \left(\tfrac{2}{3}\right)^{512} and 1 - \left(\tfrac{2}{3}\right)^{1024}, respectively — effectively 100\%.

Moreover, Byzantine proposers must include roughly 1/3 of the honest votes from epoch e in their attack chain to ensure that, after release, the attack chain can justify cp_e. To maximize honest incentive loss, the attacker may choose not to include the honest votes from epochs e+1 and e+2 in the attack chain.

By repeating these RANDAO-grinding and Byzantine collusion strategies, the attack can continue to recur cyclically.

In a single attack instance, the attack chain is released during the final 4 seconds of the last slot of epoch e+2, ensuring that honest votes are cast for the head block of the attack chain. This prevents the honest validators from re-justifying epoch e+2 in epoch e+3 and regaining the canonical chain. Prior to release, the attacker has locally enumerated and selected the most favorable RANDAO combination; upon release, the attack chain can justify cp_e and reorganize the honest chain into the new canonical chain.

Similarly, RANDAO grinding can ensure that the first slot of both epoch e+3 and epoch e+4 are assigned to Byzantine proposers. These proposers can then continue extending the canonical chain and launch sly-1/3-slot-withhold attacks in their respective epochs. The remaining Byzantine behavior in epochs e+3, e+4, and e+5 is similar to that in epochs e, e+1, and e+2. Likewise, RANDAO grinding can ensure that the first slot of epochs e+6 and e+7 are Byzantine-proposer slots. Releasing the attack chain during the final 4 seconds of the last slot of epoch e+5 will again make the attack chain the new canonical chain.

By repeating the Byzantine strategies used in epochs e+3, e+4, and e+5, the attack can continue to recur indefinitely.

[![takeover-2-exante+4s.png](https://ethresear.ch/uploads/default/optimized/3X/e/5/e5f4bd822bd69c85473c6b743a2c3615cd827974_2_690x149.png)takeover-2-exante+4s.png1985×431 49.4 KB](https://ethresear.ch/uploads/default/e5f4bd822bd69c85473c6b743a2c3615cd827974)

### Strategy 3

As shown in the figure, validators at slots t-1, t, and t+1 collude to launch a sly-sandwich attack. Validators at slots t+31 to t+33 also collude to launch another sly-sandwich attack.

In epochs e, e+1, and e+2, all Byzantine attestors—except those in slot $t+32$—collusively send their votes only to the Byzantine proposers in the current or next epoch. All Byzantine proposers locally store these blocks and delay their release; during the last slots of epochs e+1 and e+2, they repeatedly enumerate and test candidate RANDAO values to select the most favorable RANDAO for assigning duties in epochs e+3 and e+4. Each Byzantine proposer may choose to miss certain slots to avoid updating the RANDAO[2].

In this way, the numbers of RANDAOs that can be enumerated via RANDAO grinding in these two epochs are 2^{32/3 - 1} = 2^{9} = 512 and 2^{32/3} = 2^{10} = 1024, respectively. Since Byzantine validators control approximately one-third of the total stake, each enumerated RANDAO provides a one-third probability that the first slot of epoch e+3 or e+4 will be assigned to a Byzantine proposer. Therefore, the probabilities that the first slots in epochs e+3 and e+4 are Byzantine proposer slots are approximately: 1 - \left(\tfrac{2}{3}\right)^{512} \text{ and } 1 - \left(\tfrac{2}{3}\right)^{1024} \approx 100\%.

Furthermore, Byzantine proposers must include roughly one-third of the honest votes from epoch e in their attack chain to ensure that, after release, the chain can justify cp_e. To cause greater honest incentive loss, the attacker may choose **not** to include honest votes from epochs e+1 and e+2 in the attack chain.

In a single attack instance, the attack chain is released during the final 4 seconds of the last slot of epoch e+2, ensuring that honest votes are cast for the head block of the attack chain; as a result, honest validators will not re-justify epoch e+2 in epoch e+3 and thus will not regain the canonical chain. Prior to release, the attacker has locally enumerated and selected the most favorable RANDAO combination; upon release the attack chain can justify cp_e and reorganize the honest chain into the new canonical chain.

Similarly, RANDAO grinding can ensure that the first slot of both epoch e+3 and epoch e+4 are assigned to Byzantine proposers. Those proposers can then continue extending the canonical chain and launch sly-1/3-slot-withhold attacks in the corresponding epochs. The remaining Byzantine behavior in epochs e+3, e+4, and e+5 is analogous to that in epochs e, e+1, and e+2. By the same RANDAO-grinding technique, the attacker can ensure the first slot of epochs e+6 and e+7 are Byzantine-proposer slots; releasing the attack chain during the final 4 seconds of the last slot of epoch e+5 will make the chain the new canonical chain.

By repeating the Byzantine strategies used in epochs e+3, e+4, and e+5 in this cyclic manner, the attack can continue to recur indefinitely.

[![takeover-3-sandwich+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/1/4/144085f56b73ed2657bf6c825dfb3130e1abb7a2_2_690x151.png)takeover-3-sandwich+sandwich.png1993×439 51.2 KB](https://ethresear.ch/uploads/default/144085f56b73ed2657bf6c825dfb3130e1abb7a2)

### Strategy 4

As shown in the figure, validators at slots t-1, t, and t+1 collude to launch a sly-sandwich attack, while validators at slot t+32 collude to launch a sly-1/3-slot-withhold attack.

In epochs e, e+1, and e+2, all Byzantine attestors collusively send their votes only to the Byzantine proposers in the current or the next epoch. All Byzantine proposers locally store these blocks and delay their release; during the last slots of epochs e+1 and e+2, they repeatedly enumerate and test candidate RANDAO values to select the most favorable RANDAO for assigning duties in epochs e+3 and e+4. Each Byzantine proposer may choose to miss certain slots to avoid updating the RANDAO[2].

In this way, the numbers of RANDAOs that can be enumerated via RANDAO grinding in these two epochs are 2^{32/3 - 1} = 2^{9} = 512 and 2^{32/3} = 2^{10} = 1024, respectively. Since Byzantine validators control approximately one-third of the total stake, each enumerated RANDAO provides a one-third probability that the first slot of epoch e+3 or e+4 will be assigned to a Byzantine proposer. Therefore, the probabilities that the first slots in epochs e+3 and e+4 are Byzantine proposer slots are approximately:1 - \left(\tfrac{2}{3}\right)^{512} \text{ and } 1 - \left(\tfrac{2}{3}\right)^{1024} \approx 100\%.

Moreover, Byzantine proposers must include roughly one-third of the honest votes from epoch e in their attack chain to ensure that, after release, the chain can justify cp_e. To cause greater honest incentive loss, the attack chain deliberately excludes the honest votes from epochs e+1 and e+2.

In a single attack instance, the attack chain is released during the final 4 seconds of the last slot of epoch e+2, ensuring that honest votes are cast for the head block of the attack chain; as a result, honest validators will not re-justify epoch e+2 in epoch e+3 and thus will not regain the canonical chain. Prior to release, the attacker has locally enumerated and selected the most favorable RANDAO combination; upon release the attack chain can justify cp_e and reorganize the honest chain into the new canonical chain.

Similarly, RANDAO grinding can ensure that the first slot of both epoch e+3 and epoch e+4 are assigned to Byzantine proposers. Those proposers can then continue extending the canonical chain and launch sly-1/3-slot-withhold attacks in the corresponding epochs. The remaining Byzantine behavior in epochs e+3, e+4, and e+5 is analogous to that in epochs e, e+1, and e+2. By the same RANDAO-grinding technique, the attacker can ensure the first slot of epochs e+6 and e+7 are Byzantine-proposer slots; releasing the attack chain during the final 4 seconds of the last slot of epoch e+5 will make the chain the new canonical chain.

By repeating the Byzantine strategies used in epochs e+3, e+4, and e+5 in this cyclic manner, the attack can continue to recur indefinitely.

[![takeover-4-sandwich+4s.png](https://ethresear.ch/uploads/default/optimized/3X/0/6/066d3ee38bc958e634851571760467fe1ee1ae4d_2_690x161.png)takeover-4-sandwich+4s.png1996×468 49.6 KB](https://ethresear.ch/uploads/default/066d3ee38bc958e634851571760467fe1ee1ae4d)

### Strategy 5

As shown in the figure, validators at slot t launch a sly-1/3-slot-withhold attack, while validators at slots t+31, t+32, and t+33 collude to launch a sly-sandwich attack.

In epochs e, e+1, and e+2, all Byzantine attestors—except those in slot $t+32$—collusively send their votes only to the Byzantine proposers in the current or next epoch. All Byzantine proposers locally store these blocks and delay their release; during the last slots of epochs e+1 and e+2, they repeatedly enumerate and test candidate RANDAO values to select the most favorable RANDAO for assigning duties in epochs e+3 and e+4. Each Byzantine proposer may choose to miss certain slots to avoid updating the RANDAO[2].

In this way, the numbers of RANDAOs that can be enumerated via RANDAO grinding in these two epochs are 2^{32/3 - 1} = 2^{9} = 512 and 2^{32/3} = 2^{10} = 1024, respectively. Since Byzantine validators control approximately one-third of the total stake, each enumerated RANDAO provides a one-third probability that the first slot of epoch e+3 or e+4 will be assigned to a Byzantine proposer. Therefore, the probabilities that the first slots in epochs e+3 and e+4 are Byzantine proposer slots are approximately:1 - \left(\tfrac{2}{3}\right)^{512} \text{ and } 1 - \left(\tfrac{2}{3}\right)^{1024} \approx 100\%.

Moreover, Byzantine proposers must include roughly one-third of the honest votes from epoch e in their attack chain to ensure that, after release, the chain can justify cp_e. To cause greater honest incentive loss, the attack chain deliberately excludes the honest votes from epochs e+1 and e+2.

In a single attack instance, the attack chain is released during the final 4 seconds of the last slot of epoch e+2, ensuring that honest votes are cast for the head block of the attack chain. This prevents the honest validators from re-justifying epoch e+2 in epoch e+3 and regaining the canonical chain. Prior to release, the attacker has locally enumerated and selected the most favorable RANDAO combination; upon release, the attack chain can justify cp_e and reorganize the honest chain into the new canonical chain.

Similarly, RANDAO grinding can ensure that the first slot of both epoch e+3 and epoch e+4 are assigned to Byzantine proposers. These proposers can then continue extending the canonical chain and launch sly-1/3-slot-withhold attacks in their respective epochs. The remaining Byzantine behavior in epochs e+3, e+4, and e+5 is analogous to that in epochs e, e+1, and e+2. By the same RANDAO-grinding technique, the attacker can ensure the first slot of epochs e+6 and e+7 are Byzantine-proposer slots; releasing the attack chain during the final 4 seconds of the last slot of epoch e+5 will make the chain the new canonical chain.

By repeating the Byzantine strategies used in epochs e+3, e+4, and e+5 in this cyclic manner, the attack can continue to recur indefinitely.

[![takeover-5-4s+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/1/c/1c04390a540ce47ca53c7ad09447012e317a4517_2_690x205.png)takeover-5-4s+sandwich.png1593×474 44.2 KB](https://ethresear.ch/uploads/default/1c04390a540ce47ca53c7ad09447012e317a4517)

### Strategy 6

As shown in the figure, validators at slots t and t+32 launch sly-1/3-slot-withhold attacks.

In epochs e, e+1, and e+2, all Byzantine attestors collusively send their votes only to the Byzantine proposers in the current or next epoch. All Byzantine proposers locally store these blocks and delay their release; during the last slots of epochs e+1 and e+2, they repeatedly enumerate and test candidate RANDAO values to select the most favorable RANDAO for assigning duties in epochs e+3 and e+4. Each Byzantine proposer may choose to miss certain slots to avoid updating the RANDAO[2].

In this way, the numbers of RANDAOs that can be enumerated via RANDAO grinding in these two epochs are 2^{32/3 - 1} = 2^{9} = 512 and 2^{32/3} = 2^{10} = 1024, respectively. Since Byzantine validators control approximately one-third of the total stake, each enumerated RANDAO provides a one-third probability that the first slot of epoch e+3 or e+4 will be assigned to a Byzantine proposer. Therefore, the probabilities that the first slots in epochs e+3 and e+4 are Byzantine proposer slots are approximately:1 - \left(\tfrac{2}{3}\right)^{512} \text{ and } 1 - \left(\tfrac{2}{3}\right)^{1024} \approx 100\%.

Moreover, Byzantine proposers must include roughly one-third of the honest votes from epoch e in their attack chain to ensure that, after release, the chain can justify cp_e. To cause greater honest incentive loss, the attack chain deliberately excludes the honest votes from epochs e+1 and e+2.

In a single attack instance, the attack chain is released during the final 4 seconds of the last slot of epoch e+2, ensuring that honest votes are cast for the head block of the attack chain. This prevents the honest validators from re-justifying epoch e+2 in epoch e+3 and regaining the canonical chain. Prior to release, the attacker has locally enumerated and selected the most favorable RANDAO combination; upon release, the attack chain can justify cp_e and reorganize the honest chain into the new canonical chain.

Similarly, RANDAO grinding can ensure that the first slot of both epoch e+3 and epoch e+4 are assigned to Byzantine proposers. These proposers can then continue extending the canonical chain and launch sly-1/3-slot-withhold attacks in the corresponding epochs. The remaining Byzantine behavior in epochs e+3, e+4, and e+5 is analogous to that in epochs e, e+1, and e+2. By the same RANDAO-grinding technique, the attacker can ensure the first slot of epochs e+6 and e+7 are Byzantine-proposer slots; releasing the attack chain during the final 4 seconds of the last slot of epoch e+5 will make the chain the new canonical chain.

By repeating the Byzantine strategies used in epochs e+3, e+4, and e+5 in this cyclic manner, the attack can continue to recur indefinitely. This strategy is similar to the attack described in [3]. Therefore, our previous 6 strategies can be seen as an extension of [3], where, under the condition that the first slot (t or t+32) in the initial two epochs of the attack is an honest proposer and no attack occurs, five additional attack strategies are introduced by adding checks for the block proposer identities in slots t-2, t-1, and t+1 (or t+30, t+31, and t+33), thereby increasing the probability that the attack occurs on time.

[![takeover-6-4s+4s.png](https://ethresear.ch/uploads/default/optimized/3X/8/5/85bcb14185dc2f9845f2ec2fb93689d7457a0bf8_2_690x163.png)takeover-6-4s+4s.png1652×392 42.6 KB](https://ethresear.ch/uploads/default/85bcb14185dc2f9845f2ec2fb93689d7457a0bf8)

# Attack Strategy Expansion

For the six attack strategies mentioned above, a greedy strategy can be employed to delay the justification progress as much as possible, leading to the expansion of the strategies and the creation of six new attack strategies. Specifically, after meeting the initial conditions of the attack and successfully launching it, the goal is to justify the relevant epoch as quickly as possible. This reduces the granularity of the epoch during which the attack occurs, allowing the attacker to end the attack and successfully cause the rollback of the honest branch with one less epoch of waiting. At this point, the Byzantine strategies of the attack chain proposers need to be adjusted, and the specific adjustments are as follows:

1. Same as the six strategies above, release the attack chain before the vote in the last slot of epoch e+2, which can justify cp_e, update the justified checkpoint to cp_e, and make it the new canonical chain. After the attack chain is released, the attack chain up to epoch e+2 is fully released.
2. Release the attack chain before the vote in the last slot of epoch e+4. The blocks in the attack chain for epoch e+3 will include approximately one-third additional honest votes from that epoch. The first block of the attack chain in epoch e+4 will justify cp_{e+3}, update the justified checkpoint to cp_{e+3}, and make it the new canonical chain. After the attack chain is released, the attack chain up to epoch e+4 is fully released.
3. Similarly, release the attack chain before the vote in the last slot of epoch e+6. The blocks in the attack chain for epoch e+5 will include approximately one-third additional honest votes from that epoch. The first block of the attack chain in epoch e+6 will justify cp_{e+5}, update the justified checkpoint to cp_{e+5}, and make it the new canonical chain. After the attack chain is released, the attack chain up to epoch e+6 is fully released.

…

Furthermore, to ensure that there are sufficient attestations in epochs e+3, e+5, e+7, …, RANDAO grinding can be used to additionally ensure that the last slot of each epoch is also assigned to a Byzantine proposer. Similarly, the probability of this condition being satisfied is:

For epoch e+3:  1 - \left(1 - \frac{1}{9}\right)^{512}

For epochs e+5, e+7, …:  1 - \left(1 - \frac{1}{9}\right)^{1024}

This probability is close to 1.

At this point, the attack can continue to recur according to this pattern, thus accelerating the attack process and causing greater losses to the honest validators within a limited number of slots.

[![takeover-II-withhold.png](https://ethresear.ch/uploads/default/optimized/3X/4/6/46d8fc368b969e8be9ff438bd2d29297b8e44658_2_690x299.png)takeover-II-withhold.png1569×681 52.3 KB](https://ethresear.ch/uploads/default/46d8fc368b969e8be9ff438bd2d29297b8e44658)

Furthermore, Byzantine validators can choose to attack only the honest blocks of the first inactive epoch in subsequent cycles, further enhancing the flexibility of the attack. The specific strategy is as follows:

The attack chain in epoch e+1 is delayed until the first 4 seconds of epoch e+2 for release. By enumerating RANDAOs, it is further ensured that the last slot of epoch e+1 is assigned to a Byzantine proposer, who packages approximately two-thirds of the votes from epoch e+1. The first Byzantine proposer in epoch e+2 continues to extend the attack chain from epoch e+1 and releases it together. This justifies epoch e and makes the attack chain the new canonical chain. At this point, there is no need to launch a one-epoch inactivation attack in epoch e+1.

Similarly, the attack chain in epoch e+3 is delayed until the first 4 seconds of epoch e+4 for release. By enumerating RANDAOs, it is ensured that the last slot of epoch e+3 is assigned to a Byzantine proposer, who packages approximately two-thirds of the votes from epoch e+3. The first Byzantine proposer in epoch e+4 continues to extend the attack chain from epoch e+3 and releases it together. This justifies epoch e+3 and makes the attack chain the new canonical chain. At this point, there is no need to launch a one-epoch inactivation attack in epoch e+3.

…

# References

[[1] Fang, Y. (2025, October 27). One-Epoch Inactivation and Pistol Attacks . Ethresear.Ch. https://ethresear.ch/t/one-epoch-inactivation-and-pistol-attacks/23351](https://ethresear.ch/t/one-epoch-inactivation-and-pistol-attacks/23351)

[[2]Nero_eth. (2023, July 10). Selfish Mixing and RANDAO Manipulation. Ethresear.Ch. ethresear.ch/t/selfish-mixing-and-randao-manipulation/16081/](https://ethresear.ch/t/selfish-mixing-and-randao-manipulation/16081/)

[[3]Zhang, M. (2025, April 30). Liveness Attack in Ethereum PoS Protocol Using RANDAO Manipulation. Ethresear.Ch. https://ethresear.ch/t/liveness-attack-in-ethereum-pos-protocol-using-randao-manipulation/22241](https://ethresear.ch/t/liveness-attack-in-ethereum-pos-protocol-using-randao-manipulation/22241)
