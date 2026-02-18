---
source: ethresearch
topic_id: 4181
title: Plasma Prime spec?
author: nourharidy
date: "2018-11-08"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-prime-spec/4181
views: 4906
likes: 7
posts_count: 3
---

# Plasma Prime spec?

Other than [@vbuterin](/u/vbuterin)’s posts on RSA Accumulators, there seems to be no online resources describing the latest Plasma Prime flavour, not on ethresear.ch or anywhere really.

Is there a spec around that I am not aware of? If not, I assume that someone is working on the spec. In that case, how soon will it be published?

## Replies

**sourabhniyogi** (2018-11-11):

As of now, its [@vbuterin](/u/vbuterin) explaining the broad gist of it in the first 20 mins of [Plasma Researcher Call #17](https://youtu.be/YjTF05SeYxo?t=68).  I scribed the majority of it below, all errors and asides mine.

# Plasma Prime is Plasma Cash with RSA Accumulators

You have some accumulator A_0 which starts at some commonly agreed generator (e.g. A_0=3). When a Plasma block B_i is published, it includes a Sparse Merkle Tree (SMT) Root as before, but also a new accumulator value A_i that represents all the coinIDs that were modified in that block, with every coinID i assigned to a particular prime number c_i. The new accumulator A_i will be equal the old accumulator A_{i-1} to the power of the first coin c_1 to the power of the second coin c_2 to the power of the third c_3 and so forth so  A_{i} = A_{i-1}^{\prod{c_i}}.  (Aside: To see this concretely in Go, check out [my RSA Accumulator implementation](https://github.com/wolkdb/go-plasma/tree/master/accumulator) which illustrates the basic idea.)

### Exits

In order to use a transaction as part of an exit mechanism, you need: (1) the SMT branch (as before, which tells you what the actual contents of the transaction are, because RSA accumulators don’t manage key-value maps like SMTs); and (2) an RSA inclusion proof. With just 2 coins  c_0=2 and c_3=7 touched in block 7, the accumulator A_7 would equal accumulator A_6^{14} \mod  N (Aside: where N=pq where p,q are private key primes in a trusted setup, see [The RSA=trusted setup?](https://youtu.be/IMzLa9B1_3E?t=3934) then check how Bünz writeup on class groups solves this vs  [@JustinDrake EF-led modulus MPC generation ceremony of 2019](https://ethresear.ch/t/short-rsa-exclusion-proofs-for-plasma-prime/4318/8) where only one party has to be honest; also there is a lot of add/times/power interchanged and \mod N skipped that becomes clear to the implementer).  To prove that c_3=7 is part of this block B_7, you provide the cofactor 2. To prove that c_0=2 is part of block B_7, you provide the cofactor 7. But when blocks include thousands of coins, the cofactor will be a single very large number, which could be way bigger than the gas limit!  So instead we would like to use a special kind of proof-of-exponent scheme, invented in the context of [VDFs](https://tiny.cc/VDFs), where the verifier can check a VDF proof that y=x^{2^T}, for a large T e.g.1M-10B) using this trick from [Wesolowski (2018)](https://eprint.iacr.org/2018/623.pdf) to get a succinct proof that is on the order of a couple hundred bytes.  This [efficient Proof-of-Exponentiation](https://youtu.be/IMzLa9B1_3E?t=4493) needs to be articulated in a spec / prototype.

### Proof of Non-Spend

To make a proof of *non-membership*, you make a valid proof of membership adding into the accumulator a small non-zero offset/remainder that you could not make without that offset.

Example: Say, in block B_k, the coins modified are c_1=3, c_2=5, c_4=11, and you want to prove that coin c_3=7 was *not* included. Then  accumulator A_k = A_{k-1}^{165} (since c_1 \times c_2 \times c_4=3 \times 5 \times 11=165, and 165 \mod 7 = 0 is false!).   But with remainder 3 (between 0 and c_3=7) added to this accumulator, 165+3 \mod 7 = 0 (great!), where the cofactor for 7 is 24 (168/7=24).  The proof is that the previous accumulator A_{k-1} to the power of the coin id (c_3=7) to the power of the cofactor 24  is the new accumulator A_{k} = A_{k-1}^{7*24} and then the proof would provide the remainder, which is 3.  This valid inclusion proof, with this small non-zero offset/remainder, then serves as a proof of non-spend.

Critically, this proof does *not* have to happen between two *adjacent* accumulators but any two accumulators many blocks apart (e.g. A_{30} and A_{995}) – the proof takes longer to compute, but the resulting size of the proof and the complexity of verifying it is exactly the same, enabling O(1) history compression for non-membership proofs!

From [Log(coins)-sized proofs of inclusion and exclusion for RSA accumulators](https://ethresear.ch/t/log-coins-sized-proofs-of-inclusion-and-exclusion-for-rsa-accumulators/3839), instead of just assigning prime numbers to coins, you assign prime numbers to both coins and the entire binary tree going from coinID up to the root. Then for a proof of inclusion you need to provide a bunch of primes and for a proof of exclusion you prove one thing at the top of the tree.  Future posts forthcoming.

### Summary

Zooming out, for Plasma exits you need both (1) SMT Merkle branch and (2) RSA Inclusion proof, but for Proof of non-spend you only need (2) RSA Proofs of Exclusion.  The requirement for inclusion is an *and* and the requirement for exclusion is an *or*. An RSA proof of exclusion by itself proves that RSA proofs of inclusion within that range are not possible.

### How do you actually assign coinIDs to primes?

Since coinIDs are born in Plasma deposits sequentially, you may hope to assign coin ids 2, 3, 5, 7, 11, 13, … for millions to billions of coin IDs to primes that can be represented by many fewer bits than your typical 256-bit hash, gaining like a factor of 64 relative to needlessly converting hashes (256-bit) to really huge primes.

Suggestion from [prime gaps](https://en.wikipedia.org/wiki/Prime_gap) is to use mathematical results that within a large range, two prime numbers are not going to be more than ~25,000 apart. Then instead of hashing, you take the id multiplied by 25,000 (plus some constant to get into the large range) and then the clients would find the first prime after the id times 25,000, which is the same sort of approach a typical hash to prime function takes. Both the client and Root contract would actually run the algorithm for finding the first prime after like the id times 25,000 – where there are two primality tests to combine with simple rules to check divisors up to like 30.  There is the [Fermat primality test](https://en.wikipedia.org/wiki/Fermat_primality_test), but then [Carmichael numbers](https://en.wikipedia.org/wiki/Carmichael_number) can fool the test (e.g. 561 passes the Fermat primality test but is not prime).  So the recommendation is do a one-time untrusted set up and run though all the ids up to 2^{40} or more, which passes a Fermat primality test (with base 2) but are not actually prime and then shove this blacklist (which should be fairly small) into a contract and we make part of the primality test be checking against this, which every client can check themselves if they want to.

[@kfichter](/u/kfichter) proposed to organize community reference repos maintained by the community for Plasma Cash + Plasma MVP without any application specific baggage.  Starting “Specs” are on [learn-plasma](https://github.com/ethsociety/learn-plasma/tree/master/source/en/learn), which could have Prime specs and implementations separate or as part of the Cash thread.

---

**artall64** (2018-11-12):

We just added a draft of such proposal, with some custom improvements [Plasma Prime design proposal](https://ethresear.ch/t/plasma-prime-design-proposal/4222)

looking forward for the feedback

