---
source: magicians
topic_id: 4552
title: Scaling Concept
author: solubrew
date: "2020-08-29"
category: Magicians > Primordial Soup
tags: [scaling]
url: https://ethereum-magicians.org/t/scaling-concept/4552
views: 1173
likes: 2
posts_count: 4
---

# Scaling Concept

I need someone to poke holes in a scaling concept that I came up with and can’t seem to get out of my head.  Currently much effort is spent mining the same block and then dumping that work when someone finds the block.  Why could we not implement a staged transaction inclusion scheme that breaks the transactions and miners into groups.  The major issue with this is obviously a double spend attack but what if you only let one transaction per address in the “active” pool at a time?  The last block mined of the active pool would select the group of transactions to be included in all of the blocks of the active pool after the next one this way the 2 groups of miners aren’t reliant on each other.  Various mechanisms implemented to random move miners between groups and clusters.  The division of work could then be clustered and distributed the added benefit here is that by imposing random clustering a 51% attack only has about 3.119% of creating a malicious block.  Any questions or insights into why this wouldn’t be feasible please let me know.

## Replies

**jpitts** (2020-09-01):

Hi [@solubrew](/u/solubrew), thanks for posting this. You might try this topic over on https://ethresear.ch; a lot more folks over there pay attention to the underlying protocol and scaling approaches!

---

**matt** (2020-09-02):

[@solubrew](/u/solubrew) what you describe sounds similar to [Prism](https://arxiv.org/abs/1909.11261). It aims to i) decrease latency and ii) improve throughput. It achieves this by breaking up the single PoW problem into `N` problems with `N` subgroups mining on them and by pipelining the transaction data to consensus nodes to avoid long propagation delays upon solving the PoW puzzle. The nice thing is that Prism uses a sortition mechanism to determine which sub-problem the miner has solved, so one miner can’t easily choose which sub-chain to mine.

I don’t follow why you’d want to only allow one tx per address, but this is something that has been suggested as a DoS protection for [Account Abstraction](https://ethereum-magicians.org/t/implementing-account-abstraction-as-part-of-eth1-x/4020). Might be worth checking out for inspiration.

---

**solubrew** (2020-09-02):

Thanks for the replies I’ll followup on the resources provided.  Spefically about the one transaction per address that is only meant to be 1 transaction per address in a block pool at a time this would stop the potential of a double spend from the same address while allowing other transactions to be validated in parallel.

