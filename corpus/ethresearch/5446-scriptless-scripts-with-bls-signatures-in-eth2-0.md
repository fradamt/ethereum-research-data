---
source: ethresearch
topic_id: 5446
title: Scriptless Scripts with BLS signatures in ETH2.0?
author: Mikerah
date: "2019-05-13"
category: Cryptography
tags: [stateless]
url: https://ethresear.ch/t/scriptless-scripts-with-bls-signatures-in-eth2-0/5446
views: 3155
likes: 5
posts_count: 9
---

# Scriptless Scripts with BLS signatures in ETH2.0?

Scriptless Scripts enable us to use digital signatures in order to enforce execution of smart contracts off-chain. Here, we define a smart contract as a trustless multiparty cryptosystem. They were originally introduced by [Andrew Poelstra](https://github.com/apoelstra/scriptless-scripts/blob/94a4e2f961c839bd1b9ca8773abadbf0f198c34b/md/atomic-swap.md) in the context of Schnorr signatures and MimbleWimble. In 2018, [Moreno-Sanchez and Kate](https://lists.linuxfoundation.org/pipermail/lightning-dev/attachments/20180426/fe978423/attachment-0001.pdf) developed scriptless scripts using ECDSA, the signature scheme currently used in Bitcoin and Ethereum.

Naturally, one might think to attempt to figure out Poelstra-style scriptless scripts using BLS signatures. If this could be done, it would enable some forms of DApps such as atomic swaps in ETH2.0, potentially as early as Phase 0 (with some modifications of course).

So, I spent the past few weeks undertaking this endeavour. I have finally come to the conclusion that due to the properties of BLS signatures, Poelstra-style scriptless scripts may not be possible. A few Grin core developers have arrived at this conclusion several months ago and [have written up a document that goes into details about why](https://github.com/mimblewimble/grin/files/2905763/MWpp.pdf).

I would like to note that even though my attempts have been futile, I think pursuing pairing-based scriptless scripts is an interesting research problem. In fact, I might continue pursuing it.

If anyone is interested in working on developing pairing-based scriptless scripts, feel free to reach out.

UPDATE: I emailed Andew Poelstra about this. He seems to agree that is may not be possible to do this using BLS signatures for the same reasons outlined in the Grin dev’s article.

## Replies

**vbuterin** (2019-05-14):

Can’t we just do scriptless scripts via Schnorr sigs over the BLS curve?

---

**Mikerah** (2019-05-14):

Potentially. What the Grin devs came up with was a hybrid solution that enabled them to use BLS signatures whilst keeping the schnorr signatures. This compromise was made in order to still have scriptless scripts in Grin. I’m not sure if this would be a good compromise for ETH2.0 given the design goals. Assuming the same governance procedures, it could potentially be proposed as an EIP at a later date.

---

**vbuterin** (2019-05-14):

Why do we need a compromise or EIPs? These things can all be done at higher levels in contracts or execution environments.

---

**Mikerah** (2019-05-14):

The whole point of scriptless scripts is that we don’t need execution environments. Everything is enforced using the native digital signature scheme. If it’s possible to swap the digital signature scheme in ETH2.0 at a later point in the way you propose, then I suppose we can achieve Poelstra-style scriptless scripts by swapping to schnorr signatures.

---

**vbuterin** (2019-05-14):

> The whole point of scriptless scripts is that we don’t need execution environments.

How is that the whole point of scriptless scripts? I thought the point of scriptless scripts was privacy and efficiency?

The benefit of having it run in execution environments is so that we can easily try and run different schemes inside of eth2 without having to standardize a single one at consensus layer.

---

**Mikerah** (2019-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How is that the whole point of scriptless scripts? I thought the point of scriptless scripts was privacy and efficiency?

I exaggerated there. The point is that in order to take advantage of scriptless scripts, we don’t need execution environments. However, you do bring up an interesting point of leveraging execution environments in order to use alternative digital signature schemes in order to enable scriptless scripts in ETH2.0.

When do you think that would be possible to do? Can we potentially get it at Phase 1?

---

**vbuterin** (2019-05-14):

I think execution environments are part of phase 2 “by definition”. But given the simplifications that we’re seeing to phase 2, it could come fairly quickly.

---

**Rbchi1** (2019-05-15):

As far as I know, what Andrew Poelstra want to do is accomplishing more application than just transaction without script or contract,like in the MW environment.But it is tricky that they still use timelock in Grin to fulfill atomic swaps.In other word,I don’t know what part of Scriptless script can be adopted in ethereum environment. improve performance?

