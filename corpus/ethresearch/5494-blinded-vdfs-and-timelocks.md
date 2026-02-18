---
source: ethresearch
topic_id: 5494
title: Blinded VDFs and timelocks
author: JustinDrake
date: "2019-05-22"
category: Sharding
tags: [verifiable-delay-functions]
url: https://ethresear.ch/t/blinded-vdfs-and-timelocks/5494
views: 2163
likes: 4
posts_count: 3
---

# Blinded VDFs and timelocks

**TLDR**: We show a simple technique to blind VDF and timelock outputs. More specifically, let g be an element in a group of unknown order. We show how to prove knowledge of x = g^{2^t} without revealing intermediate outputs g^{2^s} for s \le t.

**Construction**

Simply reveal x^3 with a corresponding Wesolowski proof. (Notice the Wesolowski scheme works for arbitrary exponents, not just powers of two.) More concretely, the prover reveals:

- x^3 = g^{3*2^t}
- p = g^{\lfloor{3*2^t/l}\rfloor} where l is a 256-bit prime deterministically generated from x^3

The verifier checks p^lg^{3*2^t \mod l} = x^3.

**Blindness argument**

(*Note*: This is not a formal cryptographic proof. Feedback and corrections welcome.)

Notice g^{2^s} cannot be extracted from g^{3*2^t} for s \le t because that would be taking the 3*2^{t - s} th root of x^3 and taking roots is assumed to be hard in an RSA group. Also, the sequentiality assumption implies that g^{2^s} for s > t cannot be computed from g^{3*2^t} without computing g^{2^s - 3*2^t}. At best s = t+2 and g^{2^{t+2} - 3*2^t} = x must be computed first.

Similar blindness arguments apply to p. Indeed, the repeated square g^{2^s} cannot be extracted from p if 2^s < \lfloor3*2^t/l\rfloor by the roots assumption. And g^{2^s} cannot be computed from p if 2^s \ge \lfloor3*2^t/l\rfloor without first computing g^{2^s - \lfloor3*2^t/l\rfloor} which requires (except with negligible probability) essentially as much work as computing x (because l has 256 bits and 2^t has t \gg 256 bits).

**Motivation**

Blinding of repeated squares was motivated by the [refreshed LCS35 puzzle](https://ethresear.ch/uploads/default/original/2X/4/43d9e05fc637498b8dba3720407b3211f90ff280.txt) where intermediate outputs are welcome:

> CSAIL is also interested in solutions for t = 2 ^ k for 56/2 <= k < 56; these are called “milestone versions of the puzzle”

The above scheme allows to prove that milestone versions of the puzzle were computed without revealing them, and hence protecting against someone building upon them. The scheme may also be helpful in other contexts such as iterated VDFs.

## Replies

**Rjected** (2019-05-24):

This is pretty cool, although you mention RSA group here:

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> and taking roots is assumed to be hard in an RSA group

When the group is just assumed to be of unknown order, not necessarily an RSA group. The conclusion is totally the same but it might be a good thing to keep consistent.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Also, the sequentiality assumption implies that g^{2^s} for s>t cannot be computed from g^{3*2^t} without computing g^{2^s - 3*2^t}. At best s=t+2 and g^{2^{t+2} - 3*2^t} = x must be computed first.

While g^{2^s} cannot be calculated from g^{2^t} for s > t, it might be possible for an adversary to compute a g^{3*2^{t+n}} and corresponding p' without knowledge of x.

For an adversary to create a proof for a checkpoint g^{2^s}, where s = t + n, is there no reason why they can’t just raise the x^3 (as revealed by the prover in a previous proof for x) to a power 2^n? So x^{\prime3} = {x^{3}}^{2^n} = x^{3*2^n} = g^{3*2^t*2^n}=g^{3*2^{t+n}}. In this case the adversary does not know x^{\prime} yet they have generated an x^{\prime3} without doing any of the previous sequential work. This way an adversary could essentially compute a proof of the same form, starting the proof for x. Since the previous l was generated using x^3, an l' can be generated (I assume hash into primes) from x^{\prime3} and therefore used to calculate p^{\prime}=g^{⌊3*2^{t+n}/l^{\prime}⌋}, completing the Wesolowski proof. This doesn’t contradict the fact that x is blinded, but it might not prove knowledge for s>t. Does this work?

---

**JustinDrake** (2019-05-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/rjected/48/15266_2.png) Rjected:

> When the group is just assumed to be of unknown order, not necessarily an RSA group. The conclusion is totally the same but it might be a good thing to keep consistent.

Right ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I meant group of unknown order here. (I’ve been studying RSA groups specifically in the context of VDFs and sometimes equate the two.)

![](https://ethresear.ch/user_avatar/ethresear.ch/rjected/48/15266_2.png) Rjected:

> Does this work?

Ah, yes. Well spotted! A fix may be to replace the prime 3 with one that is associated with the hash of a public key. Alternatively, one could pick a different prime per checkpoint (e.g. 3 for the first, 5 for the second, 7 for the third, etc.) for the refreshed timelock puzzle.

