---
source: magicians
topic_id: 24999
title: "EIP-7998: Turn `randao_reveal` into a VRF"
author: aryaethn
date: "2025-08-04"
category: EIPs > EIPs core
tags: [core-eips, randao, randomness]
url: https://ethereum-magicians.org/t/eip-7998-turn-randao-reveal-into-a-vrf/24999
views: 431
likes: 3
posts_count: 3
---

# EIP-7998: Turn `randao_reveal` into a VRF

**EIP-7998: Turn `randao_reveal` into a VRF**

Hey Magicians,

Alberto ([@71104](/u/71104)) and I are proposing an EIP to hard-fork `randao_revea`l into a per-slot VRF. Instead of signing just the epoch number, the proposer now signs an SSZ container containing **(a) the previous epoch’s RANDAO mix** and **(b) the current slot**. Because the previous mix is unknown until the epoch closes, even the proposer can’t pre-compute future reveals, giving us *unbiased* randomness every slot.

### Why care?

- Helps reducing the well-known RANDAO bias attack vector.
- Enables secret-proposer/SSLE designs and powers follow-ups like EIP-7956.
- Uses existing BLS machinery; verification is already on-chain and free of extra proof gadgets.

The security argument rests on the [Computational Diffie-Hellman (CDH)](https://en.wikipedia.org/wiki/Computational_Diffie%E2%80%93Hellman_assumption) assumption (not [Decisional Diffie-Hellman](https://en.wikipedia.org/wiki/Decisional_Diffie%E2%80%93Hellman_assumption)), so the signature itself *is* the VRF proof.

You may see the specifications in the following PR:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/10093)














####


      `master` ← `71104:master`




          opened 07:02AM - 04 Aug 25 UTC



          [![](https://avatars.githubusercontent.com/u/1778989?v=4)
            71104](https://github.com/71104)



          [+103
            -0](https://github.com/ethereum/EIPs/pull/10093/files)







Authors: @71104 and @aryaethn.












Feedbacks are very welcome.

Thanks!

## Replies

**bbjubjub** (2025-08-04):

Hi [@aryaethn](/u/aryaethn),

Thank you for your proposal. I have some clarifying questions that I think would help figure out how much it would improve Ethereum.

Can you present an attack scenario that is thwarted by this change? The paper you reference uses *last revealer attacks*, and it does not seem like this change blocks those. The last n proposers in each epoch still have all the information they need when their slots come. Are there attacks where computing the randao mix multiple epochs in advance is useful?

Also a smaller thing: `randao_reveal` is already a VRF output, so I don’t think we can say we are turning it into a VRF.

---

**71104** (2025-08-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbjubjub/48/13986_2.png) bbjubjub:

> Can you present an attack scenario that is thwarted by this change?

A set of validators controlled by different actors may collude by publishing each other’s precomputed reveal sequences for future epochs, making the RANDAO bias vulnerability much worse.

That aside, the intended main goals of this proposal are:

- to support EIP-7956, and
- to pave the way for secret election of proposers, and that would completely block the RANDAO bias attack vector once and for all.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bbjubjub/48/13986_2.png) bbjubjub:

> Also a smaller thing: randao_reveal is already a VRF output, so I don’t think we can say we are turning it into a VRF.

I’m open to a different phrasing, but the current one looks sound to me because in the current implementation the entire reveal sequence of a participant can be precomputed for the foreseeable future, so you can’t really call it a Verifiable **Random** Function or at least you can’t use it as one.

