---
source: magicians
topic_id: 25003
title: "ERC-8000: Operator contract for non delegated EOAs"
author: marcelomorgado
date: "2025-08-04"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8000-operator-contract-for-non-delegated-eoas/25003
views: 85
likes: 1
posts_count: 2
---

# ERC-8000: Operator contract for non delegated EOAs

Hello, we’re proposing a new ERC to add the ability to have non-delegated EOAs to execute batch transactions.

## Abstract

This standard defines a contract interface that enables externally owned accounts (EOAs) to perform batch call executions via a standard Operator contract, without requiring them to delegate control or convert into smart contract accounts.

## Motivation

The [ERC-7702](https://eips.ethereum.org/EIPS/eip-7702) allows EOAs to become powerful smart contract accounts (SCA), which solves many UX issues, like the double `approve` + `transferFrom` transactions.

While this new technology is still reaching wider adoption over time, we need a way to improve UX for the users that decide to not have code attached to their EOAs.

This proposal introduces a lightweight, backward-compatible mechanism to enhance UX for such users. By leveraging a standardized Operator contract, EOAs can batch multiple contract calls into a single transaction—assuming the target contracts are compatible (i.e., implement the Operated pattern).

Further details: [ERC-8000](https://github.com/ethereum/ERCs/blob/12946d04911f19d0799e2373aa6ea4056bb64585/ERCS/erc-8000.md)

## Replies

**SamWilsn** (2025-11-19):

This looks like it has significant overlap with the [Gas Station Network](https://opengsn.org/) and [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337).

Assuming you’d still like to pursue ERC-8000, I’d like to see a comparison to similar proposals (like ERC-4337’s `EntryPoint`) in the Motivation section.

