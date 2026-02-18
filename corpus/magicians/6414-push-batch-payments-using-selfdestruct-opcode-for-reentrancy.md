---
source: magicians
topic_id: 6414
title: Push batch payments using selfdestruct opcode for reentrancy immunity, lower gas costs and untraceable transactions from recipient address
author: etherportal
date: "2021-06-05"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/push-batch-payments-using-selfdestruct-opcode-for-reentrancy-immunity-lower-gas-costs-and-untraceable-transactions-from-recipient-address/6414
views: 740
likes: 1
posts_count: 1
---

# Push batch payments using selfdestruct opcode for reentrancy immunity, lower gas costs and untraceable transactions from recipient address

[etherportal/EtherPortal: Safely push batch ether transfers - immune to reentrancy/fallback shenanigans, lower gas costs, and untraceable from recipient address (github.com)](https://github.com/etherportal/EtherPortal)

Hi hope you can take a look at my first github repository, I think it presents a novel method of pushing batch payments with real world utility for existing projects.

Transfers made through the selfdestruct opcode do not trigger the fallback() function guarding against reverts/reentrancy/unpredictable gas costs.

The transfers are also untraceable from the recipient address, for example see https://ropsten.etherscan.io/address/0x60756E15b55a6d5320cb28D1915925B45BE6ccd6, which has 1 wei but no transaction history.

I also found a method to get significant gas savings by repeatedly invoking selfdestruct at the same contract instance, instead of creating a contract instance for each transfer. Due to the nuance of the opcode implementation, the selfdestructing contract remains accessible within the same transaction call, and can repeatedly invoke selfdestruct to continue sending ether.

For batch transfers to 100 existing accounts, this results in ~30% gas savings over direct transfers from EOA.
