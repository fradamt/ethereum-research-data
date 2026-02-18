---
source: magicians
topic_id: 22895
title: "EIP-7885 : Precompile for NTT operations"
author: rdubois-crypto
date: "2025-02-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7885-precompile-for-ntt-operations/22895
views: 76
likes: 1
posts_count: 1
---

# EIP-7885 : Precompile for NTT operations

Discussion topic for EIP-9374

# Abstract

Implement a generic polynomial NTT precompile to speed-up all lattices post quantum signature candidates and Starks settlement.

Post quantum threat is one of the concern regarding Ethereum security. Lattices candidates are

seen as potential replacement for ECDSA. This precompile enables efficient implementation of those candidates without having to fix the choice too early. It also reduce gas cost for STARK settlement.

#### Update Log

- 2025-02-18: initial draft
- 2025-02-18: ethereum research post : NTT as PostQuantum and Starks settlements helper precompile - Ethereum Research

#### External Reviews

#### Outstanding Issues

None as of 2025-02-18
