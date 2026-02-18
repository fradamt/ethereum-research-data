---
source: magicians
topic_id: 21137
title: "ERC-7771: Router Proxy"
author: ethernaut
date: "2024-09-19"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7771-router-proxy/21137
views: 81
likes: 0
posts_count: 2
---

# ERC-7771: Router Proxy

## Abstract

---

The Router Proxy introduces a streamlined approach to managing multiple implementations behind a single proxy, similar to the Diamond Proxy Standard ([ERC-2535](https://github.com/ethereum/ercs/blob/master/ERCS/erc-2535.md)). Unlike the latter, this method hardcodes module addresses within the proxy’s implementation contract, offering a simpler, more explicit, and gas-efficient mechanism. This design reduces complexity, making it easier to reason about and improving overall efficiency while retaining the flexibility to manage multiple modules.

## ERC Pull Request

---



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/blob/058b636069a682a8eafdc2d7da41096e29bc8020/ERCS/erc-7771.md)





####

  [058b63606](https://github.com/ethereum/ERCs/blob/058b636069a682a8eafdc2d7da41096e29bc8020/ERCS/erc-7771.md)



```md
---
eip: 7771
title: Router Proxy
description: A Simple Proxies Architecture with Multiple Hardcoded Implementations
author: Alejandro Santander (@theethernaut), Noah Litvin (@noahlitvin)
discussions-to: https://ethereum-magicians.org/t/erc-7771-router-proxy/21137
status: Draft
type: Standards Track
category: ERC
created: 2024-09-19
---

## Abstract

The Router Proxy introduces a streamlined approach to managing multiple implementations behind a single proxy, similar to the Diamond Proxy Standard ([ERC-2535](./erc-2535.md)). Unlike the latter, this method hardcodes module addresses within the proxy’s implementation contract, offering a simpler, more explicit, and gas-efficient mechanism. This design reduces complexity, making it easier to reason about and improving overall efficiency while retaining the flexibility to manage multiple modules.

## Motivation

As Ethereum's application layer continues to mature, the complexity of smart contracts required for these applications has increased. Given the 24KB size limitation for a single smart contract, developers often need to compose applications using multiple interconnected contracts. This necessitates the use of an onchain registry to manage the relationships and interactions between these contracts. Typically, one contract within the application must know how to interact with another, querying the registry for specific addresses. Similarly, when a component of the system receives an interaction, it must verify with the registry whether the caller is an authorized part of the application. Consequently, non-trivial Ethereum applications require these "connecting wires," which are cumbersome to deploy, complex to code, inefficient at runtime, and, most importantly, prone to human error and common attack vectors due to the lack of standardized solutions.

```

  This file has been truncated. [show original](https://github.com/ethereum/ERCs/blob/058b636069a682a8eafdc2d7da41096e29bc8020/ERCS/erc-7771.md)

## Replies

**mudgen** (2024-10-15):

Hey there.

I really like the idea here about having a proxy router with hardcoded module/facet addresses.

I would like to make clear that this can and has been done using EIP-2535 Diamonds.  An EIP-2535 Diamonds implementation can have and use hardcoded module/facet addresses and selectors. The Pendle project is using such a static diamond implementation here: https://etherscan.io/address/0x0000000001e4ef00d069e71d6ba041b0a16f7ea0#code

The EIP-2535 Diamonds standard is really flexible and allows a variety of different implementations. I think it would be useful to have a new standard that standardizes static diamond implementations – a standard that implements EIP-2535 that uses hardcoded facet addresses and selectors. An article that covers the minimum things required to comply with the EIP-2535 Diamonds standard is here: [Compliance with EIP-2535 Diamonds Standard](https://eip2535diamonds.substack.com/p/compliance-with-eip-2535-diamonds)

