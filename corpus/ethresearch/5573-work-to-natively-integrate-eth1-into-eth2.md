---
source: ethresearch
topic_id: 5573
title: Work to natively integrate Eth1 into Eth2
author: JustinDrake
date: "2019-06-06"
category: The Merge
tags: []
url: https://ethresear.ch/t/work-to-natively-integrate-eth1-into-eth2/5573
views: 6849
likes: 9
posts_count: 11
---

# Work to natively integrate Eth1 into Eth2

**TLDR**: We outline considerations for a native integration of Eth1 into an Eth2 shard.

**Single shard**

Below are possible work items to “premine” the Eth1 consensus and state into a shard.

1. BLS vs ECDSA: Add BLS12-381 opcode or precompile to EVM to verify signatures of Eth2 consensus objects.
2. Keccak256 vs SHA256: Reduce gas cost of calls to SHA256 precompile (and possibly to all precompile calls) to facilitate checking Eth2 consensus Merkle paths.
3. roots: Add EVM opcode to read beacon chain block roots (alternatively, an opcode to read state roots). This could be useful, for example, to prove that a given Eth1 block has been finalized without adding an ad-hoc finality opcode.
4. SSZ vs RLP: Add support for SSZ and consider deprecating RLP.
5. sparse tree: Consider removing the hexary Patricia tree in favour of a sparse binary tree.
6. Casper FFG: As part of an intermediate hybrid PoW/PoS step, update PoW fork choice rule to respect beacon chain finality.
7. light clients: Replace PoW-based Eth1 light clients with PoS-based beacon chain light clients.
8. randomness: Find a migration path for dApps that rely on the nonce header field for randomness. RANDAO only provides a decent random number every epoch, not every block as with PoW.
9. Eth1 headers: Consider redefining Eth1 header fields which may no longer be relevant (e.g. ommersHash, difficulty, beneficiary, nonce, gasLimit) and make sure no significant dApps break as a result.
10. incentivisation: Remove PoW rewards.
11. difficulty bomb: Remove difficulty bomb.
12. statelessness: Build statelessness support into Eth1 clients (Geth, Parity, etc.). Also implement logic to produce Eth2-compliant shard blocks.
13. new liveness invariant: Make sure that there are no significant dApps that break when moving to regular 3-second slots (as opposed to the current Poisson distribution for blocks, with a ~15sec average block time).
14. libp2p vs devp2p: Migrate Eth1 clients from devp2p to libp2p.
15. Eth1 gas limit: Consider removing the Eth1 gas limit to avoid having two gas limits (Eth1 gas limit under Eth2 gas limit).
16. Eth2 gas limit: Make sure that 8,000,000 “Eth1 EVM gas” when translated to “Eth2 WASM gas” fits within the Eth2 gas limit. Significantly reducing the effective limit below 8,000,000 gas may cause unacceptable congestion. Check that the Eth2 gas mechanism (which would not have miner voting) is otherwise acceptable for Eth1.
17. WASMify Eth1 consensus: Formalise the Eth1 state transition function—including all precompiles—as WASM code. Split the WASM code into small chunks that fit within the Eth2 code limit (possibly 16kB per code chunk). This formalisation risks introducing consensus bugs on a $20B+ network so extensive fuzzing and formal verification may be required. We also want the WASM formalisation to be consistent with the wider WASM-for-blockchains standardisation effort.
18. premine load imbalance: Consider the negative consequences of the load asymmetry from premining the Eth1 state into a single shard with the other 1023 shards empty.
19. hard forks: Negotiate a timely hard fork schedule with the existing Eth1 ecosystem.
20. Eth2 consensus pollution: Consider disruptions to Eth2 whenever Eth1 will need to hark fork. Indeed, the Eth1 consensus would likely have “too big to fail” status within the Eth2 ecosystem (inconsistent with the expectation that execution engines are application-layer, not consensus-layer) which imposes an Eth2 hard fork for every Eth1 hard fork.

**All shards**

Below are further considerations to put Eth1 consensus logic on all shards.

