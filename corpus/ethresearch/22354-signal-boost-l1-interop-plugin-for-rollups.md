---
source: ethresearch
topic_id: 22354
title: "Signal-Boost: L1 Interop Plugin for Rollups"
author: jvranek
date: "2025-05-15"
category: Layer 2
tags: [based-sequencing]
url: https://ethresear.ch/t/signal-boost-l1-interop-plugin-for-rollups/22354
views: 854
likes: 13
posts_count: 1
---

# Signal-Boost: L1 Interop Plugin for Rollups

*Research by the team focused on [Fabric](https://x.com/fabric_ethereum) and [Commit-Boost](https://x.com/Commit_Boost). Thanks to individual(s) across EF Research, Nethermind, Espresso, Taiko, OpenZeppelin, Spire, ETHGas, Gattaca, L2Beat, Labrys, Luban, Puffer, and Interstate for feedback, contributions, and review. Feedback, contributions, and review does not mean endorsement.*

[![image](https://ethresear.ch/uploads/default/optimized/3X/e/9/e909ff81cd1939c591b3d7a2ecfaf7c13cec1e3f_2_375x375.jpeg)image1024×1024 42.1 KB](https://ethresear.ch/uploads/default/e909ff81cd1939c591b3d7a2ecfaf7c13cec1e3f)

## TL;DR

- Ultra Transactions, proposed by Gwyneth, introduce a powerful design for achieving synchronous composability between the L1 and based rollups by leveraging top-of-block (ToB) L1 transaction execution, clever cross-domain context switching, and real-time proving.
- Same-Slot Message Passing, proposed by Nethermind, enables L1→L2 communication within a single slot via messenger contracts, laying the groundwork for atomic L1<>L2 transactions.
- Signal-Boost combines insights from both approaches to offer flexible L1 synchronous composability to existing rollups, with minimal or no changes to their stacks.
- This allows Ethereum to offer utility to existing rollups today, while also providing a path toward becoming based as the based rollup ecosystem continues to mature.
- This would require no in-protocol changes for Ethereum, rather it would leverage the PBS pipeline, Commit-Boost, and the Constraints / Commitments APIs.
- Last, we note that rollups which choose to become based can still unlock additional benefits from Ethereum beyond what Signal-Boost provides.
- A ~100 line of code PoC implementation can be found here.

## Motivation

- Fragmentation remains one of the core challenges facing the rollup-centric roadmap.
- It has captured the attention of the industry, leading to multiple parallel efforts aimed at improving interoperability. These can broadly be categorized as approaches for achieving either asynchronous or synchronous interoperability, including intents, shared bridges, shared sequencing, based sequencing, and real-time proving.
- Among these, synchronous composability (”SC”) stands out as the most compelling solution, as it allows rollups to read and react to each other’s current state during execution atomically and within the same slot height, enabling users and applications to interact across chains with the feeling of a single unified chain.
- With real-time proving on the horizon, Ethereum will soon have all the prereqs in place for L1 SC.
- SC is typically associated with shared sequencing, where a common sequencer with a write-lock over multiple rollup domains can guarantee coordination between them. Since only the L1 proposer has a write-lock over Ethereum, SC involving the L1 is generally reserved for based rollups that use the L1 proposer as their L2 sequencer. While based rollups are coming to market, they are still early and represent a small portion of the ecosystem. In the meantime, existing rollups remain siloed from the L1, making it necessary to rely on asynchronous interoperability solutions that come with UX and DevEx tradeoffs.
- Migrating an existing rollup to support based sequencing can be seen as a win-win. Ethereum benefits from reduced fragmentation and stronger network effects, while rollups gain access to L1 users and liquidity with a snappier UX.
- Despite these benefits, there are reasons rollups haven’t yet adopted based sequencing: potential UX regressions without a “skin-in-the-game” sequencer, forfeited L2 MEV revenue, immature tech like real-time proving, and the cost and complexity of modifying their stacks.
- Fabric is working with the community on two goals: 1) creating a path for existing rollups to become based, and 2) making it easier for new based rollups to launch.
- With the first goal in mind, we began asking: Can we decouple SC from based sequencing, and can we do so in a way that not only works today but also creates a cleaner path to becoming based in the future?
- Nethermind’s work on Same-Slot Message Passing already showed that meaningful coordination between L1 and L2 is possible without fully shifting sequencing to the L1 proposer. What remains underexplored is how to extend this insight to existing rollups in a way that minimizes friction.
- We propose Signal-Boost to provide a pathway for existing rollups to achieve on-demand SC with the L1, without requiring them to become based. This allows Ethereum to offer a valuable coordination service now, while still paving the way toward a based future.
- Our hope is that this approach lets rollups have their cake and eat it too by accessing SC without overhauling their stacks. It is not a replacement for based rollups, but a complementary step forward that helps Ethereum engage a broader part of the market while the based ecosystem continues to mature.

## Background

###

Nethermind’s research enables same-slot L1→L2 messaging via paired messenger contracts on both chains. This allows rollups to react to *some* L1 actions, such as L2 deposits, within the same slot. This is sufficient to enable synchronous and atomic cross-chain bundles “such as depositing ETH from L1, swapping it for USDC on L2, and withdrawing back to L1.”

Importantly, they reached a key insight that the “L2 proposer does not have to be the L1 builder.” This means that these interactions do not require based sequencing, rather some level of coordination between the L2 and L1.

However, it has one main limitation: the L2 cannot read arbitrary L1 state, only what’s been written to the L1 messenger contract.

###

Proposed by Gwyneth, Ultra transactions enable SC between the L1 and based rollups.

- They bundle L1 and L2 transactions into a single massive, atomic L1 transaction (constructed via account abstraction by a “master builder”) that is always inserted at the top of the block (ToB) to guarantee a clean execution starting from the latest L1 state.
- A proposed XCALLOPTIONS precompile enables seamless cross-domain calls, including the ability to simulate and execute L1 “meta-transactions” within L2 domains, enabling synchronous L1->L2 calls.
- A large proof accompanies the bundle, validating all L2 state transitions and meta transaction executions.
- This construction allows L1 and rollups to synchronously read state and call contracts across each other’s domains.

Two key insights from the Ultra transaction model are:

1. ToB execution is necessary to ensure all state transitions begin from a known, clean L1 state
2. Account abstraction is a powerful primitive for batching cross-domain transactions.

### Push vs Pull Semantics for L1→L2 Messaging

Same-slot message passing is inherently *push-based*: the L1 must explicitly write data to a `SignalService` contract for the L2 to read it in the same slot. By contrast, ToB execution enables *pull-based* access, where the L2 can synchronously read arbitrary L1 state — but only at the very start of the block, limiting use cases.

Until proposals like [EIP-7814](https://github.com/ethereum/EIPs/blob/1676c9451a75fd0740c65e7d1d5f18296d68a9a0/EIPS/eip-7814.md) are live or stack overhauls are made to support L1 meta transactions, push-based signaling is the best way to access current L1 data during mid-block execution.

###

SC with the L1 requires rollups to read unconfirmed L1 state as opposed to confirmed or finalized state. Rollups who build their state from unfinalized L1 data are subject to L1 reorg risk, where previously consumed L1 inputs may cease to exist, causing dependent L2 state to mutate which they must either accept or choose to rollback the rollup’s state.

To mitigate this, most rollups deliberately lag behind the L1 head. For example, the OP Stack uses a `SequencerConfDepth` of 4 blocks, while others wait until L1 finalization. This buffer helps L1 inputs stabilize before consumption, enabling rollups to offer more credible preconfirmations. However, *introducing any lag is fundamentally incompatible with L1 SC*.

This is not necessarily a binary decision but a spectrum:

- More L1 coupling = better interop, higher reorg risk
- More L1 decoupling = worse interop, less reorg risk

Signal-Boost aims for the middle of this spectrum, to allow for SC on-demand when the L1 reorg risk is sensible but default to the lower-risk option.

## Signal-Boost Overview

Our goal is for L2s to ingest and react to L1 state in real time. Same-slot messaging enables this by allowing data written on L1 to be consumed by L2s within the same L1 slot. But this only works for L1 data that is explicitly written to the `SignalService` contract.

This creates a key limitation: protocols like Chainlink or Uniswap would need to actively push their data to L2s, requiring changes to their contract logic.

**Signal-Boost** addresses this by adopting a request-before-push model. Instead of asking L1 contracts to emit signals, anyone can query arbitrary L1 view functions and push the results to the `SignalService` contract in a verifiable way. In practice, this is especially useful when done by the L2 sequencer.

This significantly increases the utility of same slot messaging by unlocking access to live L1 data without requiring upstream contract changes. However, it introduces new challenges: What happens if the signal changes mid-slot? How do L2 users respond or verify?

To address these, Signal-Boost incorporates ideas from Ultra transactions, including [EIP-7702](https://github.com/ethereum/EIPs/blob/9b44c0d41fd714ccca411d3a7ab7705284fddaa3/EIPS/eip-7702.md) smart accounts for delegated execution and ToB inclusion for state guarantees.

### SignalBoost contract

To make same-slot messaging easier to adopt, we need a way to turn L1 data into a verifiable signal that L2s can trust. The `SignalBoost` contract provides this functionality by allowing anyone to query L1 view functions and commit the results on-chain in a format that downstream L2 contracts can consume immediately.

1. You prepare a list of read-only queries you want to make on L1, e.g.:

“What’s the price in this Chainlink contract?”
2. “What’s the balance of this address?”
3. “Is this vault active?”
4. You submit this list to the SignalBoost contract, which:

Calls all of the L1 contracts using their view functions
5. Hashes the inputs with the results
6. Builds a Merkle tree from the data
7. Posts the root of that tree (called signalRequestsRoot) to the SignalService contract on L1
8. Now the L2 sequencer can:

Read the signalRequestsRoot from the L1
9. Include it in the L2 publication
10. Allow L2 smart contracts to verify individual signals via Merkle proofs during the same L1 slot using the same techniques described in same-slot messaging.

From the POV of an L2 developer, they can verify that the L1 `output` came from the correct L1 contract call. Here’s an example to read L1 oracle data which can be consumed by other L2 contracts.

```solidity
// Example function on L2
function readL1Pricefeed(bytes calldata output, bytes32 signalRequestsRoot, bytes[] calldata proof) external returns (uint256) {
    // Verify the signal was written to the L2 SignalService
    require(SignalService.verifySignal(signalRequestsRoot), "Signal not found");
    // Reconstruct the SignalRequest for this context
    SignalRequest memory request = SignalRequest {
			target: L1_ORACLE_ADDRESS,
			selector: bytes4(keccak256("getPrice()")),
      input: bytes("")
		};

    // Reconstruct the Merkle leaf
    bytes32 leaf = keccak256(abi.encode(request, output));

    // Verify the Merkle proof
    require(verifyProof(signalRequestsRoot, leaf, proof), "Invalid Merkle proof";

    // Decode the Oracle price
    uint256 price = abi.decode(output, (uint256));

    return price;
}
```

### Smart Accounts

To ensure that the signals are as up to date with the L1 as possible, we want `SignalService.writeSignals()` to be executed immediately before the L2 batch is published.

Using EIP-7702 smart accounts helps coordinate this. They allow the L2 sequencer to bundle their own transactions together with pre-signed user transactions (assuming the user’s smart account supports delegation), all in a single L1 call. This allows for atomicity and tight control over execution ordering.

Conveniently, this is compatible without stack modifications for sequencers in the OP Stack who do not post their blobs to contracts that could allow bundling.

### Top of Block Execution

There is a subtle but important risk: the output of `SignalService.writeSignals()` can change depending on *where* the bundle containing it is executed within the L1 block.

If this output differs from what the L2 sequencer expected, then the `signalRequestsRoot` and corresponding `proof` used by L2 contracts will be invalid, causing the L2 transactions to revert.

There are a few ways to mitigate this:

1. Last transaction execution
 The bundle can be placed at the end of the L1 block to ensure it reflects all prior state changes. However, this limits its utility. At that point it’s simpler to wait for the next block and access the finalized L1 state asynchronously.
2. Execution preconfirmations
 L1 proposer can commit to executing the L1 block such that the bundle produces the expected signalRequestsRoot. If they deviate, they can be slashed. This offers an economic guarantee that doesn’t rely on a specific block position.
3. Top of Block execution
 Executing the bundle at ToB ensures a clean post-state from the previous L1 block. If SignalService.writeSignals() runs after all relevant transactions within the bundle, the resulting signalRequestsRoot will reflect the freshest L1 state possible. Also note:

Implementing ToB inclusion preconfs is simple in practice. See Tobasco for a minimal working example.
4. If ToB pricing is a concern, the bundle can include normal MEV strategies (such as CEX-DEX arbitrage) to offset its cost.
5. Based Sequencing
A based sequencer can enforce that their bundle executes with the expected result since they have a write-lock on the L1 and L2. Essentially they can give themselves the same guarantees as in 2) and 3) above, but without coordinating with anyone else. As one of the goals of Signal-Boost is allowing existing rollups to achieve SC with the L1, we’ll assume we use ToB execution for the rest of this paper.

### Putting It All Together

With `SignalBoost`, EIP-7702 smart accounts, and ToB execution, we now have the key ingredients for enabling real-time access to arbitrary L1 data from L2 contracts.

But one challenge remains: **how do L2 transactions get access to their corresponding signal proofs when the signals are written in the same slot?**

Since the `signalRequestsRoot` is only known after executing `SignalBoost.writeSignals()`, users cannot include their Merkle proofs ahead of time. There are a few workarounds:

- Delegated Construction via EIP-7702
 Users pre-sign their L2 transactions that permit the sequencer to inject the signalRequestsRoot and proof during execution. This lets the transaction be fully constructed on the fly, while still enforcing correctness at runtime. If the signal or proof is invalid, the L2 transaction reverts.
- Sequencer-Assisted Proofs
 During the L1 slot, users can query the sequencer for the latest signalRequestsRoot and corresponding proof. This avoids any special smart account logic but requires coordination between the user and sequencer.
- Sequencer-Injected Data
 With knowledge of the signalRequestsRoot and all Merkle proofs, the Sequencer can simply publish all the proofs to an L2 contract that verifies and then stores the output data. L2 contracts can then simply access the outputs from L2 storage, without knowledge of the signalRequestsRoot or proofs. This completely abstracts away the details from the L2 users but pushes the cost burden to the Sequencer.

Assuming the middle option, the end-to-end flow using [same-slot messaging](https://ethresear.ch/t/same-slot-l1-l2-message-passing/21186) is:

[![image](https://ethresear.ch/uploads/default/optimized/3X/f/6/f64f32bcf687d08b70ff4bb88db19a0fafb456d0_2_690x356.jpeg)image1806×933 149 KB](https://ethresear.ch/uploads/default/f64f32bcf687d08b70ff4bb88db19a0fafb456d0)

1. The L2 sequencer collects arbitrary L1 transactions, created by them or others using smart accounts with delegated EOA executions
2. The L2 sequencer collects SignalRequests from L2 users
3. The L2 sequencer bundles the L1 transactions with a call to SignalBoost.writeSignals()
4. The L2 sequencer simulates the execution of the bundle up to this point, allowing them to learn the signalRequestsRoot and generate Merkle proofs. The signalRequestsRoot is imported into the L2’s SignalService contract
5. L2 users query the L2 sequencer for signalRequestsRoot and a proof for their specific signal
6. L2 users send L2 transactions that consume the signals
7. The L2 sequencer creates an L2 batch and adds it to the bundle, importing the signalRequestsRoot
8. Assuming real-time proving, the sequencer optionally bundles in a validity proof to settle the rollup and any L1 transactions that consume the L2 state (i.e., L2→L1 withdrawals)
9. The bundle is sequenced at the top of the L1 block

## FAQ

### What can I do with this?

Signal-Boost unlocks synchronous access to arbitrary L1 data from L2 contracts without requiring major upstream protocol changes. This enables a range of new use cases, such as:

- Loan migration across L2 protocols
 A user can seamlessly migrate their loan between L2 lending protocols by:

Tapping into L1 liquidity to take out a flashloan (e.g., USDC)
- Synchronously processing an L1→L2 deposit, made possible by real-time signaling
- Repaying the existing L2 loan to unlock their ETH collateral
- Opening a new loan on a different L2 protocol with better terms using that ETH
- Withdrawing USDC back to L1 and using them to repay the flashloan

All of this is executed atomically within a single L1 slot. No oracle duplication or delayed bridging, just synchronous composability with the L1 and real-time proving!

**Cross-domain arbitrage**

Dual arbitrage that takes full advantage of same-slot messaging and ToB execution:

- Capture L1 arbitrage at the top of the Signal-Boost bundle
- Relay updated oracle data from L1 to L2 via SignalBoost contract
- Capture L2 arbitrage based on the newly available price

**Instant L1↔L2 swaps using intents**

Even without real-time proving, same-slot messaging instant L1<>L2 withdrawals using intents [as described by Nethermind](https://ethresear.ch/t/fast-and-slow-l2-l1-withdrawals/21161).

These examples only scratch the surface, any L2 contract that depends on timely access to L1 data scan benefit.

### How would this work on the OP Stack?

The OP Stack has no notion of a `SignalService` contract or anchor transactions which are used in the same-slot messaging design. Instead, the OP Stack’s derivation pipeline reads all L1 messages (L1 deposits / arbitrary function calls) transmitted via the `CrossDomainMessenger.sendMessage()` function and inserts them into the top of the L2 block.

The `SignalBoost` contract could be adapted to call `sendMessage()` with the `signalRequestsRoot` value instead of writing to a `SignalService` contract. No changes would be needed to add anchor transactions as the OP stack already supports similar functionality.

Additionally:

- The L2 sequencer must be the Signal-Boost bundler as the derivation pipeline expects blob transactions are submitted by the canonical batchSubmitterAddress.
- To synchronously read these L1 messages, the L2 sequencer’s SequencerConfDepth value would need to be set to 0 to follow the L1 head in real-time.

TL;DR change one config value and tweak the `SignalBoost` contract

### Does this hurt the value proposition of based rollups?

No. Signal-Boost helps expand the market for synchronous composability, but based rollups still offer unique advantages:

- Signal-Boost is simpler with based rollups, relaxing ToB or execution preconf requirements.
- Ultra transactions use based rollups to enable the most powerful form of synchronous composability.
- Shared sequencing is still necessary for synchronous cross-cluster L2 ↔ L2 composability.
- New rollups may prefer to launch as based appchains to avoid the burdens of running a centralized sequencer complexity (i.e., infrastructure costs, liveness, regulatory risk, etc).
- Using the validators as based sequencers offers maximal composability
- WW3-grade rollups prioritizing liveness would opt for based sequencers.

### Does adopting Signal-Boost require rollups to modify their existing stack?

No. Signal-Boost is designed for low-friction adoption. Rollups do not need to overhaul their stack or majorly upgrade their protocol. Sequencers can opt in selectively and only construct bundles when synchronous access to L1 state is needed.

It should be noted that different stacks will have less friction that others depending on how they currently handle L1 input data and reorgs.

### Does Signal-Boost require complicated preconfs?

Guaranteeing ToB execution reqiures a straightforward inclusion preconf that is easier to prove safety faults for than L1 or L2 execution preconfs (see the PoC [Tobasco](https://github.com/eth-fabric/tobasco)).

It’s possible to relax the ToB requirement and use execution preconfs to guarantee the expected `signalRequestsRoot` is reported on L1. This is also easy to prove but will require more sophistication from the preconfer to execute.

### Does Signal-Boost require rollups to give up sequencing control or MEV?

No, Signal-Boost is sequencing-agnostic. Whether using it’s based sequencing, classical sequencing, shared sequencing, or a rollup ecosystem (i.e., SuperChain), rollups retain full sovereignty over transaction ordering, MEV capture, and fee markets. Signal-Boost is merely a technique to allow rollups to synchronously access L1 state.

### Can Signal-Boost enable synchronous composability between two rollups?

Signal-Boost was designed for L1 ↔ L2 composability in mind, allowing a sequencer to give their users synchronous access to L1 state. The simplest implementation of this is with a centralized sequencer, that said, there is important nuance:

- Signal-Boost is sequencer-agnostic, so rollups can continue using their own interop solution (e.g., SuperChain) to enable L2 ↔ L2 composability within their cluster.
- The Signal-Boost bundle can contain an arbitrary number L2 batches, allowing for L2 ↔ L2 composability; however, for cross-cluster composability (i.e., Base <> Scroll), we still require a shared sequencer to coordinate. Based sequencers remain the most neutral and flexible candidate for this role.

### What is the difference between Signal-Boost and Ultra transactions?

Ultra transactions offer the most complete vision of cross-chain composability. They assume the L1 and rollup stacks are modified to support features like the `XCALLOPTIONS` precompile and EVM equivalence with the L1, allowing execution to move fluidly across domains. This enables arbitrary L1 ↔ L2 function calls, synchronous access to state, and atomic execution of bundled transactions all verified by a single proof.

Signal-Boost is a simplified but pragmatic adaptation of this idea to make some of the technology available to existing rollups today.

### What’s the difference between Signal-Boost and same-slot messaging?

[Same-slot messaging](https://ethresear.ch/t/same-slot-l1-l2-message-passing/21186) enables L1 → L2 communication by writing data to a messenger contract that the L2 can read in the same slot. It does not support arbitrary L1 reads, just signals that have been written to the L1 `SignalService` contract. Signal-Boost adopts the same techniques but attempts to address it’s limitation via the `SignalBoost` contract.

### Is this really synchronous composability?

Yes, but with an important caveat. Signal-Boost enables synchronous composability in the strict sense: L1 and L2 state can interact within the same L1 slot, and one domain can read and react to the other’s state atomically. This satisfies the [definitions used by Jon Charbonneau](https://dba.xyz/were-all-building-the-same-thing/#definitions), where *synchrony* implies same-slot coordination and *composability* means reactive state access.

Ultra transactions, real-time proving, and proposals like EIP-7814 allow for full bidirectional composability: arbitrary cross-domain reads and writes / interleaved function calls which is strictly better than what Signal-Boost can offer.

### Why would a rollup ever reorg with the L1 given the risk?

*Reorg risk is the price of real-time interoperability.*

A potential solution is an on-demand model: the rollup operates with a safety buffer by default to mitigate L1 reorg risk, but can temporarily reduce the buffer to 0 when synchronous L1 access is required. In the OP Stack case, this is possible by dynamically adjusting the `SequencerConfDepth` value in the sequencer’s config.

### Can anything be done about ?

Yes, a few developments may reduce L1 reorg frequency. For context, most reorgs are caused by slow or late block propagation, often due to timing games or bandwidth limitations (read more [here](https://www.notion.so/Spectrum-of-L1-Reorg-Tolerance-1eb968886c718008a82aca60ca607894?pvs=21)).

- Preconfs: As preconfs mature, they give proposers incentives to deliver blocks reliably, especially when slashing penalties are in place.
- Attester-Proposer Separation (APS): APS shifts block production to specialized high-bandwidth proposers, reducing missed or late blocks due to networking limitations.
- Slot futures: If a proposer sells a future block via preconf, the buyer (e.g., a rollup sequencer) and preconfer are incentivized to make sure the block lands on time.

### Won’t ToB be expensive?

Yes, ToB is premium block real estate.

Fortunately, nothing precludes normal MEV transactions from being inserted into the top of Signal-Boost bundles, allowing the sequencer to offset costs. Additionally, EIP-7814 would allow for arbitrary L1 reads without requiring `SignalService` contract if it is implemented in the future.

*Based rollups do not require ToB or execution preconfs.* Since they sequence the L1 block, they can ensure that no surprise transactions invalidate the expected `signalRequestsRoot`, allowing them to safely execute the Signal-Boost bundle at any position in the block.
