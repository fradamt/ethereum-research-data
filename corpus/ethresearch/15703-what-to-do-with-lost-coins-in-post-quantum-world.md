---
source: ethresearch
topic_id: 15703
title: What to do with lost coins in post-quantum world?
author: AdamP
date: "2023-05-24"
category: Consensus
tags: []
url: https://ethresear.ch/t/what-to-do-with-lost-coins-in-post-quantum-world/15703
views: 2221
likes: 7
posts_count: 10
---

# What to do with lost coins in post-quantum world?

There is a certain (relatively high) probability that quantum computers capable of breaking the elliptic curve digital signature algorithm will be built within our lifetimes. These computers will be capable of deriving the private key from the public key of an ECDSA key pair. In relation to this, virtually every blockchain will struggle with the question of what to do with addresses that have not been migrated to quantum-resistant ones.

The community will face the crucial question of what to (not) do with such addresses. In the past months, I directly contacted many developers and researchers, and unfortunately the vision of what to do in such a situation differed roughly 50/50 between the two main options (described later). After further consideration, I thought it might be beneficial to open such a discussion here. I am not bringing any new proposal to save vulnerable addresses, but I would like to read more arguments for one option or the other. Or maybe someone can present a new choice. I appreciate any response as this might be a systemic risk in the future.

**Assumptions for the consensus choice:**

- quantum computers with enough physical qubits to crack the discrete algorithm will not be available within this decade
- we will have indications of reaching the scale of a quantum computer that might be capable of breaking the ECDSA a couple of years in advance
- Ethereum will be technically equipped for the post-quantum era on all fronts: quantum-resistant signature mechanisms are available for use in account abstraction wallets, STARKs everywhere, post-quantum secure signature aggregation schemes are implemented, etc.
- secure mechanisms for migrating from quantum-vulnerable addresses to quantum-resistant addresses can be easily used
- the research will show that tens of percents of the entire supply still remain not migrated and vulnerable (in 2019, Pieter Wuille calculated that for BTC approx. 37 % of supply is at risk). For ETH, the number can be similar or maybe even worse (reusing addresses).

**What is considered safe**: addresses from which a transaction has never been sent (and the public key has not been revealed on the blockchain), contract addresses with owners (EOAs) who have never sent any transaction (e.g. Safe wallets where we add addresses with no sent txs as the owners).

**What can be done**:

**1. Do nothing**

The easiest way is to do nothing and not touch vulnerable addresses. After a number of years, when QCs have sufficient performance, these addresses will be broken and the owner of such a QC (probably a state/military actor or a large corporation) will get the funds.

![:heavy_plus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_plus_sign.png?v=12) no need to make a controversial consensus choice

![:heavy_plus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_plus_sign.png?v=12) the fundamental premise of the blockchain remains: whoever presents a valid private key has access to the funds

![:heavy_minus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_minus_sign.png?v=12) it will be impossible to know who in fact has spent the funds from a given address (the real owner / quantum adversary?)

![:heavy_minus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_minus_sign.png?v=12) in case of insufficient distribution of powerful QCs, a large percentage of ETH supply can fall into the hands of a single entity

![:heavy_minus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_minus_sign.png?v=12) the possibility of unexpected inflation if the QC attacker decides to sell

**2. Lock them**

