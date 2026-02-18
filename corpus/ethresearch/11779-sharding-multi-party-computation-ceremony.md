---
source: ethresearch
topic_id: 11779
title: Sharding multi-party computation ceremony
author: chaser
date: "2022-01-14"
category: Sharding
tags: []
url: https://ethresear.ch/t/sharding-multi-party-computation-ceremony/11779
views: 2696
likes: 6
posts_count: 6
---

# Sharding multi-party computation ceremony

given that [sharding](https://github.com/ethereum/consensus-specs/blob/50a63c4135bfc919c8c4204cd68fe293f394c80e/specs/sharding/beacon-chain.md#introduction) will very likely use [KZG commitments](https://cacr.uwaterloo.ca/techreports/2010/cacr2010-10.pdf) and [those](https://dankradfeist.de/ethereum/2020/06/16/kate-polynomial-commitments.html) require a trusted setup, with the Merge now on the horizon, let’s start talking about the setup.

my initial thoughts:

- can we start collecting participants now to have a wide enough scale by the time the MPC ceremony is due?
- can the setup incorporate the results from any previous trusted setups (like Zcash’s Powers of Tau, Aztec’s Ignition, Tornado Cash’s setup) to lower the chances of a reconstructed private key?
- what is the greatest possible damage that someone with a reconstructed private key can do to a sharded Ethereum? can we parametrize the extent of this damage?
- if every participant computes the MPC with the same client, the MPC has a single point of failure (which is, ironically, what an MPC is supposed to guard against). not least in the spirit of a multi-client Ethereum, I think this setup is critical enough to warrant multiple implementations on multiple CPU architectures.

## Replies

**delbonis** (2022-01-17):

There is the [Perpetual Powers of Tau](https://github.com/weijiekoh/perpetualpowersoftau) project that I believe Tornadocash used, although it’s been some months since that repository was updated so I’m unsure of the current status.  It’s unnecessary to use an MPC for this, but it would be neat if someone made a contribution to it in an MPC using a heterogeneous set of computers they operated themselves.

Edit: Actually, I’m not sure which curve is planned to be used for the KZG commitment, I’m assuming BLS12-381 but PPoT is only BN254.

---

**chaser** (2022-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/delbonis/48/3957_2.png) delbonis:

> There is the Perpetual Powers of Tau  project that I believe Tornadocash used

nice catch, this is what I hazily remembered. from what I see Tornado Cash [did use](https://github.com/tornadocash/trusted-setup-server) a PoT ceremony but I’m not sure it’s perpetual. and yes, their curve was also BN254.

FYI, the repo you linked to doesn’t contain every contribution to that ceremony, the total was a bit over 1000.

![](https://ethresear.ch/user_avatar/ethresear.ch/delbonis/48/3957_2.png) delbonis:

> It’s unnecessary to use an MPC for this, but it would be neat if someone made a contribution to it in an MPC using a heterogeneous set of computers they operated themselves.

even if sharding could use this ceremony, why do you think an MPC is unnecessary? I have great respect for many of the known PPoT participants, but Ethereum mainnet consensus is something the human civilization may rely upon for centuries. guarantees should be as solid as possible. community members deserve a chance to take part in the security of the cryptography, and there’s not much to lose by adding more participants. commissioning a single participant to set up computers is no different trust-wise from adding just a single participant.

---

**delbonis** (2022-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/chaser/48/8372_2.png) chaser:

> FYI, the repo you linked to doesn’t contain every contribution to that ceremony, the total was a bit over 1000.

Do you know where the PPoT is being organized now?  I saw that the original organizer is no longer at EF now.

![](https://ethresear.ch/user_avatar/ethresear.ch/chaser/48/8372_2.png) chaser:

> even if sharding could use this ceremony, why do you think an MPC is unnecessary?

Well you could think of a PoT ceremony as a kind of MPC.  You get a similar trust model at the end.

Maybe someone should organize another PPoT ceremony using BLS12-381? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**chaser** (2022-01-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/delbonis/48/3957_2.png) delbonis:

> Do you know where the PPoT is being organized now?

no idea. isn’t it still at the repo you linked to?

by the way I [asked](https://discord.com/channels/791603868696969276/791603868696969279/933047346151972886) people at Tornado Cash and I guess their setup is not useful in this case because it is related to BN128.

![](https://ethresear.ch/user_avatar/ethresear.ch/delbonis/48/3957_2.png) delbonis:

> Well you could think of a PoT ceremony as a kind of MPC. You get a similar trust model at the end.

I though “MPC” and “ceremony” are interchangeable in this context.

![](https://ethresear.ch/user_avatar/ethresear.ch/delbonis/48/3957_2.png) delbonis:

> Maybe someone should organize another PPoT ceremony using BLS12-381?

that’s why I posted in the first place ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) with regards to the curve, input would be appreciated from [@dankrad](/u/dankrad).

---

**dankrad** (2022-01-18):

Yeah indeed we will be using BLS12_381. The ceremony is indeed on our radar now. I think we will be building on existing setups to add security.

If you are interested in helping with this effort, feel free to contact me.

