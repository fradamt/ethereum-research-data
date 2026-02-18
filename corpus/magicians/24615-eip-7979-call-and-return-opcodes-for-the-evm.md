---
source: magicians
topic_id: 24615
title: "EIP-7979: Call and Return Opcodes for the EVM"
author: gcolvin
date: "2025-06-20"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7979-call-and-return-opcodes-for-the-evm/24615
views: 369
likes: 7
posts_count: 9
---

# EIP-7979: Call and Return Opcodes for the EVM

[EIP-7979: Call and Return Opcodes for the EVM](https://eips.ethereum.org/EIPS/eip-7979)

This is the smallest possible change to the EVM to support calls and returns.

This proposal introduces three new control-flow instructions to the EVM:

- CALLSUB  transfers control to the destination on top of the stack…
- ENTERSUB  marks a CALLSUB destination.
- RETURNSUB  returns to the PC after the most recent CALLSUB.

Code can also be prefixed with `MAGIC` bytes.  The complete control flow of `MAGIC` code can be traversed in time and space linear in the size of the code, enabling better tools for validation, static analysis, and JIT and AOT compilers.  On-chain, `MAGIC` code is validated at CREATE time to ensure that it will not execute invalid instructions, jump to invalid locations, underflow stack, or, in the absence of recursion, overflow stack.

These changes are backwards-compatible: the new instructions behave as specified whether or not they appear in `MAGIC` code.

## Replies

**RubyEDE** (2025-07-23):

This EIP is great! Puts an important part which EVM is missing that can have immediate benefits, reducing gas costs with backwards compatibility. This is awesome.

---

**gcolvin** (2025-07-24):

The main question right now (and the reason it’s still a draft PR) is whether we need an ENTERSUB code.  You can find them all in one pass by marking the destinations of JUMPSUB, but that’s the hard way.

---

**RubyEDE** (2025-07-27):

ENTERSUB means a little bit more development time, but it’s a worthwhile addition. It won’t add any new runtime behaviour, it just makes the structure explicit.

Bottom line, it’s a minimal addition with a lot of benefit.

---

**gcolvin** (2025-07-27):

Yes – it  amounts to a form of JUMPDEST.  It’s also not clear that a validation algorithm can be made to work efficiently without it.  Unfortunately Max – the compiler expert who was working with me on that algorithm – died a few weeks ago.

---

**RubyEDE** (2025-07-27):

Damn that’s terrible news, I’m sorry to hear about Max.

ENTERSUB makes even more sense now, if the validation algorithm becomes harder with it, then its an almsot obvious decision.

I’m not a compiler expert but I’d like to help however I can. Let me know if there’s a way I can move this forward.

---

**gcolvin** (2025-07-27):

Thanks.

What some people seem not to understand (and I don’t blame them) is the basics of control flow graphs, why they can be an essential tool for static analysis, how to extract them from machine code, why dynamic jumps can make extracting them go quadratic, and why – unlike most applications – we need to extract them in linear time.  And of course – given that static analysis is anything you can do to code without actually executing it – how many important things are forms of static analysis, including symbolic execution, translating EVM stack code to register code for faster interpretation and compiling to machine code, proofs of EVM code correctness and more.  There is an entire academic literature devoted to working around the problems caused by dynamic jumps.

All this amounts to two or three university courses, some of which I never took –  I finished school in 1982 and learned most of what I do know on the job.  So I’m not the best person to explain all of this, let alone briefly enough to fit in an EIP.

---

**RubyEDE** (2025-07-28):

Honsetly this gave me a much clearer view of what it can do. I didn’t study control flow graphs formally either, but the way you framed it makes a good case for structured control flow and ENTERSUB.

I’d love to help maybe I can write a short draft that explains the CFG/static analysis angle in layman’s terms as supporting context for people(like me haha) so it’s easier to understand. Let me know if that’s useful happy to contribute however I can

---

**jdetychey** (2025-08-07):

I support this EIP, as Ruby puts it, minimal addition with a lof of benefits!=.

