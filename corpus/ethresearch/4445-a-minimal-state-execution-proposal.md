---
source: ethresearch
topic_id: 4445
title: A minimal state execution proposal
author: vbuterin
date: "2018-12-01"
category: Sharding
tags: [execution]
url: https://ethresear.ch/t/a-minimal-state-execution-proposal/4445
views: 7303
likes: 6
posts_count: 6
---

# A minimal state execution proposal

The general goal of this post is to create a “layer 1” state execution framework that is maximally simple, and is intended to be used in practice together with considerable layer 2 infrastructure (ie. HLLs and smart contracts acting as standard libraries) on top; it is intended that different setups can compete with each other so there could be different types of contracts that work in very different ways, some roughly emulating ethereum 1.0-style contract interaction, others more UTXO-like, etc etc.

It assumes that there exists a VM called “EWASM” which takes as input code and data, runs the code, eventually exiting with a return value or an error code, and with us having the ability to specify a foreign function interface.

- There exists a global state value, TOTALFEE. By default, TOTALFEE is incremented by 1 gwei per block, but if desired more complex policies can be implemented.
- There exists one type of account, a contract. Each contract has a piece of code (a bytearray), and a piece of storage (another bytearray); its address is the hash of its initcode plus a salt (as in CREATE2). Contracts also store the TOTALFEE value at the last time they were modified (TOTALFEE_WHEN_LAST_MODIFIED).
- Contracts pay rent based on total size. That is, if a contract has stored TOTALFEE_WHEN_LAST_MODIFIED F1, and it gets modified when the global TOTALFEE is F2, the contract’s ETH balance is reduced by (F2 - F1) * (100 + len(code) + len(storage)), and its TOTALFEE_WHEN_LAST_MODIFIED is updated to F2. If the new balance is less than 0, the contract is deleted.
- There exists a special “poke” operation, with 0 gas cost but a limited number of calls per block, which acts as a no-op to some target account except that it counts as “modification”. This can be used to delete contracts that have not pay rent. In general, we rely on voluntary pokes by miners to clear out old accounts.
- Contract code is EWASM, with exposed operations READ_STORAGE, SET_STORAGE and CALL, the latter calling a contract on the same shard and sending a specified amount of ETH to it.
- There exists a contract at a specific address (eg. 0x10) on each shard, which returns environment data (eg. block number, block hashes, timestamp…)
- There exists a contract at a specific address (eg. 0x20) on each shard, which has two functions generateReceipt (which takes as input an amount of ETH, a target shard, a target address and calldata) and claimReceipt (which takes as input a Merkle branch). Calling these functions is how contracts talk to contracts on other shards.

---

Not yet specified: account abstraction schemes. There are ideas here that can still be debated (eg. store nonces or not).

Another possible feature: we add to a contract’s FFI another operation, “yank”, which deletes the contract and creates a receipt which triggers the creation of the contract with the same code and storage and ETH balance on another shard (see [cross-shard yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450)).

Another possible feature: DELEGATECALL, so libraries can easily be built.

---

A possible alternative to rent: a contract maintains a `TOTALFEE_TTL` value, and it can be destroyed if the current global `TOTALFEE` exceeds `TOTALFEE_TTL`. When a contract is touched it consumes extra G gas; `G * MINFEE` (see [this paper](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838) for the “minfee” concept) is added to the contract’s `TOTALFEE_TTL`.

---

The following can all be done at “layer 2” or otherwise without modifying this basic scaffolding:

- Sleep-wake mechanisms (see the original post for how this can be done as a layer 2)
- Cross-shard calls
- High-level-language schemes for storage, eg. this one, as they can be implemented by using smart contracts as data stores
- The ZEXE framework, and other smart contract frameworks that don’t work based on smart contracts the way we have them today
- Contracts that use Merkle trees for storage
- Contracts that use accumulators with non-inclusion proofs for storage

## Replies

**poemm** (2018-12-01):

This is a great start. As everyone knows, there are design interactions between state execution, the rest of Serenity, and WebAssembly subtleties, so this will be a great design problem. My personal goal is to optimize for scaling and simplicity.

> Contract code is EWASM, with exposed operations READ_STORAGE , SET_STORAGE and CALL

One elegant option is to do some things natively in Wasm. For example, if a contract’s storage is a linear bytearray, then there is a correspondence with Wasm opcodes

