---
source: ethresearch
topic_id: 5407
title: Fast verification of multiple BLS signatures
author: vbuterin
date: "2019-05-03"
category: Sharding
tags: [signature-aggregation]
url: https://ethresear.ch/t/fast-verification-of-multiple-bls-signatures/5407
views: 9639
likes: 11
posts_count: 16
---

# Fast verification of multiple BLS signatures

Suppose that you received n signatures, S_1 … S_n, where each signature S_i is itself an aggregate signature with pubkeys P_{i,j} and messages M_{i,j} for 1 \le j \le m_i. That is, e(S_i, G) = \prod_{j=1}^{m_i} e(P_{i,j}, M_{i,j}).

The following is a technique for optimizing verification of all n signatures at the same time, especially in the case where the same message is signed by many public keys (this is the reality in eth2).

Generate a list of n random values between 1 and the curve order, r_1 … r_n. Locally calculate S* = S_1 * r_1 + S_2 * r_2 + ... + S_n * r_n (writing the elliptic curve group additively), and M'_{i,j} = M_{i,j} * r_i. Now, simply check that e(S*, G) = \prod_{i=1}^n \prod_{j=1}^{m_i} e(P_{i,j}, M'_{i,j}). If it is, then all signatures are with very high probability valid, and if it is not, then at least one signature is invalid, though we lose the ability to tell which one.

This reduces the number of final exponentiations we need to make to only one per block, and reduces the number of Miller loops from n + \sum m_i to 1 + \sum m_i, at the cost of a few extra message multiplications.

#### Why this works

The signatures are a set of equations. It’s an elementary algebraic fact that if a set of equations y_1 = f(x_1) … y_n = f(x_n) holds true, than any linear combination of those equations y_1 * r_1 + ... + y_n * r_n = f(x_1) * r_1 + ... + f(x_n) * r_n also holds true. This gives completeness (ie. if the signatures are all valid, the check will pass).

Now, we need to look at soundness. Suppose that any of the signatures are incorrect, and specifically signature S_i deviates from the “correct” signature C_i by D_i (ie. D_i = S_i - C_i). Then, in your final check, that component of the equation will deviate from the “correct” value by D_i * r_i, which is unknown to the attacker, because r_i is unknown to the attacker. Hence, the attacker cannot come up with values for any of the other signatures that “compensate” for the error.

This also shows why the randomizing factors are necessary: otherwise, an attacker could make a bad block where if the correct signatures are C_1 and C_2, the attacker sets the signatures to C_1 + D and C_2 - D for some deviation D. A full signature check would interpret this as an invalid block, but a partial check would not.

### Why not just make a big aggregate signature?

Why not just have blocks contain S* as a big aggregate signature of all messages in the block? The answer here is that it makes accountability harder: if any of the signatures is invalid, one would need to verify the entire block to tell that this is the case, so verifying slashing messages would require many more pairings.

This technique lets us get the main benefit of making a big aggregate signature for each block, leading to large savings in signature verification time, while keeping the ability to split off individual signatures for individual verification for accountability purposes.

### Optimizations

We can gain some efficiency and sacrifice nothing by setting r_1 = 1, removing the need to make multiplications in the signature that contains the most distinct messages. We can also set other r_i values in a smaller range, eg. 1...2^{64}, keeping the cost of attacking the scheme extremely high (as the r_i values are secret, there’s no computational way for the attacker to try all possibilities and see which one works); this would reduce the cost of multiplications by ~4x.

## Replies

**gakonst** (2019-05-03):

Does this scheme require a dealer to gather each S_i * r_i share and submit S*?

If so, can the dealer trivially recover the r_i values if they have access to the original signature S_i and the signature share which they obtained to create the final aggregate signature? (ignore this question if first question is not relevant)

---

**vbuterin** (2019-05-04):

To be clear, the scheme is a purely client-side optimization that can voluntarily be done by clients verifying blocks that contain multiple signatures. Each client generates S* locally and different clients will generate different S* values because they have different r_i values.

---

