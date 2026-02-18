---
source: ethresearch
topic_id: 23998
title: Synchronous Composability Between Rollups via Realtime Proving
author: jbaylina
date: "2026-02-02"
category: Layer 2
tags: [cross-shard]
url: https://ethresear.ch/t/synchronous-composability-between-rollups-via-realtime-proving/23998
views: 1388
likes: 33
posts_count: 20
---

# Synchronous Composability Between Rollups via Realtime Proving

# Synchronous Composability Between Rollups via Realtime Proving

## 1. Based Rollups and Realtime Proving

A based rollup is a rollup where anyone can propose a new block, there is no privileged sequencer. Any participant can take the current state of the rollup, apply a set of transactions, and produce a new block.

A key design advantage emerges when we require that the data availability payload and the validity proof are submitted together, as a single atomic unit. In traditional rollup designs, data is posted first and the proof comes later, which introduces a gap that complicates the incentive design: who generates the proof? When? How do you ensure they are compensated fairly and promptly?

By posting data and proof simultaneously, we collapse this gap entirely. The block proposer is responsible for both execution and proving. If the proof is invalid or missing, the block simply does not exist. This dramatically simplifies the incentive mechanism, the block proposer is the prover, and their reward comes from the same source (e.g., transaction fees) without the need for separate proof markets or challenge periods.

This is made possible by **realtime proving** , the ability to generate validity proofs fast enough that they can be produced alongside block construction, rather than as an asynchronous afterthought.

Realtime proving is rapidly becoming practical. As of today, proving a full Ethereum block requires around 12 GPUs with an average proving time of ~7 seconds. There is still significant margin to improve and push latencies lower, both through hardware improvements and proving system optimizations, though it is difficult to predict exactly where the limit will be. Prover centralization is a valid concern: the hardware requirements are non-trivial, and not every block builder will have access to the same proving infrastructure. However, proving is inherently parallelizable and commoditizable, and the trend is clearly toward faster proofs on cheaper hardware.

## 2. What Is Synchronous Composability?

Synchronous composability means that within a single transaction, a smart contract on one chain (L1 or a rollup) can **CALL** a smart contract on a different chain (L1 or another rollup) and receive the result back in the same execution context, just as if both contracts lived on the same chain.

Today, cross-chain interactions are asynchronous: you send a message on chain A, wait for it to be relayed to chain B, and then separately handle the result. This breaks the composability model that makes Ethereum’s DeFi ecosystem so powerful. Protocols cannot atomically compose across rollup boundaries.

Synchronous composability restores this. From the developer’s perspective, calling a contract on another rollup looks and behaves exactly like calling a contract on the same chain. The transaction either succeeds atomically across all involved chains, or it reverts entirely.

## 3. The Simple Case: L2-to-L2 Composability

Before tackling the harder problem of L1↔L2 interaction, it is worth noting that composability between L2 rollups alone is relatively straightforward.

If we are only dealing with L2s, we can bundle the data availability for all affected rollups into a single blob. The block builder constructs a combined execution that touches multiple rollup states, proves them all together, and posts the result as one atomic data availability submission. Since all affected state transitions are proven and posted together, composability follows naturally, the transitions either all happen or none of them do.

This observation is the foundation. The harder problem is making this work when L1 smart contracts are part of the interaction.

## 4. Proxy Smart Contracts

The core mechanism that enables cross-chain calls is the **proxy smart contract**. A proxy is a smart contract deployed on one chain that represents a smart contract living on a different chain.

When a contract on L1 wants to call a contract on rollup R, it does not somehow execute code on R directly. Instead, it calls the proxy of that R contract, which exists on L1. The proxy contract encapsulates the cross-chain call: it knows what the target contract is, it processes the call, applies the corresponding state changes on the rollup, and returns the result, all within the same transaction execution.

From the caller’s perspective, interacting with the proxy is indistinguishable from interacting with the real contract. The proxy is the local interface to a remote contract.

## 5. L1 ↔ L2 Interaction Model

When a transaction involves both L1 and L2 smart contracts, the execution follows a structured process:

### Step 1: Ensure Proxy Contracts Exist

Before execution, all proxy smart contracts for the L2 contracts that will interact with L1 must be deployed. If a contract on rollup R will be called from L1, its proxy must already exist on L1.

### Step 2: Build and Submit the Execution Table

