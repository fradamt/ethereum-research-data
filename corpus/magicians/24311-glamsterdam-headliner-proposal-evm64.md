---
source: magicians
topic_id: 24311
title: "Glamsterdam headliner proposal: EVM64"
author: sorpaas
date: "2025-05-22"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/glamsterdam-headliner-proposal-evm64/24311
views: 454
likes: 2
posts_count: 4
---

# Glamsterdam headliner proposal: EVM64

This is a headliner proposal for EVM64 for Glamsterdam.

### Summary

Headliner proposal for EVM64.

Option A is EVM64 with prefix opcode `0xC0`.

- EIP-7937 of EVM64 for endianness-independent arithmetic, comparison, bitwise and flow operations.
- EIP-9819 for EOF support.
- EIP-9821 for little-endian BYTE64, MLOAD64, MSTORE64 and PUSH*64 opcodes.

Option B is “pure” EVM64 via EOF code section.

- EIP-9834 which defines an extended version of types_section for EOF.
- EIP-9835 which defines the EVM64 code section type.

### Detailed justification

The benefit of this proposal includes:

- Improve throughput and reduce gas costs for writing computationally intensive algorithms in EVM. Many algorithms cannot utilize the full 256-bit.
- Make EVM JITs / AOTs, as well as EVM-to-RISCV recompilers in the future, more attractive. At this moment, any EVM contract re-compile will be roughly 4x the size (because 1 256-bit op will be at least 4 64-bit ops), which is a considerable bottleneck.

Why consider the inclusion now:

- There are an increasing amount of EVM contracts on-chain that are computationally intensive nowadays, especially for rollups. Many of them wait for certain precompiles on-chain. But precompiles can’t foresee all possible use cases. EVM64 provide with them a possible alternative path that does not depend on Ethereum network upgrades.
- With the beginning of the recent discussions of potential RISC-V contracts on Ethereum, EVM64 prepares us for the future when we eventually need EVM-to-RISCV recompilation.

### Stakeholder impact

- Positive: An important tool for smart contract developers for computationally intensive contracts.
- Negative: Implementation complexity for core devs.

### Technical readiness

The core EIP (EIP-7937) is specification-ready. Benchmarks are being worked on. A reference implementation is available in [rust-evm](https://github.com/rust-ethereum/evm/tree/master/features/evm64).

### Security & open questions

The core EIP (EIP-7937) has no known open questions.

The design of the optional additional EIP with regards to `BYTE64`, `MLOAD64`, `MSTORE64`, `PUSH*64` is ready, but additional discussions about endianness is still open.

For past discussions and reviews about EIP-7937 please also see the [Github PR](https://github.com/ethereum/EIPs/pull/9687).

## Replies

**LukaszRozmej** (2025-05-28):

I love the idea, not sure if I love the whole implementation/specification, especially with the prefix opcode.

I wonder if we could combine this with EOF in that way that some functions would be in 64bit context while other in 256bit, we could then reuse opcodes and only pay slightly when crossing the boundry.

---

**sorpaas** (2025-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lukaszrozmej/48/3746_2.png) LukaszRozmej:

> especially with the prefix opcode

I personally think multibyte opcode would be inevitable. We only ever have 256 single byte opcodes and it’s probably important to save it.

Having prefix opcode is not uncommon in other architectures, and I think this will open a lot of additional doors for us. For example, we can have another prefix opcode that changes the behavior of arithmetic operations from overflowing to checked OOG, eliminating the common need for `SafeMath`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lukaszrozmej/48/3746_2.png) LukaszRozmej:

> I wonder if we could combine this with EOF in that way that some functions would be in 64bit context while other in 256bit, we could then reuse opcodes and only pay slightly when crossing the boundry.

Yep this is possible. We can build on top of EIP-4750 and define a new section type. Once entered, the full section will run EVM64/LE only (with the stack being 64-bit only).

But this one will have the drawback that almost all other (system/runtime) opcodes must be disabled (because they need 256 bit stack). We can’t have interop if we don’t use prefix opcode design, because otherwise the arithmetic operations can’t ever operate on the most significant 192 bits.

Anyway, I’ll write an EIP for this as well for us to have choices. You’ll see the pros and cons to be really obvious. Personally I really lean towards the current prefix opcode design, because the alternative will make interop difficult, and significantly hinders gradual optimization.

---

**sorpaas** (2025-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sorpaas/48/1074_2.png) sorpaas:

> Anyway, I’ll write an EIP for this as well for us to have choices. You’ll see the pros and cons to be really obvious. Personally I really lean towards the current prefix opcode design, because the alternative will make interop difficult, and significantly hinders gradual optimization.

Please see [EIP-9834](https://github.com/ethereum/EIPs/pull/9834) and [EIP-9835](https://github.com/ethereum/EIPs/pull/9835). This actually turned out to be a little bit better than I thought.

Pros:

- “Pure” EVM64.
- No more code size increase.

Cons:

- “Pure” computation only. No system/runtime calls. But this may not be that of a big problem because memory is shared.
- Can’t do gradual optimization – a function is either purely EVM64 or it is not.

