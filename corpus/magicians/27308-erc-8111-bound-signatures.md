---
source: magicians
topic_id: 27308
title: "ERC-8111: Bound Signatures"
author: wjmelements
date: "2025-12-24"
category: ERCs
tags: [signatures, cryptography]
url: https://ethereum-magicians.org/t/erc-8111-bound-signatures/27308
views: 73
likes: 1
posts_count: 2
---

# ERC-8111: Bound Signatures

# Bound Signatures

Bound signatures are ECDSA signatures bound to a specific `v`.

Constraining the y-parity allows signatures to fit into 64 bytes.

## Background

ECDSA signatures recover two public keys for the same hash.

ECDSA signatures are recoverable when they indicate which of the public keys corresponds to the signing key.

Previous developers signaled which using a y-parity bit.

In Ethereum, this bit is encoded as `v`.

ECDSA signatures (`r`, `s`) are malleable; the `s` can be reflected across `n/2` (where `n` is the elliptic curve’s order) to produce a new signature that would recover the same public keys.

This operation also flips the y-parity bit.

Therefore, if the y-parity bit is bound, the signature is **recoverable** and **not malleable**.

## Links

- PR: add ERC
- PR: add to ethers.js
- Reference Implementation
- Prior discussion thread

## Replies

**wjmelements** (2026-02-04):

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1514)














####


      `master` ← `wjmelements:erc-8111-review`




          opened 07:58PM - 04 Feb 26 UTC



          [![](https://avatars.githubusercontent.com/u/799573?v=4)
            wjmelements](https://github.com/wjmelements)



          [+1
            -1](https://github.com/ethereum/ERCs/pull/1514/files)







#### Changes
* Move ERC 8111 to Review

