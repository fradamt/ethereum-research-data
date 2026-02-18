---
source: magicians
topic_id: 10347
title: Should the ChainId change with every hardfork
author: rmeissner
date: "2022-08-12"
category: Working Groups > The Merge
tags: [evm, opcodes, core-eips, eth1-eth2-merge]
url: https://ethereum-magicians.org/t/should-the-chainid-change-with-every-hardfork/10347
views: 1017
likes: 0
posts_count: 1
---

# Should the ChainId change with every hardfork

Currently the [chain id](https://ethereum-magicians.org/t/eip-1344-add-chain-id-opcode/1131) will not change on a hardfork. The common case for the chain id is when a new network is spun up to uniquely identify it in the consesus logic (e.g. signatures and smart contracts) to enable replay protection (or other chain specific logic).

Now with [the merge](https://ethereum.org/en/upgrades/merge/) approaching it is quite likely that there will be a [Proof of Work Ethereum](https://ethereumpow.org/) which then potentially has the same chain id as the Proof of Stake Ethereum.

A way to tackle this issue would be to change the chain id with every hardfork (like a version). For example the chain id which is currently a uint256 could be separated in 2 uint128 that are a version and a chainid.

Obviously it is not that simple as there are quite some smart contracts that have hardcoded the chain id. But it will be necessary in the future to properly differentiate chains that are the result of a hardfork that was not adopted by the majority and “just sticks to the status quo”.
