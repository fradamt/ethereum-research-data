---
source: ethresearch
topic_id: 17387
title: Poloniex hacker lost $2,500,000 to a known ERC-20 security flaw that I disclosed in 2017
author: Dexaran
date: "2023-11-10"
category: Security
tags: []
url: https://ethresear.ch/t/poloniex-hacker-lost-2-500-000-to-a-known-erc-20-security-flaw-that-i-disclosed-in-2017/17387
views: 1837
likes: 3
posts_count: 8
---

# Poloniex hacker lost $2,500,000 to a known ERC-20 security flaw that I disclosed in 2017

A followup to my previous post [Security concerns regarding token standards and $130M worth of ERC20 tokens loss on Ethereum mainnet - #17 by Dexaran](https://ethresear.ch/t/security-concerns-regarding-token-standards-and-130m-worth-of-erc20-tokens-loss-on-ethereum-mainnet/16387/17)

I made [this post](https://www.reddit.com/r/ethereum/comments/17sbxpp/poloniex_hacker_just_lost_2500000_to_erc20/).

Here is a copy of the content [poloniex_hacker_lost_funds.md · GitHub](https://gist.github.com/Dexaran/9bd90c1885b4818573368ad02b784125)

It obviously got insta deleted from the subreddit. If someone can slap those reddit mods - please do it.

---

> The post

---

Poloniex exchange was [just hacked](https://www.fxstreet.com/cryptocurrencies/news/crypto-exchange-poloniex-hack-leads-to-60-million-in-assets-stolen-peckshield-says-202311101206).

A hacker made this transaction https://etherscan.io/tx/0xc9700e4f072878c4e4066d1c9cd160692468f2d1c4c47795d28635772abc18db

And the tokens got permanently frozen in the contract of GLM! This shouldn’t have happened if ERC-20 GLM token would be developed with security practices in mind. But ERC-20 still contains a security flaw that I discloser multiple times (here is a [history of the ERC-20 disaster](https://dexaran820.medium.com/erc-20-token-standard-7fa2316cdcac)).

You can also find a full history of my fight with Ethereum Foundation over token standards since 2017 here [ERC-223](https://dexaran.github.io/erc223/)

The problem is described [here](https://dexaran820.medium.com/known-problems-of-erc20-token-standard-e98887b9532c).

Here is a security statement regarding the ERC-20 standard flaw: [ERC-20 Standard - Callisto Network Security Department Statement](https://callisto.network/erc-20-standard-security-department-statement/)

As of today, about [$90,000,000 to $200,000,000 are lost](https://dexaran.github.io/erc20-losses) to this ERC-20 flaw. Today we can increase this amount by $2,500,000.

The problem with ERC-20 token is that it doesn’t allow for error handling which makes it impossible to prevent user errors. It was known for sure that the GLM contract is not supposed to accept GLM tokens. It was intended TO BE THE TOKEN, not to own the tokens. For example if you would send ether, NFT or ERC-223 token to the address of the said GLM contract - you wouldn’t lose it.

Error handling is critical for financial software. Users do make mistakes. It’s a simple fact. Whether it is misunderstanding of the internal logic of the contract, unfamiliar wallet UI, being drunk when sending a tx or panicking after hacking an exchange - doesn’t matter. Anyone could be in a position of a person who just lost $2,5M worth of tokens to a simple bug in the software that could have been easily fixed.

I would use an opportunity to mention that ERC-223 was developed with the main goal of preventing such accidents of "funds loss by mistake: https://eips.ethereum.org/EIPS/eip-223

What is even worse - EIP process doesn’t allow for security disclosures now. There is simply no way to report a security flaw in any EIP after its assigned “Final” status.

I’m proposing a modification to EIP process to allow for security disclosures here: [Modification of EIP process to account for security treatments - #12 by Dexaran - Process Improvement - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/modification-of-eip-process-to-account-for-security-treatments/16265/12)

There are ongoing debates on submission of an informational EIP regarding the ERC-20 security flaw: [ethereum-cat-herders/EIPIP#293](https://github.com/ethereum-cat-herders/EIPIP/issues/293)

And the Informational EIP pull request: [ethereum/EIPs#7915](https://github.com/ethereum/EIPs/pull/7915)

We’ve built ERC-20 <=> ERC-223 token converter that would allow both standards to co-exist and eventually prevent the issue of lost funds [ERC223 converter](https://dexaran.github.io/token-converter/)

Also my team is building a ERC-223 & ERC-20 compatible decentralized exchange that will also remove such a weird opportunity to lose all their life savings to a software bug from users: https://dex223.io/

If you are rich and worried about ERC-20 security bugs dealing damage to Ethereum ecosystem and ruining users days - welcome to our ERC-223 family. We stand for security. We don’t let our users funds to be lost by mistake.

## Replies

**ghasshee** (2023-11-20):

I had given up demanding EF for secure contract long long ago since EVM was designed to allow bugs.

I am studying compiler theory about 10 years and very slowly so that we could develop a compiler on top of EVM with which we can develop a safe contract. Why not abandon solidity and develop a new compiler ? Let’s try the research of formal verification and compiler theory!

---

**Dexaran** (2023-11-21):

I’m involved in smart-contracts security for ~8 years now (since the DAO hack). Have been an auditor, a CTO of an auditing organization and a hacker.

I’m very skeptical about formal verification. It is not possible to “formally verify” the correctness of the logic in any sensible way.

As for compilers & solidity - I think that the development of solidity was a mistake. It would be much better to take an already-existing programming language with existing and time-tested toolchain instead of developing a whole new one just for smart-contracts.

Here is my article about the new languages for contracts [New programming language for smartcontract is a mistake | EOS Go Blog](https://www.eosgo.io/blog/development-of-new-programming-language-for-smart-contract/)

---

**mratsim** (2023-11-22):

You’re mixing 2 things:

- The VM
- The languages (Solidity, Vyper, Fe) that target it

Due to very high-cost of modifying an ISA, and the almost impossibility to remove instructions/opcode from an ISA, everything that can be done at the compiler or language level should be moved to compiler and language level.

Things should be “ossified” at ISA-level only when they have demonstrated as critical to the ecosystem and native support is necessary.

For example:

- RIPEMD160 use-case quite doubtful, but everyone has to support it, including zkEVMs
- “safe arithmetic”, i.e. addition, substraction, multiplication with overflow and underflow checks or saturated arithmetics are not part of the ISA, but they can be implemented at the compiler level (Vyper, Fe) or the library level (Solidity). Note: than no hardware ISA supports overflow/underflow check, it’s always done in software at the compiler level.

The EVM cannot prevent design bugs, if someone writes a smart contract that transfer funds to 0x0000…0000, is it a bug if the funds are actually transferred? It’s the role of dev tooling to identify such.

![](https://ethresear.ch/user_avatar/ethresear.ch/ghasshee/48/3904_2.png) ghasshee:

> Why not abandon solidity and develop a new compiler ? Let’s try the research of formal verification and compiler theory!

Tezos created Michelson with this goal in mind: https://www.michelson.org/

What happened is that no one wanted to build using Michelson and they ended up needed to write compilers that target Michelson …

![](https://ethresear.ch/user_avatar/ethresear.ch/dexaran/48/12937_2.png) Dexaran:

> As for compilers & solidity - I think that the development of solidity was a mistake. It would be much better to take an already-existing programming language with existing and time-tested toolchain instead of developing a whole new one just for smart-contracts.

In many domains, people create Domain-Specific Languages to capture unique semantics of their domain and make it easy to read, write and maintain, the most successful one being SQL. There was already existing programming languages before SQL was introduced.

In 2019, I listed 40+ papers about DSLs for tensor and image processing here: [discussion: porting Halide to nim · Issue #347 · mratsim/Arraymancer · GitHub](https://github.com/mratsim/Arraymancer/issues/347#issuecomment-459351890), yet there was plenty of general purpose languages that could fit the bill. And since then there are many more that were created, in particular MLIR, by the creator of LLVM, who thought that LLVM IR, despite time-tested toolchain, felt that allowing “dialects” and each domain to represent their unique characteristics was the way forward. https://mlir.llvm.org/

The fact that Solidity has deficiencies does not mean we should throw the baby with the bathwater.

The authors of one of the largest piece of compiler and language infrastructure out there are embracing domain specific languages stack, tuned to the problems the domain faces and that there is no one size fits all. Why are we not embracing this as well?

---

**ghasshee** (2023-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/dexaran/48/12937_2.png) Dexaran:

> I’m very skeptical about formal verification. It is not possible to “formally verify” the correctness of the logic in any sensible way.

Have you already tried Coq proof assistant?

There are many ways to formally verify the logic.

We can classify them by two classes, synthetic ways and analytic ways. Coq is a synthetic verifier of program correctness depending on curry howard correspondence, while analytic verifier depending on some Logics such as LTL and CTL.

As [@mratsim](/u/mratsim) noted, we could develop DSL e.g. such that we could only allow inductive data types (which is “noetherian” and we can “guard” the overflows of the datatypes), or that we could pose some other limitations on it.

I am still trying to research from the both viewpoints.

I think there is a way.

---

**ghasshee** (2023-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> Tezos created Michelson with this goal in mind: https://www.michelson.org/
>
>
> What happened is that no one wanted to build using Michelson and they ended up needed to write compilers that target Michelson …

I believe tezos languages are much healthier than EVM community’s ones.

I would ask you too, “Have you already tried Coq?”.

There is a known good general purpose language called ocaml while it is not solely enough to achieve formally verified programs; it needs help of Coq extraction on top of it.

I would ask, “EVM has the CODECOPY opcode and thus we could pass functions from one cotract to another. We could development framework for handling higher order functions in a good manner. Is there already such a developped framework?”

And I would like to know more concretely why you mentioned SQL in the context of smart contract language development.

---

**MaxC** (2023-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/ghasshee/48/3904_2.png) ghasshee:

> There is a known good general purpose language called ocaml while it is not solely enough to achieve formally verified programs; it needs help of Coq extraction on top of it.

Have you checked out the move programming language and prover?

---

**ghasshee** (2023-11-27):

No, I haven’t heard of move language. Would you mind introducing us what is interesting technically and concretely?

