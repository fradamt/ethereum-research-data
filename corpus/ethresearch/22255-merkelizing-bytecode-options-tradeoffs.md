---
source: ethresearch
topic_id: 22255
title: "Merkelizing Bytecode: Options & Tradeoffs"
author: ihagopian
date: "2025-05-02"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/merkelizing-bytecode-options-tradeoffs/22255
views: 403
likes: 6
posts_count: 3
---

# Merkelizing Bytecode: Options & Tradeoffs

*Thanks to Jochem Brouwer, Sina Mahmoodi, Thomas Thiery, Rahul Guha, Carlos Perez, Guillaume Ballet for their review and feedback.*

**TL;DR:**

- This post provides a broad perspective on solutions for a well-known worst-case scenario involving L1 snarkification: bytecode chunking.
- Upcoming L1 scaling and other protocol changes exacerbate this worst-case scenario. While these changes must continue, it’s important to start thinking about how to address future SNARKification challenges.
- As time passes and Ethereum evolves, there is increasing diversity of opinion among core developers and researchers regarding the risks associated with significant protocol changes, so it is important to deeply explore the nuances of every potential solution.
- The goal of this document is to:

Survey potential solutions to this problem, ranging from least to most complex, highlighting the distinct tradeoffs of each.
- Raise awareness, encouraging more people to consider it and propose even better solutions.

This doesn’t require immediate action (e.g., “Glamsterdam”) — even apparently simple solutions need thorough analysis to determine the best path forward.

This document explores solutions to the worst-case scenario for block proving: contract bytecode required in execution traces. This problem is longstanding, with various proposed solutions. As time passes, protocol changes are evaluated differently regarding UX impact and risk, so a more detailed understanding of tradeoffs is helpful.

# Background & Motivation

This is an introductory section for readers unfamiliar with this issue. If you are already familiar with it, feel free to skip it.

## Why block-execution proving?

