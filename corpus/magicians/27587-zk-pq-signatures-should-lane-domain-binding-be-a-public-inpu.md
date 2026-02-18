---
source: magicians
topic_id: 27587
title: "ZK + PQ signatures: should lane/domain binding be a public input?"
author: pipavlo82
date: "2026-01-25"
category: Uncategorized
tags: [account-abstraction, zk]
url: https://ethereum-magicians.org/t/zk-pq-signatures-should-lane-domain-binding-be-a-public-input/27587
views: 16
likes: 0
posts_count: 1
---

# ZK + PQ signatures: should lane/domain binding be a public input?

As Account Abstraction and post-quantum / hybrid signatures start to coexist on Ethereum,

I think we’re quietly accumulating a new class of failure modes.

Not cryptographic — semantic.

The same signature (or ZK proof verifying a signature) can be:

- cryptographically valid
- yet replayed or reinterpreted across verification surfaces

Examples:

ERC-1271 ↔ AA validation ↔ protocol-facing precompile ↔ ZK settlement.

If a ZK circuit verifies a PQ (or hybrid) signature *without binding the verification surface*

into a public input, the proof can be reused across contexts.

This is essentially replay-by-interpretation. I’ve been calling these “domain-separation wormholes”.

A minimal mitigation I’m exploring:

→ require a **lane digest** (hash of surface binding + algo/XOF + chain context)

to be exposed as a **public input** in ZK circuits that verify signatures.

That way:

- on-chain verifiers can check lane_digest == H(envelope)
- proofs fail if replayed across surfaces with different bindings

I’m not claiming this is novel cryptographically — it’s more about *socially enforcing a minimum bar*

for ZK + PQ verification patterns.

I wrote this up as a small research/benchmark repo:



      [github.com](https://github.com/pipavlo82/gas-per-secure-bit)




  ![image](https://opengraph.githubassets.com/869521a0532b629dced37251d24cc8f9/pipavlo82/gas-per-secure-bit)



###



Gas per secure bit benchmarking for PQ signatures and VRF.










Relevant bits:

- “explicit message lanes” as a security requirement
- ZK settlement surface (Groth16 / BN254) treated as a baseline
- a short discussion on whether lane digest must be a public input

Discussion here:


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [GitHub](https://github.com/pipavlo82/gas-per-secure-bit/discussions/26)



    ![](https://opengraph.githubassets.com/893e1a78aef18051cf74a34dd886266ad90536ca6c20858ded2333d94b1db453/pipavlo82/gas-per-secure-bit/discussions/26)

###



Question Should ZK circuits that verify PQ (or hybrid) signatures be required to expose a lane digest (explicit message lane envelope) as a public input (or otherwise commit to it in a publicly ver...










Open questions I’d love feedback on:

- Is exposing a single lane digest as a public input the right minimum bar?
- For AA: is EntryPoint address sufficient as verifier binding?
- For protocol precompiles: what’s the cleanest binding identity?
- Are there existing ZK patterns/standards that already do this well?

Curious how others are thinking about this, especially as PQ verification inside ZK becomes more common.
