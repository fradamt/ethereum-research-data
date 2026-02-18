---
source: ethresearch
topic_id: 2869
title: O(1) merkle tree replacement?
author: nootropicat
date: "2018-08-09"
category: Cryptography
tags: []
url: https://ethresear.ch/t/o-1-merkle-tree-replacement/2869
views: 2930
likes: 9
posts_count: 9
---

# O(1) merkle tree replacement?

Is this scheme secure?

Let  H(x)  be a hash function with the following property:

 H(x+y) = H(x) + H(y)

while being collision and preimage resistant.

Define the accumulated hash of a set  inputs  as:

 setHash = H(sha3(input_1)+sha3(input_2) +\ ...)

equivalently

 setHash = H(sha3(input_1))+H(sha3(input_2)) +\ ...

then the proof of existence of an element  a \in inputs  is a pair:  (a, restSum)  that satisfies:

 setHash = H(sha3(a)) + H(restSum)

Batch proofs are possible with one shared  restSum .

The lost functionality compared to merkle trees is enumeration.

Security:

if  a \notin inputs  but proof for a's existence is valid, it means that either:

1. collision resistance of sha3 is broken, it’s feasible to find such a, a'  that:
 sha3(a) = sha3(a')  for  a \ne a' and  a' \in inputs
2. collision resistance of a composite function  H\ .\ sha3  is broken:
 H(sha3(a)) = H(sha3(a'))  for  a \ne a' and  a' \in inputs
3. preimage resistance of H is broken, it’s feasible to find  invalidRestSum  such that:
 setHash = H(sha3(a)) + H(invalidRestSum)
4. it’s feasible to generate  {b_1, b_2, ..., b_n} \notin inputs,  n \geq 2 ,  d \in inputs  such that:
 \sum_{i=1}^{n} sha3(b_i) = sha3(d)
which breaks sha3’s indifferentiability from random oracle assumption

Is there an attack that doesn’t require breaking hash functions?

## Replies

**musalbas** (2018-08-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png) nootropicat:

> Define the accumulated hash of a set inputs inputs as:
> setHash=H(sha3(input1)+sha3(input2)+ ...)
> equivalently
> setHash=H(sha3(input1))+H(sha3(input2))+ ...

I don’t see how these are equivalent. For one, they are different sizes? In the latter setHash, the size increases as you add more inputs.

What you’re trying to achieve sounds similar to [accumulators using a quasi-commutative one-way function](https://crypto.stackexchange.com/a/15550):

> Say you have a set Y=\{y_1,y_2,y_3\} and compute the accumulator as acc=f(f(f(x,y_1),y_2),y_3) you want to compute a witness for a value say y_2, then by quasi commutativity, the value for your witness is wit_{y_2} = f(f(x,y_1),y_3) and you can check given y_2 and wit_{y_2} whether y_2 is in the accumulator acc, you can check whether acc=f(wit_{y_2},y_3) holds.

---

**ldct** (2018-08-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png) nootropicat:

> H(x+y) = H(x) + H(y)

What do both of the + mean? Concatenation or some binary operation?

---

**nootropicat** (2018-08-09):

> For one, they are different sizes? In the latter setHash, the size increases as you add more inputs.

That’s addition, not concatenation.

I think it can be implemented using an elliptic curve, with  H(x) = x*G , but I didn’t want to conflate security of a specific ‘hash’ function with the general scheme.

For elliptic curves, (3) would reduce to a discrete logarithm problem:

 setHash-sha3(a)*G = P

find  invalidRest  so that  invalidRest*G = P

The quantum-proof alternative is [SWIFFT](https://en.wikipedia.org/wiki/SWIFFT)

> What you’re trying to achieve sounds similar to accumulators using a quasi-commutative one-way function:

Apparently - why aren’t they used in place of merkle trees then, when enumeration isn’t needed (like the state tree)? The linked papers seem concerned mainly with zero-knowledge proofs of membership, which makes them complex and slow, perhaps that’s why.

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> What do both of the ++ mean? Concatenation or some binary operation?

Operator in the abelian group

---

**ldct** (2018-08-09):

Ah ok, so you want H to have the type H: G_1 \to G_2 for abelian groups G_1 and G_2?

---

**nootropicat** (2018-08-09):

G_1 = G_2  and one in which multiplication by a scalar is infeasible to reverse (ie. preimage resistance) and it’s infeasible to find a pair  (a, a'), a \neq a'  so that  a*G = a'*G  (second preimage resistance)

---

**meronym** (2018-08-10):

> Is there an attack that doesn’t require breaking hash functions?

It looks to me that once an attacker learns any valid proof (a, restSum), he can compute the discrete logarithm of the root value (a+restSum), therefore produce proofs of the form (x, a+restSum-x) for arbitrary values of x.

This attack applies as long as H is homomorphic (not necessarily EC multiplication). But since the scheme relies on this homomorphism, it seems to be fundamentally broken.

---

**nootropicat** (2018-08-10):

You’re right, seems obvious now.

---

**HarryR** (2018-10-09):

There is a variant of the bilinear accumulator with a trusted setup which - but without the trusted setup, and that isn’t forgeable. But I would appreciate a second set of eyes.

From :  https://eprint.iacr.org/2008/538.pdf

Instead of the trusted key k with known point h = g^k

x_s, x_p = R? \in Z_q

S, P = g^{x_s}, g^{x_p}

x = x_s x_p

X = g^{x_s x_p}

A_{i+1} = Acc(A_i, x_s) = {A_i}^{x_s + x_p}

But, if you reveal x_s+x_p, or x_s x_p forgery is possible, as you can find any two components of the sum and you’re back to square one. In order to make the accumulator untrusted and accumulable in public, we need to verify that the new accumulator value is a valid transition from A_i \to A_{i+1}. This is difficult, but I’ll get onto that.

To verify you perform:

e(G_2, A) = e(W_x, S^{x_p})

Where

W_x = A^{{x_p x_s}^{-1}} = {A \over x_p x_s}

Where the value of x_s is never released, only its image S.

But this is still malleable…

To avoid malleability you then need to create a signature of both W_x and S, to verify that you know the preimage of S and aren’t just modifying existing values. So verification becomes:

e(G_2, A) = e(W_x, S^{x_p}) \land SchnorrVerify(S, H(A, W_x, S, x_p), ...)

---

The problem of updating the accumulator in public without revealing x_s to everybody can be solved in two ways:

1. Trusted third party, who you give x_s x_p to , who keeps that secret forever
2. Verifiable transition of A_{i-1} \to A_i, where A_i = A_{i-1}^{x_p x_s}

For 2. you would need to maintain two accumulators, one on each G_1 and G_2, and some kind of ratchet which verifies all parameters via parings.

---

And finally, what I described isn’t secure without a trusted setup, because you’re essentially doing {A \over x} \times x = A, which brings us back to the original problem… as described in the posts above.

