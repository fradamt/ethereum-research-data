---
source: magicians
topic_id: 27424
title: "ERC-8121: Cross-Chain Function Calls via Hooks"
author: nxt3d
date: "2026-01-12"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8121-cross-chain-function-calls-via-hooks/27424
views: 63
likes: 2
posts_count: 1
---

# ERC-8121: Cross-Chain Function Calls via Hooks

ERC-8121 introduces **hooks**, a specification for cross-chain function calls. A hook fully specifies what function to call, with what parameters, on which contract, on which chain.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1456)














####


      `master` ← `nxt3d:hooks`




          opened 04:12AM - 07 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/3857985?v=4)
            nxt3d](https://github.com/nxt3d)



          [+265
            -0](https://github.com/ethereum/ERCs/pull/1456/files)







## Summary

This PR adds a draft ERC that defines **Hooks**: a mechanism for r[…](https://github.com/ethereum/ERCs/pull/1456)edirecting a metadata record to another contract for resolution via a specified function call.

## Motivation

Hooks enable clients to resolve records from known, trusted resolver contracts, allowing credentials such as Proof of Personhood (PoP) and Know Your Customer (KYC) records to be resolved securely.

## What’s in this ERC

- A hook format for `bytes`-stored and `string`-stored metadata records
- A function-call string format and examples
- Guidance for detection and resolution, including ERC-3668 (CCIP-Read) support and recursion limits
- Rationale and security considerations around trusted resolvers












A hook combines a function selector, human-readable function call, return type, and ERC-7930 interoperable address:

```auto
hook(0xc41a360a, "getOwner(42)", "(address)", 0x000100000101141234567890abcdef1234567890abcdef12345678)
```

Hooks are useful for redirecting to trusted credential registries (PoP, KYC, KYA for AI agents), cross-chain metadata resolution, and singleton registries with known security properties.
