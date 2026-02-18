---
source: magicians
topic_id: 24455
title: "EVM 2.0: Proving-Centric vs. Execution-Centric Approaches"
author: elistark
date: "2025-06-05"
category: Magicians > Primordial Soup
tags: [evm, risc-v, cairo]
url: https://ethereum-magicians.org/t/evm-2-0-proving-centric-vs-execution-centric-approaches/24455
views: 1376
likes: 32
posts_count: 21
---

# EVM 2.0: Proving-Centric vs. Execution-Centric Approaches

# EVM 2.0 - Proving-Centric vs. Execution-Centric Approaches

This post is by StarkWare. We thank Vitalik Buterin, Tomasz Stańczak, Justin Drake, Ventali Tan, Federico Carrone (Fede), Bobbin Threadbare,  Morgan Thomas, Guilamme Ballet, Mamy Ratsimbazafy ([@mratsim](/u/mratsim)), Alexander Hicks, Kevaundray Wedderburn and Jeremy Bruestle for careful review and comments.

## Summary

We provide our outlook on the way to choose the next EVM. We see three potential routes, each presenting a different tradeoff:

1. Prioritizing fast execution and a standard toolchain at the expense of fast ZK proving,
2. Prioritizing fast proving at the expense of execution and standard toolchain, and
3. A 2-step approach that passes through a blockchain-friendly VM followed by a ZK-VM, also at the expense of standard toolchain (though not necessarily fast execution).

A few years ago Starknet faced a similar question and chose the third option. We believe this is also the best path for the next EVM. At the very least, we suggest that this option be seriously explored alongside the other options.

## Background: Rethinking the Ethereum Execution Layer

