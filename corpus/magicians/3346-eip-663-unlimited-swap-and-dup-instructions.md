---
source: magicians
topic_id: 3346
title: "EIP-663: Unlimited SWAP and DUP instructions"
author: axic
date: "2019-06-02"
category: EIPs > EIPs core
tags: [evm, opcodes, shanghai-candidate, cancun-candidate]
url: https://ethereum-magicians.org/t/eip-663-unlimited-swap-and-dup-instructions/3346
views: 8900
likes: 22
posts_count: 56
---

# EIP-663: Unlimited SWAP and DUP instructions

Discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-663)





###



Introduce SWAPN and DUPN which take an immediate value for the depth

## Replies

**charles-cooper** (2019-06-20):

[@axic](/u/axic) Where does the 1024 item limit come from? This seems out of line with the semantics of the current DUP* instructions. Also, is there currently any consensus on which of the three options to go with?

---

**axic** (2019-06-21):

It is the core design of EVM, see the Yellow Paper page 11:

> The EVM is a simple stack-based architec-ture.  The word size of the machine (and thus size of stackitems) is 256-bit.  This was chosen to facilitate the Keccak-256  hash  scheme  and  elliptic-curve  computations.   Thememory model is a simple word-addressed byte array.  Thestack has a maximum size of 1024.

---

**charles-cooper** (2019-06-21):

Thanks, I see it now in the exceptional halting conditions too:

> This states that the execution is in an exceptional halt-ing state if there is insufficient gas, if the instruction is invalid (and therefore its δ subscript is undefined), if there are insufficient stack items, if a destination is invalid, the new stack size would be larger than 1024 or state modification is attempted during a static call.

---

**chfast** (2019-07-10):

> If the current stack depth is at the limit, a stack overflow exception is issued.

SWAP instructions do not increase the stack height so this sentence do not apply.

It is not true for Option A where an additional argument is popped from the stack (so SWAP decreases stack and DUP keeps it the same height).

---

**gcolvin** (2019-07-11):

I prefer the immediate argument form, as I think in most all cases the swap or dup offset will be constant.  Variable offsets might help if you want to treat the stack more like an array in memory, but we have memory for that.

---

**chfast** (2019-07-15):

It must be specified if we count stack items from 0 or 1. I.e. is the top stack item an item at depth 0 or 1?

---

**chfast** (2019-07-15):

Currently, the spec for `SWAPn` is incorrect.

> the top stack item is swapped with the item at depth n

For `n` referring the stack top item the instruction will swap the top item with itself.

---

**chfast** (2019-07-15):

Following the current convention, instructions should be named all uppercase.

---

**chriseth** (2019-08-01):

Not sure if this has been discussed, but I wanted to make the general remark about backwards-compatibility of introducing multi-byte opcodes. Introducing new multi-byte opcodes will influence jumpdest analysis and thus can have effects on all code following the point where the new multi-byte opcode is used in old code, not only the point itself:

If the argument to a newly-introduced multi-byte opcode is the byte value of JUMPDEST, then this was a valid jump destination before the hard fork, but it is no longer a valid jump destination after the hard fork.

Even worse, if the argument is a push opcode, the push data will be interpreted as code, while it was push data before. In the worst case, this might cascade all the way to the end of the code if some push data is the byte-value of jumpdest or of the newly introduced multi-byte opcode.

Because of that, I would advise to use account versioning for any change that introduces new multi-byte opcodes.

---

**gumb0** (2019-08-01):

^ Here’s simple test demonstating this problem

https://github.com/ethereum/evmone/pull/113/commits/5e94400b6076e6c4fe701d5a6695731c2bfeab11

Bytecode there is

`600456b35b600060005260206000f3`

---

**chfast** (2019-08-01):

Using account versioning to introduce it would be overkill unless versioning is used anyway (required by any other EVM change).

For me, using variant A is no-go. Requiring “static” push before `DUPN`/`SWAPN` introduces new kind of error - invalid code. Dynamic argument on the stack for an instruction manipulating the stack looks pretty weird. Not mentioning double the cost.

I believe, the only option to proceed is to scan all deployed contracts for the opcodes pattern that would cause troubles.

