---
source: ethresearch
topic_id: 23857
title: Trust minimized transaction simulation using state proofs
author: Sednaoui
date: "2026-01-15"
category: Security
tags: []
url: https://ethresear.ch/t/trust-minimized-transaction-simulation-using-state-proofs/23857
views: 204
likes: 8
posts_count: 4
---

# Trust minimized transaction simulation using state proofs

## Summary

Transaction simulation is critical for wallet security. Users need to preview what a transaction will do before signing. But current simulation approaches require blindly trusting RPC providers for state data, creating a dangerous single point of failure. We explore a trust minimized simulation approach using Merkle Patricia Trie proofs and multi-node consensus to cryptographically verify the prestate before execution, eliminating the need to trust any single RPC provider while remaining practical for production wallets.

## The Simulation Trust Problem

Users can’t read raw transaction data. A transaction is encoded calldata: bytes that specify contract calls, parameters, and state changes. Users have no way to verify what a transaction actually does just by looking at it. This is the **blind signing problem**: users must trust their wallet to tell them what they’re signing.

Transaction simulation emerged as the solution. Before users sign, wallets simulate the transaction to show what tokens will be transferred, what approvals will be granted, what contract state changes will occur, and whether the transaction will revert. This prevents users from signing malicious transactions that drain funds, grant dangerous approvals, or behave unexpectedly. Simulation transforms blind signing into informed signing where users see decoded, human-readable results before they sign.

**But there’s a fundamental trust issue:** Most wallets don’t run simulations themselves. Instead, they rely on third-party simulation APIs: black box services where you send a transaction and receive back decoded results showing what will happen. But here’s what actually happens behind the scenes: these services typically call trace APIs (like `debug_traceTransaction` or `trace_call`) from third-party RPC providers (Infura, Alchemy, etc.), receive execution traces from those providers, decode and format the results, then return them to the wallet.

This creates multiple layers of trust: you’re trusting the simulation service’s decoding and display logic, which is trusting the RPC provider’s state data, which is trusting their EVM execution and trace generation. The simulation service doesn’t typically run its own nodes or execution - it’s aggregating and formatting data from third-party infrastructure. There’s no way to verify any of this. Even wallets that do run simulations locally still face the core problem: they fetch state and execution traces from RPC providers and trust them completely.

The infrastructure layer has centralized around a handful of RPC providers (Infura, Alchemy, QuickNode) serving the majority of users. Meanwhile, running your own node is resource-intensive, and mobile/browser wallets can’t run full nodes at all. This centralization accelerates as mobile-first wallets dominate adoption and users prioritize convenience.

## A Concrete Attack

Alice sends Bob a transaction to approve: supposedly transferring 50,000 USDC to charity. Bob can’t read the encoded transaction bytes, so he relies on his wallet’s simulation.

Bob’s wallet uses a compromised simulation API. The API returns results showing “Transfer 50,000 USDC to Charity (0x1234…)”. Bob reviews it, sees his donation to a recognized charity, and signs.

But the simulation lied. The actual transaction calldata drains Bob’s entire USDC balance to an attacker’s address (0xabcd…). The malicious service showed fake execution traces while the real transaction does something completely different.

Bob was blind signing with extra steps. Even a hardware wallet wouldn’t help because it can only verify Bob is signing what was sent to it, not whether the simulation accurately represents what the transaction will do. The attack works because the simulation service is a complete black box with no way to verify the results.

This isn’t theoretical. RPC providers get compromised through infrastructure breaches, DNS hijacking, MitM attacks, and malicious browser extensions. A single compromised simulation service could show fake simulations to millions of users across hundreds of wallets.

## Why Not Light Clients?

Light clients are the principled solution: verify state without downloading the full chain. But they face significant practical barriers including resource requirements prohibitive for mobile, long sync times, complex WASM compilation for browser support, and protocols still in active development. Many L2s lack mature light client implementations entirely. We need a practical solution today for production wallets.

## Our Approach: Verified Prestate Simulation

