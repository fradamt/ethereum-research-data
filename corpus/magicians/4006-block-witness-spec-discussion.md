---
source: magicians
topic_id: 4006
title: Block Witness Spec discussion
author: mandrigin
date: "2020-02-17"
category: Working Groups > Ethereum 1.x Ring
tags: [stateless-clients]
url: https://ethereum-magicians.org/t/block-witness-spec-discussion/4006
views: 1027
likes: 0
posts_count: 1
---

# Block Witness Spec discussion

Hey there!

I’ve just opened the first PR against the [stateless-ethereum-specs](https://github.com/ethereum/stateless-ethereum-specs/) repo: https://github.com/ethereum/stateless-ethereum-specs/pull/1

It has a draft of a block witness specification, based on the block witnesses that are used in [turbo-geth](https://github.com/ledgerwatch/turbo-geth) with a few minor tweaks.

A good thing about this format is that it works ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) Basically, we’ve been running tests on Ethereum mainnet using almost the same witness format and were able to proof blocks for the whole history of the chain.

I’m very open to any feedback regarding the spec itself and the witness format too.
