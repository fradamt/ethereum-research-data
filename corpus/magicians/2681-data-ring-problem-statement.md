---
source: magicians
topic_id: 2681
title: "Data Ring: Problem Statement"
author: tjayrush
date: "2019-02-19"
category: Working Groups > Data Ring
tags: []
url: https://ethereum-magicians.org/t/data-ring-problem-statement/2681
views: 1112
likes: 1
posts_count: 3
---

# Data Ring: Problem Statement

According to the [Denver notes](https://hackmd.io/s/Sy6g5I7B4#), we agreed that the problem we’re trying to solve is:

> Its difficult to get the data out, and also to get the data in

A couple of questions for discussion:

1. Does the above description capture what we’re trying to solve? (Here’s notes from the Prague data ring. There are some concerns voiced there.
2. Would it make sense to break into two different sub-rings? Data Extraction / Oracles? (This issue came up in the ring discussion.) I think maybe we should have two subrings.
3. Should there be a third subring: Data Delivery. (This might include data marketplaces, IPFS delivery, Web 2.0 server/API delivery, others)

Please discuss the issue of the ring’s “Problem Statement” What are we trying to solve?

## Replies

**jpitts** (2019-02-21):

Question 1.

I think that the problem statement or “mission” might mention additional pain points, data use cases, main stakeholders in this.

So something like:

> “Making use of data is key to using the Ethereum network, whether it originates from the blockchain itself or from other sources. End-users, dapp developers, and network operators are stakeholders in valuable data use cases and this Ring aims to understand and address their pain points.”

Question 2.

As for side Rings … side is better than sub ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) … perhaps let’s see which of these further topics stick.

[Query Interface / Underlying Data](https://ethereum-magicians.org/t/data-ring-topic-query-interface/2682)

[Provider Infra / Running Nodes](https://ethereum-magicians.org/t/data-ring-topic-provider-infrastructure-running-nodes/2683)

[Oracles / External Data](https://ethereum-magicians.org/t/data-ring-topic-real-world-data-oracles/2684)

[Data Verification](https://ethereum-magicians.org/t/data-ring-topic-precompiles-crypto-primitives-for-data-verification/2685)

Question 3.

Yes, but as with the others, we need a champ.

---

**jpitts** (2019-02-21):

Also, would Data Ring be involved with maintaining JSON-RPC?

