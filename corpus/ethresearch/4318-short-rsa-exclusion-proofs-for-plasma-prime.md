---
source: ethresearch
topic_id: 4318
title: Short RSA exclusion proofs for Plasma Prime
author: snjax
date: "2018-11-20"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/short-rsa-exclusion-proofs-for-plasma-prime/4318
views: 4345
likes: 12
posts_count: 11
---

# Short RSA exclusion proofs for Plasma Prime

# Short RSA exclusion proofs for Plasma Prime

## Some parameters of our plasma

The base data type for the amount is `uint48`.

The segment size for each fungible asset is `2^40`.

First segment `[0, 2^40-1]` is ether. The multiplier is `1e13`, so `1` in plasma is corresponding `10000gwei` in mainnet.

In addition, up to 256 types of assets (including ether with higher multiplier) may be included into plasma.

Prime set: each coin is corresponding to two prime numbers and each dust coin is corresponding two prime tree nodes.

The prime gap for 2^{50} elements is lesser than 916. 60 bits are enough to store  916 * 2^{50}. It is enough to use `64bit` prime numbers.

## Abstract

The similar prooving schema was proposed by [@vbuterin](/u/vbuterin) [here](https://ethresear.ch/t/log-coins-sized-proofs-of-inclusion-and-exclusion-for-rsa-accumulators/3839). For arbitrary segments effectivity of this schema is O((\log N)^2). For \log N \sim 50 we need to send about 2500 64 bit numbers to make inclusion proof in plasma. This is not cheap operation and it will be rejected due to the high gas cost by the Ethereum mainnet. Also, operation with a prime number at the Ethereum mainnet are not cheap.

Here we propose a special game helping us to prove valid exit from plasma without presenting inclusion proof at the beginning of exit procedure but using short RSA exclusion proofs.

\DeclareMathOperator{\Hash}{Hash}
\DeclareMathOperator{\Prime}{Prime}
\DeclareMathOperator{\included}{included}
\DeclareMathOperator{\ansestors}{ansestors}
\DeclareMathOperator{\descendants}{descendants}
\DeclareMathOperator{\inclusionprimes}{inclusionprimes}
\DeclareMathOperator{\inclusionnums}{inclusionnums}
\DeclareMathOperator{\exclusionprimes}{exclusionprimes}
\DeclareMathOperator{\inclusionproof}{inclusionproof}
\DeclareMathOperator{\exclusionproof}{exclusionproof}
\DeclareMathOperator{\True}{True}
\DeclareMathOperator{\False}{False}

## Single element proving schema

Let’s define a \in [g, A]_{RSA} if and only if \exists x: g^{ax}=A \mod N, where N is RSA divider.

Simple consequence is that a \notin [g, A]_{RSA}, if and only if \exists y: \gcd(y, a)=1, a \in [g, Ag^y]_{RSA}.

Let’s define s=\{a_i\} \subset [g, A]_{RSA} if and only if \forall a_i \in s: a_i \in [g, A]_{RSA}.

To prove inclusion of single element a we use proving schema proposed by Wesolovski [here](https://eprint.iacr.org/2018/623.pdf):

Let’s define

$$h = g^a \mod N,\ B=\Hash(g, A, h),\ b = h^{x \div B} \mod N,\ r = x % B.$$

Than proving key is \{b, r\} and it is enough to check following equation to prove the inclusion:

b^B h^r = A \mod N.

To prove the inclusion of multiple values, it is enough to prove the inclusion of multiplication of these values.

## Nested short RSA exclusion schema

Let’s we have RSA exclusion proof

a = \prod a_i \notin [g, A]_{RSA}.

It corresponds

a \in [g, Ag^y]_{RSA},\ \gcd(a,y)=1.

If we have about 2500 multipliers of 64bit primes per output, the cofactor y is about 160000 bit length and this is not useful for EVM.

As we can see below, in practice we need to prove the exclusion of one prime number. But if we store accepted from the operator proofs separately, we have huge overhead offchain, \sim2400 bits per prime vs 64 bits per prime if we store the proof batched.

We propose the following schema for short proof of exclusion of a single prime.

a \in [g, Ak]_{RSA}, \\
a_i \notin [g, k]_{RSA}, \\
a_i \in [g, h]_{RSA},

where

k = g^y \mod N,\\
h = g^{\prod a_i} \mod N.

From the first equation we got following

b^B h^r = Ak \mod N,\\

Indeed, to prove exclusion for a_i, we need to prove that a_i \notin [g, k]_{RSA}. That means that \gcd(y,a_i) = 1. The second part is to prove that a_i \in [g, h]_{RSA}. It is necessary in order to show that a_i is part of a.

So, we need to check two additional equations.

b_1^{B_1} g^{a_i r_1} = k g^{y_1} \mod N,\ 0<y_1<a_i,\\
b_2^{B_2} g^{a_i r_2} = h \mod N.

Proving key contains \{b,r,h,k,b_1,r_1,y_1, b_2, r_2\} 11072 bits or 43.25 `uint256` variables. It is not problem, because we are going to use it at the 2nd stage of exit game.

## Aligned slice proving schema

Let’s define aligned slice as slice [x, y], where y-x = 2^t and x = 2^t l, where t and l are natural numbers. To describe the proving schema the binary tree of aligned slices is a useful representation.

For further use, we associate each tree node with two prime numbers.

![tree1](https://ethresear.ch/uploads/default/original/2X/b/bb3110e8e815a04be156d2e0b409295cfe5993a3.svg).

This tree is corresponding to all aligned slices inside the segment [0, 8). For example, pair (5, 7) is corresponding slice [0, 4).

Let’s define inclusion of aligned slice [2,4) as an inclusion of following primes:

![tree2](https://ethresear.ch/uploads/default/original/2X/6/67c54f13f197e40d1323106adc509414c3ffe51b.svg).

The left point means that the corresponding slice is included completely. The right point means that at least one left point inside the current node or the ancestors is included.

Then we can define exclusion of aligned slice [4, 6) as the exclusion of following primes:

![tree3](https://ethresear.ch/uploads/default/original/2X/6/6ba6d34b675df5403f8b3f368d55acde28544922.svg).

As we see, inclusion and exclusion proof affect one slice, the proofs must conflict at only one point. At the figure below we see the conflict between inclusion proof of [2,4] and explosion proof of [4, 5) at prime 23.

![tree4](https://ethresear.ch/uploads/default/original/2X/f/faad37d9d28c304fd973a46a87f7f0b6c97f188e.svg).

Let’s determine inclusion and exclusion proofs through auxilary functions \alpha and \beta that is applicable for each aligned slice P of the tree and defined in the following way:

\alpha(P) = \included(P) \bigwedge_{Q \in \ansestors(P)}! \included(Q)

\beta(P) = \exists Q \in \descendants(P) \cup P: \alpha(Q)

\alpha(P) corresponds to the inclusion of the left prime and \beta(P) corresponds to the inclusion of the right prime.

Than define inclusion and exclusion proof for the aligned slice:

\inclusionproof(P) = \alpha(P) \bigwedge_{Q\in\ansestors(P) \cup P} \beta(Q) = \inclusionproof(\prod_{R \in \inclusionprimes(P)} R),

\exclusionproof(P) = !\beta(P) \bigwedge_{Q\in\ansestors(P)} !\alpha(Q) = \exclusionproof(\prod_{R \in \exclusionprimes(P)} R),

where \inclusionprimes and \exclusionprimes correspond the set of primes used for the proof (\{3, 7, 23, 29\} \{2, 11, 37\} for examples above)

As we can see, the operator cannot present inclusion proof for any included small coin. We define smaller intervals included if the operator present inclusion proof for any interval containing the one.

It is obviously to check, that

\exclusionproof(P) \Rightarrow !\inclusionproof(Q), \forall Q \in \descendants(P) \cup P.

\inclusionproof(P) \Rightarrow !\exclusionproof(Q), \forall Q \in \descendants(P) \cup P.

The main difference between this construction and proposed by [@vbuterin](/u/vbuterin) [here](https://ethresear.ch/t/log-coins-sized-proofs-of-inclusion-and-exclusion-for-rsa-accumulators/3839) is that we are using only inclusion proof to prove inclusion of aligned slice and only exclusion proof to prove exclusion of the aligned slice. This approach helps us to batch inclusion and exclusion proves for arbitrary segments, as you can see below.

## The exit game

The first enumerate all prime numbers used in the proof and determine

\Prime(N) = \max \{p \in \Prime: p\leq 1024 N\}.

\inclusionnums is the set of natural numbers corresponding \inclusionprimes.

Here is the game determining the validity of exit E. We use some components from [PrimeHash game](https://ethresear.ch/t/primehash-game-for-plasma-prime/4103).

The fist the exiter publish segment S. This segment determine aligned slices and included primes. If the challenger has exclusion proof coresponding S, he can compute conflict primes and prove exclusion of one. It is enough to reject the exit procedure.

https://raw.githubusercontent.com/snjax/drawio/master/rsagame2.svg?sanitize=true

[![rsagame](https://ethresear.ch/uploads/default/original/2X/1/1a7cede8012d41c087af4e6702474f69a5fdd1f7.svg).
See the figure with better resolution.](https://raw.githubusercontent.com/snjax/drawio/master/rsagame2.svg?sanitize=true)

## Bibliography

[Plasma call #17](https://www.youtube.com/watch?v=YjTF05SeYxo)

@vbuterin, [RSA Accumulators for Plasma Cash history reduction](https://ethresear.ch/t/rsa-accumulators-for-plasma-cash-history-reduction/3739)

@vbuterin, [Log(coins)-sized proofs of inclusion and exclusion for RSA accumulators](https://ethresear.ch/t/log-coins-sized-proofs-of-inclusion-and-exclusion-for-rsa-accumulators/3839)

Benjamin Wesolowski, [Efficient verifiable delay functions](https://eprint.iacr.org/2018/623.pdf)

@snjax, [PrimeHash game for Plasma Prime](https://ethresear.ch/t/primehash-game-for-plasma-prime/4103)

## Replies

**sourabhniyogi** (2018-11-20):

Thank you for working this out in detail!  You must know the answer to a very basic question: RSA has a trusted setup where the factorization of N=pq is known by someone.  If its the Plasma operator, the RSA accumulator can be fooled by the Plasma operator, and pretty much everything about the security of the accumulator is screwed.   Is this correct?

If so, I think we have to abandoned the RSA Accumulator in favor of a setup which is trustless, and all detailed proposals with RSA inclusion/exclusion proofs are meaningless, because most Plasma security concerns depends on being able to hold the Plasma operator in check.

---

**sg** (2018-11-20):

How do you think is the SNARKs(trusted setup) dependent construction(e.g. Zcash, Plasma snapp) meaningless? I would love to learn everyone’s attitude to trusted setup ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**JustinDrake** (2018-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/sourabhniyogi/48/808_2.png) sourabhniyogi:

> RSA has a trusted setup where the factorization of N=pq is known by someone

The Ethereum Foundation (in collaboration with several other participants) is working on an (n-1)-malicious secure RSA MPC with 1,000 participants. That means that if a single participant is honest then the RSA modulus (a single 2048-bit modulus) is secure, i.e. unfactorisable for everyone.

![](https://ethresear.ch/user_avatar/ethresear.ch/sourabhniyogi/48/808_2.png) sourabhniyogi:

> I think we have to abandoned the RSA Accumulator in favor of a setup which is trustless

Class groups have similar properties to RSA groups without a trusted setup. The main downside of class groups for accumulators is performance.

---

**vbuterin** (2018-11-20):

> The Ethereum Foundation (in collaboration with several other participants) is working on an (n-1)-malicious secure RSA MPC with 1,000 participants. That means that if a single participant is honest then the RSA modulus (a single 2048-bit modulus) is secure, i.e. unfactorisable for everyone.

For now, I would probably recommend using the RSA challenges, particularly RSA-2048: [RSA Factoring Challenge - Wikipedia](https://en.wikipedia.org/wiki/RSA_Factoring_Challenge)

---

**vbuterin** (2018-11-20):

Very nice!

I can see two issues:

1. Computing the coin-specific values b_1 and b_2 would still require raising g^{a_i} to the power of floor(\frac{y}{B_1}) and floor(\frac{\prod a_i}{B_2}), which would be expensive if there are many a_i values (particularly, if all a_i values were included, then I think there would be no space savings at all, as in that case h = Ak). So it seems to me like you’d need to find a balance; something on the order of sqrt(N) seems optimal. Or is there some different approach that you have in mind?
2. For Plasma exclusion proofs, the most convenient thing to do is that if A wants to send a coin to B, the Plasma operator can generate the proof for the coin that goes directly from the time A received it to the time A is sending it. Here, the proofs would need to be aligned across coins, so I suppose you would make them every day or something similar; this could increase the raw amount of data that needs to be maintained by the nodes.

---

**sourabhniyogi** (2018-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The Ethereum Foundation (in collaboration with several other participants) is working on an (n-1)-malicious secure RSA MPC with 1,000 participants.

So the vision is that EF conducts a ceremony like [Powers of Tau](https://z.cash.foundation/blog/conclusion-of-powers-of-tau/) with 1,000 participants one day, and all Plasma Prime implementers/users would take this public 2048-bit modulus as a given?

If so – excellent!  What is your predicted timing of reviewable MPC code (where?) + target ceremony time?

---

**JustinDrake** (2018-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/sourabhniyogi/48/808_2.png) sourabhniyogi:

> So the vision is that EF conducts a ceremony like Powers of Tau  with 1,000 participants one day, and all Plasma Prime implementers/users would take this public 2048-bit modulus as a given?

The ceremony is a nice byproduct of [the VDF project](https://slideslive.com/38911623/ethereum-20-randomness). It may make sense for some Plasma Prime implementers to participate in the MPC, and maybe the resulting modulus could become an industry standard. Having said that, there are various other options that make sense, e.g. using *both* RSA-2048 (as suggested by Vitalik) and the modulus from the ceremony, allowing to get security from both moduli.

> What is your predicted timing of reviewable MPC code (where?) + target ceremony time?

An academic paper by the Ligero team should be released in December. There’s proof-of-concept code written by them which is promising. For 256 participants on 256 different Google Cloud instances (in the same data center) it takes 100ms-300ms to generate a 256-bit modulus. The expectation is that the (synchronous) ceremony will take ~10 minutes to generate a 2048-bit modulus for 1024 participants spread across the world. I’m hoping for reviewable code early 2019 and the actual ceremony mid 2019.

---

**sourabhniyogi** (2018-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The expectation is that the (synchronous) ceremony will take ~10 minutes to generate a 2048-bit modulus for 1024 participants spread across the world. I’m hoping for reviewable code early 2019 and the actual ceremony mid 2019.

Beautiful connection between VDF / Ethereum 2.0 randomness and Plasma Prime!  By  “using *both* RSA-2048 and the modulus from the ceremony” you mean that a reasonable thing for all of us trying out Plasma Prime accumulator implementations is to use this specific constant from [RSA numbers - Wikipedia](https://en.wikipedia.org/wiki/RSA_numbers#RSA-2048) and then in mid-2019 just replace one constant with the ceremony result?

If you mean something else besides replacement, please explain –

---

**JustinDrake** (2018-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/sourabhniyogi/48/808_2.png) sourabhniyogi:

> If you mean something else besides replacement, please explain

I mean using both moduli at the same time in two parallel sub-accumulators. The accumulators is the concatenation of the two sub-accumulators, and witnesses are the concatenation of the corresponding two sub-witnesses. (I suggest you DM me if you have further questions because this is somewhat off topic ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12).)

---

**snjax** (2018-11-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Computing the coin-specific values b_1 and b_2 would still require raising g^{a_i} to the power of floor(\frac{y}{B_1}) and floor(\frac{\prod a_i}{B_2}), which would be expensive if there are many a_i values

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Here, the proofs would need to be aligned across coins, so I suppose you would make them every day or something similar; this could increase the raw amount of data that needs to be maintained by the nodes.

If we split the proof to 36-primes chunks it will use only twice the amount of disk space. But it is much simpler to generate proofs for accumulator with 36 primes than with millions.

So, coin-aligned proofs seems to be useful. The arbitary “coin” contains (log N)^2 primes. For N=2^{50} it is 2500. The overhead to store separate proofs for each coin is lesser than 1%.

It is not expensive to compute b_1 and b_2 for 2500 \{a_i\} set offchain.

If we do not spend coins every day, we do not need in proof for the coins. If we are accepting the coin, we request the history of the coin.

The defragmentation of the history is an open problem for us now. I am planning to model it and find the balance between aligning by coins or by transfers and splits.

