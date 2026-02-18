---
source: ethresearch
topic_id: 4601
title: Zero-knowledge proof of addition for large, high-entropy values
author: irakliy81
date: "2018-12-16"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/zero-knowledge-proof-of-addition-for-large-high-entropy-values/4601
views: 2137
likes: 4
posts_count: 14
---

# Zero-knowledge proof of addition for large, high-entropy values

Suppose I have committed to 3 large (230+ bits), high-entropy values a, b, c by mapping them to points on the elliptic curve g with generator G and order q. So, the commitments are A = a \cdot G, B = b \cdot G, C = c \cdot G.

The scheme below can be used to prove, very efficiently, that a = b + c in Z. I’m wondering if there are any holes in it - so, would appreciate any feedback.

### Commitments over two elliptic curves

A naive way to check this equality would be to check if A = B + C. However, this would not be in Z since the addition can underflow or overflow. To address this, we could use range proofs, but these are large and inefficient. So, we define a new commitment scheme over two elliptic curves:

Select another elliptic curve g' with generator G' and order q', such that q < q'. Then, compute a commitment to a as follows:

1. Map a to both curves as A = a \cdot G and A' = a \cdot G'.
2. Choose a random value r and compute T = r \cdot G and T' = r \cdot G'.
3. Compute u = H(G, G', A, A', T, T'), where H is a cryptographic hash function.
4. Compute v = r + a \cdot u (this is done in Z), such that \frac{v}{u} < q. This may require iterating through several values of r before a suitable v is found.
5. The commitment is then defined as a 5-tuple (A, A', T, T', v).

Using this commitment anyone can verify that A and A' are derived from the same value a, and that a < q. The verification can be done as follows:

1. Compute u = H(G, G', A, A', T, T').
2. Check that v \cdot G = T + u \cdot A and v \cdot G' = T' + u \cdot A'. This check uses proof of equality of discrete logarithms to ensure that A and A' are derived from the same value a.
3. Check that \frac{v}{u} < q. This ensures that a < q because \frac{v}{u} = \frac{(r + a \cdot u)}{u} = \frac{r}{u} + a and, thus, \frac{r}{u} + a can be less than q only if a < q

The commitment is very compact. Assuming we use 256-bit elliptic curves, points A, A', T, T' can be encoded in ≈32 bytes each. To ensure that the commitment doesn’t leak any information about the magnitude of a, the random value r should be close to 64 bytes. Thus, the total size of the commitment is 192 bytes.

### Proof of addition

Using the commitments defined in the previous section we can prove that a = b + c without revealing values of a, b, or c as follows:

Assuming (A, A', T_1, T_1', v_1), (B, B', T_2, T_2', v_2), (C, C', T_3, T_3', v_3) are valid commitments for a, b, and c respectively, a = b + c if and only if:

1. A = B + C and
2. A' = B' + C'.

Checking the equality on both elliptic curves at the same time is required to ensure that the addition does not underflow or overflow.

### Where this can be useful

Suppose we define a coin as 10^{69} indivisible units (similar to how, for example, a single bitcoin is defined as 10^8 satoshi). Under this definition, it takes 230 bits to encode a single coin but it also allows us to represent all amounts as unique values. By randomizing the lower 200 bits of an amount, we can guarantee, with extremely high degree of probability, that the same amount will not appear in the ledger more than once. For example, an amount of 2 coins may appear as 2.00000000090324324320… one time, and as 1.99999999970934309280… another time. However, from the end-user perspective, both amounts are identical and would appear as just 2 coins in wallet software.

This technique would allow us to use the scheme above to effectively hide all transaction amounts in the blockchain.

## Replies

**vbuterin** (2018-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/irakliy81/48/2429_2.png) irakliy81:

> Check that v \cdot G = T + u \cdot A and v \cdot G' = T' + u \cdot A'. This check uses proof of equality of discrete logarithms to ensure that A and A' are derived from the same value a.

Are you sure that this works? Particularly, what if an attacker chooses A and A' values with different discrete logs, a and a', and then fiddles with the T and T' values, submitting T = v \cdot G - u \cdot A and T' = v \cdot G' - u \cdot A', disregarding the fact that T and T' now have distinct discrete logs as you don’t seem to be checking for that anywhere.

---

**thericciflow** (2018-12-18):

First, an EC Pederson commitment to a value a is A=aG+rH where r is a random value and H another generator of the elliptic curve. Otherwise, committing to the same value a twice would result in the same A which gives a hint on what value you are hiding. Second, for the overflow problem this is addressed in [Greg Maxwell’s confidential transactions (CT)](https://cryptoservices.github.io/cryptography/2017/07/21/Sigs.html). In fact, to escape the overflow you need a, b and c to be small enough such that their sum does not exceed p the EC subgroup order. That is said you need to prove that b+c<p i.e. b+c < 2^{k+1} if p=\sum _{i=0}^{k}p_i 2^i. This can be done using ring signatures.

---

**vbuterin** (2018-12-18):

I think the intention of this post was to try to make a proof of addition that works without requiring range proofs. The stylized ideal protocol based on the idea in the above post that would work, but I have no idea how to actually implement, is as follows:

- Let C_a, C_b, C_c be commitments of some kind to a, b, c
- Let h = hash(C_a, C_b, C_c). Use h to generate a random elliptic curve with an unpredictable order, with some generator G
- Construct three points A, B, C on the curve, and somehow prove that dlog_G(A) is the value committed to in C_a and likewise for B and C
- Check the elliptic curve addition A + B = C

It doesn’t seem likely to me that you can do it with curves that are known ahead of time, even multiple curves, without there being some fancy Chinese Remainder Theorem-based attack that does a wraparound around all of the orders of the curves at the same time.

---

**thericciflow** (2018-12-18):

The dlog_G(A) wouldn’t be provably hard if the curve order is random and even if it is big enough the random elliptic curve can be supersingular or of Frobenius trace 1 which makes it easy to transfer the dlog problem to finite fields and thus reduce the security level.

---

**vbuterin** (2018-12-18):

Ah sorry, I meant to say a random *secure* curve.

---

**irakliy81** (2018-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> if an attacker chooses A and A′ values with different discrete logs, a and a', and then fiddles with the T and T′ values, submitting T=v⋅G−u⋅A and T′=v⋅G′−u⋅A′, disregarding the fact that T and T′ now have distinct discrete logs

I don’t think this specific attack should be possible since T and T' are inputs into the hash function that generates u. Recall that:

u=H(G,G′,A,A′,T,T′)

This means that you can’t change T and T' independently of u (assuming H is a hash function that acts as a random oracle). Basically, this part of the scheme reduces to proving key equivalence across elliptic curves of different order, and I think that it is [possible](https://crypto.stackexchange.com/a/60129). An attacker could try to brute-force invalid combinations of A, A', T, T', but my understanding is that this is computationally infeasible (equivalent to solving discrete log problem?).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It doesn’t seem likely to me that you can do it with curves that are known ahead of time, even multiple curves, without there being some fancy Chinese Remainder Theorem-based attack that does a wraparound around all of the orders of the curves at the same time.

The check that \frac{v}{u} < q is indented to guard against such warp-arounds. If the check passes, a < q and, thus, it should’t wrap around either of the curves.

Assuming the above holds, I think you should be able to use well known curves in this scheme.

---

**irakliy81** (2018-12-18):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/9dc877/48.png) thericciflow:

> EC Pederson commitment to a value a is A=aG+rH where r is a random value and H another generator of the elliptic curve. Otherwise, committing to the same value a twice would result in the same A which gives a hint on what value you are hiding.

I’m not using Pederson commitments in this scheme. The same a is never used twice (lower 200 bits of a are randomized) - so, exposing a shouldn’t be a problem. The goal of this scheme is to prove addition using solely elliptic curves (without requiring range proofs).

---

**vbuterin** (2018-12-18):

Ah, you’re right. Next attempt at an attack: choose negative values of r to mask the case where a exceeds the order of one or both curves.

---

**irakliy81** (2018-12-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> choose negative values of r to mask the case where a exceeds the order of one or both curves.

Hmmm - I guess choosing negative r can break this. One potential way to address this is to make choice of r verifiably random. It might be possible to do this using pairings. Maybe something like this:

Assuming both curves are pairing-friendly and have subgroups with generators (G_1, G_2) and (G_1', G_2') respectively, we can:

1. Compute k = H(A, A'), and then K = k \cdot G_2 and K' = k \cdot G_2'.
2. Compute r such that e(A, r \cdot G_2) = e(G_1, K) and e(A', r \cdot G_2') = e(G_1', K').
3. Compute T = r \cdot G_1 and T' = r \cdot G_1'.

And from here proceed as in the original scheme.

---

**vbuterin** (2018-12-19):

More generally, another big problem with the scheme is that I don’t see how it prevents you from committing to values of a, b, c where any one or more of them are negative. The same math should work for negative inputs as positive inputs, as your proof uses arithmetic operations, and arithmetic operations don’t care about positive vs negative (except for the \frac{v}{u} < q check, but negative a values will make it even *easier* to pass that check).

---

**irakliy81** (2018-12-19):

You are right - the addition is in Z and each number can be bounded to be between -q and q, but as is, there is nothing preventing negative numbers. I’ll see if I can come up with a way to address it.

---

**denett** (2018-12-22):

You can to proof a number is positive by showing it is bigger than a square number.

I have no experience with elliptic curves, but I think it can be done using an RSA modulo.

Using RSA modulo, addition is easy g^a . g^b \equiv  g^{a+b} \mod N, I don’t think we have to worry about overflow, because the trapdoor is unknown.

Proving a is positive can be done by showing g^{x^2}. g^y = g^{a}, where you provide a positive y and proof x^2 is a square number without revealing x.

To proof x^2 is a a square I want you use a double Wesolowski proof as shown [here](https://ethresear.ch/t/rsa-hash-accumulator-for-arbitrary-values/4485/14).

Let A_x = g^x \mod N

Let A_{x^2} = g^{x^2} \mod N

We will substitute:

x = B\lfloor \frac x B \rfloor + x \mod B

We use the following witnesses:

b_1=g^{\lfloor \frac x B \rfloor} \mod N

b_2=A_x^{\lfloor \frac x B \rfloor} \mod N

r=x \mod B

The verifier should check:

b_1^B.g^r \equiv A_x \mod N

b_2^B.A_x^r \equiv A_{x^2} \mod N

It is not very efficient, because we need a lot of witnesses: y,A_x, A_{x^2},b_1,b_2,r to just proof a is positive, but it seems to work.

---

**irakliy81** (2018-12-23):

I think what you are describing is similar to  [Boudot proof](https://www.iacr.org/archive/eurocrypt2000/1807/18070437-new.pdf) and improvements thereof (such as [this](https://pdfs.semanticscholar.org/92fd/7c18ab65a3e1736be104fd69b5bb788c6383.pdf)). The commitment sizes there are around 2KB.

I was trying to do this over elliptic curves to make it much more efficient.

