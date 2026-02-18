---
source: ethresearch
topic_id: 2273
title: Which BLS curve/DKG algorithm is going to be used for Casper?
author: kladkogex
date: "2018-06-17"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/which-bls-curve-dkg-algorithm-is-going-to-be-used-for-casper/2273
views: 4631
likes: 1
posts_count: 10
---

# Which BLS curve/DKG algorithm is going to be used for Casper?

From [https://www.youtube.com/watch?v=8-AZys80RrU](http://this video) it looks like Casper is undergoing major changes and the new version will be based on BLS signatures.

Is it known at the moment, which elliptic curve is going to be used for Casper? Also,  which Distributed Key Generation is going to be used for Casper? Is it going to be joint-Feldman?

How is one going to handle adding/removing validators to/from an existing validator set?  When a validator joins,  one will need generate a key share for this validator …

## Replies

**JustinDrake** (2018-06-17):

> which elliptic curve is going to be used for Casper?

The sharding/Casper [proof of concept code](https://github.com/ethereum/research/tree/master/beacon_chain_impl) uses BN128, and the not-set-in-stone plan is to move to [BLS12-381](https://blog.z.cash/new-snark-curve/).

> which Distributed Key Generation is going to be used for Casper?

We only do plain BLS aggregation (see [here](https://ethresear.ch/t/pragmatic-signature-aggregation-with-bls/2105)); there is no DKG. Aggregate public keys are recomputed for every aggregate signature with cheap curve multiplications.

---

**kladkogex** (2018-06-17):

Justin - thank you, this is very helpful.

Do you plan to implement signature verification in Solidity or it is going to be not smart-contract-based?

---

**JustinDrake** (2018-06-17):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Do you plan to implement signature verification in Solidity or it is going to be not smart-contract-based?

Signature verification will be outside of the EVM, implemented in native code. There will be a smart contract on the main chain to make 32 ETH deposits and initialise BLS identities with proofs of possession.

---

**kladkogex** (2018-06-17):

Vow … This does look like a total rework of Casper …

---

**cdetrio** (2018-06-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> We only do plain BLS aggregation (see here); there is no DKG. Aggregate public keys are recomputed for every aggregate signature with cheap curve multiplications.

Its easy to get confused on this point, because the other post about [offchain collation headers](https://ethresear.ch/t/offchain-collation-headers/1679) says:

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png)[Offchain collation headers](https://ethresear.ch/t/offchain-collation-headers/1679/1)

> We now instantiate a Dfinity chain called the “beacon chain” that sits below the main chain. The beacon chain provides a high-grade random beacon with a low-variance period length of 5 seconds. The beacon chain processes all transactions necessary for the random beacon, in particular the BLS Distributed Key Generation (DKG) transactions. The beacon chain processes no user transactions.

The confusion is because the old post has the best description of the beacon chain. The new post only focuses on the BLS signatures, and mentions the beacon chain only in passing. Perhaps it would help to have a full overview of the beacon chain and the signature scheme, in a single document.

---

**JustinDrake** (2018-06-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> the other post about offchain collation headers says

Although that post points in an overall direction which we have taken today, be careful with what ethresear.ch posts say. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) The ideas are generally quite fresh, definitely not authoritative, and most of them don’t make it to the final design.

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> the old post has the best description of the beacon chain

In that post I used Dfinity’s random beacon for illustrative purposes but RANDAO is the current plan. Also note the definition of “beacon chain” has changed. In that post I had a stricter definition where the beacon chain’s only role is to produce a random beacon.

Today we use the term “beacon chain” more loosely. It’s now both a random beacon and a “manager chain” for things like crosslinks, slashing conditions, accounting, Casper FFG. In other words, in Ethereum 2.0 the beacon chain is the new main chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> it would help to have a full overview of the beacon chain

See [this document](https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ?view).

---

**ChainSafe** (2018-07-09):

Recently our team has started implementing the beacon chain in js. One of our blockers is implementing [py_ecc](https://github.com/ethereum/py_ecc) in pure js. Just wondering if anyone has worked on something similar? Our repo is [here](https://github.com/chainsafesystems/lodestar_chain).

---

**vbuterin** (2018-07-10):

Have you considered compiling into asmjs or something similar from another language?

For example you could try using Cython to compile the python version, and then using some C -> asmjs compiler to get asmjs out.

I worry that native javascript will be absurdly slow for what is already a very expensive calculation (pairing verification).

---

**ChainSafe** (2018-07-10):

Thanks for the response! That’s exactly how we decided to proceed.