Verify the prestate cryptographically using Merkle Patricia Trie proofs and multi-node consensus, then execute the transaction locally with revm to generate our own execution traces.

**The mechanism:**

1. Fetch prestate: Use debug_traceCall with prestateTracer to discover required state
2. Establish consensus: Query multiple RPC nodes for state root at the simulation block
3. Require unanimous agreement: All nodes must agree on state root, otherwise reject the simulation
4. Request proofs: Call eth_getProof for all accounts and storage in prestate
5. Verify proofs locally: Walk MPT proofs, verify hashes, confirm values
6. Execute locally with revm: Only if all proofs validate, execute transaction with verified state using revm (Rust EVM implementation)
7. Generate our own traces: Produce execution traces, state changes, and results from our own EVM execution

![Simulation Flow Diagram](https://ethresear.ch/uploads/default/original/3X/b/b/bb8ca9160135d1caa7f5b3028835160a86dc97bb.svg)

## Technical Implementation

### Step 1: Discover Required State

Use `debug_traceCall` with the `prestateTracer` to discover exactly what state the transaction will access. This returns the complete prestate: all accounts that will be touched, their balances and nonces, all storage slots that will be read, and code for any contracts executed.

This discovery enables local simulation without a full node and tells us what state to verify using MPT proofs.

### Step 2: Establish State Root Consensus

Query N independent RPC nodes to establish consensus on the state root at the simulation block. For each verification node, call `eth_getBlockByNumber` and extract the `stateRoot`. All verification nodes must agree on the state root. If even one node disagrees, reject the simulation entirely since disagreement indicates you’re being targeted.

This consensus mechanism prevents a malicious simulation node from lying about the prestate. Because the prestate is verified using the consensus state root, to lie about the prestate it has to control all of your verification nodes.

### Step 3: Request and Verify Cryptographic Proofs

For each account and storage slot in the prestate, call `eth_getProof`. The response contains Merkle Patricia Trie proofs that we verify locally by walking through the proof nodes, hashing each node, and confirming values match what was claimed. Account proofs verify against the global state root; storage proofs verify against the account’s storageHash. For accounts that don’t exist yet, we verify they’re actually not deployed, and trust the local REVM execution for their state.

### Step 4: Execute Locally with Revm

Only after all proofs validate successfully, execute the transaction locally using revm (Rust EVM implementation) with the verified prestate. This is critical: we don’t just verify state and trust someone else’s execution. We run our own EVM to generate execution traces, state changes, and event logs.

The execution happens entirely on the user’s device with verified inputs. REVM is pinned to a known version with auditable upgrades, unlike opaque node provider APIs where you have no visibility into what code is running or when it changes.

If any proof fails to verify, reject the entire simulation and either retry with different nodes or alert the user to a potential attack.

## Security Properties

The threat model assumes adversarial RPC providers and simulation services. The approach maintains decentralization by requiring unanimous agreement on the state root across all verification nodes. If even a single node disagrees, the system detects the manipulation and rejects the simulation. The proofs are deterministic and transparent; anyone can verify the verification.

## Trade-offs and Limitations

The approach requires access to multiple independent RPC providers for the consensus mechanism. It depends on RPC support for `eth_getProof` (widely supported) and `debug_traceCall` with `prestateTracer` (less common). The unanimous agreement requirement means that if even one verification node is down or returns a different state root, the simulation will be rejected. This trades off availability for security.

Prestate completeness verification is not yet implemented. The current implementation verifies that provided prestate is accurate, but doesn’t verify it’s complete. A malicious node could provide accurate proofs for incomplete prestate (hiding critical storage slots). The planned defense is to verify post-execution that no storage was accessed beyond the verified prestate, but this is future work.

Conditional flows in smart contracts can trick the simulation. A malicious contract could behave differently based on conditions like `block.timestamp`, `msg.sender`, or other state variables, causing the simulation to show benign behavior while the actual onchain execution does something malicious. Another vector is MEV, where the transaction order in a block can change from what the simulation resulted. These are a general problem with all transaction simulation approaches, not specific to state verification. We’re interested in feedback on potential mitigations for this attack vector.

The approach works for EVM chains that support `eth_getProof`: Ethereum mainnet and most L2s. Chains with different state representations would need adapted verification logic.

## Discussion

This demonstrates that trust minimized transaction simulation is practical today without waiting for light client maturity. It’s not a perfect solution, but it eliminates the single point of trust that exists in nearly every wallet today.

**On the general approach:** Are there fundamental issues we’re missing? The mechanism relies on `eth_getProof` returning valid Merkle Patricia Trie proofs and consensus on state roots across independent nodes. We’d appreciate critical feedback on whether this foundation is sound for production wallet simulation or if there are attack vectors we haven’t considered.

**On consensus design:** We currently require unanimous agreement across all verification nodes for the state root. If even one node disagrees, the simulation is rejected. The reasoning is that in theory, there’s no legitimate reason for verification nodes to disagree on the state root unless you’re being targeted. This prioritizes security over availability. Is this the right trade-off for production wallets, or should there be configurability for users who prefer different security/availability balances?

**On light client comparison:** How does this compare to running a full light client for simulation? We see this as a pragmatic solution that works today across all platforms (mobile, browser, desktop). Light clients provide stronger guarantees by following the consensus layer directly, but face adoption barriers. Are there specific security properties we’re sacrificing that make this approach unsuitable for wallet simulation?

---

Looking forward to your feedback.

## Replies

**mmsaki** (2026-01-29):

This is such a profound way of using `eth_getProof`. I had no idea that this would be a good usecase so thank you for posting this. Still have to read this a few time to fully understand the problem with trusting RPC providers.

From my experience I notice that many providers do not serve the `debug_traceCall` method publicly but not sure about your experience getting debug traces from rpc providers .

---

**thegaram33** (2026-01-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/sednaoui/48/6327_2.png) Sednaoui:

> Query N independent RPC nodes to establish consensus on the state root at the simulation block.

Why not just simulate/trace the transaction on N independent RPC nodes then? What is the benefit of local re-execution?

Also, two additional ideas that you might want to consider:

1. The RPC provider could provide a validity proof of correct simulation, along with the result. I recall some team is already working on this.
2. Another concern is that the simulated result might not match the actual execution result, if the transaction’s pre-state changes. Smart accounts could execute pre- and post-execution checks to deal with this.

---

**Sednaoui** (2026-01-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> Why not just simulate/trace the transaction on N independent RPC nodes then? What is the benefit of local re-execution?

Simulating on multiple RPCs gives you consensus on the result, but not proof of correct execution. A few issues:

1. Trace quality: eth_debugTraceCall doesn’t give you full execution traces. Local execution with REVM gives you complete control over trace generation. You can extract exactly what you need for verification/display.
2. Separation of concerns: state proofs verify the INPUT is correct (verified state). Local execution verifies the EXECUTION is correct. Cleaner trust model.
3. Access to debug_traceCall is usually restricted and often gated behind paid subscriptions at RPC providers, which makes executing the same request on 5 or more independent nodes challenging. By contrast, eth_getProof is widely supported, including by public nodes, enabling straightforward verification across multiple independent providers. (cc @mmsaki, yes it is challenging to find rpc providers with debug_traceCall enabled)

The key insight is that verifying state gives you a *known good starting point*. Local execution gives you a *known good process*. Together are end-to-end verification.

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> The RPC provider could provide a validity proof of correct simulation, along with the result. I recall some team is already working on this.

Yes! this is interesting. We know a few teams exploring zk-proven execution and will keep an eye when they release.

![](https://ethresear.ch/user_avatar/ethresear.ch/thegaram33/48/13742_2.png) thegaram33:

> Another concern is that the simulated result might not match the actual execution result, if the transaction’s pre-state changes. Smart accounts could execute pre- and post-execution checks to deal with this.

This is a valid concern for simulation regardless of our approach. Simulation happens at block N, execution at block N+X. State can change. This is where execution time protection comes in. You are right, we are using this approach specifically for Safe Smart Accounts, where guards can enforce invariants at execution time and implement pre/post execution checks.

