---
source: magicians
topic_id: 16741
title: Executor Interface
author: z0r0z
date: "2023-11-24"
category: EIPs
tags: [account-abstraction, accounts]
url: https://ethereum-magicians.org/t/executor-interface/16741
views: 583
likes: 0
posts_count: 1
---

# Executor Interface

# Executor

An interface for executing contract calls.

## Interface

```solidity
/// @notice Executor interface.
interface IExecutor {
    function execute(address target, uint256 value, bytes calldata data)
        external
        payable
        returns (bytes memory result);

    function delegateExecute(address target, bytes calldata data)
        external
        payable
        returns (bytes memory result);
}
```

## Motivation

There is fragmentation in how developers implement `call` and `delegatecall` in their contracts. As an `Executor` interface is the basis of smart accounts (see ERC4337, ERC6900), a simple standard for executing `call` or `delegatecall` would allow more applications to predictably build the correct calldata, as well as promote security. For purposes of syntax, and in anticipation of new methods, the word `execute` stands in for `call`, thus `execute` works for calls and `delegateExecute` works for calls that delegate to another account’s bytecode.
