---
source: magicians
topic_id: 734
title: EVM Evolution Session
author: expede
date: "2018-07-15"
category: Protocol Calls & happenings > Council Sessions
tags: [evm, evm-evolution]
url: https://ethereum-magicians.org/t/evm-evolution-session/734
views: 2900
likes: 9
posts_count: 14
---

# EVM Evolution Session

Notes from the *EVM Evolution* session at the 2018 Berlin Council. I had to type pretty quickly; apologies if any points are missing (please leave a comment if this is the case). Since the conversation jumped back and forth a bit, these are organized by topic, not chronologically. Thanks everyone for participating and making this a great session! ![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=15)

# History

- 256-bit native is weird
- Lots of crytpography relies on large numbers
- Many people questioning why this design decision was made

Why single fixed sized? Something like the CLR or JVM

Only one VM expert early on, none at the beginning

- Looked like a simple “classroom exercise”
- Resources now going into WASM instead of EVM 1.5
- EIPs for subroutines, deprecate JUMP, vector arbitrary access

# EVM

- Old EVM contracts must always be available, esp since they can create more contracts for all time

## 1.5 Roadmap

- Discontinued / deprecated
- Subroutines, static jumps, unfinished, Sol not mature enough to test
- Vector processing complete, but untested w/ Sol
- Quasi-official statement: eWASM is on roadmap, in par with Capser/sharding
- Client devs frustrated because effort wasted (ex. previous Casper spec)
- Register too wide (256 bits), storage too narrow (256-bits)

Why not pay for pages?
- How about immutable data structures?
- Probably designed this way because of simplicity rather than real world
- These changes may make existing contracts less efficient

How realistic to get this on mainnet?

- No resources allocated for paid work
- Probably worth pushing forward to core devs
- A client team would need to champion it

## Architecture

- Stack machines perform very well on wide words
- Register machines better with narrow words
- Arbitrary with a good compiler
- Initial EVM design used stack for working memory, Sol uses as call stack
- Sol has to do weird stuff because no subroutine instructions
- Contracts don’t live long enough to really need freeing refs

#

- eWASM = WASM - floats + EEI

EEI: Ethereum Environment Interface
- People like the host function design

Main purpose *not* to run in browser, though possible

- Light client to bring closer to MetaMask, &c
- Could run over TCP/IP or sockets (and so on)

JIT probably not a great idea

- DDoS is an issue

Adversary may write a program that takes a long time to JIT
- Possible to work around, but extremely difficult

Exploring gas cost for certain cases
May gas meter JIT compilation

Some questions on why switch to WASM from major players not in room
100% of work so far is EVM-compatible

- No new opcodes, everything is transpilable
- Especially gas semantics

They’re identical to EVM

## Differences from Regular WASM

- eWASM is WASM, just restricted
- No floating-point
- No need for threads
- High determinism

## Roadmap

- Is there value in continuing with EVM vs just sticking with eWASM?
- Interest in variable-length storage

### Ideas

- ERC20 primitives/opcodes?

### Contributing Upstream

- Why no opcode for atomic ETH send

Workaround exists (requires self-destructible intermediate)
- Let’s add SIMPLE_SEND to eWASM

## eWASM is interesting because…

- EVM has mix high level and low level opcodes
- Cleans up a lot of stuff
- WASM is well designed, lots of money behind it
- Closer model to chip

Great perf
- Resource constraint friendly (phones)
- Web compatible
- Takes advantage of LLVM

Debuggers, &c

Would be much faster because (for example) native registers

Makes it easier to write new clients
Lower attack surface

#

- Based on K, correct by construction, &c &c (all the good stuff)
- Higher level of abstraction has advantages for cross-compilation, verification, and so on

# Sharding

- Only needs to share consensus and security
- Could run on whatever VM
- May not need to be EVM-bytecode compatible

## Replies

**lrettig** (2018-07-17):

Excellent notes, thanks for taking these and for sharing them!

---

**fubuloubu** (2018-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/expede/48/4738_2.png) expede:

> eWASM is interesting because…
>
>
> Lower attack surface

Can someone run through the arguments and/or proof behind this statement?

---

**fubuloubu** (2018-07-18):

