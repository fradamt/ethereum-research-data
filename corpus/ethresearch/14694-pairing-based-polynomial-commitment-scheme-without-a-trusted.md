---
source: ethresearch
topic_id: 14694
title: Pairing-based polynomial commitment scheme without a trusted setup
author: zie1ony
date: "2023-01-26"
category: Cryptography
tags: []
url: https://ethresear.ch/t/pairing-based-polynomial-commitment-scheme-without-a-trusted-setup/14694
views: 1784
likes: 2
posts_count: 4
---

# Pairing-based polynomial commitment scheme without a trusted setup

Following is the polynomial commitment scheme between Prover and Verfier. I was looking at the KATE scheme and I noticed it could be done differently and easier. Note that it doesn’t require trusted setup, nor attaching additional proof to the result F(t) for a challange t.

Let me know what you think. Is it useful? Can you break it?

## Pairing

The pairing is a map e: G_1 \times G_2 \rightarrow G_T where G_1 and G_2 are additive groups and G_T is multiplicative group.

Both groups have generators. P for G_1 and Q for G_2. These are publically known.

Pairing e satisfies:

e(aP, bQ) = e(P, abQ) = e(abP, Q) = e(P,Q)^{ab}

e(P, Q)^{a+b} = e(P, Q)^a \cdot e(P, Q)^b

## Commitment

Prover has a secret polynomial F.

F(x) = f_0 + f_1x + ... + f_nx^n

Firstly Prover generates two random secret numbers a and b. They are used to hide coefficients of F and compose new polynomial K.

K(x) = (a + bf_0) + (a+bf_1)x + ... + (a+bf_n)x^n

Second step is projecting K on G2. It means multiplying all coefficients by Q. This creates new polynomial Z over G_2.

Z(x) = K(x)Q \\
Z(x) = (a + bf_0)Q + (a+bf_1)Qx + ... + (a+bf_n)Qx^n \\
Z(x) = Z_0 + Z_1x + ... + Z_nx^n

Final part of the commitment is hiding a on G_1 and b on G_2.

M = aP \\
N = bQ

The commitment C to polynomial F can be send to Verifier.

C = (Z, M, N)

## Challange

Knowing C, Verifier can ask Prover to calculate F(t) for a given t.

Prover computes F(t) and sends the result back to the verifier.

## Verification

Verifier knows: t, F(t) and C = (Z, M, N). To make sure F(t) is correct, the following check needs to be satisfied.

p(M, (1+t+..+t^n)Q) \cdot p(F(t)P, N) = p(P, Z(t))

### Reasoning

Following transforms right-hand side of the verification check to the left-hand side.

\begin{align}
p(P, Z(t))
  & = p(P, K(t)Q) \\
  & = p(P, Q)^{K(t)} \\
  & = p(P, Q)^{(a + bf_0) + (a+bf_1)t + ... + (a+bf_n)t^n} \\
  & = p(P, Q)^{a + bf_0 + at + bf_1t + ... + at^n + bf_nt^n} \\
  & = p(P, Q)^{a + at + ... + at^n  + bf_0 + bf_1t + ... +  + bf_nt^n} \\
  & = p(P, Q)^{a + at + ... + at^n} \cdot p(P, Q)^{bf_0 + bf_1t + ... + bf_nt^n} \\
  & = p(P, Q)^{a (1 + t + ... + t^n)} \cdot p(P, Q)^{b (f_0 + f_1t + ... + f_nt^n)} \\
  & = p(aP, (1+t+..+t^n)Q) \cdot p((f_0 + f_1t + ... + f_nt^n)P, bQ) \\
  & = p(M, (1+t+..+t^n)Q) \cdot p(F(t)P, N)
\end{align}

## Replies

**seresistvanandras** (2023-01-26):

This scheme is trivially broken. It does not satisfy the polynomial binding requirement of polynomial commitment schemes. Let’s consider the following simple example. **My assumption is that the value t is known to the committer in the beginning of the protocol, otherwise your committer could not compute the group element Z in your proposed scheme**. Put differently, it needs to know, at which point it needs to evaluate the secret polynomial F(x). The adversary publishes the commitment C=(Z,M,N) to a constant polynomial F(x)=f_0. The problem is that the adversary can open the commitment C=(Z,M,N) to another linear polynomial F'(x)=f'_0+f'_1x, which is F'(x)\neq F(x). Let f'_0:=f_0+t and f'_1:=-b^{-1}a-1.

Now, let’s check that, indeed the commitment to F'(x) is the same as F(x). We only need to check that the Z values of the commitment C is the same, since we did not modify M and N. We need to check Z=(a+bf_0)Q\stackrel{?}{=}(a+bf'_0)Q+(a+bf'_1)Qt. Using the definition of F'(x) we get that Z=(a+bf_0)Q\stackrel{?}{=}(a+b(f_0+t))Q+(a+b(-b^{-1}a-1))Qt= =(a+bf_0)Q+btQ+atQ-atQ-btQ=(a+bf_0)Q.

If you want to iterate on your scheme, please consider the following suggestions.

1. Missing Evaluation protocol: In the protocol above, you did not specify one of the key ingredients of a polynomial commitment scheme, i.e., an evaluation protocol. Would you use the same strategy as in the KZG scheme? To me, this was not clear.
2. Missing security proofs: to make such an important claim, it is also necessary to back it up. You could achieve this by giving security proofs. You only proved correctness. You would also need to show that your PC scheme satisfies the remaining properties of a PC scheme, i.e., polynomial binding, hiding, evaluation binding, and knowledge soundness. Correctness is not enough.

Good luck! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**zie1ony** (2023-01-26):

Thank you for spending your time ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) I really, really appriciate that!

This is how the protocol should go:

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/75aade41159d55e60327b6a75cc078c587cf0541_2_656x500.png)image1070×815 36.1 KB](https://ethresear.ch/uploads/default/75aade41159d55e60327b6a75cc078c587cf0541)

I don’t understand your assumptions that t needs to be known to the commiter (prover) before commiting. Isn’t that the whole point of the commitment not to know the challange before commiting to the F?

By Z in C I ment coefficients of Z: {\{ Z_0, Z_1, ..., Z_n\}}, so verifier could compute Z(t) on its own. Maybe this is the missing information?

I also need some time think about the attack you proposed.

Re *Missing security proofs*, I’m a simple software engineer, I’d have to hire mathematician ![:mage:](https://ethresear.ch/images/emoji/facebook_messenger/mage.png?v=14) to do it.

---

**seresistvanandras** (2023-01-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/zie1ony/48/11207_2.png) zie1ony:

> By Z ZZ in C CC I ment coefficients of Z ZZ : {{ Z_0, Z_1, …, Z_n}} {Z0,Z1,…,Zn}{{ Z_0, Z_1, …, Z_n}} , so verifier could compute Z(t) Z(t)Z(t) on its own. Maybe this is the missing information?

Yeah, I did not understand what exactly is Z in C=(Z,M,N). Then, the commitment is not super interesting if you send as much information as the size of the commitment. Committing to each and every coefficient with Pedersen commitment would also be perfectly fine. We also crucially need succictness for a PC scheme in our applications.  Specifically, your PC scheme has a linear size in the degree of the polynomial. Ideally, the commitment should be constant-size or polylogarithmic, i.e., \mathcal{O}(\log n).

I still think that polynomial binding does not hold even in this variant of your scheme but I leave you this as a simple exercise.

