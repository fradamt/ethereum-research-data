---
source: ethresearch
topic_id: 1387
title: Fiat-Shamir statistical threshold signatures
author: vbuterin
date: "2018-03-14"
category: Cryptography
tags: []
url: https://ethresear.ch/t/fiat-shamir-statistical-threshold-signatures/1387
views: 2444
likes: 1
posts_count: 6
---

# Fiat-Shamir statistical threshold signatures

Not sure if this idea already already exists under another name, so I’ll call it “Fiat-Shamir statistical threshold signatures” for the moment.

Suppose that you have N users with N public keys (think: N > 1000). You make a shared public key out of a Merkle root of the public keys. Then, any M of the N users can make a construction as follows:

1. The M users all sign some message, H.
2. A Merkle tree of the signatures is made, where the index of each signature in the tree is the same as the index of its corresponding public key in the public key tree (positions in the tree without a signature can be filled with empty data). The Merkle root of the signature tree (possibly with some proof of work grinding) is used as a source of random entropy, which chooses a random k of the leaves of the tree.
3. Any d of these k leaves (think: d/k ~= M/N), together with the Merkle branches proving that they come from the Merkle root, together with the Merkle branches proving the public keys associated with those signatures are actually part of the root public key, can be used as a “signature” to statistically prove that close to M valid signatures for H were actually part of the Merkle tree.

As `k` increases, this scheme becomes statistically more accurate, and comes close to taking the role of a threshold signature scheme. It also has the benefits that:

- It is completely independent of the type of underlying signature used.
- It even allows the underlying signature schemes to be different; each public key could be validation code for some arbitrary signature verification function.
- It is thus (potentially) quantum-resistant.
- It does not require any kind of distributed key exchange.
- Complexity is linear in the number of participants.
- Anyone who participated in a signature, even those who were not included in the random sample, can later prove that they did so.

Its main disadvantages are:

- Large size (32 * k * log(N) + 32 * d * log(N) + d * signature_length)
- It does not generate a unique and manipulation-resistant random value as a byproduct.

## Replies

**MaxC** (2018-03-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Anyone who participated in a signature, even those who were not included in the random sample, can later prove that they did so.

You could also apply the [voting construction](https://ethresear.ch/t/sharding-fast-verifiction-of-voting-tallies-with-merkle-trees/1098) to create a threshold signature. I think that would result in a smaller k (mainly because it avoids sampling negatives) - though the maths would have to be done to be sure.

Edit: apologies, I was mistaken about the branch encoding.  Perhaps a trie construct or a mapping between addresses and numbers could improve efficiency.

---

**kladkogex** (2018-03-15):

I think this is great!)

One thing that needs to be estimated is the value of k for which the signature is secure.

If an attacker possesses a set of X signatures where size(X) < M, and if signatures are not deterministic, then the attacker could do a brute force attack by signing many times, and calculating the Merkle root, to make sure that all d signatures that are revealed belong to x.

If signatures are deterministic, then the attacker can brute force by pretending she has different “fake sets” signatures that include X.  In all cases, the goal of the attacker is to generate and try many different Merkle roots until a root that reveals only the signatures that belongs to X is uncovered.

So PoW to slow down brute force will be required. I think this can still work for the right combination of parameters.

So Vitalik - is this patent free and under GPL ?) Can we use it in the code we are developing (it is under GPL license) - we are looking for all types of threshold signatures …

---

**vbuterin** (2018-03-16):

Yeah, I hereby release all of the above under http://www.wtfpl.net/ and have no interest in patenting it.

---

**kladkogex** (2018-03-16):

Vitalik - Thank you )

---

**dlubarov** (2018-03-17):

Can you explain the motivation for the space optimizations? I.e. why choose a k < N, and why use Merkle proofs rather than broadcasting all signatures? I always figured entropy games would be done on a main chain, probably with only one party giving an input per block, so space wouldn’t be a big concern.

Ignoring space efficiency, the scheme seems similar to

1. Some message H is proposed (maybe a block hash)
2. M users sign H with whatever signature scheme
3. The concatenated signatures become the random seed

In either case each account can manipulate one bit of entropy, by presenting or withholding their signature, assuming that only deterministic signature schemes are allowed. If the last c accounts are colluding, then they can select one of 2^c random seeds, and nobody before them knows how their bits will affect the result. I think that’s reasonable; any advantages from manipulation will be pretty minor depending on how many blocks each seed is used for.

