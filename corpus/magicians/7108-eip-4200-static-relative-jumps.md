---
source: magicians
topic_id: 7108
title: "EIP-4200: Static relative jumps"
author: axic
date: "2021-09-22"
category: EIPs > EIPs core
tags: [evm, opcodes, shanghai-candidate, evm-object-format]
url: https://ethereum-magicians.org/t/eip-4200-static-relative-jumps/7108
views: 5439
likes: 9
posts_count: 38
---

# EIP-4200: Static relative jumps

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4200)





###



RJUMP and RJUMPI instructions with a signed immediate encoding the jump destination










This proposal started [as a comment](https://github.com/ethereum/pm/issues/250#issuecomment-782094832) back in February and was one of the reasons which kicked off our journey with [EVM Object Format (EOF)](https://ethereum-magicians.org/t/evm-object-format-eof/5727). In the past few months [@gumb0](/u/gumb0) has been working on experimenting and validating this in evmone ([PR here](https://github.com/ethereum/evmone/pull/351)), but now is the time to release an actual EIP.

## Replies

**chfast** (2021-09-24):

### Benchmarks

We compared performance of “static” `JUMP` instruction with new `RJUMP`.

The benchmark case consist of 4096 instruction groups called “jumppads”. During execution each jumppad is visited exactly once in fixed pseudo-random order.

- For JUMP the jumppad is JUMPDEST PUSH2 JUMP (generator, bytecode)
- For RJUMP the jumpad is just RJUMP (generator, bytecode)

Benchmarks were done on Intel Haswell CPU 4.4 GHz with [evmone/Baseline](https://github.com/ethereum/evmone) [0.8.2](https://github.com/ethereum/evmone/releases/tag/v0.8.2).

| Instruction | CPU time [µs] | Burn rate [Ggas/s] |
| --- | --- | --- |
| JUMP | 28.1 | 1.75 |
| RJUMP | 12.0 | 1.70 (cost 5), 0.99 (cost 3) |

Conservative gas cost selection for `RJUMP` is 5 to match the current performance of `JUMP` in “static” context.

However, the `JUMP` seems to be significantly overpriced as the program heavily using it runs at 1.75 Ggas/s gas burn rate. Selecting `RJUMP` cost of 3 would still be acceptable because the performance of 1 Ggas/s is still excellent.

---

**gcolvin** (2021-09-30):

I very much support this proposal, having been wanting static jumps for a long time.  It will also let me pull these jumps out of EIP-2315, including this EIP by reference.

My only worry is that it may be too soon to be removing JUMPDEST.  The pros are clear - more speed, less space, saved gas.  The cons are, as you say, that JUMPDEST serves some purposes.

EVM code can be parsed into basic blocks in one pass – because JUMPDESTs (and other control-flow instructions) delimit basic blocks.  Otherwise a preliminary pass is needed to find the destinations (such as jumpdest analysis).  Tools can take advantage of this, including disassemblers, compilers, and interpreters.  And human writers and readers.

Whether the pros outweigh the cons in the end isn’t clear to me, but getting more experience with these operations and getting feedback from toolmakers and others seems worth the wait.

---

**axic** (2021-11-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> My only worry is that it may be too soon to be removing JUMPDEST. The pros are clear - more speed, less space, saved gas. The cons are, as you say, that JUMPDEST serves some purposes.

The requirement to have `JUMPDEST` is only lifted for the static jumps. The dynamic jump opcodes are unaffected.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> EVM code can be parsed into basic blocks in one pass – because JUMPDESTs (and other control-flow instructions) delimit basic blocks. Otherwise a preliminary pass is needed to find the destinations (such as jumpdest analysis). Tools can take advantage of this, including disassemblers, compilers, and interpreters. And human writers and readers.

Analysers can be changed to also parse the destinations of static jumps to build up the blocks.  This can be done in the usual “jumpdest analysis” loop.

---

**gcolvin** (2021-11-07):

Yes, they can, but I think it does take an extra pass and extra memory to store the destinations, even if there are no JUMP*s in the code.    I’m not hard over on this, just uncertain.

---

**axic** (2021-11-08):

Why would it take an extra pass?

The only difference to finding `JUMPDEST` is that with `RJUMP` you get an offset for a different location, but one can still use a bitmap or build code blocks out of it.

Here’s some dumb version:

```python
for ([pos, instruction]: bytecode):
  if (instruction.is_push()):
    # parse pushdata
  else if (instruction.is_jumpdest()):
    jumpdest.insert(pos)
  else if (instruction.is_rjump()):
    # parse_rjump_offset reads the following 2 bytes as a big endian two's complement number
    relative_jumpdest.insert(parse_rjump_offset(next(), next())
```

---

**axic** (2021-11-08):

[@gumb0](/u/gumb0) reminds me that it may be a bit more complex to sum gas costs for a block in a single pass with backwards jumps.

---

**gcolvin** (2021-11-08):

I’m thinking of one pass tools that don’t otherwise need to do a jumpdest analysis, but instead just scan the code directly, byte by byte.

An example would be a simple disassembler that puts labels on jump destinations, decodes immediate data, and perhaps calculates fixed gas costs and stack use for each block.  With JUMPDEST that can be done in one sequential pass of the bytecode.  Without JUMPDEST it takes one pass to find the jump destinations and store the results of that pass. Then it takes a second pass to label and process the blocks, using the stored results instead of the JUMPDEST byte codes.

It might possible to combine the two passes, but however it’s done I think any one-pass tool that counts on there being JUMPDESTs would become more complex, use more memory, and be slower.  At this point the EVM is used on enough chains and there are enough tools that I cannot say how much impact this would have.  But I’m bumping into it already writing code to validate the safe use of these instructions.

---

**axic** (2021-11-09):

I think complexity considerations of off-chain tools should not influence on-chain decisions that much. We are optimising for state size and on-chain execution costs, as opposed to off-chain use cases.

---

**gcolvin** (2021-11-09):

I think we should have some concern for off-chain tools.   Not the strongest concern by far, but I don’t want to leave it unaddressed.  It’s a good thing that EVM code is easy to write tools for.   I think in essence it comes down to how much of that simplicity are we willing to give up for however much state size and performance gains we get.

This could also affect our *initcode* phase in the same ways.  @gumbo mentioned summing gas costs.  And I mentioned that I’m still working out how to change my validation algorithm to not need JUMPDEST.  Without it every instruction is a potential jump destination, so my current algorithm would need to check the *jumpdest* bitmap for each instruction it traverses to find out.  For presentation purposes that’s OK, but for production maybe not. I’m not yet clear on how to do better.

It’s this stuff that has me wondering whether we should first make it possible to remove JUMPDEST, then finally remove it in a later EOF version.  On the other hand, since none of this is going into the EVM until after the Merge we have plenty of time to work this out.

---

**gcolvin** (2021-11-13):

I’m finding that the lack of JUMPDEST really does make validating safety a little harder. To avoid checking whether every instruction is a jump destination as I traverse the byte code I think I’d need to make an extra pass of the byte code to explicitly create the control flow graph and then traverse the graph.

That graph might actually be a good representation for some interpreters – it would make it easier to do gas and stack checking at the start of each block.  But that checking would mean that JUMPDEST actually costs something.

---

**gcolvin** (2021-12-17):

In the end this wasn’t too hard because it turned out I could traverse the CFG without actually constructing it.  So I still worry a bit, but not enough to object.  I’ve changed EIP-2315 to not need JUMPDEST either.

---

**MicahZoltu** (2022-01-25):

I have a weak request to rename `RJUMP` and friends to something more descriptive like `RELATIVE_JUMP` or `RELATIVEJUMP` if we want to keep consistency of “all caps one word opcodes”.  I don’t think we gain anything significant by having the opcode words be exceedingly short (to the point of non-descriptiveness).

---

**MicahZoltu** (2022-01-25):

> Note: EIP-3670 should reject PC.

This feels like it should be an EIP (that depends on this one).

---

**MicahZoltu** (2022-01-25):

Can we remove the dynamic jumps entirely as part of this EIP (in `EOF1` contracts)?  Is there a sufficiently compelling reason to keep them?  Maybe to limit risk, we could create a separate EIP that depends on this one which removes the dynamic JUMP instructions?

---

**axic** (2022-01-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Note: EIP-3670 should reject PC.

This feels like it should be an EIP (that depends on this one).

Once we get closer to aggreement on getting these EIPs adopted together, we’ll just change 3670 to depend on 4200 and mark `PC` as invalid.

---

**axic** (2022-01-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I have a weak request to rename RJUMP and friends to something more descriptive like RELATIVE_JUMP or RELATIVEJUMP if we want to keep consistency of “all caps one word opcodes”. I don’t think we gain anything significant by having the opcode words be exceedingly short (to the point of non-descriptiveness).

I have a weak preference for the short name and a strong preference not having underscores. I find `RELATIVEJUMP` quiet long, but could compromise on `RELJUMP`? Think also about the `EXT*` prefixes.

The more interesting question is whether we should keep the `I` suffix for “IF” following `JUMPI` or go with `RJUMPIF`.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Can we remove the dynamic jumps entirely as part of this EIP (in EOF1 contracts)? Is there a sufficiently compelling reason to keep them? Maybe to limit risk, we could create a separate EIP that depends on this one which removes the dynamic JUMP instructions?

Unfortunately they cannot be deprecated as of yet. We plan to release a new EIP proposing function sections, which would be a way to get rid of them.

---

**MicahZoltu** (2022-01-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> I have a weak preference for the short name and a strong preference not having underscores. I find RELATIVEJUMP quiet long, but could compromise on RELJUMP? Think also about the EXT* prefixes.
>
>
> The more interesting question is whether we should keep the I suffix for “IF” following JUMPI or go with RJUMPIF.

Compromising on “no underscores”, this is my preference:

`CONDITIONALRELATIVEJUMP > RELATIVEJUMPIF > RELJUMPIF > RELJUMPI > RJUMPI`

---

**chfast** (2022-01-25):

# Why there is no RJUMPV

The [EIP-615](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-615.md#specification) proposes new jump instruction [JUMPV](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-615.md#specification) which looks up the jump destination in the adjusted array using the index value taken from the stack. For good reason similar control-flow instructions exist in most if not all IRs.

However, I have not found any common use-case in contracts development justifying relatively high complexity of the instruction (e.g. encoding of the array in bytecode, handling invalid index values). Furthermore, nothing prevents adding such instruction in future if it turns out to be needed.

Such instruction can help with implementing [switch statements](https://en.wikipedia.org/wiki/Switch_statement), but only if *case* constants are continuous or at least dense.

The most used “switch” in every solidity contract is the external function dispatch. But `JUMPV` will not help here as the *functions ids* are “hashed” values (sparse). You would first need to the index of a function id but then you don’t need `JUMPV` any more as a static jump will do.

I also wanted search solidity source codes on GitHub to check for interesting usages of `switch`. Just to realize solidity does not support `switch` statement at all.

The proposed `JUMPV` indeed matches the semantics of [br_table](https://webassembly.github.io/spec/core/exec/instructions.html#xref-syntax-instructions-syntax-instr-control-mathsf-br-table-l-ast-l-n) from WebAssembly. However, the LLVM IR has extended variant of such control flow instruction called [switch](https://llvm.org/docs/LangRef.html#switch-instruction). There instead of a table of indexes we have “an array of pairs of comparison value constants and [jump destinations]”. This would handle function dispatch use-case, but it complicates the instruction even more.

If I’m mistaken and there are valid use-cases for `JUMPV` please let me know.

---

**gcolvin** (2022-01-25):

I’d be happy enough to deprecate them.  But also happy enough to restrict them at validation time to safe uses.  [EIP-3779: Safer Control Flow for the EVM](https://eips.ethereum.org/EIPS/eip-3779).

---

**gcolvin** (2022-01-31):

I’d actually prefer JUMPR and JUMPRI.  I’d especially like for all of the JUMP opcodes to sort together (e.g. they are often referred to as a group with JUMP*) and for the names to be concise.  JUMPREL and JUMPRELIF would be OK, but a lot to type.


*(17 more replies not shown)*
