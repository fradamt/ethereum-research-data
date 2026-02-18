---
source: magicians
topic_id: 3918
title: EIP-1559 Go-ethereum implementation
author: i-norden
date: "2020-01-10"
category: EIPs
tags: [gas, eip-1559]
url: https://ethereum-magicians.org/t/eip-1559-go-ethereum-implementation/3918
views: 6854
likes: 19
posts_count: 22
---

# EIP-1559 Go-ethereum implementation

Hello everyone!

This thread will serve to extend the previous EIP-1559 discussions with a focus on the go-ethereum implementation provided by Vulcanize Inc.

That implementation can be found [here](https://github.com/vulcanize/go-ethereum-EIP1559)

Other relevant links:

[Updated EIP documentation](https://github.com/vulcanize/EIPs/blob/eip1559/EIPS/eip-1559.md)

[Previous discussion thread](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783)

[Skinny EIP-1559 thread](https://ethereum-magicians.org/t/skinny-eip-1559/3738)

[Ethresear.ch Post w/ Vitalik’s Paper](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838)

After incorporating feedback received here I can proceed to open a PR for the implementation and the EIP documentation updates.

Thanks!

## Replies

**edmundedgar** (2020-01-10):

Thanks for doing this. Aside from the transition part, in the final state, would you mind ELI5-ing the way the main parameters (TARGET_GASUSED, BASE_FEE etc) get set in the current proposal?

The EIP has a TARGET_GASUSED and a BASE_FEE, but the BASE_FEE is now in a header field, so is the idea that the miners are voting on BASE_FEE directly like they do with the current gas limit, and the TARGET_GASUSED is just a parameter the miners set to feed the implementation’s default method for telling their node how to vote? Or is something else meant by “BASEFEE  is maintained under consensus”?

---

**vbuterin** (2020-01-11):

Did you decide to make the basefee adjustment formula “just a suggestion”? I thought we had talked about this and decided to make it hard-coded to prevent miners from being able to individually push the fee up or down by a significant amount by adjusting the formula? Or is there some overriding rationale for making it just a suggestion?

---

**i-norden** (2020-01-12):

Hey [@edmundedgar](/u/edmundedgar) and [@vbuterin](/u/vbuterin) , thanks for the comments!

[@edmundedgar](/u/edmundedgar) `TARGET_GASUSED` is a constant that is used in the `BASEFEE` adjustment formula, it is the amount of gas we target to use and miners adjust the `BASEFEE` up or down depending on how the actual gas usage deviates from this value. Specifically, miners set a block’s `BASEFEE` as `PARENT_BASEFEE + PARENT_BASEFEE * DELTA // TARGET_GASUSED // BASEFEE_MAX_CHANGE_DENOMINATOR`, where `DELTA = PARENT_GASUSED - TARGET_GASUSED`.

The `BASEFEE` is maintained under consensus by the ethash engine. In the `verifyHeader()` method a header is invalidated if the `BASEFEE` increases or decreases relative to `PARENT_BASEFEE` more than the allowed amount (`PARENT_BASEFEE // BASEFEE_MAX_CHANGE_DENOMINATOR`).

[@vbuterin](/u/vbuterin) per your comment the above is not quite right. I will update the consensus engine so that the exact value from the basefee adjustment formula is enforced, not just an upper and lower bound on the value. The need for this is apparent, currently a miner could change their basefee adjustment algo to submit arbitrary `BASEFEE`s that are valid so long as they are within the upper and lower limits e.g. they could raise the `BASEFEE` by as much as `PARENT_BASEFEE // BASEFEE_MAX_CHANGE_DENOMINATOR` even if `PARENT_GASUSED` is below `TARGET_GASUSED`. That’s an oversight on my part, but a simple fix to make. Thank you for pointing it out!

---

**edmundedgar** (2020-01-12):

[@i-norden](/u/i-norden) Thanks, so to make sure this is clear, the proposal is that TARGET_GASUSED is hard-coded at 8 million and never changed, except by a future hard fork.

---

**i-norden** (2020-01-13):

[@edmundedgar](/u/edmundedgar) that is correct!

---

**vbuterin** (2020-01-13):

Any reason why 8m, and not the current max of 10m? Setting to the current max seems most sensible.

---

**edmundedgar** (2020-01-13):

Just a thought: It might be worth putting something about the change from miner voting to a hard-coded limit that’s only changed in hard forks in the abstract and the motivation section of the EIP; I think I understand the basic reasons why this is being done from the previous Magicians discussion, but it’s arguably a more significant change than the fee market reform that’s the subject of the EIP.

---

**i-norden** (2020-01-13):

[@vbuterin](/u/vbuterin) 8m is left over from when work began on this, before the gas limit increase to 10m. I simply missed that change. Will update to 10m now.

[@edmundedgar](/u/edmundedgar) that is a good point, I will update the EIP doc to be more explicit about this.

Thank you both!

---

**vbuterin** (2020-01-14):

Another change I would recommend is setting a hard per-transaction gas limit of 10m, arguably even set the per-transaction limit to 8m. Don’t want to set the precedent that yuge transactions are possible.

---

**i-norden** (2020-01-15):

[@vbuterin](/u/vbuterin) added a per-transaction gas limit of 8m as recommended ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**tvanepps** (2020-01-23):

Just curious, what are the next steps for moving forward with this EIP?

Will your team be presenting the updates to the spec on the Core Dev call tomorrow?

---

**i-norden** (2020-01-28):

Hi @tvanepp! Sorry for the delayed response.

We didn’t make it on the Core Dev call last Friday. The plan of action is to incorporate feedback from here and then move forward by opening a PR for the EIP doc and Go-ethereum implementation. I’ll go ahead and open those PRs at the end of the week if no more changes are recommended/requested here. A more code-focused review can occur on the Go-ethereum PR.

---

**i-norden** (2020-02-03):

Hi all!

The PRs [for the EIP doc](https://github.com/ethereum/EIPs/pull/2505) and [for the implementation](https://github.com/ethereum/go-ethereum/pull/20618) have been opened. I’ll continue to incorporate feedback received here. Thanks!

---

**Agusx1211** (2020-02-04):

I think that we should use the same constant for both GASTLIMIT and this new ‘TXGASLIMIT’, mostly because some smart contracts may assume that they can use the whole block for gas if necessary, this is sometimes used to detect out of gas exceptions on-chain.

---

**i-norden** (2020-02-04):

[@Agusx1211](/u/agusx1211) just to clarify, we should use the 16m `MAX_GAS_EIP1559 ` as the `TX_GASLIMIT`? Or the 10m `TARGET_GAS_USED`?

---

**Agusx1211** (2020-02-07):

IMO we should use the 16m (or 20m ?) `MAX_GAS_EIP1559 ` as the `TX_GASLIMIT`

---

**i-norden** (2020-02-07):

Thanks [@Agusx1211](/u/agusx1211)! One potential issue with this is that during the transition period during which both legacy and EIP1559 transactions are accepted the `MAX_GAS_EIP1559` is split between the two gas pools. For example, at the block that EIP1559 is activated 8m is in the legacy pool and 8m is in the 1559 pool. So a transaction to either pool with gas usage of `MAX_GAS_EIP1559` would be rejected. This would be the case until the EIP finalization block is reached and the entire `MAX_GAS_EIP1559` is available to the 1559 pool.

Perhaps the `TX_GASLIMIT` could be set to the portion of `MAX_GAS_EIP1559` available for processing that type of transaction at a given blockheight. But that will still cause issue for smart contracts that assume they can use the whole block for gas.

We’ve raised the `TARGET_GAS_USED` to 10m since that is the current gas limit, but I am hesitant to raise `MAX_GAS_EIP1559` to 20m. It was originally set to be 24m, but there were some concerns raised by Péter and in our Core Dev’s call about the ramifications of this ([EIP-1559: Fee market change for ETH 1.0 chain](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/45)).

---

**Agusx1211** (2020-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/i-norden/48/14424_2.png) i-norden:

> But that will still cause issue for smart contracts that assume they can use the whole block for gas.

Wouldn’t smart contracts read that the “whole block” is composed by the “portion of  `MAX_GAS_EIP1559`  available for processing that type of transaction at a given blockheight”?

If opcode 0x45 (GASLIMIT) returns the portion of the block available for processing it should be safe to allow TXs to reach the same limit, in that way we aren’t breaking the two implicit rules of the current chain A) A TX could use the totality of GASLIMIT and B) GASLIMIT can never be below the TX gas

Maybe I am missing the point

---

**i-norden** (2020-02-09):

Opcode 0x45 returns the gas limit value from the block header, after EIP1559 activation this value is the gas limit for the EIP1559 gas pool and the gas limit for the legacy gas pool is equal to `MAX_GAS_EIP1559` - this value.

Sorry for the confusion, the issue I brought up in my previous response still exists with where the per-tx gas limit is set right now (8m), e.g. just 1 block after EIP1559 activation the legacy gas pool will have less than 8m gas available for processing transactions.

---

**MrChico** (2020-02-15):

I’m thinking that it might be a good idea to introduce a check for monotonically increasing `tx.gasprice` in block validation along with this EIP.

While default miner software already orders the transactions of a block according to their gas price, there doesn’t seem to be any checks that miners running custom software adhere to this rule.

The assumption that higher gas price transactions will be executed before low gas price transactions is widespread in developing and interacting with contracts and is the default behaviour of client software. I don’t see any reason it why miners should be given the capability to order transactions as they see fit.

Transaction ordering is a highly sensitive matter, as demonstrated in [Flash Boys 2.0 by Phil Daian et. al](https://arxiv.org/abs/1904.05234) and I think we should limit miner privileges where we can. I think enforcing tx ordering by gas price would definitely increase the predictability of outcomes here.


*(1 more replies not shown)*