We can lock/burn/freeze vulnerable addresses. I liked [the idea from Justin Drake](https://www.reddit.com/r/ethereum/comments/o4unlp/comment/h2rhmnn/?utm_source=share&utm_medium=web2x&context=3):

> “What is the most palatable way to destroy such coins?”. My strategy (which strives for maximum fairness) would be to setup a cryptoeconomic quantum canary (e.g. a challenge to factor a mid-sized RSA Factoring Challenge composite) which can detect the early presence of semi-scalable quantum computers, ideally a couple years before fully-scalable quantum computers appear. If and when the canary is triggered all old coins which are vulnerable automatically get destroyed. Of course there will be complications and bike shedding around what constitutes a good quantum canary, as well as exactly which coins are quantum vulnerable

![:heavy_plus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_plus_sign.png?v=12) vulnerable coins out of circulation

![:heavy_plus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_plus_sign.png?v=12) everyone will have enough time to migrate

![:heavy_minus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_minus_sign.png?v=12) it is difficult to create the line and distinguish between vulnerable and invulnerable addresses (especially in the account abstraction world: we assume that in a couple of years most users will be using a smart contract wallet where they choose the spending conditions (including the signature mechanism which could eventually be quantum-resistant but also vulnerable ECDSA)

![:heavy_minus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_minus_sign.png?v=12) most activity will be on rollups anyway

**2b. Lock them but with a recovery operation**

Basically the second method with the following exceptions:

a)

> If an address has not been used, it’s safe, and if quantum computers come we would be able to make a hard fork that lets you move those funds into a quantum-safe account using a quantum-proof STARK that proves that you have the private key (vbuterin, https://www.reddit.com/r/ethereum/comments/rwojtk/comment/hrmqtry/?utm_source=share&utm_medium=web2x&context=3)

b)

> We completely ban the use of ECDSA but allow spending coins from addresses with revealed public key if the user presents a ZK proof that the key was derived from the mnemonic seed (we assume the seeds to be quantum resistant as they are “behind” the hash).

![:heavy_plus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_plus_sign.png?v=12) we will enable the recovery of the maximum amount of coins

![:heavy_minus_sign:](https://ethresear.ch/images/emoji/facebook_messenger/heavy_minus_sign.png?v=12) complexity, hard to find consensus for this

**TL;DR: having them frozen or having them stolen?**

## Replies

**MicahZoltu** (2023-05-25):

Since there is no hard line in the sand across which “all accounts are functionally compromised”, I don’t think we will be able to come up with a clear deadline after which we can reasonably lock user funds.  An account with 1 ETH in it will be economically secure for *far* longer than an account with 1000 ETH in it, so the threshold isn’t the same for everyone.

---

**PulpSpy** (2023-05-25):

I like this breakdown. For Case 1, another positive (I guess?) is that it incentivizes the development of quantum computing.

Are there any papers on (2b) that implement the STARK circuit for a “proof of knowledge of ECDSA private key / seed phrase” given an ETH address? It could be a fun project to see how much it costs in Cairo and to be able to say we have the circuits in hand.

---

**AdamP** (2023-05-25):

Moreover, for Case 1, the situation might not be as bad as with BTC, where we are almost certain that no one has access to the private keys of millions of coins (including Satoshi’s coins on P2PK addresses that have a revealed public key and thus are QC vulnerable). In contrast, with ETH, perhaps not a significant part of the supply is lost and people would migrate a big portion of it. Of course I have no proof of that and it might be helpful to estimate the amount of lost ETH.

2b: I haven’t read anything more comprehensive yet [except the following idea of quantum proof keypairs from Aayush](https://ethresear.ch/t/quantum-proof-keypairs-with-ecdsa-zk/14901). There was a similar idea years ago on Twitter in a conversation regarding a possible coin rescue in HD wallets. I found a [tweet from Adam Back](https://twitter.com/adam3us/status/1084546364288221188?s=20): *“also I think (fairly new thought) that HD keys that were reused could be soft-forked to require a Zero Knowledge proof of knowledge of the chain code and master even if the coin private key was public information. (and soft-fork made not be spendable with direct ECDSA.)”*

---

**PulpSpy** (2023-06-07):

I had initially thought for 2(b) that you would have to prove the pre-image you have is an actual ECDSA private key that corresponds to the ETH address, but in discussing this someone (David Jao, uWaterloo) he pointed out that knowledge of any pre-image is basically sufficient—if you know a pre-image, you crafted that address (assuming the hash function is still second pre-image resistant).

So you just need a STARK that can prove pre-images which is one of the first non-trivial circuits people try.

---

**AdamP** (2023-06-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/pulpspy/48/11243_2.png) PulpSpy:

> he pointed out that knowledge of any pre-image is basically sufficient—if you know a pre-image, you crafted that address (assuming the hash function is still second pre-image resistant).

But isn’t it the case (since the address is a part of a Keccak-256 hash of the public key) that once the address has a public key revealed, the pre-image is known by practically everyone, including the attacker? In the case of 2(b), I wanted to separate the quantum attackers (those who we assume to know both the public and private keys) and the real owners of the address (those who know the public and private keys, **but also the mnemonic seed**).

---

**PulpSpy** (2023-06-08):

That was just a mistake on my part, I meant 2(a) and not 2(b).

---

**MaverickChow** (2023-07-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/a/b19c9b/48.png) AdamP:

> In the case of 2(b), I wanted to separate the quantum attackers (those who we assume to know both the public and private keys) and the real owners of the address (those who know the public and private keys, but also the mnemonic seed).

What about the real owners of the address that did not use the mnemonic seed to generate their keys?

And I may also assume that whoever that successfully cracked the algo may also be able to “figure out” the right mnemonic seed for the keys as well.

I think locking or stealing coins that are speculated to be lost does not change the “fact” that the coin may really be lost and locking or stealing them would just finalize them being really lost for real.

If a coin is lost as a result of accident, then it should remain lost forever instead of expending undue amount of effort to recover it.

**Any effort that can successfully recover lost coins can be used by hackers to falsely “recover” coins that are not lost, as a way to steal them.**

---

**AdamP** (2023-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> And I may also assume that whoever that successfully cracked the algo may also be able to “figure out” the right mnemonic seed for the keys as well.

Well, the mnemonic seed is unlike the ECDSA key pair “protected” by the hash function which will be probably safe even for quantum attacks for the foreseeable future.

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> What about the real owners of the address that did not use the mnemonic seed to generate their keys?

Exactly. That’s why I think nothing like this can achieve consensus and after years, when QCs have sufficient performance (if ever), the lost (not migrated) coins will be vulnerable and eventually stolen.

---

**maniou-T** (2023-07-19):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/a/b19c9b/48.png) AdamP:

> “What is the most palatable way to destroy such coins?”. My strategy (which strives for maximum fairness) would be to setup a cryptoeconomic quantum canary (e.g. a challenge to factor a mid-sized RSA Factoring Challenge composite) which can detect the early presence of semi-scalable quantum computers, ideally a couple years before fully-scalable quantum computers appear. If and when the canary is triggered all old coins which are vulnerable automatically get destroyed. Of course there will be complications and bike shedding around what constitutes a good quantum canary, as well as exactly which coins are quantum vulnerable

This may be complex but worth to try. the decision between freezing or allowing vulnerable addresses to remain is a complex one that will require careful consideration and discussion within the blockchain community.

