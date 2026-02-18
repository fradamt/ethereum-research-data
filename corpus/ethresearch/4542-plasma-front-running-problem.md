---
source: ethresearch
topic_id: 4542
title: Plasma Front Running problem
author: kladkogex
date: "2018-12-10"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-front-running-problem/4542
views: 2252
likes: 7
posts_count: 6
---

# Plasma Front Running problem

A Plasma problem that has not been discussed yet, is front running.

Plasma uses a bond that goes to the challenger in case of a dispute.

The problem is that challenges can be intercepted and front-executed.

In fact, a logical thing for a miner to do on receipt of a challenge in the pending queue, is to replace it with her own challenge and execute.  The miner need to do no work in this case.

Therefore, in some cases, all bonds can go to miners, and true challengers will get zero.

## Replies

**CarlBeek** (2018-12-10):

I may be missing the point of this issue, but I think front-running is largely aside the point. The bonds going to the miners instead of the “true challengers” doesn’t change the fact that there is an economic disincentive for Plasma operators to behave maliciously.

There is an argument to be made that this disincentives non-miners from trying to find faults with execution on a Plasma chain as they will never receive the rewards. The issue with this argument is that it fails to account for inherent interests of the participants of a Plasma chain to have their own contracts execute correctly. Namely, even if you do not receive the reward, it is still worth launching a challenge against a Plasma operator if it effects your smart contracts.

Furthermore, if front-running becomes an issue to such a degree that non-miners do not bother raising challenges and that it is not in the interests of a non-miner to have the execution of the Plasma chain to be correct, miners themselves will then begin to look for disputes because of the economic incentive of the bonds.

---

**MihailoBjelic** (2018-12-13):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/df788c/48.png) CarlBeek:

> if front-running becomes an issue to such a degree that non-miners do not bother raising challenges and that it is not in the interests of a non-miner to have the execution of the Plasma chain to be correct, miners themselves will then begin to look for disputes because of the economic incentive of the bonds

This is an assumption, at IMHO it could easily be a wrong one.

When frontrunning other people’s exits, miners put no effort/waste no resources (“low hanging fruits, let me grab it”). If they want to start looking for disputes, they need to invest time and resources (“not low hanging fruits anymore, should I bother?”).

---

**gakonst** (2018-12-13):

This is not a vulnerability for people who challenge exits of their own coins. They may miss out on collecting the bond, and pay the gas fees, but what they actually care about is the safety of their coin which is preserved. The attacker who maliciously exited is still disincentivized since they lose their bond (which goes either to the frontrunner or to the honest challenger).

This can only be exploited when considering watchtower models, since the frontrunners can effectively reduce the profits of the watchtowers. It can be solved by integrating a Submarine commit/reveal scheme so that it does not leak any information. Take a look at [libsubmarine.org](http://libsubmarine.org).

It should also be noted that this is a general issue of any game which relies on bonded challenges on a chain which is controlled by miners, such as payment/state channels as well.

This is a non-issue with very low priority imho which will only manifest after we solve how to do non-grievable watchtowers, and see these watchtowers gain adoption so that frontrunners even bother attacking them.

---

**MihailoBjelic** (2018-12-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> This is not a vulnerability for people who challenge exits of their own coins. They may miss out on collecting the bond, and pay the gas fees, but what they actually care about is the safety of their coin which is preserved.

This is only true if the nominal value of coins is substantial. One possible situation here: a user tries to prevent a malicious exit of her coins and ends up with a net loss (the gas paid is more valuable than the coins, but she planned to take the bond, too).

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> It can be solved by integrating a Submarine commit/reveal scheme so that it does not leak any information. Take a look at libsubmarine.org.

I like LibSubmarine but it introduces additional complexity (on top of all existing Plasma complexity ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)) and it has its own challenges (like any commit/reveal scheme).

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> It should also be noted that this is a general issue of any game which relies on bonded challenges on a chain which is controlled by miners, such as payment/state channels as well.

Absolutely, bonded challenges are a huge challenge. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> This is a non-issue with very low priority imho

Not sure.

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> solve how to do non-grievable watchtowers

Any resources/thoughts? I’m very pessimistic when it comes to this, except in cases when “watchtowers” are essentially a fully formalized, large pool of bonded entities with programmed behavior (similar to Polkadot and Eth 2.0 validators). Even then it’s a huge challenge to reshuffle them, and if you decide to permanently assign them to a set of users/chains, we all know what can happen after some time…

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> will only manifest after we see these watchtowers gain adoption so that frontrunners even bother attacking them

Frontrunners don’t care who they’re frontrunning (users or watchtowers), it’s the same for them, so this problem will manifest immediately (if it manifests at all).

---

**kladkogex** (2018-12-14):

There is a particularly interesting case of the bad guy front running his fraudulent exit.

I am trying to exit fraudulently, and then see that someone is reporting to me. I am front running this guy and get paid bond to myself.

I think the half of the bond needs to be burnt…