**liangcc** (2019-05-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> then at least one signature is invalid, though we lose the ability to tell which one.

Would this mean in the invalid case, the client still needs to check S_1 \dots S_n  one by one to find the invalid one? How would this better than “big aggregate signature of all messages in the block” approach, in terms of the number of signatures to check?

---

**ValarDragon** (2019-05-06):

I think the smaller range should be on the order of 1...2^{128}, assuming 128 bit soundness is desired. In the case of 2 signatures, with r_1 = 1, its easy to show that 1...2^{64} only has 64 bits of soundness, and this extends to larger aggregations if an attacker can restrict the signatures to be in a subgroup of order 2^{64}, which could likely exist if the pairing friendly curve used is also a SNARK friendly curve.

Alternatively, it may suffice that a single client may falsely accept with a lower soundness, as long as its unlikely that everyone is fooled, but that seems a bit precarious imo.

---

**vbuterin** (2019-05-06):

> Would this mean in the invalid case, the client still needs to check S1…Sn one by one to find the invalid one? How would this better than “big aggregate signature of all messages in the block” approach, in terms of the number of signatures to check?

Yep! Though note that:

1. We can expect that most blocks received will be valid.
2. If a block is invalid, there’s technically no need to figure out why it’s invalid; you can just reject it and move on. A client would only do full rechecking to figure out which of the signatures is faulty if a high level of error logging is turned on.

> I think the smaller range should be on the order of 1…2^{128}, assuming 128 bit soundness is desired. In the case of 2 signatures, with r_1=1, its easy to show that 1…2^{64} only has 64 bits of soundness

Sure, but 64 bits of soundness is fine because the attacker doesn’t have the ability to try many times and check locally if they succeeded. It’s checked client-side, so it just means that there’s only a 2^{-64} chance of success

> and this extends to larger aggregations if an attacker can restrict the signatures to be in a subgroup of order 2^{64}, which could likely exist if the pairing friendly curve used is also a SNARK friendly curve.

The elliptic curve group BLS-12-381 is operating in is a prime-order subgroup. So it’s not possible for there to be a lower-order sub-subgroup of that (except the trivial one with one element).

---

**kirk-baird** (2019-06-11):

I was wondering if it would be quicker to instead multiply the public keys by r rather than the messages.

My thoughts were that since e(P, r*M) = e(r*P, M).

and public keys are on G1 then it would be quicker to do the elliptic curve multiplications by r on G1 rather than G2.

The downside I see to this would be that we would need to maintain a copy of the original public key so it would need to be copied before multiplication.

As an FYI I’ve implemented this and run some benchmarks

Verification of a Single Signature -> 8.3ms

Fast Verifcation: n = 10, m = 3 (Note mi = 3 for all i)

r * M -> 6.06ms per signature

r * P -> 5.86ms per signature

Fast Verification: n = 50, m = 6 (Note mi = 3 for all i)

r * M -> 5.14ms per signature

r * P -> 5.06ms per signature

Also r was chosen between 1..2^{63}

---

**vbuterin** (2019-06-11):

You can definitely do that. The reason why I multiply messages is that in our use cases there are many pubkeys shared per message; if this is not true in your use case then multiplying pubkeys may well be optimal.

---

**kirk-baird** (2019-06-11):

In the cases where messages are the same wouldn’t it then be quicker to aggregate the public keys? Which would replace a pairing with an elliptic curve addition.

---

**kirk-baird** (2019-08-19):

For anyone implementing this there is a further improvement that can be made here by doing ‘ate double pairings’ as can bee seen [here - ate2](https://github.com/apache/incubator-milagro-crypto-rust/blob/d358b74b046d859d2b9f3aa2b3506bc582678103/src/pair.rs#L320).

Ate double pairings are equivalent to `e(A, B) * e(C, D)` and about 30% faster than doing two pairings individually and multiplying them together. Hence when doing `n * m` pairings we can reduce this to `n * m / 2` double pairings and improving runtime by upto 30%.

---

**vbuterin** (2019-08-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/kirk-baird/48/5285_2.png) kirk-baird:

> In the cases where messages are the same wouldn’t it then be quicker to aggregate the public keys? Which would replace a pairing with an elliptic curve addition.

Yep! I guess I did not mention this because that’s an optimization every client in eth2 has been using almost since the beginning already.

---

**kirk-baird** (2020-10-29):

Now with proof of possession, I am wondering if the multiplication step is still required. That is can we not simply sum all of the aggregate signatures

S^* = \Sigma S_i

As users cannot manipulate the any of the AggregatePublicKeys to be the negation of other AggregatePublicKeys, nor can we manipulate the hashed message points to be the negation of any other message (obviously we must exclude the deposit signatures as they do the PoP).

We would be able to save n multiplications and remove the need for randomness.

---

**vbuterin** (2020-10-30):

Oh, we already use proofs of possession and that already reduces the number of pairings to one per message. The issue here is involving verifying *multiple signatures to multiple messages*.

---

**kirk-baird** (2020-10-30):

Yep but can we not do a similar process again. Say we have 3 aggregate signatures AS1, AS2, AS3, 6 PublicKeys PK1, …, PK6 and 6 Messages M1,…,M6 can we do:

AS1 -> ([PK1, PK2], [M1, M2])

AS2 -> ([PK3, PK4], [M3, M4])

AS3 -> ([PK5, PK6], [M5, M6])

S* = AS1 +AS2 + AS3

LHS = e(S*, G)

RHS = (e(PK1, M1) * e(PK2, M2)) * (e(PK3, M3) * e(PK4, M4)) * (e(PK5, M5) * e(PK6, M6))

LSH == RHS

I guess I’m not seeing what the multiplication is protecting against now public keys are proved.

---

**kirk-baird** (2020-10-30):

You know, I’ve just solved my own problem we are stopping a consensus issue in that a user could create a situation where the S* verifies but each individual AggregateSignature doesn’t e.g. by sending

AS1' = ([PK1, PK3, PK3], [M1, M2, M3])

AS2' = ([PK4], [M4])

…

So AS1’ and AS2’ would not verify individually but will when aggregated they verify.

---

**vbuterin** (2020-10-30):

> So AS1’ and AS2’ would not verify individually but will when aggregated they verify.

Right, exactly this. We want to prevent a scenario where, if S_1 and S_2 are the “actual” valid signatures for some sets of data, a malicious block producer instead sends S_1 + \Delta and S_2 - \Delta (for unknown \Delta). This is bad in our use case because while it does not break soundness of the signature scheme itself, it would make the signatures non-detachable (ie. you can’t verify them separately from the block they are included in), which would prevent slashing.

