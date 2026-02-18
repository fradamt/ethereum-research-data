---
source: ethresearch
topic_id: 5626
title: Batching of zk-SNARK proofs
author: snjax
date: "2019-06-18"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/batching-of-zk-snark-proofs/5626
views: 3560
likes: 7
posts_count: 7
---

# Batching of zk-SNARK proofs

For proof (A,B,C), verification key (\alpha, \beta, \gamma, \delta, I_n) and input data x_i, the groth16 proof is

(X, \gamma) + (C, \delta) + (\alpha, \beta) - (A, B) = O, where O is zero point and X = I_0 + \sum\limits_{i=1}^{n} I_i x_i.

For proof batching we can use approach, presented at [Fast verification of multiple BLS signatures](https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407) by [@vbuterin](/u/vbuterin) and use set of batcing multipliers r_i.

(\sum X_i r_i, \gamma) + (\sum C_i r_i, \delta) + (\sum r_i \alpha, \beta) - \sum (r_i A_i, B_i) = O.\ \ \ \ \ \ \ \ \ \ (1)

Here is 3+N pairing operations instead of 4N.

If the attacker knows {r_i}, the proof may be forged by simple way for any two or more batched proofs:

C_i := 0,

(A_0, B_0) := (\frac{1}{r_0} \sum X_i r_i, \gamma),

(A_1, B_1) := ((1+\frac{r_0}{r_1})\alpha, \beta).

If we substitute these expressions into (1), we get proof for any public inputs. The forged proof may be computed by miner, somebody, who knows expected r_i or directly onchain if the source of r_i is available for the attacker’s contract.

We can determine r_i as hash of input data. Similar approach is using in zkSTARKS to select branches of Merkle tree for the proof:

s := H(\{A_i, B_i, C_i, X_i\}),

r_0 := 1,\ r_i = H(s, i).

In such case the batching is not so vulnerable.

## Replies

**AlexandreBelling** (2019-06-19):

This seems like a legit application of the Fiat-Shamir heuristic and it should be secure in the Random Oracle Model. I wonder whether we could leverage this for efficient zk-SNARK proof aggregation.

---

**khovratovich** (2019-06-19):

Yes you can do that, as well as some other tricks, as described in the 1998 paper https://cseweb.ucsd.edu/~mihir/papers/batch.pdf, from where Vitalik’s idea is actually derived.

---

**shamatar** (2019-06-22):

There is a “practical” aspect that comes from current precompile implementation (BN curve) of the current version of Ethereum and should be transferred for all next implementations. At the moment point of infinity is not expressible as affine point that is used by the precompile, so C == 0 will cause transaction rejection. While such transformation is “cheap”, the attack is not applicable at the current state of the network.

---

**snjax** (2019-06-22):

Just replace C_i:=0 with C_0 := - \frac{r_1}{r_0} C_1 for any random nonzero C_1.

Anyway, the pairing check is carried out, and no zero points are used.

---

**vbuterin** (2019-06-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/shamatar/48/670_2.png) shamatar:

> At the moment point of infinity is not expressible as affine point that is used by the precompile

That’s actually not true. See [the EIP](https://eips.ethereum.org/EIPS/eip-197), specifically:

> Elliptic curve points are encoded as a Jacobian pair (X, Y) where the point at infinity is encoded as (0, 0) .

---

**shamatar** (2019-06-22):

Hello Vitalik.

Yeah, looks so. We were checking Geth and Parity implementations yesterday and I had an impression that “point of infinity” as input for pairing operations would be rejected with error. Checked Geth today and it doesn’t looks so. With a recent addition of another way of taking a proof looks like FS transformation is strictly required.

