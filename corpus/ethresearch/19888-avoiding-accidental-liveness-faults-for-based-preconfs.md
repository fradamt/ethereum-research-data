---
source: ethresearch
topic_id: 19888
title: Avoiding Accidental Liveness Faults for Based Preconfs
author: mteam88
date: "2024-06-22"
category: Layer 2
tags: [preconfirmations, based-sequencing]
url: https://ethresear.ch/t/avoiding-accidental-liveness-faults-for-based-preconfs/19888
views: 2808
likes: 7
posts_count: 1
---

# Avoiding Accidental Liveness Faults for Based Preconfs

# Avoiding Accidental Liveness Faults for Based Preconfs

*thanks to [Justin Drake](https://x.com/drakefjustin), [Jon Charbonneau](https://x.com/jon_charb), [Ladislaus](https://x.com/lvdaniels), [Sébastien Rannou](https://x.com/aimxhaisse), [sacha](https://x.com/lazyleger), [Drew van Der Werff](https://x.com/DrewVdW), and Max Wilde from [Aestus](https://x.com/aestusrelay) for thinking and review*

.

.

***tl;dr:** We solve one of the largest problems with based preconf opt-in from proposers: accidental liveness slashing. The mechanism we introduce requires no changes to existing based preconf protocol designs and has been under our noses the whole time. We use preconf chaining to protect individual proposers from being slashed for liveness failures.*

.

.

## Background

On Ethereum today, liveness issues with block proposals are largely accepted, and penalties are minimal. When we introduce based preconfirmations, liveness issues can mean different consequences.

When dealing with preconfs: from the user’s perspective, liveness faults (missing a block proposal) and safety faults (proposing a block that does not fulfill preconf commitments) are the same thing. In both scenarios, a user experiences a situation where their preconfirmation is not fulfilled.

[![liveness faults are safety faults](https://ethresear.ch/uploads/default/optimized/3X/9/d/9d996b95a0c2f74f54edf8f3d3b89beda26956db_2_406x500.png)liveness faults are safety faults500×615 511 KB](https://ethresear.ch/uploads/default/9d996b95a0c2f74f54edf8f3d3b89beda26956db)

Now, from the perspective of the proposer, liveness faults and safety faults are two very different things. Liveness faults may occur from a multitude of external, accidental circumstances (like power outages, wifi downtime, reorgs, spontaneous combustion) that many proposers just aren’t prepared for. On the other hand, safety faults can only occur when some party (the proposer or some delegate) acts maliciously.

Additionally, attributing liveness faults is difficult. Many actors within the block supply chain may be responsible for a liveness fault occurring. The complexity involved with this attribution would be nice to avoid.

To make proposers feel more comfortable with putting up potentially high amounts of collateral, being slashed for accidental liveness faults should be very rare if not impossible.

## Preconf Chaining

[![preconf chaining](https://ethresear.ch/uploads/default/original/3X/5/2/524180b5ef3a6673ab62d02d5afdc1a4d0d94fe5.png)preconf chaining500×500 291 KB](https://ethresear.ch/uploads/default/524180b5ef3a6673ab62d02d5afdc1a4d0d94fe5)

### Brief Assumptions:

- (we are talking about based preconfs here, not L1 preconfs)
- slashing conditions are expressive
- preconf requests include L2 block number
- “active preconfer” refers to the current preconfer (an L1 proposer or delegate in the lookahead), “next active preconfer” refers to the entity who will be the next preconfer.

### Slashing Conditions Construction:

We assume a slashing conditions paradigm that is similar to the one presented in [The Preconf Registry.](https://ethresear.ch/t/credibly-neutral-preconfirmation-collateral-the-preconfirmation-registry/19634) Specifically, that slashing conditions are “smart” and expressive enough to represent the following constructions.

The slashing conditions are designed so that a preconfer is slashed if:

- they sign a preconf request about a transaction A and block B, where B is a future L2 block. Also signed is a list of “dependents”, a list of other preconfers (by address or other ID).
- A is not fulfilled in B, or was not fulfilled in a block prior to B
- All dependents have signed the same preconf request (commitments/signatures from these are required) and have not been slashed (a challenge/cooldown period is useful here).

This dependent design enables a preconfer to conditionally preconfirm a transaction, based on the choices of other preconfer.

### Preconf Flow

- Alice (a based L2 user) wants an inclusion preconf for a transaction A
- Alice delivers a preconf request to the active preconfer
- Some entity who obtains a preconf commitment from the active preconfer (Alice, a gateway, or even the active preconfer itself) forwards Alice’s preconf request to the next active preconfer (with a dependent on the active preconfer added) and also forwards the active preconfer’s commitment.

[![diagram representing how any actor can send a chained preconf request to the next active preconfer](https://ethresear.ch/uploads/default/optimized/3X/8/4/84a8b7a1158dfc8f844abfc5447b193b3d35f12e_2_690x387.png)diagram representing how any actor can send a chained preconf request to the next active preconfer1087×610 50.9 KB](https://ethresear.ch/uploads/default/84a8b7a1158dfc8f844abfc5447b193b3d35f12e)

**Any actor with access to a preconf commitment may construct a chained preconf and forward it to the next active preconfer.**

Note that incentives for doing this vary:

- preconf RPC: aka The Preconfirmation Gateway might chain preconfs as a public good for proposers.
- gateway: A gateway might also chain preconfs as a public good for proposers, but may also use this as a feature to attract proposers (maybe called “liveness fault protection”).
- proposers: A proposer (or node operator) might also chain preconfs themselves. Their incentive is obviously to avoid being slashed for liveness faults.

### Determining Penalties

- In the case where the active preconfer represents a proposer that has a liveness failure and proposes no L2 block, they wouldn’t be slashed because the preconf could still be fulfilled by the next preconfer (and the preconf request block number would match).
- If the active preconfer proposes a block and does not fulfill the preconf request, they would be slashed for a safety fault.
- If the active preconfer does not propose a block and the next preconfer does but does not fulfill the preconf request, the second preconfer is slashed for a safety fault.
- If both preconfers have liveness issues, both are slashed for a safety fault. (This can be avoided by chaining beyond 2.)

### Incentivizing Chaining

To incentivize a future active preconfer to chain preconfs, an active preconfer might share tips. Also, a reputational expectation to chain preconfs can encourage more chaining.

One possible way to get chaining adoption is to simply require that chaining happens. To make this practical, the future active preconfers must be able to access the preconf commitments of previous preconfers. The DA problem must be solved to make this practical, and this could be done with an external DA layer. Notably, using an external DA layer introduces dependencies on another sequencer: the DA sequencer. TBD how designs of different DA layers can work around this issue and potential censorship that might occur.

## Conclusion

In this post, we focus on the benefits of chaining for proposers. Widespread chaining also increases the guarantees that users get for preconfirmations, making preconfs even more valuable. It’s a win-win!

Whether forced or opt-in, preconf chaining can protect proposers from being slashed for accidental liveness faults. This system can help proposers feel more comfortable opting into higher collateral requirements.

[![preconf chaining protects proposers from penalties for liveness faults](https://ethresear.ch/uploads/default/original/3X/c/c/cc0abe035c50a142437976c953764a60e774427a.png)preconf chaining protects proposers from penalties for liveness faults553×451 243 KB](https://ethresear.ch/uploads/default/cc0abe035c50a142437976c953764a60e774427a)

#### References

- The Preconfirmation Gateway by mteam (me) mentions chained preconfirmations as better liveness guarantees for users.
- Based preconfirmations by Justin Drake introduces a simple design for based preconfs.
- Pre-confirmation Liveness Slashing Penalties from the Proposer’s Perspective by Sébastien Rannou touches on the liveness slashing problem and explains how it decreases the economic viability of preconfs for proposers.
