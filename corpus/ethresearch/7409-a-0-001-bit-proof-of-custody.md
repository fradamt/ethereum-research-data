---
source: ethresearch
topic_id: 7409
title: A 0.001 bit proof of custody
author: dankrad
date: "2020-05-12"
category: Sharding
tags: [proofs-of-custody]
url: https://ethresear.ch/t/a-0-001-bit-proof-of-custody/7409
views: 4502
likes: 5
posts_count: 4
---

# A 0.001 bit proof of custody

**TL;DR:** A probabilistic proof of custody using only one bit per attestation has been suggested before, and is currently specified for inclusion in phase 1 of the Eth2.0 rollout. It is actually possible to extend this method to make the overhead so small that no separate data structure at all is needed: Instead, a (very small) number of shard block attestations is “poisoned”, and signing a poisoned attestation makes a validator slashable in the same way an incorrect custody bit does. We can therefore simplify the attestation data structures and logic by removing the custody bits.

# Background

In order to avoid the “honest but lazy” validator problem, validators have to compute a “proof of custody” that shows that they actually possess a copy of the data that is being signed. [@JustinDrake](/u/justindrake) introduced the idea of a 1-bit proof of custody [1] that mixes an ephemeral secret only known to the validator with the data and computes one bit. Later, validators have to reveal their ephemeral secret and everyone can check the custody bit was computed correctly.

A validator has a 50% chance of guessing the custody bit correctly without doing any computation (and thus, without requiring the data). However, since the penalty of slashing is high, this has a negative expected return, and the “lazy” validator is discouraged from doing so.

## Current implementation

In order to be maximally MPC-friendly [2], the current implementation is as follows: Let p=2^{256}-189. During each custody period, a validator computes a custody secret that consists of three numbers s_0, s_1, s_2 \in \mathbb{Z}_p. The polynomial Universal Hash Function on the data chunks d_0, \ldots, d_{n-1} is defined as

\mathrm{UHF}(d_0, \ldots, d_{n-1},s_0, s_1, s_2) = \sum_{i=0}^{n-1} d_i s_{i \mod 3}^i + s_{n \mod 3}^n

To compute a single bit from the UHF-output in an MPC-friendly way, we take the Legendre symbol as the custody bit:

\mathrm{custodybit} = L_p(\mathrm{UHF}(d_0, \ldots, d_{n-1},s_0, s_1, s_2) + s_0)

where L_p is the Legendre symbol [3] normalized to one bit, i.e.

L_p(x) = \left\lfloor \frac{1}{2}\left(\left(\frac{x}{p}\right) + 1 \right) \right\rfloor \text{.}

# Suggested updated construction

We start with the observation that any risk of incurring a slashing, with an expected loss that is greater than the average reward per epoch, would deter an honest but lazy validator from attesting without computing the proof of custody. With the current custody bit construction, the probability is 50%. Using the current beacon chain spec, at 0.5M Eth staked (the very low end for security), the reward is around 100k GWei per epoch, but the cost of slashing is 1 Eth (1 billion GWei) (both at 32 Eth staked, proportionally lower if less). This suggests even a 1/1000 chance of getting slashed is plenty of a deterrent, as the expected loss is still ten times the gain per attestation. Since we aren’t concerned about malicious (only rational) behaviour, this analysis suggests we could use a custody bit that is one 99.9% of the time and 0 only 0.1% of the time.

Given this, we can just remove the custody bit from the attestation data entirely, and say an attestation is simply invalid (and slashable) if the custody bit is 0, so that we don’t need to store it. The new custody bit is computed as the logical **OR** of the ten Legendre bits

\mathrm{custodybit}_i = L_p(\mathrm{UHF}(d_0, \ldots, d_{n-1},s_0, s_1, s_2) + s_0 + i)

for i=0, \ldots, 9. This will be zero with probability 1/1024.

## Analysis

The main advantage is a slight reduction in spec complexity and smaller attestations.

The only disadvantage of this construction is a tiny loss in the number of attestations. This should not lead to any serious security loss.

The MPC-friendlyness of the construction is preserved, and the overhead will only be increased by a tiny bit from having to compute 10 bits instead of one. Assuming that the Legendre PRF [4] is secure, the OR computation can be done in the open by secret shared validators, so we still only need a single round of online MPC computation.

A further interesting property is that since the information leak is only 0.001 bits per attestation, and with  2048 attestations per custody period, only an expected 2 bits of the custody secret are leaked, making the construction information theoretically secure with respect to recovery of the custody secret (for non-MPC validators).

[1] [1-bit aggregation-friendly custody bonds](https://ethresear.ch/t/1-bit-aggregation-friendly-custody-bonds/2236)

[2] [Using the Legendre symbol as a PRF for the Proof of Custody](https://ethresear.ch/t/using-the-legendre-symbol-as-a-prf-for-the-proof-of-custody/5169)

[3] https://en.wikipedia.org/wiki/Legendre_symbol

[4] https://legendreprf.org

## Replies

**dankrad** (2020-05-14):

One problem with the proof of custody is that the point at “all proofs of custody are correct” is not an equilibrium: If all proofs are correct, then policing it has no rewards, and thus nobody would police. We can easily correct this using the construction mentioned here by changing the custody slashing function, for example like this:

- A CustodySlashing is valid if all custody bits are 0; the offender gets slashed and the whistleblower gets a reward
- A CustodySlashing is also valid if all custody bits are 1; however, the offender does not get slashed, only the whistleblower reward is awarded

The second condition makes policing profitable even in the absence of custody offenders, and thus we can be certain that policing is always going to happen.

Since custody slashings have high overhead, we would probably modify the second condition to one that is much less likely (e.g. 1:1 million) and increase the reward.

---

**JustinDrake** (2020-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> We can easily correct this using the construction mentioned here by changing the custody slashing function, for example like this

Similar ideas have been proposed to mitigate the verifier’s dilemma in the context of [TrueBit](https://truebit.io/).

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> The second condition makes policing profitable even in the absence of custody offenders

The block proposer which triggers the second condition can self-police and receive the whistleblower reward.

---

**dankrad** (2020-06-11):

I noticed that I actually made an error in this claim:

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> A further interesting property is that since the information leak is only 0.001 bits per attestation, and with 2048 attestations per custody period, only an expected 2 bits of the custody secret are leaked, making the construction information theoretically secure with respect to recovery of the custody secret (for non-MPC validators).

Actually, the correct way to compute the entropy is the Shannon entropy:

E = -\sum_{x \in S} p(x) \log p(x)

and for the suggested 1/1024 probability of returning a 0 custody bit and therefore a slashable attestation it leaks ca. 0{.}011 bits of entropy per attestation. For the suggested custody period of 2,048 epochs this results in a leak of ca. 23 bit and can therefore be considered information theoretically secure. Extending the custody period to 2^{14}=16,384 epochs, which is currently under consideration, would lead to a 183 bit leak per custody period. Since the full signature has 762 bits this is still very likely secure, but maybe not obviously information-theoretically secure against any kind of leak. It would be worthwhile for a cryptographer to have a closer look in this case.

