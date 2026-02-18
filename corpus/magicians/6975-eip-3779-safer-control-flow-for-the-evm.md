---
source: magicians
topic_id: 6975
title: "EIP-3779: Safer Control Flow for the EVM"
author: gcolvin
date: "2021-08-30"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-3779-safer-control-flow-for-the-evm/6975
views: 3485
likes: 7
posts_count: 21
---

# EIP-3779: Safer Control Flow for the EVM

I have **withdrawn** this proposal.  The algorithm cannot be made to work ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=15)

## Abstract

This EIP specifies validation rules for some important safety properties, including

- valid jump destinations,
- valid instructions,
- no stack underflows, and
- no stack overflows without recursion.

Valid contracts will not halt with an exception unless they either run out of gas or overflow stack during a recursive subroutine call.

Code is validated at contract creation time – not runtime – by the provided algorithm.  This is a one-pass algorithm, linear in the size of the bytecode, so as not to be a DoS surface.


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3779)





###



Ensure an essential level of safety for EVM code.

## Replies

**pipermerriam** (2021-08-30):

Am I correct that is is intended to be a possible improvement under EOF (EIP3540) but that the exact mechanism through which this would be integrated with EOF is not currently specified?

---

**gcolvin** (2021-08-30):

In the end this just specifies a few more rules, in the same way that EIP-3690 “extends contact creation validation rules (as defined in EIP-3540).”  I should be more clear about that.

The validation algorithm (or its equivalent) would presumably be run at code-validation time, as defined in EIP-3540.  I should be more clear about that.  Logically, it could be run after the code given there is run.  For performance reasons an implementation would probably integrate the code into a single pass.

---