1. state growth: Make sure that the ecosystem can handle 1024 privileged copies of the Eth1 consensus. In particular, the current no-rent approach may make the maintenance costs of tracking all shards too high for services such as exchanges and Etherscan.
2. shard number: Consider adding a shard number field in Eth1 headers to easily differentiate Eth1 execution engines running on different shards.
3. yanking: Add support for contracts to move between shards and make sure that the asynchronisity introduced does not break existing Eth1 dApps.

**Conclusion**

Safely integrating Eth1 into Eth2 is a significant engineering and governance effort. It seems doable on a long-enough (likely multi-year) timescale. The native integration should be compared to significantly cheaper medium-term alternatives. For example, a two-way bridge between Eth1 and Eth2 can be built using light clients.

## Replies

**mightypenguin** (2019-06-11):

A great start on a proposal.

I personally am against embedding Eth1.

Doing so has several issues you’ve noted (keeping them in sync with hardforks etc) that would slow down the evolution of Eth2.

It seems like running Eth2 as a “sidechain” (I’m using the wrong term there) is enough interop between 1 & 2. We really do want Eth1 to go away or be frozen at some point. Embedding Eth1 into Eth2 will keep people using for longer which is a bad idea in my opinion.

The biggest problem I see is moving to a storage rent model in the future with Eth1.

---

**vbuterin** (2019-06-12):

1. BLS vs ECDSA : Add BLS12-381 opcode or precompile to EVM to verify signatures of Eth2 consensus objects.

Why is this technically needed for eth1 integration? I can see how it’s useful for the eth2-in-eth1 light client, but if eth1 is part of eth2 then what is the benefit?

1. Keccak256 vs SHA256 : Reduce gas cost of calls to SHA256 precompile (and possibly to all precompile calls) to facilitate checking Eth2 consensus Merkle paths.

Seems reasonable regardless of the upgrade path.

1. roots : Add EVM opcode to read beacon chain block roots (alternatively, an opcode to read state roots). This could be useful, for example, to prove that a given Eth1 block has been finalized without adding an ad-hoc finality opcode.

I expect the `reduce` function in the eth2 execution abstraction would have access to beacon chain block roots. So would the idea be to make an EVM opcode that redirects to calling that? If so, seems reasonable.

1. SSZ vs RLP : Add support for SSZ and consider deprecating RLP.

Support!

1. sparse tree : Consider removing the hexary Patricia tree in favour of a sparse binary tree.
2. Casper FFG : As part of an intermediate hybrid PoW/PoS step, update PoW fork choice rule to respect beacon chain finality.
3. light clients : Replace PoW-based Eth1 light clients with PoS-based beacon chain light clients.

Support!

1. randomness : Find a migration path for dApps that rely on the nonce header field for randomness. RANDAO only provides a decent random number every epoch, not every block as with PoW.

You mean the `BLOCKHASH` opcode? It seems difficult to distinguish between `BLOCKHASH` for randomness and `BLOCKHASH` to verify historical Merkle proofs (though the latter will likely break regardless). If we expose historical blocks, most recent epoch RANDAOs should be easy to verify.

1. Eth1 headers : Consider redefining Eth1 header fields which may no longer be relevant (e.g. ommersHash , difficulty , beneficiary , nonce , gasLimit ) and make sure no significant dApps break as a result.

`gasLimit` may remain relevant; not sure yet.

1. incentivisation : Remove PoW rewards.
2. difficulty bomb : Remove difficulty bomb.

Agree!

1. statelessness : Build statelessness support into Eth1 clients (Geth, Parity, etc.). Also implement logic to produce Eth2-compliant shard blocks.

This should be starting to happen with [@AlexeyAkhunov](/u/alexeyakhunov)’s work soon/already, right?

1. new liveness invariant : Make sure that there are no significant dApps that break when moving to regular 3-second slots (as opposed to the current Poisson distribution for blocks, with a ~15sec average block time).
2. libp2p vs devp2p : Migrate Eth1 clients from devp2p to libp2p.
3. Eth1 gas limit : Consider removing the Eth1 gas limit to avoid having two gas limits (Eth1 gas limit under Eth2 gas limit).
4. Eth2 gas limit : Make sure that 8,000,000 “Eth1 EVM gas” when translated to “Eth2 WASM gas” fits within the Eth2 gas limit. Significantly reducing the effective limit below 8,000,000 gas may cause unacceptable congestion. Check that the Eth2 gas mechanism (which would not have miner voting) is otherwise acceptable for Eth1.