Also, what considerations are there for the impact of inclusion of eWASM into the Ethereum 2.0 roadmap, since existing compilers and toolsets will have to be substantially rewritten to accommodate the new design? Will there be a release of the eWASM work prior to Ethereum 2.0 such that this work can be done in preparation for release of the upgraded network?

---

**gcolvin** (2018-07-18):

In the eWasm standup there was discussion of parallel, coordinated development of 1.5 and eWasm.  From memory (there are notes somewhere)

1. Delays in the Cheshire Casper mean the current EVM must live even longer than anticipated.  That leaves users with an incomplete, formally intractable machine.  Formally intractable means it’s hard to prove properties like “will not vaporize a million ETH.”
2. More progress on EMV1.5 has been made than people realize, with much of the eWasm work like Iulia able to generate 1.5 byecodes, and many 1.5 byte codes implemented.
3. eWasm is in some ways more experimental and requires more resources. E.g. it requires compilers to achieve performance goals, whereas the first phase of EVM 1.5 (EIP-615) only requires interpreter extensions.
4. eWasm experiments fairly naturally fit with casper/sharding experiments, whereas EVM1 evolution fits fairly naturally on the main chain. eWasm can start moving to the main chain when stable.
5. Transpilers and K specs can keep the two from conflicting.
6. Alternatively, eWasm can become a shard-only VM, with EVM remaining the mainchain VM.
7. I’m not the expert, but I don’t think shasper requires any changes to the mainchain.

---

**fubuloubu** (2018-07-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> Alternatively, eWasm can become a shard-only VM, with EVM remaining the mainchain VM.

Neat idea!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> eWasm can start moving to the main chain when stable.

This is needed for a smooth transition.

---

**gcolvin** (2018-07-18):

Here are the eWasm notes:

https://notes.ethereum.org/9hg30dhNQmCWdliLDI5n4w

---

**lrettig** (2018-07-18):

Greg, I broke out the EVM roadmap stuff from that hackmd into a new one: https://notes.ethereum.org/QZIZdIahTnaTlv4ICsi5wg

---

**lrettig** (2018-11-27):

It’s been a while but my interpretation of that line item is as follows. Today, if you want to build a new Ethereum client from scratch, you have to implement a bunch of things including precompiles in trusted, native code. In an Ewasm-enabled world, a lot of this logic can live *on chain* inside regular contracts running safely inside the VM. In other words, they no longer need to be trusted code. Over time, more bits and bobs of the codebase could be migrated on chain in an Ewasm-enabled world.

---

**fubuloubu** (2018-11-27):

Thanks for the clarification, that is helpful.

I took the original comment to mean that WASM had a lower attack surface than EVM. I was thinking about DoS hardenness of the two options.

The correct interpretation, as you mentioned, is that eWASM can eliminate our dependance on precompiles, which is an attack surface of the current design (computations whose true cost isn’t well reflected).

Did I get that right?

---

**lrettig** (2018-11-27):

Precisely, that’s my understanding. I wouldn’t, as a general statement, say that Wasm has a lower attack surface than EVM.

---

**seven7hwave** (2018-11-27):

(Hello Magicians. Porting this over from twitter, commenting on the Working Group Proposal; thanks Lane)

Regarding security…does the existence of two parallel VM’s introduce systemic risk? The increased complexity of having separate VM’s, executing separate instruction sets, seems to increase the attack surface. In other words, the security benefits gained from eliminating dependance on precompiles might be countered by the resulting complexity stemming from the above proposal. Or can those risks be managed? And loosely speaking, how would you go about testing this setup? Could you throw fuzzers at it, similar to how Geth/Parity is tested?

On another note, it seems like this would make life a bit easier for end-user DApp developers. If so, that’s a nice win  : )

---

**boris** (2018-11-27):

I think Lane just remembered to come back and answer some of these questions from the session in Prague - but all good as long as questions get answered!

The proposal thread is here — [Ewasm working group proposal for Eth 1.x](https://ethereum-magicians.org/t/ewasm-working-group-proposal-for-eth-1-x/2033)

---

**lrettig** (2018-11-28):

[@boris](/u/boris) is right, sorry to misdirect you [@seven7hwave](/u/seven7hwave), let’s take the discussion to that other, more recent thread? The conversation [@fubuloubu](/u/fubuloubu) and I were just having here is relevant, too, though.

