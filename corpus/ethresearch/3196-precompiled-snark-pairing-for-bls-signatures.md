---
source: ethresearch
topic_id: 3196
title: Precompiled SNARK pairing for BLS signatures?
author: kladkogex
date: "2018-09-03"
category: zk-s[nt]arks
tags: [signature-aggregation]
url: https://ethresear.ch/t/precompiled-snark-pairing-for-bls-signatures/3196
views: 5122
likes: 5
posts_count: 8
---

# Precompiled SNARK pairing for BLS signatures?

We are thinking to implement BLS signature verification using the bn128 Ate pairing verification implemented in SNARK-related precompiled contracts.

The precompiled contract uses SNARK library, which in turn uses libff library. This library uses bn128 ATE pairing curve, which seems to be OK for BLS.

The description of the curve says:  [GitHub - scipr-lab/libsnark: C++ library for zkSNARKs](https://github.com/scipr-lab/libsnark)

> “bn128”: an instantiation based on a Barreto-Naehrig curve, providing 128 bits of security. The underlying curve implementation is [ate-pairing], which has incorporated our patch that changes the BN curve to one suitable for SNARK applications.

It is not clear what the patch is and whether it affects suitability of the curve for BLS signatures. Does anyone know what the patch is?

## Replies

**vbuterin** (2018-09-03):

Any curve that’s suitable for SNARKs should be suitable for BLS. Though you do want to use alt_bn128 to take advantage of the precompiles for on-chain verification.

---

**kladkogex** (2018-09-03):

Understood - I am a little bit scared by the sentence “which has incorporated our patch that changes the BN curve to one suitable for SNARK applications.” …  It seems from the sentence the curve was modified in some way … I hope the patch does not affect BLS …

---

**cdetrio** (2018-09-03):

It sounds like a poorly worded way of saying they’re using a different BN parameter(s), one that was not in the BN paper or the `[ate-pairing]` implementation (whatever codebase that is).

The term “curve” is massively overloaded, its an abbreviated term that describes many different things. Certainly the elliptic curve equation `y^2 = x^3 + ax + b` is the same, but they changed the `a` and `b` parameters. Between bn128 and alt_bn128 the `a` and `b` parameters are the exact same; only the `G2` generator point is different (if I’m not mistaken). I spent some time figuring all this out and it was more difficult than it should be, not because the math is complex (which it is) but because the codebases tend to have large constants strewn about without any comments/explanation, though they can often be derived from rather simple formulas:  https://github.com/ethereum/py_ecc/pull/3

---

**HarryR** (2018-09-03):

One problem you’re may run into with pairing equalty checks on-chain is the `ECPAIRING` operation doesn’t allow you to directly compare arbitrary pairings without some (potentially dangerous) alterations to the verification step, also you can’t do scalar multiplication on G2 or GT elements on-chain.

Recap of BLS signatures:

- e(P_2,H(m)_1)_T = e(G_2, S_1)_T where _2 and _1 denote points of G1 and G2, and _T for GT.
- Off-chain, you take your secret x, and do xG_2 \to P_2 (your public key).
- You then provide your public key P_2 to the on-chain contract
- You then generate your signature, xH(m)_1 \to S_1
- You provide signature to on-chain contract
- It verifies e(P_2,H(m)_1)_T = e(G_2, S_1)_T

The `ECPAIRING` operation works as such: e(A_2, B_1) * e(C_2, D_1) = 1_T - which means you need to modify the pairing equality check in a way which doesn’t immediately seem intuitive.

```python
from py_ecc.bn128 import *
p = curve_order
x = randint(1, p-1) # out secret key
H_m = multiply(G1, randint(1, p-1)) # lets pretend it's HashToPoint
P = multiply(G2, x) # our public key in G2
S = multiply(H_m, x) # our signature in G1
a = pairing(P, H_m)
b = pairing(G2, S)
assert a == b # Verify signature
```

To use equivalent of `ECPAIRING`, you’d then do:

```python
c = pairing(G2, neg(S))
assert a * c == FQ12.one()
```

To aggregate them:

```auto
y = randint(1, p-1) # second secret key
Q = multiply(G2, y) # second public key
T = multiply(H_m, y)  # second signature
d = pairing(add(P, Q), double(H_m))
e = pairing(double(G2, add(S,T))
assert d == e
```

To verify the aggregates in `ECPAIRING` style:

```python
d * pairing(double(G2) neg(add(S,T))) == FQ12.one()
```

I should probably add this to my `solcrypto` repo lol, as it’s a useful bit of code, but anyway, in this case does using the pairing product operation introduce any vulnerabilities with the verification of aggregate BLS signatures?

---

**vbuterin** (2018-09-04):

The reason why the precompile is of that form is that that’s the most natural way to make it usable for both e(a, b) = e(c, d) and more complex equations like e(a, b) * e(c, d) = e(f, g), or e(a, b) * e(c, d) = e(f, g) + e(h, i), etc. You’re correct that simply negating the G1 points that are on the “right” side of the equation is the way to do it.

> Between bn128 and alt_bn128 the a and b parameters are the exact same; only the G2 generator point is different (if I’m not mistaken)

Given that, as we proved last year, there can only be one order-N subgroup of G2, that would basically mean that the alt_bn128 generator is a multiple of the bn128 generator, and I would presume the generators are constructed in such a way that we don’t know what the cofactor is. If this is true, then the pairing precompile for alt_bn128 should be exactly the same as the pairing precompile for bn128, as although it does care that the G2 points are on the right subgroup, it doesn’t care what the generator is.

---

**GuthL** (2018-09-04):

Hi Vitalik, jumping in as I share difficulties with the precompiled pairing.

I don’t understand how you can do e(a, b) * e(c, d) = e(f, g) + e(h, i) with the precompiled.

This is not what I’m looking for but still puzzled me. Is it a typo?

To go back to what [@HarryR](/u/harryr) is saying, I have been surprised when trying to implement the BBS signature not getting an element of GT or a hash of the element.

I still wonder how to implement the BBS signature which works as followed:

According to the [BBS](https://crypto.stanford.edu/~xb/crypto04a/groupsigs.pdf) algorithm, to validate a signature s (R3 belonging to the signature), you need to check

e(T_3,g_2)^{s_x}.e(h,w)^{-s_\alpha-s_\beta}.e(h,g_2)^{-s_{\delta_1}-s_{\delta_2}} = (e(g_1,g_2)/e(T_3,w))^c.R_3

Which can also be framed as:

R_3 = e(T_3,g_2)^{s_x}.e(h,w)^{-s_\alpha-s_\beta}.e(h,g_2)^{-s_{\delta_1}-s_{\delta_2}}.e(g_1,g_2)^{-c}.e(T_3,w)^c\\
R_3 = e(s_x.T_3-({s_{\delta_1}+s_{\delta_2}}).h-c.g1,g_2).e(c.T_3-({s_\alpha+s_\beta}).h,w)

One of the problem I have with the current implementation is that you cannot preprocess some of the pairings and you cannot check two elements of GT as expected by the paper.

Is there a way to do it, under the current precompiled?

---

**HarryR** (2018-12-11):

https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html is a good reference for BLS multi-signatures and aggregation.

