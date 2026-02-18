---
source: ethresearch
topic_id: 6230
title: Security Level of Random Sampling With Sharding
author: qizhou
date: "2019-10-02"
category: Sharding
tags: []
url: https://ethresear.ch/t/security-level-of-random-sampling-with-sharding/6230
views: 3220
likes: 3
posts_count: 15
---

# Security Level of Random Sampling With Sharding

I read the article of the probability of an attacker that takes over a shard is (https://github.com/ethereum/wiki/wiki/Sharding-FAQ#how-is-the-randomness-for-random-sampling-generated)

X =  ![image](https://ethresear.ch/uploads/default/original/2X/a/a9d1424e770da1c105843460eeebf51b29b47802.png)

where N is the size of a sample and p is the percentage of attackers in the pool.  This could work if there is only one shard.  However, in the case of M shards in the network, the attack probability of **at least one shard** being attacked in the M shards (i.e., 1 - P(all shards are safe)) should be (assuming the random variables of all shards being attacked are i.i.d.)

Y = 1 - (1 - X)^M, which is about X * M if X is small.

E.g., if N = 150, p = 0.333333, and M = 1024, then

X = 1.83e-5

while

Y = 0.0185

Should the security level of random sampling with sharding work like this?  I searched for several ETH2.0 documents but cannot find related explanation.

## Replies

**vbuterin** (2019-10-02):

This is correct, with one major caveat: if you’re trying to make eth2 break by computing different seeds and looking for one that makes a shard break, then checking M shards is M times more expensive than checking 1 shard (and as expensive as checking M ways to break the same shard), so the number of shards doesn’t affect the computational soundness guarantee. So it depends on whether you’re looking at attackers whose manipulation of the RNG seed is bounded computationally (the worst case) or bounded some other way (in which case the attacker’s ability to manipulate is limited anyway).

Current eth2 sharding picks parameters that are fairly conservative; specifically, it demands 2/3 online to accept a crosslink, which is much harder to get to for a 1/3 attacker than 1/2 is.

---

**szhygulin** (2019-10-02):

I think what [@qizhou](/u/qizhou) trying to say (and I have a similar concern) is that an attacker does not need to manipulate RNG. He just needs to wait the moment when at some point he gets the supermajority in any of M shards (and the probability of that event was computed above by [@qizhou](/u/qizhou)), and insert malicious transaction in the block that attacker is going to validate. Since that transaction can print a lot of fake ETHs and will be validated, it breaks the security of the whole network.

To avoid this threat, IMHO, block proposition and validation processes must be decoupled, and the proposition of invalid block should be punished (by staking?). Therefore, for an attacker to validate improper block he must submit a malicious block proposal and make sure that a randomly chosen committee validates it. And that is super costly because he cannot guarantee that his block will be validated by the committee controlled by him, the only way is to try again and again to get a match. If each failed attempt cost attacker  $1000 - he will dry his funds very fast.

---

**szhygulin** (2019-10-02):

So, if this decoupling technique is something you guys find valuable, I can elaborate on security level of this model in terms of what is optimal strategy for attacker and how much attack will cost given parameters: malicious block proposal punishment, amount of shards, total stake, etc.

Another important question is how to prevent validators from banning honest blocks. I think this can be managed by removing validator’s reward in case of block ban, since for honest validators banning malicious block is of great utility by itself, no need for extra reward here. Another option is to perform more than 1 round of voting for banning a block.

---

**qizhou** (2019-10-02):

Yes.  Here I assume the perfect random source of sampling (sufficient entropy and non-manipulatable).  My conclusion is that increasing M is essentially accelerating the attack over time with factor M.  Note that this is based on i.i.d. assumption of A_i, namely the random variable that the ith shard is attacked in a sampling.  In fact, A_i’s are dependent if all validators are selected by shuffling the validator pool (select without replacement).  In such a case, the actual attack probably may be more complicated, and

P(all shards are safe) \neq \prod_{i=0}^{M-1} P(shard i is safe).

To evaluate the actual attack probability,  we could resort to Monte-Carlo simulation.  I have a simulation code here [Monte-Carlo Simulation for Random Sampling](https://github.com/QuarkChain/pyquarkchain/blob/6139f773e31433d7f3ce4266eb3e8da7b75d3453/quarkchain/experimental/random_sampling_simulator.py).   The good news is that if M is large, the early result shows that the attack probability of validator selection wthout replacement is almost the same as that of i.i.d.

---

**szhygulin** (2019-10-02):

I played I little with parameters in your code. I found out that with a decrease of committee size actually attack probability increases greatly. Actually, if you put committee size equal to 50, you get a probability of attack around 80%.

That is interesting, because efficiently attacker’s proportion is not changing with decrease of committee size, but security lessens greatly.

---

**qizhou** (2019-10-02):

Yes, my 50000 trials simulation returns 0.018680 for N = 150, p = 0.3333, M = 1024, and pool size = 150 * 1024.

---

**qizhou** (2019-10-02):

Yes, decreasing the committee size will dramatically increase the attack probability.  The table in the link gives some examples ( https://github.com/ethereum/wiki/wiki/Sharding-FAQ#how-is-the-randomness-for-random-sampling-generated)

[![image](https://ethresear.ch/uploads/default/optimized/2X/6/65554085486d1b36db3c15be46bbf782890049d3_2_690x253.png)image1072×394 29.5 KB](https://ethresear.ch/uploads/default/65554085486d1b36db3c15be46bbf782890049d3)

---

**szhygulin** (2019-10-03):

So, based on your simulation, if N=150, and p = 0.33, given corruption threshold = 0.5, I got ~1% chance of corruption in at least one of 1024 shards, which is 10^3 times worse than stated in table above. Seems that your initial prediction Y = X * M is confirmed.

---

**adiasg** (2019-10-03):

I think the point was (as [@szhygulin](/u/szhygulin) clarified) to calculate the chance that an attacker controls some fraction of a crosslink committee not by any active attack, but just due to the random sampling. That fraction is 1/3rd to prevent crosslink to form in that epoch, and 2/3rd to include an invalid crosslink.

In both the above cases, what is the implication outside of that epoch? Is the attacker able to sabotage/control anything in future epochs?

---

**vbuterin** (2019-10-03):

> I think what @qizhou trying to say (and I have a similar concern) is that an attacker does not need to manipulate RNG. He just needs to wait the moment when at some point he gets the supermajority in any of M shards

Right, I understand. And that strategy works in the context of probabilities on the order of 10^{-5}, but the probabilities that we have in practice are much lower, because we use \frac{2}{3} as a threshold instead of \frac{1}{2}. For example with a committee size of 128, an attacker with \frac{1}{3} of total stake has a chance of only 2.2 * 10^{-14} of getting \ge 85.

---

**qizhou** (2019-10-03):

If my understanding is correct, this means, if we have 1024 shards, committee size 128, and 2/3 attack threshold attacking, then the chance of an attacker with 1/3 stake on at least one of 1024 shards becomes 2.29e-11 (1024 times higher than 2.2 * 10e-14).

---

**vbuterin** (2019-10-03):

Yep, that looks right.

---

**qizhou** (2019-10-03):

So the implication is that, suppose the original probability was designed for 1000 years per attack, now with 1024 shards, it reduces to 1 year per attack.  To reach the same security level as  a single shard network, we have to add more validators, which is about 30 validators in my rough calculation.  E.g., for committee size 128, 2/3 attack threshold and 1/3 stake, to achieve around 2e-14, we need to have about 150+ validators for all shards instead of 128 validator for a single shard network.  Similarly, to achieve around 2e-11, we need to have about 128 validators for all shards instead of 100 validators for a single shard network.

In summary, the network cost for validators will be O(M * V(M)), where M is the number of shards, and V(M) is the number of validators to reach a desired network security level (all shards are safe).  It seems that V(M) is sub-linear in terms of M, so the network cost will be sub-quadratic in terms of M.

---

**vbuterin** (2019-10-04):

V(M) should be not just sublinear, but even sub-logarithmic.

See: https://math.stackexchange.com/questions/89030/expectation-of-the-maximum-of-gaussian-random-variables

