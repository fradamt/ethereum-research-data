---
source: ethresearch
topic_id: 255
title: Fair exchange without a trusted third party
author: JustinDrake
date: "2017-11-26"
category: Sharding
tags: []
url: https://ethresear.ch/t/fair-exchange-without-a-trusted-third-party/255
views: 4673
likes: 10
posts_count: 11
---

# Fair exchange without a trusted third party

(The following mini result came about as I was thinking about tools to tackle data availability. I’m sharing it here as it may be useful for other purposes.)

In cryptographic literature the topic of “fair exchange” is an [active area of research](https://scholar.google.co.uk/scholar?hl=en&as_sdt=0%2C5&q=fair+exchange&btnG=) that tries to solve the following problem. You have two parties, Alice and Bob. Alice has a piece of data D_A (e.g. raw data identified by a hash, signatures, results of a database query, etc.) that Bob wants, and Bob has a piece of data D_B that Alice wants. Can one design a trade mechanism that ensures atomicity, i.e. either both Alice gets D_B and Bob gets D_A, or neither Alice gets D_B nor Bob gets D_A?

A key result in the field is that, in the general case, [fair exchange is impossible without a third party](https://pdfs.semanticscholar.org/208b/22c7a094ada20736593afcc8c759c7d1b79c.pdf). This impossibility result can be problematic for decentralised applications. For example, Filecoin wants to atomically exchange files for payment, but they’ve resorted to the mitigation of slicing the files into many small chunks which are released tit-for-tat using a payment channel (see [page 27 of the whitepaper](https://filecoin.io/filecoin.v2.pdf)). This is imperfect for example because the file may only be useful in its entirety, but the provider still gets paid for partially sharing the file.

As it turns out, fair exchange is possible without a trusted third party using cryptoeconomics (as opposed to pure cryptography). For that, Alice and Bob do the following:

1. They encrypt D_A and D_B using public keys Pub_A and Pub_B to produce E_A and E_B
2. They swap (non-atomically) E_A and E_B (this shouldn’t reveal information about D_A or D_B if padding is used)
3. They prove to each other in zero knowledge (e.g. using zkSNARKs or zkSTARKs) that E_A and E_B were correctly constructed
4. They post a large collateral (much larger than the value of D_A or D_B) into a fair exchange smart contract initialised with parameters Pub_A and Pub_B

Once step 4 is completed, the smart contract starts a countdown during which Alice and Bob need to post the private counterparts of Pub_A and Pub_B to the contract otherwise the corresponding collateral is burned. At this point, Alice and Bob are both highly incentivised to release the private keys, thereby completing the fair exchange.

## Replies

**vbuterin** (2017-11-27):

It’s worth noting the standard workaround to the fair exchange impossibility result is the computational one:

1: Both parties send each other the encrypted data, ZK-SNARK prove its correctness.

2. Both parties send each other the first bit of the decryption key, ZK-SNARK prove it.

3. Both parties send each other the second bit…

257. Both parties send each other the last bit of the decryption key.

Either party can abort at any point, but there is at most a 2x difference in the computational effort needed for the two parties to recover the data.

---

**JustinDrake** (2017-11-27):

Neat! This the basically the [scheme of Camacho](https://eprint.iacr.org/2012/288.pdf) (coincidentally the same guy as the [batch accumulator impossibility result](https://eprint.iacr.org/2009/612.pdf)) for signatures, but generalised.

The cryptoeconomic scheme protects against computationally powerful and/or patient adversaries, whereas the computational scheme protects against rich adversaries. This suggest the natural hybrid with *both* computational and cryptoeconomic guarantees: simply modify the fair exchange smart contract to allow any party to submit bits 1…n (with a zkSNARK proving correctness) and then require the other party to also respond with bits 1…n within a certain amount of time.

---

**MicahZoltu** (2017-11-27):

Has actually figured out the ZK-SNARKs required for this setup, or if they are just theoretical?  If they have been figured out, what is the computational power required for each?  You’ll be generating ~256 of them, and my understanding is that SNARKs are pretty expensive to compute making this a slow process at best on commodity hardware (e.g., laptop).

---

**vbuterin** (2017-11-28):

> You’ll be generating ~256 of them, and my understanding is that SNARKs are pretty expensive to compute making this a slow process at best on commodity hardware (e.g., laptop)

There are cheaper ways to do this. For example, you can encrypt a file 256 times with the encryption key being 0 or 1 each time, and then in each round you would remove one layer of encryption. Then you would only need one ZK-SNARK for the whole thing that you would do at the initial step.

---

**MicahZoltu** (2017-11-30):

Hmm, can you go into a bit more depth on that strategy?  On the surface, it seems like 256 encryptions with one of two keys suffers from one of two problems:

1. Given a key + encrypted data, you can validate whether or not the key matches.  In this case you only need to execute 512 decryptions, which is nearly free (in the timescales we are talking about).
2. Given a key + encrypted data, you cannot validate whether or not the key matches.  In this case when the counterparty gives you the next iteration of the key you don’t know whether they gave you a valid key or not (you won’t know until the last key is provided).

---

**JustinDrake** (2017-11-30):

I imagine the strategy is as follows. Each party also makes a commitment of the encryption keys, itself proved valid with the zkSNARK. For example, the commitment could be the Merkle root of a tree with 256 leaves where each leaf contains 1 bit committed using a binding and hiding scheme (e.g. each bit is concatenated with a random salt). Then in each round you would remove one layer of encryption by revealing the Merkle path for that bit.

---

**vbuterin** (2017-12-01):

Yeah, I actually realized later that having 256 layers of encryption with 2 possible keys is not such a good idea. I think what you want to do is indeed ZK-SNARK committing to the Merkle root of the bits of the encryption key.

---

**JustinDrake** (2017-12-05):

It may be worth noting that the cryptoeconomic scheme trivially generalises to [multi-party fair exchange](https://en.wikipedia.org/wiki/Multi-party_fair_exchange_protocol) (both single-unit and multi-unit general exchange). It may also help address DoS attacks from aborts in multi-party computations with identifiable abort (c.f. [here](https://eprint.iacr.org/2015/325.pdf) and [here](https://eprint.iacr.org/2016/187.pdf)).

---

**lovesh** (2018-08-27):

[@JustinDrake](/u/justindrake) Can you point to some resources elaborating on step 3, i.e., They prove to each other in zero knowledge (e.g. using zkSNARKs or zkSTARKs) that the ciphertexts were correctly constructed. Thanks

---

**JustinDrake** (2018-08-27):

That’s right. They prove to each other that the ciphertexts (most likely identified by some sort of hash) are correct. It turns out there’s a cryptoeconomic fair exchange scheme where zkproofs are not required. Below is the gist (credit to Greg Price also), reusing ideas from the challenge game in [proofs of custody](https://ethresear.ch/t/1-bit-aggregation-friendly-custody-bonds/2236).

---

Alice owns a file F identified by its Merkle root Merk(F). Bobs wants F in a fair exchange for something else, say ETH (could be another file). Let Enc(F) be the encryption of F, with random access to the encrypted 32-byte chunks. Alice sets up a collateralised smart contract with Merk(F) and the claimed Merk(Enc(F)), and sends the claimed Enc(F) to Bob. Bob notifies the smart contract he received the claimed Enc(F). This starts a 1-day countdown for Alice to send a decryption key k to the smart contract. When k is received another countdown starts in case Bob finds that the decryption of the claimed Enc(F) with k yields a file F’ where Merk(F) != Merk(F’).

The challenge game is a binary search to find an index i such that the 32-byte chunks of F and F’ at index i differ. Bob asks Alice for a Merkle branch from a random chunk index of F to Merk(F). Because the Merkle roots of F and F’ differ, the Merkle branch will identify a child of Merk(F) which differs. When the index i is found Bob sends two Merkle paths for the chunks of F and the claimed Enc(F) at index i, and the smart contracts checks that the decryption of the claimed Enc(F) chunks does not match F.

