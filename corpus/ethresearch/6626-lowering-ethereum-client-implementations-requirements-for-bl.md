---
source: ethresearch
topic_id: 6626
title: Lowering Ethereum client implementations requirements for black-box testing
author: chfast
date: "2019-12-12"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/lowering-ethereum-client-implementations-requirements-for-black-box-testing/6626
views: 1601
likes: 2
posts_count: 5
---

# Lowering Ethereum client implementations requirements for black-box testing

# Lowering Ethereum client implementations requirements for black-box testing

(The title is my interpretation)

[@AlexeyAkhunov](/u/alexeyakhunov) proposed some time ago to drive black-box testing by p2p network interface instead of RPC methods. This eliminates the need of having RPC module in an Ethereum client implementation.

I also know this was recently discussed with [@Andrei](/u/andrei) and he proposed (my interpretation) something in functionality similar to RPC but without inter-process communication — i.e. API / FFI allowing to use an Ethereum client as a shared library.

To my understanding, Hive requires a combination of CLI interface and RPC.

Personally, I don’t see using network interface as a practical solution here. The behavior is allowed to differ between implementations and preparing good testing scenarios would be difficult. Moreover, the behavior is not required to be deterministic. And further debugging may be not easy. But I’m not network expert, looking for other’s comments.

## Replies

**lithp** (2019-12-12):

My intuition is that this won’t provide a big win, but probably I’m misunderstanding the proposal? It doesn’t matter whether you’re talking to the client over RPC or over a network socket, either way it needs to implement the protocol you’re using to talk to it. And since clients already need to implement RPC it seems like adding a protocol for testing could only make it harder to write a client, implementors now have one more protocol to implement!

---

**chfast** (2019-12-13):

To my understanding, the whole point is to eliminate the RPC as something a node has to mandatory expose.

---

**gumbo** (2019-12-16):

> And since clients already need to implement RPC it seems like adding a protocol for testing could only make it harder to write a client, implementors now have one more protocol to implement!

Unfortunately the reality of the current approach of retesteth is that it heavily relies on [a number of non-standard esoteric RPC methods](https://github.com/ethereum/retesteth/wiki/RPC-Methods#test), which represent kind of an additional protocol anyway. So retesteth support is not free at all, these methods might be really difficult to implement for some client designs. For example for geth it seems the only reasonable way to support retesteth was to do it in a kind of an isolated module, that doesn’t really operate in a normal geth functioning mode, so can’t really be used to test geth.

One of the motivations of retesteth project was to become a universal test runner for all of the clients, yet no client team has adopted retesteth for this.

At the same time, it seems that all of the clients have their own implementation of the test driver, probably somewhat coupled with the consensus code. Our proposed idea here is to standardize this consensus code ↔ test driving code interaction via a stable API.

---

**gumbo** (2019-12-16):

Additionally, my other concerns about both testing via RPC and testing via devp2p:

- I don’t like the performance overhead of several interpocess/network calls for each test, we have tens of thousands test to run, we should better make it efficient
- I’m concerned even more about the complexity of any such multi-process system compared to inegrating something as a library. It can be difficult to develop this system, can be painful to setup for a user, and when something goes wrong, you have to first figure out which of the many moving parts was the reason, in which part of the stack etc.
- devp2p shouldn’t be coupled with consensus code any more than RPC is. So the logic “RPC shouldn’t be a required component of a client” applies similarly to devp2p, I think. For example, implementors of the new client should be able to start running consensus tests before they have devp2p implementation ready.
On a way to a better modularized client architecture, testing can be one such module, as a test driver decoupled from the consensus code and possibly reusable across different clients.

