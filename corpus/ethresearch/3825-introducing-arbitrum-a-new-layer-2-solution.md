---
source: ethresearch
topic_id: 3825
title: Introducing Arbitrum, a new layer 2 solution
author: hkalodner
date: "2018-10-17"
category: Layer 2
tags: []
url: https://ethresear.ch/t/introducing-arbitrum-a-new-layer-2-solution/3825
views: 19311
likes: 50
posts_count: 19
---

# Introducing Arbitrum, a new layer 2 solution

# Introduction

Hi all!

I’m Harry Kalodner, a Ph.D. student at Princeton and co-founder of [Offchain Labs](http://offchainlabs.com). We’re building a new layer 2 system on Ethereum for increasing the scalability and privacy of smart contracts based on our [academic work](http://offchainlabs.com/Arbitrum-USENIX.pdf) Arbitrum, published in USENIX Security earlier this year.

We’re currently working on building our deployment of Arbitrum on Ethereum. If you’re interested in joining the effort, contact us at [jobs@offchainlabs.com](mailto:jobs@offchainlabs.com). For more info on Arbitrum, keep reading.

Arbitrum enables the creation of Arbitrum Virtual Machines (VMs) which are smart contracts: first class actors that can send and receive funds and messages as well as perform calculations and store data offline according to their code. Arbitrum VMs are much more scalable and private than conventional ways of implementing smart contracts.

Arbitrum does almost all of the management of VMs off-chain, with a minimum of on-chain work to ensure correct execution.  To achieve this, when someone creates an Arbitrum VM, they select a set of managers who will be responsible for executing the VM. Arbitrum guarantees that any single honest manager can ensure that the VM executes correctly (even if all of the other managers conspire to try to cheat).  And because hardly any data about a VM is ever put on-chain, Arbitrum VMs are much more private than many other system.

In particular, only a cryptographic hash of the VM’s state is stored on-chain.

Arbitrum gives the managers of a VM incentives to agree on what the VM will do, and if the managers agree unanimously on what the VM will do, the system accepts that and it is recorded on-chain.

# Dispute Protocol

If, contrary to incentives, the managers cannot agree on a VM’s execution, they can fall back on an assertion/challenge/dispute protocol that’s still very efficient. First, one manager makes a disputable assertion–a claim about what a VM will do. The asserting manager escrows a deposit as a guarantee that they’re not lying. Then other managers have a fixed time period to challenge the assertion if they think it’s wrong. If nobody challenges, the system accepts the assertion.

If somebody does issue a challenge, the challenger escrows a deposit as a guarantee that they’re not lying. Now the system will referee a dispute protocol to determine who is lying, and the liar will lose their deposit. This happens in two phases:

The first phase relies on recursive bisection (based on Refereed Delegation of Computation, invented by Ran Canetti et al in 2011, and as used in TrueBit). The dispute protocol first demands that the asserter break their assertion into two half-size pieces; if the initial assertion covered N instructions executed by the VM, then each half should be an assertion about executing N/2 instructions.  Next, the challenger must pick one of the two halves to challenge. At this point the size of the dispute (the number of instructions) has been cut in half.  The same procedure is used recursively, until there is an assertion about a single instruction of execution that has been challenged.

The second phase requires the asserter to provide a “one-step proof” which demonstrates that starting with the initial VM state hash, executing one instruction will lead to the claimed final state hash. The cost of a one-step proof, in terms of size and proof-checking time, is a critical factor controlling the cost of dispute resolution. So we carefully engineered the Arbitrum VM architecture to make one-step proofs cheap. As an alternative, we could have used something like WASM, but that would have lead to substantially higher costs.

# VM Architecture

Our academic paper goes into detail about the VM architecture. The bottom line is that

using our architecture, the total cost of a challenge including the bisection is `O(log N + log log M)`. This is compared to standard architectures like WASM where the cost would be `O(log N + log M + log C)` where N is the number of instructions executed, M is the size of the memory, and C is the size of the code. Arbitrum one-step-proofs are always under 500 bytes, and usually around 200 bytes.

Our implementation of Arbitrum on Ethereum will allow Arbitrum VMs to own and send any ERC20 or ERC721 token as well as Ether. VMs are also capable of receiving data from Ethereum smart contracts.

To provide a simple example of Arbitrum in practice, imagine Alice and Bob want to bet on a game of chess. Alice and Bob create a new VM which includes the rules of chess and select themselves as managers of the VM. Assuming they are honest and online, they can play the entire game off-chain in a typical state-channel-like fashion. Even in the worst case, either Alice or Bob can force the game to complete, either through timeout or victory, without having to execute any of the chess logic on chain. This allows the checkmate-checking logic to be simply encoded in the contract with guarantees of correct execution without ever having to execute the logic on chain.

# Comparisons to Other Layer 2 Solutions

We believe Arbitrum holds some important advantages over other layer 2 systems.

Unlike Plasma, Arbitrum supports arbitrary smart contracts and doesn’t require long waiting periods for sending and receiving funds with external contracts.

Unlike State Channels, Arbitrum allows non-unanimous progress and doesn’t force large amounts of contract code to be executed on-chain in the case of disputes.

Unlike TrueBit, Arbitrum VMs are stateful smart contracts as opposed to stateless oracles. Furthermore, Arbitrum execution costs are constant rather than metered and independent of the amount of storage and code. Finally, Arbitrum does not require contract code to be public.

I’d welcome any questions or discussion here.

## Replies

**ameensol** (2018-10-17):

Will the VM / bisection code be open source?

---

**kladkogex** (2018-10-17):

VM execution is actually not a bottleneck of ETH.  The bottleneck is consensus.  VM itself can be driven to 100,000+ transactions per second, you could do things like JIT, opportunistic parallel execution of transaction, and many other things.

You are not going to be competing with Plasma, since Plasma does accelerate consensus, which is the real bottleneck and the real problem that needs to be solved.  Plasma does it by essentially placing the consensus on a single operator, where it can be done extremely fast.

---

**hkalodner** (2018-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/ameensol/48/1455_2.png) ameensol:

> Will the VM / bisection code be open source?

Our code is still under development, but once it’s in a more polished state, it’ll all be open-sourced.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> VM execution is actually not a bottleneck of ETH.  The bottleneck is consensus. VM itself can be driven to 100,000+ transactions per second, you could do things like JIT, opportunistic parallel execution of transaction, and many other things.
>
>
> You are not going to be competing with Plasma, since Plasma does accelerate consensus, which is the real bottleneck and the real problem that needs to be solved.  Plasma does it by essentially placing the consensus on a single operator, where it can be done extremely fast.

First I’ll expand on how I see Arbitrum compared to Plasma-based constructions. Then I’ll talk a little more broadly on why I don’t think that layer 1 scaling can’t solve the problem of smart contract scalability alone.

Plasma hasn’t been able to support arbitrary smart contracts like Ethereum’s base layer. This might change in the future, but current near-to-market Plasma designs seem focused on money transfer (which they’re awesome for). Fundamentally the exit mechanism requirements seem to require each item on the Plasma chain to have a specific owner, which doesn’t make sense for many types of smart contracts.

Further, how a layer 2 solutions works in the case of a dispute or dishonesty is an extremely important question. Arbitrum handles disputes cheaply and at low cost without significant load on the main chain. Plasma works well in the optimistic case, but mass-exit scenarios can cause serious issues which limits the applicability of Plasma-based constructions.

Finally, the any-trust property which Arbitrum ensures substantially reduces data-availability problems. Since we assume that at least one manager must be honest at any given time, all we need to do is make sure that all the managers have all data which is fairly simple to achieve.

Next my general comments about Arbitrum in relation to base layer computational scaling:

- In a non-sharded proof-of-work based Blockchain where longer block execution times has been shown to lead to a higher orphan rate, execution does act as a bottleneck. I expect complex execution to continue to be inefficient on-chain even in future systems.
- When a VM’s managers are able to reach unanimous consensus over its actions, only actions which modify external state (sending or receiving tokens from external parties) must go on chain. All other communication and actions can take place off-chain with on-chain transactions available in the case of a censorship attack by a manager. This does reduce the load on consensus significantly in the optimistic case, much like state channels.
- If you and I are playing a game of chess, it’s highly beneficial for to ensure that no one other than you or I have to execute the code of our chess game (while maintaining security of course). This improves efficiency, but also provides our contract with privacy from the rest of the chain.
- Arbitrum VMs are also capable of storing an arbitrary amount of state and thus work for applications that base contract logic on substantial amounts of data. A global Blockchain has a clear incentive to not allow VMs to store multiple GBs of data on-chain, whereas a single VM’s managers may be happy to do so for that VM.

---

**kladkogex** (2018-10-17):

IMHO it would be nice if you provide a tldr explaining how does the system actually work and whats the difference between it and Truebit. Many people know how truebit works, more or less.

Ethereum or other blockchains first do consensus to order messages and then run EVM on the ordered chain.  Once the chain exists, running EVM on it is more or less straightforward.

It is not clear me from reading the paper how does the consensus work. You are saying that one can use any consensus, without giving much of detail.  Then you are saying that you are addressing limitations of ETH and Plasma, but this may be considered by people as comparing apples to oranges, since both ETH and Plasma do include consensus in some form.  By consensus I mean creation of a chain of transactions with global ordering.

In particular, the statement from the paper “We present Arbitrum, a cryptocurrency system that supports smart contracts without the scalability and privacy limitations of previous systems such as Ethereum.” is a bit hard to grasp …

|If seems from the paper that the proposed solution should be compared to Truebit and not to Ethereum. Ethereum is a system that includes both consensus and smart contract execution,  while what is described in the paper seems to be VM only and many of the scalability limitations of previous systems come from the consensus …

---

**hkalodner** (2018-10-17):

Sorry, maybe I wasn’t clear enough in my original post. It was an attempt of a tldr on the 18 page conference paper, but it obviously still ended up fairly long.

Here’s my attempt at a shorter high level description. Arbitrum allows you to write code for a smart contract, select a set of managers to run the code (potentially yourself and a friend for a smart contract involving just the two of you), post a commitment to the machine on-chain, and execute the contract off-chain guaranteeing correctness if any single manager is honest.

You can say running the EVM on ordered messages is straightforward, but at least today the gas limit is a massive limit on how much a single smart contract can do.

The general Arbitrum protocol was designed as consensus independent, but our deployment of Arbitrum on Ethereum is a layer 2 system where the “Verifier” described in the paper is a Ethereum smart contract. All Arbitrum VM’s will live inside that same single Ethereum smart contract. Arbitrum VMs can advance via a state-channel-like mechanism assuming there is unanimous agreement between the managers so not all transactions involving them must be put on chain. All on-chain operations described in the paper are transactions submitted to the Ethereum verifier smart contract, but none of these will actually execute VM code which all happens off-chain.

Arbitrum provides an environment where smart contracts / VMs are entirely defined inside the Arbitrum verifier smart contract. The only data related to a VM that is stored by the verifier smart contract is metadata about the VM, not code or state. The VMs can manipulate ERC20 and ERC721 tokens providing them a great deal of interoperability with contracts defined in Ethereum’s base layer.

We use a similar bisection protocol to TrueBit, but our VM architecture and thus proof system is substantially more efficient than WASM. The rest of our protocol is also totally different then TrueBit’s. TrueBit attempts to be a trustless global stateless computational oracle. Arbitrum allows for the creation of stateful smart contracts where each smart contract has a set of managers chosen by the VM’s creator. Arbitrum doesn’t attempt to provide global correctness through incentivized verifiers. Instead Arbitrum assumes that the managers have external incentives for executing a smart contract and that users of the contract will trust at least one of the managers. In targeting this slightly weaker trust property, we achieve much greater scalability and privacy.

---

**ldct** (2018-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/hkalodner/48/2466_2.png) hkalodner:

> Arbitrum guarantees that any single honest manager can ensure that the VM executes correctly (even if all of the other managers conspire to try to cheat).
>
>
> Arbitrum gives the managers of a VM incentives to agree on what the VM will do, and if the managers agree unanimously on what the VM will do, the system accepts that and it is recorded on-chain.

This seems to be a security assumption very different from those that other layer-2 designs (state channels, plasma, truebit) use, a point which is omitted from the “comparisons” section.

---

**cryptid11** (2018-11-08):

What new opcodes are needed to use Bitcoin as the consensus layer? Is this feasible in practice?

---

**derekchiang** (2018-11-08):

[@hkalodner](/u/hkalodner) sorry about the somewhat negative (but constructive) responses in this thread!  I think Arbitrum is solving a very important problem which is verifiable off-chain execution of smart contracts.  Would certainly love to see the system come to fruition.

I’m trying to better understand Arbitrum’s security model.  Specifically, am I right in understanding that if all managers are dishonest, then arbitrary state can be notarized on-chain?  If I’m a user of an Arbitrum smart contract (but not a manager), is there any way for me to challenge/exit state, if all managers are corrupted?

Also, is there any built-in mechanism in the system for selecting managers?  If I’m an Arbitrum developer, ideally I wouldn’t want to worry about picking my own managers.

---

**hkalodner** (2018-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptid11/48/2613_2.png) cryptid11:

> What new opcodes are needed to use Bitcoin as the consensus layer? Is this feasible in practice?

I haven’t spent a ton of time thinking about the minimal capabilities of a layer 1 to support Arbitrum. It doesn’t require the full power of the EVM, for instance I’m pretty sure it doesn’t require Turing completeness and could be implemented without any gas model, but there is a significant amount of complexity required like the verification of one-step-proofs and the tracking of VM related metadata (In short there’s some pretty complex smart contracts the go into the Ethereum implementation that don’t map to Bitcoin very well).

One of the long term research projects I want to work on would be specifying a minimum set of capabilities of a UTXO based blockchain for supporting Arbitrum. Way before that though, the goal is to actually get something usable on Ethereum

![](https://ethresear.ch/user_avatar/ethresear.ch/derekchiang/48/1342_2.png) derekchiang:

> @hkalodner sorry about the somewhat negative (but constructive) responses in this thread! I think Arbitrum is solving a very important problem which is verifiable off-chain execution of smart contracts. Would certainly love to see the system come to fruition.
>
>
> I’m trying to better understand Arbitrum’s security model. Specifically, am I right in understanding that if all managers are dishonest, then arbitrary state can be notarized on-chain? If I’m a user of an Arbitrum smart contract (but not a manager), is there any way for me to challenge/exit state, if all managers are corrupted?
>
>
> Also, is there any built-in mechanism in the system for selecting managers? If I’m an Arbitrum developer, ideally I wouldn’t want to worry about picking my own managers.

Thanks for the kind words! I’m happy to get both positive and negative feedback. It all goes into building a platform that people will want to use.

You’re totally correct, if all managers are dishonest, they can do anything with the VM. If you are a manager of an Arbitrum VM, there’s no further trust assumptions added on top of the base layer, similar to state channels and plasma. If you’re not a manager, you have to rely on an anytrust assumption, that a single manager will remain honest and force the machine to execute correctly.

The current Arbitrum specification doesn’t provide any guidance on choosing managers. The creator of an Arbitrum VM gets to specify the manager set themself. If there are only a fixed set of participants, this is trivial since you just make them all managers. If the contract is open, then you face the (potentially difficult) issue of selecting managers that everyone will trust. We assume that the managers are incentived by the VM itself, for instance the VM might choose to charge users a fee which gets paid to the managers or the players of a game would want to ensure that others players don’t cheat. However these incentives aren’t built into into the core of the protocol.

I imagine that when the Arbitrum ecosystem is thriving, there will be many organizations who will advertise their services as Arbitrum managers. This can be done fairly safely since your VM is secure as long as they don’t all collude so adding malicious managers does nothing to decrease security.

Essentially what you get with Arbitrum is super efficient, off-chain (even in a dispute) smart contracts with the cost of requiring the anytrust property if you’re not a manager (about the smallest additional trust assumption you can add on top of Ethereum).

---

**derekchiang** (2018-11-08):

Thanks for the detailed reply.  I think there’s the potential to build a mechanism wherein a random beacon is used to randomly select a set of managers for any given Arbitrum contract.  Combining random selection with the anytrust property can yield a very high degree of security, I think.  But yeah, I agree that that doesn’t have to be part of the core protocol.

---

**hkalodner** (2018-11-09):

I’m really happy to have a discussion about this stuff! Everything here is still super under development and we’re still figuring out the optimal way to use this stuff.

To a large degree, Arbitrum relies on fairly static sets of managers for each VM. VMs are stateful and data availability is only guaranteed for the current set of managers. Because of that, everything is a lot simpler if there’s just a static group of managers. A VM can programmatically alter its own set of managers, and it would certainly be interesting to think about various ways a VM might want to do that.

TrueBit operates in a way where verifiers can be selected fairly randomly (this is definitely skipping over some details). Verifiers have no direct interest in verifying a piece of computation other than an incentive provided by the protocol and that introduces a lot of complexity. In this setup a lot could go wrong if incentives aren’t perfectly aligned since if the protocol-provided incentive breaks, no one will verify a piece of computation.

An important part of Arbitrum’s concept, is that managers are generally people/entities that want to see the VM operate successfully. It’s a hopefully fairly diverse set of parties who people can trust won’t all collude. They’re incentivized by the fact that they want to see the VM run successfully, either because they’re participants in the VM itself, or because they’re earning money from the successful operation of the VM.

I can’t think of any way to use random selection with managers in Arbitrum given these constraints, but it’s a really general protocol so there could totally be some way to do this for a particular VM given that a VM can modify its own manager set. One of my favorite things about Arbitrum is that you can potentially have different VMs implemented totally differently ways (with different VM architectures and different dispute resolution mechanisms) that can all interact with each other.

---

**hellolyf** (2018-11-15):

Hello, I read your paper and I have a question.Where are smart contracts stored?Or is it stored in the state tree like in ethereum?In Arbitrum, if user wants to call a function  that changes the value of X in  smart contract, how does AVM store the X?

---

**hkalodner** (2018-11-15):

The VM code is stored totally offline. Only a commitment to the full state of the machine (including the code) appears on-chain. Rather than having direct function calls, Arbitrum uses an asynchronous messaging system. A user tells the machine that it is calling the function `f` (through an ABI similar to Ethereum). Then the next time the state of the VM is advanced by a manager, the machine will receive all messages since the last time the VM was advanced and trigger the execution `f()` which will mutate the state.

Messages themselves can be sent in two ways. Managers can unanimously agree that their VM receives a certain message offline, or message data can be posted on-chain via a transaction which logs the calldata and stores a hash of the message.

One consequence of this model is there’s no way to synchronously query the state of a VM from another VM. All you can do is send the VM a message requesting information and then wait for it to reply. Thus calls between VMs are possible, but can have significant latency.

---

**hellolyf** (2018-11-16):

Thank you very much.

---

**cryptid11** (2019-02-15):

any news?

is the project still alive?

---

**jasonzhouu** (2019-04-10):

Congrats that OffchainLabs receives funds. I have some questions.

![](https://ethresear.ch/user_avatar/ethresear.ch/hkalodner/48/2466_2.png) hkalodner:

> fairly static sets of managers

- How many managers, generally?
- Assume that all managers are honest, how do they come to the consensus about the current state before executed it? Actually, I think this is where the bottleneck exists.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The bottleneck is consensus.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Plasma does accelerate consensus, which is the real bottleneck and the real problem that needs to be solved.

I think the consensus [@kladkogex](/u/kladkogex) described is the “consensus between managers”.

![](https://ethresear.ch/user_avatar/ethresear.ch/hkalodner/48/2466_2.png) hkalodner:

> The general Arbitrum protocol was designed as consensus independent

While the consensus [@hkalodner](/u/hkalodner)  described is the “consensus of Blockchain”.

Although Arbitrum protocol is consensus independent, Arbitrum mangers still need some consensus between them.

---

**Econymous** (2019-06-05):

I’d also like to know. because smart contracts are crucial for my scaling solution.

I’ve figured out stabilizing consensus at lower & lower levels with near 0 security reduction.

I’m using a economic forces to enforce distribution of the p.o.s. staking token.

for example (rough idea) a $500 contract can be secured against a $50,000 whale

here’s my [trail of research](https://ethresear.ch/t/transferring-tokens-from-mainchain-to-sidechain/5540).

I thought so much of this infrastructure was already available & I was aware of these challenges, but i just through the infrastructure was already available.

---

**hkalodner** (2019-11-01):

It’s wild that it’s been a year since this post. We’ve been blogging and publishing code for a while now, but I thought it’d make sense to come back here and share some of the biggest updates.

**We’ve got code**. Around June of this year we published our alpha and we’ve gone through a couple version upgrades since then (https://github.com/OffchainLabs/arbitrum). It’s still in alpha, but it’s usable for local testing and we’ll be pushing forward to testnet soon.

**We’re expanding our vision.** In the description of Arbitrum above, I talked about a VM with managers (which we now call validators), but I didn’t go into who they were. We now view Arbitrum as supporting a number of different modes all based on the same technology:

- Arbitrum Channels: This was our main vision of Arbitrum described above and the most efficient offchain construction we’ve developed. Here we operate in a standard state channel setup, with a fixed set of participants who each ensure the correctness of the contract. This construction solves solves a bunch of problems that standard state channels have:

Stronger availability: If one participant in a standard state channel goes offline, offchain progress halts. Arbitrum channels keep working even with participant unavailability.
- Better privacy: Since disputes require posting the full contract state, you can’t rely on standard state channels to keep their state private. Due to Arbitrum’s bisection protocol, we can avoid revealing the state of a contract on-chain, even in the case of a dispute.
- Higher computational and storage capacity: Standard state channel based contracts are limited by the fact that you need to be able to post the full state on chain and execute a state transition within the gas limit. Arbitrum’s bisection-based dispute protocol removes these limits, since bisection transactions have a fixed cost, independent of the complexity of the offchain contract.
- Simpler application development: To use a standard state channel you have to write your application as a state machine with a set of valid state transitions which is much more complicated than standard solidity development. Arbitrum instead supports running standard solidity contracts.

Arbitrum Sidechains: The same construction we describe as Arbitrum Channels, can also be used to build extremely secure sidechains that have an AnyTrust guarantee. This means that as long as a single validator is honest, the side chain will function correctly. This provides a much higher level of security than standard sidechains which depend on independent consensus systems and honesty assumptions. As an example, BFT-based systems require two-thirds of validators to be honest; Arbitrum requires just one honest validator.

Arbitrum Rollup: Inspired by Optimistic Rollup, we’ve separated out the subset of Arbitrum that provides the same type of functionality. Our original description of Arbitrum made large optimizations based around the idea of a fixed validator set, but we can remove this and still have a highly efficient system. Rather than having a fixed set of validators who can accept transactions offchain, we instead force all transaction data on-chain, allowing anyone to assert or challenge. Advantages compared to Optimistic Rollup are:

- Simpler application development: To use optimistic rollup today, you have to write a lot of very custom code (https://github.com/plasma-group/pigi/blob/42f2c3cca4cb0bd5fdbfbe14a8575ef65126b3cc/packages/contracts/contracts/UnipigTransitionEvaluator.sol). Arbitrum supports deploying standard solidity contracts on rollup which makes the technology easily accessible to all developers.
- Higher computational and storage capacity: Optimistic Rollup’s fraud proofs depend on evaluating entire transactions on Ethereum, and thus the transaction’s computation and storage use must fall within the gas limit. Arbitrum doesn’t limit transaction complexity, so you can use much more computation and storage than the gas limit would allow.

So you can see we’ve been pretty busy building out Arbitrum. We’ve made a lot of progress in the last year, and we’re getting quite close to being ready for Testnet launch. For the adventurous people out there, there are instructions on our github about how you can use Arbitrum today.