An **execution table** is constructed and stored temporarily in the L1 state. This table is a sequence of entries, where each entry describes an action and its consequences. Each entry contains:

- Action: Primarily a CALL or a RESULT.
- A set of L2 state transitions: Which rollups are affected, and what their state roots transition from/to.
- nextAction: What comes next, either a RESULT (with return data) or another CALL (to a different L1 smart contract).

The table captures the full trace of cross-chain interactions. For example, consider a nested call scenario:

```auto
A (on L1) calls B (on Rollup 2)
  → B (on Rollup 2) calls C (on L1)
    → C (on L1) returns
  → B (on Rollup 2) returns
A (on L1) continues execution
```

In this case, the execution table would contain two entries:

```auto
| # | Action                | L2 State Transitions          | nextAction          |
|---|-----------------------|-------------------------------|---------------------|
| 1 | CALL B (on Rollup 2) -| Rup2: stateRoot₀ → stateRoot₁ | CALL C (on L1)      |
| 2 | RETURN from C (on L1) | Rup2: stateRoot₁ → stateRoot₂ | RETURN to A (on L1) |
```

The first entry says: “when A calls B on Rollup 2, the rollup transitions from stateRoot₀ to stateRoot₁, and the next thing that needs to happen is a call to C on L1.” The second entry says: “once C returns, Rollup 2 transitions from stateRoot₁ to stateRoot₂, and the final result is returned to A.”

The execution table encodes this entire call/return sequence, together with all the rollup state transitions that occur at each step. Crucially, the table is accompanied by **a single validity proof** that guarantees the correctness of every execution step in the table. This proof is verified once when the table is submitted.

### Step 3: L1 Execution with Proxy Resolution

Now L1 transactions execute normally. When execution reaches a point where an L1 contract calls a proxy contract, the proxy does the following:

1. Looks up the corresponding CALL action in the execution table.
2. Verifies and applies the state root changes for the affected rollups.
3. If there are nested L1 calls in the sequence, executes them.
4. Removes the consumed entries from the execution table (to avoid wasting L1 storage).
5. Returns the RESULT to the calling L1 contract.

From the L1 execution environment’s perspective, the call happened normally and returned a result. The complexity of the cross-chain interaction is entirely abstracted away by the proxy and the execution table.

### Step 4: L2-Initiated Transactions

A transaction originating on L2 that interacts with L1 follows the same model, but the first action in the execution table is an `L2TX` rather than a `CALL`. The L2 transaction kicks off execution, and any calls to L1 contracts become nested entries in the table, resolved in the same way.

### Step 5: Handling Reverts

Two special actions: `REVERT` and `REVERT_CONTINUE`  handle reverts across chain boundaries in a way that mirrors how reverts work within a single chain.

When a revert occurs during execution on L2, a `REVERT` action is sent to L1. L1 then processes the revert by undoing any nested L1 calls that were part of the reverted execution path and updating the affected rollup state roots accordingly. Once L1 has finished unwinding the reverted calls, a `REVERT_CONTINUE` action is sent back to L2, allowing execution to resume. The end result is that reverts work the same way they currently work within a single chain.

## 6. Additional Notes

### Account Abstraction and Incentive Alignment

Ensuring that proxy contracts are deployed and that incentives between the user and the block builder are properly aligned can be handled using existing Ethereum standards — specifically **EIP-7702** (set EOA account code) and **EIP-4337** (account abstraction). These standards provide the flexibility needed to coordinate the setup phase without requiring changes to the core protocol.

### Rollups Are Not Limited to the EVM

Rollups participating in this system do not need to be EVM-native. Any rollup that can accept and generate `CALL`s to other rollups can participate. Each rollup defines its own state transition function via a **zkVerification key**. A rollup could even have an owner with full control over its state root.

The only constraint the main system imposes is **Ether accountability**: the system must track how much Ether each rollup holds and must not allow a rollup to make a `CALL` with a value higher than its total Ether balance.

### Native Tokens and Value Transfers

Rollups can define their own native token. The only restriction is that the state transition function should not accept or make `CALL`s with a non-zero Ether value from or to an external rollup if the rollup uses a different native token. This prevents accounting mismatches between the rollup’s internal token and the Ether tracked by the L1 system.

### No L1 Fork Required

This entire mechanism can be implemented **without forking L1**. Everything operates through smart contracts deployed on the existing Ethereum network.

### Orthogonal to Preconfirmations

