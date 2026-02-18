---
source: magicians
topic_id: 13849
title: "New EIP Draft: IOwnable Interface"
author: bitcoinbrisbane
date: "2023-04-17"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/new-eip-draft-iownable-interface/13849
views: 435
likes: 1
posts_count: 2
---

# New EIP Draft: IOwnable Interface

Many contract get the contract owner but there is no interface for this.  The OZ Ownable contract does not have an interface and the owner() function is only public.  Should we have a simple interface such as:

// SPDX-License-Identifier: MIT

pragma solidity =0.8.15;

interface IOwnable {

function getOwner() external view returns (address);

}

## Replies

**abcoathup** (2023-04-17):

There is an ERC already for ownership



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-173)





###



A standard interface for ownership of contracts

