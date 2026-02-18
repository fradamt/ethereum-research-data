---
source: ethresearch
topic_id: 7248
title: Eth1+eth2 client relationship
author: djrtwo
date: "2020-04-07"
category: The Merge
tags: []
url: https://ethresear.ch/t/eth1-eth2-client-relationship/7248
views: 21413
likes: 16
posts_count: 20
---

# Eth1+eth2 client relationship

# eth1+eth2 client relationship

Since Vitalik proposed an [Alternative proposal for early eth1 ↔ eth2 merge](https://ethresear.ch/t/alternative-proposal-for-early-eth1-eth2-merge/6666) in Dec 2019, there has been an active conversation about what this merger might look like from a software perspective and an eagerness to begin prototyping. The vision is a hybrid in which core consensus work is managed by an ***eth2-client*** and state/block-production is managed by an ***eth1-engine*** – together forming an eth1+eth2 client.

This document aims to make more explicit the separation of duties between an eth2-client and an adjunct eth1-engine to give better foundation to the conversation, spec writing, and prototyping. This document does *not* aim to define specific details of the protocol (e.g. precise methods eth1 client calls to eth2 engine), and any examples contained within are only that – examples to aid description and subsequent discussion.

This document assumes basic familiarity with eth2 and stateless Ethereum.

## High level separation of concerns

The aim in an eth1+eth2 merger is to leverage the existing eth1 state, ecosystem, and software in the upgraded eth2 consensus context.

Broadly, what we think of today as an ***eth2-client*** handles core PoS and sharded consensus. Essentially, the eth2 protocol and eth2 clients have been designed to be really good at producing and coming to consensus on a bunch of “stuff”. That stuff is a number of shard chains full of data and (eventually) state. The eth2 “consensus layer” is much more sophisticated and much more complex than the PoW consensus layer found in Ethereum today.

Eth1 clients today have a relatively simple and thin consensus layer – there is only one chain and PoW handles most of the complexity in sophisticated extra-protocol hardware. Most of the sophistication and optimizations of eth1 clients lie in the user layer – state storage/management, state sync, virtual machine execution, transaction processing, transaction pools, etc.

This separation of concerns makes for a great pairing when eth1 is integrated as a shard on eth2 – the eth2-client can handle the complexities of PoS and sharded consensus, while the adjunct eth1-client becomes an ***eth1-engine*** and can handle the complexities of state, transactions, VM, and everything closer to the user layer.

### Minimal changes, local communications

There are many potential paths to how eth1 and eth2 client software can be woven together (full merge, import eth1 as library, communication protocol between the two), but in this document we focus on what we consider to be the most minimally invasive and most modular approach – *a local communication protocol between an eth2-client and a stripped down eth1-engine*.

Given the diversity in implementation of both eth1 and eth2 clients, this approach prevents client software lockin on either side, allows for client teams to remain independent and focus on their own stack, and keeps the software projects largely stable to allow for rapid prototyping.

### What does it look like

Broadly, an eth1+eth2 client looks like the following:

[![](https://ethresear.ch/uploads/default/original/2X/8/84ec638ff8a3ef6367cadd1ac0d231b8a7a8eb46.png)435×462 7.32 KB](https://ethresear.ch/uploads/default/84ec638ff8a3ef6367cadd1ac0d231b8a7a8eb46)

The eth2-client and eth1-engine are run together, locally communicating over RPC driven by the eth2-client.

Each maintains it’s own p2p interface, connecting to peers and handling a networking protocol related to each particular domain.

#### eth2-client

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9ac774797d644c1c7d47fd6707470b609f62f8ce_2_690x354.png)1752×900 27.2 KB](https://ethresear.ch/uploads/default/9ac774797d644c1c7d47fd6707470b609f62f8ce)

- Beacon Chain and Beacon State

Core consensus objects upon which the rest of the system is built

Shard Chains

- eth1 shard-chain
- Many data only shard-chains

Operation Mempool *[not pictured]*

- Attestations, deposits, exits, etc

P2P Interface

- Consensus level messages
- Includes eth1 shard-block gossip

RPC to eth1-engine

- All calls are driven by the eth2-client

#### eth1-engine

[![](https://ethresear.ch/uploads/default/optimized/2X/4/478a1d2100be71cafc069014557d6fe070d8e25f_2_690x353.png)1752×897 56.3 KB](https://ethresear.ch/uploads/default/478a1d2100be71cafc069014557d6fe070d8e25f)

- EVM

Execution and validation of eth1 shard-blocks

eth1 State

- The user-level eth1 state as in Ethereum today

TX Mempool

- User-level transaction mempool, ready for block production

P2P Interface

- Transaction gossip as on Ethereum today
- State sync
- No eth1 shard-block gossip

RPC from eth2-client

- All calls are driven by the eth2-client

## Consensus

From the perspective of the core consensus, the eth2-client is in charge and drives the building of the beacon chain, the data shard-chains, and the eth1 shard-chain. Any knowledge that the eth1-engine gains about the eth1 shard-chain and the core consensus (beacon chain/state) is provided directly by the eth2-client via RPC.

Specifically, an adjunct eth1-engine *must* have access to an eth2-client as it does not maintain its own consensus. In PoW in Ethereum today, an eth1-client checks the proof-of-work, forms a block tree, and runs the fork choice rule to find the tip of the chain. In eth2, these mechanics are much different and require deep familiarity of eth2’s core consensus – thus it is entirely offloaded to the eth2-client. The eth2-client provides the up to date information about the head of the eth1 shard-chain so that the eth1-engine can maintain an accurate view of the eth1 state.

Because the eth1-engine is entirely reliant upon the eth2-client driving the consensus, we suggest that the communications between an eth2-client and an eth1-engine are all methods on the eth1-engine called by the eth2-client (e.g. `addBlock`, `getBlockProposal`, etc). This enforces a leader/follower relationship to reduce the complexity in reasoning about the system and to limit the business logic required in the eth1-engine.

From the perspective of the eth2-client and core consensus, the eth1 shard-chain is handled almost exactly the same as all of the other shard-chains (fork choice, crosslinks, block structure, signatures, etc). The primary difference is that the shard block contents can be executed against the eth1-engine and thus the eth1 shard-block data must be well-formed with respect to eth1 and has additional validation against this successful execution.

## State

eth2 has a state related to the core consensus. This is called the “beacon-state”. The beacon-state is thin (~10-40MB depending on the size of the validator set) and contains all of the information needed to understand the core consensus and how to process the shard chains. In fact, to process the consensus related portions of a shard-chain, a client *must* have access to the beacon-state (e.g. recent crosslinks to run the shard-chain fork choice, current validator-set/shuffling to validate shard-chain signatures).

eth2’s state does not reach all the way into user level state. The most it makes claims about is the availability of shard-chain data. Within this shard-chain data lies the actual user level state root, and in the case of the eth1 shard-chain, the current Ethereum user state root.

The following discuss the different levels of eth1 state in relation to an eth2-client:

### eth2-client without eth1-engine

The core eth2 protocol *can* be run without an adjunct eth1-engine. An eth2-client alone can follow the beacon chain and follow the shard-chains (including the eth1 shard-chain). Without an eth1-engine, the client cannot execute the stateless eth1 shard-blocks and so cannot fully validate them or get any useful user-level info out of them. Still, the head of the eth1 shard-chain can safely be found according to the assumptions made about the eth2 core consensus and validators.

### eth2-client with stateless eth1-engine

To run a validator, an eth2-client must be run with an adjunct eth1-engine. This can be done in a stateless manner (not storing entire eth1 state locally) because eth1 shard-blocks have witnesses available for execution. Beacon committees can check the availability of shard-block data and the validity of that data with respect to eth1 via a stateless call to the eth1-engine checking the validity of the format and execution of the block.

Other than validators, many user/application nodes might also run with a stateless or semi-stateful eth1-engine. Using the thin eth2-client to follow the head of the eth1 shard-chain and interact with it in a stateless or semi-stateless manner.

### eth2-client with stateful eth1-engine

To run a validator that can produce eth1 shard-blocks, the eth2 protocol must be run with the adjunct eth1-engine along with the full eth1 state (there are stateless block production methods being explored, but for simplicity, we leave that out of this initial discussion). The local state and tx mempool can then be used to form new, valid blocks on demand (discussed more below).

Other than validators, many user/application nodes might also run with a fully stateful eth1-engine – e.g. block explorers, archive nodes, state providers, etc.

## Networking

For simplicity, eth2 and eth1 initially maintain their independent networking stacks and protocols. Some existing eth1 protocols are deprecated in favor of the eth2 protocol in response to a shift in responsibility (e.g. eth1 shard-block gossip). A migration of eth1 protocols to libp2p might be favored after the initial prototyping phase, or further down the line, to unify the networking stack, but it is not a requirement.

eth2-client and eth1-engine have access to the same discv5 DHT, but independently find peers of appropriate capabilities and independently maintain connections.

### ENR

An eth1+eth2 client utilizes a single ENR because the node sits behind one logical network identity with multiple capabilities.

eth1 capability (state, transactions, etc) is signified with the existing `eth` (or maybe new `eth1`) key in the ENR.

eth2 capability (core consensus) is signified with the `eth2` key in the ENR.

The existence of each signifies the node’s ability and willingness to speak the class of underlying network protocols.

### Wire protocols

#### eth2 protocols

- eth2 req/resp

Status
- Beacon block sync
- Shard block sync

Core consensus gossip

- Beacon blocks
- Attestations
- Shard blocks (including eth1 shard)
- Other validator operations

#### eth1 protocols

- Subset of eth1 wire protocol

Transaction gossip
- Sync methods (getnodedata or new methods)
- Get receipts

*NOT*

- messages related to block hashes, headers, or bodies

#### Why eth2-client handle eth1 block gossip?

eth2 is designed to generically handle the production, gossip, and validation of shard-blocks. We aim to make the eth1 shard as standard and comformant to the rest of the shards as possible. With respect to the core consensus, the main difference eth1 blocks have compared to the rest of the shards is the ability to execute/validate the contents of the block against the eth1 engine.

When a validator is working to crosslink an eth1 shard-block into the beacon-chain, the eth2-client would make an additional call the eth1-engine to execute and validate the block.

When a stateful eth1+eth2 node receives a new eth1 shard-block, the eth2-client would make an additional call to the eth1-engine to validate the block and update the local state storage.

## Transaction gossip and mempool

The eth1-engine maintains user transaction gossip and the eth1 transaction mempool in almost the exact same way as in Ethereum today. The same network protocols and local mechanics can be used to gossip and maintain the pool, ready for block production.

The primary difference is how knowledge of spent transactions is ascertained and how the pool is utilized for block production, but these are arguably in a layer right outside of the pool.

eth1 shard-blocks are provided to the eth1-engine from the adjunct eth2-client. Transactions included in such blocks should be cleaned from the mempool in a similar way to Ethereum mainnet PoW blocks today.

eth1 shard-blocks are produced on demand from the adjunct eth2-client via the contents of the mempool. This RPC method and the underlying functionality is similar to `getWork` but would return the full block contents rather than just a hash.

## Block production

Within the eth2 protocol, all blocks (beacon, shard, eth1-shard) must be produced and signed by a PoS validator from the core consensus. To this end, the eth2-client is ultimately responsible for *all* block production.

For beacon blocks and non-eth1 shard-blocks, the eth2-client has everything it needs to produce valid blocks.

For the eth1 shard-blocks, the eth2-client does not have immediate/ready access to eth1 state, transactions, and other underlying eth1 structures to produce a valid block. Instead, when a validator is assigned to produce an eth1 block, the eth2 client requests a viable eth1 block data (TXs, state root, etc) from the eth1-engine. The eth2-client then bundles this eth1 block data into a full shard-block (adds slot, proposer_index, proposer_signature, etc) and broadcasts the block to the network.

The eth1-engine is able to produce valid/viable eth1 block data because it manages the eth1 transaction mempool in the same way that it does on Ethereum mainnet today, and it maintains up-to-date info on the head eth1 state via updates from the eth2-client.

## Next steps

If this general design is agreed upon, the next steps include

- Ensure assumptions about eth2-client driving eth1-engine are in harmony with and do not place unexpected burden on existing eth1 software.
- Define more explicitly the communication protocol for driving the eth1-engine – e.g. new_head(block), validate_block_transition(block), get_proposal(parent_root), etc
- Define networking components – e.g. which subset of eth1 protocol is needed, how specifically will ENRs work for discovery
- Extend Phase 1 eth2 spec to add in eth1-capable flag to validators for eth1 block production. (A Phase 1 eth2 client can be used to start and just assume all validators are eth1-capable)
- Prototype!

---

Any and all input and feedback is appreciated both here and in the [Eth R&D eth1+eth2 merge channel](https://discord.gg/YXFxybB).

## Replies

**mkalinin** (2020-04-08):

This is a very good starting point! Thanks Danny!

> This enforces a leader/follower relationship

This is exactly how it looks like in my mental model (the eth2 is leader, the eth1 is follower). The thing that I am worried about is user and developer experience after the merge. They used to work with eth1 client only and after the merge will have to maintain eth2 client and probably something else alongside. It could be mitigated by some tooling that does all the dirty work around setting up and maintaining a bunch of software required to run in upgraded Eth1. But it would be an additional burden anyway.

What are you thoughts about how far we can go stripping down Eth1 chain and client? I see the following things constraining this:

- EVM
- existing applications
- existing client implementations (like you’ve mentioned)
- existing network infrastructure unrelated to the ledger, like Swarm, Whisper (probably unaffected)
- etc.

I am currently leaning toward preserving everything on Eth1 except bits of data related to the consensus.

> An eth1+eth2 client utilizes a single ENR because the node sits behind one logical network identity with multiple capabilities.

A quick look towards this direction makes me think of a separated discovery service as the only way to share it between the parts of the client. Which puts additional complexity, of course.

---

**ralexstokes** (2020-04-08):

Yep, this is a great starting point! The main details we don’t have here are the mechanics of stateless execution (and the protocol generally) and specifics on networking. There is an entire r&d effort working on the first part and I’d imagine anyone working to prototype the above design will quickly figure out the second part ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) So in general, this seems like a really promising direction forward as it unlocks most (all?) of the benefits of eth2 for eth1 as soon as we can line up all the moving pieces.

In particular, this “leader/follower” architecture is nice in that it is minimally invasive with respect to needing to change up client software compared to other options we may imagine. The overall design also plays nicely with effectively prototyping an “execution environment” in eth2 with a software stack that is relatively well understood. This paves the way for better understanding of any tradeoffs inherent in phase 2 if/when we decide to introduce EEs to eth2.

As was touched on above, the obvious uncertainty here is the resource requirement needed to run all of the software here. The eth2 consensus ensures that “bad” eth1 shard blocks will not be accepted into the beacon chain; however, there is centralization risk if only a few players can afford to run what will effectively be two full blockchain nodes. I’m looking forward to seeing prototypes here so we can start to get some numbers. I’d also think it would be helpful to talk to as many different kinds of node operators as possible to get a sense of what they find acceptable (so if you are reading this, reach out, e.g. in the discord channel linked above!).  The “shades of statefulness” Danny outlines above goes a long way towards mitigating concerns around who can participate in eth1-on-eth2 which just underscores how important the “stateless ethereum” R&D is to this early merge.

---

**djrtwo** (2020-04-08):

Yes, the elephant in the room is certainly dev tooling around this. One idea is to expose almost the same dev RPC interface as before and have the interface *smartly* figure out which portions of the system to ask for what.  Need an eth1 block at height N? (route the request to the eth2-client). Need an account balance? (route the request to the existing api on the eth1-engine).

If we can largely maintain the same APIs against this eth1+eth2 client, deprecate some that no longer are valid (e.g. getting the difficulty), and add some new (e.g. asking about validator balances), I think we can largely keep a lot of the tooling and existing applications running without too much interference. That said, prototyping this is a great next step after the initial eth1+eth2 prototyping.

My understanding is that Swarm and Whisper, while built inside of geth (is this true anymore?), are separate protocols. In such a case, you could still flip a switch on your node to run these protocols as well. In so much as Swarm needing to talk to the existing Ethereum chain, some plumbing/calls might have to be modified.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> I am currently leaning toward preserving everything on Eth1 except bits of data related to the consensus.

Generally agreed here. eth2 handle “consensus”, eth1 handle “application layer” items. The main thing I suggest moving over to the “consensus” is the gossiping of eth1 shard-blocks.

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> A quick look towards this direction makes me think of a separated discovery service as the only way to share it between the parts of the client.

Right, this doesn’t induce additional overhead to start, but maintaining these components in two separate locations is not optimal in the long run. Ultimately, the discovery  could be an entirely independent  service that the eth2-client and the eth1-engine can just ask for peers of certain type on demand. ← that or the eth2-client can take control and give eth1-engine peers as needed.

---

**djrtwo** (2020-04-08):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/r/bcef8e/48.png) ralexstokes:

> This paves the way for better understanding of any tradeoffs inherent in phase 2 if/when we decide to introduce EEs to eth2.

Yes, agreed. I’d like to design and build this in such a way that it informs what an EE path could look like.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/r/bcef8e/48.png) ralexstokes:

> The eth2 consensus ensures that “bad” eth1 shard blocks will not be accepted into the beacon chain; however, there is centralization risk if only a few players can afford to run what will effectively be two full blockchain nodes

In a stateful manner, the eth1-engine is very thin. Essentially just the EVM available to validate a stateless block. So the load to follow the beacon chain and eth1-chain is approximately the same as just following a shard data-chain.

But yes, stateless ethereum is super important here! If not, all validators must bear the load of the entire eth1-chain in such an integration which makes the entire eth2 system much heavier by default.

One thing to note is that we can and should begin prototyping this *without* stateless ethereum two possible paths:

- essentially having all validators be eth-capable and following the eth1 shard-chain. This would allow It’s a bit of a hack, but we can get almost everything in place and with the proper interfaces. Beacon committees would make a stateful check on block validity when crosslinking blocks, rather than the end-goal of stateless
- another option is to just have beacon committees skip the eth1 block validation step (check availability of data but stub the extra call to the eth1-engine to validate the state transition).

^ both are not fully optimal but allow us to move forward on building project before stateless ethereum is ready.

---

**terence** (2020-04-08):

Great starting point, thanks for writing this out.

Just to clarify, an ` eth2-client with stateless eth1-engine` can be an eth2 validator that performs eth1 shard attester duty but NOT proposer duty. Where an `eth2- client with stateful eth1-engine` can perform both duties.

Do I have that right? If yes, I’d assume there would be an eth1-proposer opt in flag

---

**djrtwo** (2020-04-09):

I realized that `eth1-capable` is a poor name.

*All* validators must be capable of executing a stateless block against an EVM so that *all* validators can be selected for eth1 shard-chain beacon committees. The security of the random sampling assumes that the entire set of validators can be sampled for beacon committee crosslinking.

The flag (maybe `eth1-proposer`) signifies that you are willing to not only crosslink (and statelessly execute an eth1-shard block), but that you are also willing to produce these shard blocks. To start, this flag would signify that you have the eth1 state, are listening to eth1 TXs, and that you will make blocks on demand. You could imagine though, that it signifies that you have the capability to produce blocks *in some way*. If the capabilities exist, a validator could also  be stateless but just get good blocks from some third party (i.e. “stateless mining” / “stateless block production”)

---

**terence** (2020-04-09):

Makes sense.  Will the protocol supply an additional `eth1-proposer` reward or just roll with the normal `1/SHARD_COUNT` proposer reward for block proposal in the eth1 shard.

The `1/SHARD_COUNT` proposer reward may not be enough to incentive hosting and maintaining eth1 stateful set. This is probably too early of a discussion

---

**lightuponlight** (2020-04-19):

Is the plan to use the existing ETH1 code as is today, or to use a stateless version of ETH1 code?

The former seems like it could be done very quickly, the latter seems like it might be far away. I think we need to integrate ETH1 into ETH2 as soon as feasible and worry about optimizations later.

---

**axic** (2020-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> ### eth2-client with stateless eth1-engine
>
>
>
> To run a validator, an eth2-client must be run with an adjunct eth1-engine. This can be done in a stateless manner (not storing entire eth1 state locally) because eth1 shard-blocks have witnesses available for execution.

I wonder if the `BLOCKHASH` opcode has any effect on this concept (see [The curious case of BLOCKHASH and Stateless Ethereum](https://ethresear.ch/t/the-curious-case-of-blockhash-and-stateless-ethereum/7304)).The wording seems to suggest in this case the eth2 client would solely rely on the block + block witness and nothing else.

---

**djrtwo** (2020-04-23):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Will the protocol supply an additional eth1-proposer reward or just roll with the normal 1/SHARD_COUNT proposer reward for block proposal in the eth1 shard.

The current proposal is to have an EIP 1559-like mechanism for *all* shard block proposals, and for proposals to only be made if it was worth the value you can gain from making the block less the burn to 1559. This mechanism would also apply for the eth1 shard – the proposers would make the block only if transactions/data made it worth making the block. As of today, a separate reward for this exceptional shard is not expected

---

**djrtwo** (2020-04-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/lightuponlight/48/4337_2.png) lightuponlight:

> Is the plan to use the existing ETH1 code as is today, or to use a stateless version of ETH1 code?

Prototypes are starting today with the eth1 code as is with the plan to keep the interface nearly the same but swap in statelessness when ready.

As for deploying to production – the ideal is deploy stateless eth1 to eth2 as it would reduce the overall requirements on normal validators and users, but depending on relative timelines, it might be considered to deploy eth1 as is (without statelessness) to eth2. This would put the burden of the entire eth1 state on all validators/users and drastically change the base-line requirements to run eth2. Agreed though that such a compromise might be worth it depending on eth1x progress.

---

**djrtwo** (2020-04-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> .The wording seems to suggest in this case the eth2 client would solely rely on the block + block witness and nothing else.

You’re right. I wasn’t aware of this implied component of the eth1 state transition. Assuming we don’t integrate the headers into state (I think doing so is a good idea), the beacon committees would need to sync forward from the latest crosslink in state and back-fill headers (and computed roots) to have the 256 block hashes on demand. It’s doable but puts more bandwidth overhead on the rapidly changing beacon committees.

We’ve been careful with the eth2 state transition function to ensure it is a pure function of `(pre_state, block)` and not have any implied requirements. Ensure that eth1x stateless blocks are just a function of the block would make this integration much more elegant

---

**lightuponlight** (2020-04-23):

Hi Danny, thanks for the input. I do have a follow-up question.

At some point it was stated that running ETH1 validators was optional (even with stateless ETH1 clients) and that people could validate ETH1 + ETH2 or just ETH2?

Has that changed, or is there something about running stateful ETH1 on ETH2 that requires everyone to run an ETH1 client?

---

**mkalinin** (2020-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> the beacon committees would need to sync forward from the latest crosslink in state and back-fill headers (and computed roots) to have the 256 block hashes on demand. It’s doable but puts more bandwidth overhead on the rapidly changing beacon committees.

If Eth1 execution stays stateful then committees will have to keep track of Eth1 state and the history in the background to be capable of attesting to Eth1 shard on per epoch basis. If the execution becomes stateless it should implicitly solve the `BLOCKHASH` issue. It doesn’t seem necessary for Eth1 shard to treat `BLOCKHASH` in a specific way.

---

**djrtwo** (2020-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> If the execution becomes stateless it should implicitly solve the BLOCKHASH issue.

Agreed that this ideally is the case, but it is apparently up for debate (in the context of keeping requisite changes minimal) – see the conversation here [The curious case of BLOCKHASH and Stateless Ethereum](https://ethresear.ch/t/the-curious-case-of-blockhash-and-stateless-ethereum/7304)

---

**djrtwo** (2020-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/lightuponlight/48/4337_2.png) lightuponlight:

> At some point it was stated that running ETH1 validators was optional (even with stateless ETH1 clients) and that people could validate ETH1 + ETH2 or just ETH2?
>
>
> Has that changed, or is there something about running stateful ETH1 on ETH2 that requires everyone to run an ETH1 client?

So the opt-in statefulness (if eth1 was stateless) would be just required for those validators that want to propose eth1 blocks.

If eth1 was integrated in a stateful way, then *all* validators would need the state to be able to “crosslink” eth1 back into the beacon chain. It is secure to only have a subset of validators perform shard block proposal, but it is *not safe* to only have a subset be selected for crosslinking. And to securely crosslink the eth1 shard chain into the beacon chain, committees would need to check the valid execution of the eth1 shard block (easy in stateless, need all the state in stateful).

As for non-validator users, I think you could actually then run the beacon chain without needing the full eth1 state, and from there could make proofs about anything in the shard chains. *But* these users would not be able to follow the eth1 chain head and could only be some sort of light client wrt eth1.

So I misspoke, the burden of the entire eth1 state would not be on all *users* but would make the eth1 chain much less usable for these users.

---

**alonmuroch** (2020-10-11):

Maybe a dumb questions, will eth2 and eth1-shard maintain 2 different account sets?

Would I, as a user, have a BLS account on the beacon-chain and another ECDSA based account on eth1-shard?

---

**matt** (2020-10-13):

[@alonmuroch](/u/alonmuroch) yes, that is the idea. Those beacon-chain accounts may be natively integrated into the eth1 shard at some point, but there is no concrete plan for this currently.

---

**vbuterin** (2020-10-16):

The accounts on eth2 that are being introduced in phase 0 are a special type of account that’s only meant for stakers. If you’re not staking, you would only be using the eth1 (and later eth1-shard) accounts.

