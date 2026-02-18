---
source: ethresearch
topic_id: 7640
title: A new efficient constant-time hashing to some Barreto-Naehrig curves (including BN256 and BN512)
author: dishport
date: "2020-07-05"
category: Cryptography
tags: []
url: https://ethresear.ch/t/a-new-efficient-constant-time-hashing-to-some-barreto-naehrig-curves-including-bn256-and-bn512/7640
views: 1819
likes: 0
posts_count: 4
---

# A new efficient constant-time hashing to some Barreto-Naehrig curves (including BN256 and BN512)

Hi guys,

My name is Dimitri Koshelev. I am a researcher from Moscow and Paris. My field of science is elliptic curves and pairing-based cryptography.

I invented a quite efficient **constant-time** hashing (that is **without inversions and quadratic residuosity tests**) to some elliptic \mathbb{F}_{\!p}-curves E\!: y^2 = x^3 + b of j-invariant 0.

More precisely, the new hashing is applicable if Frobenius trace t := p+1 - |E(\mathbb{F}_{\!p})| is divided by 5 (i.e. there is a vertical \mathbb{F}_{\!p^2}-isogeny of degree 5 to E) or Frobenius discriminant D := t^2 - 4p is divided by 9 (i.e. there is a vertical \mathbb{F}_{\!p}-isogeny of degree 3 to E).

My approach is similar to [that for curves of j=1728](https://eprint.iacr.org/2019/1294) and [the trick of Wahby-Boneh](https://tches.iacr.org/index.php/TCHES/article/view/8348) respectively. Moreover, the new hashing to BN512 is absolutely original from scientifique point of view.

The condition 5 | t is fulfilled, for example, for the Barreto-Naehrig curve BN512 (from the standard [ISO15946-5](https://www.iso.org/standard/69726.html)). This curve may potentially be used in the near future. At the same time, 9 | D for the curve BN256 from [Article](https://eprint.iacr.org/2010/186.pdf) (early it was very popular in the industry).

Before me, there was only one known constant-time hashing to BN256 and BN512, namely SWU (Shallue-van de Woestijne-Ulas) hashing (see, e.g., El Mrabet, Joye, Guide to pairing-based cryptography, par. 8.4.2). However, it requires to perform 2 quadratic residuosity tests (QRT). If I’m not mistaken, the unique known simple constant-time implementation of QRT is 1 exponentiation in \mathbb{F}_{\!p}.  But this is a very time-consuming operation.

In contrast, my hashing to BN512 in total contains only about 100 multiplications in \mathbb{F}_{\!p} (and the new hashing to BN256 is even more efficient).

It is worth noting that BN512 has no \mathbb{F}_{\!p}-isogenies of small degree from curves of j != 0. I checked that the smallest degree equals to 1291. Therefore the trick of Wahby-Boneh originally proposed for the curve BLS12-381 does not work for BN512.

In your opinion, is this a useful result ? Please let me know in order to collaborate if any of companies or startups continues to use BN256 in its products. In this case I can implement in one of programming languges the (very non-trivial) formulas of my hashing.

Best regards.

## Replies

**JustinDrake** (2020-07-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> My name is Dimitri Koshelev. I am a researcher from Moscow and Paris. My field of science is elliptic curves and pairing-based cryptography.

Welcome back to ethresearch ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> In your opinion, is this a useful result ?

The Eth1 blockchain (which currently only has opcode support for BN254) is increasingly reticent to adding more opcodes. As for the wider blockchain space (e.g. Chia, Dfinity, Eth2, Filecoin, Zcash), it is now favouring BLS12-381 over BN254.

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> my hashing to BN512 in total contains only about 100 multiplications in \mathbb{F}_{\!p}

Do you think it is likely significant improvements to Wahby-Boneh for BLS12-381 could be found, or does Wahby-Boneh feel close to optimal to you?

---

**dishport** (2020-07-06):

> Welcome back to ethresearch

Thank you)

> The Eth1 blockchain (which currently only has opcode support for BN254) is increasingly reticent to adding more opcodes.

Can you clarify this sentence please ?

> Do you think it is likely significant improvements to Wahby-Boneh for BLS12-381 could be found, or does Wahby-Boneh feel close to optimal to you?

I think the hashing of Wahby-Boneh is quite optimal. I don’t see how to improve it.

---

**JustinDrake** (2020-07-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> Can you clarify this sentence please ?

I mean it’s unlikely that an opcode or precompile for this new hash-to-curve would be added to the Ethereum 1.0 EVM any time soon. Ethereum 1.0 is increasingly ossified and hard to change.

![](https://ethresear.ch/user_avatar/ethresear.ch/dishport/48/4198_2.png) dishport:

> I think the hashing of Wahby-Boneh is quite optimal. I don’t see how to improve it.

Great, good to know ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

