---
source: ethresearch
topic_id: 16678
title: "The return of Torus Based Cryptography: Whisk and Curdleproof in the target group"
author: asanso
date: "2023-09-19"
category: Cryptography
tags: [single-secret-leader-election]
url: https://ethresear.ch/t/the-return-of-torus-based-cryptography-whisk-and-curdleproof-in-the-target-group/16678
views: 3542
likes: 14
posts_count: 4
---

# The return of Torus Based Cryptography: Whisk and Curdleproof in the target group

# The return of Torus Based Cryptography: Whisk and Curdleproof in the target group

In the last two years the Ethereum Foundation has been working hard to devise a practical shuffle-based [Single Secret Leader Election](https://eprint.iacr.org/2020/025.pdf) (SSLE) protocol. This dedicated effort by the Ethereum Foundation’s research team has culminated in the creation of two remarkable protocols: [Whisk](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763) and [Curdleproof](https://github.com/asn-d6/curdleproofs/blob/1aa27a68997d023366970a00e12c4aa97465d511/doc/curdleproofs.pdf) (a zero-knowledge shuffle argument inspired by [BG12](http://www0.cs.ucl.ac.uk/staff/J.Groth/MinimalShuffle.pdf)).

A series of posts by [Dapplion](https://twitter.com/dapplion):

- Whisk: Induced missed initial slots
- Whisk: Expensive duty discovery
- Whisk: the bootstrapping problem

accurately describes the status quo.

The problem that we are discussing and trying to solve in this post is the [bootstrapping problem](https://hackmd.io/@dapplion/whisk_bootstrapping). To gain a clearer insight into this challenge, let’s take a moment to revisit the workings of Whisk.

For the rest of this post:

- G_1, G_2 are the BLS12-381 generators
- g_T = e(G_1,G_2)

## Whisk’s recap

As mentioned above Whisk is a proposal to fully implement *SSLE* from `DDH`and `shuffles` scheme (see also section 6 from [Boneh et al paper](https://eprint.iacr.org/2020/025.pdf)).

The idea behind this solution is pretty straightforward and neat. Let’s list below the key ingredients of the commitment scheme in Whisk (at the net of the shuffles):

1. Alice commits to a random long-term secret k using a tuple (rG,krG) (called tracker).
2. Bob randomizes Alice’s tracker with a random secret z by multiplying both elements of the tuple: (zrG,zkrG).
3. Alice proves ownership of her randomized tracker (i.e. open it) by providing a proof of knowledge of a discrete log (DLOG NIZK) that proves knowledge of a k such that k(zrG)==zkrG .
4. Identity binding is achieved by having Alice provide a deterministic commitment com(k)=kG when she registers her tracker.
5. We also use it at registration and when opening the trackers to check that both the tracker and com(k) use the same k using a discrete log equivalence proof (DLEQ NIZK).

Whisk can be implemented in any group where the Decisional Diffie Hellman problem (DDH) is hard. Currently Whisk is instantiated via a commitment scheme in [BLS12-381](https://hackmd.io/@benjaminion/bls12-381).

So far, everything is going well. BUT, the question remains: which long-term secret ‘k’ should be used?

## Bootstrapping problem and de-anonymization

This problem is discussed at length in Dapplion’s post, but just to give you a flavor of the issue, let’s assume we take the easy way and use the validator’s secret signing key k and its associated public key kG_1 for bootstrapping. The issue here is that if the validator signs at least one message where the message M is known (this is usually true for attestation), the validator’s tracker could be de-anonimized forever with a single pairing operation:

e(rG_1, kH(m)) \stackrel{?}{=} e(rk G_1, H(m))

So it is clear that the pairing operation is acting as a de-anonymization oracle.

# Using the target group

In order to contrast the pairing oracle, [Justin Ðrake](https://twitter.com/drakefjustin) proposed  instantiating Whisk using the target group instead.

**Note:** As it is customary, we will switch to multiplicative notation.

## Naive Whisk implementation using the target group

1. Alice commits to a random long-term secret k using a tuple (g_T^r,g_T^{kr}) (called tracker).
2. Bob randomizes Alice’s tracker with a random secret z by exponentiating both elements of the tuple: (g_T^{zr},g_T^{zkr}).
3. Alice proves ownership of her randomized tracker (i.e. open it) by providing a proof of knowledge of a discrete log (DLOG NIZK) that proves knowledge of a k such that (g_T^{zr})^k==g_T^{zkr} .
4. Identity binding is achieved by having Alice provide a deterministic commitment com(k)=g_T^k when she registers her tracker.
5. We also use it at registration and when opening the trackers to check that both the tracker and com(k) use the same k using a discrete log equivalence proof (DLEQ NIZK).

**N.B.:** In case there are concerns about exposing the validator key k, please note that g_T^{kr} is nothing else that e(rG_1.kG_2).

The downsize of this approach respect to the current status quo is that the coordinates of g_T lie in a large finite field \mathbb{F}^*_{p^{12}} in this case. This makes the scheme a considerably slower.

In the next section we show an attempt to improve the situation  a bit.

## XTR and CEILIDH to the rescue

[XTR](https://infoscience.epfl.ch/record/149712?ln=fr) is a Public Key System that was designed by A. Lenstra and E. Verheul presented at  CRYPTO 2000. XTR stands for *Compact Subgroup Trace Representation* and it is based on a clever observation that elements in G_{p^2-p+1}, where a prime order N subgroup G_N \subset G_{p^2-p+1} with N dividing \Phi_6(p)=p^2-p+1, can be compactly represented by their trace over \mathbb{F}^*_{p^2} which is defined by:

Tr: x \rightarrow x + x^{p^2}+x^{p^4}

Lenstra and Verheul showed that if g \in G_{p^2-p+1} and c = Tr(g) then it is possible to work eficiently and compactly using the compressed generator (with some limitations that we explore in the next subsection).

[Here](https://gist.github.com/asanso/1474faee8dab2e5042c643579406e414) you can find an example of the DH protocol implented applying XTR to the target group of the BLS6 curve defined in [this paper](https://eprint.iacr.org/2019/431.pdf).

The XTR cryptosystem works well in the cyclotomic subgroup of \mathbb{F}^*_{p^6} for prime p, although it is possible to generalize it to extension fields \mathbb{F}^*_{q^6} with q = p^m **making it compatible with the target group of BLS12-381.**

### Limitations of XTR

One drawback of using traces, as XTR does, is that the compression is not lossless, which can lead to the mapping of conjugates into identical compressed elements. However, this is not a significant issue since it is possible to employ a trace-plus-a-trit method to compress and decompress elements, much like what is done for elliptic curve compressed points.

Another, more stringent issue to consider is this: performing a single exponentiation (Tr(g^x)) in compressed form is easy, and a double exponentiation (Tr(g^xh^y)) is feasible. However, going beyond that and performing more complex operations in a compressed format is not really feasible (this limitation resembles what we encountered when attempting to translate the SSLE protocol into the isogeny/action group setting). Consequently, the XTR setting may not be suitable for porting all discrete-log cryptosystems. We believe that translating Whisk into the XTR setting is a simple exercise, while more caution needs to be applied to Curdleproof.

### CEILIDH

A significantly cleaner approach to lossless compression can be found in algebraic tori, as introduced [by Rubin and Silverberg](https://eprint.iacr.org/2003/039) in 2003. They presented two novel systems: \mathbb{T}_2, designed as a substitute for LUC and utilizing quadratic extension fields, and CEILIDH, positioned as an alternative to XTR. CEILIDH, pronounced as “Cayley,” was introduced as an acronym representing “Compact, Efficient, Enhancements over LUC, Enhancements over Diffie–Hellman” and is primarily a factor-3 compression and decompression technique designed for “hard” subgroups of sextic extension fields, lacking an efficient exponentiation method. However, it is possible to enhance CEILIDH by combining it with efficient arithmetic over compressed element.

## Conclusion

In an attempt to address the bootstrapping problem in Whisk, we explored the potential of using the target group and discussed the application of XTR and CEILIDH. While XTR does exhibit some limitations, both XTR and CEILIDH present a promising path for achieving lossless compression and improved efficiency in discrete-log cryptosystems.  To the best of our knowledge, this may be the **first deployment of a real-life protocol employing XTR**. We will dedicate time to investigate further and will report back on our findings. For an in-depth overview of XTR and Tori, [refer to the excellent paper by Martijn Stam](https://eprint.iacr.org/2021/1659.pdf).

**Acknowledgments:** We would like to thank Justin Drake, Robert Granger, Ignacio Hagopian, Gottfried Herold, Youssef El Housni, George Kadianakis, Mark Simkin, Dapplion, Michael Scott for fruitful discussions.

## Replies

**mratsim** (2023-09-22):

You might want to include [@yelhousni](/u/yelhousni) in the discussion as he has been using Torus-Based Cryptography to accelerate pairings in ZK circuits.

I’ve been also summarizing how we also could use XTR and Lucas compression in ZK circuits, and potential further improvement alluded by Karabina for Torus-Based Cryptography here: [Faster pairings · Issue #101 · axiom-crypto/halo2-lib · GitHub](https://github.com/axiom-crypto/halo2-lib/issues/101)

---

**mratsim** (2024-07-19):

I’ve added 𝔾ₜ multi-exponentiations to Constantine in [𝔾ₜ multi-exponentiations by mratsim · Pull Request #436 · mratsim/constantine · GitHub](https://github.com/mratsim/constantine/pull/436), no XTR or Torus-based cryptography just endomorphism acceleration + bucket algorithm/Pippenger on 𝔾ₜ.

For single multi-exponentiation vs single scalar multiplication, the ratio between 𝔾₁ and 𝔾ₜ is just 3x.

For multiexp and MSM, the ratio becomes 5x because of the affine formula popularized by Aztec and TurboPlonk that divides by 2 the number of base field mul (https://docs.zkproof.org/pages/standards/accepted-workshop3/proposal-turbo_plonk.pdf)

Benchmarks on a Ryzen 7840U (15W~30W laptop 8-core CPU)

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/3/a3e339e73a143b5253fa0e93eb232d1f8af02521_2_690x281.jpeg)image1280×523 118 KB](https://ethresear.ch/uploads/default/a3e339e73a143b5253fa0e93eb232d1f8af02521)

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/2/c2313338b7e5f609ebe85c3b8500479b726acc39_2_501x500.jpeg)image1280×1276 256 KB](https://ethresear.ch/uploads/default/c2313338b7e5f609ebe85c3b8500479b726acc39)

## Constant-time

I’ve also added constant-time exponentiation so that validators can commit with their private key, using my extremely optimized constant-time routines, the cost of constant-time is only 10% over vartime.

𝔾₁

[![image](https://ethresear.ch/uploads/default/optimized/3X/6/c/6c851bd93bd4e3d71166bd1098efa17f98aa0032_2_690x311.png)image2064×933 336 KB](https://ethresear.ch/uploads/default/6c851bd93bd4e3d71166bd1098efa17f98aa0032)

𝔾ₜ

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/4/1484baf839d13aac5df3e656dea65f7600b3bbf4_2_690x240.png)image1856×647 174 KB](https://ethresear.ch/uploads/default/1484baf839d13aac5df3e656dea65f7600b3bbf4)

Compared to the next best 𝔾ₜ exponentiation from Gnark, Constantine is 2.28x faster due to a combination of factors:

- 4-GLS endomorphism acceleration instead of 2-GLV
- fully lazy reduced tower for field extension
- Fp2 → Fp4 → Fp12 towering instead of the usual Fp2 → Fp6 → Fp12 towering (the tradeoff is that inversion is slower, but inversion can be batched)

[𝔾ₜ exponentiation, with endomorphism acceleration by mratsim · Pull Request #429 · mratsim/constantine · GitHub](https://github.com/mratsim/constantine/pull/429) for benches vs Gnark

[![image](https://ethresear.ch/uploads/default/original/3X/e/3/e3c4e22beb64902778d469426d6871616acd38ad.png)image667×184 17.4 KB](https://ethresear.ch/uploads/default/e3c4e22beb64902778d469426d6871616acd38ad)

---

**mratsim** (2024-12-01):

Since this summer, the Ethereum Foundation has financed a collaboration between Robert Granger, [@asanso](/u/asanso) and I to further accelerate GT multiexp so that if validator privacy becomes a priority again, the performance bottlenecks are cleared out.

I have finished the work this week [Torus-acceleration for multiexponentiation on GT by mratsim · Pull Request #485 · mratsim/constantine · GitHub](https://github.com/mratsim/constantine/pull/485) and I’m happy to announce that for the size of interest (128 and 256 points), multi-exponentiation on ConstantineGT (Fp12, 6x bigger than G1) is only:

- 3x slower than BLST G1 for 128 points
- 3.28x slower than BLST G1 for 256 points

I use blst as reference as every consensus client uses it.

BLST MSM G1

[![blst_g1](https://ethresear.ch/uploads/default/optimized/3X/7/6/76ab2bcb73d3cd2a226f09de12320a93a3a32a0a_2_690x112.png)blst_g11679×274 50.7 KB](https://ethresear.ch/uploads/default/76ab2bcb73d3cd2a226f09de12320a93a3a32a0a)

Constantine MultiExp GT

[![ctt_gt](https://ethresear.ch/uploads/default/optimized/3X/8/6/867b34544f7f2ef1ea8a4597af1641392df2eb85_2_690x437.png)ctt_gt1702×1079 312 KB](https://ethresear.ch/uploads/default/867b34544f7f2ef1ea8a4597af1641392df2eb85)

The new work involves combined Torus-based acceleration with 4-way endomorphism decomposition + projective Torus coordinates to delay/aggregate expensive operations.

There are further optimizations down-the-line which are unfortunately blocked by a Constantine performance bug, despite having up to a raw 1.7x speed advantage on Fp, it dwindles down to only a 1x advantage or worse while building higher-level construct like G1 or GT (Constantine is still the fastest on x86 for BN254_Snarks / BLS12-381 due to state-of-the-art algorithms at each abstraction level).

Another venue for a 2x~3x perf improvement is using SIMD which would allow computing on 4x uint64 (AVX2) or 8x uint64 (AVX512) per instruction instead of 1.