This proposal is fully orthogonal to preconfirmation mechanisms. It neither depends on nor conflicts with preconfirmations. In fact, it can benefit from L1 preconfirmations once they are available, as faster L1 finality would reduce the latency of cross-chain interactions.

### Reference Implementation

A first draft of how these smart contracts would work is available at: https://github.com/jbaylina/sync-rollups

## Replies

**thegaram33** (2026-02-02):

Great writeup! Synchronous composability is often discussed in abstract terms, it’s great to see a concrete design.

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> An execution table is constructed and stored temporarily in the L1 state.

If I understand it correctly, at a given L1 slot, the builder will produce both the L1 block and some number of L2 blocks on various rollups. First it simulates execution over multiple chains, then it inserts the execution table to the L1 proxies’ storage via a normal transaction (along with a proof) so that L1 nodes can re-play the state transition bundle without knowing the L2 states.

Does there need to be a similar execution table on the L2s? Otherwise, can a node from `rollupA` sync their chain without also syncing `rollupB`?

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> Since all affected state transitions are proven and posted together, composability follows naturally, the transitions either all happen or none of them do.

It’s clear that the shared sequencer can ensure atomicity, but how can it guarantee atomicity to the sender of the transaction? Is this part of the validity proof?

A related desirable guarantee is *non-interleaving* (or serializability). Does the sequencer define a single linear execution order, i.e. there can be no concurrent calls like `tx1: L1 –> L2, tx2: L2 –> L1`?

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> From the caller’s perspective, interacting with the proxy is indistinguishable from interacting with the real contract.

So L1 transactions that call a proxy can only be valid if they’re executed in the slot of a suitable shared sequencer. Would the proxy revert otherwise?

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> table is accompanied by a single validity proof that guarantees the correctness of every execution step in the table

The proof would rely on the actual L1 execution, i.e. it would be valid for the current slot but not necessarily for the next slot. Would the proxy somehow capture a digest of L1 execution and provide it as a public input?

---

**EugeRe** (2026-02-02):

That’s very nice. It could be a game changer with many use case that require in time data to ensure effective da on the market. I am interested to ask. How do you see it in more details playing out with Ethereum Interoperability Layer (EIL) ? I see you mentioned the proxy contracts to be harmonized with AA proposals either 7702 or 4337/7579 etc etc.. But also considering the roadmap for native implementation which is currently under discussion? .. I think this is crucial point from coordination perspective. But great work!

---

**Citrullin** (2026-02-02):

Good writeup overall.

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> Rollups can define their own native token. The only restriction is that the state transition function should not accept or make CALLs with a non-zero Ether value from or to an external rollup if the rollup uses a different native token. This prevents accounting mismatches between the rollup’s internal token and the Ether tracked by the L1 system.

Doesn’t the whole model break apart if they do? From a game theory incentive perspective. Shouldn’t be the native rollups always have to use ETH as native token? Also adds too much complexity for doing so. Makes it more important to see the business model of the DAO in order to make it work.

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> The core mechanism that enables cross-chain calls is the proxy smart contract. A proxy is a smart contract deployed on one chain that represents a smart contract living on a different chain

Thought about something like this too. There is this whole wasm/RISCV/MIPS debate going on. I am wondering, at that point. Couldn’t you make a whole abstraction layer at this point?

A meta-smart-contract ABI/API for cross-chain applications.

---

**fakedev9999** (2026-02-02):

Great post! Realtime proving seems to be the only missing piece.

---

**jbaylina** (2026-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/citrullin/48/22083_2.png) Citrullin:

> Doesn’t the whole model break apart if they do? From a game theory incentive perspective. Shouldn’t be the native rollups always have to use ETH as native token? Also adds too much complexity for doing so. Makes it more important to see the business model of the DAO in order to make it work.

I don’t think the model necessarily breaks. The main requirement is that per-rollup ETH accounting is properly enforced and verifiable. Beyond that, rollups can remain sovereign, with the trust model cleanly isolated per rollup.

In this setup, a rollup could behave maliciously, but the impact would be contained to users of that specific rollup and would not affect others. From a protocol perspective, this isolation is an explicit design choice rather than a flaw.

That said, I agree this is something that needs careful validation from an incentive and complexity standpoint. It’s reasonable that an initial or conservative version of the protocol restricts this to native rollups only, and later relaxes the constraint once the model is well understood.

