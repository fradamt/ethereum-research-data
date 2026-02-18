---
source: ethresearch
topic_id: 6971
title: Block Witness Format Spec Draft
author: mandrigin
date: "2020-02-17"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/block-witness-format-spec-draft/6971
views: 1362
likes: 1
posts_count: 1
---

# Block Witness Format Spec Draft

Hey there!

I’ve just opened the first PR against the stateless-ethereum-specs repo: https://github.com/ethereum/stateless-ethereum-specs/pull/1

It has a draft of a block witness specification, based on the block witnesses that are used in [turbo-geth](https://github.com/ledgerwatch/turbo-geth)with a few minor tweaks.

A good thing about this format is that it works ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) Basically, we’ve been running tests on Ethereum mainnet using almost the same witness format and were able to proof blocks for the whole history of the chain.

I’m very open to any feedback regarding the spec itself and the witness format too.
