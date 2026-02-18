---
source: magicians
topic_id: 261
title: "EIP-1051: Arithmetic overflow detection for the EVM"
author: Arachnid
date: "2018-05-02"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/eip-1051-arithmetic-overflow-detection-for-the-evm/261
views: 5290
likes: 25
posts_count: 24
---

# EIP-1051: Arithmetic overflow detection for the EVM

I’ve written up an EIP for overflow detection in the EVM, [here](http://eips.ethereum.org/EIPS/eip-1051). Feedback appreciated!

## Replies

**phiferd** (2018-05-04):

Thanks for putting this together, Nick.

> One option would be to provide an opcode that enables overflow protection, causing a throw or revert if an overflow happens. However, this limits the manner in which overflows can be handled.

Are you thinking that the EVM can provide this low level detection, and then solidity or other languages can add default checks in the future? Ideally, newly created/compiled smart contracts should automatically throw on overflow. If developers really want to handle it differently, the language can provide a switch or annotation to prevent the compiler from generating the default checks.

---

**Arachnid** (2018-05-04):

The EVM just provides a flag, and it’s up to higher level languages to decide how to utilise it. For the most part in languages like Solidity, you could check the overflow flag once per basic block.

---

**nootropicat** (2018-05-06):

Support the idea, but

1. Why the nonstandard naming? ‘Overflow’ for the carry flag and ‘signed overflow’ for the overflow flag. It’s a bit confusing.
2. Instead of two separate flag registers, one FLAGS register (like on a cpu) with bit flags allows easier extensibility and doesn’t use new opcodes for every new flag. On x86 pushf to push the flags register and popf to set it are used.
3. Given the flags register, perhaps zero and sign flag as well? They already exists on every cpu.

Using the flags register makes it easily possible to implement the ‘trap on overflow/carry’ functionality, by adding two new flags that determine throwing when they are set + flag conditional jumps which would reduce code size and gas use considerably, see:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 18 Jan 18](https://ethresear.ch/t/evm-idea-add-access-to-overflow-carry-sign-and-zero-flags-to-reduce-gas-use/782)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          EVM






Motivation:   lack of overflow flag means checking for overflow wastes gas and storage on pointless comparisons lack of carry flag makes >256 bit arithmetic slow because it has to be reimplemented via comparisons  If these two flags were to be...



    Reading time: 1 mins 🕑
      Likes: 2 ❤











Instead of simply reverting, the address of an arbitrary error handler could be set in the flags register (second dword?), jumped to after the flag is set with the offending instruction’s address on the stack.

---

**Arachnid** (2018-05-06):

Thanks for the feedback!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> Why the nonstandard naming? ‘Overflow’ for the carry flag and ‘signed overflow’ for the overflow flag. It’s a bit confusing.

We don’t currently have any opcodes that can benefit from a ‘carry’ flag, and I thought using that terminology might imply we do. I’m happy to change it back, though.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> Instead of two separate flag registers, one FLAGS register (like on a cpu) with bit flags allows easier extensibility and doesn’t use new opcodes for every new flag. On x86 pushf to push the flags register and popf to set it are used.

I’m on the fence about this. It would reduce opcodes, but it would also require more work to check the register each time.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> Given the flags register, perhaps zero and sign flag as well? They already exists on every cpu.

I don’t think those would actually be any easier to check and branch on than at present, would they? Without it, you can branch on 0 with `DUP1 NOT JUMPI`, without it it’d be `FLAGS PUSH (mask) JUMPI`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> Using the flags register makes it easily possible to implement the ‘trap on overflow/carry’ functionality, by adding two new flags that determine throwing when they are set + flag conditional jumps which would reduce code size and gas use considerably, see:

I’d be concerned about adding complexity to the VM with modal flags like this.

---

**nootropicat** (2018-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> We don’t currently have any opcodes that can benefit from a ‘carry’ flag

If any way to detect the carry flag exist it can be used to cheaply, compared to comparisons, implement an arbitrary precision arithmetic, by adding/subtracting the carry flag. On x86 there are even specialized instructions that do this, adc (add with carry) and sbw (subtract with borrow).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> I’m on the fence about this. It would reduce opcodes, but it would also require more work to check the register each time.

Fair enough. Pushf could have a byte number that means a bit to be pushed, with one special value of 0xFF that pushes the entire register. Ditto for popf (first argument the index, second the value). This combines the simplicity of one-case opcodes with extensibility.

> I don’t think those would actually be any easier to check and branch on than at present, would they? Without it, you can branch on 0 with DUP1 NOT JUMPI, without it it’d be FLAGS PUSH (mask) JUMPI.

True for the zero flag without cmp and flag-conditional jumps, but not true for the sign one.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> I’d be concerned about adding complexity to the VM with modal flags like this.

Not that much, It can be implemented as one if that pushes the address onto the stack + changes the instruction pointer to the trap handler, leaving the rest to the normal execution loop.

More generally, performance requires specialization. [Complex instructions, eg. for text parsing are still being added](https://blog.cloudflare.com/improving-picohttpparser-further-with-avx2/) into cpus. The RISC approach is dead.

There’s also the adoption and safety aspect. On the vm side the operation is one check each time the overflow/carry flag is set, but reimplementing the behavior in the compiler requires changing the code generation for each arithmetic instruction. Much more work and more room for errors. Setting a trap flag at the beginning is trivial to add in comparison. For these reasons I think VM is the best abstraction level to tackle the overflow problem.

That’s a bit offtopic, but given the performance characteristics of EVM the CISC-like approach would imo yield much higher benefits than it does in physical cpus. Like the solidity method selector: all these pushes and comparisons at the beginning of almost every contract execution could be replaced by a switch instruction that jumps according to an array specified directly in code, additionally switch-like ifs in code could be optimized that way by a compiler. A small advantage multiplied by billions of executions.

---

**gcolvin** (2018-05-09):

One problem here is implementation difficulty.  Some libraries support checking directly, others don’t.  If they don’t every specified operation will be slowed down by an explicit comparison.  I’d wager the libraries that support checking are in the minority (even in C++) so I’d as soon let the code that cares about overflow handle it explicitly.

---

**Arachnid** (2018-05-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> If any way to detect the carry flag exist it can be used to cheaply, compared to comparisons, implement an arbitrary precision arithmetic, by adding/subtracting the carry flag.

Fair enough - though this probably also depends on it being available as a separate bit for efficiency, no?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> Not that much, It can be implemented as one if that pushes the address onto the stack + changes the instruction pointer to the trap handler, leaving the rest to the normal execution loop.

Reasonable point. What do you see as the pros and cons of a trap handler vs a flag, then?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> On the vm side the operation is one check each time the overflow/carry flag is set, but reimplementing the behavior in the compiler requires changing the code generation for each arithmetic instruction. Much more work and more room for errors. Setting a trap flag at the beginning is trivial to add in comparison. For these reasons I think VM is the best abstraction level to tackle the overflow problem.

To be clear, either approach would require compiler changes. Solidity would have to allow you to specify when overflow is and isn’t wanted, and either check the flag or set and clear the trap handler.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> One problem here is implementation difficulty.  Some libraries support checking directly, others don’t.  If they don’t every specified operation will be slowed down by an explicit comparison.  I’d wager the libraries that support checking are in the minority (even in C++) so I’d as soon let the code that cares about overflow handle it explicitly.

Surely capturing overflow in implementations isn’t that hard? The underlying hardware already supports it.

---

**gcolvin** (2018-05-09):

The EVM’s 256-bit registers are emulated using available libraries for arbitrary-precision arithmetic.  The hardware is far away.  Most algorithms don’t overflow, they just produce a bigger result.  Try implementing your proposal in the Go VM and you may see the difficulty.

---

**gcolvin** (2018-05-09):

You might look at the IELE VM, which has registers that do just keep growing in size.  Like the natural numbers.

---

**nootropicat** (2018-05-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> If they don’t every specified operation will be slowed down by an explicit comparison.

Why slowed down? The cost of simple comparison on data already in L1 is effectively zero. The cost of manual checking in safemath should be more expensive by orders of magnitude. Go’s compiler optimization would have to be horrible for a comparison to be noticeable in any way.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Try implementing your proposal in the Go VM and you may see the difficulty.

Go implements big math in assembly.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/6/68f11f1b3c0b1083db3cbb7e71ba04a723150d33.png)

      [go.dev](https://go.dev/src/math/big/arith_amd64.s)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/5/51823551a25fe20bbf14ab81cf96d2a06df4bde9_2_690x400.jpeg)

###










I don’t know Go much, but [according to this](https://blog.sgmansfield.com/2017/04/a-foray-into-go-assembly-programming/) calling arbitrary native code in Go is easy and can offer big performance improvements:

> name                 time/op
> GetBucket-8          17.4ns ± 2%
> GetBucketNoInline-8  17.4ns ± 2%
> GetBucketASM-8       12.8ns ± 1%

in any case, I don’t think it would be possible to observe the difference between a comparison in go (assuming reasonable optimizing compiler) vs checking carry/overflow in assembly/C/C++, but in the case that it is, external code in C/C++, optionally with [intrinsics](https://gcc.gnu.org/onlinedocs/gcc/Integer-Overflow-Builtins.html) or inline asm could be used.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> What do you see as the pros and cons of a trap handler vs a flag, then?

Ah, I wasn’t clear enough - I meant a flag AND an option to trap on it. For example, for a FLAGS register defined in the following way:

> struct FLAGS {
> unsigned short int flags;
> unsigned short int trapMask;
> unsigned int trapHandler; //defaults to revert?
> }

with *flags*’ bits defined as:

> carryFlag | overFlowFlag | signFlag | zeroFlag | reserved | …

*trapMask* as a bitmask for traps:

> carryFlagTrap | overflowFlagTrap | signFlag | zeroFlag | reserved | …

ie. when carryFlagTrap bit is set trap on setting carryFlag.

After flags are set in EVM it’s enough to:

> if(FLAGS.flags&FLAGS.trapMask) {
> pushOnEvmStack(evmEip);
> evmEip = FLAGS.trapHandler;
> }
> //end current instruction

So this way, there are both flags, optional traps and everything is easily extensible.

I guess in this construction arguments 0-31 for pushf/popf could refer to flags’ and mask’s bits, 255 for the whole register, 254 for flags, 253 for trapMask and 252 for trapHandler. Perhaps 251 for trapMask with trapHandler at once, as these two fields are likely to be set together.

> To be clear, either approach would require compiler changes. Solidity would have to allow you to specify when overflow is and isn’t wanted, and either check the flag or set and clear the trap handler.

Well yes, but enabling trapping on overflow could be implemented as a one dumb pushf added at the beginning, pure flags require changes in code generation for arithmetic expressions. A simple pushf could in principle be added manually after compiling, or as inline asm, with a compiler that doesn’t know traps exist.

---

**Arachnid** (2018-05-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nootropicat/48/127_2.png) nootropicat:

> Ah, I wasn’t clear enough - I meant a flag AND an option to trap on it.

Fair enough. I’m concerned this pattern, while common in MCUs, isn’t really idiomatic for the EVM, though. It introduces several new concepts that haven’t previously featured.

---

**maciej** (2018-05-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Solidity would have to allow you to specify when overflow is and isn’t wanted, and either check the flag or set and clear the trap handler.

Coming from Rust, integer overflows always panic by default. Doing any sort of math that requires overflowing as a feature is such a niche use case, we handle it with a specialized method:

```rust
// Panic on runtime
let x = u32::max_value() + 1;

// No panic, x = 0
let x = u32::max_value().wrapping_add(1);
```

I realize that making all arithmetic overflows be treated as errors by default would be a breaking change for Solidity, but I really cannot think of a reason why it should not be a default.

---

**gcolvin** (2018-05-16):

I don’t know if I’m confused or the discussion is, but I don’t think the behavior of native ints is the issue here, or the fact that some big-integer libraries are written in assembly.  The issue is how to implement this in VMs that mostly are not written in assembly, and shouldn’t need to be.  Not even C provides access to the carry bit, and neither do most big-integer libraries.  So the only way to test for overflow in most cases is to not let the result overflow, then test whether it’s too big.  I’m no longer sure whether this is a big performance hit, but measurements would good to have.

As for making overflows throw, that would break not just Solidity, but every EVM program that counts on the EVM having unsigned values that don’t overflow.  Better that Solidity use whatever mechanism is provided to detect overflow to introduce a new type that traps.

---

**maciej** (2018-05-17):

I don’t know about Geth or other implementations, but the big integer primitives in Parity (implemented both in inline assembly and pure rust depending on compilation target) already return a boolean for overflows:



      [github.com](https://github.com/paritytech/primitives/blob/dfb17048cba127e086d9105e5ef9ecea240575c2/uint/src/uint.rs#L868-L874)





####



```rs


1. /// Checked multiplication. Returns `None` if overflow occurred.
2. pub fn checked_mul(self, other: $name) -> Option {
3. match self.overflowing_mul(other) {
4. (_, true) => None,
5. (val, _) => Some(val),
6. }
7. }


```










I’d have to look deeper into how signed ops are performed to see if it’s realistic to get `SOVF` flag on top, but right now it appears to me that the only performance cost for implementing this EIP in Parity EVM is just the cost of storing the flag instead of just throwing it away.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> As for making overflows throw, that would break not just Solidity, but every EVM program that counts on the EVM having unsigned values that don’t overflow.

I was talking purely about changing the behavior on Solidity side by using the new opcodes, so it would be a breaking change for Solidity and hence require a semver bump to `0.5.x`. No breaking changes to EVM.

---

**maciej** (2018-05-23):

Just to expand on this, I looked at the actual EVM interpreter and can confirm that all math is [already checking for overflows and throws the flag away](https://github.com/paritytech/parity/blob/db9397890efbc551d8ba70c3887ddcb0f6b0e097/ethcore/evm/src/interpreter/mod.rs#L685-L763): in `stack.push(a.overflowing_add(b).0);` any `overflowing_X` operation returns a tuple of `(result, overflow_flag)`, hence `.0` just grabs the result.

Since there were concerns raised during the dev call about the cost of multiplication in particular, I looked at how multiplication is done internally:

- The pure Rust implementation uses 512bit (8 limbs) on stack which then checks if any of the top half of the integer is non-zero.
- The optimized Assembly code (x86_64 only) on the other hand uses only 5 registers for result (4 limbs in the array and separate register for overflow).

I also took the liberty of looking at how Geth handles things, apologies in advance if I’m missing anything here and please correct me if I’m wrong. It appears to me that all EVM math stuff is handled by arbitrary precision `big.Int` from `math/big` that gets it’s results truncated with `U256` (which just uses a binary and operation with 2^256-1), so while it doesn’t return an overflow flag, it already does the expensive part of performing the multiplication with as many extra limbs as necessary, and getting the flag is just a single `Cmp` away. The library [does expose access to limbs](https://golang.org/pkg/math/big/#Int.Bits) if a full `Cmp` would be excessive.

TL;DR: Both Geth and Parity already do all the heavy lifting on math that is required to extract the overflow flag, I reckon the overhead of getting and storing the flag relatively speaking should be trivial, and can be well optimized with fixed-precision libraries if benchmarks disagree.

---

[@Arachnid](/u/arachnid): one thing that’s still not clear for me is the necessity of `SOVF`,  it’s not mentioned in the rationale.

---

**Nucnay3428** (2019-01-05):

I’m new to this well I’ve been trying to take the plunge into something New but not had the confidence to be fully committed for nearly two years and I’m struggling to understand reading is not a strong point but I’m getting a lot of practice and am able to make more sense of the sites thanks to all of you that replied to this 3 Detailed discussion s which each had valid points and different problems solved this has really helped with my knowledge and understanding need more posts like these👏

---

**gcolvin** (2019-01-06):

[@Arachnid](/u/arachnid) I don’t see Wasm in this discussion.  I don’t think it provides access to the overflow bit.

---

**maciej** (2019-02-08):

[@gcolvin](/u/gcolvin) It doesn’t have it AFAIK, but it’s planned: https://github.com/WebAssembly/design/blob/master/FutureFeatures.md#integer-overflow-detection

---

**gcolvin** (2021-03-14):

[@Arachnid](/u/arachnid) yes - why the non-standard names?  And perhaps, more descriptive names e.g. `ISCARRY` and `ISOVERFLOW` to go with the existing `ISZERO`

See [The CARRY flag and OVERFLOW flag in binary arithmetic](http://teaching.idallen.com/dat2343/11w/notes/040_overflow.txt)

for a detailed discussion of when to set and how to use these flags.

---

**RenanSouza2** (2023-03-28):

This may be too late, but I have some toughth on thi EIP wich is one crucial to join security and effiency

I like how signed and unsigned are treated separetely

how you can perform a batch of operations and the flags only need to be checked at the end (with some exception if you mix signed and unsigned operations)

but I also have some remarks:

The ovf flag should trigger in the operations EXP and SHL

an signed sum of a positive and a negative number should not trigger the signed and should trigger the unsigned flag. The specification says “The sovf flag is set whenever the ovf flag is set, and additionally in the following circumstances”

Division by zero, and this include operations div, mod, sdiv, smod, addmodm, mulmod as well; should be treated in the flags

The signed division -(2**255) / -1 should trigger the sovf flag

The flags related to signed multiplication is wrong, it should trigger when the modulo of the ideal multiplication is bigger equal than 2**255

The signed flag should trigger with the SHL operation, this is trickier to define when


*(3 more replies not shown)*
