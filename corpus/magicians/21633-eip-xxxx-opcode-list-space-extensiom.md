---
source: magicians
topic_id: 21633
title: "EIP-XXXX: Opcode list space extensiom"
author: Zoltan
date: "2024-11-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-xxxx-opcode-list-space-extensiom/21633
views: 50
likes: 1
posts_count: 1
---

# EIP-XXXX: Opcode list space extensiom

Note: Have not created PR yet, as it is advised to get recommendations.

Abstract:

Two new opcodes: EXTEND1, EXTEND2

EXTEND1 takes 1 byte from stack, the byte identifies an opcode from 0xFF-0x1FD

EXTEND2 takes 2 bytes from stack, the byte identifies an opcode or a precompile from 0x1FE-101FC or from 0x1FE-101F and the lowest nibble contains contextual switches, for example over&underflow check where the first stack item is the result of the check: 1= overflow 2= underflow.

I think we should use the remaining entries from the 1 byte long opcode table for more common instructions like the unimplemented CLZ for example, and add only a few special opcodes for handling a program’s state in the blockchain context.
