---
source: magicians
topic_id: 11962
title: EIP20 confused description
author: charlesxsh
date: "2022-12-01"
category: EIPs > EIPs core
tags: [erc-20]
url: https://ethereum-magicians.org/t/eip20-confused-description/11962
views: 618
likes: 1
posts_count: 1
---

# EIP20 confused description

I am writing to inquiry about the two descriptions in the EIP-20.

First one is related to description “This method can be used to improve usability, but interfaces and other contracts MUST NOT expect these values to be present.”. This description used in many functions like name(), symbol(), decimals(), etc.

This description could have two possible explanations:

1. These functions should not be called beyond the contract
2. Caller must check return value of these functions

Which one of them is the more appropriate one? If both of them are wrong, what would be the correct understanding?

Second one is the issue posted in reddit: https://www.reddit.com/r/solidity/comments/yh2ysd/should_i_emit_transfer_event_in_this_balance

Appreciate if anyone can drop your valuable comments/thoughts
