---
source: ethresearch
topic_id: 1235
title: Cryptographic canaries and backups
author: JustinDrake
date: "2018-02-26"
category: Cryptography
tags: []
url: https://ethresear.ch/t/cryptographic-canaries-and-backups/1235
views: 7404
likes: 14
posts_count: 8
---

# Cryptographic canaries and backups

**TLDR**: We propose a generic approach to safely deploy cryptographic primitives at the protocol-level. We use canary contracts to detect unsafe primitives, and to automatically deploy safer cryptographic backups.

**Background**

We want the Ethereum protocol to endure on the order of centuries yet cryptographic primitives break down on the order of decades. One generic approach to address this is “abstraction” where cryptographic choices are pushed away from the protocol layer towards users and the application layer.

Unfortunately cryptographic abstraction has its limits. In some cases we may want the protocol to enforce homogeneity across all participants (e.g. it’s useful for all Merklelised data structures to use the same hash function), and in other cases one particular cryptographic construct has a set of features that makes it uniquely appropriate for a given task, and not making use of that construct could be a wasted opportunity.

The “wasted opportunity” aspect resonates with considerations around quantum security. At this point the quantum era does seem inevitable and many primitives (e.g. ECDSA, RSA, BLS signatures, SNARKs) are known to be “pre-quantum”, i.e. not be post-quantum secure. However, the dawn of the post-quantum era may not happen for another decade, and the next decade in cryptoland is particularly critical. This makes totally avoiding pre-quantum crypto at the protocol-level a potential strategic mistake.

Below are four examples of fancy/safe pairs of primitives where the fancy (pre-quantum) version is genuinely more powerful than the safe (post-quantum) alternative:

1. Signing: ECDSA has significantly shorter signatures versus Lamport signatures.
2. Voting: Fork-free voting with BLS signatures finalises significantly faster than forkful voting.
3. Random beacons: Dfinity-style random beacons provide significantly better randomness versus blockhashes or a RANDAO approach.
4. Verification: SNARK-based verification is significantly faster than execution-based verification.

The construction below uses cryptographic canaries and backups to simultaneously leverage the power of fancy primitives and the safety of safe primitives.

**Construction**

For every fancy primitive we want to use in-protocol we construct a canary contract with an associated large bounty. My guess is that 50,000 ETH is large enough. Such an amount can be subsidised by the protocol through inflation (0.05% inflation of the total supply is a small price to pay), or could be funded by donations from the community (I’d put 1 ETH ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=9)) and the foundation.

Anyone can redeem the bounty by producing a “proof of cryptographic threat”. The canary can be very specific, e.g. only target BLS signatures. In this case the proof could be a BLS signature matching a nothing-up-my-leave public key (e.g. the binary serialisation of `"Come at me, bro"`). Alternatively the canary can be more general, e.g. target all pre-quantum crypto, where the proof would be a proof of quantum supremacy. A hash-based hiding commitment scheme is used (SHA3 is thought to be post-quantum secure).

We want the canary to be triggered *before* any production crypto is at risk. For that the canary puzzle needs to be made easy enough that only the threat of a breakdown is displayed, not an actual complete breakdown. For example the puzzle in a post-quantum canary would be hard enough for no classical computer to stand a chance, but easy enough for a reasonably-low-qbit quantum computer to crack.

We now pair every fancy protocol-layer mechanism with a safe backup. The backup remains dormant until the canary is triggered. At that point all fancy operations are automatically and immediately shut down, and the safe backup takes over. This applies to system contracts (e.g. the VMC and the FFG contract) as well as to clients for offchain protocol rules (e.g. fork choice rules). Even application-layer contracts can listen to the canary and have their own contingency plan.

## Replies

**kladkogex** (2018-03-01):

I totally agree and would like to offer two little tweaks ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

1. make bounties gradual (start with a particular strength say X bits and pay bounty each time the next bit of strength is cracked)

With RSA challenge the problem was that large organizations that had lots of parallel computational power had huge advantage against independent researchers.

1. Restrict the challenge to a single-threaded algorithm running on a single core that cracks the bounty so that all you need is a PC.  The cracked strength  will be much smaller but it is does not matter so much.  Arguably if you can crack a weaker problem and show the scaling law,  you can easily extrapolate to the stronger problem.

What you want to do is to have many independent researchers working on this thing.

The question is how to enforce the single-threaded property … May be you simply create a group of crypto researchers to attest to the fact  that the canary was cracked on a single core

---

**nate** (2018-03-01):

This is a fun idea ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=9). It reminds me of [this IC3 paper](https://eprint.iacr.org/2017/1090.pdf); essentially, create bug bounties that give people incentive to claim the bug bounty rather than exploit it (and hopefully safely recover from this as well).

That being said, I’m not sure this is totally practical. I think the benefit one would get from hiding their quantum computer and then breaking everything is much greater than they would get from any amount of ETH we might put in a bounty (if they’re evil). And if they aren’t hiding their work, then there really isn’t a need to make this happen automatically.

Also, having the “canary […] be triggered before any production crypto is at risk” seems like a hard problem. It requires us to judge how for the canary breaking is from the quantum computer that breaks everything else. We’d probably have to be very conservative here, in which case let’s just be conservative in a manual manner and not pay a bounty.

---

**kladkogex** (2018-03-02):

I think it is more to stimulate incremental progress in math …

As far a quantum computers go they are totally impractical - I guess the reason why CS people like talking about quantum computers is because they never took quantum mechanics ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

The amount of quantum coherence required by a quantum computer raises exponentially with the number of bits.  Amazing that government still funds these things ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

The real quantum computer is called a semiconductor transistor since electrons in it have a quantum gap. The reason why semiconductors semi-conduct is because of quantum interference. We all already use quantum computers ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**JustinDrake** (2018-03-02):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/n/e95f7d/48.png) nate:

> hiding their quantum computer and then breaking everything

The quantum race is led by established companies (IBM, Intel, Microsoft, Google), startups (Rigetti, IonQ, Quantum Circuits) and possibly governments (NSA, GCHQ). It seems unlikely an established company like IBM would hide their quantum computer for the purpose of breaking everything. As for startups, they are also commercial entities and claiming the “official” Ethereum bounty would be huge PR coup, and a rare “legit” opportunity to claim a significant amount of cash from breaking crypto.

This leaves us with governments… It’s possible that Ethereum will have enough global systemic importance by the time quantum computers are real that they will want to break Ethereum. But then Ethereum seems like a much less likely target than something like, say, military and financial secrets.

---

**sattath** (2023-04-15):

We used this proposal’s main idea to resolve aspects related to (what we call) “quantum procrastinators”: users that would not switch to post-quantum addresses in time, in the context of cryptocurrencies. The eprint is available here: [Protecting Quantum Procrastinators with Signature Lifting: A Case Study in Cryptocurrencies](https://eprint.iacr.org/2023/362) .

At this time, the manuscript wasn’t peer-reviewed. Comments are welcome.

---

**sattath** (2023-08-03):

We also learned that Peter Todd implemented roughly this idea specifically to detect a collision for several hash functions in 2013, see [here](https://bitcointalk.org/index.php?topic=293382.0).

---

**maniou-T** (2023-08-03):

It suggests pairing powerful pre-quantum primitives with safe backups. This approach ensures security while preparing for potential quantum risks. It’s a well-thought-out strategy for navigating cryptographic choices in a changing landscape. Nice

