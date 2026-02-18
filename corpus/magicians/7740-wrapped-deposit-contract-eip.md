---
source: magicians
topic_id: 7740
title: Wrapped deposit contract EIP
author: j_chance
date: "2021-12-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/wrapped-deposit-contract-eip/7740
views: 2245
likes: 0
posts_count: 2
---

# Wrapped deposit contract EIP

This is a discussion thread for an informational EIP describing a singleton contract meant to act as a deposit agent.

The basic strategy is deploy a tiny, stateless contract that offers a way for other contracts to accept deposits (Ether, ERC20/721). This is done by having the singleton contract call into the destination contract with information about the deposit before executing the transfer.

This means a user only needs to approve the wrapper contract once and can then deposit to many applications supporting the interface. This is designed to:

1. Remove the security implications of approving many application contracts to spend tokens
2. Improve user experience when using tokens with applications
3. Reduce the number of transactions needed when using the Ethereum network

Draft implementation of the wrapper contract [here](https://github.com/JChanceHud/wrapped-deposit/blob/main/contracts/WrappedDeposit.sol).

[EIP PR](https://github.com/ethereum/EIPs/pull/4546/files)

## Replies

**vic** (2023-04-18):

Is this still stagnant? I saw that the github bot has merged it in

