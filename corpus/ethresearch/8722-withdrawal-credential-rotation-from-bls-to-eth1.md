---
source: ethresearch
topic_id: 8722
title: Withdrawal credential rotation from BLS to Eth1
author: vshvsh
date: "2021-02-21"
category: The Merge
tags: []
url: https://ethresear.ch/t/withdrawal-credential-rotation-from-bls-to-eth1/8722
views: 5306
likes: 3
posts_count: 6
---

# Withdrawal credential rotation from BLS to Eth1

The [PR to introduce Eth1 withdrawal credentials](https://github.com/ethereum/eth2.0-specs/pull/2149) had been merged and it’s clear it’ll be implemented in not so distant future.

There’s a number of protocols and stakers who would benefit greatly from the possibility to change their BLS withdrawal credentials to Eth1 EOAs/smart contract. Collectively they account for at least 10% of staked Ether, maybe more, and that share is growing. [Lido](https://lido.fi) alone [has >5% of all Ether staked and accounts for >20% share of all deposits these days](https://explore.duneanalytics.com/dashboard/lido-finance-extended). The withdrawal credential rotation feature can reduce the amount of counterparty risk in eth2 staking and make the existing liquid staking protocol more secure.

I see three possible ways that could be implemented, in no particular order of preference:

## Withdrawal credential rotation state transition function embedded in eth2 protocol

We can design a transaction-like method by which withdrawal credentials can be rotated at any time if authenticated by the current withdrawal credential holder. I don’t think it’s a good idea, because it’s a lot of additional complexity for the protocol and the client, and that feature had been discarded in the past for good reasons, both technical and economical in nature (e.g. it enables a eth2 validator market).

## One-time withdrawal credential change from BLS to Eth1

A variant of the previous option, but much more limited in scope. Only one change per validator is permitted, and it’s only from BLS credentials to Eth1 credentials. That one is easier to implement and has fewer economical implications. One possible mechanism would be to allow block producer to put a signal to change its withdrawal credentials in the block it makes, signed by the existing withdrawal credentials: that neatly avoids the hassle of implementing transactions on the base layer for now.

## One-time bulk change of withdrawal credentials during a hardfork

During the preparations of the next hardfork, or one after that, we can collect all the signals to change BLS withdrawal credentials to Eth1 ones without processing them (e.g. using graffiti field or eth1 calldata for ordering), and incorporate one bulk state transition in the hardfork itself. That would be a bit harder than the previous option coordination-wise but will allow making state transition function a one-time thing instead of a part of a protocol.

## Replies

**jgm** (2021-02-21):

On your options, the first is likely to be the easiest to implement.  The second allows validators to change withdrawal credentials (there was a discussion about this in the transfer thread, and there are ways around it, but it’s not as simple as “let the block proposer set the credentials”).  The third will always have the problem of someone missing the cut-off point to change the credentials.

The first option *will* create a validator marketplace, but the trick is to ensure it doesn’t create a marketplace *on the beacon chain*.  The simplest way to do this would be to require that the target withdrawal credentials start with `0x01` (although there are future-proofing considerations to be made).

---

**vshvsh** (2021-02-21):

Maybe that wasn’t clear, but option #2 allows validators to submit credential change requests iff they are signed by the withdrawal credentials in question. So they can’t change the credentials by themselves, but they can censor change requests.

Don’t really see the problem with missing cut-off point in #3 given that will have months to submit their request.

---

**lsankar4033** (2021-02-23):

Validators/pools may have time to respond to the hardfork in #3, but it still requires coordination effort+communication to make sure everyone knows to do it. IMO, it doesn’t seem worth the coordination challenge.

If I understand correctly, the funcationality of #2 is a strict subset of that in #1, right? #2 being one-time change and #1 being change as many times as you want?

---

**vshvsh** (2021-02-25):

Yes, #2 is minimalistic one-time key rotation option and #1 is key rotation at will.

---

**alonmuroch** (2021-02-28):

I think many are building applications based on the fact that the withdrawal credentials can’t be rotated dynamically.

I’d say a one time rotation is preferable.

Change on block proposal will not be intuitive for users, it could take weeks between block proposals… if you manage several validators that’s a bigger headache.

