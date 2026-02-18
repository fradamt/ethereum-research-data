---
source: magicians
topic_id: 24510
title: Increase LOG Opcode Cost
author: Giulio2002
date: "2025-06-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/increase-log-opcode-cost/24510
views: 60
likes: 1
posts_count: 1
---

# Increase LOG Opcode Cost

This EIP proposes to change the gas cost calculation for the `data` field of the LOG opcodes from being charged 8 gas per byte to 32 gas per byte. This adjustment is intended to maintain network stability and prevent blocks from exceeding the devp2p 10 MiB size limit as block gas limits increase. Additionally, it increases both the base cost for LOGN opcodes and the additional cost per topic to 1095 gas from 375 gas.
