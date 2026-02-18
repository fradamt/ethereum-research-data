---
source: magicians
topic_id: 1980
title: "EIP spotlight: Fee market change for ETH 1.0 chain"
author: ligi
date: "2018-11-22"
category: EIPs
tags: [wallet]
url: https://ethereum-magicians.org/t/eip-spotlight-fee-market-change-for-eth-1-0-chain/1980
views: 580
likes: 1
posts_count: 1
---

# EIP spotlight: Fee market change for ETH 1.0 chain

Sharing this here as I completely overlooked this one but could be great for wallet UX:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/1559)












####



        opened 07:15PM - 06 Nov 18 UTC



          closed 06:22AM - 29 Apr 19 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/8/89ac618501d77ed85e1ea0663718f590291e7737.png)
          vbuterin](https://github.com/vbuterin)










**The final standard can be found here: https://eips.ethereum.org/EIPS/eip-1559*[…]()*

******

### Motivation

Provide a concrete proposal for implementing the fee market proposed in https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838 on the current 1.0 chain.

See https://github.com/zcash/zcash/issues/3473 for more detailed arguments for why this is a good idea.

### Parameters

* `FORK_BLKNUM`: TBD
* `MINFEE_MAX_CHANGE_DENOMINATOR`: 8
* `TARGET_GASUSED`: 8000000

### Proposal

For all blocks where `block.number >= FORK_BLKNUM`:

* Impose a hard in-protocol gas limit of 16 million, used instead of the gas limit calculated using the previously existing formulas
* Replace the `GASLIMIT` field in the block header with a `MINFEE` field (the same field can be used)
* Let `PARENT_MINFEE` be the parent block's `MINFEE` (or 1 billion wei if `block.number == FORK_BLKNUM`). A valid `MINFEE` is one such that `abs(MINFEE - PARENT_MINFEE) <= max(1, PARENT_MINFEE // MINFEE_MAX_CHANGE_DENOMINATOR)`
* Redefine the way the `tx.gasprice` field is used: define `tx.fee_premium = tx.gasprice // 2**128` and `tx.fee_cap = tx.gasprice % 2**128`
* During transaction execution, we calculate the cost to the `tx.origin` and the gain to the `block.coinbase` as follows:
    * Let `gasprice = min(MINFEE + tx.fee_premium, tx.cap)`. The `tx.origin` initially pays `gasprice * tx.gas`, and gets refunded `gasprice * (tx.gas - gasused)`.
    * The `block.coinbase` gains `(gasprice - MINFEE) * gasused`.

As a default strategy, miners set `MINFEE` as follows. Let `delta = block.gas_used - TARGET_GASUSED` (possibly negative). Set `MINFEE = PARENT_MINFEE + PARENT_MINFEE * delta // TARGET_GASUSED //  MINFEE_MAX_CHANGE_DENOMINATOR`, clamping this result inside of the allowable bounds if needed (with the parameter setting above clamping will not be required).

### Further explanation

There is a MINFEE value in protocol, which can move up or down by a maximum of 1/8 in each block; initially, miners adjust this value to target an average gas usage of 8 million, increasing MINFEE if usage is higher and decreasing it if usage is lower. Transaction senders specify their fees by providing two values:

1. A "premium" gasprice which gets added onto the MINFEE gasprice, which can either be set to a fairly low value (eg. 1 gwei) to compensate miners for uncle rate risk or to a high value to compete during sudden bursts of activity. The MINFEE gets burned, the premium is given to the miner.
2. A "cap" which represents the maximum total that the transaction sender would be willing to pay to get included.

Ultra-short-term volatility in transaction demand or block times will now translate mostly into ultra-short-term volatility in block sizes instead of volatility in transaction fees. During normal conditions, fee estimation becomes extremely simple: just set the premium to some specific value, eg. 1 gwei, and select a high cap. If a transaction sender highly values urgency during conditions of congestion, they are free to instead set a much higher premium and effectively bid in the traditional first-price-auction style.












Thanks to ETHGasStation for making me aware of this (via this tweet https://twitter.com/ETHGasStation/status/1065717539689414657)

It could completely remove the need for a service like ETHGasStation and lead to better UX. Currently as [@owocki](/u/owocki) states in this thread the whole gas thing is one of the biggest UX hurdles. Hope this post can help shining some more spotlight on this - so perhaps we can have it in the hard-fork after constantinople.
