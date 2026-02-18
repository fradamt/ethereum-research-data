---
source: magicians
topic_id: 5766
title: Charging Gas for reading a view function in a transaction seems odd
author: aak-dev
date: "2021-03-19"
category: Magicians > Primordial Soup
tags: [evm, gas]
url: https://ethereum-magicians.org/t/charging-gas-for-reading-a-view-function-in-a-transaction-seems-odd/5766
views: 670
likes: 1
posts_count: 3
---

# Charging Gas for reading a view function in a transaction seems odd

I just cant get my head around why view functions which are gas free suddenly cost 5k gwei when sandwiched between a state transitioning function which just uses the view function like a web3 call.

## Replies

**ajsutton** (2021-03-19):

When you execute a read only call against a node, the call is executed locally and no transaction is ever sent, so no gas is actually used (in terms of block space).  When you put that into a transaction, the read operation is executed as part of the block, taking up gas on the block and requires every node on the network to execute it - so you have to pay for that gas.

---

**aak-dev** (2021-03-20):

great thanks for explaining. But i saw for multiple views in the same transaction cost the same as first view. And just discovered eip 2930, after Berlin subsequent views are charged less would be great but 2929 is increasing the sload operation sad.