A justification for why Ethereum needs more execution throughput can be found in a [recent post](https://vitalik.eth.limo/general/2025/02/14/l1scaling.html) from Vitalik. Raising the gas limit increases block verification load linearly, requiring more computational and storage resources from attestors, which conflicts with Ethereum’s core values like decentralization and trustlessness.

Execution proofs change this relationship from linear to sub-linear, allowing safer gas limit increases without impacting attestors by shifting the workload to block proposers. This is a significant step toward safer execution throughput increases, though it doesn’t solve all scaling issues, e.g., state growth.

## Block proving hardware and proving efficiency

While block proofs offload work to block builders, minimal hardware requirements for provers have a limit. Block proving has a 1-out-of-N assumption (one honest prover ensures liveness and censorship resistance). As with any 1-out-of-N assumption, at some point, the Ethereum community should decide how many honest and independent provers are required to feel comfortable with this assumption.

This hardware budget limits the maximum gas limit the network can set, so minimizing the worst-case use of the gas limit is key. Reducing the gap between average and worst-case scenarios increases network efficiency, allowing for a lower prover budget for a given gas limit.

The two main bottlenecks for provers are contract code (bytecode) proving and mispriced opcodes/precompiles. This document focuses on the former.

## Why is contract code a bottleneck

Currently, each account bytecode is committed in a code-hash (`keccak(bytecode)`) field in the account Merkle Patricia Trie (MPT), so verifying slices of a bytecode requires providing all of it i.e., the hash can only be calculated from the complete bytecode.

This is inefficient for block proving, as transactions typically only use a fraction of a contract’s code. For instance, ERC-20 token transfers don’t involve minting code. Similarly, opcodes like `EXTCODESIZE`, which return the contract size, necessitate the entire bytecode to compute the length, as contract sizes aren’t stored directly in the tree.

For example, with the current 36M gas limit, the worst-case scenario is a block with one transaction using 36M gas to repeatedly execute `EXTCODESIZE` targeting contracts with the maximum size (currently 24KiB).  For the current 36M gas limit, the prover would be forced to hash ~338MiB of data (~`36M/2500*24KiB` by using [EIP-2930](https://eips.ethereum.org/EIPS/eip-2930)).

This isn’t a very complicated theoretical attack — some months ago, I ran a 9x downgraded attack in mainnet to check the impact on Ethproofs provers. I spent $25 ([offending tx](https://etherscan.io/tx/0x6f1a12c7f5f4abd42e267c9e32ad2eb96dd3e1b41ec38056b1a2fe2e4fa7490b), [attacked block](https://ethproofs.org/block/21895000)), and provers spent between 3x and 5x longer than average for their proofs or crashed in the process.

Note also that it isn’t only an `EXTCODESIZE` attack vector — any `CALL`-like that touches a single bytecode of a contract forces the prover to include the whole bytecode in the witness. Using `EXTCODESIZE` is just the simplest way to trigger the attack.

The worst case for different gas limits is the following:

- 36M gas = ~338MiB of data to keccak.
- 60M gas = ~563MiB of data to keccak.
- 100M gas = ~939MiB of data to keccak.
- 300M gas = ~2.8GiB of data to keccak.

Note that if the protocol increases 24KiB max contract size to 256KiB, we must multiply each case by ~10x.

I’m collaborating with [@kevaundray](/u/kevaundray) to let all zkVMs reproduce this (and other) worst-case scenarios as block tests across different gas limits and maximum contract sizes. Doing so lets zkVM teams see precisely how these extremes affect their architecture, ensuring that both engineering and protocol design are guided by concrete, reproducible metrics.

# Solutions

There are two approaches to solving the bytecode problem in the context of block proving: out-of-protocol and in-protocol.

Note that there is no perfect solution; each solution increases complexity in exchange for benefits. This document explores many possibilities, leaving the final decision to a future ACD. The solutions are ordered by ascending complexity.

## Out-of-protocol workaround

The least invasive approach is no protocol changes, but more than a solution, it is a workaround. Reth’s [Ress client](https://www.paradigm.xyz/2025/03/stateless-reth-nodes) is partially stateless, storing only bytecodes and not the rest of the state (nonces, balances, storage slots). Block provers, assuming verifiers have contract bytecodes, only need to prove code hash correctness, not the bytecode data itself.

Pros of this solution:

- There are no core protocol changes (this is a big benefit), just supporting proof distribution on the network.

Cons:

- Clients aren’t stateless but partially stateless, requiring ~10GiB of data. This requirement will continue to grow as the chain evolves, and the pace of growth will increase with increased gas limits or maximum contract sizes. This space is still relatively low for most validators, but it might exclude other very low-powered devices (e.g., smartphones).
- Block verifiers can download all contract bytecodes before joining the blockchain, but without extra trust assumptions, they can’t know the data is complete — they might need to fetch missing contract bytecodes from other network nodes. This fetching process is time-unbounded, introducing network dependencies in the block verification pipeline.
- This makes the solution unsuitable for network attestors with a strict deadline for block attestation. This is not a problem for nodes that aren’t attestors, e.g., only verifying the chain.
- Both proof and bytecode serving depend on the honesty of network nodes — compared to a full protocol solution, block proposers must include the proof within the block.

Although the above list has many cons, we can’t ask more from this solution, considering it doesn’t require any protocol change.

Nodes could mitigate these drawbacks by downloading all contract bytecode from a trusted source, ensuring no missing bytecode necessitates future network calls. This trust assumption could be eliminated by including an append-only Merkle tree of code hashes at the protocol level. The root would allow clients to verify the data and help offline nodes sync missing data.

## In-protocol options

The solution to this problem is to split the contract’s bytecode into chunks and merkelize them. This allows for proving only code chunks touched in the execution trace, which is less data than the complete contract code.

Any solution regarding code chunking has two orthogonal dimensions:

- How is bytecode split into chunks?
- How are chunks merkelized?

### How is bytecode split into chunks?

There are two main code-chunker strategies:

- 31-byte code chunker: It partitions the bytecode into 31-byte chunks using a 1-byte prefix to help with JUMPDEST analysis. A detailed explanation can be found here.
- 32-byte code chunker: it partitions the bytecode in 32-byte chunks but prepends the bytecode with a table that efficiently encodes which code chunks contain invalid jump destinations 0x5B. For example, if no PUSHN immediate contains 0x5B then any jump is valid; thus, the table would be empty — a more detailed explanation can be found here.
- Dynamic chunking: previous research explored dynamic size chunking, where code jumps could only target the beginning of a chunk. Since JUMPDEST instructions mark valid jump targets, they effectively determine where chunks start. This can avoid the need for extra mechanisms to detect invalid jumps. However,  it has potential issues that need to be solved via other mechanisms, e.g., large bytecodes without any JUMPDEST.

Note that these code chunkers solve a problem that legacy contracts can have. Upcoming EOF contracts do not have this problem since only code with valid jumps can be deployed. A while ago, I did an [analysis](https://hackmd.io/@jsign/verkle-code-mainnet-chunking-analysis#Code-access-gas-overhead-and-chunkers-comparison) comparing both strategies.

The above are two proposed chunkers, but there can be more variants.

- Usage efficiency: bigger chunks mean fewer chunks to provide in the witness, but can increase wasted bytes since not all bytes from chunks are used in the execution trace.

Both chunkers propose 32-byte code chunks, which might be the case since they were meant to have the same size as storage slots.

**Storage efficiency**: how much storage overhead is created by the chunking?

- 31-byte code chunker: 1/31~=3.2% overhead
- 32-byte code chunker: dynamic, mainnet analysis done a while ago reporting ~0.1%, and a worst case of 3.1% (i.e., every chunk contains an invalid jump).

**Complexity**: spec and implementation complexity

- 31-byte code chunker: very simple
- 32-byte code chunker: more complexity in defining table format, location, etc.

### How are chunks merkelized?

Given a chunked bytecode, we need to determine how the chunks are merkelized so proofs can be created for partial bytecode accessed in an execution trace.

We must also include the existing `codeHash` and a new `codeSize` field to support `EXTCODE*` opcodes efficiently. Doing this is pretty straightforward, so I will focus solely on the primary difficulty: merkelizing the code-chunks.

**Where to merkelize the code chunks?**

The following are some strategies on where they would be merkelized:

- Inside the current MPT.

This is proposed in EIP-2926, in particular in the Code merkelization section. The code hash field is replaced with the root of an MPT, which stores the chunked-code.
- Code chunks are naturally deduplicated since they share the same root.
- Pros:

Natural design leveraging existing trees.
- Low complexity.

Cons:

- It keeps existing overheads like RLP and keccak, which might be better than introducing more spec complexity.

**Inside a new unified state tree**

- In EIPs proposing a new unified tree (e.g., Binary Trees) for account and storage data, contract code chunks would also be stored here.
- Pro:

Natural design considering a new tree is introduced.
- Code chunking of existing code is part of the tree conversion process.

Cons:

- Current proposals don’t deduplicate identical chunks, but this could be changed.
- Bundled with many other changes, it could increase the risk of consensus bugs.

**Inside a new tree only dedicated to code-chunks**

- A new tree only for code chunks is introduced. The existing MPT is left untouched.
- Pro:

Optionally, it allows flexibility in designing the new tree (e.g., different arity or hash function).
- Deduplication is optional, depending on the key definition.

Cons:

- An extra tree root in the block header.
- A different tree design than an MPT means more spec complexity and risk of implementation bugs.

**How is the Merkelization of new and existing bytecodes handled?**

The process of merkelizing code when creating new contracts is straightforward, as [EIP-4762](https://eips.ethereum.org/EIPS/eip-4762) already outlines a structure for charging gas per stored code chunk, i.e., charge users per inserted code-chunk in the tree.

The primary challenge lies in merkelizing existing code, at least 15GiB of deduplicated data. This cannot be achieved only by doing work at the fork activation. While the new unified state tree case can do this work during the tree conversion process, the other two strategies must decide how to do it – here are some ideas:

- On-demand conversion (h/t Dankrad for mentioning this variant – pro/cons are my own)

Only when a transaction interacts with an unchunkified contract is this code chunkified. The transaction sender pays for the code chunking.
- Pros:

Very easy for the protocol since it doesn’t have to convert existing mainnet bytecodes until it is used.
- The target tree where the code is merkelized isn’t polluted with contracts that might never be used again, so it indirectly does some pruning.

Cons:

- The code chunking of a contract is paid by the first transaction that interacts with it. This can be a UX problem since who pays for it is unpredictable, and from a user perspective, it might be better to wait for someone else to pay that first than send their transaction.
- At fork activation time and for some further blocks, we might see a big spike in gas usage that is only related to code chunking. This can also affect base fees until the system stabilizes.
- This approach can leave forever unconverted bytecodes. Thus, EL clients must keep the conversion code since it might eventually be needed again. This also means the block prover has to prove code chunking, so the needed gas cost for conversions could be high.

**Multi-block conversion**

- Similar to a new tree conversion (EIP-7748), we would define a process that, on each block, migrates pending code until all code is chunkified.
- Pros:

No UX problems since users don’t pay for code chunking.
- No gas spikes or base fee disturbances.
- The block-by-block conversion allows the detection of any bug at the consensus level as soon as it happens, compared to a single block activation.

Cons:

- It adds complexity to the spec for a task only done once, and can have many implementation bugs, making it risky.

**Offline conversion**

- This is what is proposed as the conversion mechanism in the mentioned EIP-2926. See this section, which explains the idea.
- Pro:

No UX problems since users don’t pay for code chunking.
- No gas spikes nor base fee disturbances.
- At fork activation time, the system immediately switches to the desired state. There aren’t temporary conversion stages as in “Multi-block conversion”.

Cons:

- Since the conversion happens offline, a proper fork activation timestamp should be estimated. But a safe value can be easily calculated. Or rely on a manual second quick fork for the activation after EL clients do proper out-of-band checks.
- The background conversion result on each EL client remains opaque until activation time, which can be considered riskier compared to “Multi-block conversion”.
- Deep reorgs close to the fork activation should be considered for worst-case scenarios.

**On-Demand + (Bounded) Offline Mix**

- Request offline conversion only for contracts accessed within the past year to minimize workload. For the remaining unchunkified contracts, the first transaction would cover the conversion cost.
- Pros:

Minimal UX problems, as users accessing contracts from the past year won’t incur costs. Only those accessing older transactions will pay.
- Minimal gas spikes or base fee disturbances.
- Reduced workload for EL clients in offline conversion.

Cons:

- Despite fewer bytecodes needing conversion, the background conversion remains opaque, so the risk of consensus failure persists.
- The fork activation timestamp estimation remains crucial, or a manual second fork for activation may be needed.
- It has the same situation of always having unconverted code and having to prove code chunkings.

# What happens next?

After resolving the unchunkified bytecode issue, the remaining bottlenecks are mispriced opcodes/precompiles (e.g., `MODEXP` and pairings — some work on this planned for Fusaka ([EIP-7883](https://eips.ethereum.org/EIPS/eip-7883)), and state access efficiency. Researchers and zkVM engineers are analyzing the former.

The latter means using all available gas to access the state. The load depends on the underlying tree arity and hash function, which impacts the amount of hashing needed in the witness. Under the assumption of keeping the current MPT, if we do as many account accesses as possible:

- 36M gas = ~407k keccak permutations.
- 60M gas = ~678k keccak permutations.
- 100M gas = ~1.13m keccak permutations.
- 300M gas = ~3.39m keccak permutations.

*(`keccak perms = gas/2500*tree_depth*15*32/keccak_rate = gas/2500*8*15*32/136`)*

Note the above calculation uses the expected depth for mainnet in a 16-arity tree like an MPT (i.,e ~8); however, specific branches within the actual tree structure reach greater depths, presenting opportunities for utilization.

If the above projections are a problem for the considered minimal prover hardware budget, we might need to consider a state tree change or the gas model for state access.

## Replies

**0xwitty** (2025-05-03):

Thanks for post, [@ihagopian](/u/ihagopian)

Merkelizing bytecode feels like a natural next step for improving prover efficiency, especially with the push toward statelessness and scalability. I like the breakdown of chunking strategies - fixed-size is simple but kind of blunt, while dynamic chunking seems smarter but trickier to pull off cleanly.

One thing I’m curious about is how this would impact tooling and dev UX - especially debugging or source maps when bytecode gets chunked and merkelized. Would love to see more exploration around that.

Overall, solid direction - excited to see where it leads!

---

**ihagopian** (2025-05-03):

Thanks [@0xwitty](/u/0xwitty).

![](https://ethresear.ch/user_avatar/ethresear.ch/0xwitty/48/17918_2.png) 0xwitty:

> One thing I’m curious about is how this would impact tooling and dev UX - especially debugging or source maps when bytecode gets chunked and merkelized. Would love to see more exploration around that.

Great question. Adding code-access costs introduces a new dimension to the EVM gas model, so both tooling and developers should adapt.

For compilers, code layout becomes a new optimization dimension. Today, a program that “jumps all over” pays no extra gas apart from the opcodes, but with code-access fees, poor layout will cost more. Optimizers will therefore need to arrange bytecode more carefully.

Developers who want to squeeze gas-saving might also have to think about this new dimension. As in, guide or help the compiler by structuring code so the compiler can optimize better.

How important all of this is depends on how we fold code-access costs into the gas model:

- No charge: keeps code access free. This case still means having a better worst-case than today’s for the prover, but an attacker can still spam a block by touching many code chunks for only the cost of JUMP + JUMPDEST (and some CALLs, since contract size matters). The attack surface grows if we lower JUMP prices, raise the contract-size cap to 256 KiB, or increase the block gas limit. So it sounds like we might do much protocol work to not fully resolve the worst-case properly.
- Full charge: charge for every chunk, as in EIP-4762. The gas model is simpler, since it is all about leaf access e.g., code chunks and storage slots are charged the same way.
- Hybrid: maybe something like what is done in EIP-7623. Charge code-access fees only when compute/storage gas is not “heavy enough,” proving the caller is not abusing the mechanism.

That hybrid approach is just something I thought of now, so take it with a grain of salt. We could also tweak EIP-4762 to charge code-access leaves less than other leaves. Each option has a different complexity in the protocol, but it tries to make the lives of devs/users easier.

