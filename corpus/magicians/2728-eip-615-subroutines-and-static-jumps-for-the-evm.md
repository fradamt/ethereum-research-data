---
source: magicians
topic_id: 2728
title: "EIP-615: Subroutines and Static Jumps for the EVM"
author: gcolvin
date: "2019-02-23"
category: EIPs
tags: [evm, eip-615]
url: https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm/2728
views: 10357
likes: 102
posts_count: 152
---

# EIP-615: Subroutines and Static Jumps for the EVM

This proposal is first of all about deprecating dynamic jumps, which play hell with formal specs,  proofs of correctness, static analysis, optimizing compilation, and a lot more.  And being rid of them, introducing subroutines and a few other operations to replace them.  This gives an immediate benefit in formal tractability, and opportunities for increased performance.

[EIP-615: Subroutines and Static Jumps for the EVM](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-615.md)

I’m incorporating changes for later PRs [into the original proposal](https://github.com/ethereum/EIPs/issues/615#issue-224850482).

## Replies

**gcolvin** (2019-02-23):

[@AlexeyAkhunov](/u/alexeyakhunov) [@androlo](/u/androlo) [@Arachnid](/u/arachnid) [@axic](/u/axic) [@boris](/u/boris) [@cdetrio](/u/cdetrio) [@chfast](/u/chfast) @chriseth [@Ethernian](/u/ethernian)

---

**gcolvin** (2019-02-23):

[@expede](/u/expede) [@fubuloubu](/u/fubuloubu) [@fulldecent](/u/fulldecent)  [@grosu](/u/grosu) [@gumb0](/u/gumb0) [@holiman](/u/holiman)  [@karalabe](/u/karalabe) [@lrettig](/u/lrettig) [@mattlock](/u/mattlock) [@tjayrush](/u/tjayrush)

---

**gcolvin** (2019-02-23):

[@vbuterin](/u/vbuterin)

@<others I’m forgetting whose judgment I value, or should>

(you can only mention 10 people in a post)

---

**expede** (2019-02-23):

(Typing from a phone… sorry for short post. Infer detail as needed ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=9))

I would maybe put a bit more nuance on it: this proposal introduces structured control flow, which makes it MUCH easier to analyze smart contracts for correctness, security considerations, and for the EVM to performance optimize (doesn’t matter JIT or AOT), and do gas meter aggregation.

Deprecating dynamic jumps is an excellent step in driving users to more structured flow by default. There are legitimate uses of dynamic jumps, but they’re FAR into the realm of edge cases.

As part of a broader strategy (what [@boris](/u/boris) and I have been calling “EVM Evolution”), this is the first step towards a much safer & faster EVM. Ewasm is still coming, but we should improve the EVM that we have today. This change also makes it easier to port code to wasm when the day comes.

I’ve spoken with a number of mainstream client implementers at Devcon IV and Standford, and these changes sound fairly uncontroversial so far. We would love as much feedback on this proposal as possible ahead of moving this proposal to Last Call!

Thanks everyone ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=9)![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=9)![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=9)

---

**AlexeyAkhunov** (2019-02-23):

