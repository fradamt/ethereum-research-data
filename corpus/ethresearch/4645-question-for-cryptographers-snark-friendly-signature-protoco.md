---
source: ethresearch
topic_id: 4645
title: "Question for cryptographers: SNARK friendly signature protocol"
author: snjax
date: "2018-12-21"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/question-for-cryptographers-snark-friendly-signature-protocol/4645
views: 5760
likes: 6
posts_count: 8
---

# Question for cryptographers: SNARK friendly signature protocol

Now we are building plasma with SNARKs friendly state and I think that proving also the signatures inside the SNARK may be a good idea because in future it provides us transaction history compression.

Is it safe to build ECDSA on jubjub and Pedersen hash? The circuit for ECDSA is using about 10000 constraints, but I have not seen the usage of this approach anywhere.

Most of the projects are using much heavier sha256 and EdDSA.

## Replies

**barryWhiteHat** (2018-12-22):

It should be safe to build ECDSA inside a snark. I think ECDSA requires a greater than check which is quire expensive in the snark. But still totally possible.

Eddsa does not require this so thats why it was a natural option. Schnorr could work quite well inside a snark.

> The circuit for ECDSA is using about 10000 constraints, but I have not seen the usage of this approach anywhere.

Can you share this implmentation?

> Most of the projects are using much heavier sha256 and EdDSA.

We are seeing if pedersen commitments are safe inside a signature scheme and potentially moving to use that.

---

**snjax** (2018-12-22):

We have not implemented it in Bellman yet. But I can share here current draft pseudocode.

I will use notation from [wiki](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm). We get signature (r, s), public key Q_A and group element G with order n, message hash z. All integers inside the SNARK are elements of Z_p.

To verify the signature we need to check following equations::

0 < r < n \\
0 < s < n \\
Q_A \neq O \\
Q_A \in Curve \\
n Q_A = O \\
z (s^{-1} G) + r (s^{-1} Q) = (x_1, y_1) \neq O \\
x_1 = r \mod n

For circuit simplification we can transform (r, s) signature into (r_1, s_1) signature, where r_1 = r s^{-1} \mod n, s_1 = s^{-1} \mod n.

Arbitrary conditional point addition gets 8 constraints, point addition gets 6 constraints, point doubling gets 5 constraints, so we get 13 constraints per bit arbitrary point multiplication.

Constant point multiplication is described [here](https://z.cash/technology/jubjub/): 4.2 constraints per bit.

We can exclude checks for Q inside the circuit. Then the circuit will not reject wrong public keys, but plasma users are conserned to use valid public keys and consider inclusion of wrong keys as defect in plasma. So we get following system of equations:

0 < r_1 < n \\
0 < s_1 < n \\
z (s_1 G) + r_1 Q = (x_1, y_1) \neq O \\
x_1 s_1 = r_1 \mod n

We consider r_1, s_1 as elements of Z_n and transform equation system into

z (s_1 G) + r_1 Q = (x_1, y_1) \\
x_1 (s_1 G) = (r_1 G) \neq O

We can do it, because O=(0,1) for jubjub, so, x_1,\ s_1,\ r_1 \neq 0 \mod n and (x_1, y_1) \neq O here.

Here is the SNARK in pseudocode:

```python
def ecdsa_check(z, r_1, s_1, Q):
    split_to_bits(z) # 252 constraints
    split_to_bits(r_1) # 252 constraints
    split_to_bits(s_1) # 252 constraints
    C0 := ec_mulc(s_1, G) # 4.2 * 252 = 1058 constraints
    C1 := ec_mul(z, C0) # 13 * 252 = 3276 constraints
    C2 := ec_mul(r_1, Q) # 13 * 252 = 3276 constraints
    x1 := X(C1+C2) # 6 constraints
    split_to_bits(x1) # 254 constraints
    C3 := ec_mulc(r_1, G) # 4.2 * 252 = 1058 constraints
    C4 := ec_mul(x, C0) # 8 * 254 = 2032 constraints, using precomputed doublings of C0
    C3 == C4 # 2 constraints
    X(C3)^2+(Y(C3)-1)^2 != 0 # 255 constraints
```

About 12000 constraints total.

---

**barryWhiteHat** (2018-12-22):

Nice. We can do eddsa for 7000 https://github.com/HarryR/ethsnarks/blob/093b660eb22b5132c2936286a1f1c940365b5561/src/jubjub/eddsa.cpp There is eddsa in belman somewhere https://github.com/matterinc/plasma_winter hope that helps you with the implmentaiton.

---

**thericciflow** (2019-01-03):

Jubjub is a pairing-freindly curve (Edwards birationally equivalent to BLS12-381). So what about using a BLS short signature?

---

**barryWhiteHat** (2019-01-03):

how expensive would paring operation be to compute inside a snark?

---

**HarryR** (2019-01-05):

Pairing operations are implemented for Weierstrass curves in libsnark: https://github.com/scipr-lab/libsnark/tree/master/libsnark/gadgetlib1/gadgets/pairing although I’m unsure of how many constraints it requires.

However, to implement it for the BabyJubJub curve you would need to implement similar algorithms as above, described in:

- https://link.springer.com/chapter/10.1007/978-3-540-85538-5_14
- https://eprint.iacr.org/2012/532.pdf

Alternatively we could find new Weierstrass curve parameters as an alternative to the ones supported by the existing libsnark gadgets. The SCIPR lab already has code for this: https://github.com/scipr-lab/ecfactory - but I’m unsure about what would be necessary to tune them to find a candidate suitable for the alt-bn scalar field - doing so would be really cool as it opens opportunities for recursive SNARKs on EVM *now*.

---

**mathcrypto** (2019-09-05):

[@barryWhiteHat](/u/barrywhitehat) I have computed the number of constraints for eddsa verification [here](https://github.com/Ethsnarks/ethsnarks-hashpreimage/blob/master/circuit/hashpreimage.cpp)

and I found 7000 constraints + constraints for Pedersen hash function 1881 used twice

which makes total 10762 constraints. I was wondering if these numbers are correct?

```auto
def eddsa_check(R,B,S,A, M):

split_to_bits(R) # 252 constraints
split_to_bits(A) # 252 constraints
hash_RAM = H(R, A, M)  #1881 constraints
IsValid(R)  // is_oncurve and is_notloworder doubled three times so 5*3=15 + 5415 constraints for is_notloworder
lhs = ScalarMult(B, s)  # 4.2 * 252 = 1058 constraints // lhs = B*s
M = H(m)  # 1881  // M = H(m)
At = ScalarMult(A,hash_RAM) # 4.2 * 252 = 1058 constraints // A*hash_RAM
rhs = PointAdd(R, At) # 6 constraints // rhs = R + (A*hash_RAM)
lhs == rhs # 2 constraints
```

Going back to not_loworder, I found it cost 5415 constraints by following this algorithm

```auto
EdFieldElement x = //...
EdFieldElement y = //...

EdFieldElement a = curve.getA();
EdFieldElement d = curve.getD();
EdFieldElement lhs = 1.add(y.multiply(y).multiply(y.multiply(y).multiply(d)); // 6+5+5+13.252+4.2.252 constraints so 4350

EdFieldElement rhs = x.multiply(x).multiply(a); // 5+4.2*252=1063

boolean pointIsOnCurve = lhs.equals(rhs); // 2 constraints

Total 5415
```

