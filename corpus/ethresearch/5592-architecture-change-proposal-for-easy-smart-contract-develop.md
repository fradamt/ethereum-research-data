---
source: ethresearch
topic_id: 5592
title: Architecture change proposal for easy smart contract development
author: spartucus
date: "2019-06-10"
category: Architecture
tags: []
url: https://ethresear.ch/t/architecture-change-proposal-for-easy-smart-contract-development/5592
views: 1487
likes: 0
posts_count: 2
---

# Architecture change proposal for easy smart contract development

I’m new to Ethereum smart contract development, I was eosio smart contract developer earlier. First time to deal with solidity and web3.js, it was full of unfriendliness to beginners. I must be familiar with both solidity and js, maybe html/css. What if I just want make a contract that just using it with command tool, not for UI users, do I have to master these skills?

I don’t think so. For example, eosio has **cleos** and **nodeos**, first one is client, second one is node, developer just use cleos to make push and get( like transaction and call in ethereum), and for all contracts, it’s push and get, no other extra functions. And cleos has power to let developer use it to call for contract, no matter it’s a push or a get, no need to call it using a different tools like web3.js or anything else. Developer just focus on the contract itself, not other js/html/css.

I’m a big fan of ethereum, it would be wonderful if ethereum improve this in future.

## Replies

**kladkogex** (2019-06-12):

I think truffle has a command line like this.  I have also seen another CLI recently, dont remember the name of it though …

