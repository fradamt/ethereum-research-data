---
source: magicians
topic_id: 6806
title: "EIP-3690: EOF - JUMPDEST Table"
author: axic
date: "2021-08-06"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-3690-eof-jumpdest-table/6806
views: 3892
likes: 2
posts_count: 9
---

# EIP-3690: EOF - JUMPDEST Table

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3690)





###



Details on Ethereum Improvement Proposal 3690 (EIP-3690): EOF - JUMPDEST Table

## Replies

**gcolvin** (2021-08-15):

I think it is important that EVM code directly defines EVM execution without the need for external tables.  (Consider the difficulty in modifying the Yellow Paper to express this proposal.)  Especially tables that the human coder will need fancy tools to encode.

Tables that provide auxiliary information (e.g. useful for validation or optimization,) or that are created at init-time make more sense to me.

Also, it seems the effect of making JUMPDEST undefined is to make almost all existing code undefined.  Why can’t we just leave JUMPDEST be?

It would seem to be more useful to introduce the static jumps and jumptables that [@gumb0](/u/gumb0) is working on and the static version of EIP-2315 that I am working on.  Dynamic jumps can then be deprecated going forward, jumpdests will be unnecessary, and init-time jumpdest analysis and runtime checking would only be needed for legacy code.

Further, think (correct me if I am wrong) that Solidity almost always uses jumps statically - that is, the value on the top of the stack is constant.  And I was telling [@holiman](/u/holiman) recently that,

“I think it actually isn’t that hard to determine which jumps have a constant argument and avoid checking their destination at runtime.  Just maintain a stack during validation, marking stack slots created by PUSH or PC as const, carrying the const-ness through swaps and dups, and unmarking when top of stack becomes the result of a non-const operator (arithmetic, calls, gas, etc.).”

If so, then most existing code can be shown at init-time to have only valid jumps, and jumpdest tables can created at init-time for the few exceptions.  If desired, programs with invalid jumps can be deprecated so that no jumpdest tables or runtime checking is needed.

---

**gcolvin** (2021-08-17):

If my above comment wasn’t confused and confusing enough, I have more confusion.

> Currently existing contracts require no validation of correctness, but every time they are executed, a list must be built containing all the valid jump-destinations. This is an overhead which can be avoided, albeit the effect of the overhead depends on the client implementation.

As I indicated, we won’t need jumpdest tables at all going forward if we deprecate JUMPs and replace them with static jumps and subroutines, and/or do a static analysis to validate jump destinations at init time.  (And of course this also saves the cost of checking each jump at runtime.)

Failing that, if we take out JUMPDEST instructions then the only necessarily invalid jump destinations are inside of immediate data - so a (typically smaller?) table of invalid locations is what is needed.

And there may be reasons to leave JUMPDEST instructions in - they do help mark programmer’s intent, make it easier to delimit basic blocks, and serve as a place to charge for gas and stack checking once we can do that again.

Regardless, the cost of validating jumps or of creating a table of invalid or valid jumps is (I think) proportional to the size of the code.  So why can’t we just do it at init-time and charge for gas according to the size of the code?

Also, why is the “jumpdests load” column empty for all but the worst case?  It seems the table still needs to be decoded, parsed, and validated.  And possibly rewritten into whatever form the client prefers to use at runtime.

> Finally, this change puts an implicit bound on “initcode analysis” which is now limited to jumpdests section loading of max size of 0xffff. The legacy code remains vulnerable.

It seems that going forward we can explicitly limit the size of the initcode.  Does this not take care of the vulnerability?  Or am I still not understanding the vulnerability?

---

