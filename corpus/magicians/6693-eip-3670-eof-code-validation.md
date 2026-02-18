---
source: magicians
topic_id: 6693
title: "EIP-3670: EOF - Code Validation"
author: axic
date: "2021-07-20"
category: EIPs > EIPs core
tags: [evm, shanghai-candidate, evm-object-format]
url: https://ethereum-magicians.org/t/eip-3670-eof-code-validation/6693
views: 28780
likes: 1
posts_count: 13
---

# EIP-3670: EOF - Code Validation

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3670)





###



Validate EOF bytecode for correctness at the time of deployment.

## Replies

**axic** (2022-02-05):

Since EIP-3670 was added to the CFI (Considered for Inclusion) list for Shanghai today, I’d like to raise a question regarding this in the rationale:

> The deprecated CALLCODE (0xf2) opcode may be dropped from the valid_opcodes list to prevent use of this instruction in future. Likewise SELFDESTRUCT (0xff) could also be rejected. Yet we decided not to mix such changes in.

It would be nice to disallow these two instructions, which means EOF contracts containing those instructions cannot be deployed. (Legacy contracts are unaffected.)

I think `CALLCODE` is a no brainer.

`SELFDESTRUCT` is a more complicated topic, depending on the fate of it, it may become a feature for sending value without triggering execution. I personally think that is not a good idea, so would propose to reject that in EOF.

---

Furthermore, depending on other proposals it would be possible to restrict further instructions:

- PC if EIP-4200 is adopted
- JUMPDEST if either EIP-3690 or EIP-4200+EIP-4750 is adopted

---

**gcolvin** (2022-02-07):

If an instruction is deprecated then I think that almost by definition a contract that uses them is invalid, and therefore should not pass code validation.

---

**poojaranjan** (2022-05-25):

EVM Object Format (EIP-3540 & EIP-3670) with [@gumb0](/u/gumb0) [@axic](/u/axic) [@chfast](/u/chfast)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/8/8737bc420fc5c63f4a0a33520a906086af2447d0.jpeg)](https://www.youtube.com/watch?v=GMeRA-xPp-E)

---

**fulldecent** (2024-11-04):

I am writing to express opposition for EIP-3670 and all the related changes for contract correctness consensus changes.

---

The threshold for changing consensus clients should be high. Extremely high. Billions of dollars high.

Currently the price of upgrading the consensus client is artificially low because Ethereum Foundation owns an exclusive use to the “Ethereum” trademark and nobody else can fork the project. And they [refuse to answer any questions](https://x.com/fulldecent/status/1852313638092296422) about whether forks are acceptable if they are proposed by the community.

---

So, does this EIP clear the threshold of being extremely valuable? Of course not!

Static analysis can be done easily. Every client can do this static analysis every time any transaction is prepared.

That static analysis can be standardized (do it!). We can call it EVM version 20.1 instead of 20.0 or whatever the current version is. And the ecosystem can voluntarily opt into it.

It could even be done on-chain as a registry if anybody really cared about this.

But making the clients reject transactions for the static analysis check is obviously not worth it.

---

**fulldecent** (2024-11-04):

Also FYI [@axic](/u/axic) [@gcolvin](/u/gcolvin), the SELFDESTRUCT is now officially deprecated, if that makes a difference. EIP-6049.

---

**gcolvin** (2024-12-03):

Hello [@fulldecent](/u/fulldecent).  I’m not concerned here about the politics of the Foundation.  I’m concerned about what – to me and the many other people who need them – are *obviously* valuable changes.

---

**shemnon** (2024-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> So, does this EIP clear the threshold of being extremely valuable? Of course not!

3x efficiency gains on zk evaluation is extremely valuable.  This is made possible by code validation and stack validation, which allows the zk systems to skip stack height checking and other categories of checks that must be done per-operation in the absence of prior validation, which looks to be 66% of the per-op overhead in zk arithmetization.



      [x.com](https://x.com/cairoeth/status/1853521032826745032)





####

[@cairoeth](https://x.com/cairoeth/status/1853521032826745032)

  What are the performance benefits of EOF (EVM Object Format)?

At the @SuccinctLabs residency, my benchmarks reveal ZK proving EOF is ~3x more efficient and runs 2.69x faster than the current EVM version ⛽

(link below)

  https://x.com/cairoeth/status/1853521032826745032

---

**fulldecent** (2024-12-27):

All of these changes can be implemented much better without making breaking changes to the client.

1. Make improvements to the client for static analysis
2. Make improvements to the compiler for code generation

It is not necessary to implement a rejection of any currently-legal code to achieve this.

If 3x reduction is possible you get 3x reduction for the contracts that do the better things.

---

**shemnon** (2024-12-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> It is not necessary to implement a rejection of any currently-legal code to achieve this.

This does not propose the rejection of any currently-legal code.  That occurred with [EIP-3541](https://eips.ethereum.org/EIPS/eip-3541), as part of the London hard fork.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> If 3x reduction is possible you get 3x reduction for the contracts that do the better things.

Part of this 3x improvement comes with a presumption that any EOFv1 contract has been verified prior to being added to an account on the chain. That’s what this EIP does: for contracts that chose to opt in (by having the EOF header) the creation contract will run these validations once as part of contract deployment.  If a collaborative approach were used then the ZK systems could not assume the contract is valid simply by a marker, and would have to re-verify. The performance gains then become percentages instead of multiples if validation must occur for each transaction or block.

---

**fulldecent** (2024-12-28):

The validation can be performed whether or not we require validations to be performed right?

And a successful validation can be saved as a bit of data, right?

---

**pdobacz** (2025-01-14):

We need to require the validation, in order for the presumption [@shemnon](/u/shemnon) is referring to above to be true for code on-chain. This in turn can only be achieved by clients agreeing on what valid code is.

---

**chfast** (2025-01-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Make improvements to the client for static analysis

This task may be difficult to perform but it is easy to benchmark. Can you propose any such improvement? This can be checked against all Mainnet deployed contracts for evaluating its effectiveness.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Make improvements to the compiler for code generation

This assumes cooperation between compilers and client implementations what is generally not the case. This is adversarial environment so even of all known compilers obey some agreed rules nothing prevents someone to deploy a code that don’t. If you want to prevent it by “economics” you will likely need a complicated gas model. Will it be simpler than the validation?

Moreover, compilers optimize for the gas model. If there is competition between compilers they may exploit some gap in the gas model even though this would be against the pre-agreed cooperation rules.

