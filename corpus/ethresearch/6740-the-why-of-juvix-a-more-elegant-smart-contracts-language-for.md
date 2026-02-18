---
source: ethresearch
topic_id: 6740
title: The Why of Juvix – A more elegant [smart contracts] language for a more civilized age
author: awasunyin
date: "2020-01-08"
category: Applications
tags: []
url: https://ethresear.ch/t/the-why-of-juvix-a-more-elegant-smart-contracts-language-for-a-more-civilized-age/6740
views: 2252
likes: 7
posts_count: 5
---

# The Why of Juvix – A more elegant [smart contracts] language for a more civilized age

After many months of R&D, starting today we will publish more blogposts and articles about the Juvix project and its research. Just wanted to share with the ETH research community in case there are people interested in the topic of secure smart contract design / languages.

---

In addition to validation and protocol development, in the past several months Cryptium

Labs has embarked upon a new project: research & development of a novel smart contract language, Juvix. Juvix is designed to address the problems that we have experienced while trying to write & deploy decentralised applications and that we observe in the ecosystem at large: the difficulty of effective verification, the ceiling of compositional complexity, the illegibility of execution costs, and the lock-in to particular backends. In order to do so, Juvix draws upon and aims to productionise a deep reservoir of prior academic research in programming language design & type theory which we believe has a high degree of applicability to these problems.

There should be a substantial bar to meet before electing to write a new language. After investigating many simpler approaches and developing distributed ledgers & smart contracts ourselves, we’ve decided that this bar, for the use-case of smart contracts on public ledgers, is met — there are many unique, fundamentally difficult problems which can be convincingly solved at the language level, but only by designing & engineering a language and

compiler stack from scratch.

This post, the first part of a two-part series, explains the background of considerations and requirements that motivated us to design a new language.

---

You can find the full article here: https://research.cryptium.ch/the-why-of-juvix-part-1-on-the-design-of-smart-contract-languages/

## Replies

**dankrad** (2020-01-11):

I think that improving the state of smart contract languages and enabling formal verification is absolutely essential for Ethereum, so great to see some work on this. In you Medium article, you state:

> Many of the observed mistakes & bugs in smart contracts are not specific to the blockchain use-case at all — they are just common errors made in imperative languages by programmers everywhere: unintentional side-effects, type mismatches, and failure to handle exceptions or unexpected states.

I would be interested to actually see if that’s true. I understand that the DAO bug was due to an unintended side effect, nevertheless, a side effect (a transfer of money) was actually intended. In Haskell you might have passed a Monad to the function. It would not have prevented the bug.

I know there are many lovers of functional languages out there, but it just hasn’t turned out to be very practical for most applications. Adding some functional elements to imperative languages has been successful, but starting from a functional language not. I would be interested to see any *specific* arguments why smart contracts would be different. Formal verification is one argument, but I think it probably won’t be strong enough (I doubt all smart contracts will be formally verified).

Also, I think to get more feedback here, it would be best if you would just link to some example smart contracts written in Juvix, from very basic examples to slightly more complex ones (like ERC20 and a DAO). That way people can actually judge what it would feel like to write in it.

---

**cwgoes** (2020-01-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I would be interested to actually see if that’s true. I understand that the DAO bug was due to an unintended side effect, nevertheless, a side effect (a transfer of money) was actually intended. In Haskell you might have passed a Monad to the function. It would not have prevented the bug.

Indeed, encapsulating effects in a monad alone would have been insufficiently precise to capture the intended semantics (& prevent the bug). Instead, Juvix will use an effects system similar to that of [Idris](http://docs.idris-lang.org/en/latest/effects/index.html) and [F*](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/08/fstar.pdf), which can utilise the underlying dependent type theory to precisely capture semantics - such as by constraining the “transfer”/“send” effect (in this case) to a bounded amount and particular user.

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> I know there are many lovers of functional languages out there, but it just hasn’t turned out to be very practical for most applications. Adding some functional elements to imperative languages has been successful, but starting from a functional language not. I would be interested to see any specific arguments why smart contracts would be different. Formal verification is one argument, but I think it probably won’t be strong enough (I doubt all smart contracts will be formally verified).

Functional languages do have some industrial success in cases I would consider similar in requirements to smart contracts, such as in [proprietary trading](https://blog.janestreet.com/why-ocaml/), [banking](https://www.youtube.com/watch?v=hgOzYZDrXL0), and [network security](https://github.com/awakesecurity) - but I agree, formal verification alone will not be a sufficient draw - not all smart contracts will be (or need to be) formally verified, and the requirements in programmer expertise & time will be significant for the foreseeable future.

We think there are two other notable advantages of this language design which are independent of formal verification.

First, strong type-systems & functional purity can reduce the costs of developing intricate contract logic, especially logic dependent on the correct composition of many different contracts (some of which are perhaps developed by different entities), since the types of functions, storage, etc. constrain what the program can do and free the programmer from reasoning about potential side effects or unintended control flow. This is hard to put a number on, but it is true in our experience (I have also [written complex logic in Solidity](https://github.com/wyvernprotocol/wyvern-v3)).

Second, resource consumption of contracts can be calculated & bounded ahead of time - see [this issue](https://github.com/cryptiumlabs/juvix/issues/45) for discussion of the method - essentially, terms can be annotated with a symbolic cost (either a constant or some equation, which could depend on the inputs to a contract call thanks to the dependent typesystem), costs can be composed in a monad, and the Juvix compiler can check these annotations at compile-time - thus allowing the gas costs for a particular contract call to be calculated prior to executing the call. This provides greater legibility of execution costs to programmers, and can eliminate the overhead of runtime gas-metering entirely if the execution environment integrates the typechecker (this could be possible with an Eth2 execution environment programmed to do so).

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Also, I think to get more feedback here, it would be best if you would just link to some example smart contracts written in Juvix, from very basic examples to slightly more complex ones (like ERC20 and a DAO). That way people can actually judge what it would feel like to write in it.

Juvix is not yet production-ready - just sharing here for early feedback - we will definitely provide such examples once we have them in a user-ready form; I agree that they would be more easily digestible.

---

**cwgoes** (2020-01-22):

We’ve released the second part of this two-part post series, which enumerates the various theoretical ingredients in Juvix that we think will enable it to meet these challenges, describes the current state of specification and implementation, and provides a list of further resources & instructions should you wish to learn more.

You can find the full article here: https://research.cryptium.ch/the-why-of-juvix-ingredients-architecture/.

---

**DaniellMesquita** (2020-01-23):

I were going to create a post with a simple proposal for a Rust-based new version of Solidity with focus on security, then I saw this topic in the start page.

So, Juvix shares properties with Rust?

