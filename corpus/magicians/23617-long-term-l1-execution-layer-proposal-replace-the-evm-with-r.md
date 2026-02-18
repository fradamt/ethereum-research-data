---
source: magicians
topic_id: 23617
title: "Long-term L1 execution layer proposal: replace the EVM with RISC-V"
author: vbuterin
date: "2025-04-20"
category: Magicians > Primordial Soup
tags: [evm, risc-v]
url: https://ethereum-magicians.org/t/long-term-l1-execution-layer-proposal-replace-the-evm-with-risc-v/23617
views: 31346
likes: 302
posts_count: 113
---

# Long-term L1 execution layer proposal: replace the EVM with RISC-V

This post proposes a radical idea for the future of the Ethereum execution layer, one that is equally as ambitious as the beam chain effort is for the consensus layer. It aims to greatly improve the **efficiency** of the Ethereum execution layer, resolving one of the primary scaling bottlenecks, and can also greatly improve the execution layer’s **simplicity** - in fact, it is perhaps the only way to do so.

The idea: **replace the EVM with RISC-V** as the virtual machine language that smart contracts are written in.

Important clarifications:

- The concepts of accounts, cross-contract calls, storage, etc would stay exactly the same. These abstractions work fine and developers are used to them. Opcodes like SLOAD, SSTORE, BALANCE, CALL, etc, would become RISC-V syscalls.
- In such a world, smart contracts could be written in Rust, but I expect most developers would keep writing smart contracts in Solidity (or Vyper), which would adapt to add RISC-V as a backend. This is because smart contracts written in Rust are actually quite ugly, and Solidity and Vyper are much more readable. Potentially, devex would change very little and developers might barely notice the change at all.
- Old-style EVM contracts will continue to work and will be fully two-way interoperable with new-style RISC-V contracts. There are a couple ways to do this, which I will get into later in this post.

