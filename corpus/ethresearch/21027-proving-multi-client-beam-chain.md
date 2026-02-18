---
source: ethresearch
topic_id: 21027
title: Proving multi-client Beam chain
author: mratsim
date: "2024-11-18"
category: Consensus
tags: []
url: https://ethresear.ch/t/proving-multi-client-beam-chain/21027
views: 1165
likes: 16
posts_count: 7
---

# Proving multi-client Beam chain

Hello teams,

I have a couple questions to make sure zkVM teams support the Beam chain proposal as best as possible.

## Implementation

What languages will clients be built in. In our case at Lita/Valida, we can support C, Nim (through C), Rust. And we plan to add Go, WASM (for Javascript clients) and Zig support (seems to be a popular new language that Eth devs want to build in).

Are Nethermind and Teku/Besu team planning to build a Beam Client, will it be in C# and Java? What about LambdaClass and Elixir?

## Networking

What proof sizes are we targeting?

## Performance

What proving speed do we need? We plan to add some benchmarks of the current state transition function of Grandine, Lighthouse and Nimbus to get a baseline.

If block times become 4s, should the proof be aggregated over a whole “epoch”

## Replies

**JustinDrake** (2024-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> What languages will clients be built in.

It’s early days and the dust needs to settle. As of today there are provisionally 12 teams that have signalled an interest in building a beam client. Languages (in alphabetical order) include C, C++, C#, Elixir, Go, Java, Nim, Rust, Zig.

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> Are Nethermind and Teku/Besu team planning to build a Beam Client, will it be in C# and Java? What about LambdaClass and Elixir?

It’s so early days that my suggestion would be to talk to individual teams directly. Having said that, I do expect that most existing consensus teams would retain the language used for their beacon client. (As I understand Lodestar may be looking at higher-performance alternatives to TypeScript.)

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> What proof sizes are we targeting?

I’m assuming the post-quantum proofs would be ~100KB in size. Proofs would be gossiped offchain in separate gossip channels. Some clients may choose to temporarily wrap post-quantum proofs into shorter pre-quantum SNARKs until quantum computers become powerful enough.

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> What proving speed do we need?

Proofs for the current block need to reach attesters by the start of the next slot. As such, proof latencies needs to be sub-slot. If slot durations are 4 seconds and 1 second is budgeted for gossiping there would only be a budget of 3 seconds for proving latency. For the 1-of-n honest-minority prover assumption to be highly credible, reasonably modest hardware (e.g. a high-end laptop) should be sufficient for proving.

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> If block times become 4s, should the proof be aggregated over a whole “epoch”

Proofs need to come every slot to give attesters the option to attest without running naively verifying blocks. Low-latency proving is also important for the UX of wallets (and other pieces of infrastructure) that consume the proofs. As a side note, with single-slot finality the notion of epoch would likely be deprecated.

---

**jtfirek** (2024-11-18):

Wouldn’t the wrapper SNARK need to prove the validity of the post-quantum proof making the total size the post-quantum proof PLUS the SNARK overhead?

---

**JustinDrake** (2024-11-19):

The wrapper SNARK would ingest the post-quantum proof as witness data so the final size is just the wrapper SNARK (roughly 100x smaller than the post-quantum proof). This is a common technique zk-rollups use to save on gas for onchain proof verification.

The main downside of the wrapper SNARK (besides the fact that it needs to be removed before quantum computers become practical) is that it adds proving latency. Total proving latency is the post-quantum proof latency PLUS the wrapper SNARK latency.

---

**0xalizk** (2024-11-22):

> What languages will clients be built in.

I think the primary question should be: **what ISAs to target** for arithmetization, and language optionality should follow from that.

Ideally:

- There should be 1 ISA and 1 compilation toolchain across all clients.
- Auditing efforts are then pooled on this unified toolchain.
- Diversity can flourish at the higher language level, and at the IOP backend level:

The former shields against implementation bugs (as is now with client diversity)
- The latter shields against soundness bugs

So, an **~immutable standardized toolchain core, and a diverse plug-n-play front- and backends**.

The ISA aspect should be a standardization question, not an optimization question. First, they are all just `pc` `registers` `RAM` `ROM` in one way or another. Second, any edge custom ISAs bring is outweighed by the [difficulties](https://lita.gitbook.io/lita-documentation/architecture/llvm-valida-compiler#current-progress) their custom toolchain brings, which must be audited on its own A-Z (no compounding benefits from *other* audits).

A client team would be concerned with the ISA choice of *other* clients because it would be verifying proofs from them, so their soundness has implication on the integrity of their own client. A combinatorial explosion of language x ISA should be avoided.

Therefore, the ecosystem can probably only afford the auditing overhead of 1 toolchain.

#### A note on garbage-collected languages:

- For custom handrolled circuits of specific L1 components, client teams of GC-languages should probably just focused on a side-car design where they prove/verify in a non-GC language via either FFI or IPC.
- For the zkCL in entirety (CL STF), I suspect that wrapping the STF in a GC lanaguge in a zkVM will be a challenging: compiling Go to RISCV for example via LLVM IR, you need to weave-in the GC, LLVM doesn’t do that for you. Add to that the performance hit GC brings in terms of number of constraints -I suspect.

ZK side-car binaries would be:

- Recursive prover for hash-based validator signatures (this will be a unified enshrined verifier for all clients)
- Verifier of other clients’ proofs of the entire CL (this could be an off-chain out-of-spec thing).
- From the EL side (not part of the Beam upgrade), a verifier of zkEL (produced by block builders; enshrined) and prover/verifier of potentially-by-then-binary-merklized state tree for answering/forwarding queries of light-clients (off-chain out-of-spec).

> What proving speed do we need?

I think the target should be < 1s for zkCL overall, which means milli- or even micro-seconds for 1 recursive SNARK of the hash-based signature scheme.

This unlocks optionality in two ways:

- As large of participating validator set as possible, giving Orbit-style designs more room
- As much time as possible for future zkEL SNARKification needs:

Looking ahead, CL clients would also be verifying zkEL proofs (produced by builders). We would want to allow as high of a target on zkEL verification as possible in order to allow as big of blocks as L1 scalability needs.
- The future p2p costs should be kept in mind as well. We will want to leave enough room for big EL blocks to propagate (the witness). In the super End Game, zkEL could be proven in zero-knowledge (the block is private input) and only selective parts of the state are sought by a node (state will be PeerDAS’d), but even then, that part will need time to propagate.

The leaner we make the Beam the thicker we can afford to make zkEL for max L1 scalability needs.

---

**ClementWalter** (2024-11-29):

I have to say that I’m not convinced yet by the single ISA claim.

At Kakarot, we are actually building an EVM prover and aim at building also a consensus client in Cairo, using consequently a whole different tool chain and ISA (currently Cairo ISA, may change with Stwo allowing more dynamic layouts and custom AIRs).

The benefit I understand from your post is that a single ISA ease interoperability between code producers and prover providers, and simplify the audit process. But it seems far to early to me to freeze a given ISA. For example, currently the RISC-V ISA is hyped amongst the zk community, though I’m definitely not convinced that this is a good option.

---

**mratsim** (2024-12-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/0xalizk/48/15474_2.png) 0xalizk:

> There should be 1 ISA and 1 compilation toolchain across all clients.

The role of multi-clients, multi-language is to ensure that if there is a bug in 1, less than 33% of the validator pool is affected and we don’t have liveness issues.

Unless that 1 ISA, 1 toolchain is formally verified end-to-end, aka “correct-by-construction”, there are still risk of bugs. Currently the only production-ready formally verified compiler for a fast enough language is CompCert, assuming we write a C implementation (or formally verify Nim->C compilation), but even Risc-V ISA isn’t formally verified as far as I know and it’s unrealistic to formally verify Rust within 5 years. NWe could also consider languages designed for formal verification like Ada/Spark or Lean, we can have something but Lean is too slow and Ada/Spark needs licensing.

Will it be in 5 years, I sure hope so but as Clement mentioned, ZK languages and ISA like Cairo, Noir, Valida have inherent benefits that an ISA optimized for hardware cannot attain.

For example:

1. For locality, they use registers, an addition would need 2 load from memory, 1 add in register, 1 store. A ZK optimized language or ISA, would forego registers and have a trace 4x smaller by directly operating on memory.
2. Also for locality, each function requires saving all registers modified by the function (either callee or caller saved depending on the call convention), and then restoring them at the end. A ZK optimized language or ISA does not need that. See RISC-V Bytes: Caller and Callee Saved Registers · Daniel Mangum on Risc0, register x18 to x27 need to be saved, potentially generating huge proof overhead if a library is made of many small functions. And if you look at consensus specs, many functions are very small:

- compute_committee
- compute_epoch_at_slot
- compute_activation_exit_epoch
- compute_fork_data_root
- compute_fork_digest
- compute_domain
- compute_signing_root
- get_current_epoch
- …

So there is a ceiling, assuming proving load/store have the same cost as proving a compute operation:

- from 1, if working on new data (i.e. not in registers) RISC-V based zkVM are at best 4x slower than ZK optimized languages/ISA. This is the case, we get new blocks all the time and rehash everything.
- from 2, while having small descriptive functions with single responsibility is what the Ethereum spec strive for, optimizing for Risc-V zkVMs would instead encourage developing with large functions that would be error-prone, hard to maintain and audit.

