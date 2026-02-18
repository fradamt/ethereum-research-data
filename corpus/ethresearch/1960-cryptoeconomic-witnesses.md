---
source: ethresearch
topic_id: 1960
title: Cryptoeconomic witnesses
author: JustinDrake
date: "2018-05-09"
category: Sharding
tags: [stateless]
url: https://ethresear.ch/t/cryptoeconomic-witnesses/1960
views: 2173
likes: 4
posts_count: 7
---

# Cryptoeconomic witnesses

**TLDR**: We suggest a scheme for proposers to omit witnesses in the context of stateless validator execution.

**Construction**

Let P be a proposer proposing a collation C for execution by stateless validators. Instead of providing a “witness object” W to validators, the proposer provides a “state object” S which only contains the storage elements (storage locations and data) accessed by transactions in C. Given C, S and the pre-stateroot, a stateless validator can compute a corresponding post-stateroot (or raise an exception if S has missing or extraneous storage elements).

If a particular storage element s \in S is invalid (i.e. does not correspond to the pre-stateroot) the next proposer can slash P by providing a Merkle path for the correct storage data at the storage location of s. In general, proposers are responsible for slashing other proposers in their windback, and are themselves liable to slashing if they don’t.

**Discussion**

When sharing a state object S the proposer is making an easily-refutable cryptoeconomic claim that storage elements in S faithfully corresponds to the pre-stateroot (Merkle root) without the need to share the witnesses (intermediate Merkle nodes) for storage elements (Merkle leaves).

The state object S handles the availability part of the witness object W, and the cryptoeconomic claim handles the validity part of the W. Because the bulk of W is intermediate Merkle nodes using S instead of W allows for synchronous stateless execution to consume significantly less bandwidth (~10x less bandwidth).

## Replies

**skilesare** (2018-05-10):

Yes! Of course.  Awesome insight.

---

**NicLin** (2018-05-12):

![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=9) on this improvement. But what if there’s a re-org which results in mismatched storage data?

If a proposer provide an invalid state object, he will lose the chance to earn proposer fee which perhaps already serves as an incentive for not providing invalid state object?

---

**JustinDrake** (2018-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/niclin/48/1326_2.png) NicLin:

> what if there’s a re-org which results in mismatched storage data?

The collation C and state object S are relative to the pre-stateroot, and a re-org changes the pre-stateroot.

![](https://ethresear.ch/user_avatar/ethresear.ch/niclin/48/1326_2.png) NicLin:

> If a proposer provide an invalid state object, he will lose the chance to earn proposer fee which perhaps already serves as an incentive for not providing invalid state object?

A proposer that provides an invalid state object is liable to slashing.

---

**NicLin** (2018-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> The collation C and state object S are relative to the pre-stateroot, and a re-org changes the pre-stateroot.

Is state object committed to the pre-stateroot? I was wondering if the state object prior to re-org can be used to slash the proposer after the re-org.

---

**JustinDrake** (2018-05-13):

> Is state object committed to the pre-stateroot?

Yes

---

**JustinDrake** (2018-06-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> a stateless validator can compute a corresponding post-stateroot

On second thought the validator does require witnesses to compute the post-stateroot when writing to (as opposed to reading from) the state. At least that’s with a dynamic Merkle accumulator such as the sparse Merkle tree planned for the EVM 2.0.

