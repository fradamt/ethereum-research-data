---
source: magicians
topic_id: 7493
title: Ultimate Heavy IO Relief
author: jessielesbian
date: "2021-11-17"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/ultimate-heavy-io-relief/7493
views: 726
likes: 2
posts_count: 4
---

# Ultimate Heavy IO Relief

I have an idea for a new optimization technique that will definitely relieve the heavy IO loads on Ethereum nodes. My idea extends the EIP-2200 gas refunds to the block level, not just the transaction level. My idea involves a ‘state cache’ that stores frequently-used storage slots in RAM and gives out heavy gas discounts for reads and writes to those storage slots.

Every time a storage slot is accessed, it’s considered hot and is cached for the next 5 blocks. Reads or writes to a hot storage slot would not follow normal storage gas metering rules. Instead, reads and writes to hot storage slots should cost 10 gas for reads and 50 gas for writes.

## Replies

**mlaw** (2021-11-27):

Given that hot slots are probably cached in-memory via the kernel buffer cache, I’m not sure this will much improvement on (disk) IO. But I like the idea of a discounts for such accesses as it’s a good incentive. This would be kinda like a generalization of EIP-2930 for all transactions, with possibly better UX since knowing which slots will be accessed isn’t always feasible.

---

**hmijail** (2021-11-27):

Imagine you wanted to take advantage of this mechanism. You send your transaction and want it to get the mentioned “discounts”. How would you actually do it? How do you know which slots are hot when your transaction runs?

Apart from that, this technique ignores the actual problem in the way a regular Ethereum client accesses its DB. Not only the kernel, but the DB engines already go to lengths to cache stuff and be fast, possibly taking into account hardware characteristics - that’s their whole job. And still, the heavy IO remains a problem, because it’s intrinsic to the way in which the Ethereum state is typically stored.

You might be interested to read how the Erigon client works to fix that problem: [GitHub - ledgerwatch/erigon: Ethereum implementation on the efficiency frontier](https://github.com/ledgerwatch/erigon#more-efficient-state-storage)

---

**matt** (2021-11-27):

Probably a good time to review this gist: [Caching.md · GitHub](https://gist.github.com/holiman/2fae5769b0334b857443b53a5aa746ec)

