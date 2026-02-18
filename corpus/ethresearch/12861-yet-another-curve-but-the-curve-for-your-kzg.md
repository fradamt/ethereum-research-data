---
source: ethresearch
topic_id: 12861
title: Yet another curve, but THE curve for your KZG!
author: yelhousni
date: "2022-06-14"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/yet-another-curve-but-the-curve-for-your-kzg/12861
views: 4058
likes: 11
posts_count: 5
---

# Yet another curve, but THE curve for your KZG!

With my co-authors [Aurore Guillevic](https://members.loria.fr/AGuillevic/) and [Diego F. Aranha](https://dfaranha.github.io/), we published on ePrint mid-May a survey of elliptic curves for proof systems ([ePrint 2022/586](https://eprint.iacr.org/2022/586)). Recently, there have been many tailored constructions of these curves that aim at efficiently implementing different kinds of proof systems. In that survey we provide the reader with a comprehensive view on existing work and revisit the contributions in terms of efficiency and security. We present an overview at three stages of the process:

1. curves to instantiate a SNARK,
2. curves to instantiate a recursive SNARK, and
3. curves to express an elliptic-curve related statement.

In this post, we are only interested in the first case. For pairing-based SNARKs, such as the circuit-specific Groth16 [[1]](#1), bilinear pairings (e:\mathbb{G}_1\times \mathbb{G}_2 \rightarrow \mathbb{G}_T) are needed for the proof verification. For universal SNARKs, such as PLONK [[2]](#2) or Marlin [[3]](#3), a polynomial commitment scheme is needed. An example of an efficient one is the Kate-Zaverucha-Goldberg (KZG) scheme [[4]](#4). The verifier needs to verify some polynomial openings using bilinear pairings.

So far, for both circuit-specific and universal constructions, the verification algorithms boil down mainly to pairing computations. However, the prover work is not the same. For Groth16, it is mainly multi-scalar-multiplications (MSM) in *both* \mathbb{G}_1 and \mathbb{G}_2 while for KZG-based schemes it is mainly MSMs in \mathbb{G}_1 *only*. In section 4 of the survey paper, we look at a particular family of pairing-friendly elliptic curves suitable for KZG. We derive algorithm 6 to tailor this family to the SNARK context. Note that KZG is also useful for other compelling applications such as Verkle trees for blockchain stateless clients.

## Pairing-friendly curves

A pairing is a non-degenrate bilinear map

e: \mathbb{G}_1 \times \mathbb{G}_2 \rightarrow \mathbb{G}_T

(P,Q) \mapsto e(P,Q)

where

- \mathbb{G}_1 and \mathbb{G}_2 are groups of order r defined over elliptic curves (with generators G_1 and resp. G_2) and
- \mathbb{G}_T is also a group of order r defined over a finite field extension.

We usually deal with type-3 pairing where

- \mathbb{G}_1 is defined over a curve E(\mathbb{F}_p), \mathbb{G}_2 over E(\mathbb{F}_{p^k}) and
- \mathbb{G}_T over \mathbb{F}_{p^k}.

The integer k is defined as the smallest integer such that r \mid p^k-1 and \mathbb{G}_2 coordinates can be sometimes compressed into a smaller field because \mathbb{G}_2 can be isomorphic to the r-torsion on a different curve E'(\mathbb{F}_{p^{k/d}}) for some d (the twist degree) that characterizes the curve E.

[![pairing-fig2](https://ethresear.ch/uploads/default/optimized/2X/1/15745c5ea6afc3faa216fc1d277b14c2a609ee25_2_690x255.jpeg)pairing-fig23381×1252 135 KB](https://ethresear.ch/uploads/default/15745c5ea6afc3faa216fc1d277b14c2a609ee25)

A pairing-friendly curve construction aims at generating a curve with k not too big (for efficient arithmetic in \mathbb{G}_2 and \mathbb{G}_T) and not too small (for hard discrete logarithm DLP in \mathbb{G}_T). The widely used BLS12-381 curve [[5]](#5), is defined over a field \mathbb{F}_p of size 381 bits and has a prime subgroup order r of 255 bits. It has k=12 so \mathbb{G}_T is over \mathbb{F}_{p^{12}} and d=6 so \mathbb{G}_2 is over \mathbb{F}_{p^2}. This curve is derived from the Barreto-Lynn-Scott of embedding degree 12 (BLS12) family and aims at optimizing the computations in all fronts:

- \mathbb{F}_r: size is 255 bits (1 spare-bit and hard DL)
- \mathbb{G}_1: coordinates over a 381-bit field
- \mathbb{G}_2: coordinates over a 762-bit field (381\times2) and \mathbb{F}_{p^2}[u] is constructed using the irreducible polynomial u^2+1 (p \equiv 3 \mod 4)
- \mathbb{G}_T and pairing: elements over a 4572-bit field and the Hamming weight of the 64-bit Miller loop size (the curve seed for BLS) is just 6.

In some applications as we will see in KZG, not all fronts should be optimized to the same extent. One can for example reduce the size of the \mathbb{G}_1 at the cost of the \mathbb{G}_2 size.

## KZG polynomial commitment

A polynomial commitment scheme allows to commit to a polynomial and then open it at any point (showing that the value of the polynomial at a point is equal to a claimed value, *i.e.* p(z)=y).

### The protocol

- (vk,pk)\leftarrow\texttt{setup}(\tau, 1^\lambda): For some security parameter \lambda, sample randomly \tau \leftarrow \mathbb{F}_r and then compute pk=\tau^iG_1 for i\in\{1,\dots,m\} and vk=\tau G_2.
- C\leftarrow\texttt{commit}(pk,p): given the polynomial p(x)\in \mathbb{F}_r[x] and the proving key pk, compute C=p(\tau)\cdot G_1=\sum_{i=0}^{n[1] https://eprint.iacr.org/2016/260.pdf

[2] https://eprint.iacr.org/2019/953.pdf

[3] https://eprint.iacr.org/2019/1047.pdf

[4] https://www.iacr.org/archive/asiacrypt2010/6477178/6477178.pdf

[5] [BLS12-381 For The Rest Of Us - HackMD](https://hackmd.io/@benjaminion/bls12-381)

[6] [Implement BLS24-319 Curve · Issue #733 · arkworks-rs/algebra · GitHub](https://github.com/arkworks-rs/curves/issues/10#issuecomment-714863120)

[7] https://eprint.iacr.org/2010/104.pdf

---

[![logo_gnark](https://ethresear.ch/uploads/default/original/2X/a/a1ecff6b21ab25cd0c2f413bf9f869b7441064d3.png)logo_gnark640×228 6.37 KB](https://ethresear.ch/uploads/default/a1ecff6b21ab25cd0c2f413bf9f869b7441064d3)

*Author: [Youssef El Housni](https://yelhousni.github.io/).*

*I’m part of a research team at [ConsenSys](https://consensys.net/). If you are interested in our work ([fast finite field arithmetic, elliptic curves, pairings](https://github.com/consensys/gnark-crypto), and [zero-knowledge proofs](https://github.com/consensys/gnark)), [give us a shout](mailto:gnark@consensys.net).*

## Replies

**dausonhoang** (2022-07-09):

Thanks for the post [@yelhousni](/u/yelhousni), in the implementation section, for “BenchmarkKZGOpen-32”, does 32 refer to the size of the data (m)? If not then I am wondering which m was used? It seems both “Commit” and “Open” steps take time linear in m? Thank you.

---

**yelhousni** (2022-07-18):

oh sorry for the confusion [@dausonhoang](/u/dausonhoang). The `-32` suffix denotes the number of CPUs used to run the benchmark, as specified by `GOMAXPROCS` (which is defaulted to the number of cores available on my machine).

---

**dausonhoang** (2022-07-19):

I see [@yelhousni](/u/yelhousni), the computation was run in parallel with 32 cores then. I am wondering how big m is in the experiment? Because obviously the generations of commitments and witnesses (open) depend on m.

---

**yelhousni** (2022-07-19):

`m=2^16` in the benchmarks above. The code is available [here](https://github.com/ConsenSys/gnark-crypto/blob/450e0206211eea38bbb5b5ffddf262efe65bd011/ecc/bls24-317/fr/kzg/kzg_test.go#L327) (`benchSize`).

