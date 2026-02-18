---
source: ethresearch
topic_id: 19621
title: Queue End Of Block Transaction OPCODE
author: MicahZoltu
date: "2024-05-23"
category: Execution Layer Research
tags: [mev]
url: https://ethresear.ch/t/queue-end-of-block-transaction-opcode/19621
views: 1843
likes: 3
posts_count: 5
---

# Queue End Of Block Transaction OPCODE

## Abstract

A new OPCODE or System Contract that allows queuing some piece of code with a well defined gas used that will execute at the end of a block.  If two transactions queue the same end-of-block code, it will only execute once.  Gas costs are covered with ETH in the calling contract.

## Motivation

This would enable things like block auctions, by allowing a bunch of people to submit transactions to swap some asset, and then they would all execute together via a block-auction at the end of the block in a way defined by the contract, rather than in a sequential order that they appear.  Each transaction would queue the end-of-block code execution.  If a single transaction does a swap on some pool, then the end-of-block execution would not change anything from today.  If multiple people submit swaps on some pool within a single block, then the contract can execute a block-auction rather than executing the swaps in the order they are received.  This allows the contract to get the best price for everyone and combat things like in-block front-running.  This does *not* address cross-block front-running/back-running, but that is far harder to execute than within-block front-running and sandwiching.

## Specification

Mostly TBD, but gas paid by the contract allows for cost sharing strategies between transactors (e.g., split costs and refund at end) and requiring a fixed gas usage for the end-of-block execution helps with solving the bin-filling problem introduced by delayed execution.

## Considerations

It could be useful to allow for specifying dependencies, so one contract could say “I want my end-of-block execution to run after this other contract’s end-of-block execution”.  Care would need to be taken to avoid circular dependencies, but this could be achieved by just asserting that if a circular dependency is detected then all contracts in the circle do not get their end-of-block execution.  This strongly encourages people to *only* depend on immutable end-of-block executors with fixed dependency trees.

## Replies

**shemnon** (2024-10-17):

I think this would be better suited as a system contract rather than an opcode.  Within the EVM there is no real way to interact with other transactions, and opcodes are entirely focused on items that can be reacted to later within the same call.

We are also moving towards removing as much gas awareness from opcodes themselves the system contract is a more sensible place to add gas awareness.  This facilitates things like L2 gas schedule updates (so ZK can charge appropriate rates for keccak, for example)

And if new features like multi-variable-gas are introduced then a system contract is easier to modify or provide a new version for than an opcode.

---

**MicahZoltu** (2024-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/shemnon/48/4204_2.png) shemnon:

> I think this would be better suited as a system contract rather than an opcode.

Wouldn’t a system contract require core dev buy-in on its behavior?  My hope with this is that anyone could queue an end-of-block transaction, not only entities with enough clout to convince core devs to do work.  Perhaps I’m misunderstanding what you mean by system contract here?

---

**shemnon** (2024-10-19):

An opcode requires core dev buy in too, and I would say is a higher bar because it impacts literally every L2 that wants to upgrade to that VM version.  A system contract also gives each chain the flexibility to do it’s own custom take on scheduling, since you are in effect interacting with the sequencer.

I don’t think it’s a good fit as an opcode because no opcodes interact with the transaction processing code at the moment.  The closest are the LOG opcodes, but that is plain output. Any operations are read-only and that is just the NUMBER opcode.  All other interactions with the block are currently inserted into the storage slots of system contracts.

My position is that opcodes should be reserved for in-transaction logic only.  Anything that crosses that barrier is no longer an VM concern but a concern for block production.  The more we can keep those two layers separate the cleaner the model will be. If I could turn back time I would take out the blob opcodes and make them system contracts.  The same with practically all the opcodes that transmit info from the block to the VM.

---

**MicahZoltu** (2024-10-20):

Ah, you are suggesting having a system contract that queues a system transaction, rather than an OpCode that queues a “regular” transaction?  I would be fine with that.  I have no specific preference of OPCODE over precompile/system contract, and the transaction being executed as a system transaction rather than a regular transaction seems fine by me (or a new type of transaction).

