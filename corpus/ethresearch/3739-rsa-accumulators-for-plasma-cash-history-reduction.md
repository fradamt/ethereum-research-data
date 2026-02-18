---
source: ethresearch
topic_id: 3739
title: RSA Accumulators for Plasma Cash history reduction
author: vbuterin
date: "2018-10-08"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/rsa-accumulators-for-plasma-cash-history-reduction/3739
views: 19941
likes: 42
posts_count: 24
---

# RSA Accumulators for Plasma Cash history reduction

*Special thanks to Justin Drake for discussion*

One of the challenges for all Plasma flavors, Plasma Cash too, is the amount of history data that users need to keep around, and send to recipients if they want to send coins. For example, suppose a Plasma chain has one block committed to chain per minute, with \approx 2^{16} transactions per minute (~= 1000 transactions per second). We assume each user has their coins split across \approx 10 fragments. To have the full information needed to win an exit game, each fragment requires a Merkle branch of length \approx 16 per block, so that’s 16 hashes * 32 bytes * 500000 minutes * 10 fragments \approx 2.5 GB for one year. In a transfer or atomic swap or similar operation, this is data that must be transferred.

---

We can increase the efficiency here with RSA accumulators. An RSA accumulator is a data structure providing similar functionality to a Merkle tree: a large amount of data can be compressed into a single fixed-size “root”, such that given the data and this root, one can construct a “witness” to prove that any specific value from the data is part of the data represented by that root. This is done as follows. We choose a large value N whose factorization is not fully known, and a generator g (eg. g = 3) which represents the empty accumulator. To add a value v to an accumulator A, we set the new accumulator A' = A^v. To prove that a value v is part of an accumulator A, we can use a proof of knowledge of exponent scheme (see below), proving that we know a cofactor x such that (g^v)^x = A (note that x may be very large; it is linear in the number of elements, hence why we need a proof scheme rather than providing x directly).

For example, suppose that we want to add the values 3,5,11 into the accumulator. Then, A = g^{165}. To prove that 3 is part of A (we’ll use the notation “part of [g...A]” from now on for reasons that should become clear soon), we use a proof of knowledge scheme to prove that (g^3)^x = A for some known cofactor x. In this case, x = 55, but in cases involving many thousands of values x could get very large, which is why the proof of knowledge schemes are necessary.

