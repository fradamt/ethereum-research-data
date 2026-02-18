---
source: magicians
topic_id: 7363
title: "EIP-4396: Time-Aware Base Fee Calculation"
author: adietrichs
date: "2021-10-29"
category: EIPs > EIPs core
tags: [eip-1559]
url: https://ethereum-magicians.org/t/eip-4396-time-aware-base-fee-calculation/7363
views: 2456
likes: 3
posts_count: 2
---

# EIP-4396: Time-Aware Base Fee Calculation

This EIP proposes accounting for time between blocks in the base fee calculation to target a stable throughput by time, instead of by block. It appears to be desirable to have something like this in place already for the merge, to avoid (or at least greatly reduce) throughput degradation due to missed slots, or even due to potential consensus issues.

To maximize the chance of this EIP being included in the merge fork, the adjustments are kept to a minimum, with more involved changes discussed in the rationale section.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4396)














####


      `master` ← `quilt:time-aware-basefee`




          opened 03:59AM - 29 Oct 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8a50f6f985d5442bad261d7c3f7243ce2fdf90a9.jpeg)
            adietrichs](https://github.com/adietrichs)



          [+158
            -0](https://github.com/ethereum/EIPs/pull/4396/files)







This EIP proposes accounting for time between blocks in the base fee calculation[…](https://github.com/ethereum/EIPs/pull/4396) to target a stable throughput by time, instead of by block. Aiming to minimize changes to the calculation, it only introduces a variable block gas target proportional to the block time. The EIP can, in principle, be applied to either a Proof-of-Work or a Proof-of-Stake chain, however the security implications for the Proof-of-Work case remain unexplored.

## Replies

**barnabe** (2021-11-12):

For future reference, a note with some arguments for the properties of various fee market modifications.

[Note](https://notes.ethereum.org/@barnabe/HkUg2pLUK)

