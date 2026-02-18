---
source: ethresearch
topic_id: 430
title: Verifying the Purity of the Function Stored at the Validation Code Address
author: ltfschoen
date: "2018-01-03"
category: Sharding
tags: []
url: https://ethresear.ch/t/verifying-the-purity-of-the-function-stored-at-the-validation-code-address/430
views: 1347
likes: 5
posts_count: 3
---

# Verifying the Purity of the Function Stored at the Validation Code Address

In the [VMC section of the Sharding Specification](https://github.com/ethereum/sharding/blob/develop/docs/doc.md#validator-manager-contract-vmc) what is “purity-verified” referring to?

Would a standard approach to verifying the purity of the pure function that is expected to be stored at the Validation Code Address `validationCodeAddr` simply involve performing a Unit Test to verify its actual outputs are what we expect them to be for given inputs? Or are there other recommended Quality Assurance steps?

## Replies

**vbuterin** (2018-01-04):

The check is done by the purity checker contract, which is written here: https://github.com/ethereum/research/tree/master/impurity

It can’t be a unit test; it has to be airtight, which means actual static analysis of the code to verify that it does not have any state-accessing opcodes.

Purity verification doesn’t mean checking that outputs are “correct” or match some “expectation” in any sense; it means checking that output is dependent on input ONLY, and not on any kind of state, and that the contract does not have any effects on the state. The reason why this is important is so that an attacker cannot create a malicious validation code that somehow returns true when you process it in order to verify votes but later return false when the validator misbehaves and someone provides evidence of this misbehavior to the `slash` function.

---

**jamesray1** (2018-01-06):

Thanks for the clarification, that makes sense now!

