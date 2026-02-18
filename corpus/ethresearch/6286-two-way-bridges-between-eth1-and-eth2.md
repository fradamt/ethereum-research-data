---
source: ethresearch
topic_id: 6286
title: Two-way bridges between eth1 and eth2
author: vbuterin
date: "2019-10-10"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/two-way-bridges-between-eth1-and-eth2/6286
views: 12018
likes: 6
posts_count: 14
---

# Two-way bridges between eth1 and eth2

The goal of this post will be to illustrate some of the challenges in making a two-way bridge between eth1 and eth2 (eg. to support two-way convertibility of ETH), and how it could be implemented.

An eth1 → eth2 link already exists as part of the eth2 proposal, and is necessary to allow deposits to happen. This link is implemented using the [eth1data voting mechanism](https://github.com/ethereum/eth2.0-specs/blob/fffdb247081b184a0f6c31b52bd35eacf3970021/specs/core/0_beacon-chain.md#eth1-data). Note that this mechanism assumes that PoS validators are an honest majority, and that the PoW chain does not get attacked (specifically, that it does not revert more than ~5 hours); if either assumption fails, then the two chains would no longer “agree” with each other. There is an implied “social contract” at least at the beginning that if either case happens this would be remedied, more likely via a soft-fork of the PoS chain, though if the PoW chain really does revert more than 5 hours then a community agreement that the attack chain is illegitimate is also quite likely. **Note that, in either of these cases, it is not possible for a failure of the PoS chain to necessitate a soft-fork of the PoW chain.**

If we want the eth1 chain to be aware of eth2 state (a prerequisite to allow ETH to move back from eth2 to eth1), there are two ways to do this. One is to have the PoW chain contain a light client of the PoS chain. The other is to have PoS finality also finalize the PoW chain. The latter could be done by adding a mechanism where if a PoS block B_S includes a reference to a PoW block B_W via `eth1_data` voting, and B_S is finalized, then B_W is also treated as finalized. However, this implies that PoW miners (and clients) also need to be running an eth2 implementation so that they know what eth2 chains are finalized.

[![TwoWay2](https://ethresear.ch/uploads/default/optimized/2X/1/17b77da4169642ffd40e156fe47966d1d6f5c7a1_2_690x131.png)TwoWay21208×231 15 KB](https://ethresear.ch/uploads/default/17b77da4169642ffd40e156fe47966d1d6f5c7a1)

[![TwoWay](https://ethresear.ch/uploads/default/optimized/2X/4/40bab01f90c5131362a26e702311fa982ef660b4_2_690x195.png)TwoWay1088×309 15.7 KB](https://ethresear.ch/uploads/default/40bab01f90c5131362a26e702311fa982ef660b4)

The former requires an eth2 client implemented inside of eth1. This would require either webassembly or native support for BLS-12-381 verification, neither of which are currently expected to happen soon. Additionally, it only provides a light-client level of security.

The latter is more interesting, because it gives eth1 a “native” form of reversion limitation (this is often called the “finality gadget proposal”). Note that this proposal does something different from the first, in that while it does make the eth1 *fork choice* aware of eth2, it does not immediately make eth1 aware of eth2 *state*. For instance, note that it’s theoretically possible for two competing eth2 chains to finalize the same eth1 block (this would imply eth2 has broken, but it is still theoretically possible). More commonly, there could be two eth2 finalized blocks where one is a child of the other, both of which support the same eth1 block, and some miners could be aware of the more recent of the two eth2 blocks and the others not aware. This is not a problem for “eth2 as finality gadget” but it does mean we need more infrastructure to make eth1 explicitly aware of eth2 block state for the purposes of allowing withdrawals from the deposit contract.

One possibility is to simply create an `eth2_data` voting mechanism inside eth1; essentially, replicate the same mechanism as used to make eth2 aware of eth1. This could be combined with the above to ensure consistency: eth1 miners would only vote for `eth2_data` blocks if those blocks are (i) finalized and (ii) reference in their `eth1_data` blocks that are ancestors of the eth1 block that the miner is building.

### Challenges

Both of these proposals would require eth1-side changes. Currently, the eth2 roadmap has zero eth1-side changes before “[the final transition](https://ethresear.ch/t/the-eth1-eth2-transition/6265)”. Both of these proposals would require emergency remedial action on the eth1 side if the eth2 side breaks. The latter proposal would require all eth1 miners to also be running an eth2 node. Hence, while both proposals are absolutely feasible, they are not something that should be implemented quickly.

However, as eth2 continues to run and proves its resilience, then there certainly comes a point at which implementing such a bridge makes sense. To reduce risks, there are a few things that could be done:

- Running eth2 voting on eth1 with a one-week voting period, to allow time for human intervention if things go wrong
- The eth1 chain becoming aware of eth2 finalized blocks via light client could also have a one-week delay before withdrawal for similar reasons
- Only turn the bridge on when deposited stake is high enough (eg. >5 million)
- Set the voting threshold higher than 50% (eg. 80%); bias the system toward not including any eth2 blocks unless there is strong agreement in their favor.

## Replies

**bitsbetrippin** (2019-10-11):

*“However, this implies that PoW miners (and clients) also need to be running an eth2 implementation so that they know what eth2 chains are finalized.”*

**
Summary**

Does this mean for pool operators, they would need to ensure they are running a eth2 implementation, additionally, if you wanted to have an instance where a individual miner wanted to mine eth1 PoW solo, they too would need to ensure eth2 was in operating locally.

NM, I read further and you answered this in the Challenges section.

---

**nrryuya** (2019-10-12):

If the “ETH2 as the finality gadget of ETH1” is enabled, favoring ETH2 over ETH1, how about putting `Eth2Data` in ETH1 block and adding a validity condition of ETH1 blocks (which is verified by ETH2 validators) that the `Eth2Data` must be a finalized block in ETH2 chain, instead of the `Eth2Data` voting inside ETH1?

---

**djrtwo** (2019-10-18):

[@nrryuya](/u/nrryuya) I agree with this. The eth1 block producers and eth2 validators would only see the eth1 block as valid if the `eth2data` contained within it is both (1) finalized and (2) either (a) the same `eth2data` as the previous block or (b) newer child `eth2data` consistent with the `eth2data` previously in the chain.

This does allow miners to stall inclusion of new `eth2data` but not to insert invalid data.

If the beacon chain had two conflicting finalized blocks (`A` and `B`), then the pow chain would likely fork into two versions of itself, one following `A` and one following `B`. And to note: if using the finality gadget, this would happen regardless of the `eth2data` mechanism.

---

**MihailoBjelic** (2019-10-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> this implies that PoW miners (and clients) also need to be running an eth2 implementation so that they know what eth2 chains are finalized

I assume that by “eth2 implementation” you mean the beacon chain client? If so, Eth1 miners (and clients) will only be aware of (finalized) crosslinks and will not be aware of the actual transactions happening in shards. Given that every “Eth2 → Eth1” transaction will have to be initiated as a shard transaction, I wonder how will Eth1 clients become aware of them?

Maybe this whole idea is only about moving beacon chain (staked) ETH back to Eth1?

---

**Mikerah** (2019-10-20):

If I understood correctly, in order to properly enable a eth1 <> eth2 bridge, you need both a way to introspect and validate state on both eth1 and eth2? If so, is there a way to possibly generalize this for say any EVM-based blockchain?

---

**vbuterin** (2019-10-20):

> If I understood correctly, in order to properly enable a eth1 <> eth2 bridge, you need both a way to introspect and validate state on both eth1 and eth2?

Yep!

> If so, is there a way to possibly generalize this for say any EVM-based blockchain?

It would be a blockchain-wide feature to have introspection capacity for specific other blockchains, and this would need to be implemented on both sides at protocol level, so I don’t expect this to be the mechanism by which ethereum becomes some kind of cross-chain interop chain. For that, you probably want the light client approach.

---

**cdetrio** (2019-10-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If we want the eth1 chain to be aware of eth2 state (a prerequisite to allow ETH to move back from eth2 to eth1), there are two ways to do this. One is to have the PoW chain contain a light client of the PoS chain. The other is to have PoS finality also finalize the PoW chain. The latter could be done by adding a mechanism where if a PoS block B_S includes a reference to a PoW block B_W via eth1_data voting, and B_S is finalized, then B_W is also treated as finalized. However, this implies that PoW miners (and clients) also need to be running an eth2 implementation so that they know what eth2 chains are finalized.

Isn’t “have the PoW chain contain a light client of the PoS chain” (the former) a prerequisite dependency for “have PoS finality also finalize the PoW chain” (the latter)? Or does the latter require a full client of the PoS chain, not just a light client?

I’m confused because the rest of your post compares them as two different ways, but really they are the same way: the PoW chain becomes aware of the PoS chain (as a light client or a full client). If we assume no long re-orgs of the PoW chain, then the two ways are equivalent.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The former requires an eth2 client implemented inside of eth1. This would require either webassembly or native support for BLS-12-381 verification, neither of which are currently expected to happen soon.

Doesn’t the latter also require an eth2 (light) client implemented inside of eth1?

---

**swapman** (2019-10-22):

This is a bit of a different angle, but from a markets perspective what would exchanges be expected to do?

Would all ETH be renamed as ETH1, representing ETH on the ETH1.0 chain, and then a new asset created of ETH2 representing ETH on the ETH2.0 chain?

A two-way bridge would create a no-arbitrage clause where any market price differential of ETH on ETH1.0 and ETH2.0 would be arb’ed out, but it would be hard to imagine what exchanges would otherwise do if not to support both chains? There are 3 options:

1. Refuse to support ETH1.0, force convert ETH balances of all users to ETH2.0 and only allow deposit/withdrawal of ETH2 after it is launched (ETH as an asset symbol now effectively is ETH2.0)
2. Refuse to support ETH2.0, only allow deposit and withdrawal of ETH1. (ETH as an asset symbol now effectively is ETH1.0)
3. Support ETH1.0 and ETH2.0 (where ETH disappears and two new assets are created which share the supply: ETH1 and ETH2):
(a) Leave users’ ETH balance as ETH1 and allow deposits and withdrawals for ETH1 and ETH2, but no convertibility tool in the exchange
(b) Force convert users’ ETH balances to ETH2 and allow deposits and withdrawal for ETH1 and ETH2
© Let users choose and have a convertibility tool between ETH1 and ETH2

---

**cdetrio** (2019-10-22):

The ideas in this thread are referenced by [a tweet](https://twitter.com/VitalikButerin/status/1185392070048960512?s=19) of pics from a talk by [@djrtwo](/u/djrtwo), which says that a two-way bridge would encumber eth2 and eth1 protocol development.

But these ideas can also be used to enable a two-way bridge that is entirely at the application-layer, so eth2 and eth1 protocol development can continue unencumbered.

I tried filling in some detail to see at which point the bridge becomes encumbering.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> One is to have the PoW chain contain a light client of the PoS chain.

option A: implement an eth2 light client as an EVM contract on eth1.

- to update the light client state, users must submit transactions to the contract (like the old btcrelay contract)
- no action or HF’s required for eth1 (except to add a BLS12-381 precompile; alternatively, add support for fast 384-bit or 512-bit multiplication to EVM)

option B: add an “eth2 bridge” to eth1 implemented natively in clients

- e.g. a new value is added to EVM: either as a field in the block header, or as the value returned by a new opcode ETH2_LAST_FINALIZED_BEACONBLOCKHASH. All eth1 miners run eth2 light clients to support this opcode. The valueis not entirely deterministic, as two blocks with different values may both be considered valid (like the Timestamp field in a block).
- HF is required on eth1
- effectively the same as option B, but better DevEx (a cheap and reliable opcode to read the relayed Eth2 finalized beacon block hash, instead of a contract which needs users to pay gas to update the relayed state)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The other is to have PoS finality also finalize the PoW chain.

The PoS chain already implicitly finalizes the PoW chain, by using eth1 block hashes for the eth1_data (to read the deposit contract). It would require an Eth1 soft fork to get miners to respect the PoS finality: the majority of miners can simply adopt a fork choice rule prohibiting reorgs at depths beyond the block finalized on the PoS chain.

To support a bridge, eth2 needs some way of transferring bETH between accounts (whether validator accounts or EE’s), and some way of reading eth1 contract state. Reading eth1 contract state could be done in eth2 at the protocol-level, like the `deposit_count` value read from the eth1 deposit contract. Or it could be done at the application-level, e.g. with Ewasm execution an eth1 light client could be implemented in Ewasm and state could be read from any contract on the eth1 chain by users submitting proof data in blocks (in beacon blocks or shard blocks).

At this point, we have all the features needed to implement a “two-way bridge”, which would enable two-way conversion between ETH on the eth1 chain and bETH on the eth2 chain.

What’s left unclarified is how the bridge would be implemented on Eth1. Here’s two possibilities:

- protocol-layer bridge:

the “bridge contract” is a contract on eth1 (a beacon chain block hash relay contract). possibly a “system contract” resembling the blockhash refactoring proposal
- bridge contract could be implemented using either option A (with relay logic implemented in EVM) or option B (relay logic implemented in eth1 clients, simplified usage as an EVM opcode ETH2_LAST_FINALIZED_BEACONBLOCKHASH)
- the bridge contract wraps bETH held on the eth2 chain as wbETH (wrapped-beacon-ETH). wbETH can be burned on the eth1 side to redeem bETH on eth2. Or it could issue new wbETH if a proof-of-burn on the eth2 side is provided
- an Eth1 HF is needed to make ETH and wbETH equivalent in the Eth1 protocol

application-layer bridge:

- the “bridge contract” is a contract on eth1 (a beacon chain block hash relay contract). possibly a “system contract” resembling the blockhash refactoring proposal
- bridge contract could be implemented using either option A (with relay logic implemented in EVM) or option B (relay logic implemented in eth1 clients, simplified usage as an EVM opcode ETH2_LAST_FINALIZED_BEACONBLOCKHASH)
- the bridge contract wraps bETH held on the eth2 chain as wbETH (wrapped-beacon-ETH). wbETH can be burned on the eth1 side to redeem bETH on eth2.
- users could do two-way conversion of wbETH back into ETH by trading with someone who wants to convert ETH into wbETH

Notice that for the most part, a protocol-layer bridge and an application-layer bridge are implemented in the same way. The difference is that a protocol-layer bridge requires an Eth1 HF to make ETH and wbETH equivalent.

---

**djrtwo** (2019-10-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> Isn’t “have the PoW chain contain a light client of the PoS chain” (the former) a prerequisite dependency for “have PoS finality also finalize the PoW chain” (the latter)? Or does the latter require a full client of the PoS chain, not just a light client?

The difference here is (A) *embeds* a beacon chain light client into the EVM as a contract while (B) requires eth1 clients to run a beacon chain client as an additional piece of software informing their consensus. If (A) were implemented that there would still need to be consensus rule changes on eth1 to respect native bi-directional transfers.

The nice thing about (A) is that you could do this and utilize the eth2 data layer *without* introducing any consensus changes on eth1, but that conversation is orthogonal to the bi-directional bridge.

---

**vbuterin** (2019-10-23):

The second proposal would basically require every validator of one system to run at least a light node of the other system. This is intentional.

---

**djosey** (2020-07-30):

Just for color and to add a potential use case to this conversation – I’ve been researching the possibility of building out a service that automatically splits staking rewards between two addresses (ie to [automatically fund a commons dao](https://ethresear.ch/t/incentivizing-commons-infrastructure-with-a-validator-dao/7761)

I asked the Prysm team about this and they suggested that the two most viable paths to achieve this were either 1. write an EIP for direct support for splitting staking rewards in Eth2 phase2 or 2. some implementation of the two way eth1-eth2 light client bridge.  Just figured I’d mention this here as I keep looking into it in case this specific use case might affect any future upstream architecture.

---

**SyedMuhamadYasir** (2023-04-25):

[@vbuterin](/u/vbuterin) hi, i know a lot of time has elapsed

i would like to know if any progress has been made in this regard ?

is there a bridge between PoS & PoW ethereum chains ?

