---
source: magicians
topic_id: 15921
title: Any EIP for a precompile for CallPermit Account Abstraction
author: dominic
date: "2023-09-27"
category: EIPs
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/any-eip-for-a-precompile-for-callpermit-account-abstraction/15921
views: 534
likes: 0
posts_count: 1
---

# Any EIP for a precompile for CallPermit Account Abstraction

Hey there,

I’ve seen quite a couple of account abstraction discussions especially:

- Implementing account abstraction as part of eth1.x
- EIP-2938: Account Abstraction
- ERC-4337: Account Abstraction Using Alt Mempool

All of these are very complex and EIP-4337 especially requires to make smart contracts compatible. E.g. you can’t use your existing contracts with it that are not aware of EIP-4337.

Now comparing that to the solution of a native pre-compile which allows impersonation of an account given a valid EIP-712 signature: [Gasless Transactions with the Call Permit Precompile | Moonbeam Docs](https://docs.moonbeam.network/tutorials/eth-api/call-permit-gasless-txs/) – It seems the native pre-compile route is much more flexible and brings much higher compatibility.

Now my question has this approach been discussed before and there are really good reasons why Ethereum is not opting to solve this with a new precompile or is it just that nobody has created that EIP yet?
