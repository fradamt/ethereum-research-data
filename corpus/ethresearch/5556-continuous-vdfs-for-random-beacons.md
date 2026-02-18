---
source: ethresearch
topic_id: 5556
title: Continuous VDFs for random beacons
author: MihailoBjelic
date: "2019-06-04"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/continuous-vdfs-for-random-beacons/5556
views: 2053
likes: 4
posts_count: 3
---

# Continuous VDFs for random beacons

Cornell researchers have proposed Continuous VDFs.

In a nutshell, continuous VDF enable efficient verification of “sequences of VDFs”, which was not possible before.

The authors demonstrate three potential applications, the most interesting one probably being the construction of public randomness beacons that only require an initial random seed (and no further unpredictable sources of randomness).

Was wondering if someone looked into this in the context of blockains/beacon chains..


      ![](https://ethresear.ch/uploads/default/original/3X/7/9/7995f333f5f3d1beee809cc146dbc1b3039d1cdd.png)

      [IACR Cryptology ePrint Archive – 3 Jun 19](https://eprint.iacr.org/2019/619)



    ![](https://ethresear.ch/uploads/default/original/3X/e/7/e736bbb9f0ed43b3ded1a93346e3fffba5b71c39.png)

###



We introduce the notion of a \textit{continuous verifiable delay function} (cVDF): a function $g$ which is (a) iteratively sequential---meaning that evaluating the iteration $g^{(t)}$ of $g$ (on a random input) takes time roughly $t$ times the time...










cc [@JustinDrake](/u/justindrake)

## Replies

**JustinDrake** (2019-06-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> public randomness beacons that only require an initial random seed (and no further unpredictable sources of randomness)

If true this would be huge. Unfortunately, IMO their statement is at best very misleading. The authors have burried a critical caveat in footnote 2:

> we can only guarantee that the (\epsilon \cdot t)-th value into the future is unpredictable

So basically an attacker with non-zero speed advantage relative to honest players has linearly growing lookahead over time. This makes their construction non-practical for any application I can think of. Moreover, such an “eventually unpredictable” randomness beacon can trivially be built using a non-continuous VDF, especially in the context of blockchains where we have light clients.

---

**gokulsan** (2020-08-07):

Hi [@JustinDrake](/u/justindrake) Nice to see your succinct and sharp reviews on Continuous VDF. Can we construct a continuous VDF with recursive SNARKs with multi-exponentiation provers such that it can reduce the chance of linearly growing lookahead over time for verification. Please correct me if my inputs are misplaced.