**axic** (2021-09-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> In the end this just specifies a few more rules, in the same way that EIP-3690 “extends contact creation validation rules (as defined in EIP-3540).” I should be more clear about that.

[3690](https://eips.ethereum.org/EIPS/eip-3690) extends the rules defined in [3670](https://eips.ethereum.org/EIPS/eip-3670). The basic validation rules are defined by 3670 and not [3540](https://eips.ethereum.org/EIPS/eip-3540).

For clarity I suggest to provide a reference implementation in Python which extends the validation of 3670 the same way 3690 does.

---

**gcolvin** (2021-09-01):

Aha.  I’ve been using Go for example implementations because I don’t know Python, and when I write the reference implementation it will almost surely be a draft PR against Geth.

Anyway, this PR would render 3670 unnecessary - all jump destinations are validated, and no jumpdest table is needed.  However, EIPs generally should not reference other EIPs that are still Drafts.  We are making an exception for 3540 because it is almost sure to go in.  3670 is more controversial.

---

**axic** (2021-09-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Anyway, this PR would render 3670 unnecessary - all jump destinations are validated, and no jumpdest table is needed.

3670 does not introduce a jumpdest table (3690 does), so not sure what do you mean.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> However, EIPs generally should not reference other EIPs that are still Drafts. We are making an exception for 3540 because it is almost sure to go in.

3540/3670/3690 are all in Review and not Draft.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> 3670 is more controversial.

Why is 3670 controversial?

---

**gcolvin** (2021-09-02):

> 3540/3670/3690 are all in Review and not Draft.

Good, I and I think [@MicahZoltu](/u/micahzoltu) I missed that, or it changed since his review.

> Why is 3670 controversial?

Sorry - I meant 3690.  3670 is good.  3690 I don’t like at all.

---

**gcolvin** (2021-09-03):

I’ve added an EOF container section with a jumptable which gives valid jump destinations for every dynamic jump.  This extends the range of valid programs without sacrificing tractable validation.

---

**gumb0** (2021-09-28):

> I’ve added an EOF container section with a jumptable which gives valid jump destinations for every dynamic jump. This extends the range of valid programs without sacrificing tractable validation.

I would prefer this extension to have a separate opcode pair (`JUMPTABLE` / `JUMPTABLEI` ?), and maybe to be proposed in a separate EIP.

Now it seems like two different semantics (that will need two different implemantations) conflated into `JUMP/JUMPI`.

---

**gumb0** (2021-09-28):

Some more comments / confusions:

> Valid contracts will not halt with an exception unless they either run out of gas or overflow stack during a recursive subroutine call.

As I understand here by subroutines you mean subroutines as they’re currently generated by compilers (with dynamic jumps).

So recursive call to a subroutine can overflow, but why wouldn’t be the same possible with a simple loop doing `PUSH` ?

> A new EOF section called vjumptable (section_kind = 4 ) is introduced. It contains a sequence of n tuples (jumpsrc, jumpdesti_, sorted in ascending lexicographic order.

Please specify how `jumpsrc` and `jumpdest` are encoded (16-bit unsigned integer?)

> Every JUMP and JUMPI either
>
>
> matches at least one tuple in the vjumptable or the vtraptable, or
> is static

First, as noted above these two cases I think should better be different opcodes.

Then, for the tabulated jump, I think validation should check:

- each jumpsrc and jumpdest in both tables points to an instruction (is within code bounds and doesn’t point to immediate)

potentially we could restrict jumpdest to point to JUMPDEST opcode for consistency. Not sure it’s worth it, but it probably will simplify breaking into blocks?
- jumpsrc could alse be additionally restricted to point to a tabulated jump instruction

each tabulated jump instruction always has exactly one item in `vtraptable` with corresponding `jumpsrc`.
number of items in `vjumptable` for each `jumpsrc` is not contstained (can be 0)

Your algorithm code doesn’t seem to check all potential destinations of tabulated jumps, did you intend to support switch-like control flow with this at all?

---

**gcolvin** (2021-09-28):

> … subroutines as they’re currently generated by compilers (with dynamic jumps).

Yes, as limited by the rules.  I want to loosen up the rules enough to capture most of what Solidity generates.

> … So recursive call to a subroutine can overflow, but why wouldn’t be the same possible with a simple loop doing PUSH ?

Because that breaks the constant stack depth rule.

> … A new EOF section called vjumptable (section_kind = 4 ) is introduced. It contains a sequence of n tuples (jumpsrc, jumpdesti_, sorted in ascending lexicographic order.

Please specify how `jumpsrc` and `jumpdest` are encoded (16-bit unsigned integer?)

The whole table layout needs to change, so this will get fixed, thanks.  Probably 2 MSB-first bytes, unsigned.

---

**gcolvin** (2021-09-28):

> Every JUMP and JUMPI either
>
>
> matches at least one tuple in the vjumptable or the vtraptable, or
> is static

First, as noted above these two cases I think should better be different opcodes.

My desire in this EIP is *not* to introduce new opcodes, but to constrain the existing opcodes so that they are safer (as defined) without breaking too much existing code that is already safe.

> Then, for the tabulated jump, I think validation should check:
>
>
> each jumpsrc and jumpdest in both tables points to an instruction (is within > code bounds and doesn’t point to immediate)
> potentially we could restrict jumpdest to point to JUMPDEST opcode for consistency. Not sure it’s worth it, but it probably will simplify breaking into blocks?
> jumpsrc could alse be additionally restricted to point to a tabulated jump instruction
> each tabulated jump instruction always has exactly one item in vtraptable with corresponding jumpsrc.
> number of items in vjumptable for each jumpsrc is not contstained (can be 0)

I think I just didn’t get around to validating the jump tables themselves, thanks for noticing.  I think that will still require some version of jumpdest analysis be done.

JUMPDEST does makes it easier to break code into basic blocks with a simple one-pass algorithm.  My intent is that every JUMP* instruction has at least one entry in the jumptable.  And yes, there needs to be exactly one vtraptable destination for each JUMP*, and at most one vjumptable destination for every JUMP*.

> Your algorithm code doesn’t seem to check all potential destinations of tabulated jumps, did you intend to support switch-like control flow with this at all?

Yes.  Switches, virtual functions, and function pointers should all be handled via this mechanism.

Brooke and I are working on the algorithm, will be sure we get this right, thanks.

---

**gumb0** (2021-11-10):

Just an observation for myself to not forget, what “constant stack depth rule” would imply.

I don’t know if this would be a concern, but it does change what is possible to do in EVM.

So this kind of code will be forbidden with it:

```auto
for (i = 0; i < 3; ++i)
  push(x);
for (i = 0; i < 3; ++i)
  pop()
```

and

```auto
if (flag)
{
  push(x)
  push(y)
}
else
  push(z)
...
if (flag)
{
  pop()
  pop()
}
else
  pop()
```

---

**gcolvin** (2021-11-11):

Yes, those would be forbidden.  That is the price of detecting underflows.  It’s possible to generate use cases for this – like subroutines that take or return variable numbers of arguments – but those can be handled in memory as well. I’m pretty sure the JVM and Wasm have this restriction as well.

---

**gumb0** (2022-02-04):

I’m trying to understand the algorithm again, and here’s my current confusion: data stack contains some valid values from PUSH and some INVALID from other instructions, which are supposed to not matter.

When we get to `case JUMP` branch it gets jumpdest from the stack, and then it might be INVALID .

I guess your intention is to guarantee that all destinations of dynamic jumps come from previous PUSHes, but this is never checked by an algorithm.

(Also I think `case JUMP` is missing `pc = jumpdest`)

---

**gumb0** (2022-02-04):

Ah well I guess `valid_jumpdest(jumpdest)` is supposed to return false for `INVALID`, this makes sense now, I didn’t get this intention at first.

---

**gumb0** (2022-02-04):

Another question: say we want to pass arguments to a subroutine, so we push them and then execute `RJUMPSUB`. If called subroutine tries to access these arguments, wouldn’t algorithm consider this an underflow?

(I think maybe it would because `RJUMPSUB` does `bp = sp`, and then any pop will move `sp` below `bp` and this is checked for each instruction)

Actually this applies not only to subroutines, but to conditional jumps, too. I’m confused whether such code would be valid at all:

```auto
push(1)
if (flag)
  pop()
else
  pop()
```

---

**gumb0** (2022-02-04):

Also confused about what is `used_items`. Is it maximum stack height for entire path? (this is what comment says about return value of `validate_path`).

If this is its meaning, shouldn’t it do for each instruction `used_items = max(used_items, used_items + added_items(pc) - removed_items(pc)` ? Also then `sp += used_items` doesn’t look correct for each instruction, it would add max to `sp` on each iteration…

---

**gcolvin** (2022-02-04):

Thanks for looking at this in detail, Andrei, [@gumb0](/u/gumb0).  Rather than try to answer here and now I’ll go back to the code and fix any mistakes first.  The problems you point out look like bugs in the validator, rather than conditions that can’t actually be validated.  The algorithm is subtle, and I’ll try to explain it better as I go.

If we decided to just deprecate JUMP it would be a simpler proposal and algorithm.

---

**gumb0** (2022-02-04):

See also I fixed some minor typos in https://github.com/ethereum/EIPs/pull/4769

---

**gcolvin** (2022-02-04):

[@gumb0](/u/gumb0) I’ve merged your changes and the changes I had in progress, and I think we have the algorithm close to correct, thanks.  At your leisure, you can take a look if you want. (And I suppose that at some point the code should be ported to Python.)

