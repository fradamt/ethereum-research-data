---
source: magicians
topic_id: 3218
title: EVM evolution Working Group Formation
author: AlexeyAkhunov
date: "2019-04-29"
category: Working Groups > Ethereum 1.x Ring
tags: [evm, eth1x, evm-evolution]
url: https://ethereum-magicians.org/t/evm-evolution-working-group-formation/3218
views: 2675
likes: 10
posts_count: 11
---

# EVM evolution Working Group Formation

Some relevant discussion has been happening [here](https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm/2728).

There is also recent presentation by [@expede](/u/expede): https://www.youtube.com/watch?v=qck2KBqT14o at Eth1x gathering in Berlin.

This post is to formally acknowledge the de-facto existence of the EVM evolution Working Group, led by [@expede](/u/expede). The Working Group will be performing necessary steps (research, proof of concept implementation, generation of conformance tests, etc.) to enable further improvement in the EVM. Once the group is formed and funded (at least short term), we should expect to hear more of what their current plan is, given other simultaneous developments in Ethereum 1x (State Rent, semi-stateless clients, eWASM), and given their time/money constraints.

## Replies

**boris** (2019-04-29):

Thanks Alexey.

Brooke’s EVM Evolution presentation from Core Devs is on YouTube here:

Slides are here:

https://drive.google.com/open?id=1_taRpfsEF-ofF0UpwKyGOH-ogPqxmpUD

And we’ve got more on plans and progress on our site here: https://fission.codes/evm-evolution/

Leave a comment if you’d like to get involved with the working group!

---

**gcolvin** (2021-04-01):

Thanks [@AlexeyAkhunov](/u/alexeyakhunov).  I’m waking up this group because, as [@vbuterin](/u/vbuterin) put it, the merge is a sort of last chance to get the EVM tidied up for the future.  At this point we have a fair number of related proposals going, including at least the following.  I think they all deserve discussion and refinement into a coherent whole, and propose this group as a good place to pull these discussions together.

- EVM encapsulation format
- EVM384
- List of EVM features potentially worth removing
- EIP-3337: Frame pointer support for memory load and store operations
- EIP-3336: Paged memory allocation for the EVM
- EIP-2930: Optional access lists
- EIP-2327: BEGINDATA
- EIP-2315: Simple Subroutines for the EVM
- EIP-1153: Transient storage opcodes
- EIP-1051: Overflow checking for the EVM
- EIP-663: Unlimited SWAP and DUP instructions
- EIP-616: SIMD Operations for the EVM
- EIP-615: Subroutines and Static Jumps for the EVM

The authors include at least [@Arachnid](/u/arachnid), [@axic](/u/axic), [@cdetrio](/u/cdetrio), [@chfast](/u/chfast), [@chriseth](/u/chriseth), [@holiman](/u/holiman), [@MrChico](/u/mrchico), [@poemm](/u/poemm), and jwasinger

---

**AlexeyAkhunov** (2021-04-02):

To create some “coopetition”, here is what I would like to try: [TEVM Transpiled EVM: accelerate EVM improvement R&D, but learning from eWASM · ledgerwatch/turbo-geth Wiki · GitHub](https://github.com/ledgerwatch/turbo-geth/wiki/TEVM---Transpiled-EVM:-accelerate-EVM-improvement-R&D,-but-learning-from-eWASM)

---

**gcolvin** (2021-04-02):

Yes, “coopetition” is a good word for it, as what you lay out is an implementation strategy for an EVM that could be surfaced for general use later, independently of other work.  I’ll await a better understanding of your ideas before digging in very much, but it does sound a lot like eWasm.

I think there has been enough work on the proposals I listed over the years that we can probably come to agree (or agree that we can’t agree) on a reasonable subset of features for an initial upgrade.  (Including features that might make TEVM’s life easier.)

---

**AlexeyAkhunov** (2021-04-03):

As a first case study for TEVM, I am planning to add EIP-615 (in its entirety) to TEVM ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9) and try to use our abstract interpretation analyser to transpile EVM byte codes to it. Even if for already deployed contract and even if semi-manually to start with.