Agree!

1. WASMify Eth1 consensus : Formalise the Eth1 state transition function—including all precompiles—as WASM code. Split the WASM code into small chunks that fit within the Eth2 code limit (possibly 16kB per code chunk). This formalisation risks introducing consensus bugs on a $20B+ network so extensive fuzzing and formal verification may be required. We also want the WASM formalisation to be consistent with the wider WASM-for-blockchains standardisation effort.

Could we FV this using the existing EVM formalizations that have been created with K and the like?

1. premine load imbalance : Consider the negative consequences of the load asymmetry from premining the Eth1 state into a single shard with the other 1023 shards empty.

What are some concrete negative consequences that we might expect to see? Imbalance is not itself bad; blocks are imbalanced already all the time.

1. hard forks : Negotiate a timely hard fork schedule with the existing Eth1 ecosystem.

Note that it’s likely that the HF will require a 1-2 hour “chain shutdown” period. This is NOT unprecedented; it happened chaotically/involuntarily during the consensus failure in Nov 2016, but it is something that would need to be signalled beforehand.

1. Eth2 consensus pollution : Consider disruptions to Eth2 whenever Eth1 will need to hark fork. Indeed, the Eth1 consensus would likely have “too big to fail” status within the Eth2 ecosystem (inconsistent with the expectation that execution engines are application-layer, not consensus-layer) which imposes an Eth2 hard fork for every Eth1 hard fork.

Agree!

**All shards**

Below are further considerations to put Eth1 consensus logic on all shards.

1. state growth : Make sure that the ecosystem can handle 1024 privileged copies of the Eth1 consensus. In particular, the current no-rent approach may make the maintenance costs of tracking all shards too high for services such as exchanges and Etherscan.

My expectation is that the cost for exchanges’ storage largely comes from history, not state, as they have to store both and history is much bigger, and sharding is going to add a HUGE amount of history (10 MB/sec ~= 6 TB/week) regardless.

1. shard number : Consider adding a shard number field in Eth1 headers to easily differentiate Eth1 execution engines running on different shards.

Shouldn’t we just make `SHARD_NUMBER` an opcode?

1. yanking : Add support for contracts to move between shards and make sure that the asynchronisity introduced does not break existing Eth1 dApps.

Support!

---

