---
source: ethresearch
topic_id: 3839
title: Log(coins)-sized proofs of inclusion and exclusion for RSA accumulators
author: vbuterin
date: "2018-10-17"
category: Economics
tags: []
url: https://ethresear.ch/t/log-coins-sized-proofs-of-inclusion-and-exclusion-for-rsa-accumulators/3839
views: 6465
likes: 17
posts_count: 13
---

# Log(coins)-sized proofs of inclusion and exclusion for RSA accumulators

Prerequisite: [RSA Accumulators for Plasma Cash history reduction](https://ethresear.ch/t/rsa-accumulators-for-plasma-cash-history-reduction/3739)

In a naive RSA Plasma Cash implementation, each coin is assigned a unique prime number as a coin ID, and the RSA accumulator update for that block includes the coin ID for each coin that was spent. For a user with a width-n fragment, a proof of inclusion has size O(N) and a proof of exclusion has size O(N), and the operator has O(N) overhead, making this scheme ineffective if we want to achieve very fine denominations.

We’ll start off with a scheme that cuts down proofs of exclusion to size O(log(N)) at the cost of increasing proofs of inclusion for one coin to O(log(N)) (a proof for N coins only increases by a factor of two). We generate a tree of primes associated with indices of coins and subsets of indices corresponding to nodes in a binary tree, for example for 4 coins as follows:

![image](https://ethresear.ch/uploads/default/original/3X/c/d/cd01d2b34f6caeb8502bce55b696ecda10a6e3e2.svg)

To include coin 7, you would set A' = A^{2 * 3 * 7}. To include both coins 13 and 17, you would set A' = A^{2 * 5 * 13 * 17}, to include both 11 and 13 you would set A' = A^{2 * 3 * 5 * 11 * 13}. To prove membership of eg. coin 17, you would need to prove that 2 * 5 * 17 is part of the accumulator (ie. A' is a known power of A^{2 * 5 * 17}).

To prove non-membership of an **aligned slice** (a slice which corresponds exactly to a subtree), only a single proof of non-membership, eg. of 3, is required. For arbitrary slices, you can construct a proof that batches together log(n) proofs of subtrees; in general, any slice [a,b] can be decomposed into log(b-a) adjacent aligned slices. For example, to prove that 11, 13 and 17 are all not part of the accumulator, you would need to prove that 11 and 5 are both excluded, and so you need simply prove that log_A(A') \mod 55 is a value that is not a multiple of 5 or 11. Hence, proving non-membership of a range can now be done compactly. However, proving membership of a range unfortunately still requires a batched proof of all of the individual coins.

We can deal with this problem by extending the scheme further, making a Merkle forest instead of a tree:

![image](https://ethresear.ch/uploads/default/original/3X/f/0/f066284df69ced90380e58e8949c554c51ef959f.svg)

To prove membership of a single aligned slice, you now need to prove several things:

- The leaf value corresponding to the subtree is included, as are all of its ancestors up to that root.
- The leaf values in any higher tree in the forest are not included.
- The value corresponding to the subtree is not included in any lower tree in the forest.

This is best illustrated by example. Suppose we want to prove membership of coin 1 (ie. the second coin from the left). Values for which we prove membership are colored greed, and values for which we prove non-membership are colored red:

![image](https://ethresear.ch/uploads/default/original/3X/2/b/2bab198c2584210dde46fd61140fd1d61a688878.svg)

Now, suppose we want to prove inclusion of the aligned slice containing coin 0 and coin 1:

![image](https://ethresear.ch/uploads/default/original/3X/5/7/578018d558a9f1a24ff76557de39ed78ededa808.svg)

The general principle is that there are separate trees that are used to prove membership of an aligned slice at each 2^k size level, and this proof of membership includes a proof that aligned slices intersecting with that slice at higher or lower levels are not included.

Now, to prove that a given aligned slice is not included, we make a proof as follows (using coins 0 and 1 as an example):

![image](https://ethresear.ch/uploads/default/original/3X/5/b/5b0b49363d258cd9a40fc1c3e21230d55dee2f6a.svg)

This proves that:

1. The aligned slice [0...3] cannot be included (as that would require including the prime 2, which we prove is excluded)
2. The aligned slice [0...1] cannot be included (as that would require including the prime$7$)
3. The individual coins 0 or 1 cannot be included (as either of those proofs would require including the prime 13)

All of these proofs are of size log(n) for n total coins, and this includes both cost of verification and transmission *and* cost of construction. If all transactions ever only touched two-coin aligned slices, no one will ever need to do any calculations using the primes 19, 23, 29 or 31.

If a Plasma Cash implementation wishes to use a very large number of coins (eg. 2^{50} coins), then this is a very helpful feature. However, how do we assign primes to that many coins? Ideally, we want primes that are as small as possible, as these are more efficient to generate proofs for.

One solution is to come up with a function that deterministically generates a prime on-demand for any given index. Given what we know about [prime gaps](https://en.wikipedia.org/wiki/Prime_gap#Numerical_results), simply mapping x to the first prime above 25000 * x should be sufficient. The problem is that [deterministic 100% effective primality tests](https://en.wikipedia.org/wiki/Primality_test#Fast_deterministic_tests) have a high runtime, making them difficult to use on-chain. A simpler approach (thanks [@ldct](/u/ldct)) is to simply do one round of precalculation which generates the list of the first 2^{40} prime numbers and stores them in a Merkle tree; any use of the primes on-chain would need to be combined with a Merkle branch. Any client could check the precalculation locally.

## Replies

**ldct** (2018-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> To implement this in practice, the most efficient path seems to be to run a one-time “setup” computation (no trust required; anyone can independently check it) that runs through all values of get_prime(i)get_prime(i) for 0≤i<2400 \le i < 2^{40}) and finds all values that are not prime that do pass Fermat’s test (eg. Carmichael numbers ), and creates a file containing them. The implementation of get_prime used inside of the contract would use the Fermat test followed by checking non-membership in the file of “spooky numbers” created by the setup as its primality test.

It seems to me that if we are willing to impose on users the cost of a deterministic “setup” phase that explicitly enumerates ~ 2^{40} primes, one alternative would be for the plasma contract to hard-code a merkle root of a depth-40 tree containing the first 2^{40} primes, and any transaction that requires a hash-to-prime must provide witnesses into this tree.

---

**vbuterin** (2018-10-17):

Hmm, now that I think about it, I agree this is much better and lower hassle!

---

**ldct** (2018-10-18):

One problem with setup phases is that it seems unfeasible to enumerate even just 2^{50} primes, limiting the number of coins and hence granularity in a “range-based” system.

An alternative direction that works for classic plasma cash is cryptoeconomic primality proofs; the depositor provides a coinid, and the smart contract allows anyone who factors a coinid to instantly claim the coin without a challenge period; a coin validity rule is added that a recipient must run a primality test on the coin id before accepting the a coin.

Unfortunately this doesn’t work for range-based plasma cash, since we must have a way to compare coins in the exit game (if I am the proper owner of some interval I_1 and someone tries to exit I_2 such that I_1 \cap I_2 \ne \emptyset I must prove that I_1 \cap I_2 \ne \emptyset in the challenge game). I wonder if there is a way to fix this.

---

**vbuterin** (2018-10-18):

> One problem with setup phases is that it seems unfeasible to enumerate even just 2^{50} primes, limiting the number of coins and hence granularity in a “range-based” system.

Not necessarily. I think it could be done quite quickly if we built a truebit game to get it done and put up a mining reward (realistically a hybrid mining/staking reward; you’d need to put down your deposit to attest to the validity of any subtrees you compute). Bitcoin mining goes through 2^{80} hashes every few hours these days.

As one practical point, the prime number theorem estimates that the number of primes that fit into a 64-bit uint is \approx 2^{59.8}, so you don’t even need to get into the inefficiencies of bigints to run the computation.

Though I do agree that it is fundamentally limiting. Still though, even at 2^{40} primes, a denomination of $0.001 and a capacity of $1.1 billion seems totally reasonable for most applications. If you need more, you’ll have the resources to compute or pay for computing the 2^{50}.

---

**benj0702** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Though I do agree that it is fundamentally limiting. Still though, even at 2^{40} primes, a denomination of $0.001 and a capacity of $1.1 billion seems totally reasonable for most applications.

Actually, we can construct it so that the granularity/denominations between the Merkle accumulator and the RSA accumulator are not equal.  This just means if two merkle coins’ boundary does not align perfectly with an RSA boundary, both coins must download the tx merkle branch if either changes hands.  So, we can make arbitrary denomination payments on a much lower-fidelity RSA accumulator, at the cost of occasionally downloading neighbors’ transactions.

---

**nginnever** (2018-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> For a user with a width-n fragment, a proof of inclusion has size O(N)

Can we aggregate inclusion proofs with Shamir’s trick and reduce this to O(1) for a proof of inclusion of a batch of any transactions?

\pi_1^x=A , \pi_2^y=A , where \pi_1=g^{\frac{u}{x}} and \pi_2=g^{\frac{u}{y}}

*Shamir’s Trick*

a*x + b*y=1

\pi_{1,2}=\pi_1^b\pi_2^a

\pi_{1,2}^{x*y}=A

i.e.

let A=g^{3*5*7}, x=3, y=5

A=g^{105}

\pi_1=(g^{35})

\pi_2=(g^{21})

a*3+b*5=1

a=7

b=-4

\pi_{1,2}=(g^{35})^-4 * (g^{21})^7

\pi_{1,2}=g^{-140} * g^{147} = g^{7}

*check*

(g^{7})^{3*5} = g^{3*5*7}=A

To be clear I don’t fully yet understand simultaneous exponentiation, just following Benedikt’s work from his talk and have questions about how {a,b} are computed.

Also I wonder if it would just be easier to aggregate u and divide out the product of every transaction inclusion you are proving. Using the example above you can notice \pi_{1,2}=g^{\frac{u}{x*y}}

Using this, Wesoloski would be h=g^{x*y}, z=h^{\frac{u}{x*y}}

---

**keyvank** (2018-12-17):

This is a little bit hard to grasp. Is this how we include aligned slices [0...2] or [0...3] in our accumulator?

Coins 0 & 1 & 2:

![](https://ethresear.ch/uploads/default/original/3X/5/b/5ba6c8a55a93d3f90b4c4699d42193b89f3d74af.svg)

Coins 0 & 1 & 2 & 3:

![](https://ethresear.ch/uploads/default/original/3X/f/b/fb6a438e8c446ea175a0d852e8ab063a323685fc.svg)

---

**vbuterin** (2018-12-17):

Both look right to me!

---

**keyvank** (2018-12-17):

You explained how to create inclusion/exclusion proofs for aligned slices of coins but you didn’t explain how to “include” multiple arbitrary slices in this merkle-forest. I also had another question, if some range of coins is included in the accumulator, shouldn’t I also be able to create an inclusion proof for part of this range? E.g. If coins 0 & 1 are included using your scheme, shouldn’t I also be able to prove that coin 0 or 1 is included? In your example, I need to provide an exclusion proof for 13 in order to prove that aligned slice [0,1] is in the accumulator, if 13 is excluded, how can I then prove that coin 0 or 1 exists in the accumulator? (As I need inclusion proof of 13 here)

---

**vbuterin** (2018-12-18):

If an entire aligned slice is included, then you prove inclusion of any sub-slice by proving inclusion of the entire slice.

---

**vadym-f** (2019-04-04):

Regarding prime number generation and testing: relatively prime polynomials were used at IACR preprint 2008/363 like (1 + x * s) for a free variable x and a parameter s.

---

**vadym-f** (2019-04-04):

Another point: having parameters assigned to graph (tree) nodes like s and t for “source” and “target”, a “prime” polynomial was assigned to an arc like (1 + x * s + y * t)

