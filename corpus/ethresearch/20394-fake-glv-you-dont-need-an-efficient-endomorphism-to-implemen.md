---
source: ethresearch
topic_id: 20394
title: "Fake GLV: You don't need an efficient endomorphism to implement GLV-like scalar multiplication in SNARK circuits"
author: yelhousni
date: "2024-09-09"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/fake-glv-you-dont-need-an-efficient-endomorphism-to-implement-glv-like-scalar-multiplication-in-snark-circuits/20394
views: 1751
likes: 27
posts_count: 10
---

# Fake GLV: You don't need an efficient endomorphism to implement GLV-like scalar multiplication in SNARK circuits

```auto
 _____     _           ____ _ __     __
|  ___|_ _| | _____   / ___| |\ \   / /
| |_ / _` | |/ / _ \ | |  _| | \ \ / /
|  _| (_| |
[Background](#Background)
[The fake GLV trick](#The-fake-GLV-trick6)

- Implementation

Benchmark
- Comparison

## Introduction

P-256, also known as secp256r1 and prime256v1, is a 256-bit prime field Weierstrass curve standardized by the NIST. It is widely adopted in internet systems, which explains its myriad use cases in platforms such as TLS, DNSSEC, Apple’s Secure Enclave, Passkeys, Android Keystore, and Yubikey. The key operation in elliptic curves based cryptography is the scalar multiplication. When the curve is equipped with an efficient endomorphism it is possible to speed up this operation through the well-known [GLV](https://www.iacr.org/archive/crypto2001/21390189.pdf) algorithm. P-256 does unfortunately not have an efficient endomorphism (see [parameters](https://neuromancer.sk/std/nist/P-256#)) to enjoy this speedup.

Verifying ECDSA signatures on Ethereum through precompiled contracts, i.e. smart contracts built into the Ethereum protocol (there are only 9) is only possible with the *secp256k1* curve and not the P-256.

Verifying ECDSA signatures on P-256 requires computing scalar multiplications in Solidity and is especially useful for smart-contract wallets, enabling hardware-based signing keys and safer, easier self-custody. Different solutions can bring P-256 signatures on-chain. There are primarily three interesting approaches: (zk)-SNARK based verifiers, smart contract verifiers (e.g. [[Dubois23]](https://eprint.iacr.org/2023/939.pdf), Ledger/FCL (deprecated), [smoo.th/SCL](https://github.com/get-smooth/crypto-lib) and [daimo/p256verifier](https://daimo.com/blog/p256verifier)), and native protocol precompiles ([EIP/RIP 7212](https://github.com/ethereum/RIPs/blob/196f28d2164f30333b503481e7da954d4bf32ea3/RIPS/rip-7212.md)).

Using SNARK (succinctness) properties, provides a great way to reduce gas cost for computation on Ethereum (e.g. ~232k gas for [Groth16](https://eprint.iacr.org/2016/260.pdf), ~285k gas for [PLONK](https://eprint.iacr.org/2019/953.pdf) and ~185k gas for [FFLONK](https://eprint.iacr.org/2021/1167)). This is very competitive with (and sometimes better that) the currently gas-optimal smart contract verifier. Moreover one can batch many ECDSA verifications in a single proof, amortizing thus the gas cost. However verifying P-256 signatures in a SNARK circuit can be very expensive i.e. long proving time. This is because the field where the points on the P-256 curve lie is different than the field where the SNARK computation is usually expressed. To be able to verify the proof onchain through the procompile the SNARK field needs to be the [BN254](https://hackmd.io/@jpw/bn254) scalar field. Different teams tried to implement the ECDSA verification on P-256 in a BN254 SNARK circuit efficiently. Among these: [zkwebauthn/webauthn-halo2](https://github.com/zkwebauthn/webauthn-halo2), https://github.com/zkwebauthn/webauthn-circom and [PSE/circom-ecdsa-p256](https://github.com/privacy-scaling-explorations/circom-ecdsa-p256).

*If P-256 had an efficient endomorphism we could have optimized the proving time a great deal!*

In this note we show a way to implement a GLV-like scalar multiplications in-circuit without having an efficient endomorphism.

### Other applications

- This technique can be applied to any elliptic curve without an efficient endomorphism (e.g. Curve25519, P-384, MNT-753 (k=4, k=6), STARK curve, \mathcal{B} of “cycle5”, …). See this database for other curves.
- This would question the choice of Bandersnatch (an embedded endomorphism-equipped curve over BLS12-381) over Jubjub (an embedded curve over BLS12-381 without endomorphism) for Ethereum Verkle trees.
- This can speedup ECDSA verification in Starknet and Cairo (through the STARK curve).
- This can speedup natively the folding step (à la Nova) of Ed25519 signatures through the 2-cycles proposed here by Aurore Guillevic.

## Background

### Standard scalar multiplication

Let E be an elliptic curve defined over the prime field \mathbb{F}_p and let r be a prime divisor of the curve order \#E(\mathbb{F}_p) (i.e. the number of points).

Let s \in \mathbb{F}_r and P(x,y) \in E(\mathbb{F}_p), we are interested in proving scalar multiplication s\cdot P over the r-torsion subgroup of E, denoted E[r] (i.e. the subset of points of order r).

The simplest algorithm is the standard left-to-right *double-and-add*:

```auto
INPUT: s = (s_{t−1},..., s_1, s_0), P ∈ E(Fp).
OUTPUT: sP.
1. Q ← ∞.
2. For i from t−1 downto 0 do
    2.1 Q ← 2Q.
    2.2 If s_i = 1 then Q ← Q + P.
3. Return(Q).
```

If/else branching is not possible in SNARK circuits so this is replaced by constant window table lookups inside the circuit. This can be achieved using polynomials which vanish at the constants that aren’t being selected, i.e. a 1-bit table lookup `Q ← s_i * Q + (1 - s_i) * (Q+P)`. Hence this double-and-add algorithm requires t doublings, t additions and t 1-bit table lookup.

This can be extended to *windowed* double-and-add, i.e. scanning more than a bit per iteration using larger window tables, but the multiplicative depth of the evaluation increases exponentially. We use affine coordinates for doubling/adding points because inverses cost as much as multiplications, i.e. instead of checking that 1/x is y we provide y out-circuit and check in-circuit that x\cdot y = 1. However since we start with Q ← ∞ it is infeasible to avoid conditional branching since affine formulas are incomplete. Instead, we scan the bits right-to-left and assume that the first bit `s_0` is 1 (so that we start at `Q ← P`), we double the input point `P` instead of the accumulator `Q` in this algorithm and finally conditionally subtract (using the 1-bit lookup) `P` if `s_0` was 0.

```auto
INPUT: s = (s_{t−1},..., s_1, s_0), P ∈ E(Fp).
OUTPUT: sP.
1. Q ← P.
2. For i from 1 to t−1 do
    2.1 If s_i = 1 then Q ← Q + P.
    2.2 P ← 2P.
3. if s_0 = 0 then Q ← Q - P
4. Return(Q).
```

### GLV scalar multiplication

However it is well known that if the curve is equipped with an efficient endomorphism then there exists a faster algorithm known as [[GLV]](https://www.iacr.org/archive/crypto2001/21390189.pdf).

**Example 1 :** suppose that E has Complex Multiplication (CM) with discrimant -D=-3, i.e. E is of the form y^2=x^3+b, with b \in \mathbb{F}_p. This is the case of `BN254`, `BLS12-381` and `secp256k1` elliptic curves used in Ethereum. There is an efficient endomorphism \phi: E \rightarrow E defined by (x,y)\mapsto (\omega x,y) (and \mathcal{O} \mapsto \mathcal{O}) that acts on P \in E[r] as \phi(P)=\lambda \cdot P. Both \omega and \lambda are cube roots of unity in \mathbb{F}_p and \mathbb{F}_r respectively, i.e. \omega^2+\omega+1 \equiv 0 \pmod p and \lambda^2+\lambda+1 \equiv 0 \pmod r.

**Example 2 :** suppose that E has Complex Multiplication (CM) with discrimant -D=-8, meaning that the endomorphism ring is \mathbf{Z}[\sqrt{−2}]. This is the case of the `Bandersnatch` elliptic curves specified in Ethereum Verkle trie. There is an efficient endomorphism \phi: E \rightarrow E whose kernel is generated by a 2-torsion point. The map can be found by looking at 2-isogeneous curves and applying Vélu’s formulas. For Bandersnatch it is defined by (x,y)\mapsto (u^2\cdot \frac{x^2+wx+t}{x+w},u^3\cdot y\cdot \frac{x^2+2wx+v}{(x+w)^2}) for some constants u,v,w,t (and \mathcal{O} \mapsto \mathcal{O}) that acts on P \in E[r] as \phi(P)=\lambda \cdot P where \lambda^2+2 \equiv 0 \pmod r.

The GLV algorithm starts by decomposing s as s = s_0 + \lambda s_1 and then replacing the scalar multiplication s \cdot P by s_0 \cdot P + s_1 \cdot \phi(P). Because s_0 and s_1 are guaranteed to be \leq \sqrt{r} (see Sec.4 of [[GLV]](https://www.iacr.org/archive/crypto2001/21390189.pdf) and Sec.4 of [[FourQ]](https://eprint.iacr.org/2015/565.pdf) for an optimization trick), we can halve the size of the for loop in the double-and-add algorithm. We can then scan simultaenously the bits of s_0 and s_1 and apply the [Strauss-Shamir trick](https://crypto.stackexchange.com/questions/99975/strauss-shamir-trick-on-ec-multiplication-by-scalar). This results in a significant speed up but only when an endomorphism is available. For example the left-to-right double-and-add would become:

```auto
INPUT: s and P ∈ E(Fp).
OUTPUT: sP.
1. Find s1 and s2 s.t. s = s1 + 𝜆 * s2 mod r
    1.1 let s1 = (s1_{t−1},..., s1_1, s1_0)
    1.2 and s2 = = (s2_{t−1},..., s2_1, s2_0)
2. P1 ← P, P2 ← 𝜙(P) and Q ← ∞.
3. For i from t−1 downto 0 do
    3.1 Q ← 2Q.
    3.2 If s1_i = 0 and s2_i = 0 then Q ← Q.
    3.3 If s1_i = 1 and s2_i = 0 then Q ← Q + P1.
    3.4 If s1_i = 0 and s2_i = 1 then Q ← Q + P2.
    3.5 If s1_i = 1 and s2_i = 1 then Q ← Q + P1 + P2.
4. Return(Q).
```

Using the efficient endomorphism in-circuit is also possible (see [[Halo, Sec. 6.2 and Appendix C]](https://eprint.iacr.org/2019/1021.pdf) or [[gnark implementation]](https://github.com/Consensys/gnark/blob/ea53f373f45d2f9ad9cc1639c34359a35f771191/std/algebra/emulated/sw_emulated/point.go#L530) for short Weierstrass curves and [[arkworks]](https://github.com/zhenfeizhang/bandersnatch-glv) and [[gnark]](https://github.com/Consensys/gnark/blob/dc04a1d3b221dbe7571b5a8394b55d02c2872700/std/algebra/native/twistededwards/scalarmul_glv.go) implementations for twisted Edwards). But one should be careful about some extra checks of the decomposition s = s_0 + \lambda s_1 \mod r (not the SNARK modulus). The integers s_0, s_1 can possibly be negative in which case they will be reduced in-circuit modulo the SNARK field and not r.

## The fake GLV trick

Remember that we are proving that s\cdot P = Q and not computing it. We can “hint” the result Q and check in-circuit that s\cdot P - Q = \mathcal{O}. Now, if we can find u,v \leq \sqrt{r} such that v\cdot s = u \pmod r then we can check instead that

(v\cdot s)\cdot P - v\cdot Q = \mathcal{O}

which is equivalent to

 u\cdot P - v\cdot Q = \mathcal{O}

The thing now is that u and v are “small” and we can, similarly to the GLV algorithm, halve the size of the double-and-add loop and apply the Strauss-Shamir trick.

**Solution**: running the half-GCD algorithm (i.e. running GCD half-way) is sufficient to find u and v. We can apply the exact same trick for finding the lattice basis as in the GLV paper (Sec. 4). For completeness we recall the algorithm hereafter.

We apply the extended Euclidean algorithm to find the greatest common divisor of r and s (This gcd is 1 since r is prime.) The algorithm produces a sequence of equations

w_i \cdot r + v_i \cdot s = u_i

for i = 0, 1, 2, \dots  where w_0 = 1, v_0 = 0, u_0 = r, w_1 = 0, v_1 = 1, u_1 = s, and u_i \geq 0 for all i. We stop at the index m for which u_m \geq \sqrt{r} and take u = u_{m+1} and v = -v_{m+1}.

*Note:* By construction u is guaranteed to be a positive integer but v can be negative, in which case it would be reduced in-circuit modulo the SNARK modulus and not r. To circumvent this we return in the hint u, v and a \texttt{b}=1 if v is negative and \texttt{b}=0 otherwise. In-circuit we negate Q instead when \texttt{b}=1.

### Implementation

A generic implementation in the gnark library is available at [gnark.io (feat/fake-GLV branch)](https://github.com/Consensys/gnark/feat/fake-GLV). For Short Weierstrass (e.g. P256) look at the `scalarMulFakeGLV` [method](https://github.com/Consensys/gnark/blob/62c89cb10cff1413e9d68cce054c7e711d04c726/std/algebra/emulated/sw_emulated/point.go#L1263) in the emulated package and for twisted Edwards (e.g. Bandersnatch/Jubjub) look at the `scalarMulFakeGLV` [method](https://github.com/Consensys/gnark/blob/62c89cb10cff1413e9d68cce054c7e711d04c726/std/algebra/native/twistededwards/point.go#L261) in the native package.

#### Benchmark

The best algorithm to implement scalar multiplication in a non-native circuit (i.e. circuit field ≠ curve field) when an efficient endomorphism is *not* available is an adaptation of [[Joye07]](https://www.iacr.org/archive/ches2007/47270135/47270135.pdf) (implemented in [gnark here](https://github.com/Consensys/gnark/blob/fdb2b0de422b1c4fc5c6d08e81e788095ac818a6/std/algebra/emulated/sw_emulated/point.go#L748)).

Next we compare this scalar multiplication with our fake GLV in a PLONKish vanilla (i.e. no custom gates) circuit (scs) over the BN254 curve (Ethereum compatible). We also give benchmarks in R1CS.

| P-256 | Old (Joye07) | New (fake GLV) |
| --- | --- | --- |
| [s]P | 738,031 scs  186,466 r1cs | 385,412 scs  100,914 r1cs |
| ECDSA verification | 1,135,876 scs  293,814 r1cs | 742,541 scs  195,266 r1cs |

> Note here that the old ECDSA verification uses Strauss-Shamir trick for computing [s]P+[t]Q while the new version is merely two fake GLV multiplications and an addition.

#### Comparison

[p256wallet.org](https://www.p256wallet.org/) is an ERC-4337 smart contract wallet that leverages zk-SNARKs for WebAuthn and P-256 signature verification. It uses [PSE/circom-ecdsa-p256](https://github.com/privacy-scaling-explorations/circom-ecdsa-p256) to generate the webAuthn proof, and underneath [PSE/circom-ecdsa-p256](https://github.com/privacy-scaling-explorations/circom-ecdsa-p256) to generate the ECDSA proof on P-256 curve. The github README reports `1,972,905 R1CS`. Compiling our circuit in R1CS results in **`195,266 R1CS`**. This is more than a **10x** reduction, which is not only due to the fake GLV algorithm but also to optimized non-native field arithmetic in gnark.

#### Other curves

Similar results are noticed for other curves in short Weirstrass, e.g. P-384 and STARK curve:

| P-384 | Old (Joye07) | New (fake GLV) |
| --- | --- | --- |
| [s]P | 1,438,071 scs | 782,674 scs |
| ECDSA verification | 2,174,027 scs | 1,419,929 scs |

| STARK curve | Old (Joye07) | New (fake GLV) |
| --- | --- | --- |
| [s]P | 727,033 scs | 380,210 scs |
| ECDSA verification | 1,137,459 scs | 732,131 scs |

and also in twisted Edwards e.g. Jubjub vs. Bandersnatch:

| Jubjub | Old (2-bit double-and-add) | New (fake GLV) |
| --- | --- | --- |
| [s]P | 5,863 scs  3,314 r1cs | 4,549  scs  2,401 r1cs |

| Bandersnatch | Old (GLV) | New (fake GLV) |
| --- | --- | --- |
| [s]P | 4,781 scs   2,455 r1cs | 4,712 scs  2,420 r1cs |

---

*EDIT: Thanks to [Ben Smith](https://www.lix.polytechnique.fr/~smith/) for reporting that a similar idea was proposed in [[SAC05:ABGL+]](https://cacr.uwaterloo.ca/techreports/2005/cacr2005-28.pdf) for ECDSA verification. We note that, in our context, the trick applies to a single scalar multiplication and that the half GCD is free through the hint.*

## Acknowledgement

I would like to thank Arnau Cube, Aard Vark, Holden Mui, Olivier Bégassat, Thomas Piellard and Ben Smith for fruitful discussions.

## Replies

**Liam-Eagen** (2024-09-10):

Very cool!

A related but under appreciated trick can be used to combine both the normal GLV trick and this “fake GLV” trick. Let E be a curve with an order r subgroup and with efficient CM endomorphism \phi : E \rightarrow E corresponding to multiplication \phi(P) = [a] P where f(a) = 0 \bmod r on the order r subgroup. Let \mathbb{K} = \mathbb{Q}[\alpha]/f(\alpha) be the associated CM number field and let (r_0, r_1) be the smallest values such that r \mid N(r_0 + \alpha r_1).

To show Q = [s] P we can first find (s_0, s_1) such that s = s_0 + a s_1 \bmod r (the ordinary GLV endomorphism trick) and then write s_0 + \alpha s_1 = (u_0 + \alpha u_1) / (v_0 + \alpha v_1) \bmod (r_0 + \alpha r_1) by applying the half gcd algorithm in more or less exactly the same way to s_0 + \alpha s_1 and r_0 + \alpha r_1 over \mathbb{K}. The values u_0, u_1, v_0, v_1 are all about r^{1/4} (up to a constant factor).

Technically this requires that the number field \mathbb{K} be a euclidean domain, which is the case for j invariant 0 (\alpha = \frac{1+ \sqrt{-3}}{2}) and 1728 (\alpha = \sqrt{-1}) curves as well as Bandersnatch since \alpha = \sqrt{-2}, but is not in general true. More generally it suffices to find a short vector (not necessarily the shortest) in the lattice

\mathcal{L} = \{ (u_0, u_1, v_0, v_1, q) : u_0 + u_1 \alpha - v_0 s - v_1 s \alpha + r q = 0 \}

which is always possible using standard lattice reduction techniques like LLL or BKZ. Then to check Q = [s] P it suffices to check [u_0] P + [u_1] \phi(P_1) - [v_0] Q - [v_1] \phi(Q) = \mathcal{O}. This would allow us to apply both tricks to e.g. Bandersnatch and enjoy even better Pippenger-like speed up as a 4-msm.

---

**yelhousni** (2024-09-10):

That is so cool!

Indeed it seems we can turn a single scalar multiplication to a 4-dimensional GLV-like algorithm!

---

**mratsim** (2024-09-18):

Romain Dubois ([@rdubois-crypto](/u/rdubois-crypto)) proposed the same “fake-GLV” acceleration but for generic ScalarMul in smart contracts in April: [RIP-7696 : generic Double Scalar Multiplication (DSM) for all curves - RIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/rip-7696-generic-double-scalar-multiplication-dsm-for-all-curves/19798)

---

**yelhousni** (2024-09-18):

Not really. The speedup is comparable but the technique used is different (rational reconstruction of scalar + hinted result vs. precomputation of [2^{128}]P but one needs to trust this input in Solidity). I shared this writeup with Renaud Dubois before publishing it here and we are now discussing if both tricks can be combined in a Solidity context.

---

**yelhousni** (2024-09-18):

The idea of Liam to first apply GLV and then the “fake GLV” by doing a half GCD in the number field \mathbb{K} works for curves of j-invariant 0 and 1728. Basically the half GCD in Eisenstein and Gauss ring of integers works the same as in \mathbb{Z}. [Here](https://gist.github.com/yelhousni/5d175ba601be3dac86c1c05070861675) is a working example in sagemath for `secp256k1` (j=0). However it does not seem to be working for Bandersnatch \mathbb{K}=\mathbb{Q}[\sqrt{-2}] as the geometry is different. So the remark on Jubjub/Bandersnatch still holds IMO.

> This would question the choice of Bandersnatch (an embedded endomorphism-equipped curve over BLS12-381) over Jubjub (an embedded curve over BLS12-381 without endomorphism) for Ethereum Verkle trees.

---

**rdubois-crypto** (2024-10-15):

The technics are actually very similar once the “extra bases” are obtained. If the input can be trusted, which is the case for a signature verification with non ZK (here it is meant true ZK, not validity but privacy preserving), and for classical VM (where shifts are cheaps), DSM is more efficient.

But for circuits, where shifts are as expansive as multiplications, the cost is equivalent, and does enable privacy (such as ZKpasseport/ZKmail use cases) because the input are not to be trusted, so Fake GLV is superior here in all aspects.

---

**defitricks** (2024-10-16):

How does the Fake GLV approach mitigate the need for an efficient endomorphism while maintaining computational efficiency in SNARK circuits, and could this method have broader implications for elliptic curve cryptography beyond zero-knowledge proofs?

---

**yelhousni** (2024-10-16):

Morally you would use the expected result (free through a hint in SNARK circuits) as the second point (equivalently to the image of the input point by the endomorphism in the normal GLV). Implementations of both the fake GLV and the 4D version of [@Liam-Eagen](/u/liam-eagen) are implemented in gnark here: [Feat: 4-dimensional fake GLV by yelhousni · Pull Request #1296 · Consensys/gnark · GitHub](https://github.com/Consensys/gnark/pull/1296)

---

**yelhousni** (2025-11-25):

Just wanted to mention that the ideas discussed here (fakeGLV, GLV+fakeGLV), their extensions to 2-MSM, formalisms through lattice reduction, proven algorithms bounds and corresponding implementations have been published in Latincrypt with my co-authors Simon Masson, Thomas Piellard and Liam Eagen: [Fast Elliptic Curve Scalar Multiplications in SN(T)ARK Circuits | SpringerLink](https://link.springer.com/chapter/10.1007/978-3-032-06754-8_4) ([eprint 2025/933](https://eprint.iacr.org/2025/933.pdf))

