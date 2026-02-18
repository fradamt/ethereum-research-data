---
source: ethresearch
topic_id: 2791
title: EVM performance
author: kladkogex
date: "2018-08-03"
category: EVM
tags: []
url: https://ethresear.ch/t/evm-performance/2791
views: 13992
likes: 37
posts_count: 25
---

# EVM performance

Our of our engineers recently measured bare-bones EVM performance both for JIT and not JIT  for transactions that did not include state changes (so this is essentially performance of bytecode interpretation).

It was 20,000 TPS without JIT and 50,000 TPS JIT for simple transaction (Fibonnachi number calculation)

We are currently measuring TPS for transactions that involve state transitions. It looks that state transitions take much longer than math for typical transactions.

Does this sound sane ?)

## Replies

**mratsim** (2018-08-03):

What are the number in MIPS (Millions of Instructions Per Seconds), i.e. opcodes interpreted per second? And what is the CPU frequency and generation (Haswell, Skylake, …).

I would expect a big hit of EVM speed compared to naive VM due to the use of uint256 by default, especially for Go as those require heap allocation (or a memory pool).

Here is a wiki where I compiled several resources on [state-of-the-art VM optimization.](https://github.com/status-im/nimbus/wiki/Interpreter-optimization-resources) It also includes a naive VM with 7 instructions benchmark that can serve as a baseline to compare EVM against. And can be used to compare language raw speed on the same machine as well.

Edit:

It seems like your impression is consistent with Aleth/Cpp-ethereum: [C++ DEV Update - July edition | Ethereum Foundation Blog](https://blog.ethereum.org/2016/07/08/c-dev-update-summer-edition/)

> In practice, these speedups will only be relevant to “number-crunching” contracts because the computation time is otherwise largely dominated by storage access.

---

**kladkogex** (2018-08-07):

Great resources !

It seems to me that EVM should always do compilation. Smart contracts are deployed very infrequently and run for long time.

---

**gcolvin** (2018-08-08):

Thanks for the Wiki [@mratsim](/u/mratsim), will help me catch up on the literature.  Most interesting point I saw so far is that on recent Intel chips simple switch dispatch is much faster than it used to be.

Can I ask which EVM you were measuring, [@kladkogex](/u/kladkogex)?  They vary widely in their performance, as I reported at Devcon3.  The numbers you give look about right for the C++ interpreter versus the C++ JIT.

It’s true that the 256-bit registers hurt performance a lot.  A compiler could optimize this away in many cases, but that doesn’t change the gas cost.  Switching to a gas model like IELE’s might help that – they charge more gas for an operation as the size of the operands increases.  eWasm solves the gas problem by not supporting wide registers.

However we solve the gas problem, JITs can’t help us.  They are too big of an attack surface, as the eWasm team reported recently on an AllCoreDevs call.  Bytecode will need to be translated to machine code at deployment time with DoS-hardened compilers.

And indeed state access currently accounts for more time than contract execution, but that is in part because contract execution is so expensive that people don’t write computationally intensive contracts.  Including us–we write new pre-compiles instead.

---

**kladkogex** (2018-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/gcolvin/48/41_2.png) gcolvin:

> Can I ask which EVM you were measuring, @kladkogex? They vary widely in their performance, as I reported at Devcon3. The numbers you give look about right for the C++ interpreter versus the C++ JIT.

We run ethereum-cpp - our codebase started with ethereum-cpp fork …

![](https://ethresear.ch/user_avatar/ethresear.ch/gcolvin/48/41_2.png) gcolvin:

> However we solve the gas problem, JITs can’t help us. They are too big of an attack surface, as the eWasm team reported recently on an AllCoreDevs call. Bytecode will need to be translated to machine code at deployment time with DoS-hardened compilers.

Not 100% sure. Java applets run on JIT-compiled code - they are reasonably secure …

---

**gcolvin** (2018-08-08):

The security issue here is denial of service.  Unless designed to prevented it compilers are subject to quadratic blowup.  Fuzz testing of V8 by the eWasm team found that most contracts could be compiled in 100ms, but some “compiler bombs” could take 2 secs.  So an attacker could use such bombs to create DoS attacks.  (There are other vulnerabilities, such as caches of compiled code that can be defeated.)

[Ethereum Core Devs Meeting 39 Notes, Concerns about wasm](https://github.com/ethereum/pm/blob/master/All%20Core%20Devs%20Meetings/Meeting%2039.md#concerns-about-wasm)

---

**kladkogex** (2018-08-11):

I see … One could reject smartcontracts if they dont compile after certain number of cycles …

---

**gcolvin** (2018-08-12):

One could, but the wasm team doesn’t see that as an answer, since some compilers might choke and others not on the same input.  Rather, we’ll need compilers that never take more than about n*log(n) time or space.

---

**0zAND1z** (2018-08-13):

Thanks for the input [@gcolvin](/u/gcolvin), I’m working on the integrating [binaryen](https://github.com/webassembly/binaryen) to EWASM’s `hera` Virtual Machine.

Hope these passes may be of useful reference with context: https://github.com/WebAssembly/binaryen/tree/master/src/passes

Happy to make notes & work on the performance down the line.

---

**kladkogex** (2018-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/gcolvin/48/41_2.png) gcolvin:

> wasm

I understand.

BTW - does a (possible) move to EWASM look like a bad thing to you from the point of security?  It seems that currently EVM is simple and moving to EWASM introduces lots of things. Just based on a generic complexity lots of things mean lots of potent

ial security holes.

Another question is whats the point for Ethereum to move to EWASM at all? The network for the PoW chain is so slow at 15 transactions per second, that it seems that the best for the PoW chain is to stay with EVM as is. Whats the driver behind the move to EWASM?

---

**gcolvin** (2018-09-01):

[@kladkogex](/u/kladkogex)

The desire for a faster VM is to stop the need for writing precompiled contracts.  They only exist because the EVM isn’t fast enough, and/or charges too much gas.  Secondarily, to let users do similar expensive crypto stuff that we didn’t put into a precompile for them.

Another reason for eWasm is the desire to reuse other work, so far as languages, compilers, VMs, IDEs etc.

The eWasm subset (not full-on Wasm) needn’t be a security issue, but it needs DoS-hardened compilers, just as a faster EVM would.  Even at 15 TPS we’ve had at least two DoS attacks on the EVM: one due to mispricing EXP and another due to geth’s JIT going quadratic.

It’s looking likely that eWasm will continue as part of the shasper work, and I will restart my EIP-615 and EIP-616 work to get the EVM more formally tractable and performant on the main chain, with transpiling from EVM to eWasm providing a bridge.

---

**mratsim** (2018-09-01):

I’m wondering the impact of Meltdown, Spectre and L1TF/Foreshadow mitigations: https://www.phoronix.com/scan.php?page=article&item=linux-419-mitigations&num=1.

Much of the performance of VMs rely on efficient branch predictor, especially after improvement Haswell even on switch-based dispatch. Disabling speculative execution might make the EVM much slower.

The Phoronix benchmarks show horror stories of more than 20% performance lost on some benchmarks.

---

**gcolvin** (2018-09-20):

From what I’ve read it’s not at at all clear to me what impact the various patches will have on the EVM, or on the client as a whole  The biggest losers on the benchmarks look to be things like process scheduling.

---

**fubuloubu** (2018-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/gcolvin/48/41_2.png) gcolvin:

> Another reason for eWasm is the desire to reuse other work, so far as languages, compilers, VMs, IDEs etc.

How does this balance with the fact that it will nuke our existing selection of tools, even though they are still young? Existing languages, compilers, etc. would also have to be adopted to the unique challenges of programming consensus-critical, immutable code in a different model than most general purpose languages leverage. How many of these languages have primitives for account-based transactional programming and atomic commitments?

![](https://ethresear.ch/user_avatar/ethresear.ch/gcolvin/48/41_2.png) gcolvin:

> The eWasm subset (not full-on Wasm) needn’t be a security issue

I think it’s a fair assessment from a network liveness standpoint, but I interpret “security” in an immutable programming framework like ours as the ability to write this code well prior to deployment, as to avoid (as much as possible) any dangerous and unanticipated state changes that may alter ownership of funds and assets built into Ethereum. How does this new paradigm affect security from that perspective?

---

These are the kind of questions that keep me up sometimes, along with the shear complexity of analyzing the security model of a JIT VM to conduct proper code review for a high-value user. Many high end firms have WASM experience, but it may price the lower end of security reviews out of the market due the complexity of the anaylsis required. The simplicity of the EVM is very attractive to me for that reason, but it is a trade with tooling.

The longer we work on EVM, the more painful it will be to port over the ecosystem later.

---

**axic** (2018-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> How does this balance with the fact that it will nuke our existing selection of tools, even though they are still young?

It will not nuke it, at least not Solidity. The plan is that the intermediate language of Solidity, Yul, will have an ewasm target.

Other languages are invited to use Yul as an intermediate output, Vyper could do that also ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**fubuloubu** (2018-09-27):

That works for Compilers!

How does that work for testing frameworks, formal analysis tools, semantic analyzers, etc.?

Edit: that was our plan with LLL

---

**fubuloubu** (2018-09-27):

Developing smart contracts is (or should be) 10% code, 90% validation and verification. Those are the tools I’m talking about.

---

**gcolvin** (2018-09-30):

[@fubuloubu](/u/fubuloubu)  80/20 or 90/10 is the rule of thumb across many domains.

The security of individual contracts is a matter of whether they do what they are intended to do.  Verify, review, test…  The simplicity or the EVM makes formal verification simpler, and I’m working to make it simpler still. eWasm is simple enough at this level as well, and technically EVM and eWasm can continue to evolve in parallel.

The security of the network is a matter of gas costs aligning well enough with actual client performance to not be DoS vectors.  Our simple, battle-hardened EVM interpreters have the advantage there for now.

---

**fubuloubu** (2018-09-30):

I agree that network security is a separate concern, and have confidence that it will be handled well to prevent DoS.

Compilers can be updated with hopefully minimal disruption to developers by substituting a new IR compilation process. This is assuming none of the fundamentals of using the EVM change (in a backwards-incompatible way).

Verification tools is a larger effort. Many tools manage their own model of the EVM and present that to the user for analysis, and if they have not created adequete abstraction this process could be painful for them and their users. We should account for it in any release schedule. K framework, Mythril, and Manticore are a few I have in mind, but many more exist.

Perhaps this is already accounted for, but we must have all the stakeholders aligned in advance of releasing eWASM so we all have time to add this ability to our projects and inform our users of how to migrate their code. This needs to happen regardless of whether Ethereum 1.0 ends up a subchain or not.

---

**gcolvin** (2018-10-14):

I have less confidence than you do that network security will be handled well, Bryant.  Ethereum’s requirements are not the same as most other networks, and I think many client developers have yet to grapple with the implications.

I’m not sure which compilers it is you think can be updated easily.  I think most all our EVMs are interpreters, and wouldn’t trust existing Wasm compilers with any kind of security.

As I understand it the EVM would not wind up a subchain anytime soon, as EVM code must keep running on the mainchain in order for the Shasper beacon chain to work.  Further, every accessible EVM contract on the blockchain must keep running somewhere.

And indeed, verification is difficult, and porting verified EVM code to eWasm–and your specs and models and tools–might not be fun.  It would easier to trust an evm2wasm compiler.

So I expect it will take a while for the community to sort out where all of this is going, and expect eWasm to expand the ecosystem rather than replace the EVM.  Things have by no means all been accounted for–in many ways we are just getting started.

---

**chfast** (2018-10-14):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I see … One could reject smartcontracts if they dont compile after certain number of cycles …

Reject and do what? Once the contract has been deployed you **must** execute it no matter how hard it is.

What currently looks promising for wasm are so called “baseline” JITs. These sacrifice optimization of the final machine code but are capable of performing verification and compilation in a single pass. Both SpiderMonkey (Firefox) and V8 (Chrome, nodejs) now have those.

We should have some number for Devcon.


*(4 more replies not shown)*
