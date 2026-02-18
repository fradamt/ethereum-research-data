---
source: magicians
topic_id: 21513
title: "EIP-7793: Conditional Transactions"
author: marchhill
date: "2024-10-30"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7793-conditional-transactions/21513
views: 821
likes: 29
posts_count: 34
---

# EIP-7793: Conditional Transactions

Discussion thread for [EIPs/EIPS/eip-7793.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7793.md)

> This EIP proposes to add a new transaction format for “conditional transactions”, that are only valid at a specified slot and index within the block. A new opcode TXINDEX is introduced to expose the conditional transaction index onchain.
>
>
> The proposal aims to improve support for encrypted mempools. Transactions in an encrypted mempool are ordered while the transactions are encrypted, before being decrypted and included onchain at the top of the block. If the builder does not respect the order when including the decrypted transactions then they could frontrun decrypted transactions. The new transaction type can be used to make this impossible; if a decrypted transaction is not included at the correct index, it will be invalid.

## Replies

**shemnon** (2024-11-01):

Could this be a precompile/system contract instead of an opcode?

I’d like to reverse the tide of consensus specific opcode entering into the EVM.

---

**marchhill** (2024-11-02):

Sure it could be, do you think this would make implementation less complex?

I’m not too sure what you mean by consensus specific as the tx index only depends on the execution payload.

---

**shemnon** (2024-11-04):

My concern is less about introspection and more about adding features in L1 that future L2s may not need, to keep the EVM as “modular” as possible.

Adding opcodes that reflect Ethereum’s specific consensus algorithm create baggage that other “ethereum equivalent” L2s have to manage.  Some are obvious, such as how to handle blobs in a L2 that doesn’t have sub-blobs: return zeros and otherwise handle the block like there were no blobs.

What we are doing with the beacon block root I think is the better way forward: surface it in the contracts instead of altering the VM when a new consensus feature is exposed.  L2s that don’t have a beacon block root don’t then have to alter the EVM to remove or alter an opcode.

---

**marchhill** (2024-11-05):

That’s a good point, will change to a precompile ![:+1:t5:](https://ethereum-magicians.org/images/emoji/twitter/+1/5.png?v=12)

---

**sbacha** (2024-12-04):

why not make this available as an OPCODE?

---

**shemnon** (2024-12-04):

It started out as an opcode.  I requested it to not be one based on the arguments found in [this comment](https://ethereum-magicians.org/t/eip-7793-txindex-precompile/21513/4). The EIP was then changed to be a precompile, along with the title of this thread.

---

**sbacha** (2024-12-15):

This has use cases beyond what the EIP proposes, this proposal pre-dates this suggestion even.

---

**Arvolear** (2024-12-15):

I think that will be a cool addition. However, have you analyzed the impact this has on MEV?

I mean, this EIP opens a handful of use cases, like:

- MEV priority-based transactions.
- Enforcing DEX swaps to not happen the first in the block.
- Cheaper reentrancy protection.
- Something else?

---

**sbacha** (2024-12-16):

you even get the ability to do pull based transactions easily and flashloans natively.

RSK has this opcode implemented already

---

**The-CTra1n** (2025-01-07):

Hey! I’ve been thinking about how this could affect MEV, but it feels like using an uninformed tx index without context of what else has happened in a block might make MEV protections based on tx index maniplutable.

Specifically, DEXs, loan protocols, etc. need to know specific states have been updated, and sometimes in specific ways, to protect against MEV e.g. oracle update, top-of-pool arbitrage, before they want to update. I’m not sure if tx index on its own provides enough context in this regard. Maybe you have something specific in mind?

Cheaper re-entrancy protection sounds cool, and not something I’m familiar with. How would tx index help here?

---

**Arvolear** (2025-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/the-ctra1n/48/14199_2.png) The-CTra1n:

> Maybe you have something specific in mind?

From the top of my head: a price oracle contract can save the `txId` during the update and the integration protocol may check that it is only called after `X` transactions have passed (or in a different block).

Don’t really know the benefit of this approach, however, it looks like an area worth exploring.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/the-ctra1n/48/14199_2.png) The-CTra1n:

> Cheaper re-entrancy protection sounds cool, and not something I’m familiar with. How would tx index help here?

Having actually thought about it, seems like I was a bit too excited about that one ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) . Transient storage pretty much solves all reentrancy gas-related problems. Apologies for the confusion.

---

**wjmelements** (2025-01-08):

