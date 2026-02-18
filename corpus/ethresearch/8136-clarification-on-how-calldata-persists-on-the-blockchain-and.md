---
source: ethresearch
topic_id: 8136
title: Clarification on how Calldata persists on the blockchain and how Optimistic Rollups use it
author: ZkZak
date: "2020-10-20"
category: Layer 2
tags: []
url: https://ethresear.ch/t/clarification-on-how-calldata-persists-on-the-blockchain-and-how-optimistic-rollups-use-it/8136
views: 9302
likes: 15
posts_count: 11
---

# Clarification on how Calldata persists on the blockchain and how Optimistic Rollups use it

Hey all I have tried asking this on various other forums but haven’t gotten a clear answer.

So I see that a lot of optimistic rollup solutions say that they store the chain’s transaction data on Ethereum via “calldata” which is way cheaper in gas costs than contract storage (I understand this is due to the ever expanding State trie). Looking up how calldata works, it seems it is read-only memory slot for function arguments. But if it is memory that means it is non-persistent after the the function has completed thus the data wouldn’t be available for users to rebuild the chain if necessary.

Where is the Calldata stored in the blockchain after the transaction is complete? Is it in the transaction trie? Also for optimistic rollups a guess is that once a submit block function is initiated via a transaction, the transaction and calldata are not removed from memory until the function ends (after the the usual two 2 week finality period). Thus the calldata would available for anyone wanting to create the rollup state, and after the two weeks it can be removed from calldata as the fraud proof period is over. Is this correct?

Tldr; Basically where do I find the transaction data for optimistic rollups if I want to re-create the state of the child chain? Thanks!

## Replies

**barryWhiteHat** (2020-10-20):

Call data is stored as part of the eth chain history. If you want to validate the whole chain you need to have the call data so it needs to be available for a chian to be considered valid.

Miners could try and make this call data unavailable but that attack would be similar in difficulty to a 51% attack.

You can get the call data by running a full node.

---

**ZkZak** (2020-10-20):

Would the calldata be stored within the transaction trie then? If I was running a fullnode is that where I would search to find the calldata? I assume it avoids posting into the storage trie because avoiding state bloat is basically the purpose of rollups.

---

**vbuterin** (2020-10-21):

> Would the calldata be stored within the transaction trie then?

Yes.

---

**kladkogex** (2020-12-25):

Most people that run geth, run geth in fast mode including us at SKALE. Our validators also run geth in fast mode.

It is pretty hard to run a full node. We tried it a couple of times, and never were able to fully sync, so we ended up abandoning the idea.  I think very few people do it, and as a result user experience is unfriendly.  The same can be said about light client mode by the way,  we tried it a couple of times and  never could make it work.

We are researching using calldata in the near future (within the next couple of months),  especially once SLOAD becomes more expensive.  In our case submitting pieces of the state to the smart contract in calldata may lower gas costs as compared to storing the state in EVM.

The problem is, if we do it, every validator needs to run a full node, and, as I described above, this may cause lots of pain.

I think the best way to solve this problem is to introduce a “fast+” switch to geth that does the fast mode, plus downloads all transactions that were ever sent to a particular destination address.

---

**edmundedgar** (2020-12-26):

I may be missing something but doesn’t a `geth fast` sync already have all the blocks so it has all the calldata? Is the issue that it’s not efficient to query?

PS My `geth light` node works great, not sure what wasn’t working for you guys…

---

**kladkogex** (2020-12-28):

Oops looks like I made a mistake.

Fast mode download blocks  …

![](https://ethresear.ch/user_avatar/ethresear.ch/edmundedgar/48/2287_2.png) edmundedgar:

> PS My geth light node works great, not sure what wasn’t working for you guys…

Please post how exactly you run it, I will try it on my desktop …

---

**sina** (2021-01-06):

Small note for anyone who stumbles upon this, since it wasn’t immediately obvious to me:

The calldata isn’t just sent in a noop transaction-- it’s *merklized by the EVM* and the resulting root is stored in the contract’s storage. So any disputes that want to reference that calldata can do so via merkle proof with the root that the contract holds.

After that, the calldata isn’t available to the contract unless explicitly provided again by a disputer (with a proof to show its path to the stored root). So if you want to create a dispute, you’ll need to do some of the work the other replies are mentioning-- perusing the eth chain history. Note that the contract being able to merklize the data is a good guarantee of its availability (ie. since the whole network had to process that calldata), so this isn’t too bad.

The part that you’re asking about regarding the calldata being available for only 2 weeks isn’t relevant for current rollups running on eth1 IIUC. It may become relevant when the data availability is on eth2, but that domain is still a bit too in-flux to say for sure.

---

**MicahZoltu** (2022-01-06):

jaglinux:

> Then why using storage is costlier than calldata ?

It has to do with the way it is stored on disk.  Also it has to do with the guarantees made around its future availability.  Calldata is stored in an append only DB (essentially), which can (in theory) be put on a large but slow disk like a spinning disk, tape drive, etc.  The guarantees that calldata will be available to all clients indefinitely are also much weaker than the guarantees that state will be available indefinitely.  Historic calldata also cannot be accessed by the EVM directly, which is part of why it can be written to a slow disk rather than needing an high IOPS disk.

---

**sudeepdino008** (2023-07-07):

For what I understand, direct calls to contracts, have tx.data, which gets loaded into a special transient data location space called calldata, which can then be accessed by the callee.

Now a contract execution can call other contracts (internal txs). In this case, the caller would load the arguments into calldata location, and then execution is handed off to the callee. In such cases, the calldata is dynamically generated, and is transient (like memory, it’s removed once the execution is done).

So, calldata, like memory, provides a temporary working space for the purpose of loading function arguments. The cost of calldata persistence comes indirectly from a direct tx.data. In the other scenario of internal tx, the function arguments are runtime generated, and so the cost of storage in this case is somewhat intrinsic in the contract code (for example, if there is a contract constant that’s always passed to a calldata-based function call).

For the availability of calldata, one needs to execute the contract, and “trace” the calldata-based function calls. It’s not persisted explicitly in the blockchain.

---

**rachit77** (2023-12-28):

yes Calldata are stored in transaction trie

