---
source: ethresearch
topic_id: 22230
title: Before jumping on the riscv bandwagon
author: gballet
date: "2025-04-28"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/before-jumping-on-the-riscv-bandwagon/22230
views: 697
likes: 12
posts_count: 4
---

# Before jumping on the riscv bandwagon

I have been a long-term riscv enthusiast. I have 4 riscv devices, that I toy with and use some as home servers, some as compilation targets to check that work, and as a testbed for my work on zkvms. I was in the room when [r55](https://github.com/r55-eth/r55) was created, I helped building it, and I came up with the name (I won’t tell you where it comes from, it’s a stupid pun).

**Disclaimer** even though it’s adjacent to the current debate on EOF v. riscv, this is not primarily about this. It’s a honest evaluation of the relevance of investing energy into riscv at this point in time.

In my view, there are a few reasons not to replace the EVM with riscv, let alone in the sort term:

- One thing that is obvious when tinkering, is that the riscv ecosystem isn’t production-ready: linkers are deadly slow, library support is drearily wanting so very few things compile, and there is no network effect since very few projects even bother building riscv releases.
- There isn’t only one riscv, there’s many flavors. There’s the choice between 32 bytes and 64 bytes. There are extensions to the instruction set architecture (ISA) to support memory management, floating points, etc… The modularity is great, but all these extensions can be confusing. Compilers typically support only one or two targets, and more often than not, it’s not the one that is needed. For example, go only compiles to riscv64gc but most zkvms target riscv32imc. We could easily spend a year trying to decide which extensions we want.
- The riscv hardware itself is still very, very slow: it’s much faster to emulate the evm on a fast amd64 processor than run native code on a riscv processor[*]
- I hear some zkvms are moving away from riscv and either using WASM (e.g. powdr) or developing their own ISA. From what I gather, riscv isn’t that zk-friendly either. It’s definitely better than EVM because the word size is smaller, but it’s possible to do much better. If zkvms are the endgame, enshrining riscv now is probably a bad idea.

**TLDR** I don’t think it’s a good idea to rush into making such a big change at this moment.

I do love riscv and I want a riscv-enabled Ethereum. I believe the better route, would be that of an execution engine. My opinion is that riscv should come as part of the native rollup roadmap, as a secondary execution engine, rather than a replacement for the EVM. This would make the transition smoother, as the engine could be maintained independently.

[*] I’m aware that there exist some Chinese boards that have much better performance, but they’re currently unavailable for purchase, and the listed price is bonkers.

## Replies

**0xbryer** (2025-04-28):

Thanks for the thoughtful post - I strongly agree with the idea that zkVMs should prioritize proving efficiency over hardware compatibility.

While RISC-V offers a familiar and standardized ISA, zkVMs aren’t constrained by real-world execution, and their main bottleneck is proof size and generation time. Designing a minimal, ZK-optimized instruction set - even if it’s “nonstandard” - seems like the right path for truly scalable and efficient ZK rollups and applications.

In fact, a “ZK-first ISA” could open doors to custom circuits that dramatically outperform any adapted general-purpose architecture. Maybe the real opportunity here isn’t to pick a standard like RISC-V, but to invent something even better, designed from first principles with ZK needs in mind.

Curious to hear if you (or others) have ideas about what *features* an ideal zkVM ISA would include!

---

**g11in** (2025-04-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/gballet/48/4230_2.png) gballet:

> riscv should come as part of the native rollup roadmap, as a secondary execution engine, rather than a replacement for the EVM

this is definitely a better strategy for enshrinement. we should go for as much composability we can get out there.

---

**codygunton** (2025-05-15):

Thanks for raising all of these points. I think issues around zk friendliness have a higher profile, so I want to echo especially the first two points and add a particular piece of data. In recent work relating to RISC-V compliance testing and fuzzing, I ran into ttps://github.com/riscv-software-src/riscv-tests/issues/368 (sorry, I can’t post links yet). In brief, since at least January 2022, if you have implemented the current version of the base instruction set (or, say, RV32IM, which some of the zkVMs use), then these canonical RISC-V tests crash your implementation. This is because some macros used to set up the tests make use of instructions that have been removed from the base instruction set.

Like [@gballet](/u/gballet), I feel that RISC-V is an awesome project worth supporting. I’m just raising the point that a flexible standard and lots of existing tools does not necessarily mean easy bootstrapping to meet our needs.

Let me also explicitly say that I this issue is, to me, separate from whether we can deploy L2 scaling in the short and medium term via RISC-V based VMs. Of course there could be some synergy there, but IMO that synergy would come too far down the road to consider now, given the pace of development of zk and the more immediate need to scale.

