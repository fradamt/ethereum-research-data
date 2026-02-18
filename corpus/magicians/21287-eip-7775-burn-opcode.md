---
source: magicians
topic_id: 21287
title: "EIP-7775: BURN opcode"
author: itsdevbear
date: "2024-10-07"
category: EIPs > EIPs core
tags: [token, evm, opcodes]
url: https://ethereum-magicians.org/t/eip-7775-burn-opcode/21287
views: 186
likes: 1
posts_count: 1
---

# EIP-7775: BURN opcode

This proposal introduces a new `BURN` opcode to burn native tokens at the given address. Right now burning tokens involves just sending them to some unrecoverable address, and/or for smart contracts with intended burn functionality, just letting them sit in the contract forever.

https://github.com/ethereum/EIPs/pull/8914
