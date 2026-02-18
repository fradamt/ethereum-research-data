---
source: ethresearch
topic_id: 1835
title: Fork-free RANDAO
author: JustinDrake
date: "2018-04-26"
category: Sharding
tags: []
url: https://ethresear.ch/t/fork-free-randao/1835
views: 2842
likes: 1
posts_count: 3
---

# Fork-free RANDAO

**TLDR**: We combine a RANDAO scheme with a threshold mechanism to force-reveal preimages of inactive participants. Thanks to Bernado David (author of SCRAPE) for feedback and suggestions.

**Construction**

For registration, a participant P picks a secret s and posts onchain a hashchain commitment c = H^{1024}(s). After some time, P is assigned an honest-majority committee to which he must respond with publicly verifiable shares of s and a zk-proof that the shares faithfully correspond to c. Specific constructions:

- PVSS: We use the SCRAPE construction for the shares of the secret s. Using n/2 exponentiations where n is the size of the committee we build a DLOG-based commitment of the form h^s where h is a random group generator.
- zk-proof: We build a zkSNARK that s is the 1024th preimage of c and that the same s is the exponent in the commitment h^s.

At every round a participant is selected to reveal his next hashchain preimage. If he does not, the committee corresponding to the participant reconstructs his secret, submit the preimage on his behalf, and the inactive participant is slashed.

**Discussion**

With a 50%+ honest majority assumption the above construction yields a fork-free grinding-free RANDAO. In the default case a single message is required to generate the next RNG output. In the exceptional case, n/2 messages are required.

The most expensive part of the setup phase is the zk-proof that s is the 1024th preimage of c. As benchmarked by Jacob Eberhardt, it takes 5 seconds per 64 hashes. So the setup phase would require ~2 minutes of compute time for each participant.

Assuming 1,000 participants and 5-second periods, the registration phase must be renewed every 1000 * 1024 * 5 / 60 / 60 / 24 ~= 60 days (one “era”).

## Replies

**tawarien** (2018-04-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> For registration, a participant PP picks a secret ss and posts onchain a hashchain commitment c=H1024(s)c = H^{1024}(s). After some time, PP is assigned an honest-majority committee to which he must respond with publicly verifiable shares of ss and a zk-proof that the shares faithfully correspond to cc.

why do we need a repeated hash for the commitment? Would a single application c=H(s) not work equally well? This would make the zk-proof considerably easier.

---

**JustinDrake** (2018-04-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> why do we need a repeated hash for the commitment? Would a single application c=H(s) not work equally well?

It wouldn’t work as well because the setup phase (PVSS + zk-proof) would have to be repeated at every period (as opposed to once every 1024 periods). Redoing and sharing new PVSS shares would cause bandwidth and computation overhead.

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> This would make the zk-proof considerably easier.

The extra zkSNARK costs (namely 1024 / 64 * 5 = 80 seconds once per era) is marginal.

