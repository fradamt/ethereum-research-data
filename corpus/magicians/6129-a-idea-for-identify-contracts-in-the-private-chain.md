---
source: magicians
topic_id: 6129
title: A idea for identify contracts in the private chain
author: xieyi1393
date: "2021-05-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/a-idea-for-identify-contracts-in-the-private-chain/6129
views: 481
likes: 0
posts_count: 1
---

# A idea for identify contracts in the private chain

When I was using the private chain, I have a idea that we can identify some contracts for special usage.

Such as identifying the ENS as “Private ENS”.

Then we can use the ENS without special configure it in wallet.

But for security,they can only use in the chain which using Proof-of-Authority.And the request should sent by the administrator of the chain.

I think we can allocate a pre-build contract.It did’t do anything in EVM but costs some ETH for gas to preventing attack.When we want to send a request to  identify a contract,we can send a transaction which  contains the address of the contract and its name to the pre-build contract.Then all nodes checks the permission of the sender of the transaction.If the check passed,then the node record the name of the contract.

What do you think?