---

**gcolvin** (2021-04-04):

That would be gratifying, but still not where I’d start - EVM-615 is restricted in ways that make it a difficult target for the EVM.  I think I’d start with looking at eWasm and EVMC, which attempt to separate out purely computational concerns from the rest, which is part of what you seem to want.  But we should talk about it next week.

And I wonder what you mean by unrolling storage ops.

---

**AlexeyAkhunov** (2021-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> And I wonder what you mean by unrolling storage ops.

Good question! I have added a new Case study section about this into the doc (only initial ideas, but I hope it will make things clearer). I have also added the case study about structured control flow, and an extra feature of non-deterministic instructions with hints. Hope you’ll enjoy the read: [TEVM Transpiled EVM: accelerate EVM improvement R&D, but learning from eWASM · ledgerwatch/erigon Wiki · GitHub](https://github.com/ledgerwatch/turbo-geth/wiki/TEVM---Transpiled-EVM:-accelerate-EVM-improvement-R&D,-but-learning-from-eWASM)

---

**gcolvin** (2021-04-07):

> Transpilation of EVM into Web Assembly (for performance reasons) was the idea behind starting eWASM (ethereum Web Assembly) project. Lessons need to be learnt from this. For example, are these statements true?:
>
>
> One EVM instruction gets translated into many Web Assembly instructions, thus creating additional overhead.
> Executing many Web Assembly instructions takes longer than executing a corresponding single EVM instruction. Having higher-level instruction may be inconvenient (as referred later), but it does have a benefit of amortising the cost of the interpreter loop.
> Web Assembly code is harder to meter efficiently than EVM bytecode, again due to the finer granularity of operations. Because of this finer granularity, the relative overhead of metering for Web Assembly code can be much higher than for EVM bytecode.
> Problems above are not unsolveable

All true, but not show-stoppers.  The big EVM operations are mostly calls to native crypto and big-int libraries, which can have their gas counted as a unit.  So the EVM isn’t necessarily better that way.  The NEAR folks are doing well with Wasm.

---

**gcolvin** (2021-04-07):

I don’t  understand, but unrolling storage ops sounds like a good idea.  How would it compare to just having EIP-1153?

I’m still unconvinced that EIP-615 is a very good target for EVM code – it’s being so much more constrained than the EVM would mean that optimized EVM code would need to be de-optimized.  There is probably a better design for the purpose – less dynamic than EIP-2315, and less restricted than EIP-615.

And I remain fairly unconvinced that transpiling arithmetic operations is a good strategy anyway.  It’s not uncommon for interpreters to translate their input into a different form for better performance, some not looking much like byte-code, or even being easy to serialize.

What makes sense to me as a starting point is separating out the purely computational parts of the EVM – the VM proper – then looking at what remains – like state access and message calls and where they fit.  Wasm and eWasm have done a fair amount of work on this.

---

**AlexeyAkhunov** (2021-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I don’t understand, but unrolling storage ops sounds like a good idea. How would it compare to just having EIP-1153?

As we established, I think, presenting a new resource (transitive storage, subroutine) without also presenting lots of usecases for it (not theoretical, but practical), seems to greatly reduce the changes of the new resource being adopted in EVM in the “head on” way. That is why I would like to introduce these resources in a “roundabout” way to go deeper and start using them before “Ethereum governance” approves of them and “community” starts caring about these things ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) From my point of view, this is the only way. As I mentioned before, “trading EIPs for years of my life is not a good trade”. I want to make stuff that works, and show people how it works.

> And I remain fairly unconvinced that transpiling arithmetic operations is a good strategy anyway

That is where the difference between eWASM and TEVM is. As far as I understand, eWASM idea was to transpile 256-bit operations into 64-bit operations, and with TEVM we won’t, and we will also go the other way, introducing 384-bit operations, and perhaps even longer words.

> Wasm and eWasm have done a fair amount of work on this.

Correct. That is why part of this effort is to study the “history of eWASM”

