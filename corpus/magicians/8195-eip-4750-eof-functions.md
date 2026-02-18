---
source: magicians
topic_id: 8195
title: "EIP-4750: EOF Functions"
author: axic
date: "2022-02-03"
category: EIPs > EIPs core
tags: [evm, opcodes, shanghai-candidate, evm-object-format]
url: https://ethereum-magicians.org/t/eip-4750-eof-functions/8195
views: 4158
likes: 3
posts_count: 23
---

# EIP-4750: EOF Functions

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4750)





###



Individual sections for functions with `CALLF` and `RETF` instructions

## Replies

**gumb0** (2022-02-04):

We have considered alternative formats for representing section types in EOF container, but decided not to overload EIP text with it. Here’re some ideas:

### 0. Version proposed in EIP: one type section with types for all code sections

```auto
format, magic, version, type_section_header, (code_section_header)+, [data_section_header], 0, type_section_contents, (code_section_contents)+, [data_section_contents]
```

```auto
type_section_header := 3, number_of_code_sections * 2 # section kind and size
type_section_contents := 0, 0, code_section_1_inputs, code_section_1_outputs, code_section_2_inputs, code_section_2_outputs, ..., code_section_n_inputs, code_section_n_outputs
```

### 1. Version with multiple type sections, one type section per each code section:

```auto
format, magic, version, (type_section_header)+, (code_section_header)+, [data_section_header], 0, (type_section_contents)+, (code_section_contents)+, [data_section_contents]
```

```auto
type_section_header := 3, 2 // section kind and size
type_section_0_contents := 0, 0
type_section_n_contents := code_section_n_inputs, code_section_n_outputs
```

This is less compact than proposed version, requiring `n` bytes just for each type section kind.

### 2. Version where all types are encoded inline in type section headers, removing the need for type section contents:

```auto
format, magic, version, (type_section_header)+, (code_section_header)+, [data_section_header], 0, (code_section_contents)+, [data_section_contents]
```

```auto
type_section_n_header := 3, code_section_n_inputs, code_section_n_outputs
```

This would be most compact and require fewer reads to get each section type, but it violates section definition from EIP-3540 (its definition requires each section header to contain only section size), so we decided against it for consistency.

### 3. Version where instead of designated type sections we encode inputs and outputs number as two first bytes of each code section.

In this case it makes sense to introduce a new kind of code section for this - “typed code section” - but the first code section would remain regular untyped one:

```auto
format, magic, version, code_section_header, (typed_code_section_header)+, [data_section_header], 0, code_section_contents, (typed_code_section_contents)+, [data_section_contents]
```

```auto
typed_code_section_header := 3, size
type_code_section_contents := inputs, outputs,
```

Downsides of this: having more than one kind of code sections might be confusing, having non-code bytes inside code sections would mean we have to be careful to not consider them executable (i.e. code bounds are `[section_start+2, section_end]`), `PC=0` corresponds to offset `section_start+2`.

---

Overall we don’t feel very strongly about picking one version over others, if anyone has good arguments for alternative format, please let us know.

---

**ekpyron** (2022-02-04):

Adding `TAILJUMPF` or `TAILCALLF` (with obvious specs, i.e. consumes current stack as arguments, called function has to return the same amount of values as the current one) may be worth a thought as an eventual extension to this.

---

**gcolvin** (2022-02-04):

What are the advantages of this approach over EIP-2315?  It would seem to be both less efficient and – by moving each function into its own section –  get in the way of further optimization.

The meta question is, What do want to do with additional code sections?  To me they seem most useful as a way of linking in library code as modules with defined interfaces.

---

**gcolvin** (2022-02-07):

Leaving the meta-question aside…

My biggest concern is that we wind up with new exceptional halting conditions (and new machine state and code to enforce them) when I’m trying to get rid of them. However, I’m pretty sure they can be enforced at validation time instead along the lines of EIP-3779.

My second biggest concern is that you can’t do tail call optimization.  But that’s the price we pay for some useful structure.  That’s part of why I’ve come to like having, in Intel’s terminology, both subroutines and procedures.  These are well-defined procedures.

---

**gcolvin** (2022-02-23):

> Version where instead of designated type sections we encode inputs and outputs number as two first bytes of each code section.

I’d prefer something like this.  It could generalize nicely to a more flexible section header.

> having non-code bytes inside code sections would mean we have to be careful to not consider them executable

If the first byte is a new opcode the rest can be encoded as the immediate data of that opcode.

---

