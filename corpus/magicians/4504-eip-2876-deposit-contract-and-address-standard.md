---
source: magicians
topic_id: 4504
title: "EIP-2876: Deposit contract and address standard"
author: junderw
date: "2020-08-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2876-deposit-contract-and-address-standard/4504
views: 748
likes: 1
posts_count: 2
---

# EIP-2876: Deposit contract and address standard

This ERC defines a simple contract interface for managing deposits. It also defines a new address format that encodes the extra data passed into the interface’s main deposit function.

EIP is here: https://eips.ethereum.org/EIPS/eip-2876

Sample Implementation is linked in the EIP.

One major question brought up: Why not EIP-681? It also supports ERC-20 which many exchanges need.

I mention why no ERC-20 support is not an issue in the EIP (separation of logic and keys) and as for why not EIP-681 I answered [here](https://github.com/ethereum/EIPs/pull/2876#issuecomment-673845508).

Some goals I want to accomplish after this EIP is in a Final stage:

1. Get support for generating and verifying deposit addresses into as many popular libraries in as many languages as possible.
2. Get a widely reviewed implementation of a simple forwarding contract that implements the interface and also has some Event emitting and a kill switch. This way merchants and exchanges can just deploy the one contract and start accepting deposits immediately.
3. Get support for sending to these deposit addresses in all major wallet software.
4. Get major exchanges to support sending to these addresses.

Anyways. Now that you all are up to speed on my goals and reasoning, tear my proposal apart, please. I look forward to discussing with you all.

## Replies

**poojaranjan** (2021-02-19):

An overview of the ‘Deposit Contract and Address Standard’ proposal to prevent the wastage of gas in the deposit on an exchange, with bonus thoughts on a probable approach to decrease high gas usage in the overall network by [@junderw](/u/junderw) in [PEEPanEIP](https://www.youtube.com/playlist?list=PL4cwHXAawZxqu0PKKyMzG_3BJV_xZTi1F).

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/b/be898d15eb6985f13285c9c543bfc1ff5ad592f8.jpeg)](https://www.youtube.com/watch?v=ha8uOWNT6sg)