One example of a proof of knowledge scheme, [described by Wesolowski](https://eprint.iacr.org/2018/623.pdf) (see also [this talk by Benedikt Bünz](https://www.youtube.com/watch?v=IMzLa9B1_3E&t=3521s)) is as follows. Let h = g^v and z = h^x. Select B = hash(h, z) \mod N. Compute b = h^{floor(\frac{x}{B})}, and r = x \mod B. A proof is simply (b, z), which we can verify by checking b^B * h^r = z (proof of completeness: b^B * h^r = h^{B * floor(\frac{x}{B}) + x \mod B} = h^x). Note that this proof is constant-sized.

To prove that a value is v *not* part of [g...A], we need only prove that we know r such that 0 < r < v where A * g^r *is* a known power of g^v using the algorithm above. For example, suppose we want to prove that 7 is not part of [g...A] in the example above. 7 is not a factor of 165, so there is no integer x such that (g^7)^x = g^{165} = A. But g^7 *is* a known root of A * g^3 = g^{168}, so we can provide the values r=3 (satisfying the desired 0 < r < 7) and cofactor x = 24, and we see (g^7)^{24} = A * g^3 = g^{168}.

---

Now, here is how we can use this technique. We require Plasma Cash roots to come with both a Merkle tree of transactions *and* an RSA accumulator of coin indices that are modified in that block. Using a transaction in an exit game requires both the Merkle proof and the RSA accumulator proof of membership. This means that a RSA proof of non-membership is sufficient to satisfy a user that there is no data in that block that could be used as a transaction in an exit game. However, the RSA accumulator that we use is *cumulative*; that is, in the first block, the generator that we use can be 3, but in every subsequent block, the generator used is the accumulator output of the previous block. This allows us to batch proofs of non-membership: to prove that a given coin index was not touched in blocks n .... n+k, we make a proof of non-membership based on the post-state of the accumulator after block n+k using the pre-state of block n as the generator. If a user receives this proof of non-membership, they can be convinced that no proof of membership can be generated for *any* of the blocks in the range n ... n+k.

This means that the history proof size for a coin goes down from one Merkle branch per Plasma block to two RSA accumulator proofs *per transaction of that coin*: one proof of membership for when the transaction takes place, and one proof of non-membership for the range where it does not. If each coin gets transacted on average once per day, and an RSA proof of non-membership is ~1 kB, then this means \approx 1 Kb * 365 days * 10 fragments \approx 3.6 MB for one year.

If there are many coins, then we can optimize further. Proofs of non-membership can be batched: for example, if you prove that A * g^{50} is a power of g^{143}, then you know that log_g(A) = -50 \mod 143, which implies it is not a multiple of 11 *or* 13. This works well up to a few hundred indices, but if we want to have very fine denominations it may be possible to batch much more, see [Log(coins)-sized proofs of inclusion and exclusion for RSA accumulators](https://ethresear.ch/t/log-coins-sized-proofs-of-inclusion-and-exclusion-for-rsa-accumulators/3839)

## Replies

**gluk64** (2018-10-09):

Here is a [great talk about RSA accumulators](https://www.youtube.com/watch?v=IMzLa9B1_3E&t=3521s) by Benedikt Bünz from ‘Scaling Bitcoin Kaizen’ a few days ago.

Is this scheme still secure if the operator who provided the RSA setup knows factors of N? Wouldn’t they be able to provide non-membership proof for any coin?

According to Bünz, there have been suggested an ideas of trustless RSA setup [based on modules over Euclidean rings](https://www.researchgate.net/profile/Helger_Lipmaa/publication/226120659_Secure_Accumulators_from_Euclidean_Rings_without_Trusted_Setup/links/0f31752f56e1fe71c0000000/Secure-Accumulators-from-Euclidean-Rings-without-Trusted-Setup.pdf). I could not find any more information on the security of this approach, unfortunately.

---

**barryWhiteHat** (2018-10-10):

So if i am following correctly you are allowing accumulating, not just prime numbers. Which means that a user can make a fake proof.

Example: Say they commit 14. They can then fake their witness that either 7 or 2 or 14 have been accumulated.

> This means that the history proof size for a coin goes down from one Merkle branch per Plasma block to two RSA accumulator proofs per transaction of that coin : one proof of membership for when the transaction takes place, and one proof of non-membership for the range where it does not. If each coin gets transacted on average once per day, and an RSA proof of non-membership is ~1 kB, then this means ≈1 Kb * 365 days * 10 fragments ≈3.6 MB for one year.

There is also the need of each user to update their witness as the accumulator is updated. Which adds data availability requirements as well as extra bandwidth to keep their witness up date. But i guess this is less than the merkle tree bandwidth requirements.

---

**gluk64** (2018-10-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> So if i am following correctly you are allowing accumulating, not just prime numbers. Which means that a user can make a fake proof.

Apparently you need to hash committed values to primes. We can also use predefined sequence of primes as a mapping, maybe that will be cheaper for execution in the EVM.

---

**vbuterin** (2018-10-10):

> Apparently you need to hash committed values to primes. We can also use predefined sequence of primes as a mapping, maybe that will be cheaper for execution in the EVM.

Definitely the latter. Just use the sequence of primes starting from the beginning: 2, 3, 5, 7, 11, 13, 17, 19… This way a batched proof of inclusion or exclusion only requires ~2-4 bytes per coin included, and not >=32.

---

**gluk64** (2018-10-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A proof is simply (b, z), which we can verify by checking b^B∗h^r=z

Please correct me if I’m wrong, but wouldn’t proof be (b, z, r)? In the Weselowski scheme x = 2^\tau and is publicly known, so the verifier computes r \leftarrow x \mod B, while in your scheme x is only known to the prover.

> To prove that a value is v not part of an accumulator A, we need only prove that we know r such that 0 < r < v where A * g^r is a known power of g^v using the algorithm above.

Could you please elaborate this part a little more? How do we find r? Why does the proof hold?

---

**vbuterin** (2018-10-11):

> Please correct me if I’m wrong, but wouldn’t proof be (b,z,r)? In the Weselowski scheme x=2τ and is publicly known, so the verifier computes r←xmodB, while in your scheme x is only known to the prover.

Ah yes, I think you’re right.

> Could you please elaborate this part a little more? How do we find r? Why does the proof hold?

Suppose I prove that A * g^3 is a power of g^{10}. Then, I know that DLOG_g(A) equals 7 mod 10, and so it is NOT a multiple of 10. Replace 3 with r and 10 with v.

---

**kfichter** (2018-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> which we can verify by checking bB∗hr=z

It seems this proof would have to be verified on-chain. Do you have a ballpark for the cost of the full operation? I guess it needs logarithmic exponentiations with the size of the exponent + modulo the large RSA prime (?) Don’t have a strong intuition for the gas cost of that.

---

**vbuterin** (2018-10-12):

> Do you have a ballpark for the cost of the full operation?

The check is b^B * h^r = z. B is a 256-bit value, as is r as r < B. b and h are both RSA-modulus-sized values. So it’s two calls to MODEXP with 256-bit exponents, and two calls with a one-bit exponent plus a manually implemented adder (this is using the formula ab = \frac{(a+b)^2 - (a-b)^2}{4}).

---

**ldct** (2018-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> To prove that a value v is part of an accumulator A, we can use a proof of knowledge of exponent scheme, proving that we know a value x such that (g^v)^x=A

Can we instead have g^x be the inclusion witness and have the verification be that (g^x)^v = A?

(the proof of knowledge of exponent scheme would still be needed to prove that the accumulator output in a block uses the previous block’s accumulator output as generator)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This means that the history proof size for a coin goes down from one Merkle branch per Plasma block to two RSA accumulator proofs per transaction of that coin : one proof of membership for when the transaction takes place, and one proof of non-membership for the range where it does not.

I wonder if the the following scheme works instead: supposing a coin (whose id is q) has been spent t times, and the genesis block accumulator generator is g=3. Then the latest block accumulator value should be A = g^{q^t {p_1}^{e_1} {p_2}^{e_2} \ldots } where q \ne p_i for all i. The coin validity proof consists of a proof that q^{t+1} is not part of A and 1 RSA inclusion proof and merkle inclusion proof per transaction of the coin (as before).

---

**vbuterin** (2018-10-12):

> I wonder if the the following scheme works instead: supposing a coin (whose id is q) has been spent t times, and the genesis block accumulator generator is g=3. Then the latest block accumulator value should be A=gqtp1e1p2e2… where q≠pi for all i. The coin validity proof consists of a proof that qt+1 is not part of A and 1 RSA inclusion proof and merkle inclusion proof per transaction of the coin (as before).

What’s the goal here? To reduce the size of the history proof by a further ~50%? If so it does seem like that does it.

---

**nadahalli** (2018-10-16):

gmaxwell’s posts on this thread about RSA accumulators are worth a read, imho.

https://bitcointalk.org/index.php?topic=1064860.0

---

**eolszewski** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The check is bB∗hr=zb^B * h^r = z. BB is a 256-bit value, as is rr as r<Br < B. bb and hh are both RSA-modulus-sized values. So it’s two calls to MODEXP with 256-bit exponents, and two calls with a one-bit exponent plus a manually implemented adder (this is using the formula ab=(a+b)2−(a−b)24ab = \frac{(a+b)^2 - (a-b)^2}{4}).

Given that the accumulator is ever-increasing, wouldn’t we very quickly run into problems with integer overflow when representing these values (both on-chain and off-chain)?

---

**vbuterin** (2018-10-18):

The multiplication is modulo some N for which we don’t know the factorization.

---

**DamianStraszak** (2018-12-29):

How do you pick N with uknown factorization without a trusted dealer? None of the methods mentioned in Bünz’s talk seem reasonable. Is there a well established way to do that?

---

**gakonst** (2019-01-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/damianstraszak/48/4013_2.png) DamianStraszak:

> How do you pick N with uknown factorization without a trusted dealer?

You can do either a secure multi party computation, or pick an RSA number such as RSA-2048.

I wrote a blogpost about accumulators and the proof of exponentiation schemes here by the way:

https://medium.com/@gakonst/deep-dive-on-rsa-accumulators-230bc84144d9

---

**gakonst** (2019-01-13):

Note that the verifier needs to additionally check that A’ accumulates from A, ie that the product of the newly accumulated elements {x1x2 … xn} is the discrete log of A’ base A.

The proof has to be the NI-PoKE2 from [Stanford’s paper](https://eprint.iacr.org/2018/1188.pdf), and not just the b^B * h^r = z check.

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/7f870ca932f724e9e083f88d54b58e6074aa2b7b_2_482x499.png)image568×588 51 KB](https://ethresear.ch/uploads/default/7f870ca932f724e9e083f88d54b58e6074aa2b7b)

---

**denett** (2019-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> Note that the verifier needs to additionally check that A’ accumulates from A

This check should be done for every published accumulator value to make sure the operator is only doing additions. See my comment on this post:[Let's assign prime numbers to transactions instead of coins - #7 by denett](https://ethresear.ch/t/lets-assign-prime-numbers-to-transactions-instead-of-coins/4578/7)

If this is done, I think the b^B * h^r = z check is sufficient.

---

**emacbrough** (2019-02-23):

In [@gakonst](/u/gakonst) 's deep-dive, he cautions against using [@vbuterin](/u/vbuterin) 's non-membership due to the lack of a formal proof. I just wanted to chime in for those not convinced by Vitalik’s argument above, with a direct constructive reduction from Vitalik’s NMP to the LLX NMP.

Suppose we’re trying to prove that a prime x is not committed to in A, and we are able to produce q,r where 0<r<x and (g^x)^q=Ag^r as in Vitalik’s scheme. First of all we can replace q\gets q-1 and r\gets x-r, so that we instead have (g^x)^q\cdot g^r=A.

Since x is prime, we know \gcd(x,xq+r)=1, since otherwise x|(xq+r)\implies x|r, but 0<r<x by assumption, contradiction. Thus by running the Euclidean algorithm on x,xq+r, we can find a,b such that ax+b(xq+r)=1. But g^{xq+r}=A by assumption, so g^{ax}A^b=g^1, which exactly means that (g^a,b) is a valid LLX proof.

**EDIT/P.S.**: For batched NMPs of x_1,...,x_n, it is **not** enough to simply make sure 0<r<\prod x_i. You further need to verify that \gcd(r,\prod x_i)=1. If x is in the accumulator, then for any arbitrary m you can produce a batch NMP for x,m that’s valid except for the fact that x|r.

---

**denett** (2019-03-06):

As [@gakonst](/u/gakonst) explains in his deep dive, the value B should be prime and is calculated via a hash to prime function. Is there an efficient way to do a hash to prime function on chain? Or is there an efficient method to verify that a given B is calculated correctly?

---

**adlerjohn** (2019-03-08):

Forgive me if this seems like a stupid question, but where/how are the results of MODEXP stored, in order to be used later? Doesn’t the EVM only support 256-bit integers natively?


*(3 more replies not shown)*
