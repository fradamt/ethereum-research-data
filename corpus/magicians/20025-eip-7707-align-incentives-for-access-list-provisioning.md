---
source: magicians
topic_id: 20025
title: "EIP 7707: Align incentives for access list provisioning"
author: benaadams
date: "2024-05-16"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7707-align-incentives-for-access-list-provisioning/20025
views: 964
likes: 3
posts_count: 4
---

# EIP 7707: Align incentives for access list provisioning

To facilitate future developments of parallel data load, we need to encourage as many transactions as possible that contain as complete and valid access lists. Current access list pricing does not sufficiently incentivize their inclusion, and this EIP aims to address this gap.

https://github.com/ethereum/EIPs/pull/8563

## Replies

**OlegJakushkin** (2024-05-16):

- Oked by CI
- @vbuterin, @holiman, please take a look.

---

**vbuterin** (2024-05-22):

This would *massively* increase the theoretical max number of state accesses in a block, to the point of making statelessness and even running regular nodes in some contexts unviable.

Today, the theoretial max accesses per block is 30000000 / 1900 = 15789. This EIP would increase that to 30000000 / 320 = 93750.

Given that we’re already struggling to make Verkle tree updates, and in the future STARKs over Binary tree branches, fast enough, I don’t think we can handle this increase.

I feel like if we want to take this path, we should actually do the other direction, and make outside-the-list accesses *more expensive*, though start with a gentler ratio (eg. 1.5) at first.

---

**benaadams** (2024-05-22):

If increasing the non-access list price, what about significantly dropping the warm SLOAD, TLOAD price at same time?



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/benaadams/48/9199_2.png)
    [EIP-7609 reduce transient storage pricing](https://ethereum-magicians.org/t/eip-7609-reduce-transient-storage-pricing/18435/24) [Core EIPs](/c/eips/core-eips/35)



> One element of calldata is VeryLow (3) + Memory (3) => 6; so is question if TLOAD should be lower than calldata
> So maybe something like
> SLOAD cold => 2100 (Unchanged)
> SLOAD warm => 6 (CallData 1 Word Read)
> TLOAD => 6 (CallData 1 Word Read)
> TSTORE => 10 (High) + inclusion in Memory expansion cost at x2 (key+value)
> SSTORE => Unchanged
> While SLOAD and TSTORE are slightly more complicated than a call data read; call data also includes 3 pops vs 1 pop for the loads, so evens out  …