**gumb0** (2021-08-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I think it is important that EVM code directly defines EVM execution without the need for external tables.

Well I think this goal would be limiting too much what we can achieve with EOF. Even the simplest separation of code and data sections (proposed in [EIP-3540](https://eips.ethereum.org/EIPS/eip-3540)) already requires for EVM to access something (data section) outside of the executed code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Also, it seems the effect of making JUMPDEST undefined is to make almost all existing code undefined. Why can’t we just leave JUMPDEST be?

No, it doesn’t affect any existing code, the new rules are only for EOF-formatted code.

The motivations for making JUMPDEST undefined (as opposed to leaving it noop) are: cleaning up opcode list, eliminating confusion of having both a JUMPDEST section and an opcode,  not allowing users to deploy obviously stupid (or at least useless) things, generally having less unneeded flexibility to avoid future backwards compatibility problems.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> As I indicated, we won’t need jumpdest tables at all going forward if we deprecate JUMPs and replace them with static jumps and subroutines, and/or do a static analysis to validate jump destinations at init time. (And of course this also saves the cost of checking each jump at runtime.)

I think overall this is a valid critique: if we were sure that getting rid of dynamic jumps alltogether was around the corner, then this proposal would be unneded complication. But if we expect that dynamic jumps are going to exist for a while, this proposes an optimizing improvement to how they work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> And there may be reasons to leave JUMPDEST instructions in - they do help mark programmer’s intent, make it easier to delimit basic blocks, and serve as a place to charge for gas and stack checking once we can do that again.

All this is still possible with this proposal without having JUMPDEST bytes inside code section.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Regardless, the cost of validating jumps or of creating a table of invalid or valid jumps is (I think) proportional to the size of the code. So why can’t we just do it at init-time and charge for gas according to the size of the code?

How is this different from what we do now?

The motivation for this proposal is getting rid of repeating the same analysis for each execution.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Finally, this change puts an implicit bound on “initcode analysis” which is now limited to jumpdests section loading of max size of 0xffff. The legacy code remains vulnerable.

It seems that going forward we can explicitly limit the size of the initcode. Does this not take care of the vulnerability? Or am I still not understanding the vulnerability?

Yes, this paragraph refers to [EIP-3540](https://eips.ethereum.org/EIPS/eip-3540) encoding code section size as uint64, and therefore implicitly setting the code size limit (and taking care of vulnerability). This doesn’t affect legacy initcode, which still can have unlimited size.

---

**gcolvin** (2021-08-18):

OK - I’m starting to understand.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gumb0/48/12_2.png) gumb0:

> gcolvin:
>
>
> I think it is important that EVM code directly defines EVM execution without the need for external tables.

Well I think this goal would be limiting too much what we can achieve with EOF.

Simply separating code into sections isn’t the issue - though I’m not sure how the data section will be accessed by the code – via CODECOPY?

The issue is that putting the jumpdests into an encoded table separate from the code is a much less clear way to present the same information as leaving them as operators within the code - less clear for the reader, and more difficult to write.  And the only reason we *have * to have jump destinations is to check dynamic jump locations at runtime.

So I do think deprecating or constraining the existing JUMP opcodes is the way to go, and should be the focus.

As for not changing the meaning of JUMPDEST - I’d like to put off the “two interpreters” problem for as long as we can.  That is, as much as possible, existing code should not require the interpreter to execute the same opcodes in different ways,  and should continue to be valid according to the new rules.

> The motivation for this proposal is getting rid of repeating the same analysis for each execution.

Yes.  It seems that going forward whatever analysis we do – jumpdests, gas, stack – can be done at creation time rather than at execution time.  If I understand things, the initcode is the exception, and I’m suggesting (as has [@holiman](/u/holiman)) that we put an explicit limit on initcode size to bound the vulnerability.

---

**chfast** (2021-08-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Also, why is the “jumpdests load” column empty for all but the worst case? It seems the table still needs to be decoded, parsed, and validated. And possibly rewritten into whatever form the client prefers to use at runtime.

We assume the same worst case figure (9.36) for all cases.

---

**gcolvin** (2021-08-30):

I think the best way to deal with jumdest taebles is not to have them at all.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png)

      [EIP-3779: Safer Control Flow for the EVM](https://ethereum-magicians.org/t/eip-3779-safe-control-flow-for-the-evm/6975) [EIPs core](/c/eips/eips-core/35)




> I have withdrawn this proposal.  The algorithm cannot be made to work
>
> Abstract
> This EIP specifies validation rules for some important safety properties, including
>
> valid jump destinations,
> valid instructions,
> no stack underflows, and
> no stack overflows without recursion.
>
> Valid contracts will not halt with an exception unless they either run out of gas or overflow stack during a recursive subroutine call.
> Code is validated at contract creation time – not runtime – by the provided …

---

**gcolvin** (2021-09-02):

To pull together my scattered thoughts - I strongly object to this EIP, and to this general approach.  It makes code too hard to write, and too hard to read, and does not fit the simple state machine model of EVM execution.  We have proposals on the table that make jumpdest tables unnecessary, and I believe those proposals or work in that direction is the way to go.

(Would not let me reply, so had to make this edit:)

To elaborate a little…

Currently contracts are literally just a string of bytes, and can be (and are) written and read with simple tools – a text editor, a table of opcodes, and a hex calculator may suffice.  EOF doesn’t fundamentally change that.  With this proposal you need an auxiliary table of valid jump destinations with a non-trivial encoding and decoding.  So specialized tools are needed even to read a contract, and existing bytecode and tools (e.g. disassemblers) become more difficult to port to EOF.

This seems a high price to pay just to speed up validation when we have yet to deliver an upgrade with any validation at all.  And [@holiman](/u/holiman) explained to me recently that his current jumpdest analysis is actually faster than traversing every byte in the code,  so it’s not clear to me how much of a performance gain we can actually get.  And over time we will likely be adding further validation, so it’s not clear to me how much difference any gains would make to total validation time going forward.

---

**gcolvin** (2021-09-21):

I’m confused by the performance analysis, which I think is central to this proposal.

My Python is weak, but…  The validation algorithm appears to create a list of JUMPDEST offsets by decoding and decompressing the table created by the person or program writing the bytecode.  The inner loop of the validation then traverses all of the non-pushdata bytes, attempting to remove the current byte offset from that list of offsets.  OK?

By contrast, the current JUMPDEST-analysis also traverses all of the non-pushdata bytes, marking the pushdata offsets in a bitvector or other structure.

So this EIP seems to require preprocessing of an external table and then accessing a data structure for every non-pushdata byte, versus no preprocessing and then accessing a data structure for every push instruction.

It’s hard for me to see how the former could be so much faster than the latter, depending on a number of factors the EIP doesn’t break out.  Speed of access to data structures is language and structure dependent, but the EIP should at least tell us not just how many JUMPDESTs are in the tested code, but also how many pushes and how much pushdata.

(Had to delete unanswered comments before being allowed to make more.  They weren’t very important.)

(And had to add below as an edit to this comment for the same reason.)

I dug up a [histogram of opcode frequencies](https://gist.github.com/gcolvin/ab8993d79d583076f3c6bc072e7ba0c6) I made for thousands of contracts near the end of last year’s chain.  340,604,415 instructions in all.  Some stats taken from that are below. 7% of the instructions are JUMPDEST, 23% of the instructions are a PUSH, and 43% of the total bytes are pushdata.

So for this sample I’d say that:

- Eliminating JUMPDEST wouldn’t safe very much space.
- Both algorithms would traverse about 341 million instructions.
- The validation algorithm for this EIP would access a list of JUMPDEST offsets about 341 million times.
- The JUMPDEST-analysis algorithm would access a bitvector of pushdata offsets about 78 million times.

So I might be miscalculating or missing something, but it seems that JUMPDEST-analysis should be faster than this EIP unless accessing the lists of JUMPDEST offsets is much faster than accessing the bitvectors of pushdata offsets.

| OP | Count | % | pushdata | % pushdata | % data |
| --- | --- | --- | --- | --- | --- |
| JUMPDEST | 22,374,953 | 6.57% |  |  | 6.57% |
| JUMPI | 14,963,477 | 4.39% |  |  | 4.39% |
| JUMP | 11,389,635 | 3.34% |  |  | 3.34% |
| All PUSH | 78,137,163 | 22.94% | 261,092,018 | 100% | 43.39% |
| PUSH20 | 2,921,374 | 0.86% | 58,427,480 | 22.38% | 9.71% |
| PUSH32 | 1,818,938 | 0.53% | 58,206,016 | 22.29% | 9.67% |
| PUSH2 | 28,280,939 | 8.30% | 56,561,878 | 21.66% | 9.40% |
| PUSH1 | 37,886,773 | 11.12% | 37,886,773 | 14.51% | 6.30% |
| PUSH4 | 5,247,460 | 1.54% | 20,989,840 | 8.04% | 3.49% |

