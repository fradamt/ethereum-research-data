---
source: ethresearch
topic_id: 12808
title: Do not add bls12 precompile, implement Pasta curves w/o trusted setup instead
author: p_m
date: "2022-06-06"
category: Cryptography
tags: []
url: https://ethresear.ch/t/do-not-add-bls12-precompile-implement-pasta-curves-w-o-trusted-setup-instead/12808
views: 7711
likes: 37
posts_count: 27
---

# Do not add bls12 precompile, implement Pasta curves w/o trusted setup instead

Zcash got a huge upgrade: [NU5](https://z.cash/upgrade/nu5/), which uses [Pasta curves](https://electriccoin.co/blog/the-pasta-curves-for-halo-2-and-beyond/) as a basis for Halo proving system. These are two curves (Pallas & Vesta) with very interesting relation between them. Using these allowed ZEC to ditch trusted setup altogether.

In ETH2, BLS12-381 pairings are used to verify aggregate signatures for effective beacon chain communication. However, the need for trusted setup makes it deficient for apps that use circuits / zk-SNARKs.

Since neither EIP-2537, nor EVM384 precompiles have been implemented on mainnet, I would strongly suggest to focus on Pasta curves instead. Right now most zk apps on eth are using bn254, because it has its precompile. However, it’s pretty bad, the approximate security level can be just 100 bits, or even lower. Some time in the future, folks will start switching to new technologies. If we act early, folks won’t need to do `bn254 => bls12-381 => something w/o trusted setup`, they would be able to go straight to step 3.

Some readers would think adding BLS precompiles is fine, since “we can always add new tech later”, however this will require **all** EVM implementations to implement pairings on BLS curve and keep it forever, because VM code would still need to be executed in the future. That’s why I think it’s necessary to drop “bls in ETH apps” idea altogether.

We can keep using BLS12-381 for beacon chain, there won’t be any need for switches / upgrades.

## Replies

**MicahZoltu** (2022-06-07):

It seems to be that BLS12 in the EVM is useful because it allows you to do things like validate beacon chain compatible signatures.  Even if there are better things out there, BLS12 is used in the beacon chain and as long as that is true it will be useful (IMO) to have in the EVM.

---

**p_m** (2022-06-07):

> useful because it allows you to do things like validate beacon chain compatible signatures

How is that useful? Can you list precise use-cases where this is useful to have in EVM, instead of keeping it outside of EVM?

---

**mkoeppelmann** (2022-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/p_m/48/18530_2.png) p_m:

> How is that useful? Can you list precise use-cases where this is useful to have in EVM, instead of keeping it outside of EVM?

One usecase: if you could evaluate BLS signatures inside the EVM it would allow to run a light client of another beacon chain within the EVM. We (Gnosis Chain) are started another [beacon chain](https://beacon.gnosischain.com/) and could build (after the merges) a trustless bridge from and to Ethereum as outlined [here](https://hackmd.io/g8TK7IzYQjClTTaor-ypIQ).

---

**jgm** (2022-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/p_m/48/18530_2.png) p_m:

> How is that useful? Can you list precise use-cases where this is useful to have in EVM, instead of keeping it outside of EVM?

The next hard fork after the merge is likely to make either a beacon state root or beacon block root available, to allow for proofs of beacon information.  This can be useful for proving the state (*e.g.* balance) of validators on the beacon chain within the EVM.  Also possibly useful to prove withdrawals.

---

**p_m** (2022-06-08):

In any case, even if bls precompile gets added, I think we should point users to proper primitive for circuits, which is: pasta curves. Should we create a EIP for that?

---

**Pratyush** (2022-06-10):

Wrt SNARKs, constructions based on the pasta curves occupy a different trade-off space to constructions based on pairing-friendly curves like BLS12-381. In particular, achieving sufficiently fast verification of SNARKs for non-trivial circuits requires very involved constraint optimization skills, whereas achieving fast verification with pairing-based SNARKs is straightforward.

Also, pairings are useful for tons of other cryptographic primitives, like IBE, short signatures, quadratically-homomorphic encryption, etc., which could find applications later on.

---

**xerophyte** (2022-06-10):

agreed. I think the inherent trade-off here is

BLS: the ability to do pairing

Pasta: faster MSM

I can see the case that both are useful in the context of ethereum.

---

**xerophyte** (2022-06-10):

Also the trusted setup fundamentally is a property of the proof systems rather than the curves. For example, you can construct a proof system using BLS12-381/BN w/o trusted setup.

---

**p_m** (2022-06-11):

Where can one read more info regarding comparison of SNARK verification between those two? Are there papers, or so?

---

**kladkogex** (2022-06-14):

The only curve in ETH is very expensive.  In most useful cases of m out of n (even for things like 11 out of 16) , is way cheaper to implement a trivial multisig using many ECDSAs than to use BLS.

So the most important question is to make it cheap.

But then what I am always curios about is security.

Curves that have more mathematical structure than “random” curves are

per se less secure, unless proven otherwise, since the existence of the structure

may  be used for a compromise.

In most cases, people do not discuss this, and there were already examples in the

past that some of “specialized” curves have been hacked.

For example the Pasta curves mentioned here. Most of people do not know what they are, and only few will invest time in understanding them,  I am not even talking about analyzing their security.

Compare this to the original Diffie Hellman algorithm that arguably any person in the world with a high school math degree can understand and argue to be secure.

---

**asanso** (2022-06-17):

I would love to see an example of “specialized” curves being hacked. Unless you refer to anomalous curves (or supersingular one) I am not aware of any “specialized” curve that got attacked. What do you actually mean with “specialized”?

If with “specialized” you mean being built with Complex Multiplication (CM) method well the fact that are less secure than “random” curves is a bit a bold claim (with our current knowledge). There is no evidence that are insecure indeed. Even the curve currently used in Bitcoin/Ethereum namely secp256k1 has been built using CM .

---

**p_m** (2022-06-18):

> is way cheaper to implement a trivial multisig using many ECDSAs than to use BLS

BLS is used a) to construct aggregate signatures with constant-time verification b) for pairings. Can you show us how to construct such a signature with secp? It must be verifiable in O(1), not in O(n).