Ethereum – the “World Computer” – is the first and most successful blockchain that supports smart contracts and general computation. In a recent pair of influential posts [[1](https://ethereum-magicians.org/t/long-term-l1-execution-layer-proposal-replace-the-evm-with-risc-v/23617), [2](https://vitalik.eth.limo/general/2025/05/03/simplel1.html)], Vitalik suggests “we [replace the EVM with either RISC-V](https://ethereum-magicians.org/t/long-term-l1-execution-layer-proposal-replace-the-evm-with-risc-v/23617), or another VM that is the VM that Ethereum ZK-provers will be written in.”

The question of “which VM should we use?” is something StarkWare dealt with over the past 7 years, and as we brought more and more systems to production our insights shifted and matured. The following document, based on our collective experience, is StarkWare’s contribution to the important discussion surrounding the major architectural question that Ethereum is facing:

What should Ethereum’s next-generation execution layer look like?

This question spans multiple dimensions:

- Execution Efficiency: Can Ethereum design a VM that allows faster contract execution, lower latency for users, and better resource utilization for sequencers and full nodes?
- Provability: Should the VM be optimized for integration with zero-knowledge proofs, enabling verifiable execution and trustless scalability through zk-rollups or zk-proven Layer 1s?
- Developer Experience, Ergonomics and Safety: How can Ethereum improve language tooling, debugging, and formal verification, while ensuring the execution model is safe, deterministic, and easy to reason about?
- Open Source: As a decentralized and permissionless blockchain, it is important that whatever stack is chosen by Ethereum, it be sufficiently accessible and usable, which means open sourcing all relevant core components.
- Backwards compatibility: The current code base of Ethereum smart contracts and systems is the result of thousands of developer years, and its safety is backed by thousands of auditing years. Any VM that diverges significantly from the existing one will lead to (1) maintaining two VMs and code bases indefinitely and (2) increased costs and lower safety.

Below, we break down the main tradeoffs between execution-focused and proving-focused VM designs, evaluate the requirements for blockchain-safe execution, and explain our view for the best way to converge these different goals to form a unified architecture.

## Key Concepts

Unlike traditional computing environments, blockchain execution must adhere to strict constraints around safety, determinism, and verifiability. These constraints inform how we reason about low-level code behavior (e.g., through sanitization), runtime isolation (sandboxing), and whether a VM is optimized for zero-knowledge proofs. This section introduces these core concepts and explains why they are essential in designing a secure and scalable blockchain execution environment. After presenting these concepts we’ll dive into concrete suggestions for the next generation EVM.

### Blockchain Execution Safety

When executing blockchain transactions, the question of safety arises, as we wish to ensure smooth, safe and consistent execution across a diverse range of platforms. Safe execution requires, among other things:

- Restricting direct access to host resources (e.g., file system, system calls)
- Preventing side effects outside of state transitions
- Ensuring deterministic behavior across all nodes
- Restricting resource usage, either by gas metering (as on Ethereum) or by restricting the VM itself (as on Bitcoin)

### ZK-friendliness

A ZK-friendly VM is one that is designed with efficient zero-knowledge proof generation in mind. Key attributes include:

- Minimal overhead when representing valid execution via arithmetic constraints
- Efficient memory models, avoiding dynamic access patterns or complex system-level features
- Traceability, enabling easy generation of proof witnesses
- Recursion-friendly execution, allowing proofs to be aggregated

zkVMs are virtual machines explicitly designed for efficient zero-knowledge proof generation. They prioritize structured computation, traceability, and memory determinism to enable succinct, verifiable proofs. These systems are ideal when real-time or low-latency proving is essential,

such as in ZK-rollups or on-chain verifiability.

***Note:** This short and quickly-written post omits many nuances that are crucial to the discussion, like:*

- The execution environment and the metadata that needs to be proved (Patricia-Merkle trees vs. other commitment schemes) should play an important role in the choice of the next EVM.
- Each of the topics introduced here is worthy of far greater attention (which proving system are we assuming ZK friendliness over? Should multiple proving systems and multiple finite fields be supported? etc.)

*We hope the Ethereum community undertakes this study at greater depth than what we cover here.*

# Design Options

Having explained the constraints arising from blockchain execution and from zk-friendliness, we move on to examining the architectural choices available. Broadly, these fall into three categories, each reflecting a different priority: optimizing for execution performance and developer experience; optimizing for provability; or combining the strengths of both through a layered approach. Each option introduces tradeoffs across performance, safety, tooling, backwards compatibility and future scalability. In the sections that follow, we outline what each path entails, highlight notable real-world examples, and explain how these designs respond to the challenges unique to blockchain environments.

## Option 1: Execution-Focused Blockchain VM

If the primary goal is to create a new blockchain VM that delivers high performance and developer-friendly tooling, one should lean towards making the next EVM as close as possible to an established toolchain, one that is well maintained outside of the world of blockchain. This approach prioritizes:

- Fast Execution: Native-level performance for contract execution on commonly available hardware, to minimize block production and verification compute and latency. Notice that fast execution requires optimizing much more than the CPU because in modern computers CPUs are vastly faster than memory and I/O operations.
- Developer-Friendly Tooling: Compatibility with popular languages (blockchain and non-blockchain ones), IDE support, testing frameworks, and debugging tools.

However, the blockchain specific requirement above lead to either picking a blockchain stack, or modifying a popular standard stack, to ensure the unique blockchain requirements, including:

- Deterministic, Consensus-Safe Behavior: All contract execution must be sandboxed and produce deterministic results across all nodes in the network. Execution must be isolated from host machine internals. This prohibits system calls, file access, and unrestricted memory operations.
- Safe and Predictable Resource Usage: Includes built-in gas metering, bounded memory, and restricted instruction sets — ensuring contracts don’t overconsume resources or violate consensus rules.
- Upgradeable & Modular Design: Ideally, the VM allows for upgradable components (e.g., custom precompiles, cryptographic primitives) to be added in a backward compatible way.

Examples of existing blockchain-VMs that are optimized for execution include:

### 1. FuelVM (used by the Fuel network)

- Parallelizable execution (via UTXOs)
- Minimal and analyzable IR
- Custom language (Sway) with clear control over side effects
- Strong focus on modularity.

### 2. MoveVM (used by Aptos and Sui)

- Resource-oriented programming model enforces strict ownership and prevents data races or unauthorized state mutations.
- No unrestricted global state access, reducing runtime bugs and improving safety.
- Gas metering is integrated directly at the bytecode level.
- Extremely safe and deterministic, especially in DeFi contexts.
- Good language ergonomics and analyzability.

### 3. CosmWasm (WASM for Cosmos, used by Cosmos)

- Runs smart contracts compiled to WASM in Cosmos SDK chains.
- Uses Rust + no_std, C compiled to WASM, or similar compilation paths that ensure contracts cannot access unsafe system APIs.
- Supports multi-chain deployments due to Cosmos’s IBC (Inter-Blockchain Communication).
- Built-in gas accounting and memory limits.
- Leverages the WASM ecosystem safely, while sandboxing execution in a blockchain-native runtime.
- Ideal for developers already familiar with Rust or AssemblyScript.

## Option 2: ZK-Proving Focused Language/VM

If Ethereum’s priority is to build a ZK-friendly system, then a VM explicitly designed for provability is called for. Such a VM would typically minimize circuit size, remove registers (or drastically minimize their number), enable recursion, and use a simple, well-constrained, instruction set.

Examples of existing VMs that are optimized for ZK-proving (Proper Disclosure: CairoVM is built by StarkWare, the co-authors of this writeup)

### 1. CairoVM (Used by Starknet)

- Designed from the ground up for STARK-based proof systems
- Uses a minimal, arithmetic-friendly instruction set
- Avoids problematic features like dynamic memory, indirect jumps, or system calls
- Stack-less, register-less architecture
- Paired with Sierra, a high-level, typed intermediate representation that provides safety and prevents undefined behavior.
- Compiles efficiently down to traceable, provable CASM code.

### 2. Valida VM (used by the Valida project)

- 31-bit field compatibility
- LLVM backend for compilation from high level languages, including Rust, C, WASM and more.
- Minimal instruction set, defined by degree-3 constraints
- Stack-less architecture, with direct memory manipulation

### 3. Miden VM (used by the Miden project)

- ISA with native instructions for both field and 32-bit arithmetic operations.
- Assembly language with structured control flow to simplify transpiration from WASM and enable use of WASM as an intermediate representation for higher-level languages.
- MAST (Merkelized Abstract Syntax tree)-based program representation to ensure deterministic linking and program commitments.
- Support for multiple isolated execution contexts enforced at the VM level, including separation between root and user contexts.
- Configurable kernels that enable extensibility without the need to modify the core arithmetic circuits of the VM.
- Focus on recursion-friendliness and client-side proving (i.e., relatively low memory requirements).

## Option 3: Combine Both: Blockchain-Safe Language + ZK-Friendly VM

If Ethereum’s goal is to combine ZK efficiency, execution performance, and language safety then we should first acknowledge that there currently is no widely accepted framework, used outside of blockchain, which is a natural fit. Blockchain-related requirements of sanitization and sandboxing pull in one direction, whereas ZK-friendliness pulls in another direction. Going explicitly with one direction will mean that the other one is not well served.

This is the problem that StarkWare has faced in the past, and it is worth recounting our experience. After deploying our very first product – StarkEx – in the summer of 2020, we wanted to improve it and add new features. But the way we built that first system, writing polynomial constraints by hand, couldn’t be scaled safely. Our first Turing complete VM was the Cairo VM, which was a ZK-VM but one that wasn’t blockchain-safe. At inception we envisioned only StarkWare running this VM for its customers (Dexes and exchanges) and thus the blockchain attributes of sanitization and sandboxing were enforced internally when we wrote the code for those systems.

However, when we chose to develop Starknet as a general purpose L2, the issue of blockchain-safety raised its thorny head. To address this, we opted for a 2-step approach:

- HLL → Safe blockchain Intermediate Representation (Sierra): A high level language (like Cairo in the case of Starknet, or a Solidity-like language for Ethereum) is compiled to a blockchain-safe intermediate representation (Sierra). Sierra is a structured, typed intermediate representation designed for safety, determinism, and clear semantics.
- Sierra → zkVM: The Sierra code, already safe and gas-metered, is now compiled to a ZK-friendly VM for execution, supporting highly efficient proof generation. Starknet uses the Cairo VM but any of the aforementioned ZK-friendly VMs would be suitable for this purpose.

This approach also lends itself to fast native execution. To get this, one compiles the Sierra code for native execution (e.g., on x86 machines). Indeed, this approach is used by Starknet, via the Cairo-native compiler built by LambdaClass.

This two-step approach supports:

- Safe execution (and, with native compilation, also fast execution)
- Efficient proving using STARKs and recursive proof composition
- Flexible developer ergonomics, with growing support for high-level smart contract languages

The pros of this approach are execution safety and language structure, without compromising on proving performance. The cons of this approach are that it is a programming language and compilation stack that is non-standard (outside the context of the Starknet blockchain) which means that the developer experience, existing tooling, native execution performance and the ease of onboarding of new developers are worse than for standard non-blockchain toolchains. Additionally, the equivalence of the zkVM and native execution has to be established.

# RISC-V as the next EVM - Challenges and Open Questions

Recall that what initiated this post is Vitalik’s suggestion to use RISC-V as the next EVM. To [quote Vitalik](https://ethereum-magicians.org/t/long-term-l1-execution-layer-proposal-replace-the-evm-with-risc-v/23617), his suggestion

> aims to greatly improve the efficiency of the Ethereum execution layer, resolving one of the primary scaling bottlenecks, and can also greatly improve the execution layer’s simplicity - in fact, it is perhaps the only way to do so.

The advantages of RISC-V are numerous - it is a general purpose ISA that is open source, and it has extensive tooling, good developer experience and support for numerous high level languages. Running in an emulated setting bypasses some of the main challenges having to do with gas metering, unsafe opcodes, etc. This might come at some loss of ecosystem benefits, as most RISC-V libraries assume unrestricted environments.

Which leads to the following open questions, which we suggest answering before deciding on it as the next EVM:

1. How fast will a sandboxed, sanitized and gas-metered RISC-V VM be? .
2. How efficient will zk-proofs be for the emerging code?

# Conclusion

- Using existing architectures like RISC-V requires non-trivial modifications which may compromise the benefits of fast execution.
- ZK-proving general-purpose VMs will likely be less efficient than ZK-proving ZK-friendly VMs, and comparing the efficiency of the two approaches should be part of the research process of choosing the next EVM (assuming ZK-proving is one of the new EVM’s goals)
- A 2-step approach like Sierra + Cairo should be considered alongside the other two approaches – pure standard ISA (like RiscV/MIPS/x86) and pure ZK-VM (like Valida/Cairo/Miden).

## Replies

**simpleTestnet** (2025-06-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elistark/48/7748_2.png) elistark:

> How fast will a sandboxed, sanitized and gas-metered RISC-V VM be?

CKB VM can be used to benchmark [GitHub - nervosnetwork/ckb-vm: CKB's vm, based on open source RISC-V ISA](https://github.com/nervosnetwork/ckb-vm)

More information available here

https://ethereum-magicians/t/long-term-l1-execution-layer-proposal-replace-the-evm-with-risc-v/23617/55

---

**odysseas_eth** (2025-06-08):

Polkadot has spent approx. 2+ years in developing a blockchain-native RISC VM, with attention to performance and safety. I am pretty sure though that they haven’t explored or optimized it for ZK-friendliness.

An interesting aspect of such an approach, is that one can imagine pretty easily the development of system contracts which implement popular VMs like the EVM.


      ![image](https://europe1.discourse-cdn.com/flex005/uploads/polkadot2/optimized/1X/b9cc9861ba6191f242df592276ca071e38fa4818_2_32x32.png)

      [Polkadot Forum – 30 Aug 23](https://forum.polkadot.network/t/announcing-polkavm-a-new-risc-v-based-vm-for-smart-contracts-and-possibly-more/3811)



    ![image](https://europe1.discourse-cdn.com/flex005/uploads/polkadot2/original/1X/6ea9950aed34af4aa14a3bbe5ce85549b54278a1.svg)



###





          Tech Talk






            wasm
            smart-contracts







(This is a continuation my previous forum topic; I’m posting this as a new thread to start with a clean slate, and for extra visibility.)  After many weeks of work I have the pleasure to announce the release of PolkaVM 0.1, a tech preview of our...



    Reading time: 47 mins 🕑
      Likes: 215 ❤

---

**EugeRe** (2025-06-11):

Hey [@elistark](/u/elistark)  I have a question. How would you evaluate ligetron zkvm into the different described implementations? [CSDL | IEEE Computer Society](https://www.computer.org/csdl/proceedings-article/sp/2024/313000a086/1RjEaU3iZEY)

---

**elistark** (2025-06-13):

what’s your tl;dr for this?

---

**elistark** (2025-06-13):

Where can I read more about this VM? It’s not my specialty but can ask the team for a back-of-envelope assessment.

---

**EugeRe** (2025-06-13):

[@elistark](/u/elistark) I am attaching their supposed publication in the IEEE explore here: https://ieeexplore.ieee.org/document/10646776

Many thanks! ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

---

**MASDXI** (2025-06-17):

CKB and FuelVM offer high performance for token transfers thanks to their UTXO-based models. However, when it comes to smart contract interactions, they still require conflict detection and resolution, which limits parallelism.

Adding a UTXO layer to a smart contract-capable platform can make sense. But if the primary goal is simply to speed up transaction transfer execution, this approach starts to resemble Avalanche’s architecture—where different chains or virtual machines are separated by purpose (e.g., transfers on the X-Chain, contracts on the C-Chain).

---

**simpleTestnet** (2025-06-17):

CKB VM is a pure software implementation of the RISC-V instruction set. Right now it implements full IMCB instructions for both 32-bit and 64-bit register size support.

Right now CKB VM has 2 different modes, a Rust interpreter mode and an Assembly based interpreter mode(ASM mode)

However, a native dynasm-based AOT VM ( /github.com/nervosnetwork/ckb-vm-aot), and an LLVM-based closed-to-native AOT VM have also been implemented, more information can be found here xuejie.space/2022_09_08_a_journey_to_the_limit/),

The VM is metered in compute cycles according to this

/github.com/nervosnetwork/rfcs/blob/master/rfcs/0014-vm-cycle-limits/0014-vm-cycle-limits.md

Appreciate your reply, please share any questions!

---

**sorpaas** (2025-06-18):

For the LLVM AOT of CKB VM, have you measured compile time? Because that’s usually where the problem is – the runtime will definitely be really fast, but now compile time is slow.

---

**simpleTestnet** (2025-06-19):

Yeah the LLVM AOT version of CKB-VM has a slow compilation time, something like 3 seconds for secp256k1 case.

That being said, the 3 second time is measured when compiling in a single thread environment. There are definitely work arounds:

- Use more cores for compilation
- Switch to cranelift instead of LLVM, the runtime performance might be slightly slower but compilation time will be faster

---

**sorpaas** (2025-06-19):

I’m always quite skeptical if such thing will ever work. In general, JIT/AOT in a blockchain environment can only be single-pass. Otherwise we run into the problem of “JIT bomb”. There can be short program specifically designed to compile slowly on a JIT implementation. In Web2 it’s no big deal because one can just kill the process. In blockchain it’s a security issue.

Cranelift suffers from the same problem in that it’s not single-pass.

Revm/Reth team has a JIT for EVM called `revmc` that suffers from the same problem. The runtime is now really fast, but the compile time is slow.

This just means I think your existing single-pass CKB VM AOT is probably already the best that can be done (but of course, benchmark shows that the code itself can still be further optimized). But the thing is, we can’t really apply much more compilation steps (and therefore no further optimization opportunities).

This means that blockchain JIT/AOT must be really close to native architecture. RISC-V is good, but also if someone does native x86_64 (eBPF!?), then it will work good as well.

On the other hand, things are not so bright regarding EVM JITs. My opinion is that we’ll never be able to JIT regular EVM. Yes we can get faster runtime, but then it’ll be really slow compile time. Or we do single-pass and the performance benefits will be really small (let alone all the extra costs of 4x contract sizes and such). Regular EVM is probably always better to stay interpreted.

---

**xxuejie** (2025-06-20):

In a sense you are correct, a JIT will always suffer from JIT bomb. And yes, it will really be ideal that a singlepass compiler be used in a blockchain environment. LLVM and cranelift both suffer from the bombing issue.

However, I do want to provide my insights in 2 directions:

- Let me just say that I do believe there is a huge gap between our initial single-pass CKB VM AOT (/github.com/nervosnetwork/ckb-vm-aot) and the LLVM-based AOT (xuejie.space/2022_09_08_a_journey_to_the_limit/). The first one is a naive attempt modeling after an interpreter, while the latter one uses an architecture that matches x64 native code more closely. I do believe it is possible that we can take the architecture in the LLVM-based AOT, but instead use a singlepass compiler design that translates RISC-V to native code in linear time. It is true that such a design might not achieve the performance number from the LLVM-based AOT, but my bet is that it will be much better than our original CKB VM AOT. So I would doubt the claim that “your existing single-pass CKB VM AOT is probably already the best that can be done”. A typical RISC-V binary already contains many close-to-the-metal optimizations done by compilers, which is quite different from EVM binaries. All we need to do here, is a way to match RISC-V instructions to x64 instructions in a overhead-free way.
- This argument does not apply to Ethereum, but just want to provide a complete pictures in our design: these days blockchains really come in all shapes. While for a L1 blockchain, singlepass makes a lot of sense, everyday we see L2 blockchains or even other L1 blockchains that are happy with a JIT based architecture. Our belief is that the LLVM-based CKB-VM AOT can perfectly suit those environments, while at L1(in both CKB and Ethereum), I do agree a singlepass compiler might be the right way to go.

> RISC-V is good, but also if someone does native x86_64 (eBPF!?), then it will work good as well.

Now it’s time to share some stories behind our original choice of RISC-V:

Back in 2018 - 2019 when we first designed CKB-VM, there are already other ISAs that are like RISC-V, some are even simpler and easier to implement than RISC-V. One can also argue that eBPF falls in this category. In a way, we can argue that any native ISA(just to be precise, personally, I don’t consider EVM or WASM to be native ISAs) could be a good choice, and all the techniques used in one ISA, can always be ported to another. We end up with RISC-V due to several reasons:

- Simpler ISAs do have fewer instructions and are easier to implement. But there is actually always a threshold you need to meet to efficiently express all cryptographic algorithms. I remember there was one time that EVM does not have bit-shifting operations, and it takes a lot of gases for heavy bitwise computations. This works as a good example that you want the ISAs to be not too simple nor too complex. Even if we add 64-bit integer types to EVM today, you will still need to add a considerable amount of operations(not just add/sub/mul) to make math-heavy programs performant enough. Another such example is: CKB-VM actually started out as a 32-bit RISC-V machine for simplicity. But as we build more programs on CKB-VM, it is clear to us that the programs could benefit a lot in performance with 64-bit instructions. On the other hand, almost all moderm machines run on 64-bit CPUs, and it would really be a waste of resources if we only allow 32-bit operations: to a modern CPU, both a 32-bit add and a 64-bit add finishes in one cycle in the ideal case. eBPF, to me also falls in this category, I would encourage one to compare standard eBPF instructions (/www.ietf.org/archive/id/draft-thaler-bpf-isa-00.html) to RISC-V Bitmap instructions(/github.com/riscv/riscv-bitmanip). I do understand it might not be fair comparing eBPF core instruction set to a RISC-V extension, but note that all RISC-V CPUs in the future will already support bitmap instructions(/riscv.org/riscv-news/2024/10/risc-v-announces-ratification-of-the-rva23-profile-standard/), so in a way it is no longer an extension, but part of the standard.
- Another part of the story is that we don’t want to keep maintaining a fork of compiler toolchain for our ISA of choice. A major goal of CKB-VM, is that it shall be possible to build CKB-VM programs with standard off-the-shell compiler suites without any patches. And back at the time, it really seemed that RISC-V has caught the most momentum. Today, I think it’s safe to say we have made the right choice: tons of devices ship with RISC-V cores inside(/riscv.org/wp-content/uploads/2024/12/Tue1100_Nvidia_RISCV_Story_V2.pdf), the support for RISC-V in LLVM, Rust and many compiler suits has caught up. To me, RISC-V is no longer a weird ISA, but one of the most widely use ISAs in the whole computer industry. I think blockchains can also benefit from the share ecosystem.

So those are why we want to bet on RISC-V: the ecosystem is already big enough, it is also similar enough to x64 / arm64 underneath, so I do believe we can build more performant singlepass translation compiler, compared to higher level solutions such as EVM or WASM.

---

**koute** (2025-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> This just means I think your existing single-pass CKB VM AOT is probably already the best that can be done (but of course, benchmark shows that the code itself can still be further optimized). But the thing is, we can’t really apply much more compilation steps (and therefore no further optimization opportunities).

If you want to use vanilla unmodified RISC-V *and* you want single-pass recompilation into native code then you’ll always have a non-insignificant amount of execution time overhead, but you can still get *relatively* fast-ish. FWIW, my initial RISC-V to amd64 single-pass recompiler that I wrote in two days (which essentially translated RISC-V almost 1-to-1 into amd64) achieved a 5x slowdown compared to native execution, so that’s probably the rough limit of how fast you can go on this particular benchmark (YMMV depending on the benchmark, of course).

For comparison, PolkaVM achieves ~1.7x slowdown (which is similar to how fast non-singlepass WASM VMs can go) on this benchmark compared to native, while also having pure single-pass recompilation, and AFAIK is the current state-of-art when it comes to single-pass recompiler VMs.

I already said this somewhat in the other thread, but let me repeat it more explicitly - if Ethereum wants to switch to a VM which 1) [has a spec](https://graypaper.com), 2) [has 30+ independent implementations currently being written](https://graypaper.com/clients/), 3) supports upstream toolchains and normal programming languages which people use, 4) [achieves near-native execution speeds](https://github.com/paritytech/polkavm/blob/master/BENCHMARKS.md), 5) is designed to be secure, 6) achieves state-of-art singlepass recompilation speeds (faster to recompile the code from scratch than BLAKE3 hash it), 6) can run normal programs with minimal modifications on-chain (we’ve recently ran Quake *on-chain* at full speed), 7) will support *secure* gas metering, then you’re welcome to use PolkaVM instead of reinventing the wheel with yet another RISC-V VM. I know this won’t happen for political reasons, but nevertheless, the offer officially stands.

---

**sorpaas** (2025-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xxuejie/48/15020_2.png) xxuejie:

> While for a L1 blockchain, singlepass makes a lot of sense, everyday we see L2 blockchains or even other L1 blockchains that are happy with a JIT based architecture. Our belief is that the LLVM-based CKB-VM AOT can perfectly suit those environments, while at L1(in both CKB and Ethereum), I do agree a singlepass compiler might be the right way to go.

Can you explain more how this works in practice? Is it like spawning new threads for LLVM AOT and if it takes too long, kill it and fallback to interpreter?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/koute/48/14955_2.png) koute:

> then you’re welcome to use PolkaVM instead of reinventing the wheel with yet another RISC-V VM

It would honestly be great if you can do a diff of PolkaVM vs RISC-V.

---

**koute** (2025-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> It would honestly be great if you can do a diff of PolkaVM vs RISC-V.

What do you mean by “diff of PolkaVM vs RISC-V”? Compare the performance? Or describe what exactly I changed (and how) vs vanilla RISC-V to make PolkaVM?

---

**sorpaas** (2025-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/koute/48/14955_2.png) koute:

> Or describe what exactly I changed (and how) vs vanilla RISC-V to make PolkaVM?

This! I know what PolkaVM changed in the early days, but not sure if you have also modified other things since then?

---

**xxuejie** (2025-06-20):

> Can you explain more how this works in practice? Is it like spawning new threads for LLVM AOT and if it takes too long, kill it and fallback to interpreter?

Yeah that is one way to go, another solution is after deployment of a contract, the interpreter can first handle calls, and when the AOT in the background finishes, the AOT then starts handling calls.

---

**elistark** (2025-06-20):

just read the abstract. According to it, they arithmetize and prove WASM, so this is the 1st approach, of taking a standard execution VM and ZK proving it. Applied in this case to WASM.

---

**EugeRe** (2025-06-20):

All clear, many thanks for clarifying that. [@elistark](/u/elistark)

---

**sorpaas** (2025-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xxuejie/48/15020_2.png) xxuejie:

> Yeah that is one way to go, another solution is after deployment of a contract, the interpreter can first handle calls, and when the AOT in the background finishes, the AOT then starts handling calls.

This pattern sounds really interesting to me because we’re able to break all those constraints about JIT/AOT on a blockchain. Basically we have:

- A main thread that handle normal block/transaction processing. It uses already compiled blob when available, or interpreter as fallback.
- An optimization thread in the background that gradually optimizes contracts in the state.

We can imagine that the optimization thread would first try a simple (inefficient) one-pass AOT, and when time permits, try an advanced LLVM AOT with aggressive optimization.

I would say this feels like when we first used GC for memory management. It will be a complicated beast, but whoever managed to implement it gains great advantages because then we’re not constrained by single-pass and all optimizations become possible.

I would even argue that if we ever find a proper algorithm (so that we efficiently select the next contract, skip JIT bomb contracts and do reasonable gas metering for all situations), then this will even make PolkaVM obsolete, because now we can use a more complex non-single-pass-optimized instruction set for better storage efficiency.

But the open question is still whether such algorithm is actually possible…

