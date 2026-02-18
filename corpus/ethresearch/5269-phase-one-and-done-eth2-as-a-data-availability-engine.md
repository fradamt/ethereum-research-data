---
source: ethresearch
topic_id: 5269
title: "Phase One and Done: eth2 as a data availability engine"
author: cdetrio
date: "2019-04-07"
category: Sharding
tags: [data-availability]
url: https://ethresear.ch/t/phase-one-and-done-eth2-as-a-data-availability-engine/5269
views: 21885
likes: 13
posts_count: 14
---

# Phase One and Done: eth2 as a data availability engine

At present, the bottleneck constraining throughput on the Ethereum 1.0 chain is state growth. So if we want to scale Ethereum, the logic goes, then 1000 shards where each has independent state would enable 1000x more throughput.

But consider the direction that Eth 1.x seems to be heading. The desire for Eth1.x is to make a large cost adjustment to two resource types: storage and tx data. Currently, storage is underpriced and tx data is overpriced. This incentivizes dapp developers to write contracts that utilize storage more than tx data, which results in storage becoming the throughput bottleneck. Proposals are to increase the price of storage, and decrease the cost of tx data. After these cost adjustments, developers will be incentivized to utilize tx data, and not storage (i.e. they will be incentivized to write stateless contracts rather than stateful). Thus in the near feature (if the Eth 1.x roadmap achieves adoption), we can expect that throughput on Ethereum 1.0 will be constrained by tx data, and not storage.

If we assume that throughput is constrained by tx data, then in order to scale Ethereum, shards on Serenity do not need to be stateful. If the bottleneck is tx data executed by stateless contracts, then 1000 stateless shards would enable 1000x more throughput.

