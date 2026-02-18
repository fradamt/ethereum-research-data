---
source: ethresearch
topic_id: 7876
title: Precompiled contract for verification of ZKProofs
author: Giulio2002
date: "2020-08-19"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/precompiled-contract-for-verification-of-zkproofs/7876
views: 1905
likes: 5
posts_count: 6
---

# Precompiled contract for verification of ZKProofs

I was thinking about opening an EIP about a precompiled contract that verifies ZKProofs. The contract takes two parameters: `p`, the proof, `v_k` the verification key and `x`, the public input. the contract then proves `p` and `x` using `v_k`. This is already done in Zokrates’s Verifier contract. However, given the steady increase in gas price and the consequent increase in the popularity of ZkProofs in verifying transactions with the minimum amount of gas, I think it would be beneficial for simplifying the process of verification (solidity-development-side) and make it more efficient so that we could save some gas in the process of verification.

The code of the precompiled will be pretty much the same as the one in the Zokrates Verifier contract so it’s not something that is to be started from scratch.

Any thoughts?

## Replies

**barryWhiteHat** (2020-08-19):

So the core component of snark verifier is a pairing check and exponentiaions. This pairing check is also used in other places for example BLS signatures. So the reason that EVM inclludes this messy contract for Snark is to make it so that we can use these core components in other places.

I agree that its messy and difficult to use. I think that in future more thought being payed to making cleaner APIs may be required. But retrospective changes are probably unlikely.

---

**Giulio2002** (2020-08-19):

It’s true that a precompile about pairing checks already exist. However, I think that with the large adoptions that snark are having on ethereum, making a precompiled that add an extra layer will be eventually needed, both in terms of computations(gas usage) and in terms of promoting the use of ZkSnarks.

---

**vbuterin** (2020-08-20):

The problem is that there continue to be new zk snark protocols developed, and new versions of existing ones, so I just don’t see what long-term value enshrining a specific type of proof will have.

---

**Giulio2002** (2020-08-20):

I think that although new protocols will be developed in the future, as of now, ethereum is experiencing severe congenstion and people are now looking at these kind of protocols that can agevolate them in terms of gas. I think that, as of now, this kind of ZKProofs should be included because they are the most popular and most used across many projects such as [loopring.io](http://loopring.io) for example. It’s true that new protocols will be invented in the future but i don’t think that it will cause any harm in the long-term. Additionally, the alt_bn128 curve has its precompiled contracts even though in the future better curves will be invented, so i don’t see how this case is any different. It’s just a way to promote people to scale ethereum using ZkProofs by making them more accessible and more convenient.

---

**vbuterin** (2020-08-21):

The issue is basically that >99% of the computation cost of verifying a ZK-SNARK *is* the elliptic curve computations, so having elliptic curve computations as precompiles is sufficient. If the goal is convenience for developers, then that can be accomplished by eg. someone writing a software library and putting it up as a contract that anyone can call. That seems like it would have essentially the same effect for developers, no?

