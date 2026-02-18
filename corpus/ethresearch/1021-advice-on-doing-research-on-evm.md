---
source: ethresearch
topic_id: 1021
title: Advice on doing research on EVM?
author: kladkogex
date: "2018-02-08"
category: EVM
tags: []
url: https://ethresear.ch/t/advice-on-doing-research-on-evm/1021
views: 2664
likes: 12
posts_count: 12
---

# Advice on doing research on EVM?

We are planning to do some research on EVM at my company, such as adding new opcodes related to vector computations and deep learning. We have an engineer who just has been assigned to this task and starting to learn.

1. I wonder whats the best way for someone that does not know all bells and whistles of the current EVM impelementation to learn the basics and  start “tweaking it”.
2. We are looking at at a Python-based EVM implementation. Would py-evm be a good starting point, or there are simpler implementations?
3. What would a good, time-saving  development strategy to run py-evm off-chain and start tweaking it? Are there any tools/scripts/documentation within py-evm that can help?

## Replies

**hwwhww** (2018-02-08):

IMO I’d recommend tracing code on [py-evm](https://github.com/ethereum/py-evm) + comparing with [yellow paper](https://github.com/ethereum/yellowpaper).

No such documents for `py-evm` right now, a good way to start is using [eth-tester](https://github.com/ethereum/eth-tester), you can choose the “backend” between `py-evm` and `pyethereum`. ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=9)

---

**kladkogex** (2018-02-08):

Thank you :-))

I also found this talk [on plugging in different EVM implementations](https://www.youtube.com/watch?v=fps6cSoJxpQ)

It seems a bit strange though that they are using essentially  C-headers as a compatibility tool, having the industry trends one would expect more of a microservice API approach in this case …

---

**rumkin** (2018-02-08):

The best way for me to learn something is to implement it yourself. It helps to understand all caveats and to feel the code better. It’s not required to implement every behaviour but a parts. Also it’s very helpful to read and understand source code. It’s the only way to became a pro in short term.

---

**kladkogex** (2018-02-08):

The problem is how to make it compatible ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

EVM probably has zillions of cornercases not included in the yellow paper, so if we have our own thing, what the chance of it being really compatible ?)

On the other hand if we take a production EVM and slowly inject our stuff into it we will be guaranteed to have all the bugs the production EVM has, so we will get really really  compatible ![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)![:rofl:](https://ethresear.ch/images/emoji/facebook_messenger/rofl.png?v=9)

It seems that the EVM has this [forks directory](https://github.com/ethereum/py-evm/tree/master/evm/vm/forks), which specifies alternative opcodes, so if we want to introduce an opcode,  then we just need to add another fork there …

---

**jamesray1** (2018-02-08):

There’s also K-EVM which is used for verifying the EVM. But the Yellow paper is a good place to start, and Py-EVM is easiest to read and play around with.

---

**yhirai** (2018-02-09):

I have a list for you https://github.com/pirapira/awesome-ethereum-virtual-machine#specification

py-evm sounds good.

---

**gumbo** (2018-02-12):

Speaking of vector computations - SIMD opcodes proposal might be of interest to you https://github.com/ethereum/EIPs/issues/616

Also the implmentation in cpp-ethereum’s EVM https://github.com/ethereum/cpp-ethereum/pull/4233

---

**kladkogex** (2018-02-12):

Andrei - thank you, this is interesting.

So we basically apply this patch, recompile it and get the SIMD functionality.

Do you think that the SIMD functionaly has a chance of going  into an official release anytime soon?

---

**gumbo** (2018-02-12):

It’s merged into `develop` branch of cpp-ethereum, so theoretically to make it work you need only to build with `EIP_616` flag enabled. (and cpp-ethereum doesn’t have official releases lately)

---

**jamesray1** (2018-02-13):

[@yhirai](/u/yhirai) I put your list in the Wiki.

https://github.com/ethereum/wiki/wiki/Ethereum-Virtual-Machine-(EVM)-Awesome-List

---

**jamesray1** (2018-02-26):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The problem is how to make it compatible

You can use [GitHub - ethereum/tests: Common tests for all Ethereum implementations](https://github.com/ethereum/tests).

