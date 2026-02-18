---
source: magicians
topic_id: 12765
title: Introduce Opcodes B0 DUPN and B1 SWAPN (ignore)
author: green
date: "2023-01-31"
category: Uncategorized
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/introduce-opcodes-b0-dupn-and-b1-swapn-ignore/12765
views: 712
likes: 1
posts_count: 2
---

# Introduce Opcodes B0 DUPN and B1 SWAPN (ignore)

I mainly want to understand why only the 16 first elements of the stack can be interacted with, and start a conversation about introducing two opcodes that could allow for all stack elements to be brought forward

- was there any security consideration when adding this limitation? (like, not allowing other functions to tamper with previous stack?)
- was it just intended to keep the DUP and SWAP mechanic simple? (by not needing to deal with the N element of the stack)
- if DoS, could it get compensated by increasing gas costs?

DUPN: pops the passed N and pushes the nth element of the stack (Nth considered after consuming the N)

[3, 10, 11, 12, 13, 14] =>

[13, 10, 11, 12, 13, 14]

SWAPN: pops the passed N and swaps the now first and nth element of the stack (Nth considered after consuming the N)

[3, 10, 11, 12, 13, 14] =>

[13, 11, 12, 10, 14]

N > 1023 reverts

gas could be larger than their shorter counterparts, if there were any DoS concerns

## Replies

**gumb0** (2023-01-31):

This was proposed many times, see latest version of the proposal at [EIP-663: Unlimited SWAP and DUP instructions](https://eips.ethereum.org/EIPS/eip-663)

