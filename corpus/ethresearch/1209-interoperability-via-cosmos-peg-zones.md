---
source: ethresearch
topic_id: 1209
title: Interoperability via Cosmos, Peg Zones
author: Chjango
date: "2018-02-23"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/interoperability-via-cosmos-peg-zones/1209
views: 5132
likes: 2
posts_count: 12
---

# Interoperability via Cosmos, Peg Zones

https://blog.cosmos.network/the-internet-of-blockchains-how-cosmos-does-interoperability-starting-with-the-ethereum-peg-zone-8744d4d2bc3f

## Replies

**kladkogex** (2018-02-23):

Lots of gas spend on each ECDSA verification.

Why dont you guys use threshold signatures? ![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)

How many witnesses are you going to use and how are you going to punish them for doing bad things? It seems like all of your security depends on them!

---

**nate** (2018-02-23):

What’s the recovery mechanism if there is a > 100 block fork? Does hub governance somehow have to get involved?

---

**asmodat** (2018-02-24):

There are no forks and no confirmations required in cosmos, once validators agree upon state its done at the same instant.

---

**nate** (2018-02-24):

This is true of the Cosmos hub or anything running Tendermint (to some extent, see a good point [here](https://ethresear.ch/t/fork-free-sharding/1058/5)), but I was specifically asking about a > 100 block fork on the Ethereum chain. As the article above states, the peg zone “waits for 100 blocks, the finality threshold, and implements this pseudo-finality over the non-finality chain.”

Thus, in the case that a > 100 block fork occurs, if the peg zone happens to have “pseudo-finalized” the fork that dies, then the peg zone must have some way to recover. It seems like governance or something similar is the solution here (especially considering the tokens floating around on the hub that might not really be where we think they are), but maybe I’m missing something.

---

**Chjango** (2018-02-27):

We’re opting for BLS signatures over threshold signatures because the former is non-interactive which saves us coordination overhead.

Witnesses will be the same set as the Cosmos Hub validators.

---

**Chjango** (2018-02-27):

You’re right; just a governance solution… ![:expressionless:](https://ethresear.ch/images/emoji/facebook_messenger/expressionless.png?v=9)

---

**kladkogex** (2018-02-28):

BLS signatures are threshold signatures ![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)

---

**Chjango** (2018-03-04):

No…The former is non-interactive while the latter is interactive afaik.

---

**Chjango** (2018-03-10):

To expound, a threshold signature is only valid if a certain threshold of signature shares is computed to complete 1 signature. To do this requires coordination overhead, classifying threshold sigs as interactive, meanwhile the threshold signature doesn’t contain information about the signees.

BLS signatures OTOH has distinct signers submitting individual valid signatures. And these can optionally be aggregated without coordination overhead.

---

**sunnya97** (2018-03-14):

> We’re opting for BLS signatures over threshold signatures because the former is non-interactive which saves us coordination overhead.

You can use BLS signatures as threshhold signatures or as plain aggregate signatures (both can be done non-interactively).

> Why don’t you guys use threshold signatures?

From some “back of the napkin” math, we calculated that in the current state, BLS verification in the EVM is more expensive than verifying multiple ECDSA signatures for the number of singatures in our use case (67 or less).

> How many witnesses are you going to use and how are you going to punish them for doing bad things?

The witnesses are the validators of the Cosmos Hub blockchain, and any wrongdoings will be punished through slashing on the Hub.

> What’s the recovery mechanism if there is a > 100 block fork?

Governance would have to figure it out.  But let’s be real, if there’s a 100 block fork in Ethereum, we’re gonna have 2 Ethereums ![:stuck_out_tongue_winking_eye:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue_winking_eye.png?v=12)

---

**MaxC** (2018-03-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/sunnya97/48/2035_2.png) sunnya97:

> From some “back of the napkin” math, we calculated that in the current state, BLS verification in the EVM is more expensive than verifying multiple ECDSA signatures for the number of singatures in our use case (67 or less).

Hey there, just a quick question as I do not know much about interoperable frameworks: how do interoperable zones deal with security? If you have N block-chains won’t that reduce the security by a factor of N, since any one of these may be compromised? Unless you are checking each block-chain for validity, but then you lose the benefits of  relying on N distinct block-chains to drive forward consensus.