`READ_STORAGE` \leftrightarrow `i32.load`, `i64.load`, etc;

`SET_STORAGE` \leftrightarrow `i32.store`, `i64.store`, etc; and

`CALL` \leftrightarrow `call` or `call_indirect`.

---

**kladkogex** (2018-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> There exists a contract at a specific address (eg. 0x20) on each shard, which has two functions generateReceipt (which takes as input an amount of ETH, a target shard, a target address and calldata) and claimReceipt (which takes as input a Merkle branch). Calling these functions is how contracts talk to contracts on other shards.

For security, you probably should not be able to call a contract from another shard if it does not want to be called.  The way we do it at Skale, is in order to be called from a different chain, a contract needs to specifically implement a “receiveMessage” call with a particular signature. The typical signatures will be

receiveMessage(srcShardID, srcContractAddress, bytepayLoad, srcShardBlockID);

sendMessage(dstShardID, dstContractAddress, bytepayLoad);

Another important thing: both sendMessage and receiveMessage should automatically generate log events, which in case of sendMessage should include the return value of the function, even if receiveMessage fails, otherwise this thing is hard to debug.

Overall I think it is a reasonable scheme.

---

**jvluso** (2019-01-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> There exists a contract at a specific address (eg. 0x20) on each shard, which has two functions generateReceipt (which takes as input an amount of ETH, a target shard, a target address and calldata) and claimReceipt (which takes as input a Merkle branch). Calling these functions is how contracts talk to contracts on other shards.

Would it be possible to combine this functionality with the sleep/awaken mechanism so that by default a contract that gets deleted can be recreated with the same merke proof that `claimReceipt` uses?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> There exists a special “poke” operation, with 0 gas cost but a limited number of calls per block, which acts as a no-op to some target account except that it counts as “modification”. This can be used to delete contracts that have not pay rent. In general, we rely on voluntary pokes by miners to clear out old accounts.

One way we could make sure that miners do this is by making this operation count as negative gas so that they could claim more transaction fees if they participate. The overall gas limit would be lower to take this extra into account on average.

---

**vbuterin** (2019-01-04):

> Would it be possible to combine this functionality with the sleep/awaken mechanism so that by default a contract that gets deleted can be recreated with the same merke proof that  claimReceipt  uses?

Yep! See [Cross-shard receipt and hibernation/waking anti-double-spending](https://ethresear.ch/t/cross-shard-receipt-and-hibernation-waking-anti-double-spending/4748)

---

**naterush** (2019-02-08):

Another possible additional feature is having VM versioning from the get-go. Relevant discussion (from EIP-1283) from [here](https://ethereum-magicians.org/t/immutables-invariants-and-upgradability/2440) and [here](https://ethereum-magicians.org/t/remediations-for-eip-1283-reentrancy-bug/2434/).

Here’s one proposal:

- each contract stores an ID for the VM it uses. This can be stored in its code byte array or just as an extra field - and is immutable.
- there can be multiple VMs, each with a unique ID. Contracts are run by the VM that has the ID they store.

When introducing new VMs, which requires a hard-fork, we promise to not break the following invariants:

1. A contract is the only one that can edit its own storage.
2. When making a call, a contract can’t lie about its address or the amount of Ether it’s sending.

There might be more invariants we want to insist on, but the above 2 seem like a reasonable starting point. The idea is that a contract should expect *anything* at all to happen when they make a call to another contract - but the execution of the code in this contract will always work exactly the same as the day it was deployed.

I’m no expert in formal methods, but if these invariants could be represented in something like [K-Framework](http://www.kframework.org/index.php/Main_Page), then formal proofs could be given about these contracts operating correctly - without having to worry about what new virtual machines are introduced in the future.

---

At a first glance, this appears to add a bunch of unnecessary complexity. But it’s worth noting that any changes to the single “EWASM” VM pretty much introduce at least this level of complexity (and often it’s much worse).

It’s very likely that we will want to introduce new virtual machine semantics as compared to the first version of the “EWASM” VM. When we do this, it seems like our options are:

1. Make changes to the semantics of the existing VM.
2. Some form of VM versioning where contracts can communicate even if they are in different versions.
3. The same as above, except contracts running different versions cannot communicate.

The first option, as demonstrated by EIP-1283, can be very hard to reason about, and very dangerous. The third option is pretty much equivalent to introducing new shards that have different execution schemes - but this seems at least as complicated as and less powerful than option two.