Thank you! The reason I am interested in this is potential for more efficient concurrent execution of transaction. Provided that if the Ethereum state keeps growing at least for next couple of years, we have started exploring the ideas of storing parts of the state remotely and fetching them in batches during the execution. I have done some crude modelling [here](https://medium.com/@akhounov/looking-back-at-the-ethereum-1x-workshop-26-28-01-2019-part-4-a69b48e14309), but realised very quickly that static analysis might be used together with symbolic execution to elide locks during such executions. Any concrete hints in that direction?

---

**gcolvin** (2019-02-23):

Thanks [@AlexeyAkhunov](/u/alexeyakhunov).  That’s a difficult read that will take me a cup of coffee here as the sun rises.  Could say more about how symbolic execution would help this scheme?  I suspect [@expede](/u/expede) might even understand you!

---

**fubuloubu** (2019-02-23):

So yes, while it really isn’t possible to get rid of dynamic jumps since they are used so heavily in current EVM programs, I would say most languages could move users over to that if a static jump option were available that was sufficiently cheap (and it should be cheaper than a dynamic jump because of how much more optimizable it would be for program flow, data loading, etc)

Vyper has spoken very positively about this proposal, and as a smaller, security-focused language we would have no problems deprecating the use of dynamic jumps entirely. However, I don’t think that would be possible for a larger, more powerful language that opens up to assembly instructions like Solidity, but it would be good enough if the higher level language were able to make the switch for all internal calls, which certainly seems plausible.

---

**fubuloubu** (2019-02-23):

P.S. is there any chance that subroutines can be considered separately?

---

**gcolvin** (2019-02-23):

A static jump is O(1).  A dynamic jump takes a binary search of a table of every JUMPDEST in the program.  So O(1) vs O(log n) to start with, even before low-level optimizations.

---

**gcolvin** (2019-02-23):

Get rid of dynamic jumps and how to construct subroutines?

---

**fubuloubu** (2019-02-23):

No I mean to put this proposal into stages and reduce implementation risk.

1. Add subroutines
2. Add static jump opcodes
3. Work on community education and reducing the prevalence of dynamic jump usage

---

**fubuloubu** (2019-02-23):

Would also be good to get a survey of dynamic jump usage, I’m not exactly sure how prevalent it is or how many different ways it is used

---

**gcolvin** (2019-02-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> However, I don’t think that [deprecating dynamic jumps’ would be possible for a larger, more powerful language that opens up to assembly instructions like Solidity.

Deprecating just means that validation will reject Solidity programs that attempt to meet the new standard.  Whether a means for new code to bypass validation is maintained indefinitely will get determined after the 1st phase of optional validation.

---

**gcolvin** (2019-02-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> Would also be good to get a survey of dynamic jump usage, I’m not exactly sure how prevalent it is or how many different ways it is used

Every return from a subroutine in Solidity requires a dynamic jump.

---

**fubuloubu** (2019-02-23):

Is that the only use? Do people develop in assembly alternative uses? Where’s the usage data?

---

**gcolvin** (2019-02-23):

Dynamic jumps also used for switch statements and virtual functions, and could be used in lots of creative ways in assembly code, I suppose.  I’m not too concerned about placing a bit of a burden on creative assembly coders in return for better high-level code generation.

---

**fubuloubu** (2019-02-23):

I just want to make sure we don’t miss a geniune use case in our mission to salt the earth of dynamic jumps (sarcasm mine)

---

**gcolvin** (2019-02-23):

Thus the call for introduction in two phases.  We can make validation optional if need be, but I’m not sure I’ve ever seen the use of unconstrained dynamic jumps in programs for other CPUs.  Or even an unconstrained dynamic jump instruction (and please someone correct me.)

---

**expede** (2019-02-23):

Yes, they could be split into 2 (or 3) EIPs. I feel that this would be cleaner as well. I brought this up a while back, and the prevailing feeling was that since this EIP already has momentum, just let it be. TL;DR yes, but no for political reasons.

Also, I don’t think that any of these features are controversial. Let’s just get them into the spec.

---

**expede** (2019-02-23):

Yes, absolutely we could do that. In fact, there’s nothing stopping a client from doing actor-style parallel execution for performance reasons today, *without these changes,* for large use cases. Invoking the *same* contract concurrently gets much more tricky, but yes that analysis is both possible and easier if these changes go in.

As an aside, there’s a lot of optimization that mainstream clients could be doing that they’re not currently. From my cursory reads through several of them, they’re pretty much straight out of the Yellow Paper verbatim, run interpreted, don’t attempt to use natively-sized words, process sequentially, and do gas bookkeeping with at runtime on each opcode call. There’s a lot of room to speed up the existing clients, without needing to wait for eWASM.


*(131 more replies not shown)*