![](https://ethresear.ch/user_avatar/ethresear.ch/citrullin/48/22083_2.png) Citrullin:

> Thought about something like this too. There is this whole wasm/RISCV/MIPS debate going on. I am wondering, at that point. Couldn’t you make a whole abstraction layer at this point?
> A meta-smart-contract ABI/API for cross-chain applications.

Yes, I think this is the right direction. Introducing an abstraction layer — a kind of meta smart-contract ABI/API — allows cross-chain applications to be defined independently of the execution model.

This naturally fits with **app-rollups**, where the state transition function does not need to be expressed in terms of a specific VM like EVM, RISC-V, or WASM. Instead, the STF itself becomes the first-class object, and can be any well-defined state transition function.

In this model, virtual machines are just one possible implementation choice, not a requirement. Interoperability happens at the level of the abstract STF interface, rather than at the VM instruction set.

---

**Citrullin** (2026-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/fakedev9999/48/22294_2.png) fakedev9999:

> Great post! Realtime proving seems to be the only missing piece.

Realtime Proving Bidding Markets sounds a lot like [decentralized realtime auctions](https://arxiv.org/html/2506.00282v1). There is probably a lot to take from Advertising.

---

**jbaylina** (2026-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> If I understand it correctly, at a given L1 slot, the builder will produce both the L1 block and some number of L2 blocks on various rollups. First it simulates execution over multiple chains, then it inserts the execution table to the L1 proxies’ storage via a normal transaction (along with a proof) so that L1 nodes can re-play the state transition bundle without knowing the L2 states.
>
>
> Does there need to be a similar execution table on the L2s? Otherwise, can a node from rollupA sync their chain without also syncing rollupB?

Yes, you’ve got it right.

For L2-to-L2 calls, a similar mechanism can be used as the one described for L1, although there may be more efficient designs. One possible approach is the following:

When a call is issued from L2A to L2B, the execution in L2A assumes a result for that call and commits to it by adding a hash of the assumed call (including its result) into a cryptographic accumulator. Later, when L2B processes that call, it produces the actual result and removes (or cancels) the corresponding entry from the accumulator.

At the end, all proofs can be composed into a single aggregated proof that enforces the invariant that the accumulator evaluates to zero. This guarantees that every assumed cross-rollup call has been correctly matched with its real execution, without requiring each rollup to track the full state of the others.

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> It’s clear that the shared sequencer can ensure atomicity, but how can it guarantee atomicity to the sender of the transaction? Is this part of the validity proof?
>
>
> A related desirable guarantee is non-interleaving (or serializability). Does the sequencer define a single linear execution order, i.e. there can be no concurrent calls like tx1: L1 –> L2, tx2: L2 –> L1?

The atomicity guarantee to the sender does not rely on trusting the sequencer’s “good behavior” alone. It is enforced by the protocol’s validity rules and checked as part of the proof.

The shared sequencer defines a single linear execution order across L1 and L2s for a given slot. Atomicity and non-interleaving (i.e. serializability) are properties of this ordered execution: a cross-domain transaction either fully succeeds in that linear order or is fully reverted. Concurrent interleavings such as `tx1: L1 → L2` and `tx2: L2 → L1` within the same slot are not allowed, because the sequencer commits to a total order.

From the user’s perspective, if the sequencer behaves incorrectly, the outcome is either that the proof is invalid or that the transaction simply reverts. In both cases, the user is not affected beyond the transaction not being included, while the sequencer bears the cost of the misbehavior through the protocol’s penalty mechanism.

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> So L1 transactions that call a proxy can only be valid if they’re executed in the slot of a suitable shared sequencer. Would the proxy revert otherwise?

Yes. If the call is not executed within a slot produced by the shared sequencer, the proxy call will revert.

More precisely, the shared sequencer can be **any participant and may change from block to block**. However, if a transaction is not executed through the shared sequencer logic for that slot, the execution table will be empty (or missing the required entry). In that case, the proxy detects the absence of a valid execution record and explicitly reverts, invalidating the full transaction.

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> The proof would rely on the actual L1 execution, i.e. it would be valid for the current slot but not necessarily for the next slot. Would the proxy somehow capture a digest of L1 execution and provide it as a public input?

The proof guarantees that all entries in the execution table are correct with respect to a specific initial L2 state.

When the execution table is consumed by the proxy, the initial L2 state (or its commitment) is verified first. Only if this state matches does the proxy apply the state transitions described in the table. This effectively binds the proof to a particular execution context, so the table is valid only for that state and slot.

As a result, the proof does not rely on replaying L1 execution itself, but on verifying that the state transitions encoded in the table are consistent with the committed initial state.

---

**jbaylina** (2026-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/eugere/48/16295_2.png) EugeRe:

> That’s very nice. It could be a game changer with many use case that require in time data to ensure effective da on the market. I am interested to ask. How do you see it in more details playing out with Ethereum Interoperability Layer (EIL) ? I see you mentioned the proxy contracts to be harmonized with AA proposals either 7702 or 4337/7579 etc etc.. But also considering the roadmap for native implementation which is currently under discussion? .. I think this is crucial point from coordination perspective. But great work!

I agree that coordination is crucial, and I think synchronous composability is a core building block for making the Ethereum Interoperability Layer work in practice.

One of the strengths of this proposal is that it can be fully developed and deployed **without requiring a hard fork at L1**. It works with today’s Ethereum by using proxy contracts and validity proofs, and can naturally integrate with account abstraction approaches such as 4337 or 7702/7579.

At the same time, this does not preclude a future native implementation. As the roadmap evolves, parts of this model could be absorbed into the protocol itself, reducing complexity and improving efficiency. In that sense, this approach can act both as a practical near-term solution and as a concrete blueprint for how native interoperability could eventually look.

---

**keyneom** (2026-02-02):

This is pretty similar to [Introduction - Spire](https://docs.spire.dev/pylon/) ‘s approach. You can see the proxy call made in their https://human.spire.dev demo here as if it were a call to a local chain contract which definitely improves the cross-chain devex: [self-pylon-demo/contracts/src/HumanNFT.sol at 6ccdcc1ec4e70e92b0b99e6f9e6cab45059b1dfa · spire-labs/self-pylon-demo · GitHub](https://github.com/spire-labs/self-pylon-demo/blob/6ccdcc1ec4e70e92b0b99e6f9e6cab45059b1dfa/contracts/src/HumanNFT.sol#L47)

---

**EugeRe** (2026-02-03):

I totally agree. In terms of use, I am picturing a scenario where this system for instance, can really benefit complex environments. Where business requirements need to be verified at once (maybe for selective disclosure). Think of complex investment operations, where policies and trade execution logic should be tied in the same finality to ensure reporting. This should be very powerful, especially for institutional environments. What do you think [@jbaylina](/u/jbaylina)  ?

---

**thegaram33** (2026-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> The proof guarantees that all entries in the execution table are correct with respect to a specific initial L2 state. […] This effectively binds the proof to a particular execution context, so the table is valid only for that state and slot.

I don’t see how that’s true.

The scenario I have in mind is: L2A calls to L1, which then calls to either L2B or L2C based on some L1 state.

The simulation that the proof is based on might call to L2B, but when it is actually submitted to L1 state is different so it calls to L2C.

You might say the call to L2C will fail because it has no corresponding entry in the execution table, but there might be similar scenarios (e.g. L1 either calls to L2B, or does not do anything).

Therefore, I think the proof must somehow commit to the L1 execution (or L1 pre-states) as well.

---

**jbaylina** (2026-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> I don’t see how that’s true.
>
>
> The scenario I have in mind is: L2A calls to L1, which then calls to either L2B or L2C based on some L1 state.
>
>
> The simulation that the proof is based on might call to L2B, but when it is actually submitted to L1 state is different so it calls to L2C.
>
>
> You might say the call to L2C will fail because it has no corresponding entry in the execution table, but there might be similar scenarios (e.g. L1 either calls to L2B, or does not do anything).
>
>
> Therefore, I think the proof must somehow commit to the L1 execution (or L1 pre-states) as well.

The important point is **who performs the simulation and generates the execution table**.

In the intended design, the simulation and the corresponding proof generation are done by the **block builder**, who already knows the exact L1 state the transaction will be executed against (or, equivalently, there is some form of pre-commitment to that L1 state).

In that case, there is no ambiguity: the L1 execution path (e.g. whether L1 calls L2B or L2C, or does nothing) is fixed at simulation time, and the execution table contains exactly the state transitions that correspond to that concrete execution.

Even if we consider a weaker model where a sequencer submits a transaction without knowing the final L1 state, correctness is still preserved. If the actual L1 execution diverges from what was simulated:

- if L1 attempts to execute a call for which no matching entry exists in the execution table, the transaction simply fails;
- if L1 follows a different branch (for example, it does nothing), the execution table entries corresponding to the simulated call are never applied.

In all cases, proofs are not “included” or “rejected”: they only attest that certain state transitions are valid. Those transitions are applied if and only if the corresponding execution step is actually reached; otherwise, the transaction fails or the entries are unused.

---

**thegaram33** (2026-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> Those transitions are applied if and only if the corresponding execution step is actually reached; otherwise, the transaction fails or the entries are unused.

Yeah, I think I see your point. We do not need to commit to a specific execution path on L1, simulated and actual execution on L1 can diverge:

1. It is enough if the actual L1 execution is compatible with the simulated one: different execution path and state updates on L1, but exactly the same interactions (calls, arguments) with L2s.
2. It is also acceptable if the actual execution is some subset of the simulated one, as in the above example.

We already committed to the cross-domain call arguments as part of the validity proof. If the arguments change (e.g. `RETURN from C (on L1)` in your example returns a different value), then the `actionHash` will change and execution will fail.

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> if L1 follows a different branch (for example, it does nothing), the execution table entries corresponding to the simulated call are never applied.

Just two nuances to consider:

1. If a rollup state update is skipped and there are subsequent calls from/to the same rollup, then the whole transaction will fail (missing entry in execution table).
2. Skipped execution table entries should not be used in subsequent blocks. Maybe storing them in transient storage would be most suitable? Or hashing in a way that they’re only valid in the current block.

---

**jbaylina** (2026-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> If a rollup state update is skipped and there are subsequent calls from/to the same rollup, then the whole transaction will fail (missing entry in execution table).
> Skipped execution table entries should not be used in subsequent blocks. Maybe storing them in transient storage would be most suitable? Or hashing in a way that they’re only valid in the current block.

In this model you still need to compute the new `stateRoot`, and it will **definitely change** if the rollup state changes. So I don’t think that storing a partial state change really helps.

---

**thegaram33** (2026-02-03):

To be clear, I was just considering whether the block builder can post an inconsistent update, by mistake or malicious intent. It seems the answer is no, with the caveats in my previous message.

---

**ed** (2026-02-03):

Lovely writeup!  I’m curious how you feel this compares to a mailbox-based approach such as [CIRC](https://hackmd.io/@EspressoSystems/HyiHI5RUbl/edit) or SCOPE.  Fundamentally, the two designs are variants of the same theme.  The execution table could be viewed as a version of a mailbox.  To me, it seems the main difference is that this approach requires proxy contracts for each contract on another chain, whereas a mailbox approach only requires a single mailbox contract.

---

**mkoeppelmann** (2026-02-03):

To make things a bit more plastic - here a screen recording of an early POC.

It demonstrats synchronous calls that write e.g. into L1 from L2 and even are able to continously run more code on the L2 with the return value.


      ![](https://ethresear.ch/uploads/default/original/3X/3/4/34f15c3347d13398c0832a1a13539f72db6559b0.png)

      [Descript](https://share.descript.com/view/5jFVPqFNCNO)



    ![](https://ethresear.ch/uploads/default/optimized/3X/e/5/e5af4da64fef9ac6700ba7de6413e6d6c4042318_2_690x388.jpeg)

###




Okay. I want to share some recent work about synchronous composable roll-ups, roll-ups, that you can, where you can interact with the contracts that live on them,  natively from the L one as if they










POC repo:



      [github.com](https://github.com/koeppelmann/synchronous_surge)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/d/d/dda27d414db7700afb1743c5c0445e4c136f8b1b_2_690x344.png)



###



Contribute to koeppelmann/synchronous_surge development by creating an account on GitHub.

---

**tbrannt** (2026-02-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/jbaylina/48/2448_2.png) jbaylina:

> A based rollup is a rollup where anyone can propose a new block

I generally wonder, with a based rollup design where anyone can submit a block with the data availability payload and the validity together:

Would that make DOSing the rollup possible?

Couldn’t someone just keep adding 1 transaction blocks (with only their own transaction) and always be the first to calculate the next block because they had a few seconds head start in calculating the next block as they already knew the content of the previous block (their own) before it was published on ethereum L1?

---

**jbaylina** (2026-02-04):

May be, anybody is too much. I’d say any block-builder/validator…

