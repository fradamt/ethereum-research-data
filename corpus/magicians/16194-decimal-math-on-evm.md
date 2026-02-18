---
source: magicians
topic_id: 16194
title: Decimal Math on EVM
author: 1m1-github
date: "2023-10-21"
category: EIPs > EIPs core
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/decimal-math-on-evm/16194
views: 1872
likes: 4
posts_count: 3
---

# Decimal Math on EVM

**Add decimal math to the EVM** by adding the following OPCODEs:

DECADD, DECNEG , DECMUL, DECINV, DECEXP, DECLN, DECSIN

A Decimal defined as c∗10^q with c (coefficiant) and q (exponent) taken from the stack and interpreted as `int256`.

**Why decimal?**

Most calculations conducted by humans work with decimal values. E.g. 0.1 is a very commonly used number, but cannot be represented in binary finitely.

**Why `exp`, `ln`, `sin`?**

`exp`, `ln`, `sin` are universal functions. Combining `exp` and `ln` allows one to compute powers (`a^b = exp(b*ln(a))`), which gives access to all polynomials. From `sin`, one can derive all of trigonometry. In total, we get all [elementary functions](https://en.wikipedia.org/wiki/Elementary_function)

> This invites mathematical finance, machine learning, science, digital arts and more to Ethereum.

It allows one to solve integrals, differential equations, optimize and so much more.

**eVm**

The EVM is a *virtual* machine and thereby not restricted by hardware. Usually, assembly languages provide OPCODEs that reflect the ability of the hardware. In a virtual machine, we have no such limitations and nothing stops us from adding more complex OPCODEs, as long as fair gas is paid. At the same time, we do not want to clutter the OPCODEs library.

**OPCODE definitions**

DECADD a+b OpCode = 0xd0 (ac, aq, bc, bq, precision) → (cc, cq)

DECNEG -a OpCode = 0xd1 (ac, aq) → (bc, bq)

DECMUL a*b OpCode = 0xd2 (ac, aq, bc, bq, precision) → (cc, cq)

DECINV 1/a OpCode = 0xd3 (ac, aq, precision) → (bc, bq)

DECEXP exp(a) OpCode = 0xd4 (ac, aq, precision, steps) → (bc, bq)

DECLN ln(a) OpCode = 0xd5 (ac, aq, precision, steps) → (bc, bq)

DECSIN sin(a) OpCode = 0xd6 (ac, aq, precision, steps) → (bc, bq)

precision is the # of digits kept. steps for DECEXP and DECSIN are the # of Taylor expansion steps. steps for DECLN is the depth of the continued fractions expansion.

**Implementation**

I have implemented these OPCODEs already, as part of the ETHOnline hackathon (2023); pls see the link at the bottom.

My plan for the hackathon was submitting an EIP. I was not aware that a discussion on this forum was required beforehand.

More details can be found in the Readme.md, incl. [gas considerations](https://github.com/1m1-github/go-ethereum-plus/tree/main#gas), etc. Not sure whether I should rewrite those things here.

The `geth` implementation is functional, with precise gas costs, charged double. It is currently named EVM+, to suggest that this is like going from a basic calculator (EVM) to a scientific calculator (EVM+). I will soon run an (open) EVM+ node and welcome anyone to do the same.

Two first examples that work, as Yul smart contracts:

[The BlackScholes formula](https://github.com/1m1-github/go-ethereum-plus/blob/main/tests/EVMPlus/BlackScholes.yul), gas cost ca. 32k.

[A single sigmoid Neuron](https://github.com/1m1-github/go-ethereum-plus/blob/main/tests/EVMPlus/Neuron.yul), gas cost ca. 24k.

The actual charged gas is currently doubled.

repo: [GitHub - 1m1-github/EVMPlus: add decimal math to EVM](https://github.com/1m1-github/go-ethereum-plus)

live node: [EVMPlus/README.md at main · 1m1-github/EVMPlus · GitHub](https://github.com/1m1-github/EVMPlus/blob/main/README.md#live)

EIP: [Add EIP: EVM decimal math by 1m1-github · Pull Request #7904 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7904)

## Replies

**EvanOnEarth** (2023-10-21):

Amazing work, [@1m1-github](/u/1m1-github)! This is clearly a huge upgrade to the EVM, with a number of different advantages. To me, the most important part of this EIP is how it leads to a brighter AI future.

Years from now, will artificial intelligence revolt against humankind in some sort of 2001 Space Odyssey nightmare? Maybe. With over 90% of ML and AI development going into adtech and surveillance technology, centralized companies’ developments largely contribute towards a future AI that wants to manipulate us, spy on us, and sell us things.

With this EIP, artificial intelligences can live on democratic, fully transparent distributed computers. These AIs, rather than growing ever more effective at supporting companies’ private interests, would instead grow ever more effective at supporting the democratically-decided interests of all humankind.

It also appears that this EIP has no downside. The use of these opcodes is optional, correct? So anyone who wants to use the existing opcodes for arithmetic can still use them, yes? This means it couldn’t have any negative effects on existing smart contracts either. Please correct me if I am wrong on this [@1m1-github](/u/1m1-github).

---

**1m1-github** (2023-10-22):

ty … yes, the opcodes are completely independent from others … it benefits those that need some math … the others can ignore … the community would just need to decide whether it’s worth blocking 7 opcodes … i think yes

