---
source: ethresearch
topic_id: 5525
title: "ShareLock: Mixing for Cryptocurrencies from Multiparty ECDSA"
author: seresistvan
date: "2019-05-29"
category: Cryptography > Multiparty Computation
tags: [transaction-privacy]
url: https://ethresear.ch/t/sharelock-mixing-for-cryptocurrencies-from-multiparty-ecdsa/5525
views: 4207
likes: 9
posts_count: 6
---

# ShareLock: Mixing for Cryptocurrencies from Multiparty ECDSA

In this post I would like to introduce and explain briefly ShareLock, which we believe, [@omershlo](/u/omershlo) and me, that can bring privacy-enhanced transactions to Ethereum **TODAY**.

For more details please have a look at the [paper](https://eprint.iacr.org/2019/563.pdf) and the [Github repo.](https://github.com/KZen-networks/ShareLock)

tl,dr: ShareLock is a novel coin mixer, which unlike previous proposals is deployable on today’s Ethereum. It does not rely on account abstraction or relayer services.

A few weeks ago [@HarryR](/u/harryr)  posted a super exciting, plain-spoken and honest post here: [Privacy/Anonymity on Ethereum is Doomed](https://ethresear.ch/t/privacy-anonymity-on-ethereum-is-doomed/5430) This is a good start if you are not familiar with the privacy issues we are having on Ethereum.

Ethereum still lacks a commonly used privacy-enhancing overlay. For instance, in this regard, Bitcoin is ahead of Ethereum, since we can use Chaumian CoinJoin developed by Wasabi wallet. Even if there were several proposals, they did not work and did not get traction. And this is not by accident.

**[![|643px;x391px;](https://ethresear.ch/uploads/default/optimized/3X/c/8/c8475ff709bb2e5183df1cdecdb6e0df6f8f11ef_2_690x419.png)|643px;x391px;929×565 76.1 KB](https://ethresear.ch/uploads/default/c8475ff709bb2e5183df1cdecdb6e0df6f8f11ef)**

Möbius, Miximus by [@barryWhiteHat](/u/barrywhitehat), MixEth and other mixer proposals work as follows:

1. Users deposit equal amount of coins into a smart contract.
2. They withraw mixed coins from a fresh address by providing some non-linkable cryptographic proof (zkSNARK, ring signature etc.) to prove that they deposited previously.

The problem with this design is that at step 2. transactions cannot be issued without leaking privacy as of today. Either Alice funds herself the fresh address or she sends the tx via a relayer service. The details and the framework for a relayer service is not established. *OR* we could wait for the account abstraction which would allow recipients to pay for the incurred gas costs. Account abstraction might come in 2020, 2021, … who knows?!

ShareLock chose a different design:

**[![|519px;x422px;](https://ethresear.ch/uploads/default/optimized/3X/d/c/dc7e552304dcc919ae21cdc878a34b71cebb30dc_2_615x500.png)|519px;x422px;678×551 68.6 KB](https://ethresear.ch/uploads/default/dc7e552304dcc919ae21cdc878a34b71cebb30dc)**

Users still need to deposit to a contract, this seems inevitable in mixing for account-based cryptocurrencies, since txs cannot have multiple outputs. Then they run off-chain a distributed key generation (DKG) protocol and threshold sign the list of the addresses derived from the threshold public keys.

Any of the participants, or say a wallet company, we call this party an activator could poke the contract with the threshold signed transaction to make the contract sending out the mixed coins to the addresses yielded from the DKG.

If parties are unable to threshold sign the “poke” transaction, then after a time-out they are able to withdraw their dirty coins (unmixed) back to their original addresses.

Since security is proven in the UC framework one could just pick her favourite threshold ECDSA protocol. In the paper we sticked to the [GG’19 paper](https://eprint.iacr.org/2019/114). However one could also use threshold BLS in order to avoid interactivity in the off-chain signing phase.

How does ShareLock relate to other privacy-enhancing solutions? [![jpg-large](https://ethresear.ch/uploads/default/original/2X/6/61326043fdfa0ac72e7b7dd3429a7a7782cb4b96.jpeg)jpg-large985×206 13.3 KB](https://ethresear.ch/uploads/default/61326043fdfa0ac72e7b7dd3429a7a7782cb4b96)

ShareLock provides k-anonymity and it consumes altogether cca.140k gas. Aztec gives confidential transactions, while Zether provides both. Currently an Aztec tx consumes cca. 900k gas, while Zether around 7.2M gas (almost fills an entire block).

We envision ShareLock as a useful plugin for wallets, where one would not only have a Send button but also a Send mixed coins button. The common and widespread use of such a privacy-enhancing overlay in the community could remarkably ameliorate privacy for everyone in Ethereum.

Please let us know your thoughts, comments, questions, critiques!

## Replies

**Mikerah** (2019-05-29):

How does this scale as the anonymity set grows? One of the major problems with mixers is that the anonymity set scales linearly with the number of people in the mixer.  There are have been recent constructions for ring signatures, for example, that allow anonymity sets to scale logarithmically in the number of people. These constructions are pretty new though and I have yet to see them applied to CryptoNote, RingCT, Mobius,etc.

---

**HarryR** (2019-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/seresistvan/48/1649_2.png) seresistvan:

> OR we could wait for the account abstraction which would allow recipients to pay for the incurred gas costs. Account abstraction might come in 2020, 2021, … who knows?!

This is one significant thing missing from Ethereum, “account abstraction” could enable any other blockchain to run on Ethereum as its own smart contract, if only the fundamental algorithms are supported (e.g. arbitrary operations over the secp256k1, bn256 and bl123-381 curves, various hashing algorithms etc.).

However, for now we could make do with ShareLock, and while it is considerably cheaper than Aztec and even more so than Zether, are they comparably as ‘private’ as either ZCash or Monero? What about in comparison - e.g. ShareLock vs Aztec vs Miximus vs Möbius etc.

With account abstraction it would be possible to be at least be half of what ZCash is, but without the lynch-pin nothing can even close can be achieved, with the limitations imposed.

---

**HarryR** (2019-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> How does this scale as the anonymity set grows? One of the major problems with mixers is that the anonymity set scales linearly with the number of people in the mixer.

Monero has worked hard to increase the size of the anonymity set, fundamentally by using ad-hoc linkable ring signatures with nullifiers to prevent double-signing, and ZCash also uses nullifiers albeit with an initial anonymity set which is *everything* rather than just the ring of N unwilling participants as is used by Monero. (and with delicate selection of the unwilling participants you can have good anonymity unless there are malicious active actors who willingly participate at their own cost because they know when they are 7/9 participants, or even 8/9 of the signers in the ring, then there is a limited cost associated with determining that anybody else signing in those rings is *you* rather than *them* etc.)

TL;DR I think that, without ring signatures without attribution or some kind of non-repeatable zero-knowledge set-membership proof, there is no way to increase the size of the anonymity set. And any effort on Ethereum will fall short because it’s just fundamentally not possible…

---

**Mikerah** (2019-05-30):

I just realized my mistake in my reply. Yes, when designing a mixer, you want the anonymity set to be as large as possible so that it’s harder to trace a transaction back to you. But, with a mixer, adding more people to the mixer increases the complexity of what is needed on behalf of the mixer’s participants. What I originally, meant is that this complexity is linear in the number of people in the mixer. Ideally, you want this complexity to be sublinear e.g. logarithmic.

---

**seresistvan** (2019-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> But, with a mixer, adding more people to the mixer increases the complexity of what is needed on behalf of the mixer’s participants. What I originally, meant is that this complexity is linear in the number of people in the mixer. Ideally, you want this complexity to be sublinear e.g. logarithmic.

I think this is quite bearable. If we would use [this recent paper](https://eprint.iacr.org/2019/523.pdf) from Jack Doerner, Abhi Shelat et al. for the threshold ECDSA, then this would be the off-chain complexity.

[![image](https://ethresear.ch/uploads/default/optimized/2X/6/6a1afe149d9c23fba14b6ded7e5701140064fbcb_2_690x364.png)image1184×626 54.2 KB](https://ethresear.ch/uploads/default/6a1afe149d9c23fba14b6ded7e5701140064fbcb)

IMO this is super promising and say for an anonymity set of 64 people, we could  threshold sign the “poke” transaction in less than 100 ms. This is crazy in my opinion. You would not even recognize the overhead once it is integrated into a wallet (Metamask, Mycrypto, ZenGo etc. etc.)

![](https://ethresear.ch/user_avatar/ethresear.ch/harryr/48/1671_2.png) HarryR:

> TL;DR I think that, without ring signatures without attribution or some kind of non-repeatable zero-knowledge set-membership proof, there is no way to increase the size of the anonymity set. And any effort on Ethereum will fall short because it’s just fundamentally not possible…

Correct me if I’m wrong but this attack vector is also present in Möbius/Miximus. One could just flood the mixer and then would have an easier time to de-anonymize the remaining parties in the contract. So in that sense even ring sigs/zkSNARKS cannot help.

![](https://ethresear.ch/user_avatar/ethresear.ch/harryr/48/1671_2.png) HarryR:

> However, for now we could make do with ShareLock, and while it is considerably cheaper than Aztec and even more so than Zether, are they comparably as ‘private’ as either ZCash or Monero? What about in comparison - e.g. ShareLock vs Aztec vs Miximus vs Möbius etc.

For the first question, my answer is that we need to see this once we have something widely adopted. From a privacy perspective IMHO it is better to have a widely used/adopted coin mixer or a barely-used shielded transaction pool a la Zcash.

In comparison with other coin mixer proposals I see mostly 3 main advantages. 1) ShareLock unlike Aztec, Miximus does not rely on a trusted-setup, which would be super challenging to carry out in a community-wide range. 2) ShareLock unlike Miximus/Möbius does not depend on the gas-payer linkability problem. 3) From an on-chain scalability perspective ShareLock is the best choice due to its significantly lower gas costs. Even if asymptotically the “poke” transaction grows linearly in the number of the anonymity set, one added party only means an added address in the arguments’ list. So it is luckily a tiny constant and is way better than that of Möbius for instance.

