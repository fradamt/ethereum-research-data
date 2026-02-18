---
source: magicians
topic_id: 5454
title: EIP proposal - Pull operator pattern out of ERC777 into its own EIP
author: albertocuestacanada
date: "2021-03-02"
category: EIPs
tags: [erc-777]
url: https://ethereum-magicians.org/t/eip-proposal-pull-operator-pattern-out-of-erc777-into-its-own-eip/5454
views: 562
likes: 0
posts_count: 1
---

# EIP proposal - Pull operator pattern out of ERC777 into its own EIP

ERC777 includes an access control pattern that lets *users* to *authorize* *operators* to operate with the user tokens.

I’m thinking on extracting this pattern as an ERC, as a way of providing a set of best practices and a building block to make other ERCs leaner.

This is a common pattern ([ds-auth](https://github.com/dapphub/ds-auth), [Delegable](https://github.com/yieldprotocol/yield-utils/blob/e910118fdb8b2076ae6148047961aee36cf7f913/contracts/access/Delegable.sol)) which can be easily drafted and then used as a building block in many other ERCs (ERC20, ERC721, ERC777, ERC1155).

In particular, ERC777 is a beast of an ERC, and it doesn’t need to be. Segregating the operator pattern into its own ERC would allow ERC777 to be easier to understand. Later ERCs could pick apart other features of ERC777 like granularity and hooks.

Is there any interest in opening this can of worms?