---

**karalabe** (2019-08-07):

Multi-byte opcodes will node make it into Istanbul. Those would break one of the most basic invariants of EVM implementations, so that’s not something we can ship in the 12th hour.

I generally don’t like the idea of account versioning, because it explodes the possible issues, so unless there’s an extremely good reason to do it, I don’t see that going in. This EIP is most definitely not worth versioned accounts (IMHO).

[@chfast](/u/chfast) Why does a static push introduce a possibility for invalid code?

---

**chfast** (2019-08-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> Multi-byte opcodes will node make it into Istanbul. Those would break one of the most basic invariants of EVM implementations, so that’s not something we can ship in the 12th hour.

I don’t want to rush this EIP. Personally, I’m not even interested in shipping this at all, but because solidity team expressed that this might be helpful to solidity and other languages and I touched it at some point I want to agree on the spec. Only if we have a spec (single variant) we can discuss when to ship it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> @chfast Why does a static push introduce a possibility for invalid code?

**Option A** requires a PUSH directly preceding SWAPN/DUPN instructions. In case there is no PUSH before we have to report a new kind of exception like “malformed instruction” (but still unrecognizable from OOG by contracts) . I expect, following current EVM behavior in other places, the exception should happen when the instruction is reached, *not* when to code is analyzed  before execution.

After writing the explanation, it might not be so bad as I thought previously and very different what we currently have in EVM.

---

**gumb0** (2019-08-08):

> Option A  requires a PUSH directly preceding SWAPN/DUPN instructions.

It doesn’t strictly require it, it just gets the top item from the stack (with the possibility of regular stack underflow error)

I guess what you mean is that this option makes it impossible to figure out during the pre-execution analysis the stack depth required for the opcode?

---

**chfast** (2019-08-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gumb0/48/12_2.png) gumb0:

> It doesn’t strictly require it, it just gets the top item from the stack (with the possibility of regular stack underflow error)

This is exactly an option within Option A I’d like to avoid.

---

**ekpyron** (2019-08-08):

I mean the JUMPDEST problem could be avoided by defining the new opcodes specially, s.t. they are only valid, if they are directly preceded by a PUSH2, so the new opcodes would in fact be the compounds 0x61 [two bytes of static stack depth] 0xb0 and 0x61 [two bytes of static stack depth] 0xb1 - that shouldn’t cause any issues, right?

But that’s quite hacky and that’s how I understood [@chfast](/u/chfast)’s comments.

---

**chfast** (2019-08-08):

Yes, that’s good understanding. As far as Option A is concerned, I’d like to require the PUSH1 or PUSH2 to directly proceed the DUPN/SWAPN instruction.

In other words, **the operand value of DUPN/SWAPN should be known during EVM program loading / bytecode analysis** (whatever we call this phase of execution).

*Why this is important?*

The most effective EVM optimization is calculating gas (for most of the instructions) and checking stack requirements once per block of instructions. If the operand is “dynamic” the stack requirements are also “dynamic” and this optimization cannot be applied to DUPN/SWAPN making them much more expensive to execute.

---

**ekpyron** (2019-08-08):

Just to confirm that: for the use in solidity (i.e. alleviating the limit on the number of “live” local variables), dynamic access to the stack is not required, so [@chfast](/u/chfast)’s variant of “Option A made static” would be sufficient for that.

---

**axic** (2019-08-11):

One version of the EIP proposed this version: https://github.com/ethereum/EIPs/pull/663#issuecomment-312950394

I’m not even sure why “Option A” ended up with this terrible wording, but it was supposed to be what you guys interpreted. It must be preceded by the PUSH opcode.

---

**axic** (2019-08-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> I’m not even sure why “Option A” ended up with this terrible wording, but it was supposed to be what you guys interpreted. It must be preceded by the PUSH opcode.

Pushed this as “Option A+” to the EIP to make discussion clearer: [EIP663: add Option A+ by axic · Pull Request #2235 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2235)

I think we can agree that “Option A” should not be accepted.

Question about “Option A+”: if this option is considered, do we want to introduce a validation stage?


*(35 more replies not shown)*
