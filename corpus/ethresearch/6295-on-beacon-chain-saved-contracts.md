---
source: ethresearch
topic_id: 6295
title: On-beacon-chain saved contracts
author: vbuterin
date: "2019-10-11"
category: Sharded Execution
tags: []
url: https://ethresear.ch/t/on-beacon-chain-saved-contracts/6295
views: 5552
likes: 6
posts_count: 18
---

# On-beacon-chain saved contracts

This is NOT a new idea; it has existed in discussions for a long time. However, it seems useful to have a post explicitly discussing this.

In a sharded blockchain, and especially a *stateless* sharded blockchain, there will be many pieces of code (or even non-code data such as cryptographic constants) that are shared between many use cases. This includes cryptographic algorithms, smart contract wallet implementations, token contract implementations, etc. To prevent witness sizes from getting too large as a result, we can introduce a functionality where such pieces of code can, at a high cost (eg. 1 ETH per kB), be saved on the beacon chain, and then referenced from shard chain blocks by index.

We would do this by introducing a new beacon chain transaction type, `newCode: [code, validator_index, signature]`, which could be created by a fully inactive validator. This transaction type would be processed as follows:

1. Verify the signature
2. Subtract BEACON_CODE_BYTE_FEE * len(code) from the validator’s balance (if the validator has not enough balance, this fails)
3. Add (code, current_slot_number) to an in-state list of codes: List[Tuple[Bytes, Slot]]

`BEACON_CODE_BYTE_FEE` would be set to a high amount, eg. 0.001 ETH per byte.

Shard execution would have access to an opcode `execute_beacon_code(index, data)`, which could execute the program with the given `index` with the given `data` and return the output (we save the activation slot so that in fraud proofs we know whether or not the code existed at the time a block was executed). We expect all nodes to have access to the beacon chain, so the code is information that they can access.

This is a very useful feature in light of many features of the eth2 roadmap:

- Account abstraction, where signature verification algorithms need to be part of every piece of account code
- ERC20 tokens already being abstracted
- Contracts frequently needing to be yanked across shards, passing all contract code in through a receipt
- The general move to witness and receipt-based workflow, where every byte of data read needs to be part of a block

In all cases, large pieces of code could be replaced by a simple 4-byte index of which beacon code to use.

### Possible extensions

- Allow beacon codes to be removed, eg. by storing who deposited them and allowing withdrawal with an 8-month delay if the depositor agrees (the depositor address could be changed to 0 to signal a permanent guarantee of non-removal)
- Make the fee dynamic, eg. targeting a specific beacon chain state growth rate

## Replies

**DB** (2019-10-11):

This proposal has a free parameter, BEACON_CODE_BYTE_FEE, that is decided centrally and not by the market. A rate for such data accumulation can be set, and similarly to EIP-1559, increase or decrease BEACON_CODE_BYTE_FEE based on actual use (can set a high floor for minimizing beacon usage). This still isn’t optimal, and can be improved by letting validators change the desired data accumulation rate (similar to gas limit today).

---

**SamW** (2019-10-12):

How does this interact with execution environments? Would EEs be able to make similar calls? Would a contract written for one EE be able to call into beacon code for a different EE?

---

**vbuterin** (2019-10-12):

Contracts on the beacon chain would not be “for” any specific EE. Any EE could access them.

---

**vbuterin** (2019-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/db/48/1527_2.png) DB:

> This proposal has a free parameter, BEACON_CODE_BYTE_FEE, that is decided centrally and not by the market. A rate for such data accumulation can be set, and similarly to EIP-1559, increase or decrease BEACON_CODE_BYTE_FEE based on actual use (can set a high floor for minimizing beacon usage). This still isn’t optimal, and can be improved by letting validators change the desired data accumulation rate (similar to gas limit today).

The equilibrium (price, quantity) is decided by the intersection of the supply and demand curves. The demand curve is set by the market, the supply curve is set by the protocol. It could be a vertical supply curve (fix quantity, market sets the price) or it could be a horizontal supply curve (fix price, market sets the quantity) or even diagonal (fix price / quantity, markets sets price * quantity), but there’s always something that’s fixed.

