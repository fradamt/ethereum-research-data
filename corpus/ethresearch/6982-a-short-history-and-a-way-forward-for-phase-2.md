---
source: ethresearch
topic_id: 6982
title: A Short History and a Way Forward for Phase 2
author: villanuevawill
date: "2020-02-18"
category: Sharded Execution
tags: [execution-environment]
url: https://ethresear.ch/t/a-short-history-and-a-way-forward-for-phase-2/6982
views: 8414
likes: 33
posts_count: 11
---

# A Short History and a Way Forward for Phase 2

# In the Beginning…

Vitalik’s [2nd proposal](https://notes.ethereum.org/@vbuterin/Bkoaj4xpN?type=view) solidified the idea of `Execution Environment`s. Lets take a look at some of the initial changes it brought to the beacon chain (for now we’ll **completely** ignore the shards).

First, before the `Execution Environment` proposal, the beacon chain looked something like this (fields omitted). Thanks to Casey for providing these initial diagrams:

[![](https://ethresear.ch/uploads/default/optimized/2X/0/0a8aec46443ac1f8a7eb65c639eaf4d2b59d82c6_2_690x299.png)1621×704 57.8 KB](https://ethresear.ch/uploads/default/0a8aec46443ac1f8a7eb65c639eaf4d2b59d82c6)

Similar to eth1, validators maintain basic account fields. Lets define this as the eth2 validator account tree. These accounts do not support code or storage roots.

# Enter Execution Environments

`Execution Environment`s came into the mix with [Vitalk’s phase 2 proposal](https://notes.ethereum.org/@vbuterin/Bkoaj4xpN?type=view). Without thinking of the shards, the beacon state could be updated as follows:

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9c6d2614d72049e08d320e01eefde07f00a22a53_2_690x276.png)1722×689 80.7 KB](https://ethresear.ch/uploads/default/9c6d2614d72049e08d320e01eefde07f00a22a53)

We simply added the `execution_environments` field to the Beacon State. To deploy a new `Execution Environment`, we introduce a new transaction to the Beacon Chain, `NewExecutionScript`(or a new [Beacon Chain Operation](https://github.com/ethereum/eth2.0-specs/blob/8201fb00249782528342a51434f6abcfc57b501f/specs/phase0/beacon-chain.md#beacon-operations) to stay true to the current specifications). It could look like the following:

```auto
{
    "sender": uint64,
    "slot": uint64,
    "code": bytes
    "pubkey": BLSPubkey,
    "signature": BLSSignature
}
```

There was one major flaw to this method. `Execution Environment`s held their balances on the beacon chain. This means `Execution Environments` could not send eth between each other without putting load on the beacon chain (since naturally balances would have to be updated on the beacon chain). Lets continue the discussion.

# Tracking ETH on Shards

Vitalik released a new proposal at Devcon, [“Eth2 Shard Chain Simplification Proposal”](https://notes.ethereum.org/@vbuterin/HkiULaluS). It introduced an “operating system” by which `Execution Environment`s could pass balances across shards to each other. Here was his associated diagram:

[![](https://ethresear.ch/uploads/default/optimized/2X/f/f1a9cd71c079cd7ae20d2cd460a4fad311a11f56_2_432x500.png)671×776 16.3 KB](https://ethresear.ch/uploads/default/f1a9cd71c079cd7ae20d2cd460a4fad311a11f56)

To add clarity to this diagram, the operating system defined how EEs pass eth between each other across shards. First of all, each EE would have a balance on each shard, `ExecEnvID -> (state_hash, balance)`. To pass eth between `Execution Environment`s within a shard, a host function would just update the `balance` field. To pass Eth across shards, a receipt root would be generated, `shard -> [[EE_id, value, msg_hash]...]`. Details on how the receipt roots would arrive on different shards were left to the reader. Also, it seemed the overhead would **limit** the amount of cross-shard transfers.

Next, we needed to more concretely define the details behind a system like this. Vitalik [released a problem statement](https://ethresear.ch/t/moving-eth-between-shards-the-problem-statement/6597).

At this point, lets take a step back and analyze where we have come to.

1. EEs hold a balance and state_hash on each shard
2. An operating system needs to be established to prevent leakage. AKA the protocol needs to make sure balance or eth can be passed across shards without eth being lost or printed.

We began to realize we’re basically defining an account model for `Execution Environment`s. Lets first take a look at what the account model looks like in Eth1 and use a simple ERC20 contract as an example:

[![](https://ethresear.ch/uploads/default/optimized/2X/4/4f1fbc271448555456f77d9820d5a9046d29d5e0_2_439x500.png)1012×1151 119 KB](https://ethresear.ch/uploads/default/4f1fbc271448555456f77d9820d5a9046d29d5e0)

An `Execution Environment`’s place is not so different within a shard - especially now that we store `balance` and `state_hash` on the shard. We’d likely see an almost identical account model within Eth2’s shards:

[![](https://ethresear.ch/uploads/default/optimized/2X/4/43ccc0254bbc2abe4cfefc0e4f45db05c9868c92_2_690x240.png)2335×813 97.3 KB](https://ethresear.ch/uploads/default/43ccc0254bbc2abe4cfefc0e4f45db05c9868c92)

Whether the `E2contract` leaf is on the beacon chain or not, the core of the `E2ContractState` does not seem to be too different than what we have on eth1. There is a wasm code hash, balance, and state root. So lets view `Execution Environment`s through a different lens. They seem to just represent top level contracts or accounts within the shards. This puts a new lens/image on the entire cross-shard discussion and problem statement. Lets review the points made earlier:

1. EEs hold a balance and state_hash on each shard
2. An operating system needs to be established to prevent leakage. AKA the protocol needs to make sure balance or eth can be passed across shards without eth being lost or printed.

#2 is just enshrining a transaction model or way to transfer eth between accounts, not too different than how eth1 has an enshrined transaction model. We’d also need a standardized serialization format (hint: SSZ!). We’d probably need a way for EEs to call into each other programatically and send eth between each other (hint: CALL Opcode). Vitalik [takes a stab](https://ethresear.ch/t/an-even-simpler-meta-execution-environment-for-eth/6704) at how that may be done via a netting model and what is called a “meta-execution EE”. Casey puts together a [very clear explainer](https://ethresear.ch/t/an-even-simpler-meta-execution-environment-for-eth/6704/3) of what the netting model is. We put together [some scribbles](https://hackmd.io/g-FvxXFoRDWYGPIEs82AAQ) on how this may be put in action (don’t let this confuse you too much - you can just keep following this writeup). The conclusion is that we’re basically defining a core protocol layer - a transaction and account model for `Execution Environment`s or what we can call as simply `Top Level Contracts`. For the remainder of this writeup, I’ll use these terms interchangeably.

# Native Integration of Eth1 Account Model

So lets take this conversation forward another step. If we’re already enshrining a root level contract or account model, what is the point of `Execution Environment`s at all? Why not just have contract wallets, ERC20 contracts, exchange contracts and everything else live at this root protocol layer - similar to eth1? I’m putting the eth1 account model below again just to remind you:

[![](https://ethresear.ch/uploads/default/optimized/2X/4/4f1fbc271448555456f77d9820d5a9046d29d5e0_2_439x500.png)1012×1151 119 KB](https://ethresear.ch/uploads/default/4f1fbc271448555456f77d9820d5a9046d29d5e0)

So the big question is, how are `Execution Environment`s actually different than an eth1 contract since here has to be an enshrined transaction, serialization format and call/send method anywyas? Simply put, it’s not that different (lets ignore whether the wasm code is stored on the beacon chain or shard for now). However, in the direction of eth2, we wanted to introduce generality and a light core protocol layer with a unique degree of abstraction. Lets add a few more diagrams here:

[![](https://ethresear.ch/uploads/default/original/2X/f/f222ac1a4da62c140502b6056ba6b82cf5385aef.png)621×321 3.68 KB](https://ethresear.ch/uploads/default/f222ac1a4da62c140502b6056ba6b82cf5385aef)

Here we assume each EE gets a 32 byte state root in the shard. This state root may actually be stateful on the shard. We will cover the scenario where it isn’t in a moment. For now, lets assume the shard stores this 32 byte state root (on the shard state or via a **cache** works just fine). When a validator syncs to the shard, it downloads these state roots.

So why doesn’t it just transform into the following?

[![](https://ethresear.ch/uploads/default/original/2X/8/81e137e1e939b278a7a39f6308146264c0136fc0.png)621×321 4.79 KB](https://ethresear.ch/uploads/default/81e137e1e939b278a7a39f6308146264c0136fc0)

Why don’t users just manage their accounts or contract wallets at this top level? All the tools that are necessary exist here (wasm code, balance, transferrability). The answer is simple. We want to keep the core eth2 protocol light and unopinionated. There are several different ways of designing execution systems and instead of choosing or locking into one, Eth2 may allow for multiple to be designed and experimented with in parallel. The effect can be seen in the following diagram:

[![](https://ethresear.ch/uploads/default/optimized/2X/3/30d34dec8b7bfb076f1c210343ca6e8207077976_2_690x156.png)1418×321 6.8 KB](https://ethresear.ch/uploads/default/30d34dec8b7bfb076f1c210343ca6e8207077976)

Maybe `EE1` follows a hexary-patricia tree. Maybe `EE2` follows a sparse merkle tree. Regardless, you see that contracts (as we know them today in eth1) get pushed down one level in the tree of accounts. They get pushed down as child contracts.

What effects does this have?

# Effects of a Minimal Protocol

## Governance

An Execution Environment (or top level contract) will likely have to set its own governance rules. In eth1, if we needed to change the transaction format, account model, accumulator for the patricia tree, storage methods, or state rent, we would need to fork the core protocol.

Initially, this could also be done in eth2. Hard forks could change the wasm code for deployed EEs, adjusting its rules as desired. Long term however, in a world of multiple EEs, governance and upgrade patterns could no longer rely on system wide forks. Instead, EEs would have to choose whether to include ways to upgrade its own code - e.g. via coin voting, staking, or a multisig - or to remain immutable forever. Additionally, contracts could choose to offer migration functionalities to move to an upgraded new EE, e.g. via yanking patterns.

## State Rent

Each EE or account model may present different pros/cons. Maybe EE1 provides limited state but no state rent. Maybe EE2 provides limitless state but it costs more and integrates a state rent model. Maybe EE1 restricts the total state to 1TB (these would all have direct effects on state provider pricing, etc.).

## Ecosystem Funds

Each EE could have its own ecosystem fund. EE1 may say 0.5% of its gas fees get routed to an ecosystem fund. This ecosystem fund may then be routed towards developers who are working around/in this EE.

## Shard Presence

EEs could reduce their shard footprint and only exist on a range of shards. They may have governance models in place to expand those over time. This may in effect decrease fees to use this EE in the short term until it expands and grows.

## Accumulator

EEs would define their own accumulators with what fits in their model.

## Transaction Model

EEs would define their own transaction structure and fields.

## Serialization

Other serialization methods may show promise over SSZ that the core protocol provides. Leaving this in the hands of the EE is interesting.

## Cross Shard Communication

With ETH as the native protocol currency, [some enshrined method for cross shard ETH transfers will be necessary](https://ethresear.ch/t/implementing-cross-shard-transactions/6382). Beyond that however, EEs could be free to [choose their own communication standards](https://github.com/ethereum/wiki/wiki/Sharding-FAQ#how-can-we-facilitate-cross-shard-communication) such as bitfield or queue/nonce models for receipt processing.

---

The TL;DR is that this model seems to push innovation/adptation and encourages protocol developers to use Eth2 as a base protocol to try new models & approaches on execution frameworks. By pushing the complexity down a level in the tree, we **do not** couple the protocol to these adaptations. Eth2 developers do not have to take opinions on ecosystem funds, state rent or areas of governance. If we want to try new transaction formats or serialization formats, we get to do this and we don’t need to fork the protocol! Eth2 seems to become a foundation for major innovation in the blockchain/cryptography space with a fluid way to advance & adapt over the years.

In order to accomplish all of this, we need to introduce an incentive to push this complexity down a level in the tree. We do this via simply making it **quite expensive** to deploy an `Execution Environment` or `Top Level Contract`. We suggest a model where a fee (say 500 eth) has to be locked up (aka a rent by deposit model), but there are many incentive mechanisms that can be evaluated, and these can be adjusted over time.

# Enshrined Execution Model

So lets continue to move forward. What happens if instead of following this tiered model (or having Execution Environments), we just enshrine one model to the protocol to start off with? Well, we already talked about how the protocol **is already** doing that for the top level or for `Execution Environment`s. So lets explore the route where Eth2 essentially becomes a modernized eth1 - we likely add needed host functions for account abstraction, shard awareness, cross shard transactions, etc..

[![](https://ethresear.ch/uploads/default/original/2X/8/81e137e1e939b278a7a39f6308146264c0136fc0.png)621×321 4.79 KB](https://ethresear.ch/uploads/default/81e137e1e939b278a7a39f6308146264c0136fc0)

Our regular contracts (wallet contracts etc.) all get thrusted to the top tier of the tree. The roots for each of these may be stateless. They could also be stateful if we choose (or driven by a cache).

[![](https://ethresear.ch/uploads/default/original/2X/f/f1f5109cb4355f340fe1d19c459e9fa2012dfdcb.png)621×231 3.77 KB](https://ethresear.ch/uploads/default/f1f5109cb4355f340fe1d19c459e9fa2012dfdcb)

If we move in this direction, this means deploying at the top layer of the tree would be inexpensive. We would also be enshrining one accumulator, account model, execution model etc. into eth2. We basically have an upgraded eth1 that is shard aware. This approach may be interesting, because of reduced complexity.  However, what drawbacks may this have?

1. Language-specific implementation for each client. Each client would likely build this logic in their own language
2. Any changes to the account model, accumulators, transaction model, etc. require forking the core protocol
3. State rent, state size limits needs to be coupled to the core protocol
4. We risk stunting innovation on the EE front (there are multiple efforts right now building an ORU, eth2 EE, ZK rollup EE, mixers, etc.)
5. We risk locking/coupling the protocol to one model and a more general/iterative model with parallel efforts is stunted

It may be argued, that this approach is **not that** different and that we can still accomplish an EE-like model in this setup. Essentially, we can still push abstraction and contract frameworks in a model like this:

[![](https://ethresear.ch/uploads/default/optimized/2X/c/c3b3767568f2daf045dd455ca9caa7254ae8c203_2_690x219.png)1015×323 5.95 KB](https://ethresear.ch/uploads/default/c3b3767568f2daf045dd455ca9caa7254ae8c203)

However, encapsulation and separation of concerns with the core layer seem to introduce issues. This new contract framework under experimentation may have general caveats. For example, if there is a different governance rule, state rent scheme, upgrade plan, etc. then it may be risky to encapsulate your logic in this child contract framework (when the top level provides functionality). For example, a contract may instead just decide to use storage at the top level.

[![](https://ethresear.ch/uploads/default/optimized/2X/9/93bc423b9dac4e283aa0b78d9393d86403f0ca20_2_690x177.png)1247×321 15.4 KB](https://ethresear.ch/uploads/default/93bc423b9dac4e283aa0b78d9393d86403f0ca20)

There are many other examples that can be used on breaking encapsulation. Forking the protocol may have an effect on these child contracts (or no effect and couples governance/updates). Why even go with the trouble of pushing abstraction down another level - when it appears to introduce more conplexity on top of what the protocol already has? How hard will it be to in the future decouple transaction, account logic etc. from the core, eth2 protocol and transition it to a lighter model? In reality, it appears this encapsulation and world of child contracts is discouraged in this model.

However, maybe we can accomplish the same result of simplicity and hyperfocus on just one account model to start and still get the benefits of a light, core protocol that pushes abstraction down a level? Perhaps we can have a phased, phase 2.

We go back to our original diagram where it is expensive to deploy a `top level contract` or `Execution Envrionment` in the higher tier of the tree.

[![](https://ethresear.ch/uploads/default/optimized/2X/3/30d34dec8b7bfb076f1c210343ca6e8207077976_2_690x156.png)1418×321 6.8 KB](https://ethresear.ch/uploads/default/30d34dec8b7bfb076f1c210343ca6e8207077976)

We hyperfocus on the development of `EE1` in that diagram. Upcoming testnets and design choices still allow multiple `top level contract`s to form (or `Execution Environment`s), but we take an opinion that the initial launch of phase 2 **may not** allow for additional deployments until we are ready. It looks like this instead:

[![](https://ethresear.ch/uploads/default/original/2X/9/9fa42a27129d7d69bad7e23480db2d078451f483.png)661×411 5.13 KB](https://ethresear.ch/uploads/default/9fa42a27129d7d69bad7e23480db2d078451f483)

In the meantime, our testnets allow for multiple `Execution Environment`s and we can experiment with how `Execution Envrionment`s communicate with each other.

So what is the biggest difference here? It’s that the logic for `EE1` is defined entirely in wasm. Our roadmap still optimizes for a world of multiple `Execution Environment`s and a light, general protocol. But the actual amount of work and complexity **does not** increase from an enshrined model. We don’t have to take a concrete opinion on cross-EE communication. We can iterate on that as we see more activity in our testnets.

How do we upgrade this `Execution Environment` or `EE1`?

In the early stages, we can choose to update one wasm script **across all clients** and fork the protocol to update that. Once we find stability, we can expand deployments for multiple EEs and no longer require forks to upgrade the canonical EE.

Note: this scenario would not preclude us from launching several EEs from the start. We would even prefer to have more than just the one canonical EE ready for the phase 2 launch. However, the deployment of custom EEs **may** be restricted in the beginning and only be opened up at a later time.

## Cross Shard Transactions

So lets continue the discussion from where we left off earlier. Vitalik framed a model to pass eth between EEs and across shards to prevent eth leakage aka [meta-ee discussion](https://ethresear.ch/t/an-even-simpler-meta-execution-environment-for-eth/6704). We continue to build into our model (at the core protocol) a method like this (netting scheme). But nailing the details on the cross-EE discussion isn’t as important right away. However, in a one EE model or multiple EE model, we still need to decide how the protocol supports cross shard transactions.

The netting scheme (linked above) is somewhat orthogonal to the discussion of transferring arbitrary data across shards (hint: receipts). The main question we need to decide: should the protocol offer a built in mechanism for cross-shard data transfers, aka an enshrined receipt system?

Having such a system provided by the protocol layer could simplify cross shard communication from the EE perspective, as the EE would not have to deal with most of the associated complexity (e.g. replay protection, ordering, …). This would however come at the cost of moving that complexity to the protocol, which goes against the general eth2 design goal of having a slim, minimal base layer. In particular, questions around guaranteed delivery would be challenging to answer:

- Does the protocol guarantee execution of a cross-shard transaction on the receiving shard?
- How would fee payment work under such a system?
- What if a shard would receive a high number of incoming transactions from multiple other shards?
- If delivery was not guaranteed by the protocol, who would be responsible for processing the incoming transactions?

We believe avoiding this complexity on the base layer fits better with the overall eth2 philosophy. Thus, it should be up to the `Execution Environment` to implement cross-shard communication patterns such as through a [bitfield/receipt mechanism](https://github.com/ethereum/wiki/wiki/Sharding-FAQ#how-can-we-facilitate-cross-shard-communication), [nonce/queue model](https://ethresear.ch/t/implementing-cross-shard-transactions/6382), or via [object capabilites](https://notes.ethereum.org/Sd3pOEwrQSaYeXHdAmIEvw?view) with replay protection. This takes an overall **passive** approach and supports models as [described here](https://ethresear.ch/t/commit-capabilities-atomic-cross-shard-communication/6509).

However, we may find that certain properties we come across (such as in the object capabilities model), make sense to introduce supporting host functionality. For example, this functionality could enable the protocol to provide proper error or success handling in communication between EEs.

## State Provider Network or Witness Protocol

One of the main research questions is regarding Static State Access (SSA) vs. Dynamic State Access (DSA). [This writeup](https://gist.github.com/SamWilsn/369de587ac7373c8f77ed26079531671) describes DSA & SSA. [Here was an early overview and writeup](https://ethresear.ch/t/state-provider-models-in-ethereum-2-0/6750) on state provider networks in eth2 and how DSA/SSA affects the conversation. Since this writeup, we’ve somewhat shifted our hypothesis towards recommending an SSA model. It could offer major benefits by introducing a more elegant model around memory/storage which somewhat mimics Rust style ownership/borrowing syntax. Eth1 currently operates on a DSA model, but our early research suggests that moving to an SSA model could be possibe without loss of functionality (including for DeFi applications). [We have been extending current solidity](https://github.com/SamWilsn/solidity/tree/state-taint-0.5.16?files=1) tooling with taint analysis in order to detect DSA in an automated format and foresee the necessary tooling for contract developers. If we can accomplish SSA properly, we will likely see significantly reduced complexity in the state provider network implementation and benefits in **account abstraction** (AA) models.

# Proposal for a Phase 2 Implementation Plan

Summarizing the narrative above, we suggest breaking up the implementation work into two steps, but with the goal of deploying it all at once. We organize these steps into the necessary work required at the core protocol vs. the `Execution Environment` (EE) layer.

- Phase 2 base protocol with:

Netting for cross-shard ETH transfers
- SSA (with the exception of the eth1 shard continuing to support DSA)
- Native support for transaction verification to support Account Abstraction (AA)
- Other host functions deemed necessary along the way
- Possible restricted EE deployment to just the canonical or several predefined EEs

Canonical / General Purpose EE (aka EF sanctioned EE):

- User level cross-shard communication capabilities (experimenting with different approaches - aka bitfield, nonce/queue, object capabilites
- Account Abstraction
- Passive cross-shard developer tooling
- Extending Solidity to support development of SSA smart contracts, development including access to all relevant eth2 host functions

With a canonical/general purpose EE, we will assume early updates will require forking the protocol before we remove restrictions on EE deployments.

**Goals to reach for**:

- Strong, cross-EE communication standard
- Canonical EE, Optimistic Rollup EE, ZK Rollup EE supported on launch
- Unrestricted EE deployment
- Non-altruistic state network

Quilt has [already been building tooling](https://github.com/quilt) to support this roadmap. Our concrete plan **is to have** an open EE testnet in 3-6 months with a testnet around the canonical/general purpose EE in 6 months to a year.

Thanks to my fellow Quilt team for contributing to this writeup: [@adietrichs](/u/adietrichs), [@SamWilsn](/u/samwilsn), [@matt](/u/matt), and @gt

Also thanks to [@rjdrost](/u/rjdrost), [@cdetrio](/u/cdetrio), and [@adlerjohn](/u/adlerjohn) for review and guidance.

*This writeup is the perspective from the Quilt team on the way forward with eth2 phase 2.*

## Replies

**djrtwo** (2020-02-19):

Thank you [@villanuevawill](/u/villanuevawill) and everyone else that that has put so much into this.

I’m generally in favor of the plan. As I’ve said in other channels, we *must* solve all of the concrete problems (other than the proper level of abstraction) at least once. If we spend too much time and effort debating the most perfect level of abstraction today, we stand to greatly delay an initial useful launch. In addition to that, if we don’t launch Eth2 with something that feels tangibly like Ethereum to the developer community (the people that make the ecosystem so great today), then we stand to muddy the narrative and to lose some of Ethereum’s momentum.

EEs – what they are, who should be writing them, and why they are useful – are even confusing to many of us at the core of eth2. A clear vision of *an* executable eth2 must be presented to the wider (non-protocol focused) developer ecosystem.

Abstraction should be something we generally plan for and continue to chew on as we move forward with a concrete, Ethereum-like single EE along with a path to integrate Eth1 into the scalable Eth2 infrastructure.

If we do go for the long-term open EE landscape, I think we must more clearly define the advantages in explicit design cases. I too have the general intuition that EEs make Ethereum more future-proof and extensible in the coming decades, and that they **might** solve certain governance issues. But on the technical side, clearly demonstrating that e.g. a ZK Rollup specific EE has significant concrete benefits over defining it as a contract inside of a more general EE will be valuable (for example: significant reduction in costs of evaluating ZKPs, major accumulator gains, etc).

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Language-specific implementation for each client. Each client would likely build this logic in their own language

This is not certainly a downside. Having language/client specific implementations of fundamental logic could in some cases lead to much more performant implementations. A key thing we must demonstrate even as we follow a single-EE path is that a WASM implementation can be performant enough to meet our base layer expectations (i.e. is fast or faster than the compiled implementations of the EVM today).

---

I see four parallel tasks that we, across teams, must prototype and specify:

1. The migration of eth1 into a single shard (ideally in a way that makes it EE-like or can be made EE-like eventually). Other important items are how eth1 clients (or components of them) sit in the mix here, the communication protocol between an eth2 and eth1 client, and how these patterns might inform other EE design
2. Core sharded and stateless protocol mechanics – cross-shard ETH transfers, cross-shard general communication (e.g. receipts), what state exists in shards, state providers, relayers, network structures, etc
3. An Ethereum-like cross-shard aware EE (aka, the eth2 EE). Ideally written in WASM, demonstrating that WASM can be the appropriate choice for core execution.
4. The general model of extensible EEs – additional beacon chain operations, economics (ETH lock, load on core protocol, etc), cross-EE comms, prototyping future EEs and demonstrating advantages, EE developer tooling, upgradability, etc

My current read is that: (4) is getting too many resources, (2) is getting appropriate resources, whereas (1) and (3) are at a deficit. I propose that we reorganize some of our efforts to ensure that (1) and (3) get a really solid push in the coming 6 months so that we can deliver on the full (initial) eth2 vision soon ![:tm:](https://ethresear.ch/images/emoji/facebook_messenger/tm.png?v=12). EEs are hot ![:fire:](https://ethresear.ch/images/emoji/facebook_messenger/fire.png?v=12) and very exciting, but, again, we must solve the concrete problems of execution at least once to deliver on an executable Eth2 for the devs and users of Ethereum’s current amazing ecosystem.

---

**kladkogex** (2020-02-20):

Hard to imagine  why Execution Environments are useful at all.  Most people program in EVM and need a better EVM.  Similarly for web programming most people like Javascript and want a better Javascript.  You can include any generic EE in a browser, people wont notice it for the most part and will continue programming in javascript.  It is a solution in search of a problem imo, people simple do not need this except niche academic experimentation. If providing a tool to academia is the purpose, then EEs are definitely useful.

---

**villanuevawill** (2020-02-20):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Most people program in EVM and need a better EVM.

From a developer perspective, people are writing their contracts in solidity and compiling to Yul as an intermediate. Improving on the EVM can be fairly orthogonal to EEs - aka the vision plan in this writeup is to first focus on one execution model (EE).

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Hard to imagine why Execution Environments are useful at all.

I’d love to hear a direct response to the points, benefits, etc. in the writeup above. There appear to be a lot of interesting benefits to an EE path (the writeup covers these) - particularly, it is relatable from a computing perspective. If we have a light, unopinionated base layer, then eth2 **could** be seen as a platform supporting a world of kernels or VMs. Currently, teams who are interested in trying out an entirely different execution model rely on trying to start a new ecosystem or chain. In a light, core protocol layer, this abstraction/approach can be built on this base layer.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Most people program in EVM and need a better EVM.

Again, this appears to be fairly orthogonal. The roadmap outlined hyperfocuses on one execution model. I’ll **reiterate**, we don’t know what the future of the blockchain/disributed computing world will become. A flexible, light protocol layer allows us to have reasonable upgrade paths without locking ourselves into one model in the longterm (it seems these decisions help us from a longevity standpoint). To this day, one of the hurdles in eth1 is how coupled the execution logic/account model is to the core protocol (even though a lot of the decisions we realize in hindsight did not make a lot of sense).

---

**hkalodner** (2020-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> A flexible, light protocol layer allows us to have reasonable upgrade paths without locking ourselves into one model in the longterm

In a lot of ways I hate this comparison, but this makes me think about what SegWit did for Bitcoin, making it so that significant feature additions are easily possible via soft fork whereas before it would have extremely complicated to implement them without a hard fork.

The most powerful part of Ethereum to me has always been how easy it is to innovate on, and the changeover to EEs seems to unlock the ability to innovate on a large array of components that are hardcoded in ETH1.

---

**villanuevawill** (2020-02-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> is there a market and users for this?

The canonical EE **is an upgraded** version of eth1 designed around a multi-sharded world. I don’t think there is a disagreement here. The conversation around Execution Environments is fairly orthogonal to this, although it still appears it would likely improve the user experience in the longterm.

In eth1, there are many eips that could not get launched because it is a big task to change the base protocol layer. If the platform supported a quicker iteration cycle (and less coupling to the core protocol layer), we would likely see a platform on eth1 today that is significantly improved for users. Although it seems like a protocol research move, it still appears to be beneficial to the user layer.  For example, If we build one strong EE that is user centric - that is great. Now there could be a much better upgrade, innovation path with the direct result being eth2 may likely iterate quicker for user needs via Execution Environments. Developers don’t need to coordinate execution/account changes to the base protocol layer to add functionality. Also, we don’t require new chains/ecosystems to pop up as a result of not having a flexible protocol layer where changes can be added.

I’ll  **reiterate** , we don’t know what the future of the blockchain/disributed computing world will become. A flexible, light protocol layer allows us to have reasonable upgrade paths without locking ourselves into one model in the longterm (it seems these decisions help us from a longevity standpoint). To this day, one of the hurdles in eth1 is how coupled the execution logic/account model is to the core protocol (even though a lot of the decisions we realize in hindsight did not make a lot of sense and impacted the users directly).

At worst, if it turns out there is no need for multiple EEs, eth2 would just be an upgraded eth1 in a multi-sharded world. We don’t lose anything (although I do not think this will be the case at all).

---

**MrChico** (2020-02-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Eth1 currently operates on a DSA model, but our early research suggests that moving to an SSA model could be possibe without loss of functionality (including for DeFi applications).

I’m very curious about this point. Do you have any pointers to this research or can you provide some hints on how for example a DEX can be implemented with only SSA?

For a transaction grabbing the best offer from an order book, it seems natural that the contract would need to first look up the best offer in state, and depending on this state variable further decide which accounts to credit.

---

**adietrichs** (2020-02-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/mrchico/48/2264_2.png) MrChico:

> I’m very curious about this point. Do you have any pointers to this research or can you provide some hints on how for example a DEX can be implemented with only SSA?
> For a transaction grabbing the best offer from an order book, it seems natural that the contract would need to first look up the best offer in state, and depending on this state variable further decide which accounts to credit.

We have started looking at several of the most popular projects to evaluate their reliance on DSA, with DEXes high up on that list. However, most of the DEXes we have looked at so far use mechanisms of off-chain order matching and only do on-chain settlement (e.g. IDEX and 0x). The settlements there are either already SSA or could be easily adapted, given that the counterparties are already known at the time of transaction creation.

Additionally, Uniswap as the most popular DEX uses a one-sided model, where trades happen directly with the Uniswap exchange contracts - so no problem there either.

We will continue looking at additional Eth1 projects to see whether there are any more fundamental SSA issues. It is important to note however that even for complex use cases like on-chain order matching there could be SSA workarounds (see e.g. [this old post by Vitalik](https://ethresear.ch/t/common-classes-of-contracts-and-how-they-would-handle-contract-state-root-plus-witness-architecture/4547), specifically the “On-chain order books” section).

We are also [developing tooling around SSA contract development](https://ethresear.ch/t/automated-detection-of-dynamic-state-access-in-solidity/7003/3), hoping to demonstrate how the move to SSA would only have a minimal impact for contract developers.

We will likely have further results of our SSA research to share later on, which I will then make sure to link here.

---

**sinamahmoodi** (2020-02-24):

> A flexible, light protocol layer allows us to have reasonable upgrade paths without locking ourselves into one model in the longterm…one of the hurdles in eth1 is how coupled the execution logic/account model is to the core protocol

I’d like to decouple this and talk about flexibility and protocol-lightness separately. A protocol with one canonical EE can still be (more-or-less) flexible. ZK-rollup, optimistic-rollup, etc. can and are being built on eth1. You could even build an “Eth1 EE” in evm right now.

I agree eth1 could be more flexible. What I’d like to see discussed is what exactly is hurting innovation and flexibility on eth1. Account abstraction is one, e.g. by removing nonce & signature from the tx format we could allow a wider variety of innovation and there’s already demand for it. On the other hand I don’t think defining a storage accumulator in the protocol harms flexibility much. Contracts are free *not* to use it, just SSTORE a 32-byte value and use any accumulator off-chain. The VM and metering have to be defined in both variants (multi-EE, single-EE), so no difference. What host functions are exposed to contracts affects flexibility. This one is interesting because adding more host functions improves flexibility but hurts protocol-minimalism.

> In eth1, there are many eips that could not get launched because it is a big task to change the base protocol layer

If we had a NewShinyEE with as much value locked on it as eth1, it’ll have the same iteration cycle as Eth1, and for good reason. Moving it from the protocol doesn’t immediately solve the need for backwards-compatibility, security analysis, etc. Besides with a flexible canonical EE a rollup contract could still offer a migration path to its improved new version (same way an EE would migrate, I’m not sure how that is).

---

**adietrichs** (2020-02-28):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> A protocol with one canonical EE can still be (more-or-less) flexible. ZK-rollup, optimistic-rollup, etc. can and are being built on eth1.

I agree that Eth1 has been remarkably flexible over the years and that it is indeed not certain that Eth2 will need the additional flexibility EEs would give us. However, I would argue that one main design goal for Eth2 should be to maximise its future-proofness. And in my view having a clear separation between the core protocol and the execution environment(s) is key to being future-proof.

There are many different arguments one can come up with for how multiple EEs could be useful in the future: For some of the large projects it might make sense to move to their own special-purpose EEs. Under Eth1, those projects can iterate quickly on their own code, but have to wait a long time for any protocol-related changes they need. With their own EE, they could now iterate on all details of execution with the same agility, while under SSA retaining the ability to synchronously communicate with the main EE. For smaller projects that do not need a full custom tailored EE, but specifically rely on a EE-level change, it might make sense to fork the canonical EE, add the desired feature and deploy on this EE. Should the canonical EE later on adopt the feature, the project could have provisions in place for migrating back to it. Additionally, while we expect there to only be one general purpose EE to start with (as laid out in the post), long-term we might also see broader experimentation with different approaches to general purpose on-chain computation.

The point here again is not to predict exactly how Eth2 will be used, but to design it in a flexible way to accommodate any of these potential use cases. And I think this is especially reasonable in the case of EEs, where the price we pay is just the clear separation between core protocol and execution environment. The core protocol (analogy: hardware) should contain all functionality that required for all execution and is mostly unchangeable. It should thus be as un-opinionated as possible and has to be manually implemented by every Eth2 client. An execution environment (analogy: operating system), on the other hand, is more like a set of core libraries, providing standardisation around things like transaction formats, state, account system, etc. Here it makes sense to be opinionated, designing an environment well suited for most executions. Having these EEs be defined in EWASM (or theoretically EVM) is critical, as it means that clients don’t have to manually implement support for new or upgraded EEs - EEs really are just code.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> ZK-rollup, optimistic-rollup, etc. can and are being built on eth1. You could even build an “Eth1 EE” in evm right now.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> I don’t think defining a storage accumulator in the protocol harms flexibility much. Contracts are free not to use it, just SSTORE a 32-byte value and use any accumulator off-chain.

There are several disadvantages to having EE-like systems on the contract level under one main execution environment. For one, having to double all functionality causes significant overhead. In your accumulator example, if you want to still have on-chain execution, the storage would in fact have to be handled on-chain. In addition, going down that route would increase the risk of a fractured contract landscape, with broken encapsulation as described and illustrated by [@villanuevawill](/u/villanuevawill):

[![](https://ethresear.ch/uploads/default/original/2X/4/454ddbcc222979c179f599429394fe85a6fde871.png)690×177 7.94 KB](https://ethresear.ch/uploads/default/454ddbcc222979c179f599429394fe85a6fde871)

Worst case, if we see that the one canonical EE is all that is needed, we effectively just fall back to the enshrined execution model. To me this seems like a situation with low downside and high potential upside.

---

**kladkogex** (2020-03-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> At worst, if it turns out there is no need for multiple EEs, eth2 would just be an upgraded eth1 in a multi-sharded world. We don’t lose anything (although I do not think this will be the case at all).

Well … Will -  let me play a bit of a Devil’s Advocate (as if I did not already do too much of it on this message board )

First, as a side comment,  sharding is far from obvious the right way to scale layer 1. (not going to go into that rabbit hole any further  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)  ). If I had a vote (as if anyone is interested to count my vote) I would vote to keep the Layer 1 network free of sharding.  It is too complex for Layer 1. Moreover, it is very non-obvious to me how many users will be  fast enough to learn the complexity of sharding.

For execution environments you actually DO lose something, meaning security. EVM running on an EE vs the current EVM will have another attack surface, namely, EE.

It will take time to prove this thing is secure. I hope that there will be no embarrassments similar to the ones that happened during the first years of Solidity.

Having said that, I have to confess,  I like EEs!!! mainly due to the reasons you bring up in your comments.

