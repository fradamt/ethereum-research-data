---
source: ethresearch
topic_id: 2512
title: Checking for contracts in Constantinople
author: MoonMissionControl
date: "2018-07-10"
category: EVM
tags: []
url: https://ethresear.ch/t/checking-for-contracts-in-constantinople/2512
views: 1580
likes: 0
posts_count: 2
---

# Checking for contracts in Constantinople

Right now, in solidity, there are two ways to check for a contract, via extcodesize or by checking if tx.origin == msg.sender.

tx.origin is going to be deprecated.

extcodesize does not work for contracts calling via their constructor.

This should be fixed. A clear way should be presented to check if an address is a contract OR an user, especially when “user wallets” will have actual code in them in the future.

## Replies

**enderphan94** (2019-11-28):

Same concern, have you found the solution?

