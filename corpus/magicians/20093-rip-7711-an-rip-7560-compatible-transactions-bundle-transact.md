---
source: magicians
topic_id: 20093
title: "RIP-7711: An RIP-7560 compatible transactions bundle transaction type"
author: alex-forshtat-tbk
date: "2024-05-23"
category: RIPs
tags: [account-abstraction, rip]
url: https://ethereum-magicians.org/t/rip-7711-an-rip-7560-compatible-transactions-bundle-transaction-type/20093
views: 536
likes: 6
posts_count: 3
---

# RIP-7711: An RIP-7560 compatible transactions bundle transaction type

The original RIP-7560 previously required a separation of a Native Account Abstraction transaction flow into non-atomic validation frame and execution frame.

We now believe that this separation may not be necessary for some L2 implementations, so this separation of transactions into non-atomic parts has been extracted into a separate document here:

https://github.com/ethereum/RIPs/pull/22

## Replies

**colinlyguo** (2025-05-07):

Hey, I have a question related to the motivation for this RIP. It mentions:

> On “single sequencer” Layer 2 chains that do not have a “transaction mempool” in a traditional sense, this proposal provides no benefit compared to the original RIP-7560.

This claim seems to have an assumption that the sequencer will serve transactions in a first-come first-served order, so it won’t be bothered by state conflicts among native aa transactions.

However, if the sequencer picks transactions from a public mempool based on factors like effective gas tip, this RIP could still help mitigate state conflicts among native AA transactions. Am I understanding this correctly?

---

**alex-forshtat-tbk** (2025-05-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/colinlyguo/48/13417_2.png) colinlyguo:

> However, if the sequencer picks transactions from a public mempool based on factors like effective gas tip, this RIP could still help mitigate state conflicts among native AA transactions. Am I understanding this correctly?

Yes, you are correct, as long as there exists an open mempool of AA transactions and the sequencer, or a block builder, mostly relies on transactions from this mempool, we need a mechanism to isolate the transactions or else the block builder may “choke” on a huge number of invalid AA transactions.

In this moment in time it does not matter if this is a centralised sequencer or a PoS validator, they both will have the same problem.

Our proposed solution to this problem is a combination of RIP-7711 and ERC-7562.

