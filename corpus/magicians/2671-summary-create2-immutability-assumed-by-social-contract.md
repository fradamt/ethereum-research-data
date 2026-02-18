---
source: magicians
topic_id: 2671
title: "[Summary] CREATE2: immutability assumed by social contract"
author: Ethernian
date: "2019-02-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/summary-create2-immutability-assumed-by-social-contract/2671
views: 1192
likes: 2
posts_count: 2
---

# [Summary] CREATE2: immutability assumed by social contract

As a preparation for discussion about [Social Contract and Immutability](https://ethereum-magicians.org/t/immutables-invariants-and-upgradability/2440/64) that will hopefully take place at Paris Council, would you please explicitly collect here a changes of Social Contract and Immutability Assumptions that the CREATE2 will create?

It will help us to have more focused and prepared discussion.

This thread is aimed to be an implication summary discussed in [Potential security implications of CREATE2? (EIP-1014)](https://ethereum-magicians.org/t/potential-security-implications-of-create2-eip-1014/2614).

I am starting the list:

Our **Social Contract on Immutability**:

1. Immutable References: In our communication we consider contract address as a sufficient and immutable reference to immutable object. We don’t use contract revisions or block ranges additionally to contract address to refer to particular contract mutation.
2. We follow “Audit once - Trust many” paradigm. Regular contract audits are not necessary because of assumed immutability of deployed contract.
There are two exceptions: Hard Forks and Declared mutability of dependencies.
3. Hard Forks are considered to be impossible to fulfill in hidden without a publicly well-known announcement. This announcement allows to re-audit implication of the hard fork for particular contract in advance.
4. A Declared mutability of dependencies is a ability to replace a particular contract in the bundle. “Upgradable proxied Contracts” is a good example. This kind of mutability should be recognized by first audit. Anyway, a particular contract assumed to remain immutable.
It is assumed to be impossible to introduce any unexpected mutability later.
5. ///please continue///

[@jpitts](/u/jpitts): can I make this post to Wiki?

## Replies

**pereztechseattle** (2019-02-18):

1. Under CREATE2 , any “audit” of a qualifying contract’s bytecode is rendered useless since the contract could theoretically be replaced at any time by the owner.  Further, because we can’t be certain of transaction ordering, there’s no way to check-then-proceed-if-ok.  In addition, only those with a fully synced node would have any hope of “knowing” what the target contract actually consists of.

