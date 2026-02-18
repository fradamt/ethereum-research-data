---
source: ethresearch
topic_id: 1639
title: Extending skin-in-the-game of notarization with proofs of custody
author: vbuterin
date: "2018-04-07"
category: Sharding
tags: [proofs-of-custody]
url: https://ethresear.ch/t/extending-skin-in-the-game-of-notarization-with-proofs-of-custody/1639
views: 4314
likes: 3
posts_count: 4
---

# Extending skin-in-the-game of notarization with proofs of custody

One immediate challenge in the notarization mechanism as described [here](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638) is: why would notaries even bother to check if a collation is available? Given that most collations are available, isn’t it too easy to just skip the availability checking step and always vote 1?

One answer comes in the form of [collation availability traps](https://ethresear.ch/t/proposer-withholding-and-collation-availability-traps/1294): if you vote 1 on the availability of some collation, then later on anyone can challenge you by providing the index of some chunk in the collation, and in order to either (i) recover your deposit, or (ii) notarize any further messages, you would need to respond to the challenge by providing the Merkle branch corresponding to that chunk. If a notary fails to respond within some period (eg. two months), then the notary’s entire deposit is lost, and the challenger can get some portion (eg. 33%). This creates an incentive for proposers to sometimes publish unavailable proposals that try to “trap” lazy non-verifying notaries into accepting them, thereby extracting their deposits from them.

![image](https://yuml.me/diagram/scruffy/class/%5Broot%5D%20-%3E%20%5B%20%5D%2C%5Broot%5D%20-%3E%20%5B%20%20%5D%2C%5B%20%5D%20-%3E%20%5BD4%5D%2C%5B%20%5D%20-%3E%20%5BD3%5D%2C%5B%20%20%5D%20-%3E%20%5BD2%5D%2C%5B%20%20%5D%20-%3E%20%5BD1%5D)

But we can strengthen this mechanism further by adding a “proof of custody” mechanism. This works as follows. A notary is required to provide not just a signature of some hash root of the notarized data, but also a Merkle root of an altered data tree, where each 32 byte chunk of data D[i] is replaced by xor(D[i], x) for some value x; the notary must also commit to H(x).

![image](https://yuml.me/diagram/scruffy/class/%5Broot%5D%20-%3E%20%5B%20%5D%2C%5Broot%5D%20-%3E%20%5B%20%20%5D%2C%5B%20%5D%20-%3E%20%5BD4%20xor%20x%5D%2C%5B%20%5D%20-%3E%20%5BD3%20xor%20x%5D%2C%5B%20%20%5D%20-%3E%20%5BD2%20xor%20x%5D%2C%5B%20%20%5D%20-%3E%20%5BD1%20xor%20x%5D)

When challenged with any index i, the notary must provide (i) a Merkle branch of D[i] in the data tree, and (ii) a Merkle branch of xor(D[i], x) in the altered tree; from these two values x can be recovered and checked against the hash commitment provided. **This ensures that the notary must not just be confident that the data will be available (eg. because a few other notaries have already signed off on it), but also that the notary actually has that data themselves at that specific time**, as otherwise they have no way to generate the altered data tree.

Notaries should also be required to publish the preimage of every key that they submit at some point (eg. if the keys are generated in some deterministic fashion, like `k1 = SHA3(masterkey + 0x01)`, `k2 = SHA3(masterkey + 0x02)`, etc, then they would have to eventually publish `masterkey`); this allows auditors to generate the proofs of custody client-side, and check for every collation if the Merkle roots match.

If an auditor computes the signature root and the root that they compute does not match the root that was provided, then an auditor can determine the index where the notary would not be able to respond to the challenge in maximum log(n) steps. The algorithm is as follows:

- Challenge index 0. Wait to receive the Merkle branch.
- Walk down the Merkle branch that they provide until you find a point where the provided tree and your computed agree (this could possibly be the first point; but it definitely hops at least one step down). At that point, the two trees agree on some node A, but disagree on the parent of A, implying that they disagree on the sister of A. Challenge the index corresponding to the node opposite that point.
- Repeat until you’re at the bottom of the tree, and you found a bottom-level index where the provided and computed trees disagree. Challenge that index.

When a challenge succeeds, the deposit of the notary could be split among all challengers, thereby rewarding anyone who helped participate in the binary search process.

The protocol can potentially subsidize some random amount of auditing by giving some proposers the ability to make a “challenge” of whatever index they want to whatever notary they want for free.

## Replies

**jamesray1** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We can increase efficiency by replacing signatures with hashes: replace sig(data, key) with SHA3(key ++ data)

Here’s a cross-reference in which this idea is proposed: [Enforcing windback (validity and availability), and a proof of custody - #2 by kladkogex](https://ethresear.ch/t/enforcing-windback-validity-and-availability-and-a-proof-of-custody/949/2). However this mechanism using zk-S(T/N)ARKs has more overhead and will need more optimizations with STARKs. There’s are linked posts in that article, e.g. this follow-up: [Finality and Windback - Proof of Custody Revisited - #3 by jamesray1](https://ethresear.ch/t/finality-and-windback-proof-of-custody-revisited/1434/3).

---

**jamesray1** (2018-04-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The protocol can potentially subsidize some random amount of auditing by giving some proposers the ability to make a “challenge” of whatever index they want to whatever notary they want for free.

Either that or like Truebit some executors deliberately sometimes publish invalid executions so that verfiers have an incentive to get rewards from verifying. Having a reward for challenging and having a fair probability of actually discovering a bug (deliberate or otherwise) sounds better than a subsidy to make challenges free.

---

**JustinDrake** (2018-04-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This ensures that the notary actually has that data themselves at that specific time

The claim of custody can be extended from covering a single collation body to covering all collation bodies in the notary’s current “storeback” across all shards. That way every vote makes a stronger claim, and the votes collectively form claims of storage across the relevant time and space boundaries.

