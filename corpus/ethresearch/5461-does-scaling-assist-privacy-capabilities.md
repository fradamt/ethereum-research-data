---
source: ethresearch
topic_id: 5461
title: Does scaling assist privacy capabilities?
author: Econymous
date: "2019-05-16"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/does-scaling-assist-privacy-capabilities/5461
views: 2434
likes: 3
posts_count: 4
---

# Does scaling assist privacy capabilities?

Enigma is working on something called secret contracts. Data that can be kept private privacy yet run on the open blockchain. I’m doing my best at estimating exactly how it works, but i know that part of this privacy technique involves splitting the data between different nodes. Not all nodes carry the same data.

I was wondering if a scaling solution could amplify this sharding security.

Am I wrong?

## Replies

**adlerjohn** (2019-05-16):

The general approach to scaling with privacy tech is to 1) optionally hide transaction data 2) execute the transactions within the private execution environment 3) provide a proof that this execution was done correctly to the main chain, that is exponentially cheaper to verify than execution of the transaction data. It doesn’t really matter what privacy tech is used.

Unfortunately, while this scheme has incredible properties (see: [roll_up](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477) for one instantiation), it *should never be used*. A bug, such as one that allows the operator to mint themselves a bunch of coins, in the invariably extremely-complex off-chain circuit/code/whatever is used as privacy tech is impossible to prove on-chain. Blockchain are about *auditability*, not *verifiability*. In addition, proofs for these systems are usually extremely expensive to generate, and are monopolistic rather than competitive like mining, tending towards becoming permissioned.

---

**Econymous** (2019-05-16):

Thank you, I am gonna really need to digest this.

Okay. So it sounds a bit like enigma is trying to something that’s impossible?

---

**leafcutterant** (2019-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> while this scheme has incredible properties (see: roll_up  for one instantiation), it should never be used .

[@Econymous](/u/econymous) I’d like to clarify a bit as to what [@adlerjohn](/u/adlerjohn) probably meant by this, as their reaction could be taken for complete rejection. They probably meant that rollups and plasmas shouldn’t be used as building block baked into the layer 1 protocol. In *that* case, the exploitation of a vulnerability could enable an attacker to inflate at will and wreak havoc on layer 1. However, rollups and Plasmas as layer 2 solutions would be, I think, in their mind, completely acceptable. In that manner, no inflation dangers exist as these constructs rely on the security of layer 1. In fact, both already exist in live settings, plasmas can even be be found on the mainnet today. They indeed require some dedicated entities who are not the base-layer miners/validators, but these *can* function in a permissionless manner if implemented well. Today that’s not the case.

Not welcoming these solution on layer 1 is a valid point of view. However, I think adlerjohn is way too dismissive towards these approaches. Plasmas and rollups do have a place and can be used en masse. It all depends on how they’re implemented and whether your use case fits their level of security. (Playing with your cryptokitties? Definitely okay on a plasma chain. Settling a major financial transfer between two hostile countries? You may want to guarantee things by using layer 1.) Also, entire blockchains exist based on the verification of proofs, such as Monero’s utilization of zero-knowledge proofs.

Enigma works with multi-party computations. The work is split into small pieces and distributed among computing nodes. In simple terms, if the majority of the nodes don’t conspire with each other to share the pieces, the private part of the computation can’t be reconstructed. This also helps scaling, so it’s not something impossible. But it has security assumptions different from a publicly auditable blockchain. The level of security is highly dependent on *how* the solution is exactly built.

To try to answer your question, sharding already splits the load between many nodes. Whether adding MPC to it or replacing sharding with MPC is a good idea depends on the security properties of the MPC in mind.

