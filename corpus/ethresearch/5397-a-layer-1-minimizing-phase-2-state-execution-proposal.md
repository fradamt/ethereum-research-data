---
source: ethresearch
topic_id: 5397
title: A layer-1-minimizing phase 2 state execution proposal
author: vbuterin
date: "2019-05-01"
category: Sharded Execution
tags: [execution]
url: https://ethresear.ch/t/a-layer-1-minimizing-phase-2-state-execution-proposal/5397
views: 4993
likes: 10
posts_count: 4
---

# A layer-1-minimizing phase 2 state execution proposal

![](https://ethresear.ch/uploads/default/original/2X/9/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://notes.ethereum.org/@vbuterin/HylpjAWsE?type=view)



    ![](https://ethresear.ch/uploads/default/original/2X/8/882285f3628ea3784835c306639dd8f62179a6d9.png)

###



# Phase 2 Proposal 1  ### Introduction  This document describes a proposal for modifications to the










Copying the introduction:

This document describes a proposal for modifications to the beacon chain, and definition of the shard state and shard state transition function, for phase 2 (state and transaction execution) of ethereum 2.0. The general ethos of the proposal is to have a relatively minimal consensus-layer framework, that still provides sufficient capabilities to develop complex frameworks that give us all of the smart contract capabilities that we need on top as a second layer. The first part of the document describes the framework; the second part gives a basic example of implementing in-shard ETH transfers on top of the framework.

The basic idea of the approach is that contracts as a base-layer concept exist only on the beacon chain, and ETH only exists on the beacon chain (ETH can be held by either beacon chain contracts [also called “precompiles”] or by validator accounts). However, shards continue to have their own execution and their own state. A transaction on a shard must specify which precompile it calls, and the in-shard state transition function executes the specific beacon chain precompile code using the transaction as data, with the code execution having the ability to read and write from a region of the state of any shard reserved for that precompile and issue receipts. It turns out that this provides sufficient functionality to allow an execution environment that supports smart contracts in shards, cross shard communication and all of the other features that we expect to be built using a beacon chain contract.

## Replies

**axic** (2019-05-02):

I have some questions regarding the processing design.

> exec(code, data) executes code with MAX_TX_GAS_LIMIT (tbd).

I assume “precompiles” are vetted before they get included in the state.

Q: What is the process of getting a precompile added?

Q: What kind of “precompiles” do you imagine to be added?

> executeCode(code: bytes, data: bytes) -> bytes : runs exec(code, data) as a pure function (except for the ability to use callPrecompile ) and returns the output

Q: Why is there a need to execute raw code? This is dynamic data and makes verification of the “precompile” much harder.

Q: Is this execution starting off with its own `MAX_TX_GAS_LIMIT` or whatever is left at the time of calling it?

> Each shard block would have a gas limit of N gas; transactions being applied in a block would consume gas from this pool.

Q: Is this gas limit the same as `MAX_TX_GAS_LIMIT`?

---

**axic** (2019-05-02):

Wrote up a potential translation of the execution engine API into WebAssembly: https://github.com/ewasm/design/issues/190#issuecomment-488726054

---

**vbuterin** (2019-05-03):

> I assume “precompiles” are vetted before they get included in the state.

Nope! BTW I just renamed “precompile” to “execution script” to clarify that these aren’t like eth1 precompiles. There’s two major use cases for execution scripts:

1. As the code that is used to execute top-level transactions.
2. As functions that can get called by other code, where those functions represent code that is expected to get executed many times by many different actors, and so benefits from being stored once in the beacon chain rather than in every shard and from being stored by clients in compiled form so it can get executed much more quickly.

> Q: Why is there a need to execute raw code? This is dynamic data and makes verification of the “precompile” much harder.

The execution scripts on the beacon chain are meant to be very few in number, perhaps a few thousand at most. There’s not enough space on the beacon chain to hold code for every user. So the way that user-level code would be stored is that it would be stored in storage slots on the shards, and then the execution scripts would handle the logic of “treat this storage data as contract code, treat this other storage data as contract storage, and execute the code with storage and tx data as input”.

> Q: Is this execution starting off with its own MAX_TX_GAS_LIMIT or whatever is left at the time of calling it?

Removed `MAX_TX_GAS_LIMIT` for the moment. The goal is that there is N total gas per block that gets assigned to transactions in that block; if that N gas runs out before all the transactions get processed, then the remaining transactions would either get skipped over or they would get processed with some minimum quantity of gas that lets them do basic operations but not more.

