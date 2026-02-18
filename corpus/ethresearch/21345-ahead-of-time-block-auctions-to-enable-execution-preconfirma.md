---
source: ethresearch
topic_id: 21345
title: Ahead-of-Time Block Auctions To Enable Execution Preconfirmations
author: irfanshaik11
date: "2025-01-01"
category: Layer 2
tags: [preconfirmations, based-sequencing, sequencing]
url: https://ethresear.ch/t/ahead-of-time-block-auctions-to-enable-execution-preconfirmations/21345
views: 5372
likes: 6
posts_count: 1
---

# Ahead-of-Time Block Auctions To Enable Execution Preconfirmations

# Ahead-of-Time Block Auctions To Enable Execution Preconfirmations

Thanks to [Burak Oz](https://x.com/boez95), [Bo Du](https://x.com/brobobo_bo_bobo), [Ladislaus](https://x.com/lvdaniels), [Domothy](https://x.com/domothy), Alejandro Ranchal-Pedrosa, Justin Drake for discussion or review. Final work is the author’s and reviews are not an endorsement! Also thank you to the teams who participated in [Sequencing Week](https://x.com/drakefjustin/status/1857083454011101600).

This post assumes familiarity with [preconfirmations](https://ethresear.ch/t/based-preconfirmations/17353). This post is opening a potential design direction for discussion and not an endorsement or necessarily a reflection of any team’s roadmap.

## Summary

Execution preconfirmations have two problems in order to ensure they are more profitable for the proposer than today’s existing PBS pipeline:

- Adversarial flow: how to prevent searchers from submitting transactions via execution preconfirmations, which extract money from the builder and proposer
- Pricing: how to price blockspace and mitigate the futures risk of the block becoming more valuable later

There are two approaches, one where the gateway is an unsophisticated entity, and the other where the gateway is a sophisticated builder.

The unsophisticated gateway addresses this issue by having pricers compete to take on the futures risk on behalf of the gateway. This avoids further gateway centralization.

The sophisticated builder gateway addresses this issue by designating block builders as the preconfirmation gateway. Builders can detect and block adversarial top of block `ToB` activity, preventing searchers from exploiting MEV opportunities. Moreover, builders are uniquely positioned to accurately price slots within the block.

## Pricer System

In this system, the gateway acts as an unsophisticated auction house. It holds a bidding process where *pricers* can bid to underwrite the futures risk of a preconfirmation request, in exchange for receiving the preconfirmation bid. Under this design, for every incoming transaction, a bidding process will occur in which a pricer agrees to take on its futures risk in exchange for a fee.

[![photo_2024-12-31 20.01.44](https://ethresear.ch/uploads/default/optimized/3X/9/d/9d0026e7ebec86b743eb5920d22012e33c5d14f1_2_690x349.jpeg)photo_2024-12-31 20.01.44993×503 30.1 KB](https://ethresear.ch/uploads/default/9d0026e7ebec86b743eb5920d22012e33c5d14f1)

*Ethereum Sequencing Call #13*

The pricer will be exposed to the futures risk of the contract, in exchange for accepting the tip, they will be exposed to the future risk of block space value. The key issue with the pricer system is: how to compare the value of a block with an execution constraint versus a block without the execution constraint. It could be possible to check bundles that affect a certain state in a BuilderNet-style TEE, and check the value of the block with and without the constraint to figure out the opportunity cost of transaction inclusion. This enables appropriately moving the futures risk onto the pricer.

## Current Design

This is a sketch of the components of the preconfirmation pipeline.

[![Created During Sequencing Week](https://ethresear.ch/uploads/default/optimized/3X/b/c/bc1d251a7cdcc71b459cb329a23e271302c27ac0_2_690x409.jpeg)Created During Sequencing Week1280×759 50.2 KB](https://ethresear.ch/uploads/default/bc1d251a7cdcc71b459cb329a23e271302c27ac0)

*Design suggested at [Sequencing Week](https://x.com/drakefjustin/status/1857083454011101600)*

In this design, the proposer delegates the right to issue a preconfirmation transaction to an external party, the gateway, a block builder, which is issued the right to add transactions to the top of block `ToB`, along with an inclusion list constraint on Rest of Block `RoB`. The gateway submits an ordered list that must be added to `ToB` and an unordered list that must be included in `RoB`.

This protects the proposer from DDOS attacks and allows the gateway to have more complicated and computationally expensive logic. Research by Burak Oz and others [1]  have shown that roughly 60-70% of block builder profits is earned by off-chain agreements including searcher flow and exclusive order flow. Therefore, pricing the preconfirmation is a challenging task, as only 30–40% of the data required to price the transaction is on-chain. Certain proxies like cex-dex volatility can be used to attempt to predict the off-chain MEV; however, it requires the gateway to perform complex decision-making.

The gateway must:

- successfully predict the on-chain MEV extracted in the block
- successfully predict the off-chain MEV extracted via off-chain agreements
- take on the futures risk of selling blockspace now that may increase in value later on

execution preconfirmations are particularly difficult because the gateway must predict which contentious state is MEV-valuable, and therefore deny transactions that affect certain pieces of contentious state

avoid being gamed by searchers and other entities that may seek to buy blockspace for less than its value, thereby extracting value from the proposer

The entity with the best data on the value of the upcoming block is the builder themselves. We propose merging the role of the builder and the preconfer into the gateway, we ask block builders who reap high MEV rewards to also take on the role of predicting the value of the upcoming block, and therefore pricing the preconfirmation.

Execution preconfirmations are especially valuable because they allow for synchronous composability between L2s and the L1 in advance of a block, they also allow the gateway to act as a shared block builder between the L2s and L1. They allow following transactions to act on the output state of the first transaction, creating continuous block building, massively improving UX.

## Ahead of Time Slot Auction

The gateway can buy the rights to build the top of the block either Just In Time `JiT` just ahead of the slot start time, or up to 32 slots in advance. We believe it’s better to hold an auction closer to the slot time, as the gateway has more data, and can bid higher.  Meanwhile the existing PBS pipeline is preserved, the gateway can auction off space in the `RoB` that has not yet been auctioned.

The block can be sold in the following positions:

- bid for gateway rights (ToB and RoB inclusion constraint) 32 slots in advance (potentially even traded every slot)

the issue with trading the block far in advance is there will likely be a discount to the block’s value vs a JIT auction. Therefore, we suspect a JIT auction slightly ahead of the slot start time is preferable.
- JIT auctions in advance of every slot prevent multi-slot MEV

bid for gateway rights just before the upcoming block
sell the rest of the slot via existing pbs pipeline.

Instead of selling the block at the end of the block, as is done currently, we propose auctioning the block JIT before the current slot

In exchange for taking on the responsibility of issuing preconfirmations, the builder earns additional fees for preconfirmation risk.

## Concerns

- Centralization of the Gateway

By moving the auction process just ahead of the block, we simply move the existing process that occurred at the end of the block to in advance of the block, this adds minimal changes beyond what exists today. We expect the builder market to further decentralize, we can reuse these innovations to further decentralize the gateway.

Bidding in an ahead of time auction vs JIT, where as a builder you would need to discount the expected MEV given there’s uncertainty. So depending on how long in advance you have to bid, it may not be optimal for the proposer.

- We believe the additional profits earned from preconfirmation tips may be greater than the blockspace futures risk, so the builder and proposer will be net more profitable.

## References

[1] [Burak Öz](https://arxiv.org/search/cs?searchtype=author&query=%C3%96z,+B), [Danning Sui](https://arxiv.org/search/cs?searchtype=author&query=Sui,+D), [Thomas Thiery](https://arxiv.org/search/cs?searchtype=author&query=Thiery,+T), [Florian Matthes](https://arxiv.org/search/cs?searchtype=author&query=Matthes,+F), [Who Wins Ethereum Block Building Auctions and Why?](https://arxiv.org/abs/2407.13931)

[2] [Preconfirmations Call #13](https://www.youtube.com/watch?v=oNLPglf2cQY)
