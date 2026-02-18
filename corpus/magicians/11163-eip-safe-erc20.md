---
source: magicians
topic_id: 11163
title: "EIP: Safe ERC20"
author: BoxChen
date: "2022-10-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-safe-erc20/11163
views: 551
likes: 0
posts_count: 1
---

# EIP: Safe ERC20

## Introduction

This thread is for discussing a new, alternative Token protocol for ERC20.In light of the recent mass thefts, I have a new idea. I would like to build a Token protocol that works properly but also has security. It is a new protocol based on the combination of EIP-2612 and some features.

## Detail

According to the current requirements in common contracts. There are two main cases of user authorization:

- call the contract after authorization to transfer tokens directly - UNISWAP, Masterchef, Lend.
- wait for other timing to transfer after authorization. – Seaport and other NFT markets.

Two solutions come to mind here.

- force all Tokens must use permit and prohibit EOA account call approve, only allow the contract account calls. Also add a new function to force the user to set the nonce to achieve the role of a skip, used to act as a solution after the illegal permit. The problem with this is that the NFT market will not be able to transfer WETH directly, but only to pre-deposit, while not knowing their signature. But in practice, users can convert from ETH to WETH, and then Approve WETH transactions into Deposit ETH. and is very effective for most cases where a single token transfer is used.
- add a deadline mechanism to approve, in the wallet plug-in, set a smaller deadline for approve by default, and can modify the function signature, the default setting for approve without deadline parameter is +10 minutes. to reduce the risk of legacy after the contract is breached.
The advantage of the first solution is that the signature is used as it is signed, but the pitfall is that it is not compatible with DAPPs that are not used instantly, and the advantage of the second solution is that the original code is less modified, but the security improvement is also smaller.

Most of the cases of approve all token are about reducing the number of transactions and fees for users. Therefore, it may be a better way to solve the problem from the root. If the two solutions are combined, it can solve many problems, but whether it is necessary to do so needs to be discussed.
