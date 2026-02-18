---
source: magicians
topic_id: 3472
title: "EIP-615: Subroutines and Static Jumps for the EVM -- Last Call"
author: gcolvin
date: "2019-07-12"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm-last-call/3472
views: 6230
likes: 15
posts_count: 33
---

# EIP-615: Subroutines and Static Jumps for the EVM -- Last Call

This proposal is about significantly increasing the formal tractability of the EVM.  We deprecate dynamic jumps, which play hell with formal specs, proofs of correctness, static analysis, fast compilation, and more. And being rid of them, introduce subroutines and other facilities to replace them.  People doing auditing and build tools for analyzing EVM code intend to take advantage of the formal tractability if they can, and the eWasm team is investigating the possibilities for near-linear-time compilation of well-structured EVM and eWasm code.

https://github.com/ethereum/EIPs/pull/2189/

[Much previous discussion was here.](https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm/2728)

## Replies

**gcolvin** (2019-07-16):

[Merged draft](http://eips.ethereum.org/EIPS/eip-615) is now ready for discussion.  Previous discussions over the years can be found [here](https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm/2728), [here](https://github.com/ethereum/EIPs/issues/615), and [here](https://github.com/ethereum/EIPs/issues/184).


      [Ethereum Improvement Proposals](http://eips.ethereum.org/EIPS/eip-615)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.

---

**fulldecent** (2019-07-16):

Following is my review of EIP-615. This includes all issues past and present which apply to the current text. This includes technical problems which warrant cancelling/extending this Last Call, specific recommendations to improve the EIP (I will supply PR if invited), and arguments on theoretical and practical topics.

# Dependency is missing

In the text it states

> ### Dependencies
>
>
>
> EIP-1702. Generalized Account Versioning Scheme.  This proposal needs a versioning scheme to allow for its bytecode (and eventually eWasm bytecode) to be deployed with existing bytecode on the same blockchain.

However, such a dependency is missing in the front matter header.

EIP-1702 DRAFT is not a finalized document. Therefore I believe EIP-615 is prematurely in Last Call status. For precedent, please see ERC-721 where ERC-165 was a prerequisite and the latter was finalized before the former entered Last Call.

There will be no benefit, and much cost, in finalizing EIP-1720 if it cannot be used. The prerequisites are not met and so it can’t be used. The cost is that it cannot continue to be edited. So again, Last Call should be aborted.

Another dependency. The instruction arguments are specified to use “MSB-first, two’s-complement, two-byte positive integers”. This puts an upper bound on the non-data part (and non-`JUMPDEST` part) of contract sizes at 0x7fff. This depends on contract sizes being limited, which is currently specified by EIP-170 to be limited to 0x6000, so this is good. This dependency on EIP-170 can please be included in the front matter for cross reference purposes, and referenced in text.

# Test cases are missing

EIP-1 states:

> Test Cases - Test cases for an implementation are mandatory for EIPs that are affecting consensus changes. Other EIPs can choose to include links to test cases if applicable.

However this EIP fails to include test cases.

# Backwards compatibility is incomplete

This EIP introduces a backwards compatibility against a finalized EIP, specifically EIP-1167. Requesting please that this be added as a note for cross-reference.

# Formal verification is not shown to provide any practical benefit

The first line in the EIP states:

> …formal specification and verification are an essential tool against loss.

However this claim is not substantiated sufficiently. Only references are made under the heading “some papers” at bottom.

I have raised this topic before, but that wasn’t Last Call, so I’ll do it again here.

**Has anybody translated any deployed contract to the proposed byte code and successfully detected any actual problem using formal verification? Would EIP-615 have prevented this week’s exploit on 0x Exchange 2.0?**

# Notes on complexity are misleading

The paper hypothesizes a vulnerability where contract authors can evade formal analysis by introducing quadratic complexity against a static analyzer.

> Otherwise, Contracts can be crafted or discovered with quadratic complexity to use as denial of service attack vectors against validations and optimizations.

This is entirely impractical because no serious projects publish using EVM, they all use a higher level language. Everybody knows that a contract which does not publish its higher-level source code is suspect. And since Solidity is advertised here to be able to target EIP-615 as easily as current EVM, now therefore all the formal analysis benefits of EIP-615 already exist today against Solidity source code.

Separately, there is a note on complexity at:

> All of the instructions are O(1) with a small constant, requiring just a few machine operations each, whereas a JUMP or JUMPI typically does an O(log n) binary search of an array of JUMPDESToffsets before every jump.

This is an implementation detail. Anybody that cared to implement `JUMPDEST` lookup in `O(1)` time would simply store all bytecode in 9-bit bytes where the extra bit denotes valid jump destinations.

# Dynamic jumps are rarely used

I have provided a method to analyze existing contracts to find if they are actually using dynamic jumps or if instead there is a trick to immediately (`O(1)`) find jump destinations.

This analysis is performed here:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/615#issuecomment-467230869)












####



        opened 05:01PM - 27 Apr 17 UTC



          closed 02:51AM - 16 Jul 19 UTC



        [![](https://avatars.githubusercontent.com/u/16827129?v=4)
          gcolvin](https://github.com/gcolvin)










---
eip: 615
title: Subroutines and Static Jumps for the EVM
status: Draft
t[…]()ype: Standards Track
category: Core
author: Greg Colvin <greg@colvin.org>, Brooklyn Zelenka (@expede), Paweł Bylica (@chfast), Christian Reitwiessner (@chriseth)
discussions-to: https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm-last-call/3472
created: 2016-12-10
---

## Simple Summary

In the 21st century, on a blockchain circulating billions of ETH, formal specification and verification are an essential tool against loss. Yet the design of the EVM makes this unnecessarily difficult. Further, the design of the EVM makes near-linear-time compilation to machine code difficult. We propose to move forward with proposals to resolve these problems by tightening EVM security guarantees and reducing barriers to performance.

## Abstract

EVM code is currently difficult to statically analyze, hobbling critical tools for preventing the many expensive bugs our blockchain has experienced. Further, none of the current implementations of the Ethereum Virtual Machine—including the compilers—are sufficiently performant to reduce the need for precompiles and otherwise meet the network's long-term demands.  This proposal identifies dynamic jumps as a major reason for these issues, and proposes changes to the EVM specification to address the problem, making further efforts towards a safer and more performant the EVM possible.

We also propose to validate—in near-linear time—that EVM contracts correctly use subroutines, avoid misuse of the stack, and meet other safety conditions _before_ placing them on the blockchain.  Validated code precludes most runtime exceptions and the need to test for them.  And well-behaved control flow and use of the stack makes life easier for interpreters, compilers, formal analysis, and other tools.

## Motivation

Currently the EVM supports only dynamic jumps, where the address to jump to is an argument on the stack.  Worse, the EVM fails to provide ordinary, alternative control flow facilities like subroutines and switches provided by Wasm and most CPUs.  So dynamic jumps cannot be avoided, yet they obscure the structure of the code and thus mostly inhibit control- and data-flow analysis.  This puts the quality and speed of optimized compilation fundamentally at odds.  Further, since many jumps can potentially be to any jump destination in the code, the number of possible paths through the code can go up as the product of the number of jumps by the number of destinations, as does the time complexity of static analysis.  Many of these cases are undecidable at deployment time, further inhibiting static and formal analyses.

However, given Ethereum's security requirements, **near-linear** **`n log n`** **time complexity** is essential.  Otherwise, Contracts can be crafted or discovered with quadratic complexity to use as denial of service attack vectors against validations and optimizations.

But absent dynamic jumps code can be statically analyzed in linear time.  That allows for _linear time validation_.  It also allows for code generation and such optimizations as can be done in `log n` time to comprise an _`n log n`_ _time compiler_.

And absent dynamic jumps, and with proper subroutines the EVM is a better target for code generation from other languages, including
* Solidity
* Vyper
* LLVM IR
  * front ends include C, C++, Common Lisp, D, Fortran, Haskell, Java, Javascript, Kotlin, Lua, Objective-C, Pony, Pure, Python, Ruby, Rust, Scala, Scheme, and Swift

The result is that all of the following validations and optimizations can be done at deployment time with near-linear `(n log n)` time complexity.
* The absence of most exceptional halting states can be validated.
* The maximum use of resources can be sometimes be calculated.
* Bytecode can be compiled to machine code in near-linear time.
* Compilation can more effectively optimize use of smaller registers.
* Compilation can more effectively optimize injection of gas metering.

## Specification

### Dependencies

> **[EIP-1702](./eip-1702.md). Generalized Account Versioning Scheme.** This proposal needs a versioning scheme to allow for its bytecode (and eventually eWasm bytecode) to be deployed with existing bytecode on the same blockchain.

### Proposal

We propose to deprecate two existing instructions—`JUMP` and `JUMPI`—and propose new instructions to support their legitimate uses.  In particular, it must remain possible to compile Solidity and Vyper code to EVM bytecode, with no significant loss of performance or increase in gas price.

Especially important is efficient translation to and from [eWasm](https://github.com/ewasm/design) and to machine code.  To that end we maintain a close correspondence between [Wasm](https://webassembly.github.io/spec/core/_download/WebAssembly.pdf), [x86](https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.pdf), [ARM](https://static.docs.arm.com/100076/0100/arm_instruction_set_reference_guide_100076_0100_00_en.pdf) and proposed EVM instructions.

| EIP-615   | Wasm          | x86  | ARM
| --------- | ------------- | ---- | ---- |
| JUMPTO    | br            | JMP  | B    |
| JUMPIF    | br_if         | JE   | BEQ  |
| JUMPV     | br_table      | JMP  | TBH  |
| JUMPSUB   | call          | CALL | BL   |
| JUMPSUBV  | call_indirect | CALL | BL   |
| RETURN    | return        | RET  | RET  |
| GETLOCAL  | local.get     | POP  | POP  |
| PUTLOCAL  | local.put     | PUSH | PUSH |
| BEGINSUB  | func          |      |      |
| BEGINDATA | tables        |      |      |

#### Preliminaries

These forms
> *`INSTRUCTION`*
>
> *`INSTRUCTION x`*
>
> *`INSTRUCTION x, y`*

name an *`INSTRUCTION`* with no, one and two arguments, respectively. An instruction is represented in the bytecode as a single-byte opcode. Any arguments are laid out as immediate data bytes following the opcode inline, interpreted as fixed length, MSB-first, two's-complement, two-byte positive integers. (Negative values are reserved for extensions.)

#### Branches and Subroutines

The two most important uses of `JUMP` and `JUMPI` are static jumps and return jumps. Conditional and unconditional static jumps are the mainstay of control flow.  Return jumps are implemented as a dynamic jump to a return address pushed on the stack.  With the combination of a static jump and a dynamic return jump you can—and Solidity does—implement subroutines.  The problem is that static analysis cannot tell the one place the return jump is going, so it must analyze every possibility (a heavy analysis).

Static jumps are provided by
> `JUMPTO jump_target`
>
> `JUMPIF jump_target`
>
> which are the same as `JUMP` and `JUMPI` except that they jump to an immediate `jump_target` rather than an address on the stack.

To support subroutines, `BEGINSUB`, `JUMPSUB`, and `RETURNSUB` are provided.  Brief descriptions follow, and full semantics are given below.

> `BEGINSUB n_args, n_results`
>
> marks the **single** entry to a subroutine.  `n_args` items are taken off of the stack at entry to, and `n_results` items are placed on the stack at return from the subroutine.   The subroutine ends at the next `BEGINSUB` instruction (or `BEGINDATA`, below) or at the end of the bytecode.

> `JUMPSUB jump_target`
>
> jumps to an immediate subroutine address.

> `RETURNSUB`
>
>returns from the current subroutine to the instruction following the JUMPSUB that entered it.

#### Switches, Callbacks, and Virtual Functions

Dynamic jumps are also used for `O(1)` indirection: an address to jump to is selected to push on the stack and be jumped to.  So we also propose two more instructions to provide for constrained indirection.  We support these with vectors of `JUMPDEST` or `BEGINSUB` offsets stored inline, which can be selected with an index on the stack.  That constrains validation to a specified subset of all possible destinations.  The danger of quadratic blow up is avoided because it takes as much space to store the jump vectors as it does to code the worst case exploit.

Dynamic jumps to a `JUMPDEST` are used to implement `O(1)` jumptables, which are useful for dense switch statements.  Wasm and most CPUs provide similar instructions.

> `JUMPV n, jump_targets`
>
> jumps to one of a vector of `n` `JUMPDEST` offsets via a zero-based index on the stack.  The vector is stored inline at the `jump_targets` offset after the BEGINDATA bytecode as MSB-first, two's-complement, two-byte positive integers.  If the index is greater than or equal to `n - 1` the last (default) offset is used.

Dynamic jumps to a `BEGINSUB` are used to implement `O(1)` virtual functions and callbacks, which take at most two pointer dereferences on most CPUs.   Wasm provides a similar instruction.

> `JUMPSUBV n, jump_targets`
>
>jumps to one of a vector of `n` `BEGINSUB` offsets via a zero-based index on the stack.  The vector is stored inline at the `jump_targets` offset after the DATA bytecode, as MSB-first, two's-complement, two-byte positive integers.  If the index is greater than or equal to `n - 1` the last (default) offset is used.

#### Variable Access

These operations provide convenient access to subroutine parameters and local variables at fixed stack offsets within a subroutine.  Otherwise only sixteen variables can be directly addressed.

> `PUTLOCAL n`
>
> Pops the stack to the local variable `n`.

> `GETLOCAL n`
>
> Pushes the local variable `n` onto the stack.

Local variable `n` is the nth stack item below the frame pointer, `FP[-n]`, as defined below.

#### Data

There needs to be a way to place unreachable data into the bytecode that will be skipped over and not validated.  Indirect jump vectors will not be valid code.  Initialization code must create runtime code from data that might not be valid code.  And unreachable data might prove useful to programs for other purposes.

> `BEGINDATA`
>
> specifies that all of the following bytes to the end of the bytecode are data, and not reachable code.

#### Structure

Valid EIP-615 EVM bytecode begins with a valid header.  This is the magic number  ‘\0evm’ followed by the semantic versioning number '\1\5\0'.  (For Wasm the header is '\0asm\1').

Following the header is the BEGINSUB opcode for the _main_ routine.  It takes no arguments and returns no values.  Other subroutines may follow the _main_ routine, and an optional BEGINDATA opcode may mark the start of a data section.

### Semantics

Jumps to and returns from subroutines are described here in terms of
* The EVM data stack, (as defined in the [Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)) usually just called “the stack.”
* A return stack of `JUMPSUB` and `JUMPSUBV` offsets.
* A frame stack of frame pointers.

We will adopt the following conventions to describe the machine state:
* The _program counter_ `PC` is (as usual) the byte offset of the currently executing instruction.
* The _stack pointer_ `SP` corresponds to the [Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)'s substate `s` of the machine state.
  * `SP[0]` is where a new item is can be pushed on the stack.
  * `SP[1]` is the first item on the stack, which can be popped off the stack.
  * The stack grows towards lower addresses.
* The _frame pointer_ `FP` is set to `SP + n_args` at entry to the currently executing subroutine.
  * The _stack items_ between the frame pointer and the current stack pointer are called the _frame_.
  * The current number of items in the frame, `FP - SP`, is the _frame size_.

> **Note**: Defining the frame pointer so as to include the arguments is unconventional, but better fits our stack semantics and simplifies the remainder of the proposal.

The frame pointer and return stacks are internal to the subroutine mechanism, and not directly accessible to the program.  This is necessary to prevent the program from modifying its own state in ways that could be invalid.

Execution of EVM bytecode begins with the _main_ routine with no arguments, `SP` and `FP` set to 0, and with one value on the return stack—`code_size - 1`. (Executing the virtual byte of 0 after this offset causes an EVM to stop.  Thus executing a `RETURNSUB` with no prior `JUMPSUB` or `JUMBSUBV`—that is, in the _main_ routine—executes a `STOP`.)

Execution of a subroutine begins with `JUMPSUB` or `JUMPSUBV`, which

* pushes `PC` on the return stack,
* pushes `FP` on the frame stack
  * thus suspending execution of the current subroutine,
* sets `FP` to `SP + n_args`, and
* sets `PC` to the specified `BEGINSUB` address
  * thus beginning execution of the new subroutine.

Execution of a subroutine is suspended during and resumed after execution of nested subroutines, and ends upon encountering a `RETURNSUB`, which

* sets `FP` to the top of the virtual frame stack and pops the stack,
* sets `SP` to `FP + n_results`,
* sets `PC` to top of the return stack and pops the stack, and
* advances `PC` to the next instruction

thus resuming execution of the enclosing subroutine or _main_ routine.  A `STOP` or `RETURN` also ends the execution of a subroutine.

For example, starting from this stack,
```
_________________
      | locals      20 <- FP
frame |             21
______|___________  22
                       <- SP
```
and after pushing two arguments and branching with `JUMPSUB` to a `BEGINSUB 2, 3`
```
PUSH 10
PUSH 11
JUMPSUB beginsub
```
and initializing three local variables
```
PUSH 99
PUSH 98
PUSH 97
```
the stack looks like this
```
                    20
                    21
__________________  22
      | arguments   10 <- FP
frame |___________  11
      | locals      99
      |             98
______|___________  97
                       <- SP
```
After some amount of computation the stack could look like this
```
                    20
                    21
__________________  22
      | returns     44 <- FP
      |             43
frame |___________  42
      | locals      13
______|___________  14
                       <- SP
```
and after `RETURNSUB` would look like this
```
_________________
      | locals      20 <- FP
      |             21
frame |___________  22
      | returns     44
      |             43
______|___________  42
                       <- SP
```

### Validity

We would like to consider EVM code valid iff no execution of the program can lead to an exceptional halting state, but we must validate code in linear time. So our validation does not consider the code’s data and computations, only its control flow and stack use.  This means we will reject programs with invalid code paths, even if those paths are not reachable.  Most conditions can be validated, and will not need to be checked at runtime; the exceptions are sufficient gas and sufficient stack.  As such, static analysis may yield false negatives belonging to well-understood classes of code requiring runtime checks.  Aside from those cases, we can validate large classes at validation time and with linear complexity.

_Execution_ is as defined in the [Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)—a sequence of changes in the EVM state.  The conditions on valid code are preserved by state changes.  At runtime, if execution of an instruction would violate a condition the execution is in an exceptional halting state.  The Yellow Paper defines five such states.
>**1**  Insufficient gas

>**2**  More than 1024 stack items

>**3**  Insufficient stack items

>**4**  Invalid jump destination

>**5**  Invalid instruction

We propose to expand and extend the Yellow Paper conditions to handle the new instructions we propose.

To handle the return stack we expand the conditions on stack size:
>**2a**  The size of the data stack does not exceed 1024.

>**2b**  The size of the return stack does not exceed 1024.

Given our more detailed description of the data stack we restate condition 3—stack underflow—as
>**3**  `SP` must be less than or equal to `FP`

Since the various `DUP` and `SWAP` operations—as well as `PUTLOCAL` and `GETLOCAL`—are defined as taking items off the stack and putting them back on, this prevents them from accessing data below the frame pointer, since taking too many items off of the stack would mean that `SP` is less than `FP`.

To handle the new jump instructions and subroutine boundaries, we expand the conditions on jumps and jump destinations.
>**4a**  `JUMPTO`, `JUMPIF`, and `JUMPV` address only `JUMPDEST` instructions.

>**4b**  `JUMPSUB` and `JUMPSUBV` address only `BEGINSUB` instructions.

>**4c**  `JUMP` instructions do not address instructions outside of the subroutine they occur in.

We have two new conditions on execution to ensure consistent use of the stack by subroutines:
>**6**  For `JUMPSUB` and `JUMPSUBV` the frame size is at least the `n_args` of the `BEGINSUB`(s) to jump to.

>**7**  For `RETURNSUB` the frame size is equal to the `n_results` of the enclosing `BEGINSUB`.

Finally, we have one condition that prevents pathological uses of the stack:
>**8**  For every instruction in the code the frame size is constant.

In practice, we must test at runtime for conditions 1 and 2—sufficient gas and sufficient stack.  We don’t know how much gas there will be, we don’t know how deep a recursion may go, and analysis of stack depth even for non-recursive programs is nontrivial.

All of the remaining conditions we validate statically.

#### Costs & Codes

All of the instructions are `O(1)` with a small constant, requiring just a few machine operations each, whereas a `JUMP` or `JUMPI` typically does an `O(log n)` binary search of an array of `JUMPDEST` offsets before every jump. With the cost of `JUMPI` being _high_ and the cost of `JUMP` being _mid_, we suggest the cost of `JUMPV` and `JUMPSUBV` should be _mid_, `JUMPSUB` and `JUMPIF` should be _low_, and`JUMPTO` and the rest should be _verylow_.  Measurement will tell.

We suggest the following opcodes:
```
0xb0 JUMPTO
0xb1 JUMPIF
0xb2 JUMPV
0xb3 JUMPSUB
0xb4 JUMPSUBV
0xb5 BEGINSUB
0xb6 BEGINDATA
0xb7 RETURNSUB
0xb8 PUTLOCAL
0xb9 GETLOCAL
```

## Backwards Compatibility

These changes would need to be implemented in phases at decent intervals:
>**1.**  If this EIP is accepted, invalid code should be deprecated. Tools should stop generating invalid code, users should stop writing it, and clients should warn about loading it.

>**2.**  A later hard fork would require clients to place only valid code on the block chain.  Note that despite the fork old EVM code will still need to be supported indefinitely; older contracts will continue to run, and to create new contracts.

If desired, the period of deprecation can be extended indefinitely by continuing to accept code not versioned as new—but without validation.  That is, by delaying or canceling phase 2.

Regardless, we will need a versioning scheme like [EIP-1702](./eip-1702.md) to allow current code and EIP-615 code to coexist on the same blockchain.

## Rationale

This design was highly constrained by the existing EVM semantics, the requirement for eWasm compatibility, and the security demands of the Ethereum environment.  It was also informed by the lead author's previous work implementing Java and Scheme interpreters.  As such there was very little room for alternative designs.

As described above, the approach was simply to deprecate the problematic dynamic jumps, then ask what opcodes were necessary to provide for the features they supported.  These needed to include those provided by eWasm, which themselves were modeled after typical hardware.  The only real innovation was to move the frame pointer and the return pointer to their own stacks, so as to prevent any possibility of overwriting them. (Although Forth also uses a return stack.)  This allowed for treating subroutine arguments as local variables, and facilitated the return of multiple values.

## Implementation

Implementation of this proposal need not be difficult.  At the least, interpreters can simply be extended with the new opcodes and run unchanged otherwise.  The new opcodes require only stacks for the frame pointers and return offsets and the few pushes, pops, and assignments described above. The bulk of the effort is the validator, which in most languages can almost be transcribed from the pseudocode above.

A lightly tested C++ reference implementation is available in [Greg Colvin's Aleth fork.](https://github.com/gcolvin/aleth/tree/master/libaleth-interpreter)  This version required circa 110 lines of new interpreter code and a well-commented, 178-line validator.

## Appendix A
### Validation

Validation comprises two tasks:
* Check that jump destinations are correct and instructions valid.
* Check that subroutines satisfy the conditions on control flow and stack use.

We sketch out these two validation functions in pseudo-C below.  To simplify the presentation only the five primitives are handled (`JUMPV` and `JUMPSUBV` would just add more complexity to loop over their vectors), we assume helper functions for extracting instruction arguments from immediate data and managing the stack pointer and program counter, and some optimizations are forgone.

#### Validating Jumps

Validating that jumps are to valid addresses takes two sequential passes over the bytecode—one to build sets of jump destinations and subroutine entry points, another to check that addresses jumped to are in the appropriate sets.
```
    bytecode[code_size]   // contains EVM bytecode to validate
    is_sub[code_size]     // is there a BEGINSUB at PC?
    is_dest[code_size]    // is there a JUMPDEST at PC?
    sub_for_pc[code_size] // which BEGINSUB is PC in?

    bool validate_jumps(PC)
    {
        current_sub = PC

        // build sets of BEGINSUBs and JUMPDESTs
        for (PC = 0; instruction = bytecode[PC]; PC = advance_pc(PC))
        {
            if instruction is invalid
                return false
            if instruction is BEGINDATA
                break;
            if instruction is BEGINSUB
                is_sub[PC] = true
                current_sub = PC
                sub_for_pc[PC] = current_sub
            if instruction is JUMPDEST
                is_dest[PC] = true
            sub_for_pc[PC] = current_sub
        }

        // check that targets are in subroutine
        for (PC = 0; instruction = bytecode[PC]; PC = advance_pc(PC))
        {
            if instruction is BEGINDATA
                break;
            if instruction is BEGINSUB
                current_sub = PC
            if instruction is JUMPSUB
                if is_sub[jump_target(PC)] is false
                    return false
            if instruction is JUMPTO or JUMPIF
                if is_dest[jump_target(PC)] is false
                    return false
            if sub_for_pc[PC] is not current_sub
                return false
       }
       return true
    }
```
Note that code like this is already run by EVMs to check dynamic jumps, including building the jump destination set every time a contract is run, and doing a lookup in the jump destination set before every jump.

#### Subroutine Validation

This function can be seen as a symbolic execution of a subroutine in the EVM code, where only the effect of the instructions on the state being validated is computed.  Thus the structure of this function is very similar to an EVM interpreter.  This function can also be seen as an acyclic traversal of the directed graph formed by taking instructions as vertices and sequential and branching connections as edges, checking conditions along the way.  The traversal is accomplished via recursion, and cycles are broken by returning when a vertex which has already been visited is reached.  The time complexity of this traversal is `O(|E|+|V|)`: The sum of the number of edges and number of vertices in the graph.

The basic approach is to call `validate_subroutine(i, 0, 0)`, for `i` equal to the first instruction in the EVM code through each `BEGINDATA` offset.  `validate_subroutine()` traverses instructions sequentially, recursing when `JUMP` and `JUMPI` instructions are encountered.  When a destination is reached that has been visited before it returns, thus breaking cycles.  It returns true if the subroutine is valid, false otherwise.

```
    bytecode[code_size]     // contains EVM bytecode to validate
    frame_size[code_size ]  // is filled with -1

    // we validate each subroutine individually, as if at top level
    // * PC is the offset in the code to start validating at
    // * return_pc is the top PC on return stack that RETURNSUB returns to
    // * at top level FP = SP = 0 is both the frame size and the stack size
    // * as items are pushed SP get more negative, so the stack size is -SP
    validate_subroutine(PC, return_pc, SP)
    {
        // traverse code sequentially, recurse for jumps
        while true
        {
            instruction = bytecode[PC]

            // if frame size set we have been here before
            if frame_size[PC] >= 0
            {
                // check for constant frame size
                if instruction is JUMPDEST
                    if -SP != frame_size[PC]
                        return false

                // return to break cycle
                return true
            }
            frame_size[PC] = -SP

            // effect of instruction on stack
            n_removed = removed_items(instructions)
            n_added = added_items(instruction)

            // check for stack underflow
            if -SP < n_removed
                return false

            // net effect of removing and adding stack items
            SP += n_removed
            SP -= n_added

            // check for stack overflow
            if -SP > 1024
                return false

            if instruction is STOP, RETURN, or SUICIDE
                return true

            // violates single entry
            if instruction is BEGINSUB
                 return false

            // return to top or from recursion to JUMPSUB
            if instruction is RETURNSUB
                return true;;

            if instruction is JUMPSUB
            {
                // check for enough arguments
                sub_pc = jump_target(PC)
                if -SP < n_args(sub_pc)
                    return false
                return true
            }

            // reset PC to destination of jump
            if instruction is JUMPTO
            {
                PC = jump_target(PC)
                continue
            }

            // recurse to jump to code to validate
            if instruction is JUMPIF
            {
                if not validate_subroutine(jump_target(PC), return_pc, SP)
                    return false
            }

            // advance PC according to instruction
            PC = advance_pc(PC)
        }

        // check for right number of results
        if (-SP != n_results(return_pc)
            return false
        return true
    }
```
## Appendix B
### EVM Analysis

There is a large and growing ecosystem of researchers, authors, teachers, auditors, and analytic tools--providing software and services focused on the correctness and security of EVM code.  A small sample is given here.

#### Some Tools

* [Contract Library](https://contract-library.com/)
* [EthereumJ](https://github.com/ethereum/ethereumj)
* [Exthereum](https://github.com/exthereum/blockchain)
* [Harmony](https://github.com/ether-camp/ethereum-harmony)
* [JEB](https://www.pnfsoftware.com/blog/ethereum-smart-contract-decompiler/)
* [Mythril](https://github.com/ConsenSys/mythril)
* [Securify](https://github.com/eth-sri/securify)
* [Skale](https://www.skalelabs.com/)
* [Status](https://status.im/)

#### Some Papers

* [A Formal Verification Tool for Ethereum VM Bytecode](https://www.google.com/url?q=http://fsl.cs.illinois.edu/FSL/papers/2018/park-zhang-saxena-daian-rosu-2018-fse/park-zhang-saxena-daian-rosu-2018-fse-public.pdf)
* [A Lem formalization of EVM and some Isabelle/HOL proofs](https://github.com/pirapira/eth-isabelle)
* [A survey of attacks on Ethereum smart contracts](https://eprint.iacr.org/2016/1007.pdf)
* [Defining the Ethereum Virtual Machine for Interactive Theorem Provers](https://www.google.com/url?q=http://fc17.ifca.ai/wtsc/Defining%2520the%2520Ethereum%2520Virtual%2520Machine%2520for%2520Interactive%2520Theorem%2520Provers.pdf)
* [Ethereum 2.0 Specifications](https://github.com/ethereum/eth2.0-specs)
* [Formal Verification of Smart Contracts](https://www.cs.umd.edu/~aseem/solidetherplas.pdf)
* [JelloPaper: Human Readable Semantics of EVM in K](https://jellopaper.org/)
* [KEVM: A Complete Semantics of the Ethereum Virtual Machine.](https://www.ideals.illinois.edu/bitstream/handle/2142/97207/hildenbrandt-saxena-zhu-rodrigues-guth-daian-rosu-2017-tr.pdf)
* [Making Smart Contracts Smarter](https://eprint.iacr.org/2016/633.pdf)
* [Securify: Practical Security Analysis of Smart Contracts](https://arxiv.org/pdf/1806.01143.pdf)
* [The Thunder Protocol](https://docs.thundercore.com/thunder-whitepaper.pdf)
* [Towards Verifying Ethereum Smart Contract Bytecode in Isabelle/HOL](https://ts.data61.csiro.au/publications/csiro_full_text//Amani_BBS_18.pdf)
*[A Lem formalization of EVM 1.5](https://github.com/seed/eth-isabelle/tree/evm15)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).












It demonstrates that the vast majority of `JUMP`s on EVM are not actually dynamic.

This puts into question the underlying motivation of this EIP which is to remove dynamic jumps. This relevant analysis is not referenced from the EIP.

# Other notes/corrections

> (Negative values are reserved for extensions.)

At current, zero is also unused and could be reserved.

---

**gcolvin** (2019-07-17):

Thanks for the feedback [@fulldecent](/u/fulldecent).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> EIP-1702 DRAFT is not a finalized document. Therefore I believe EIP-615 is prematurely in Last Call status

This draft doesn’t much care what versioning scheme is provided, so long as there is one.  If necessary the core devs can hold off on assigning this EIP to a fork until such a scheme is available.  But this proposal has been languishing since December of 2016 and my availability to work on it is rapidly dwindling, so I think it’s past time to move it forward.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> This EIP introduces a backwards compatibility against a finalized EIP, specifically EIP-1167. Requesting please that this be added as a note for cross-reference.

I’m sorry, but I don’t understand the compatibility issue here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> dependency on EIP-170 can please be included in the front matter for cross reference purposes, and referenced in text.

Will do.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> this EIP fails to include test cases.

True.  This proposal was written long before this requirement was imposed.  I’ll let the core devs decide whether to grandfather it in, or ask for somebody else to prepare a new draft with test cases.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Has anybody translated any deployed contract to the proposed byte code and successfully detected any actual problem using formal verification?

Not that I know of.  I think they are waiting on the proposal to be accepted.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> The paper hypothesizes a vulnerability where contract authors can evade formal analysis by introducing quadratic complexity against a static analyzer.
> …
> This is entirely impractical because no serious projects publish using EVM, they all use a higher level language.

What gets deployed on the blockchain is EVM code.  An attacker can generate vulnerable EVM contracts by design, by fuzzing, or by scanning the blockchain looking for them.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> all the formal analysis benefits of EIP-615 already exist today against Solidity source code

There is no formal specification for Solidity.  There are at least two for the EVM.  So if you want to be certain of what of an EVM contract does you have to analyze the bytecode.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> … the vast majority of JUMP s on EVM are not actually dynamic.

Solidity uses dynamic jumps to implement function calls.

---

**shemnon** (2019-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> this EIP fails to include test cases.

True. This proposal was written long before this requirement was imposed. I’ll let the core devs decide whether to grandfather it in, or ask for somebody else to prepare a new draft with test cases.

I do not consider grandfathering out test cases for consensus critical code to be a good idea, especially with such a large change as this one.  There are 10 new opcodes, as many opcodes that has been added to the EVM since frontier, combined.

While I feel that what is in this EIP to be a good idea asking a non-specific “somebody else” to prepare the tests does not make me confident this EIP is ready for inclusion in any hard fork.

---

**gcolvin** (2019-07-17):

It’s a practical matter [@shemnon](/u/shemnon). Last year we applied for an EF grant for [@expede](/u/expede) and I to work on this proposal. For months we never got either an acceptance or a rejection. So we both took on other work. If the core devs reject this proposal it will be dead until I leave my job, [@expede](/u/expede) and [@boris](/u/boris) business fails, or somebody else decides to champion it.

I think it would be a shame to reject years of work because I didn’t do something that was not required until years after the proposal was first written.

---

**boris** (2019-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I think it would be a shame to reject years of work because I didn’t do something that was not required until years after the proposal was first written.

That’s not the point. This proposal / Working Group was not funded even though all the other ETH1x ones were because “somebody at the EF doesn’t like Boris”. At least, that’s the only feedback we got.

Thus can’t afford to spend time building tests etc. That’s the core issue for all “third party” EIPs: if you aren’t employed by the EF or Parity or Pegasys, you’ve got volunteer time only.

Greg’s wording is weird, but “our business failing” seems to mean that we might circle back around and volunteer to work on this if we have nothing else to do.

That is not the case. The way we were treated by the EF means we are unlikely to volunteer on core going forward.

---

**shemnon** (2019-07-17):

EIP requirement or not, a fully worked sample is something that would have been an aid in understanding how the opcodes work.  This EIP covers a lot of ground and contains at least three distinct categories of opcodes that may have been better served as separate EIPs.

It doesn’t need to be as exhaustive as the the reference tests but something as simple as including some of the unit tests from your proof of concept implementation and making them normative is what is needed.

---

**gcolvin** (2019-07-17):

[@boris](/u/boris) All I meant is that so long as you and [@expede](/u/expede) are starting up a business Brooke will not have time to champion this EIP.  If your business fails (and I pray it succeeds) then she might, given EF or other support.  Same goes for me and my current employment.  The point remains that it would be a shame to see years of work lost because the primary author could no longer afford to go without funding.

---

**gcolvin** (2019-07-17):

[@shemnon](/u/shemnon)  I’ll see what I can do.  What is there now is a section laying out the effects of the primitive instructions on the stack.  From a conversation with Dimitry writing test vectors for this EIP should not be very difficult for someone who knows how to do it.  I don’t think I can reconstruct the testing I did in 2017.

We discussed breaking up the EIP earlier. If we remove dynamic jumps these are the minimal set of opcodes needed to replace them.  They are also the minimal set needed to map one-to-one to Wasm opcodes.  It would be a lot of work at this point to spit the EIP up, and we would have to start the process over for each resulting new EIP.  Which, given the constraints on my future time, would have the same effect as withdrawing this EIP completely.

---

**shemnon** (2019-07-17):

Have the Vyper and Solidity projects had a look at these opcodes?  How would they impact their tooling?  Would they use it or ignore it?

---

**gcolvin** (2019-07-17):

[@fubuloubu](/u/fubuloubu) tells me the Vyper project (or at least he) is in support.  As I recall it the Solidity team added hooks for at least the primitive opcodes into Yul.  I think some degree of support was added to Solidity as well.  [@axic](/u/axic) would know.

---

**gcolvin** (2019-07-18):

[@shemnon](/u/shemnon)  I just checked the source.  Yul and Solidity have hooks (defined opcodes and empty code generation functions) for the eventual implementation of this proposal.  [@axic](/u/axic) or [@chriseth](/u/chriseth) would know how much work remains.

---

**fubuloubu** (2019-07-18):

We moved from internal calls to dynamic jumps for gas savings within our contracts and have had nothing but problems with it. This proposal would be very helpful, as it would allow us to get the safety we need while saving gas, which is what lead us to make that decision.

---

**axic** (2019-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> We moved from internal calls to dynamic jumps for gas savings within our contracts and have had nothing but problems with it. This proposal would be very helpful, as it would allow us to get the safety we need while saving gas, which is what lead us to make that decision.

A quick note here: [EIP-1380: Reduced gas cost for call to self](https://eips.ethereum.org/EIPS/eip-1380) would also help achieving that by using the old system for calls in Vyper.

---

**axic** (2019-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Yul and Solidity have hooks (defined opcodes and empty code generation functions) for the eventual implementation of this proposal. @axic or @chriseth would know how much work remains.

The Yul assembler has support for a version of EIP615 from 2 years ago. No recent changes are applied. Back when it was implemented there were no decision on the size of the immediate. The output of the assembler was never tested given there is no testing environment for it.

Solidity to Yul is still progress, so there is no complete support for Solidity to EVM615.

---

**chriseth** (2019-07-18):

Solidity has zero support for this. Many internal routines of the code generator would have to be rewritten or at least modified.

There is support for compiling Yul to something like this proposal, but it is completely untested. Furthermore, we are currently working on a full rewrite of the code generator to target Yul. Once that is finished, we can compile to both web assembly and execution environments that require static jumps, but this will still take several months.

In general, I strongly oppose this proposal in its current form. I think the introduction of multi-byte opcodes is dangerous and in general, it is a big change to EVM implementations.

The proposal was initially written with speedup in mind and not with easy of verification. The speedup turned out to be not really present, Pawel’s evmone implementation seems to be a much better solution.

I do not see the benefit of ease of verification worthwhile when compared to the risk of radical changes to the EVM, especially as implementations still need to keep both implementations. If code is analyzed, symbolic execution has to be performed in any case. In most situations, this can easily resolve the jump targets even when they are taken from the stack. At least when compiled from Solidity, the situations where this is difficult will still remain: The only situation where the jump target is not directly available on the stack is when function types are used. These function types would still need a dispatch table, so the problem is not really solved. The benefit of a dispatch table over dynamic jumps is of course that the set of potential targets is smaller. I would say that this set can already be restricted in the current EVM by analyzing how many elements on the stack are accessed by a routine, how many elements are returned and similar techniques. Furthermore, additional output from the compiler can also be used to improve the analysis - the compiler knows which jumpdest is dynamic and which is not. Unless when jump targets are read from storage (and maybe even then!), a formal system should be able to verify the correctness of this information to guard against compiler bugs.

In closing, I think this is a problem that should be solved above the EVM. It is a big risk to modify the EVM implementations and also the Solidity code generator to conform to it. Even when this proposal is implemented, malicious code can still run the old way, so this can only be a protection against bugs and not against bad intent. If it is just about finding bugs, we should have access to the source code and can use the help of the compiler and other tools. Furthermore, instead of adapting Solidity’s “legacy” code generator, I would prefer to focus on the re-implementation that uses Yul. The code that is generated from Yul will already use a dispatch table instead of dynamic jumps and it should be rather straightforward to resolve all jump destinations.

---

**gcolvin** (2019-07-18):

Thanks for the feedback [@chriseth](/u/chriseth). Most of it would have been more helpful when you co-authored this proposal in 2016.  By now it is simply too late to change the form of this proposal–it would amount to abandoning the proposal, probably permanently.  The best I can do now to simplify it would be to stick to the primitive operations and eliminate JUMPV, JUMPSUBV, GETLOCAL, and PUTLOCAL.

Improving the tractability of formal analysis of EVM code was a desiderata from the start. (See link to original proposal below.)  The performance gains were to be had by facilitating near-linear-time compilation, in the same way that Wasm compilers like [Lightbeam](https://github.com/CraneStation/lightbeam) take advantage of its clean control flow to that end.  My measurements indicate that evmone is about twice as fast as aleth, and my study of the code indicates that this is primarily because it implements optimizations that you decided not to pay me to implement for aleth back in 2017.  It’s true that those optimizations do not depend on this proposal.

https://github.com/ethereum/EIPs/issues/184

---

**shemnon** (2019-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> and my study of the code indicates that this is primarily because it implements optimizations that you decided not to pay me to implement for aleth back in 2017.

Please, let’s keep the discussion technical and not personal.

---

**gcolvin** (2019-07-19):

Thank you, [@shemnon](/u/shemnon).  And my apologies, [@chriseth](/u/chriseth).

---

**gcolvin** (2019-07-20):

[@chriseth](/u/chriseth) has expressed very belated but very strong and reasoned [objections](https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm-last-call/3472/18) to [EIP-615](http://eips.ethereum.org/EIPS/eip-615).  Being as he is a core developer and coauthor of the proposal I must take it that there is not consensus to move forward.  I am withdrawing the proposal from further consideration.


*(12 more replies not shown)*
