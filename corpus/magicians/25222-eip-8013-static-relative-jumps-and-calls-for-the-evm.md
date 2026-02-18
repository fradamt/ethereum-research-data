---
source: magicians
topic_id: 25222
title: "EIP-8013: Static relative jumps and calls for the EVM"
author: gcolvin
date: "2025-08-24"
category: EIPs
tags: [evm, core-eips]
url: https://ethereum-magicians.org/t/eip-8013-static-relative-jumps-and-calls-for-the-evm/25222
views: 107
likes: 4
posts_count: 2
---

# EIP-8013: Static relative jumps and calls for the EVM

Discussion topic for [EIP-8013](https://eips.ethereum.org/EIPS/eip-8013)

> Five new EVM jump instructions are introduced (RJUMP, RJUMPI, RJUMPV, RJUMPSUB, and RJUMPSUBV) which encode destinations as signed immediate values. These can be useful in almost all JUMP and JUMPI use cases and offer improvements in cost, performance, and static analysis.

#### Update Log

- 2025-09-05: initial draft

#### External Reviews

- yyyy-mm-dd: Single sentence description, link to review

#### Outstanding Issues

 yyyy-mm-dd: Issue description, link to issue

## Replies

**gcolvin** (2025-09-16):

Note:  For lack of EOF, this EIP may well depend on the safe immediate encodings introduced here:

[Update EIP-663: Remove EOF requirement, introduce safe immediate encoding](https://github.com/ethereum/EIPs/pull/10298/)

But see also [@frangio](/u/frangio)’s discussion of [EVM Immediates](https://ethereum-magicians.org/t/evm-immediates/25605/2)

