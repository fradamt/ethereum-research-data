---
source: magicians
topic_id: 15414
title: "EIP-7480: EOF - Data section access instructions"
author: gumb0
date: "2023-08-11"
category: EIPs > EIPs core
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/eip-7480-eof-data-section-access-instructions/15414
views: 1767
likes: 1
posts_count: 3
---

# EIP-7480: EOF - Data section access instructions

Discussion topic for [EIP-7480: EOF -  Data section access instructions](https://github.com/ethereum/EIPs/pull/7480)

## Replies

**ryley-o** (2024-06-11):

Regarding the lack of `EXTDATACOPY`, I am concerned that this is a slight regression for systems that plan to use the data storage functionality for immutable data.

Previously, EXTCODECOPY could be safely used to read immutable data stored in the bytecode of arbitrary contract addresses. Now, with no equivalent EXTDATACOPY, a view function on the contract containing the data must be called, which will be allowed to execute arbitrary logic, meaning there is no guarantee that a contract is returning an immutable value. For example, after a certain block, a contract could return a different section of its data.

This is especially relevant to protocols that allow third parties to upload arbitrary data, but have a review process for assurance of things like community guidelines, compliance, etc. before they are shown publically.

I’m curious what others think about this regression, and if it is worth more investigation!

---

**shemnon** (2024-06-12):

A contract that wants to share it’s data can copy from data and return it from an EXTCALL operations, so EOF data contracts can continue to exist.

That being said, there is a chance the costing models in Verkle will make data contracts a less efficient way to store large amounts of data on-chain.

Legacy contracts will continue to exist for a number of years, and there may still be room for EXTDATACOPY to arrive in EOF.  It was not judged as essential to the first implementation, however.