One precedent for this is the Nervos CKB VM, which is [basically RISC-V](https://github.com/nervosnetwork/ckb-vm).

## Why do this?

In the short term, the main bottlenecks to Ethereum L1 scalability are addressed with upcoming EIPs like [block-level access lists](https://github.com/ethereum/EIPs/pull/9580), [delayed execution](https://ethresear.ch/t/delayed-execution-design-tradeoffs/21877) and distributed history storage plus [EIP-4444](https://eips.ethereum.org/EIPS/eip-4444). In the medium term, we address further issues with [statelessness](https://github.com/ethereum/EIPs/pull/9257) and [ZK-EVMs](https://ethproofs.org/). In the long term, the primary limiting factors on Ethereum L1 scaling become:

1. Stability of data availability sampling and history storage protocols
2. Desire to keep block production a competitive market
3. ZK-EVM proving capabilities

I will argue that replacing the ZK-EVM with RISC-V solves a key bottleneck in (2) and (3).

This is a table of the number of cycles that the Succinct ZK-EVM uses to prove different parts of the EVM execution layer:

[![download (6)](https://ethereum-magicians.org/uploads/default/optimized/2X/4/427a7b7e9276aff1ad078ff49361a4ca68157f3a_2_690x309.png)download (6)800×359 154 KB](https://ethereum-magicians.org/uploads/default/427a7b7e9276aff1ad078ff49361a4ca68157f3a)

There are four parts that take up a significant amount of time: `deserialize_inputs`, `initialize_witness_db`, `state_root_computation` and `block_execution`.

`initialize_witness_db` and `state_root_computation` both have to do with the state tree, and `deserialize_inputs` refers to the process of converting block and witness data into an internal representation; hence, realistically over 50% of it is proportional to witness sizes.

These parts can be heavily optimized by replacing the current keccak 16-ary Merkle patricia tree with a binary tree that uses a prover-friendly hash function. If we use Poseidon, we can [prove 2 million hashes per second](https://x.com/dlubarov/status/1845862467315920940) on a laptop (compared to ~15,000 hash/sec for keccak). There are also many options other than Poseidon. All in all, there are opportunities to massively reduce these components. As a bonus, we can get rid of `accrue_logs_bloom` by, well, [getting rid of the bloom](https://ethereum-magicians.org/t/eip-7668-remove-bloom-filters/19447).

This leaves `block_execution`, which makes up roughly half of prover cycles spent today. If we want to 100x total prover efficiency, there’s no getting around the fact that we need to at least 50x EVM prover efficiency. One thing that we could do is to try to create implementations of the EVM that are much more efficient in terms of prover cycles. The other thing that we can do is to **notice that ZK-EVM provers today already work by proving over implementations of the EVM compiled down to RISC-V, and give smart contract developers access to that RISC-V VM directly**.

Some numbers (see [here](https://arxiv.org/pdf/2504.14809)) suggest that in limited cases, this could give efficiency gains over 100x:

| download (7)800×476 154 KB | 4a3981f5-7c49-4631-9c7c-3216b4c62466583×528 33.4 KB |
| --- | --- |

In practice, I expect that the remaining prover time will become dominated by what today are precompiles. If we make RISC-V the primary VM, then the gas schedule will reflect proving times, and so there will be economic pressure to stop using more expensive precompiles; but even still the gains won’t be *quite* this impressive, but we have good reason to believe they will be very significant.

(Incidentally, the roughly 50/50 split between “EVM” and “other stuff” [also appears in regular EVM execution](https://www.paradigm.xyz/2024/04/reth-perf), and we intuitively expect that the gains from removing EVM as “the middleman” should be similarly large)

## Implementation details

There are a number of ways to implement this kind of proposal. The least disruptive is to **support two VMs, and allow contracts to be written in either one**. Both types of contracts would have access to the same types of facilities: persistent storage (SLOAD and SSTORE), the ability to hold ETH balances, the ability to make and receive calls, etc. EVM and RISC-V contracts would be free to call into each other; a the RISC-V perspective calling an EVM contract would appear from its perspective to be doing a syscall with some special parameters; the EVM contract receiving the message would interpret it as being a CALL.

A more radical approach from a protocol perspective is to **convert existing EVM contracts into contracts that call an EVM interpreter contract written in RISC-V that runs their existing EVM code**. That is, if an EVM contract has code C, and the EVM interpreter lives at address X, then the contract is replaced with top-level logic that, when called from outside with call params D, calls X with (C, D), and then waits for the return value and forwards it. If the EVM interpreter itself calls the contract, asking to run a CALL or SLOAD/SSTORE, then the contract does so.

An intermediate route is to do the second option, but create an explicit protocol feature for it - basically, **enshrine the concept of a “virtual machine interpreter”, and require its logic to be written in RISC-V**. The EVM would be the first one, but there could be others (eg. Move might be a candidate).

A key benefit of the second and third proposal is that they **greatly simplify the execution layer spec** - indeed, this type of idea may be the *only* practical way to do that, given the great difficulty of even incremental simplifications like removing SELFDESTRUCT. Tinygrad has the hard rule of [never going above 10000 lines of code](https://x.com/__tinygrad__/status/1863898910387003694); an optimal blockchain base layer should be able to fit well within those margins and go even smaller. The beam chain effort holds great promise for greatly simplifying the consensus layer of Ethereum. But for the execution layer to see similar gains, this kind of radical change may be the only viable path.

## Replies

**benaadams** (2025-04-20):

A difficulty of going as low level as a cpu architecture for the VM means it’s difficult to optimize back up

So at the moment the `UInt256` operations in the Evm are usually implemented with `Avx2` or `Avx512` (equivalent on Arm); operating with 256bit or 512bit registers.

If that was decomposed to RISC-V 64bit or worse 32bit instructions; that then becomes a extremely hard problem to recognise the patterns and then recompose back to 256bit operations when the RISC-V code is then run on AMDx64 or ARM64 that most blockbuilders and validators will be running (as there is currently no high performance RISC-V hardware).

C/C++ compilers; which spend a long time compiling, have a hard time doing auto-vectorisation in this way; and they only auto-vectorize simple repetitive structures, they don’t recognise entire algorithms and convert them to a totally different form (which is normally the case with using specific CPU SIMD instructions effectively).

The risk here is that zk-proving may get better, but blockbuiling and execution will deteriorate significantly?

---

**pcaversaccio** (2025-04-20):

Hmm, so if I understood correctly, the basic idea is that proving basic RISC-V instructions (simple adds, moves, comparisons) might be much quicker & easier for ZK systems than proving the complex EVM execution step. Generally, that makes sense I think. But what about all the *other* stuff needed to actually run smart contracts? Like, I’m thinking about standard RISC-V features like integer multiplication and especially division, or more complex bit manipulation instructions. And crucially, what about the special `syscalls` needed to interact with Ethereum’s state, like reading/writing storage (`SLOAD`/`SSTORE`) or making calls? How hard are *those* specific things to prove in ZK? Is there a risk that even if the basic instruction proving gets faster, these necessary extras (especially things like division, or maybe even floating-point or vector math if they were ever added) could become the new major bottlenecks, essentially the new *hotspots* that dominate the proving time?

---

**AdamCochran** (2025-04-20):

I think the simplicity argument makes a lot of sense.

But, taking a step back, I think it raises the question of what is Ethereum’s priority purpose right now?

L1 execution, simplicity, decentralization, or L2 enablement?

This would be great for L1 execution, but that lowers the value add of L2s, competing against ourselves, and doesn’t add much value to that roadmap in exchange for a huge technical lift.

It seems like there are a lot of other ambitious pie in the sky efforts that could either improve drastically the execution for L2s or have more moderate boosts for both L1 & L2

- Blob‑only data model + mandatory danksharding
- Recursive‑proof aggregation precompile (“VERIFY_RECURSIVE” / “AGGREGATE_SNARKS” – folds N rollup proofs into one SNARK so the slot verifies a single proof)
- Unified prime‑field crypto stack & BLS signatures (Adopt a single curve—e.g., BLS12‑381—for user sigs, KZG commitments, and SNARK verifiers. + Poseidon/Rescue hash precompile in the same field.)
- Stateless KZG / IPA commitment root (Replace the Merkle Patricia/Verkle tree with a polynomial commitment of the full state vector)
- Enshrined global message bus (native inbox/outbox for all L2s)
- Sequencer‑level PBS (proposer‑builder separation at the rollup block level)
- BLS aggregate‑signature mempool (Mempool nodes accept only bundles where thousands of user or rollup signatures are pre‑aggregated into one BLS sig)

Where as RISC-V move seems to 50x - 100x L1 execution, but very little benefit for the L2 model.

**TL;DR**:

-agree it seems like a good idea for the L1 that solves points 2 and 3 of the L1 bottlenecks.

-but is this the set of priorities we want to solve for, especially given the scale of technical cost here?

That I don’t have the answer for, but thought it was worth raising the question!

---

**levs57** (2025-04-20):

### Please don’t.

Hi.

This is not a good plan, largely based on wrong priors about proof systems and their performance.

### Checking the assumptions

As far as I understand the argumentation, main arguments are (1) scalability and (2) maintainability.

At first, I would like to address **maintainability**.

Realistically, all RISC-V zk-VMs use precompiles to perform the computationally intense operations. List of SP1 precompiles can be found here: docs.succinct.xyz/docs/sp1/writing-programs/precompiles , you can see that it includes pretty much every relevant “computational” opcode from EVM.

Therefore, any change to cryptographic primitives of the base layer will require writing and auditing circuits for these precompiles. This is a severe restriction.

It is correct, indeed, that maintenance of “out-of-EVM” part of the execution client plausibly becomes relatively easy if performance is *good enough*. I am not exactly sure if it is good enough, either, but this part is low-confidence:

- Indeed, state tree computation can be done much faster by using a friendly precompile, such as Poseidon.
- It is less clear that you can deal with deserialization in an elegant and maintainable way.
- Also, I think there are some nasty details such as gas metering and various checks, they are probably in “block evaluation time” but realistically they are better quantified as “out-of-EVM” part (and these are mostly subject to maintenance pressure).

Second, **scalability**

To reiterate, there is no way RISC-V works without precompiles for EVM payload. It does not.

So the statement

> In practice, I expect that the remaining prover time will become dominated by what today are precompiles.

is while technically correct, is unnecessarily optimistic. It assumes there won’t be precompiles. In fact (in this future world), there will be exactly the same set of precompiles as computation-heavy opcodes that we have in EVM (signatures, hashes, possibly large modular operations).

To address Fibonacci example, it is hard to judge without digging into extremely low-level details, but at least large parts of these advantages are:

1. Interpretation vs execution overhead.
2. Loops unrolling (decreases control flow on RISC-V part, not sure if done by solidity but even if done singular opcodes still perform a lot of control flow / memory accesses due to interpretation overhead).
3. Using smaller data type.

What I want to point out here, is that to get advantages 1 & 2, you *must* kill interpretation overhead. That seems aligned with RISC-V idea, but this is not the RISC-V as we currently speak of it, rather it is something resembling (?) RISC-V capable of various things.

### So, there is a bit of a problem

1. To get plausible advantages to maintainability, you have to have RISC-V (with precompiles) that your EVM compiles to. Which is, basically, current status.
2. To get plausible advantages to scalability, you need to have entirely different beast - something (plausibly resembling RISC-V) that has the concept of a “contract”, aware of the various restrictions of Ethereum runtime, and is able to run contracts as executables, without interpretation overhead.

I am assuming, now, that you mean 2 (because it seems that the rest of the post suggests so). I urge you to realize that everything *outside* of this environment will be written on whatever thing RISC-V zkVMs are currently written in, with implications for maintenance.

### Some caveats

1. It is possible to compile the bytecode from high-level EVM opcodes. Compiler then is in charge of ensuring that the resulting program maintains invariants such as absence of stack overflow. I would like to see it demonstrated in normal EVM. SNARK of correct compilation then can be supplied together with contract deploying instruction.
2. It is possible to construct a formal proof that some invariants are preserved. This approach (instead of virtualization) is used in some browser contexts, as far as I remember. By making a SNARK of this formal proof, you can also achieve similar result.
3. Simplest option is biting the bullet and…

### Constructing a minimal “blockchain-y” MMU

I think this is probably implicit in your post, but let me clarify once again. What you actually need if you want to get rid of virtualization overhead is execution of *compiled* code. That means that you need to somehow prevent the contract (which is now executable!) from writing to the kernel (off-EVM implementation?) memory, at the very least.

So, naturally, we need some kind of MMU. Arguably, approach with pages (used in normal computers) is largely unnecessary, as the “physical” memory space is almost unlimited. This MMU, ideally, should be minimal (as it lives on the same level of abstraction as the architecture itself); though possibly some features (say, atomicity of transactions) could be moved to this level.

Provable EVM then becomes a kernel program running in this architecture.

### RISC-V might be not the best choice for the task

Interestingly enough, under all these conditions it might turn out that the actual ISA that is optimal for this task is not RISC-V, but, rather, something similar to EOF-EVM.

The reason for that is that “small” opcodes create, in fact, an extremely large amount of RAM accesses, which are hard to prove using current methods.

Similarly, to minimize branching overhead, in our recent paper Morgana (eprint/2025/065) we show how to prove the code with *static* jumps (similar to EOF) with precompile-level performance.

My recommendation is, instead, constructing a proof-friendly architecture with minimal MMU allowing to run contracts as separate executables; I don’t think it should be RISC-V; rather a separate ISA - ideally, aware of limitations dictated by SNARK protocols. Even ISA resembling some subset of opcodes of EVM will likely be better (+ as we are aware, the precompiles will be with us whether we want it or not, so RISC-V doesn’t give any simplification here).

---

**levs57** (2025-04-20):

(not sure how to edit posts here, so just write some additional thoughts)

1. LLVM has a lot of compiler bugs. Solidity, in comparison, has excellent track record. This is largely thanks to much simpler pipeline.
2. None of RISC-V vms are production ready, and their complexity is significant. Their teams might falsely claim otherwise, but, for example, SP1 recommends their customers to use a trusted prover. It came in handy when we have recently uncovered a soundness bug allowing to prove arbitrary statements.
3. @pcaversaccio this is correct intuition. The likely bottleneck is stack management (due to larger granularity of instructions), and, potentially, jumps. That being said, of course going from interpretation to execution will have huge advantages anyway, but this requires to figure out things written in my previous post.
4. @AdamCochran strongest possible support of enshrined aggregation of stateless computations.

---

**SirSpudlington** (2025-04-20):

I agree with [@benaadams](/u/benaadams) here, The EVM as a whole is very much U256 based, so abstracting down to riscv would decrease overall execution performance. From my limited STARK knowledge, I know that the AIR can be built more easily over register-based instruction sets.

The immediate first solution I think of is using a language like Cairo, or a pseudo-cpu architecture similar to risc-v but designed for emulation, e.g 256 bit registers. These solutions are somewhat adhoc and may present overt complexity when actually being implemented, but they may serve as an alternative POV.

---

**underflow** (2025-04-20):

Would agree here with [@levs57](/u/levs57), virtualization can be an intermediate step, but this will not achieve the optimal scenario (by far). Compilation to a better ISA than RISC-V will likely be needed (ala TinyRAM) given that RISC-V was never designed for verifiable computation, and then, also include a proof of correct compilation (this part may or may not be too hard, depending on trust assumptions and how far up into the compiler stack we want to prove).

Even in the case of virtualization, one would require formal proofs that (1) the virtualized RISC-V EVM code is correctly implemented (i.e., it follows the EVM specs), (2) the RISC-V circuits themselves correctly follow the RISC-V specs, (3) a formal proof that the RISC-V circuits, I/O, memory-checking mechanisms (for RAM and registers), and bootloading mechanisms (for program initialization) satisfy both completeness and soundness so no invalid proof will be accepted, and lastly (4) a formal proof that the verifier itself is indeed sound, building on top of (3).

However, part of the challenge of building these formal proofs include that the circuits and proof systems are ever changing in the current landscape, so before investing deeply into doing this, one would want to fix a zkVM architecture – but by the time this effort is completed, such an architecture may now be deemed outdated.

---

**underflow** (2025-04-20):

[additional thoughts]

Having said the above, I do think the original proposal is worth seriously pursuing – that in fact, we’re doing at Nexus, however reaching true scalability and maintenance will be a hard and long task, and one will eventually need to indeed (1) provide a better ISA than RISC-V, (for the Nexus RISC-V zkVM, we’ve explored this direction, in the lines of a simple “Universal Turing Machine” designed, particularly, for verifiable computation, but this in experimental stages), and (2) provide proofs of correct compilation, which require carefully specifying and mapping the invariants.

---

**malik672** (2025-04-20):

This is not true in anyway and short sighted, a register based system will be way faster than a stack based one bseides there’s literally no difference, you can emulate U256 via limbs(that’s how it’s mostly done anyway)

---

**malik672** (2025-04-20):

Those one are like the easiest, I urge you to read the risc-v specs just for the 32 bits: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-118.pdf

for syscalls we can just ECALLS(which are already already control by design)

---

**malik672** (2025-04-20):

MTER :  make the EVM RISC

---

**SirSpudlington** (2025-04-20):

I was not stating that stack-based architectures are faster, they’re are not (in most cases), merely that it would be inefficient to use serveral cycles to compare and add 8 different U256 limbs, and that either an extention or modification to the risc-v architecture to have U256 registers may be better for optimisation.

I edited the above post for clarification.

---

**GCdePaula** (2025-04-20):

**Yes, please ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=12)![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=12)**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> replace the EVM with RISC-V

What ISA exactly in the RISC-V family were you considering?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> One precedent for this is the Nervos CKB VM, which is basically RISC-V.

Another one, more mature, is the [Cartesi Machine](https://github.com/cartesi/machine-emulator), which is proper RISC-V. Specifically `rv64gc` — it even boots Linux and runs Doom!

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adamcochran/48/14905_2.png) AdamCochran:

> but very little benefit for the L2 model.

If the L2s also become RISC-V, keeping L1 compatibility, wouldn’t they see (in their execution environment) a similar speedup?

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/levs57/48/14899_2.png) levs57:

> run contracts as executables, without interpretation overhead.

I really don’t get this part, can you give more details?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/levs57/48/14899_2.png) levs57:

> LLVM has a lot of compiler bugs.

The scale at which LLVM and GGC are used is ridiculously higher than the Solidity compiler. I believe this is one of the most important metrics for security. Personally, I’d bet on LLVM and GCC. If that’s not enough, there’s always CompCert, which also targets RISC-V.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/levs57/48/14899_2.png) levs57:

> None of RISC-V vms are production ready

Perhaps true for zkVMs, but not true for non-zkVMs.

---

**vbuterin** (2025-04-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/levs57/48/14899_2.png) levs57:

> None of RISC-V vms are production ready, and their complexity is significant. Their teams might falsely claim otherwise, but, for example, SP1 recommends their customers to use a trusted prover. It came in handy when we have recently uncovered a soundness bug allowing to prove arbitrary statements.

Sure, but this is a limitation on the existing EVM too. ZK-EVMs today *are written as ZK RISC-V plus an EVM implementation in RISC-V*. And this trend seems to be solidifying more and more over time. So exposing RISC-V to the user directly cuts out the middleman.

> I urge you to realize that everything outside of this environment will be written on whatever thing RISC-V zkVMs are currently written in, with implications for maintenance.

Today, the parts other than VM execution are written in (or rather, compiled down to) RISC-V.

> The EVM as a whole is very much U256 based, so abstracting down to riscv would decrease overall execution performance

The important point here is that most of the *usage* of the EVM is not u256 based. The great majority of values that the stack deals with are u32 or u64, balances are u128. And so the HLL code that devs write can be compiled down to something that uses the smaller-sized RISC-V instructions and gets the benefits of doing so directly.

---

**SirSpudlington** (2025-04-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> The important point here is that most of the usage of the EVM is not u256 based. The great majority of values that the stack deals with are u32 or u64, balances are u128.

Now that I think about it a bit more, having a 32-bit ISA allow for easier proving via fields like goldilocks, so it would probably be a better trade off having easier proving at the cost of VM cpu cycles.

---

**pkieltyka** (2025-04-20):

I know it’s a stretch, but what about considering EVM+/Stylus by the Offchain Labs team as the future L1 execution layer? It offers full EVM bytecode compatibility that runs in a WASM VM, and allows any WASM-targetable language like Rust, with significant performance improvements, while maintaining full interoperability with EVM bytecode contracts at runtime. Feels likejj the easiest upgrade path while maintaining compatibility.

---

**eigmax** (2025-04-21):

[repost to fix an ambiguity]

1. If we use Poseidon, we can prove 2 million hashes per second on a laptop (compared to ~15,000 hash/sec for keccak). this is an issue of the MPT, but nothing to do with any ISA (EVM bytecode, RISCV or MIPS). Strongly agree with supporting the zk-friendly hash function and make it possible to align the prover’s cost with the gas used.
2. notice that ZK-EVM provers today already work by proving over implementations of the EVM compiled down to RISC-V, and give smart contract developers access to that RISC-V VM directly.. On ethproofs, please notice that ZKM is MIPS based, and ZKM’s cycles is far way less than others. This is due to keccak sponge precompile and MIPS ISA.
3. Should EF maintain its own RISCV instruction set, compiler and other toolchains? like static analyzer, linter, etc. Or reuse LLVM? Since it claims a RISCV VM, if I compile a CPP program into RISCV, should I be able to use this library in the VM interpreter? we have an example here to demo how to use a CPP static library in zkMIPS (unfortunately links is not allowed to be included here). I say this cause if we are saying supporting RISCV, we are supporting a general purpose backend of any compiler that has supported.
4. If RISCV becomes mass adopted by all miners for snarkifying everything, this means block producer can generate the proof of the block, and all other validators just verify the proof instead of re-executing the block. Will overall computing power for prove-and-verify be less than mine-and-validate and when?

---

**MASDXI** (2025-04-21):

If EVM transitions to RISC-V VM, I think it’s similar to the concept of the [revive](https://github.com/paritytech/revive) to run Solidity on PolkaVM which is RISC-V VM.

---

**elevenarms** (2025-04-21):

[@vbuterin](/u/vbuterin) this is an awesome idea.

Realizing the full potential of a global distributed computer is fundamentally constrained by Layer 1 transaction throughput. While L2 solutions are vital, enhancing core L1 performance remains crucial for broader adoption and further success.

**A key advantage of RISC-V is its defined extensibility. We should investigate defining a set of custom RISC-V instructions specifically designed to accelerate core, performance-critical EVM opcodes.**

RISC-V’s open nature permits specialized hardware implementations (ASICs, FPGAs) beyond generic CPU execution. This offers a path to significant L1 TPS improvements by accelerating core EVM logic directly in silicon, potentially orders of magnitude faster than current software interpretation or JIT approaches.

Verifiability & Security: The modularity and clean design of RISC-V lend themselves more readily to formal verification methods compared to complex legacy ISAs. A formally verified RISC-V core executing EVM logic could provide much stronger guarantees about runtime behavior, crucial for securing high-value smart contracts.

It would be great for the community to Initiate focused research tracks and working groups to:

- Benchmark existing EVM implementations against potential RISC-V software models. @MASDXI - revive/PolkaVM looks great - it currently only targets RV32EM which is worth discussion.
- Identify high-impact EVM operations suitable for custom RISC-V instruction acceleration.
- Develop proof-of-concept RISC-V models (FPGA/emulation) with custom EVM extensions.
- Engage with the RISC-V community on standardization potential for blockchain-specific extensions.
- Evaluate the formal verification advantages and challenges.

**RISC-V, potentially enhanced with custom EVM-centric instructions, offers a compelling path towards a more performant, secure, and scalable Layer 1** ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**dilrong** (2025-04-21):

Vitalik Buterin claims that replacing the Ethereum Virtual Machine (EVM) with RISC-V could improve zero-knowledge (ZK) proof efficiency by 50 to 100 times. However, is RISC-V truly superior? The EVM has been a stable, battle-tested environment for approximately nine years, while RISC-V lacks substantial real-world experience in blockchain execution contexts. Although PolkaVM has adopted RISC-V, I believe it has not been adequately validated, as it has yet to be thoroughly proven on a mainnet.

The EVM is specifically optimized for smart contract execution, whereas RISC-V, designed as a general-purpose architecture, may lack tailored optimizations for blockchain use cases. While RISC-V’s versatility allows the use of programming languages from other blockchains, Vitalik himself noted that improvements leveraging existing Solidity are preferable. Transitioning the entire ecosystem to a new architecture is a daunting challenge.

Implementing RISC-V in software inevitably leads to performance degradation. Using an emulator for software-based execution raises doubts about its ability to process tasks efficiently. On the other hand, adopting RISC-V hardware would entail significant transition costs. I believe that ZK-EVMs already provide sufficient efficiency for current needs. When considering the costs of development, the effort required for transition, and the potential for unforeseen errors, replacing the EVM with RISC-V does not seem like a compelling approach.

While transitioning to RISC-V may offer potential benefits, I argue that improving ZK-EVMs and optimizing the existing EVM are more practical and stable alternatives.


*(92 more replies not shown)*