**gumb0** (2022-03-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> It would seem to be both less efficient and – by moving each function into its own section – get in the way of further optimization.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> My biggest concern is that we wind up with new exceptional halting conditions (and new machine state and code to enforce them) when I’m trying to get rid of them. However, I’m pretty sure they can be enforced at validation time instead along the lines of EIP-3779.

I agree it might be less efficient comparing to 2315 because base pointer is saved additionally in the return stack, and this is a price to pay for more runtime correctness guarantees. I.e. 4750 approach guarantees that callee cannot read caller’s stack, while 2315 allows this.

And yes, in the future we should be able to get rid of these runtime underflow checks by using 3779-style validation. Then inefficiency goes away, too.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> My second biggest concern is that you can’t do tail call optimization. But that’s the price we pay for some useful structure. That’s part of why I’ve come to like having, in Intel’s terminology, both subroutines and procedures. These are well-defined procedures.

Tail call optimization should be possible with a special new opcode like TAILCALLF as [@ekpyron](/u/ekpyron) noted above.

---

**gumb0** (2022-03-10):

Overall 2315 approach is less restricted and I guess allowing more funky optimizations.

And 4750 is more strict, with more runtime checks, which allows for simpler reasoning about bytecode and its structure, fewer edge cases in protocol rules, possibly easier to audit compilers’ code.

I can also see both approaches possibly co-existing (less restricted “subroutines” inside restricted “procedures”), if compiler authors would find this complexity worthwhile.

---

**gumb0** (2022-03-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> having non-code bytes inside code sections would mean we have to be careful to not consider them executable

If the first byte is a new opcode the rest can be encoded as the immediate data of that opcode.

I like this idea more than just bytes with a special meaning inside code section. (but this wastes precious opcode space)

---

**gcolvin** (2022-03-10):

I’ve roughly sketched out an extension to this proposal – [EOF - Modules and Procedures - HackMD](https://hackmd.io/@gcolvin/S15_OxdW9) – that allows for multiple entry points to each code section, mainly by having one type section for each code section.  I’ve called these *procedures*  – per [Procedures for the EVM - HackMD](https://hackmd.io/@gcolvin/r1XVbWQVK) –  to distinguish them from the [Simple Subroutines for the EVM - HackMD](https://hackmd.io/@gcolvin/HJ5Nv6iXt) they are built on, and from the [EIP-4750](https://eips.ethereum.org/EIPS/eip-4750) *functions* defined here.

I’ve made a PR.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4919)














####


      `master` ← `gcolvin:patch-6`




          opened 03:59PM - 15 Mar 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/6/63a6cccc763f1241415aa726f7d7dea80a2b86da.png)
            gcolvin](https://github.com/gcolvin)



          [+48
            -56](https://github.com/ethereum/EIPs/pull/4919/files)







Expand code sections from single-entry functions to multiple-entry modules.

W[…](https://github.com/ethereum/EIPs/pull/4919)hen opening a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

---

**gcolvin** (2022-09-10):

I closed this in favor of [EIP-5450: EOF - Stack Validation](https://eips.ethereum.org/EIPS/eip-5450).  Thanks!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Update EIP-4750: Static stack use validation for EOF functions. by gcolvin · Pull Request #5109 · ethereum/EIPs · GitHub
>
>
> The only other change I’d beg for is longer names to distinguish them from all of the other CALL opcodes. CALLFN, CALLFUN, CALLFUNC … ?
>
>
> @gumb0 @chfast @axic

---

**gcolvin** (2022-09-10):

I still prefer that EOF code sections represent [Modules](https://github.com/ethereum/EIPs/pull/4919) containing multiple procedures rather than being a single [Function](https://eips.ethereum.org/EIPS/eip-4750).  This allows for low-level optimizations within a module, but no control flow between modules except via defined interfaces.  In my opinion modules provide a more useful level of packaging.

---

**gcolvin** (2022-10-28):

Multiple entry points can also be added in a future upgrade, so they are not at all a showstopper for me.  Let’s just keep in mind that they do allow for inter-procedural optimizations, which single-entry code sections impede. Modules could also support linking libraries of separately-compiled code sections into programs, which is a traditional purpose of object file formats.  I’ve closed this PR.

---

**gcolvin** (2022-10-28):

> And 4750 is more strict, with more runtime checks, which allows for simpler reasoning about bytecode and its structure, fewer edge cases in protocol rules, possibly easier to audit compilers’ code.

From my point of view leaving checks until runtime makes reasoning more difficult – you don’t know for sure that a program won’t halt in those ways –  but with [EIP-5450: EOF - Stack Validation](https://eips.ethereum.org/EIPS/eip-5450) the constraints can mostly be checked at validation time.  So I think this proposal should be made to require 5450, and most all of the places that call for an exceptional halt should be changed to use “MUST”.

---

**haltman-at** (2022-12-17):

Hey, I notice that this EIP doesn’t include any requirement that when using JUMPF the function being jumped to has the same number of outputs as the current function.  That seems like it could have some pretty odd results.  I suspect there should be such a requirement.

---

**gumb0** (2022-12-19):

It is validated at deploy-time, see `Code Validation` section of the spec:

> Code section is invalid in case an immediate argument of any JUMPF is such that type[callee_section_index].outputs != type[caller_section_index].outputs, i.e. it is allowed to only jump to functions with the same output type.

---

**haltman-at** (2022-12-19):

Oh, I see, I missed that, thanks!

---

**purplehat** (2023-01-05):

> Deprecating JUMPDEST analysis

For my understanding, does this refer to deprecating the `JUMPDEST` op-code itself, or just in reference to a change in how Ethereum client-implementations do `JUMPDEST` analysis?

---

**shemnon** (2023-01-05):

The JUMPDEST analysis is what is deprecated, replaced with code and stack validaiton.

JUMPDEST becomes a NOOP code inside of EOF code (zero stack impact and no external changes on invocation).

---

**purplehat** (2023-01-05):

Roger that–makes sense to me, thank you for clarifying! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**rabib** (2023-04-01):

> JUMPDEST (0x5b ) instruction is renamed to NOP (“no operation”)

This nomenclature makes sense for EOF code, but if legacy contracts are to continue being executed, we need to retain `JUMPDEST`.

Or is the idea that EOF enables versioning of the opcode table, and therefore different versions will include different names for opcodes? So EOFv1’s version of the opcode table will see `JUMPDEST` replaced by `NOP`?


*(2 more replies not shown)*