I’m opposed to exposing the tx.index because it makes reordering transactions less practical. The main impact is reduced throughput for parallel processing whenever it is used. It therefore should be very expensive to discourage its use.

I also don’t see any real positive use cases. Perhaps it is because I don’t understand how the encrypted mempool would work. Is there somewhere I can read about it?

Lastly I think the precompile should return one word, 32 bytes, even though we don’t expect blocks to have that many transactions, to provide forward compatibility in case sequential blocks become obsolete in favor of some parallel architecture.

---

**marchhill** (2025-01-09):

Interesting, could you expand a bit on how you think txindex could be used for this? Also how is it used on rootstock?

---

**marchhill** (2025-01-09):

In the case of local block building, it can still be done efficiently with txindex. Maybe it makes things  more complicated for sophisticated block builders but I don’t see this as a big problem since they have lots of resources to throw at the problem. Also there may already be problems with parallelising block building due to the GAS opcode and state access.

In regards to encrypted mempools, the idea is to enforce with a smart contract that a transaction from the encrypted mempool must be included at the top of block or it will be invalid. This prevents frontrunning. I’ll post more about this in future and share it here.

If we filled a block with `UINT_MAX` basic transfers we would get a 90 terragas block, seems future proof to me but maybe I’m not thinking big enough ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12). I’m not sure what you mean by a parallel architecture, could you expand on that?

---

**sbacha** (2025-01-10):

It would enable contracts to check if two different calls are from two different tx’s, so that a contract could securely allow both the payment tx and the callback tx to occur within the same block.

> The basic idea is that instead of pushing and pulling tokens to each other, contracts transiently push and pull tokens into the transaction. You can consider these to be flash loan without an external contract calls.[1]

1. see https://github.com/ricobank/allow-spend-pattern ↩︎

---

**Arvolear** (2025-01-10):

Can’t wrap my head around it. How can you enforce the refund to be made?

I mean flash loans just revert if amounts mismatch.

---

**shemnon** (2025-01-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sbacha/48/4661_2.png) sbacha:

> It would enable contracts to check if two different calls are from two different tx’s, so that a contract could securely allow both the payment tx and the callback tx to occur within the same block.

Have you looked into using transient data?  First call leaves a “I was here” marker in transient data, second call validates the marker is here before doing whatever task was gated by needing both calls to be in one TX.

---

**marchhill** (2025-01-24):

[@shemnon](/u/shemnon) I understand that with EOF you are trying to minimise introspection. Could you tell me a bit about what kinds of introspection you are trying to minimise and whether that might apply to this or EIP or the related [EIP-7843](https://ethereum-magicians.org/t/eip-7843-slot-precompile/22234)?

---

**shemnon** (2025-01-24):

Two kinds principally: Code and Gas.

For code we don’t want bytecode going to or coming from any user accessable memory.  This saves space for optimizations like compiling the contract, either to a normal machine or a zk proving machine.  If we allowed it all contracts would have to bring their old code as data or (worse) have to have a way to interpret or compile new code on-the-fly.  Bringing in new contracts only as part of create transactions or as payloads in transactions allows those systems to handle the creation out-of-band.

For gas we want to make sure that the solution to any gas schedule change is to send more gas to your contract.  When you read gas you can hard code aborts based on available gas, and when you limit gas to downstream calls you prevent the tx from sending more gas to handle situations like SLOAD going up 10x.  accessLists were one solution but don’t scale outside of storage. The difficulty here is that there are legitimate use cases that it closes down (EIP04337 entrypoint contract), it remains to be seen if we need to allow limiting tx gas somehow or if we simply enshrine those use cases.  Out of the box solutions like requiring the gas amount to come from not-code but memory/storage/txdata may be the middle ground, but those solutions have not been discussed in any seriousness.

As for slot and txindex, neither one of those pieces of data is intrinsic to the EVM execution, but are metadata to the packaging of how the EVM execution occurs.  There are other consensus systems where these ideas don’t apply well, such as single-tx “blocks” (where the chain is strictly an ordering of TXes without checkpoints) and dag style execution (where ordering is only resolved for conflicts and “meeting” of data).  That is why for these two I prefer the data to be communicated via a system contract rather than being enshrined as an opcode.  This reduces the friction applying the EVM to more exotic consensus mechanisms future L2s may want to use.

---

**marchhill** (2025-01-27):

[@shemnon](/u/shemnon) cheers Danno that’s really helpful


*(13 more replies not shown)*
