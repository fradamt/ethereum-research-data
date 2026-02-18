---
source: ethresearch
topic_id: 10234
title: DAI-like stable asset pegged to BASEFEE (post EIP-1559)
author: shadycoderjeff
date: "2021-08-02"
category: Applications
tags: []
url: https://ethresear.ch/t/dai-like-stable-asset-pegged-to-basefee-post-eip-1559/10234
views: 1410
likes: 4
posts_count: 5
---

# DAI-like stable asset pegged to BASEFEE (post EIP-1559)

Hi Friends,

I wanted to seek feedback on designing a token, say $FEE, which is pegged to BASEFEE.

Motivation:

1. Hedge against varying BASEFEE with the expected demise of CHI/GasTokens (post EIP-3529)
2. Meta transactions are better price din BASEFEE
3. Growing demand for a stable coin which is not pegged to currencies of nation states (inspired by RAI and also several tweets by prominent thinkers)

Why is BASEFEE a good unit of account for motivation #3? Because BASEFEE always buys you a certain quantity of compute resource (can be considered a proxy to a certain kind of basket of goods).

Proposed design:

1. Users lock X ETH in a contract and mint Y BaseFeeTokens where X / Y >= C * BASEFEE, C is the collateralization ratio
2. Liquidation, redemption etc like Maker
3. BASEFEE can double/halve in 6 blocks, C needs to be large enough to cover liquidation window of N blocks

A big benefit of pegging to BASEFEE: No oracles needed anywhere, BASEFEE is available in the EVM directly.

Would be happy to hear thoughts of like-minded people around refining the design.

## Replies

**MicahZoltu** (2021-08-02):

The `BASEFEE` can be manipulated at a cost.  Whatever mechanism you have for tracking the base fee value you will need to make sure that it isn’t profitable for someone to manipulate the base fee in order to profit.  For example, open a highly leveraged position when the base fee is low, then block stuff for a while to drive the base fee up and sustain it as long as necessary to trigger the oracle update, then close out your position at a profit greater than the cost of block stuffing.

---

**Mister-Meeseeks** (2021-08-02):

Has anyone done modeling work on what the cost manipulating BASEFEE would be?

The cool thing about it is that it’s the first on-chain, manipulation resistant source of random bits that doesn’t rely on an external protocol. Up until now, the output of every other op code (e.g. block hash or tx hash) could be completely manipulated by miner or sender.

BASEFEE’s the only primitive whose output depends on a multi-block history. Therefore no single miner can control it. The least significant bits can obviously be manipulated within a single block. But the most significant bits would require coordination over a large successive number of blocks. It’d be cool to get formal bounds on how much manipulation resistant entropy we can use.

---

**MicahZoltu** (2021-08-02):

I wouldn’t classify it as random at all.  It is 100% manipulable by the *prior* block author.  For the high bits, you can bribe miners to leave blocks empty, or you can bribe stuff blocks full.  I don’t think anyone should be using BASEFEE for any kind of entropy.

---

**Mister-Meeseeks** (2021-08-02):

Thanks, Micah for pointing that out. You’re a lot more familiar with the low-level nuts and bolts of the EVM, so I’ll definitely defer to your judgement here.