I suppose we could use arguments from http://ethresear.ch/uploads/default/original/2X/1/197884012ada193318b67c4b777441e4a1830f49.pdf to determine what is more important to fix. Given that support for constrained devices is a goal, it does feel like there is value in setting a limit on storage size, or at least pushing for predictability. So that would lend support for a more diagonal curve. I could actually see `price = quantity * k / (t - t0)` or even `price = (1+k) ** (quantity / (t - t0))` working pretty well.

---

**SamW** (2019-10-13):

So would these beacon contracts have to be compiled to WASM?

---

**jvluso** (2019-10-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> (eg. 1 ETH per kB)

This should be 1 ETH per kB per kBlocks, right? Each element of the list will produce perpetual costs for all clients for as long as it remains available in the list. Therefore these should be leased, not owned.

---

**DB** (2019-10-14):

You can do rent only in a stateful protocol. This is problematic, because no other party will be able to use it in smart contracts, fearing it won’t be there in the future.

---

**DB** (2019-10-14):

I think the supply needs to take into account the usage over a period, and not just the last block (unless I’m misreading the notation and it’s already there). As a user I care more about the total space I need to store for the beacon chain and less about the size of a single block.

Ideally, the supply side needs to be (somewhat) adjustable by network participants. One could argue that the validators represent the interests of the network/all users, but this is a weak argument. Maybe this question can wait until this is an actually a problem and we have usage data.

---

**vbuterin** (2019-10-15):

I think the fee should be one-time for permanent storage, and we can make the fee high to compensate. We really do want it to be possible to rely on these beacon chain contracts as permanent fixtures.

---

**MihailoBjelic** (2019-10-20):

I thought the original idea was for EEs to be deployed/published on the beacon chain, so every shard can access them? This could also potentially give some guarantees with regards to immutability of (some of the) EEs.

---

**Mikerah** (2019-10-20):

If the beacon chain stored all the EEs, wouldn’t the beacon chain be more “bloated” than it needs to be? Hence the rationale for this proposal by Vitalik.

---

**vbuterin** (2019-10-20):

The beacon chain would store EEs *and* this type of contract. I don’t think it would be that bloated; 100 MB is plenty enough to store most code that people would want to commonly use.

---

**Mikerah** (2019-10-20):

If that is the case then what are your thoughts on [@loredanacirstea](/u/loredanacirstea)’s proposals for a master shard for caching shard data that can easily be retrieved later? Here’s the [post](https://ethresear.ch/t/a-master-shard-to-account-for-ethereum-2-0-global-scope/5730/7) that I’m referencing.

---

**vbuterin** (2019-10-20):

What’s the concrete difference between that proposal and just using the beacon chain for storing contracts/data that users want to store?

---

**Mikerah** (2019-10-20):

It’s not exactly clear what the ramifications are of that proposal vs just storing everything on the beacon chain. Would this be a thing we can prototype in scout and/or reason through?

---

**DennisPeterson** (2019-10-28):

Seems the differences are (1) data on the “master shard” is always just a copy of data on shard; it’s used only as cache, and (2) all data accesses check the cache first, and then go to the shard if not in cache.

I think state rent would be fine this way. Cache accesses could pay towards rent, so things naturally fall out of cache if not used enough. It might even be possible to use a mechanism like 1559, to gradually adjust the rent fee and target a particular amount of storage.

---

**NunoSempere** (2020-01-24):

Under a rent mechanism, you could also have the social norm under which the rent of highly valuable code is paid by the ETH foundation, or better yet by another governance mechanism, where perhaps the original sponsor is rewarded.

I dislike the option of a one-time fee, because of clutter; it seems likely that over the long term you’d end with stale code, the equivalent of old fortran code which you can’t change and can’t delete… An (optional) updating mechanism would also be useful, but would pose security concerns.

