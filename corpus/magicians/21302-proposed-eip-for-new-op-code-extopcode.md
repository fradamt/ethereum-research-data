---
source: magicians
topic_id: 21302
title: "Proposed EIP For New Op Code: `extopcode`"
author: nathanglb
date: "2024-10-08"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/proposed-eip-for-new-op-code-extopcode/21302
views: 56
likes: 1
posts_count: 1
---

# Proposed EIP For New Op Code: `extopcode`

EVM op codes are only 1-byte long, so the most “core” op codes that can ever exist is 255.  Thus, any new op codes must be carefully vetted, and many are rejected.

This proposal suggests the addition of an `extopcode` op code.  When present, a two-byte extension opcode would follow.  With 2-byte extension op codes, it would open the door to 65,535 new op codes, which could make it easier to get new functionality incorporated into the EVM.

No official EIP has been drafted.  This is intended to kick start a discussion about it.
