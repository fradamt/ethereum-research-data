---
source: magicians
topic_id: 12884
title: "EIP-6466: SSZ Receipts"
author: etan-status
date: "2023-02-08"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-6466-ssz-receipts/12884
views: 2041
likes: 0
posts_count: 7
---

# EIP-6466: SSZ Receipts

Discussion thread for [Add EIP-6466: SSZ receipts root by etan-status · Pull Request #6466 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6466)

# Background

Split from [EIP-6404: SSZ Transactions](https://ethereum-magicians.org/t/eip-6404-ssz-transactions/12783)

Relevant channel: `#typed-transactions` on ETH R&D Discord

## Transactions

Vitalik’s notes: [Proposed transaction SSZ refactoring for Cancun - HackMD](https://notes.ethereum.org/@vbuterin/transaction_ssz_refactoring)

#### Update log

- 2025-07-02: Adopt ProgressiveContainer

## Replies

**etan-status** (2023-02-28):

One feedback from discord was that the per-receipt logs bloom field may be unnecessary: [Discord](https://discord.com/channels/595666850260713488/779922457631916064/1079878531066101850)

---

**jflo** (2023-04-20):

uint256 seems like overkill for transaction status, which per the mentioned EIP-658 is a single bit. Do we foresee overloading this field in the near future?

---

**etan-status** (2023-04-20):

It had a historic meaning of representing an intermediate state root instead of the status bit. This is still prevalent in the devp2p protocol: [devp2p/eth.md at bd17dac4228c69b6379644355f373669f74952cd · ethereum/devp2p · GitHub](https://github.com/ethereum/devp2p/blob/bd17dac4228c69b6379644355f373669f74952cd/caps/eth.md#receipt-encoding-and-validity)

```auto
post-state-or-status: {B_32, {0, 1}},
```

I don’t think that the `post-state` case can happen at this time. If there are no new use cases that need the full width of this field, it could be reduced to a `bool` instead.

---

**etan-status** (2023-08-30):

Updated to use [EIP-6493](https://eips.ethereum.org/EIPS/eip-6493) `Receipt`.

This addresses design space concerns while retaining the merkleization benefits of common fields sharing the same generalized index.

---

**etan-status** (2024-10-08):

Updated once more: [Update EIP-6404: Add `from`, `authorities`, and drop `logs_bloom` by etan-status · Pull Request #8939 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8939)

This now includes [EIP-7668: Remove bloom filters](https://eips.ethereum.org/EIPS/eip-7668), and syncs with the latest EIP-7702 Set Code transaction changes and EIP-6404 transaction changes.

---

**etan-status** (2025-07-02):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9966)














####


      `master` ← `etan-status:6466-progressive`




          opened 09:10AM - 02 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/89844309?v=4)
            etan-status](https://github.com/etan-status)



          [+72
            -28](https://github.com/ethereum/EIPs/pull/9966/files)







- `logIndex` now based per receipt rather than entire block
- Switch to `Progre[…](https://github.com/ethereum/EIPs/pull/9966)ssiveContainer` / `CompatibleUnion` based design












- logIndex now based per receipt rather than entire block
- Switch to ProgressiveContainer / CompatibleUnion based design

