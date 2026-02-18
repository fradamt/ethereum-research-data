---
source: magicians
topic_id: 2685
title: "Data Ring Topic: Precompiles / Crypto Primitives for Data Verification"
author: tjayrush
date: "2019-02-19"
category: Working Groups > Data Ring
tags: []
url: https://ethereum-magicians.org/t/data-ring-topic-precompiles-crypto-primitives-for-data-verification/2685
views: 993
likes: 2
posts_count: 2
---

# Data Ring Topic: Precompiles / Crypto Primitives for Data Verification

There was discussion at [Denver](https://hackmd.io/s/BJlWuPNnX) about things the node could provide to help with data verification.

1. Verification of complex data relationships (e.g. pre-compiled contracts/ Zksnarks)
2. Recursive Zksnarks to prove current block is descendant of its parent block
3. Blinded attestations of transaction histories

**Action Items:** We need one!

## Replies

**tjayrush** (2019-02-19):

My take:

I’m supportive of these ideas, but I think there may be a distinction to be made between data that is intended to be fed back into the system ([see this topic](https://ethereum-magicians.org/t/data-ring-topic-real-world-data-oracles/2684)) and data that is destined to be used in outside systems. Also, there may be a fruitful distinction between what I’ll call ‘close-to-the-head’ data and ‘historical, never-changing’ data.

I know that there is technically no such thing as ‘never-changing’ data given that the chain can fork arbitrarily back into infinite history (infinitesimal), so the first thing we could agree on is ‘How old does the data need to be to never look back?’ Once we’ve made that sort of decision, then people can build systems that have to be aware of this (and handle it if needed).

Also, I’m convinced that once data becomes immutable, it’s possible to derive any further data from it (as long as you carefully exclude any ‘meta-data’) in such a way that the derived data can be as mathematically secure as the original ‘consented-to’ data. In other words, the fact that address `0x...whatever` mined block 10100 is true now and will be true for the rest of human history. We should take advantage of that.

One of the reasons why I want to make this distinction is because the “feature” of querying broadly across the entire chain–including as deeply as one wishes into its history–imposes the need for ‘sorting’ and ‘mixing’ of new and old data. An index of every miner (or every address for that matter) from every block sorted by address changes each time a new address is added to the index. This ‘adding’ and ‘sorting’ negates the benefit of publishing an historical index to a content addressable file system such as IPFS.

Another way to accomplish the same thing (make a query across every address) possible would be to publish ‘digests’ or ‘volumes’ of  addresses per some grouping function (such as after a certain number of records) and publish those digests to IPFS. This would make the data undeniable to anyone who has the ability download IPFS and has access to the hash to the digests. It solves the ‘rising price of data excludes all but the wealthy’ problem.

Another huge benefit of publishing frozen, immutable digests is that as different people query for different addresses, and the hashes of the digests is returned, and if end users then pinned those files locally, the index would naturally be distributed across the world. (in other words, we would be taking advantage of immutable data on a content addressable file system.) Furthermore, heavy users would tend to download and pin a larger number of digests (this is why per number of records is important as opposed to per time period). Smaller users (addresses with few transactions) would download (and share and store) a much smaller portion of the index.

Over time, assuming people can trust the hashes for the digests, the total number of bytes flowing through the system would decrease as users no longer need to query for their own historical transactions (since its local and pinned). Plus, this makes an improvement on the issues [discussed here](https://ethereum-magicians.org/t/data-ring-topic-provider-infrastructure-running-nodes/2683). With an index of transactions for any given address users can query directly against their own locally-running node for a full and complete audit trail of all activity on that account (i.e. permissionless auditing). This gives an incentive for more people to run more nodes because the nodes become more useful.

Sorry for the brain dump, but I’m glad that crap is now outside my head. I’d love to hear some feedback.

