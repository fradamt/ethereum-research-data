---
source: magicians
topic_id: 12003
title: How to extract contract metadata from creation code
author: michprev
date: "2022-12-03"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/how-to-extract-contract-metadata-from-creation-code/12003
views: 566
likes: 1
posts_count: 1
---

# How to extract contract metadata from creation code

Hello,

I am building a tool (testing framework + debugger) and, I need to unambiguously link a contract being created with its AST. For deployed contracts I can simply use the deployed bytecode - the last 53 metadata bytes that should be unique in the project. However, in the case of CREATE and CREATE2 I cannot use the deployed bytecode because the transaction might have reverted in that CREATE/CREATE2 call.

I know that creation code:

- contains bytecode from solc + encoded arguments for a contract constructor
- contains metadata of the contract being deployed
- can also contain metadata of other contracts used in the contract being deployed
- metadata of the contract being deployed does not need to be the first or the last metadata in the creation code (i.e. metadata of the deployed contract can be located in between metadata of other contracts)

Is there any deterministic way, how to distinguish between metadata of the contract being deployed and other contracts metadata in the creation code (i.e. code passed to the CREATE/CREATE2 opcodes)?
