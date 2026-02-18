---
source: magicians
topic_id: 999
title: Scheme for off-chain signatures and encoding for on-chain verification
author: dekz
date: "2018-08-09"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/scheme-for-off-chain-signatures-and-encoding-for-on-chain-verification/999
views: 588
likes: 2
posts_count: 1
---

# Scheme for off-chain signatures and encoding for on-chain verification

## Overview

There are discrepancies and nuances to encoding signatures for usage and verification on-chain.

ECDSA is the dominant form of proof and is comprised of v, r and s fields. Signers often return this v,r,s as an encoded hex string where the components are concatenated. In many EIPS and documentation the order is either v,r,s or r,s,v. In many signers the order is r,s,v.

As the order of these components is ambiguous it is often difficult to predict the signer behaviour and this is usually checked/fixed in library wrappers.

Formalising on a standard encoding will reduce library code bloat, reduce developer overhead and increase contract interoperability.

## The case for v,r,s

- The Ethereum yellowpaper often describes these parameters in the order v,r,s.
- Ethereum Transactions signatures are encoded as v,r,s
- ecrecover in solidity ecrecover(bytes32 hash, uint8 v, bytes32 r, bytes32 s) returns (address)
- EIPs: 86, 155, 232 all use the order v,r,s.
- ethereumjs-utils returns {v,r,s} object to avoid ambiguity.

## The case for r,s,v

- JSONRPC eth_sign returns r,s,v. First occurence seems to be here with no justification. This has propagated to many signer implementations.

## Proposals

- Off-chain always use v,r,s, so transactions and signing is the same order. On-chain expect v,r,s.
- Return a v,r,s object from eth_sign so there is less ambiguity. On-chain expect v,r,s.

Future discussion:

- v=v-27 vs v=27|28
- A standard way to represent the signature type
