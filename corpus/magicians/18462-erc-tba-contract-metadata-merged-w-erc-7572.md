---
source: magicians
topic_id: 18462
title: ERC-<TBA> Contract Metadata -> merged w/ ERC-7572
author: xinbenlv
date: "2024-02-03"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-tba-contract-metadata-merged-w-erc-7572/18462
views: 921
likes: 1
posts_count: 3
---

# ERC-<TBA> Contract Metadata -> merged w/ ERC-7572

## Abstract

A standard for exposing an interface describing a contract, main goal is to achieve backward compatibility and drive adoption and forward extension

## Specification

```solidity
interface ERC-DESC {
  contractURI() public view returns(string);
}
```

```json
// A subset of
// https://schema.org/Thing and
// https://docs.opensea.io/docs/contract-level-metadata
{
  "name": "",
  "description": "",
  "image": ""
}
```

## Rationale

1. compatible with Schema.org which are used by major search engines’ indexing and OpenGraph, good for SEOs and future adoption
2. compatible with OpenSea, good for crypto adoption.

## Replies

**ryanio** (2024-02-05):

We have already proposed [ERC-7572: Contract-level metadata via `contractURI()`](https://ethereum-magicians.org/t/erc-7572-contract-level-metadata-via-contracturi/17157), looks like your proposal is similar/the same, if you have any suggestions please feel free to comment in that thread.

---

**xinbenlv** (2024-02-13):

Hi [@ryanio](/u/ryanio), thanks for bringing to my attention for ERC-7572. That sounds good. Happy to converge to yours if we share the same goal and same design philosophy.

Everyone reading this ERC proposal, please join discussion here [ERC-7572: Contract-level metadata via contractURI()](https://ethereum-magicians.org/t/erc-7572-contract-level-metadata-via-contracturi/17157)

