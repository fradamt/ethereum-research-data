---
source: magicians
topic_id: 2655
title: CREATE2 Safe Deploy contract on mainnet (prevents the create2 - selfdestruct - create2 attack vector!)
author: jochem-brouwer
date: "2019-02-14"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/create2-safe-deploy-contract-on-mainnet-prevents-the-create2-selfdestruct-create2-attack-vector/2655
views: 719
likes: 1
posts_count: 1
---

# CREATE2 Safe Deploy contract on mainnet (prevents the create2 - selfdestruct - create2 attack vector!)

Hey everyone!

Due to the recent discussions and various articles on some news portals about CREATE2 “bugs” and attack vectors about the possibility to deploy different code at the same address I decided to write a quick contract to prevent against this. The contract can be found on mainnet here [here](https://etherscan.io/address/0x5df4c8e56fe3a95f98ce3d1935abd1b187525915#code) and obviously does not work at this point.

This contract has not been audited so use it at your own risk. It’s not a complicated contract, it simply stores deployed contracts in a mapping and throws if it sees that a contract has already been marked as “deployed” either before or after creation of the contract. The sender can choose what option to use - I tried to reduce as much gas as possible here.

It is impossible for different senders to deploy at the same address since the seed which is provided is hashed with `msg.sender`. This is obviously different from CREATE2, but in my opinion this is a good feature for this type of proxy contract.

Feedback is well appreciated!
