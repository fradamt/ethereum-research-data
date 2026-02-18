---
source: magicians
topic_id: 25486
title: "EIP-8024: Backward compatible SWAPN, DUPN, EXCHANGE"
author: frangio
date: "2025-09-16"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-8024-backward-compatible-swapn-dupn-exchange/25486
views: 226
likes: 8
posts_count: 6
---

# EIP-8024: Backward compatible SWAPN, DUPN, EXCHANGE

Discussion topic for [EIP-8024](https://eips.ethereum.org/EIPS/eip-8024).

This is a fork of [EIP-663](https://eips.ethereum.org/EIPS/eip-663) without a dependency on EOF.

#### Update Log

- 2025-09-06: initial proposal to update EIP-663
- 2025-09-15: decision to fork as new EIP
- 2025-11-04: updated encode_pair, decode_pair to fix inconsistency between spec and examples

## Replies

**frangio** (2025-09-27):

Discussion of alternatives:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png)
    [EVM Immediates](https://ethereum-magicians.org/t/evm-immediates/25605) [Primordial Soup](/c/magicians/primordial-soup/9)



> All current EVM instructions other than the push opcodes take all of their operands from the stack. Many instructions have been proposed in the past that would’ve liked to use immediate operands, where the operand value is a constant hardcoded in the bytecode instead.
> No such instruction has been accepted yet because it would imply a breaking change to existing EVM bytecode. EOFv1 (EIP-7692) would have addressed this, but the proposal was ultimately rejected.
> This post looks at the problem ane…

---

**charles-cooper** (2025-12-17):

I want to voice opposition against including this EIP in Glamsterdam for the same reasons that I opposed EIP-663 inclusion with EOF (cf. the Compiler Complexity Reduction section in [EOF: When Complexity Outweighs Necessity - HackMD](https://hackmd.io/@pcaversaccio/eof-when-complexity-outweighs-necessity#Compiler-Complexity-Reduction)).

First of all, I want to point out that Vyper does not have the stack-too-deep problem. We have two pipelines, legacy and venom, with different tradeoffs (overuse of memory vs sometimes inefficient stack spilling), but we are making rapid progress on them. I believe Solidity is also making progress on this as well. Therefore, adding more opcodes to the VM is solving an application level problem at the VM level, needlessly increasing complexity, as enumerated below.

The solution presented by this EIP has several problems, as mentioned in the hackmd article, but I’ll enumerate them again below:

- it hurts EVM-to-native compilation (either JIT or AOT, but both have to execute within a defined performance envelope) due to the register allocation problem. Linear-time register allocation also exists, but it is suboptimal and increases memory pressure. Memory pressure should be paid for explicitly(!) by actually using EVM memory!
- it burns valuable L1 cache space – the “hot” portion of the stack grows from 512 bytes to 235 * 32 = 7.5KB, which is a substantial portion of the L1 budget (most CPUs have between 32kb and 64kb of L1 cache). allowing user-access to more stack space increases cache thrashing / stack space that is likely to be kept in cache
- the backwards-compatibility encoding to avoid JUMPDEST analysis is a complexity that clients will pay forever

It also burns opcodes needlessly, while solving the wrong problem – the reason the Solidity compiler needs deep stack access is because they can’t predict where their dynamically allocated memory will end.

[EIP-7923](https://eips.ethereum.org/EIPS/eip-7923) proposes a more general solution which solves multiple problems at once:

- heap vs call stack separation, allowing better EVM compiler design
- EVM languages can allocate reserved areas of memory for stack spilling which they can guarantee do not get trampled by other allocators
- developers get a modern memory model, not one from the 80s
- it is a general fix that improves the design space for compilers and low-level developers without adding EVM complexity besides a pricing change

---

**norswap** (2025-12-17):

I second Charles’ analysis, fixing the memory model would be a much more elegant solution that avoids the downsides.

---

**frangio** (2025-12-17):

I agree that “stack too deep” can be solved without these opcodes! However, solc hasn’t been able to solve it yet, and we can’t wait forever. This error is not acceptable in what should by now be a mature tech stack, and with Solidity being the most popular language for the EVM, I don’t think it’s unreasonable for Ethereum to take this measure at the VM level.

I think the listed downsides are only minor issues or can be mitigated:

- Cache: This is a fair point that needs to be measured and reflected in the gas schedule. For example, if SWAPN/DUPN are likely to read from L2 cache instead of L1 cache, the cost might be 10x that of SWAP/DUP (which would be 10 gas if repriced according to EIP-7904).
- Decoding complexity: We’re talking about 25 lines of self-contained code consisting of simple arithmetic and conditionals. However, if this is deemed too complex, the EIP can very easily be switched to use push-postfix immediates, which require no decoding.
- Compilation to native: I think this requires a more careful statement and discussion. I’m personally not convinced that the addition of SWAPN/DUPN makes compilation any more difficult than it already is. If I understand correctly, the argument is that these opcodes can potentially increase the number of simultaneously live values, but IMO they don’t: if a sequence of instructions grows the stack to height N, we can assume there are N live values, whether they are accessed via SWAPN/DUPN or only accessed when they’re in the top 16 stack slots. A compiler has to figure out what to do with the other N-16 values, with or without SWAPN/DUPN. Most likely, they will be spilled to memory, and that’s where SWAPN/DUPN should read them from. This would also support a higher gas cost, but as far as I know compilation to native is not a consideration that goes into choosing the gas schedule.
- Opcode use: I believe there are currently 106 free opcodes, so definitely not a shortage. If this is a real concern, the same impact can be achieved by just including DUPN.

I’m supportive of changing the memory model. I agree that it’d be a good improvement with broader impact than this EIP. It wouldn’t be as immediate a fix for “stack too deep” as this EIP though.

---

**charles-cooper** (2025-12-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> However, solc hasn’t been able to solve it yet, and we can’t wait forever

Maybe try a different language or compiler, which does solve it!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> This error is not acceptable in what should by now be a mature tech stack

I totally agree

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> with Solidity being the most popular language for the EVM

Thanks to the EF pushing and providing the bulk of its compiler/languages budget to it all these years. For example, [ethereum.org](http://ethereum.org) makes no mention of other languages besides Solidity. Why don’t they start promoting languages which *don’t* have stack too deep errors?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> I don’t think it’s unreasonable for Ethereum to take this measure at the VM level.

I disagree. It increases complexity of the instruction set and VM, and it’s unnecessary given that a simpler solution has presented which not only increases reasonability of the VM’s memory model, but also improves the design space for compilers and users in a more general way.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Cache: This is a fair point that needs to be measured and reflected in the gas schedule. For example, if SWAPN/DUPN are likely to read from L2 cache instead of L1 cache, the cost might be 10x that of SWAP/DUP (which would be 10 gas if repriced according to EIP-7904).

Which is more expensive than memory at current prices, at which point applications should just use memory.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Decoding complexity: We’re talking about 25 lines of self-contained code consisting of simple arithmetic and conditionals. However, if this is deemed too complex, the EIP can very easily be switched to use push-postfix immediates, which require no decoding.

Doesn’t this increase decoding time? OTOH, using push-postfix immediates would increase the instruction size to 3 bytes per SWAPN or DUPN, which is think is undesirable from a codesize perspective.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Compilation to native: I think this requires a more careful statement and discussion. I’m personally not convinced that the addition of SWAPN/DUPN makes compilation any more difficult than it already is. If I understand correctly, the argument is that these opcodes can potentially increase the number of simultaneously live values, but IMO they don’t: if a sequence of instructions grows the stack to height N, we can assume there are N live values, whether they are accessed via SWAPN/DUPN or only accessed when they’re in the top 16 stack slots. A compiler has to figure out what to do with the other N-16 values, with or without SWAPN/DUPN. Most likely, they will be spilled to memory, and that’s where SWAPN/DUPN should read them from. This would also support a higher gas cost, but as far as I know compilation to native is not a consideration that goes into choosing the gas schedule.

With only 16 addressable stack slots, compilation to native on an architecture is kind of super straightforward – you map stack slots to registers (on x86 you can even map to zmm0-15), when they go out of scope (depth 17 or deeper) you write them to memory, when they go back into scope you recover them from memory. SWAP instructions even map to register renames, which is extremely efficient on modern CPUs. No register allocation is needed.

OTOH if you have 235 addressable values, you need to run a register allocation routine, which finds the live ranges of each stack slot, spills them to memory when there are not enough registers, and then pops them back when there is enough “register space” again. As I’ve mentioned before, the best known algorithms are polynomial time; linear-time algorithms also exist but the quality of the code will be poorer. I highly recommend anybody interested in this problem and who is wondering about the effect of EIP-8024 (and 663) on EVM-to-native read the wikipedia article on register allocation: [Register allocation - Wikipedia](https://en.wikipedia.org/wiki/Register_allocation).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Most likely, they will be spilled to memory, and that’s where SWAPN/DUPN should read them from. This would also support a higher gas cost, but as far as I know compilation to native is not a consideration that goes into choosing the gas schedule.

As I understand, you are saying that the 17th+ stack items should be stored in memory as in the first scheme I have described above (where when they go out of scope they get written to memory). That’s fine, but there is already an abstraction modeling memory access in the EVM, which is **memory**, users should just use that. (And yes, the memory pricing model should be fixed! As I described in my previous post and also below.)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> It wouldn’t be as immediate a fix for “stack too deep” as this EIP though.

I don’t think this is actually even true. Let me explain: with EIP-8024, the “fix” for stack too deep would be to emit deeper dup/swap instructions, rather than spilling.

However, EIP-8024 also only pushes the problem out. You need to fall back to spilling in the case that the user has more than 235 variables on the stack (which can easily happen if functions are inlined or more kinds of variables are lifted to the stack). So you need to make sure you have a correct spilling algorithm anyways!

With EIP-7923, the solution instead would be to spill at a high address. This solution is actually even easier to implement in the compiler (at least in Vyper) - calculating the safe spill point is trivial with EIP-7923, it’s just a high number. (As mentioned we still have to implement spilling anyways, so it’s not like EIP-8024 lets us skip that).

