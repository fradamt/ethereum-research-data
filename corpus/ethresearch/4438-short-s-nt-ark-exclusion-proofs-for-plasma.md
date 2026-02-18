---
source: ethresearch
topic_id: 4438
title: Short S[NT]ARK exclusion proofs for Plasma
author: snjax
date: "2018-12-01"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/short-s-nt-ark-exclusion-proofs-for-plasma/4438
views: 3836
likes: 1
posts_count: 5
---

# Short S[NT]ARK exclusion proofs for Plasma

# Short S[NT]ARK exclusion proofs for Plasma

Reading [STARK-based accumulators](https://ethresear.ch/t/a-sketch-for-a-stark-based-accumulator/4382) proposed by [@vbuterin](/u/vbuterin), I summarize that current prooving schema looks so:

1. Arbitrary slices
2. Aligned slices
3. STARK-based accumulator
4. STARK-based exclusion proof for history reduction

Let’s consider some reduction of these stages up to:

1. Arbitrary slices
2. S[NT]ARK-based exclusion proof for history reduction

We do not need to do anything with aligned slices (\div \log N complexity) and do not need to do anything with inclusion/exclusion proof for the aligned slices (also \div \log N complexity).

As it turned out, zk-SNARKs are useful to make batch exclusion Merkle proof for Plasma Cashflow.

The state of Plasma Cashflow is looking something like this:

[![plasma cashflow state](https://ethresear.ch/uploads/default/original/2X/e/e2c583d55559acdbbd07830ae7eb3bf32b817745.svg)](https://raw.githubusercontent.com/snjax/drawio/master/plasma%20cashflow%20state.svg?sanitize=true)

[View with better resolution.](https://raw.githubusercontent.com/snjax/drawio/master/plasma%20cashflow%20state.svg?sanitize=true)

The space of plasma at the picture equals to `[0, 1000000)`. So, each block contains this interval inside the root node. There are transactions included in the block and voids inside the leaves.

It is enough to prove the existence of a NULL node at the current slice for any chunk of blocks to prove exclusion of the slice.

We do not need to prove tx validity, signatures or something like this. Here is the example circuit written on pseudocode, it is a very simple construction with Merkle prooves inside only:

```auto
gadget ExclusionProof(slice, blockSum:public, nullIntervals[N], sumMerkleProof[N] :private)
  for i:= 1..N:
    root[i]:=SumMerkleProof(nullInterval[i], NULL, sumMerkleProof[i])
    nullInterval[i].x1 <= slice.x1
    slice.x2 <= nullInterval[i].x2
  blockSum == hashsum(root)
```

Below I represent computations for 10k tps plasma with one block per 5 minutes publishing:

There are about `3000000` tx per block. The Merkle tree depth is `22`. If we use 160bit cryptography, there are about 30k constraints per block. If we use 10M constraint SNARK, it can prove 300 blocks with 300 bytes proof size.

Raw Merkle proof of 300 blocks weights 300 kilobytes. So, we got x1000 disk space reduction to store the history.

There are 100k 5minute blocks per year, so the history of the coin without reduction weights about 100 Mb and history of the coin with reduction weights 100 kb.

The S[NT]ARKs do not need to be checked onchain. That means that STARKs and recursive SNARKs may be used. One thing we need to implement onchain: plasma state and challenges using S[NT]ARK-friendly hash functions. We can do it not expensive through truebit or SNARKs+truebit.

# Related links

@barryWhiteHat [Roll_up / roll_back snark side chain ~17000 tps](https://ethresear.ch/t/roll-up-roll-back-snark-side-chain-17000-tps/3675)

@vbuterin [A sketch for a STARK-based accumulator](https://ethresear.ch/t/a-sketch-for-a-stark-based-accumulator/4382)

[Plasma call #16](https://www.youtube.com/watch?v=0ApUUoWYt8U)

[Plasma cashflow spec](https://hackmd.io/DgzmJIRjSzCYvl4lUjZXNQ?view)

@vbuterin, [RSA Accumulators for Plasma Cash history reduction](https://ethresear.ch/t/rsa-accumulators-for-plasma-cash-history-reduction/3739)

Alessandro Chiesa, Lynn Chua, Matthew Weidner [On cycles of pairing-friendly elliptic curves](https://arxiv.org/pdf/1803.02067.pdf)

Eli Ben-Sasson, Alessandro Chiesa, Eran Tromer, Madars Virza [Scalable Zero Knowledge via Cycles of Elliptic Curves](https://eprint.iacr.org/2014/595.pdf)

## Replies

**vbuterin** (2018-12-01):

The reason to use hash-chain accumulators rather than Merkle proofs is that with a Merkle tree you need to check 22 hashes, so there’s a ~22x increase in the amount of proving you need to do per value. Also, the implementation complexity goes up considerably (eg. it risks getting to the point where you can’t hand-roll a STARK, you need to use an HLL, which adds overhead and bug surface area…)

My understanding is that at present with reasonably optimized SNARKs and using MIMC you can prove a branch in ~2 seconds. With STARKs you can get that down to ~0.2, and replacing the Merkle branch with a hash chain ~0.01, and probably even less with improved hash functions (Jarvis?) so you get to the point where it actually is viable for a Plasma server.

---

**snjax** (2018-12-01):

Thank you for your explanation! I consider the accumulators on zk-STARKS as promising construction.

I see one issue in the accumulators: we need to push \sim (\log N)^2 objects inside it to prove the inclusion of one arbitrary slice.

Now I am working at reducing the size of log-proofs. At the current stage, we can reduce inclusion proof size up to 5 times and increase exclusion proof size up to 2 times (or vise versa).

We are going to check the accumulators with STARK-friendly hash functions in our plasma

---

**vbuterin** (2018-12-02):

See [@karl](/u/karl)’s work in making plasma prime work by assigning primes to slices instead of fixed coin IDs. You can get the complexity down to O(1) by doing it that way.

---

**snjax** (2018-12-04):

I have overviewed last [@karl](/u/karl)’s works on Plasma, but have not seen the solution. Perhaps, [@karl](/u/karl) is planning to commit the solution [here](https://github.com/karlfloersch/research), but it is still tagged “top secret”.

Also, we have discussed the O(1) solution in our workshop after the devcon4 and found history split issue: the plasma operator can forge queer chains and hide them from honest users. Users can easily prove the consistency and validity of the real chain offchain. But plasma operator can try to exit from a queer chain and it is not easy to expand history back onchain and find the defect.

![chains](https://ethresear.ch/uploads/default/original/2X/9/96f1a3ee2f8325f729cc26846c6685687da66c39.svg)

I did not look at the problem intently, but now I see, that the complexity is about \log_2 M, where M is a number of transactions with the coin in the real chain from the deposit or checkpoint.

There is not so a huge number of challenges for coin used once per day (lesser than 9 steps for a year) and more complex problem for coin used every 5 minutes (17 steps for a year). The steps can be batched (for example, \times 8 for one request size and \div 3 for a number of requests).

Probably I missed the best solution. So, I have a question: have you got constant time challenges in your O(1) prime number plasma spec?

