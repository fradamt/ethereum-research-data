---
source: ethresearch
topic_id: 16186
title: Priority fee should be burned for reverted transactions
author: michaelscurry
date: "2023-07-25"
category: Economics
tags: []
url: https://ethresear.ch/t/priority-fee-should-be-burned-for-reverted-transactions/16186
views: 1786
likes: 1
posts_count: 3
---

# Priority fee should be burned for reverted transactions

Problem:

Currently, gas fees for reverted transactions are distributed in the same way as regular transactions. This is to discourage spamming of the network. However, this hurts normal users in high load situations (e.g. NFT mint, Uniswap trade) and is a poor user experience if their transaction is reverted since often the gas fee lost is substantial. I’ve personally often encountered a scenario where my txn is stuck in a mempool for setting the gas fee too low and will revert due to being past a deadline. Then I have to submit a no-op txn to save the gas.

Proposal:

Instead of sending the priority fee to the validator, the priority fee should be burned or a percentage thereof. This would discourage the validator from including a transaction that they know will revert, and *should* still deter spam txns since the spammer would still have to put funds at risk.

Curious if you think this would still be sufficient to deter spam attacks.

## Replies

**barnabe** (2023-07-26):

The issue I see is that burning the priority fee is not OCA-proof (in the sense of [Tim Roughgarden’s definition](http://timroughgarden.org/papers/eip1559.pdf)), as in, if a user wants to express priority fee p, and part of this fee is burnt, there is an incentive for the block producer and the user to organise off-band to settle some priority fee away from the protocol’s view. Of course this infrastructure is not that easy to put in place (it would probably rely on some of the existing builder infra), but there may be a preference to not enshrine mechanisms that are gameable in theory.

Also, looking ahead, if proposals such as mev-burn are enshrined, burning the PF would not deter a validator from including the transaction, but in fact they would be incentivised to do so as this would maximise the burn.

---

**michaelscurry** (2023-07-26):

[@barnabe](/u/barnabe) thanks for the reply and including the research as well, I will need some time to digest that so may change my mind after reading that. My immediate thought though is that I am not recommending *always* burning the priority fee, but only when transactions are reverted. It wouldn’t be rational to me that a user and block producer would conspire to settle a reverted transaction away from the protocol.

As for MEV-burn, whatever is burned due to a reverted txn shouldn’t be counted as MEV.