> Most of people do not know what they are, and only few will invest time in understanding them

There are very few people who know how pairings work, that doesn’t matter for all the great apps that are being built with them.

> Compare this to the original Diffie Hellman

So what? The progress train is moving, we need complex protocols.

---

**kladkogex** (2022-06-23):

Well - my argument is simply that the more mathematical structure an object has, the more work you need to prove that it is secure, simply because insecurity can come from combinatorial interactions of different mathematical the structure.

From this perspective:

Elliptic curves are less secure than regular numbers, and BLS is less secure than elliptic curves, because it has pairing structure, and Pasta curves are less secure than BLS, because it also has the Pasta thing ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

There has been very little work done on explaining why pairing-based crypto is secure.

People just hope for the most time.

There have been pairing curves with structure that people thought were secure and they turned out to be insecure.

99% of mathematicians that work in pairing-based crypto do not know how pairing works.

If you read the original BLS paper, they had no independent argument that pairing was secure, that just assumed it.

They just assume it exists and secure. The result is that several people on this planet understand things. Compare this to Diffie-Hellman algorithm based on simple numbers. Everyone understands it.

Complexity is equal to insecurity.

BTW pairing based crypto is still NOT approved for any use by NSA and US Gov

---

**CPerezz** (2022-07-01):

From my perspective(ZK-Crypto dev), the most common use cases for ZKCrypto are for example rollups and zkevm chains now. Things like TornadoCash or ZK.money, ZKEVM-Community edition or Polygon’s solution.

For these, it’s unfeasible to use IPA (pasta curves PCS to-go for) as the verification will take simply too much time considering how massive these circuits tend to be and the block times that we currently have. (Unless of course, a really cool design appears. But anyway they’d probably verify this proof inside of a SNARK and publish the SNARK proof instead).

Also it’s much more tricky to decide upon a cost for the MSM operations which would be variadic. And there’s a lot of MSM optimizations that require parallelism, AVX features and similar stuff that might not be possible to be integrated on all the node runners.

Pairings provide constant time results and are used always when you need to verify really big circuits in a really short period of time. You can still aggregate proofs anyway with aggregation circuits and verify a single one making verifier costs really cheap.

It’s also pretty difficult to imagine that in the short term that recursion would be taking over and making ETH chain unusable due to the abcense of precompiles in order to perform it.

---

**Pratyush** (2022-07-04):

While I agree that, all else being equal, simpler protocols are better, I don’t think your examples support this claim.

- If by “regular numbers” you mean schemes based on the hardness of DL in finite fields, then we know that these are at most as secure as schemes based on standard elliptic curves (not pairing-friendly ones); we have non-generic attacks on FFDL, while we don’t know of any non-generic attacks on ECDL.
- We don’t know that Pasta curves are “less secure” than pairing-friendly curves. In fact, we suspect the opposite: we have no known attacks on cycles of curves that are faster than the generic attacks, while for pairing-friendly curves we know of attacks that exploit the target group structure. Furthermore, there’s no indication that the Pasta curves (or any cycle of curves, for that matter) has a more complex implementation than a pairing-friendly curve. In fact, as somebody who’s implemented both kinds of curves, the Pasta curves required much less work to implement.

---

**Genya-Z** (2022-07-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Elliptic curves are less secure than regular numbers, and BLS is less secure than elliptic curves, because it has pairing structure, and Pasta curves are less secure than BLS, because it also has the Pasta thing

Except, the Pasta curves do not have a pairing structure.  Also, every CM curve, including the BLS curves, is part of a “pasta pair”.  Just because we don’t use its “pasta twin” doesn’t mean it doesn’t exist.

So by your logic we expect pasta curves to be more secure than BLS curves.

---

**Pratyush** (2022-07-22):

Quick correction, not every CM curve has a cycle; only *prime-order* CM curves have a cycle. However, secp256k1 has a cycle, so if we’re ruling out the Pasta curves by the cycle criteria, we should also abandon the secp256k1 curve.

---

**kladkogex** (2022-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/genya-z/48/9249_2.png) Genya-Z:

> So by your logic we expect pasta curves to be more secure than BLS curves.

OK )) Agreed )

But if they do not have pairing one cant have threshold and aggregated sigs

So bls precompile still needed

---

**Genya-Z** (2022-07-26):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> But if they do not have pairing one cant have threshold and aggregated sigs

Yes, one can.  See the following papers for examples of who to do this.

Rosario Gennaro, Stanisław Jarecki, Hugo Krawczyk, and Tal Rabin, *Secure Distributed Key Generation for Discrete-Log Based Cryptosystems*, J. Stern (Ed.): EUROCRYPT’99, LNCS 1592, pp. 295–310, 1999.

Rosario Gennaro and Steven Goldfeder, *Fast Multiparty Threshold ECDSA with Fast Trustless Setup*, https://eprint.iacr.org/2019/114.pdf

Rosario Gennaro and Steven Goldfeder, *One Round Threshold ECDSA with Identifiable Abort*, https://eprint.iacr.org/2020/540.pdf

---

**David** (2022-12-03):

Sorry for resuscitating an old thread, but I’m not finding much about the pasta curves and I would be highly interested in having some pasta curves support in the EVM. We also use them in Mina protocol and supporting them on the EVM would allow us to have a fully verified light client for Mina running in Ethereum.


*(6 more replies not shown)*