Sounds great, but it requires shards that execute, which aren’t planned until Phase 2. In the meantime, we can use Phase 1 as a [data availability engine](https://medium.com/@trenton.v/transcript-scalable-blockchains-as-data-layers-vitalik-buterin-11aa18b37e07?sk=52eba61c9f8eb4a2462e9a45bc00df81), a term that seems to be catching on. Let’s think about how this will work.

Take the example of zk-rollup, which is constrained by data availability. Could a zk-rollup contract on eth1 make effective use of eth2 as a bridged availability guarantor? Well, if execution (i.e. verify the snark proof and update the state root) happens without a simultaneous data availability guarantee, then you have the plasma-ish [zk-rollback](https://ethresear.ch/t/roll-up-roll-back-snark-side-chain-17000-tps), which gets you 17 zillion tps, but with a complexity tradeoff of needing [plasma-style operator challenges](https://www.reddit.com/r/ethereum/comments/9l2hw6/roll_up_roll_back_snark_side_chain_17000_tps/e74ox0p) and exit games. And in availability challenges, anybody can provide the data to prove availability, so its not really clear how putting the data in a bridged eth2 shard would simplify things.

Now with the other version of zk-rollup, i.e. the [500 tps zk-rollup](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477/79), everything is much simpler. Instead of needing a designated Operator, anyone can act as a Relayer at any time and generate snark proofs to update the state. The fact that a data availability guarantee always comes with every state update means that there are no plasma-style operator challenges and exit games to deal with. But it requires that execution happen in the same transaction as the data availability guarantee, and unfortunately we can’t do that with a bridged availability engine. In other words, a bridge is sufficient for a [fraud proof system](https://medium.com/starkware/validity-proofs-vs-fraud-proofs-4ef8b4d3d87a) like zk-rollback, but not a validity proof system like zk-rollup. So the important feature we need in an availability engine at Layer-1, in order to get the simplicity of validity proofs at Layer-2 is, apparently, the ability to guarantee data availability atomically with executing the state transition.

Maybe we should not be surprised at this realization. If data availability alone (with no execution) was truly useful, then there wouldn’t have been talk about Phase 1 launching only to guarantee availability of a bunch of zero-filled data blobs, and there wouldn’t have been dissatisfaction over having to wait *yet another* launch phase before eth2 can actually do something useful (besides PoS). We’re trying harder to use Phase 1 as a data availability engine, but it is still out of reach of any execution, so it feels underwhelming (Yay, we can do sovereign Mastercoin 2.0!).

So what are the reasons for resisting execution in Phase 1? Well, if we are assuming stateful execution, then everything revolves around each shard maintaining some local state. If validators are required to maintain lots of local state, then validator shuffling becomes a lot more complex. On the other hand, if we aren’t doing execution then there’s no local state to worry about. Validator shuffling becomes a lot simpler, and we can focus on constructing shard chains out of data blobs, and launch a lot sooner.

But let’s not assume execution is stateful. What if we try to do execution with a stateless, dead simple VM?

Suppose there are three new validator fields in the BeaconState: `code`, `stateRoot`, and `deployedShardId`. And there’s a function, `process_deploy` (right below [process_transfer](https://github.com/ethereum/eth2.0-specs/blob/6ca3c64526a1683aa72866d6b6f7a210cbea399f/specs/core/0_beacon-chain.md#transfers)). When code is deployed, a validator must maintain the minimum balance (so at least 1 ETH is locked up. if there is no SELFDESTRUCT in the code, then 1 ETH is effectively burned and the code is permanently deployed).

Now there are accounts with code in the global state.

Next we try to get a particular data blob included in a shard, but how? As far as I know, it is an open question how shard validators in Phase 1 will decide what data blobs to include in shard blocks. Suppose that the Phase 1 spec leaves this unspecified. Then for a user to get their data blob included in a shard, they would either have to contact a validator and pay them out-of-band (e.g. in an Eth 1.0 payment channel), or they would have to become a validator and include it themselves (when they are randomly elected as the block proposer for a shard). Both of these are bad options.

A better way is to do the obvious and specify a transaction protocol enabling a validator to pay the current block proposer a fee in exchange for including their data blob in the shard chain. But if beacon block operations such as validator transfers have [minimal capacity](https://github.com/ethereum/eth2.0-specs/blob/6ca3c64526a1683aa72866d6b6f7a210cbea399f/specs/core/0_beacon-chain.md#max-operations-per-block), then that won’t work. Without a transaction protocol enabling validators to prioritize what data blobs they’ll include, the “phase 1 as a data availability engine” use cases will be crippled (whether for contracts on eth1 using a bridge to the beacon chain, or Truebit, or Mastercoin 2.0, or any of the data availability use cases I’ve heard proposed). In any case, let’s just assume that however shard proposers are deciding what blobs to include in the “data availability engine without execution” model, we are doing the same thing in a “data availability engine with dead simple stateless execution” model.

So a particular data blob is included in a block. Limit execution to one tx per block (e.g. the whole blob must be one tx). We’re also not specifying whether the tx has to be signed by a key (if we have a transaction protocol), or if the tx is not signed (assuming no tx protocol). Let’s assume the latter, with the code implementing its own signature checking (a la account abstraction; there is a block gas limit, but no fee transfer mechanism so no gas price and no GASPAY opcode). If the blob can be successfully decoded as a tx, then execute the destination account code with the data and current state root as input. If execution returns success, then the return data is the new state root.

How do we update the validator account `stateRoot`? We can’t update it in the BeaconState on every shard block (again, because of the strict limits on the number of beacon chain operations). But shard fields in the beacon state *are* updated on crosslinks. Take the list of updated state roots for accounts on the same shard, and suppose they are hashed into a `shard_state_root`. Seems not that different from the `crosslink_data_root` (both are hashes dependent on the content in previous shard blocks) that is in Phase 1 already.

Admittedly, because all shard state roots are not updated every beacon block, there is some local state. But if accounts are global, then the state root data will be minimal. It seems not that different from the some number N of recent shard blocks that need to be transferred between validators during shuffling anyway.

Enough details have been glossed over. The point I’m trying to make is that the requirements for stateless execution seem to be mostly already satisfied in Phase 1. The biggest issue imo is the unspecified way that users will get their blobs included into the chain (which again, if not solved this issue may prevent Phase 1 from being usable even as a bridged availability engine). Or maybe its just the first issue, and I’m overlooking other big ones. What am I missing? What would be the most difficult part of bolting this onto Phase 1 (or Phase 1.1, if you prefer)?

The big reason for the simplicity of this execution model compared to Phase 2 proposals seems to be that contract accounts are global, like validator accounts. This means the number of contract accounts must be limited and so it will be expensive to deploy code in the same way it is expensive to become a validator (though hopefully not quite as expensive ;). But if we get to introduce execution into Eth2 much sooner, isn’t this an acceptable tradeoff? Deployed code is equivalent to immutable contract storage, so another way to state what we’re trying to do is to offer execution in Phase 1 without trying to scale contract storage. We still scale the important use case: massive throughput of data availability (1000x the transaction throughput).

Even with basic stateless execution, users can do cross-shard contract calls by passing proofs of state about one contract as the tx data to another contract. Contracts could also implement their own receipt-like functionality (a receipt in a contract’s state root is just as verifiable as a receipt field in a block header). The developer experience is not great because there is no assistance from the protocol. But the Phase 2 proposals being circulated also seem to be lacking real features to facilitate cross-shard contract interaction (the messy stuff is left to the dapp developer, who must implement logic for getting receipts from different shards, making sure receipts are not double-spent, and so forth). So when it comes to developer experience, basic Phase 1 stateless execution does not sound much worse than the “simple” Phase 2 ideas. Basic stateless execution would also be sufficient to enable two-way pegs between BETH on the beacon chain and ETH on the main chain.

The main difference compared to Phase 2 proposals is that they aim to scale contract storage. But storage, and hence stateful execution, also seems to be the source of most complexity making it difficult to imagine including execution in Phase 1.

## Replies

**ldct** (2019-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> So the important feature we need […] is the ability to guarantee data availability atomically with executing the state transition.

It seems to me that this can be done at the application layer, e.g., the rollup smart contract can maintain a list of verified state roots, which it keeps extending, but does not consider any of them finalized for withdrawal purposes until a receipt from the bridge is included. Users will need to wait for the cross-chain receipt inclusion time (presumably longer than the finalization time for either chain).

---

**cdetrio** (2019-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> cdetrio:
>
>
> So the important feature we need […] is the ability to guarantee data availability atomically with executing the state transition.

It seems to me that this can be done at the application layer, e.g., the rollup smart contract can maintain a list of verified state roots, which it keeps extending, but does not consider any of them finalized for withdrawal purposes until a receipt from the bridge is included. Users will need to wait for the cross-chain receipt inclusion time (presumably longer than the finalization time for either chain).

Okay, but if done like that, can the state roots be extended by a Relayer? No, because the contract can’t check (atomically, in the same transaction) if the state root is valid or fraudulent. So only a designated operator can extend the state roots, and you need the complexities of fraud proofs and operator elections.

---

**ldct** (2019-04-07):

I see; so the claim is that designs where the set of parties allowed to commit offchain state transitions is not fixed are impossible with only an asynchronous bridge to a data availability chain, but eg a design where that set is a single operator is not disallowed

---

**cdetrio** (2019-04-07):

The main claim is that adding execution to Phase 1 might be surprisingly easy (much easier than the usual conception of Phase 2) if we focus just on adding execution, and not on scaling contract storage (which is an additional goal also tackled in Phase 2).

The rollup versus rollback issue is just one example to motivate that Phase 1 is only truly useful as a data availability engine if it also does execution. And that a bridged Phase 1 (i.e. eth1.0 using a light client bridge to the beacon chain when phase 1 only confirms data blobs but doesn’t do any execution and doesn’t have a transaction protocol), is not very useful. (I don’t think this is a contentious claim given that the roadmap has planned for Phase 1 to have data blobs filled with zero bytes).

---

**ldct** (2019-04-07):

> Phase 1 is only truly useful as a data availability engine if it also does execution

But “rollup with a single operator” is a pretty useful thing…

---

**cdetrio** (2019-04-07):

And you can do that right now on Eth1.0. The way a bridge to beacon chain shard blobs would help is that it would make it easier for the operator to submit proofs of data availability when challenged, e.g. in the protocol you suggest, “Users will need to wait for the cross-chain receipt inclusion time” proofs are batched and submitted continually, rather than waiting for a challenger. But this will only be usable if operators can reliably get their data included in the shard blobs proposed by validators, and that will require some kind of transaction protocol for paying fees to validators. If there’s a transaction protocol (or some out-of-band system) for validators to earn fees for including user data in shard blobs, then we are most of the way (I claim) to having everything we need for doing execution in Phase 1 (and your zk-rollback on eth1-bridged-to-eth2 can be done more simply as zk-rollup on eth2).

If you don’t think we should bother adding execution to eth2 because its sufficient to do all execution on eth1 with a bridge to eth2, then hey I’m fine with that. Other people are anxious to add execution to eth2 asap and want to rush Phase 2. I’m suggesting that if we want to deliver contracts on shards with rushed barebones DevEx, we can do that in Phase 1 (if we only scale tx throughput, and not contract storage).

---

**vbuterin** (2019-04-24):

So I actually have surprisingly enough been thinking in a somewhat similar direction. The details are likely different in some ways, but the key idea of a minimal execution engine that relies on contracts in global state as the main thing that transactions go through is there. I have a partially completed writeup, will get it done over the next couple of days.

---

**ryanreich** (2019-05-01):

I like the idea of data availability as a goal for a blockchain — you describe an application to stateless execution, but you can actually build a much more elaborate smart contract system on top of an execution model with no global state, as long as you are careful about how calls to stateful contracts are made.  Specifically, they need to be made up-front, like spending a UTXO, so that it is clear what state belongs to what execution thread (and so, to what shard).

I did a lot of work exploring this; [here](https://sites.google.com/consensys.net/fae/learn/architecture) is a document describing the resulting architecture of the smart contract system.  It sounds like it may fit as a “data availability subsystem” within Ethereum according to your arguments.  It is certainly geared towards providing a very high degree of sharding, and (I think) presents few difficulties for potential future evolution of the consensus mechanism around it.  I’d be interested in your reactions.

---

**cdetrio** (2019-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So I actually have surprisingly enough been thinking in a somewhat similar direction. The details are likely different in some ways, but the key idea of a minimal execution engine that relies on contracts in global state as the main thing that transactions go through is there. I have a partially completed writeup, will get it done over the next couple of days.

Great, and thanks for this mention btw (and to assist any archivists/indexers, the writeup is [over here](https://ethresear.ch/t/a-layer-1-minimizing-phase-2-state-execution-proposal/5397)).

---

**cdetrio** (2019-05-09):

I’m late on the follow-up but I do want to close off one line of the argument above, and concede on the usefulness of a data availability bridge without “general execution” per se. The question of how users get their blobs into a Phase 1 shard chain came up during the Eth2 workshop in Sydney a few weeks ago (it was asked by [@djrtwo](/u/djrtwo) and answered by [@vbuterin](/u/vbuterin)). The solution is clever and simple (perhaps even obvious), which is for a contract on eth1 to pay the phase 1 block proposer who includes the data, at the time when data availability is confirmed through the bridge. This also provides an atomic availability guarantee, enabling zk-rollup proper (rather than rollup-rollback) meaning the phase 1 block proposer is a rollup Relayer (rather than a rollback Operator). This wasn’t clear to me initially, but now I do understand how a zk-rollup contract on Eth1 and rollup relayers could make use of a bridge to Eth2 phase 1.

The next issue that comes up about the usefulness of an availability bridge to a phase 1 without execution is what hash function will be used for the phase 1 blocks. If the hash function is standardized to say sha256, then that means the zk-rollup contract on Eth1 is required to use sha256 in its snark circuit. This is undesirable because sha256 is not well suited for snark circuits, so the snark proof generation time (i.e. the proof generation done by the rollup relayers) is a lot longer than if a more suitable hash function, such as Pedersen hashes, were used. This issue could be resolved if phase 1 data blobs have some kind of [multihashing feature](https://ethresear.ch/t/multihashing-in-ethereum-2-0/4745), which works by having other hashing functions available as “precompiles”. If block proposers somehow specify which precompile function to use when hashing the block, then this is arguably a very limited kind of execution feature, but it is obviously not general execution. (A pedantic aside: I’m unsure whether the usefulness of multihashing for Phase 1 data blobs and a data availability bridge to Eth1 was widely realized until it came up at the Sydney workshop. Its not explicitly mentioned in the [multihashing thread](https://ethresear.ch/t/multihashing-in-ethereum-2-0/4745), but it is here now, at least).

Both solutions (paying fees to phase 1 block proposers using contracts on eth1, and a multihashing feature for phase 1 data blobs) combined would make a phase 1 data availability bridge very useful for zk-rollup contracts on Eth1. Of course general execution in phase 1 would be even more useful, but it would also be more complex (though not too much more complex, I’d still argue).

I also wonder what the scalability limits would be of a phase 1 bridge. Could it be possible for all the availability bandwidth of eth2 shards to be consumed through the bridge by zk-rollup contracts on eth1? It depends on the estimate of Eth1 throughput (both bandwidth and computational capacity), which I think has been under-estimated and would be significantly boosted by Eth1.x upgrades.

---

**cdetrio** (2019-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/ryanreich/48/3479_2.png) ryanreich:

> I did a lot of work exploring this; here is a document describing the resulting architecture of the smart contract system.  It sounds like it may fit as a “data availability subsystem” within Ethereum according to your arguments.  It is certainly geared towards providing a very high degree of sharding, and (I think) presents few difficulties for potential future evolution of the consensus mechanism around it.  I’d be interested in your reactions.

Thanks for sharing this here, very interesting stuff. There is a lot to chew on in the Fae docs, but one aspect in particular is relevant and I want to expand on it. Incidentally, thinking about this aspect was what first led me to “Phase One and Done”, but I wasn’t sure how to articulate it (I’m still not, as you’ll see, but please forgive me for rambling anyway). The data availability bridge was a second line of thought that I ended up writing down instead, but maybe this first take was the better one, lol.

Starting with excerpts of the relevant aspect from [faeth-doc](https://sites.google.com/consensys.net/fae/learn/faeth-doc):

> We will call an Ethereum transaction having an embedded Fae transaction of this form a “Faeth transaction”. Note that since the input is entirely occupied by data that is nonsensical to Ethereum

This is analogous to the data in shard blocks being nonsensical to Phase 1 validators; all data blobs are equivalent junk data and may as well be zero bytes as far as Phase 1 is concerned.

> This allows Fae to quickly scan Ethereum transactions to find valid Faeth transactions.

“Quickly”, but it has to backward-scan the Ethereum chain back to the Faeth genesis block, in order to find all the Feath transactions, right? That would be a lot of data to download and process, so sounds like this would make Faeth light clients impossible.

> Although everyone must process the Faeth transaction as an Ethereum transaction, this entails little work because the EVM is not run. The actual work, the Fae transaction, is only executed by Ethereum participants who happen to be “invested” in Fae and who care about the results of the transaction.

Again, analogous to a conception of the job of Phase 1 block proposers being to include data blobs but not execute them. Only Phase 2 executors do the actual work of executing transactions.

> Note that Bitcoin itself does not allow a Faeth analogue because its transaction messages do not contain any uninterpreted fields in which to embed a Fae transaction.

Somewhat tangential, but isn’t OP_RETURN a field that meta-protocols on bitcoin can use to embed their meta-transactions ([throwback Mastercoin thread for reference](https://bitcointalk.org/index.php?topic=265488.940))?

All of this relates to a distinction between two approaches to execution, which was emphasized when the Phase 1 vs Phase 2 architecture was first proposed. At root is the fundamental difference between a “data availability consensus game” that is the ordering of blocks (which has a non-deterministic outcome), versus an “interactive verification game” that is the execution of transactions (which has a deterministic outcome, given an ordering). One approach is to couple execution with consensus (as in Ethereum 1.0). The other approach is to separate execution from consensus (as in Ethereum 2.0, Phase 1 vs Phase 2).

The approach of separating execution and consensus is mentioned in the Ethereum 1.0 whitepaper, as a “Metacoin” protocol. The meta-protocol works by attaching data to bitcoin transactions and then using a separate client to execute the data according to the custom transaction protocol (see the Metacoins section in the [white paper](https://web.archive.org/web/20190403172018/https://github.com/ethereum/wiki/wiki/White-Paper)). The primary downside, as argued in the whitepaper, is that it makes light clients impossible (“Hence, a fully secure SPV meta-protocol implementation would need to backward scan all the way to the beginning of the Bitcoin blockchain to determine whether or not certain transactions are valid.”) If it was just light clients as a user experience thing then it would not be so problematic; there are UX workarounds. The real downside to lack of true light clients (not explained in the white paper, but I’ll argue it here) is that it becomes difficult to imagine how a cross-chain protocol would work; the usual way to do cross-chain stuff is to imagine a contract on one chain being a light client of another chain (and if two contracts on two different chains can be light clients of each other, then trustless cross-chain atomic swaps become possible). This, among other reasons, motivated building Ethereum as its own chain (with execution coupled to consensus) rather than as a meta-protocol that piggybacks on data attached to bitcoin tx’s.

When the Phase 1, Phase 2 architecture was proposed, I liked it and agreed that decoupling Phase 2 from Phase 1 is a clean design (decoupled meaning Phase 2 Executors are a separate role from shard data blob proposers/validators). I also liked the decoupled design because my preferred conception of Phase 2 was also delayed execution (rather than “immediate execution” or whatever you want to call the conventional way as it works in Ethereum 1.0), mainly because under delayed execution it becomes much easier to imagine how [synchronous cross-shard transactions](https://ethresear.ch/t/synchronous-cross-shard-transactions-with-consolidated-concurrency-control-and-consensus-or-how-i-rediscovered-chain-fibers/2318) would work. (I guess Faeth’s “lazy evaluation” sounds similar to delayed execution). Also relevant is something [@benjaminion](/u/benjaminion) suggested at the Eth2 workshop back in November 2018 (before Devcon4), which stuck in my mind, “how about having multiple execution engines?”. If Phase 2 is actually decoupled from Phase 1, then indeed it does seem possible to have multiple execution engines, with Phase 2 execution engines being opt-in choices that Validators and/or Executors may or may not choose to run.

I suppose you can see where I’m going here. If Phase 2 is decoupled from Phase 1, wouldn’t that mean Phase 2 execution is ultimately a meta-protocol on Phase 1 data blobs? If so, then maybe there are ways to overcome the limitations of meta-protocols pointed out in the Ethereum 1.0 white paper, and it is an advantageous approach nonetheless. (I’ve been unable to do better than just wonder out loud as I’m doing here, and would be very interested if someone else articulates what I’m trying to get at. To be fully honest I’m a bit sheepish for not going full circle from the Ethereum 2.0 architecture back to the 1.0 white paper and asking this question much earlier; at least I can’t remember anyone else asking it explicitly).

On the other hand, if execution is not decoupled from Phase 1, meaning that shard block proposers are not indifferent to the data blobs but do interpret the data contained in shard blocks, then the Phase 2 vs Phase 1 description of the architecture is misleading and we should just call it execution in Phase 1 (or “Phase One and Done” which I hope catches on hehe). I guess “Phase One and Done” versus “Phase 2 decoupled from Phase 1” are two distinct approaches, roughly outlined, to execution on Eth2.

---

**vbuterin** (2019-05-10):

The challenge with making everything be zk rollups is that as far as I can tell there’s a lot of demand for an execution environment that’s highly similar to what people have in eth1, and actually coming up with efficient SNARK circuits/provers for that (especially the general-purpose EVM bits) may prove to be very difficult, and lead to extra multi-year-long delays before ultra-scalable smart contract execution is possible.

One other thing I wanted to highlight is that there are intermediate gradations of phase-2-ness potentially worth exploring here. There’s already computation happening if [@cdetrio](/u/cdetrio)’s proposal gets implemented because we need to Merkle-hash the blobs in a SN/TARK-friendly way. But we could potentially extend this further, and allow block proposers to specify *reduction functions* `f(data) -> Bytes32` that get executed as pure functions on data. Mathematically speaking, a hash function is just a type of reduction function, so we get the same level of abstraction, except now the reduction functions can verify signatures etc etc, without a lot of the complexity of full phase 2 because there is not yet persistent state (reduction functions are pure).

We could add beacon-chain-only state, by storing a 32-byte state field for every execution environment, and running `exec_env.state = reduce(exec_env.state, data)`. The entire set of state changes in a crosslink would be small enough that it could simply be included as part of crosslink data, so the crosslink data would just specify all changes to execution environment state. Now, we have a little more state, but we have enough abstraction that we could make fairly complex execution environments inside of shards, and we don’t have any of the complexity that comes with layer-1 state in shards (so we still have the ability to eg. remove the crosslink/persistent committee distinction).

And if we go a bit further, and allow oracle access into shard state, then we basically have the proposal that I made.

---

**ryanreich** (2019-05-13):

This has taken a while to write because of its length; sorry.

> “Quickly”, but it has to backward-scan the Ethereum chain back to the Faeth genesis block, in order to find all the Feath transactions, right? That would be a lot of data to download and process, so sounds like this would make Faeth light clients impossible.

Yes, I am using that word to refer to the speed of a Faeth client handling an individual Ethereum transaction: it should be obvious without reading much data whether there is an embedded Fae transaction in the data.  It definitely does require scanning the whole chain.

Now, this is not in itself a problem, because Ethereum 1.0 also requires processing the whole chain.  A blockchain client is supposed by default to be a full client, and light client protocols are add-ons that achieve shortcuts through extra information added to the blocks.  Ethereum currently uses state root hashes (and I don’t think sharding is going to really change that), which are computed by full nodes and then trusted by light clients to download a state blob.

Fae can do this too!  I have a feature where contract call return values can be “versioned”, i.e. associated with a content-based hash, which is like a localized state root describing the state on which that return value depends, and nothing else.  This is, I think, just a more granular version of how shards work, because Fae’s sharding is more granular than Ethereum 2’s.  A light client can receive a data blob to stand in for the computed return value; in fact, it requires quite a bit less information than the Ethereum state blobs, because it describes only one return value, and not any actual state.

This, by the way, exposes where validation is important in smart contracts: not in verifying correct computations, but in synchronizing the essentially redundant datum of a state hash with the actual computed state.  A light client operating as described above will be vulnerable to a swindle where some transaction *intentionally* reports an incorrect version, say by supplying the version of a return value that represents money that doesn’t actually exist; the light client will blindly accept the fraudulent return value and perhaps act in response to the appearance of having been paid, when on the actual chain, they weren’t.  Validation exists to protect them from this.  It is not actually useful for full clients, who are by definition validators themselves.

> Somewhat tangential, but isn’t OP_RETURN a field that meta-protocols on bitcoin can use to embed their meta-transactions (throwback Mastercoin thread for reference )?

Hmm, I didn’t know about that.  I dug a bit into the bitcoin block structure to see if there were any uninterpreted fields and didn’t find any, but I figured that the script field *had* to be meaningful because it was executed.  It seems someone thought of this exact use case.  Faeth could work with OP_RETURN by passing the hash of the Fae transaction to it as an argument, and then distribute the transaction message itself separately.  This does diminish one nice feature of Faeth (from my perspective), that it lets Ethereum serve as the actual distribution channel for Fae transactions.  But with the cryptographic security of a good hash, a regular p2p channel could work for that anyway.

> I guess Faeth’s “lazy evaluation” sounds similar to delayed execution

I think so.  Lazy execution is run-on-demand, rather than strictly sequentially.

> The primary downside, as argued in the whitepaper, is that it makes light clients impossible (“Hence, a fully secure SPV meta-protocol implementation would need to backward scan all the way to the beginning of the Bitcoin blockchain to determine whether or not certain transactions are valid.”)

The problem isn’t exactly transaction validity — a concern that I think is a little exaggerated — but rather history-truncation validity: the matching of state hashes with state blobs I discussed above.  Without a validator intervening in the block formation, or some other assurance that the state hash is correct, the light client has no protection against the swindle I described.  The base protocol would of course not have validation of a meta-protocol as part of its consensus process.

Actually invalid transactions are not a problem in this way: anyone at all can syntactically verify them, and anyone with the correct initial state can verify correct execution, but the problem of getting that correct initial state is more fundamental.

I don’t feel like going all the way to “you can’t get light clients without integrated execution and consensus” is necessary, though.  It’s true that a given light client can’t necessarily trust an *arbitrary* state hash that appears in the meta-protocol; however, if the operator of the light client is expecting, say, a payment, then they can set up a personal verifier pool themselves through smart contract logic.  Say, offer a bunch of friends (or professional verifiers with no interest in any particular activity — exactly the kind of apathetic profile that leads to trustlessness) some of the money they are expecting.  Roll your own economic incentives, basically.

I may be an idealist in this matter, but I feel that it is better to have a clean, minimal design with maximal functionality that can, later, be secured for more specialized applications by using some of that functionality, than to prematurely optimize for an imagined application and in so doing, make the general case so much harder.