**AlexeyAkhunov** (2019-06-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> statelessness : Build statelessness support into Eth1 clients (Geth, Parity, etc.). Also implement logic to produce Eth2-compliant shard blocks.
>
>
> This should be starting to happen with @AlexeyAkhunov’s work soon/already, right?

Yes, I am still on it. Have just done some simplifications and optimisations, to get more data, quicker, and now forcing my brain to gets some initial specs out…

---

**MaverickChow** (2019-06-15):

Will Ethereum 2.0 be using different algorithm to generate new private keys? In other words, will users with ETH stored in Ethereum 1.0 be in need to generate new public addresses and private keys and transfer ETH from Ethereum 1.0 to new Ethereum 2.0-based public addresses in order to participate in Ethereum 2.0 blockchain? Otherwise, why not just do a short cool down of the network in which during the cool down, a snapshot of all public addresses of the Ethereum 1.0 blockchain be taken, and correspondingly issue the same amount of ETH on Ethereum 2.0’s public addresses, where such Ethereum 2.0 addresses can be accessed with the same private keys generated from Ethereum 1.0? The same is with the dapps. Ethereum 1.0 transaction histories will just be maintained for the record.

Currently, two different private keys may lead to the same public key. So this may be a chance for Ethereum 2.0 to generate a much longer and different public address, so that a single private key may only lead to a single public address and not two with Ethereum 2.0. Users do not need to do anything extra except regenerate a new public address with a new Ethereum 2.0-based wallet generator, offline, and update their public addresses. Old public addresses from Ethereum 1.0 would be unusable in Ethereum 2.0 transactions. Cold storaged ETH since Ethereum 1.0 would remain cold thereafter. One problem is how to figure out what new public address to generate based on the old Ethereum 1.0 address alone. But this part is just optional.

The whole process will transition Ethereum 1.0 to Ethereum 2.0 layer 1 without being a shard.

Just my opinion.

---

**vbuterin** (2019-06-15):

I think the goal is to move toward account abstraction, where you can have addresses using whatever signature / anti-replay scheme you want.

---

**axic** (2019-06-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Keccak256 vs SHA256 : Reduce gas cost of calls to SHA256 precompile (and possibly to all precompile calls) to facilitate checking Eth2 consensus Merkle paths.
>
>
> Seems reasonable regardless of the upgrade path.

This is already considered for the upcoming Istanbul hard fork through two proposals: [EIP-2046](https://eips.ethereum.org/EIPS/eip-2046) and [EIP-1109](https://eips.ethereum.org/EIPS/eip-1109).

---

**cdetrio** (2019-06-19):

> BLS vs ECDSA: Add BLS12-381 opcode or precompile to EVM to verify signatures of Eth2 consensus objects.
> Keccak256 vs SHA256: Reduce gas cost of calls to SHA256 precompile (and possibly to all precompile calls) to facilitate checking Eth2 consensus Merkle paths.

These EVM improvements/optimizations are already on the eth1 roadmap. Side note, I’m not sure the current cost of calling sha256 would be a bottleneck.

> roots: Add EVM opcode to read beacon chain block roots (alternatively, an opcode to read state roots). This could be useful, for example, to prove that a given Eth1 block has been finalized without adding an ad-hoc finality opcode.

Its not clear to me what the usecase is for eth1 contracts to be aware of finality around eth1 EE shard blocks. Eth1 clients being aware of eth2 finality is useful for a finality gadget, but that’s client-level awareness rather than contract-level. I could imagine a usecase for doing cross-shard stuff in eth1-on-eth2 contracts, but I think there are better solutions that won’t require dapp devs to implement finality checking logic in their contracts.

> SSZ vs RLP: Add support for SSZ and consider deprecating RLP.
> sparse tree: Consider removing the hexary Patricia tree in favour of a sparse binary tree.

Upgrading the trie structure (and perhaps swapping out the use of RLP in the eth1 trie) is a definite high priority, and happens to be one of the most difficult items on the 1.x wishlist. Some believe it to be so difficult that doing the upgrade on 1.0 might be a challenge comparable to doing an eth2 switchover, i.e. during the eth2 switchover might be the best opportunity to perform this upgrade.

> Casper FFG: As part of an intermediate hybrid PoW/PoS step, update PoW fork choice rule to respect beacon chain finality.
> light clients: Replace PoW-based Eth1 light clients with PoS-based beacon chain light clients.

The finality gadget is already on the 1.x roadmap. A question eth2 switchover optimists could ask is whether a hybrid intermediate step can be leap-frogged by jumping straight to a switchover (I’m not an optimist yet, but in any case I don’t think this intermediate step is particularly burdensome).

Note that the finality gadget will require eth1 clients to also be eth2 light clients. I would guess that the finality gadget and eth1 bridge usecases will be the primary driver, at least initially, of eth2 light client development.

> randomness: Find a migration path for dApps that rely on the nonce header field for randomness. RANDAO only provides a decent random number every epoch, not every block as with PoW.

Aside: I wonder how the quality of randomness comparison would look if instead of valuing the randomness of PoW blocks using the nominal block reward, strategies like selfish mining are accounted for.

> Eth1 headers: Consider redefining Eth1 header fields which may no longer be relevant (e.g. ommersHash, difficulty, beneficiary, nonce, gasLimit) and make sure no significant dApps break as a result.

Avoiding breakage of dapps is the challenging constraint in general with doing eth1 changes/upgrades. Changing Eth1 header fields is particular to an eth2 switchover (I’m not aware of any 1.x proposals/directions that would significantly change header fields).

> incentivisation: Remove PoW rewards.

The hybrid PoW/PoS finality gadget only reduces PoW, it doesn’t remove them totally. Is there any option on the table for total removal of PoW from eth1, and thus a full switch to PoS, other than doing an eth2 switchover?

> difficulty bomb: Remove difficulty bomb.

This is trivial (technically).

> statelessness: Build statelessness support into Eth1 clients (Geth, Parity, etc.). Also implement logic to produce Eth2-compliant shard blocks.

Stateless eth1 clients are a prerequisite for an eth1-into-eth2 switchover, and perhaps the most important task (which blocks many other tasks). They are already on the 1.x roadmap, purely for the 1.x interest of addressing 1.0 state bloat / sync times.

Logic to produce eth2 shard blocks (maybe what we are calling EE relayers?) is a general need for eth2. A relayer specific for eth1 would have much overlap with the eth1 stateless clients that are already on the 1.x roadmap.

> new liveness invariant: Make sure that there are no significant dApps that break when moving to regular 3-second slots (as opposed to the current Poisson distribution for blocks, with a ~15sec average block time).

Aside: are 3-second slots documented anywhere? I just skimmed the eth2 specs and saw 6 seconds stated somewhere, but not 3.

> libp2p vs devp2p: Migrate Eth1 clients from devp2p to libp2p.

iiuc “use libp2p not devp2p” is an oversimplified view (e.g. some phase 0 testnet clients are planning to use devp2p for peer discovery, and maybe a gossip protocol based on libp2p??). Anyway the broader question is whether eth1 clients will migrate, or new eth1-in-eth2 clients will be written, or some combination of both (e.g. I can imagine a landscape where bridge nodes relay between Eth1-full-nodes-running-devp2p and Eth2-shard-proposers-running-libp2p). I don’t think we can answer this question; we can try to predict, but in the end we’ll just have to wait and see how it evolves.

> Eth1 gas limit: Consider removing the Eth1 gas limit to avoid having two gas limits (Eth1 gas limit under Eth2 gas limit).

Agreed, this would be a good simplification.

> Eth2 gas limit: Make sure that 8,000,000 “Eth1 EVM gas” when translated to “Eth2 WASM gas” fits within the Eth2 gas limit. Significantly reducing the effective limit below 8,000,000 gas may cause unacceptable congestion. Check that the Eth2 gas mechanism (which would not have miner voting) is otherwise acceptable for Eth1.

Agreed, benchmarking this in prototypes is a high priority task - one of the basic prototypes/experiments to run and demonstrate that an eth2 switchover is viable.

> WASMify Eth1 consensus: Formalise the Eth1 state transition function—including all precompiles—as WASM code. Split the WASM code into small chunks that fit within the Eth2 code limit (possibly 16kB per code chunk). This formalisation risks introducing consensus bugs on a $20B+ network so extensive fuzzing and formal verification may be required. We also want the WASM formalisation to be consistent with the wider WASM-for-blockchains standardisation effort.

I guess we start by designing the Eth1 EE, in parallel with detailing a minimal execution spec and the constraints it would place on EEs. Formally verifying a wasm implementation would be done after its been implemented.

Consensus bugs on Eth1 are already a risk, regardless of Eth1 upgrades, and regardless of client code changes. Of course the risk is increased in a complex change such as an eth2 switchover, but we should emphasize that robust testing is the way to safely make changes/upgrades to complex systems (or concede that complex systems are doomed to stagnation).

> premine load imbalance: Consider the negative consequences of the load asymmetry from premining the Eth1 state into a single shard with the other 1023 shards empty.

Shard imbalance is a concern regardless of an eth1-eth2 switchover, but a switchover is cause for additional concern. The other shards won’t necessarily be empty (only if the switchover happens simultaneously with launch of execution). In any case, benchmarking and prototyping is the best way to study this issue imo.

> hard forks: Negotiate a timely hard fork schedule with the existing Eth1 ecosystem.

Yes, and also negotiate timely phases and milestones in the Eth2 launch plan.

> Eth2 consensus pollution: Consider disruptions to Eth2 whenever Eth1 will need to hark fork. Indeed, the Eth1 consensus would likely have “too big to fail” status within the Eth2 ecosystem (inconsistent with the expectation that execution engines are application-layer, not consensus-layer) which imposes an Eth2 hard fork for every Eth1 hard fork.

Ideally, the switchover would be the last Eth1 hard fork. To plan for emergency bug-fixes, I see three options: (1) coordinate a bug-fix as an irregular state change (replace the eth1 EE state root and code with a fixed state root and code, at some activation block); (2) add upgrading/fixing features to the eth1 EE; (3) coordinate fixes as adoption of a newly deployed Eth1 EE (using the last known good eth1 state root).

For the first option, I’m unclear what will be possible technically. Maybe it could be possible to do an irregular state root update (and point to newly deployed code) with a coordinated majority of validators assigned to the Eth1 EE shard committee? (rather than needing all Eth2 beacon and shard validators to activate the fork). But likely not, an irregular update of an eth2 EE will probably require action on the part of all Eth2 validators. Though it should be possible to make the process smoother by adding opt-in features for eth2 clients to update wasm blobs, and so forth.

The second option raises many governance questions.

The third option has the downside that all users of Eth1 will need to update their software to reflect a change in the eth2 address of the canonical eth1 EE. But it has the upside that no action would be required from Eth2 validators.

> state growth: Make sure that the ecosystem can handle 1024 privileged copies of the Eth1 consensus. In particular, the current no-rent approach may make the maintenance costs of tracking all shards too high for services such as exchanges and Etherscan.

(aside: I’m confused about what “1024 privileged copies” means here)

State growth of Eth1 and the rent versus no-rent question is an issue on Eth1.x, regardless of an eth2 switchover (and regardless of stateless versus stateful on eth2). It will be addressed (or not) on its own, in the 1.x roadmap.

> shard number: Consider adding a shard number field in Eth1 headers to easily differentiate Eth1 execution engines running on different shards.
> yanking: Add support for contracts to move between shards and make sure that the asynchronisity introduced does not break existing Eth1 dApps.

Changes to Eth1, in combination with Eth1 EE features, to get improved integration and interoperability with Eth2 contracts/EEs will be (imo) the major area of focus around DevEx on Eth2. (If the plans for minimal execution, EEs, and an Eth1 EE switchover are demonstrated to be viable and chosen as the preferable path forward).

> Safely integrating Eth1 into Eth2 is a significant engineering and governance effort. It seems doable on a long-enough (likely multi-year) timescale. The native integration should be compared to significantly cheaper medium-term alternatives. For example, a two-way bridge between Eth1 and Eth2 can be built using light clients.

I agree that alternative approaches to integration should be explored. Of course, a simple two-way bridge with light clients is cheaper/faster than a switchover, but it would (imo) be a crappy integration with terrible DevEx, and probably also performance/communication bottlenecks that could be alleviated with a better integration. We could also try to improve on the simple bridge with something a little more costly but not as expensive/time-consuming as a full switchover, but some believe that attempting a full switchover makes more sense.

---

**holiman** (2019-09-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> Eth1 headers : Consider redefining Eth1 header fields which may no longer be relevant (e.g. ommersHash , difficulty , beneficiary , nonce , gasLimit ) and make sure no significant dApps break as a result.

Avoiding breakage of dapps is the challenging constraint in general with doing eth1 changes/upgrades. Changing Eth1 header fields is particular to an eth2 switchover (I’m not aware of any 1.x proposals/directions that would significantly change header fields).

Minor note: `ommersHash`  and `nonce` are not accessible to Dapps, only `gasLimit`, `difficulty` and  `beneficiary`/`COINBASE` are (of the ones listed).

---

**kladkogex** (2019-09-30):

The best solution is probably not to couple systems at all in any way.  As Steve Jobs used to say, the best things are those that you decided not to do.

This one is a clear example of something that does not have to be done. ETH 1.0 already runs fine.

---

**ravachol70** (2019-11-07):

What of the FV language project that was announced by the EF some months back? Shouldn’t that group be dealing with it?

If I recall correctly, there was a fancy-dancy website. The name of the language was some lady’s name but I may be reaching. Anybody know what I’m talking about? It’s not Ada; I can assure you of that. It was something cosmo and catchy.

Drat, I totally forgot it. Please advise.

