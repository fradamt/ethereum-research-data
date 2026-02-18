---
source: magicians
topic_id: 24039
title: Paginated getLogs
author: sakulstra
date: "2025-05-04"
category: Working Groups > Provider Ring
tags: []
url: https://ethereum-magicians.org/t/paginated-getlogs/24039
views: 208
likes: 5
posts_count: 5
---

# Paginated getLogs

### Motivation

When I first entered this space >4 years ago, the first thing i built was an indexer for the aave protocol. Now 4years later, looking at this app not much has improved and I would probably do it the same way again.

Indexing events should be easy, but it is not.

Perhaps i might be able to do [a few calls less](https://ethereum-magicians.org/t/proposal-for-adding-blocktimestamp-to-logs-object-returned-by-eth-getlogs-and-related-requests/11183), or I might be able to use alchemy* on L2s, but the core pain of `eth_getLogs` persists.

- there is no cursor
- there is no handling of reorgs
- constant block-range limits on increasingly faster chains are pain

Running an archive node myself, might be possible, but it’s a huge barrier of entry for “getting started”.

While the bigger providers, started to offer custom built solutions for the problem ([pipelines](https://www.alchemy.com/pipelines) by alchemy, and [streams](https://www.quicknode.com/streams) by quicknode), these solutions require a vendor lock in, so there should be a feasible node level alternative imo.

### Spec

My knowledge on the topic is at best, limited. Therefore I will not suggest any specific spec.

That said, I assume a new method would need to be introduced to not break existing `eth_getLogs` usage.

My naive assumptions is that:

1. fromBlock should also accept a blockHash. This way *getLogs could return removed: true events, if the fromBlock was reorged.
2. if the search range exceeds some sort of limit on the archive node, the node should just return (not error) and the return should contain the last visited blockHash, so on the next query one can continue from there.

Perhaps it could make sense to have a more complex cursor including e.g. a `txIndex`. I assume with ever growing blocks one might end up in a situation where one block might exceed the node limits (iirc. there was some issue with infura in the past).

### Prior work

There seem to be two related prs that i could find:

- Proposal: Paginated Filter Queries ethereum/go-ethereum#17487 i think the first time this issue was raised, but eventually the topic has gotten stale
- JSONRPC responses with cursor/paging · Issue #617 · ethereum/execution-apis · GitHub a somewhat newer thread on the topic, with what i think are bot responses
- predictable block ranges when using eth_getLog · Issue #10606 · paradigmxyz/reth · GitHub slightly unrelated, but seems like ppl have pushed to get at least alchemy level feature parity accross clients

*In contrast to other node providers, alchemy does not implement a strict maximum blockRange, but allows for a dynamic range / suggest a dynamic range if the range contained to many matches `Based on your parameters, this block range should work: [0x0, 0x270f]`

edit: I was not aware before posting, but there is a [tg group](http://t.me/blockchain_data_standards) discussing a new standard

## Replies

**wjmelements** (2025-05-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sakulstra/48/15100_2.png) sakulstra:

> there is no handling of reorgs

Large reorgs don’t really happen anymore, and if you use a logs subscription they come with a `removed` field, which *does* handle reorgs.

---

**sakulstra** (2025-05-14):

> Large reorgs don’t really happen anymore,

That’s only partially true. On ethereum yes, but ethereum sets the baseline for a lot of other l1/l2s - also it does not really matter if large or not.

> and if you use a logs subscription they come with a removed field, which does handle reorgs.

Websockets, are only supported by a subset of node providers, stateful connections are not suitable for all use-cases and even if you use websockets, you still need to handle connection drops.

I’m not saying there are no workarounds. People obviously work around these issues, but it must be acknowledged that the default experience currently is quite bad and should be improved.

---

Also i want to emphasize that handling reorgs would just be a nice side effect of better getLogs. The main thing boosting dx would be pagination which could even be necessary given ever increasing blocksize.

---

**wjmelements** (2025-05-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/sakulstra/48/15100_2.png) sakulstra:

> Websockets, are only supported by a subset of node providers

The way to do it without websockets (eth_subscribe) is with filters (eth_newFilter). Don’t use providers that don’t support subscriptions or filters. If they won’t provide the good API that lets you notice log removals they are ripping you off by forcing you to make extra requests. With so many alternatives there’s no excuse. You can just use anyone else, or run your own node.

---

**sakulstra** (2025-05-27):

`eth_newFilter` has different limitations though.

Anyhow, i feel like the conversation has derailed a bit.

I feel that when “fixing” getLogs, reorgs should be handled so you don’t need other workarounds, but overall the notes about reorgs are secondary.

If you want to query all events for a contract from block `0` to `now`, the current getLogs is problematic.

- with a max blockRange of 10_000 you’d need > 2000 calls, no matter if there is one or thousands of events. On l2s more.
- with bigger blocks and shorter block times the problem will get worse
- the current api leads to ppl doing workarounds and optimizations in userland that should be on the node level*

*Imagine you want to index a contract, but you don’t know when it was deployed.

There is no standardized api to get the the deployment txn/block, so ppl do binary search to then do getLogs.

---

On a side-note, since I created this post alchemy disabled the range recommendation(they always recommend 10k blockRange) for all chains but mainnet, so on L2s getLogs for historical indexing is now unusable.

