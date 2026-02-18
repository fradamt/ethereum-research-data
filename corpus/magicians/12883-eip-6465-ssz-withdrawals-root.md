---
source: magicians
topic_id: 12883
title: "EIP-6465: SSZ Withdrawals Root"
author: etan-status
date: "2023-02-08"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-6465-ssz-withdrawals-root/12883
views: 2319
likes: 1
posts_count: 7
---

# EIP-6465: SSZ Withdrawals Root

Discussion thread for [EIP-6465: SSZ withdrawals root](https://eips.ethereum.org/EIPS/eip-6465)

EIP-4895 reference:

- EIP-4895: Beacon chain withdrawals as system-level operations - #50 by etan-status

# Background

Split from [EIP-6404: SSZ Transactions](https://ethereum-magicians.org/t/eip-6404-ssz-transactions-receipts-and-withdrawals/12783)

Relevant channel: `#ssz` on ETH R&D Discord

#### Update Log

- 2025-07-03: Adopt ProgressiveContainer / ProgressiveList

## Replies

**matt** (2023-02-08):

I would personally much rather see all the SSZ changes in 1 EIP. It will be easier to discuss and reason about.

---

**etan-status** (2023-02-09):

Splitting the changes into multiple EIPs allows more rollout flexibility; it is not necessary to bundle them in the same release.

This also allows more focused discussion on individual topics. For example, the Union/Onion vs normalized type discussion does not affect withdrawals. And the SSZ `Optional` may be useful irrespective of the root format in the execution block header, e.g., for EIP-4844.

However, I can also understand the desire to see all changes on 1 page, though. Hopefully, once the PRs are merged, [Core | Ethereum Improvement Proposals](https://eips.ethereum.org/core) can be used to regain that overview.

---

**matt** (2023-02-09):

I’m just speaking from the experience of EOF – I think the fractured spec caused much more trouble than was worth. Plus I generally don’t think we should move the accumulators to SSZ piecewise and should instead do them all together.

---

**jflo** (2023-04-25):

Mostly agree with this idea of consolidating SSZ related EIPS, however I would stop short of including EIP-6493 with the others. 6466, 6465 and 6404 are all improvements to how accumulators work by leveraging SSZ merkleization, and so designing (if not but maybe also delivering) them together makes sense.

---

**etan-status** (2023-08-30):

Added typed withdrawal envelope to EIP-6465 to support exchange of SSZ `Withdrawal`; this is the same mechanism as defined in EIP-6493 / EIP-2718

Regarding EIP consolidation, the withdrawals EIP (EIP-6465) seems less connected to the transactions (EIP-6404) / receipts (EIP-6466) ones.

---

**etan-status** (2025-07-03):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9974)














####


      `master` ← `etan-status:6465-progressive`




          opened 09:36AM - 03 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/89844309?v=4)
            etan-status](https://github.com/etan-status)



          [+27
            -20](https://github.com/ethereum/EIPs/pull/9974/files)







Use EIP-7495 / EIP-7916 for forward compatibility.












- Use EIP-7495 / EIP-7916 for forward compatibility.

