---
source: magicians
topic_id: 1458
title: Towards a stateless node API
author: Arachnid
date: "2018-09-25"
category: Working Groups > Ethereum Architects
tags: [json]
url: https://ethereum-magicians.org/t/towards-a-stateless-node-api/1458
views: 2251
likes: 12
posts_count: 18
---

# Towards a stateless node API

By and large the JSON-RPC API that nodes expose is stateless; each call to the API is independent. The exception to this is filters; they carry state across multiple requests, requiring a caller to first configure a filter, then to poll it. This has several issues:

- It requires the node to handle and retain state between calls
- It requires nodes to figure out when to garbage-collect obsolete state
- It introduces permissioning issues - if an endpoint has multiple callers, there’s no way to ensure only the creator can modify, poll, or delete a filter.
- It still requires polling for new events, since the supported transports don’t use push notifications.
- It introduces DoS vulnerabilities for public nodes, since they can be asked to retain large amounts of state for open filters.
- If a node or an app restarts, there’s still no way for the app to be sure they didn’t miss any events or reorgs while the filter was offline.

As a result, public JSON-RPC APIs like INFURA don’t offer filters. Stateful filters are also difficult for apps to use properly, meaning many apps that might benefit from event logs don’t use them as much as they otherwise would.

What we need is an effective way to get event logs that is stateless and respects reorgs. `eth_getLogs` fulfils the first of these criteria, exposing the filter API in a stateless fashion, but simply polling it won’t handle reorgs. Handling them properly requires complex code that checks whether the block hash for recent events is still part of the canonical chain.

As a first step towards fixing this, I’m proposing the following change: Make log filters accept block hashes for the `fromBlock` and `toBlock` arguments, instead of just block numbers. When fetching logs for a range, the process then becomes:

1. Find the first common ancestor of fromBlock and toBlock; call it ancestor
2. Fetch any matching events between ancestor and fromBlock and emit them with removed: true
3. Fetch any matching events between ancestor and toBlock and emit them as normal

As a result, anyone can poll for filtered events by repeatedly calling `eth_getLogs`, each time supplying the block hash of the last event received as `fromBlock`, and be assured that they will be informed of any events removed by reorgs.

I’ve implemented this for go-ethereum in [this PR](https://github.com/ethereum/go-ethereum/pull/17743), and I’d love to see it adopted as an extension of the JSON-RPC standard across other clients.

Thoughts?

## Replies

**hiddentao** (2018-09-25):

I think the two tasks - watching for blocks and parsing logs - should be done separately.

How I would have it: You should be able to subscribe to incoming block numbers. And then, though block no. X has come and gone, I might want to wait until X + 10 before I process X (this takes care of re-orgs). Once I’m ready to process X I can fetch its data (by block number) from the node and use a separate parser to extract the events I’m interested in from the block logs.

The assumption being made here is that block numbers are always ordered correctly, which I think is a fair assumption to make.

---

**Arachnid** (2018-09-25):

Nodes are able to filter and parse logs a lot more efficiently than a client can. Having clients fetch every log for the network and parse logs out of it will impose a lot of unnecessary load on nodes, as well as adding unnecessary functionality to every app that wants to understand logs.

---

**hiddentao** (2018-09-25):

I think that doing the filtering on the node itself has more weight as an argument if/when Ethereum transaction throughput hits many many multiples of what it is today, since perhaps clients (and in particular resource constrained ones) would be better off not doing such parsing at that point.

But even then (and in particular for servers which are watching the blockchain), it makes sense to me have a log streaming API which can be subscribed to. Thus clients can then choose whether to process log themselves or not. As for clients needing to have the parsing logic within, that’s easily solved through libraries (of which there are already a few).

My argument mainly stems from the poor state of log filtering today via Web3 and other APIs, as you’ve outlined. If you can’t rely on the node doing a good job for you you have it do it yourself.

---

**juanfranblanco** (2018-09-25):

I believe that both scenarios are valid, another scenario you maybe watching many events from different contracts and it is more efficient to get the transaction receipt logs, and do the work locally.

On the other hand, I totally agree with just using get_logs, there should not be a dependency on a single client, I personally see the rpc server clients as the lightest client layer. Although it whilst not for this topic (food for thought) I would like to see the capability to verify rpc calls with multiple clients.

---

**Arachnid** (2018-09-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddentao/48/16854_2.png) hiddentao:

> I think that doing the filtering on the node itself has more weight as an argument if/when Ethereum transaction throughput hits many many multiples of what it is today, since perhaps clients (and in particular resource constrained ones) would be better off not doing such parsing at that point.

We already have a filter API that allows the nodes to flexibly select logs that you care about, though. What purpose would abandoning it serve?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddentao/48/16854_2.png) hiddentao:

> But even then (and in particular for servers which are watching the blockchain), it makes sense to me have a log streaming API which can be subscribed to. Thus clients can then choose whether to process log themselves or not. As for clients needing to have the parsing logic within, that’s easily solved through libraries (of which there are already a few).

That’s pretty much exactly what I’m proposing here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddentao/48/16854_2.png) hiddentao:

> My argument mainly stems from the poor state of log filtering today via Web3 and other APIs, as you’ve outlined. If you can’t rely on the node doing a good job for you you have it do it yourself.

What problems do you see with filtering today? The one problem I see, as I outlined in my original post, is the statefulness of the API, which my proposal aims to fix.

---

**MicahZoltu** (2018-09-25):

I agree that the current system is bad and should be removed because it causes so many people to fall into the trap of using it and then being surprised when unexpected behavior occurs.

I disagree with the solution though because it still leaves a hole.  In particular, if you have blocks 1-5 (by hash) and you request “logs since block 5 (by hash)”, there is no guarantee that what you have for block 5 is still part of the canonical chain, thus no guarantee that the client you are talking to still knows what that hash is.  As you indicated, requesting blocks by number has its own set of problems, but *just* requesting by hash doesn’t fully solve the problem.

I am of the belief that in order for a client to correctly process blocks using a stateless protocol with the node, they *must* maintain their own view of the blockchain back some number of blocks.  This *must* happen in the client failure domain and cannot happen in the node failure domain unless the node is storing (indefinitely) state on behalf of the client (which I agree with you, is bad).

A while back I wrote ethereumjs-blockstream to handle all of these rough corners.  It maintains the last `n` (default 100) blocks in memory in the client and when it gets a new block it makes sure that it can reconcile with its in-memory chain, which means it will walk back fetching blocks until it can connect the two chains (or it runs off the end of what it has in memory).  This is necessary for making sure that we see all blocks (in order) and remove blocks (in order) when a reorg occurs regardless of whether we are talking to the same backend or we are talking to a different backend every time.  It results in being eventually consistent with the node you are talking to and doesn’t rely on any state being stored in the node on behalf of the client.

The library *also* handles fetching logs for each block it sees for you, but it doesn’t do so by range, only one block at a time and by hash (in the vNext version since fetching logs by hash is not in stable versions of all clients yet).

In general, I do not find much value in fetching large ranges of logs *near head*.  If you want to fetch a large range of logs, you should fetch up to something like `head - 10` and then use something like blockstream to play near head.  There are just too many rough edges when fetching logs near head, and in almost all cases you *also* want to fetch blocks near head and in order to not end up in an inconsistent state I do not think you should be batch fetching logs and batch fetching blocks as separate processes near head.

---

**Arachnid** (2018-09-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I disagree with the solution though because it still leaves a hole. In particular, if you have blocks 1-5 (by hash) and you request “logs since block 5 (by hash)”, there is no guarantee that what you have for block 5 is still part of the canonical chain, thus no guarantee that the client you are talking to still knows what that hash is. As you indicated, requesting blocks by number has its own set of problems, but just requesting by hash doesn’t fully solve the problem.

Good point. I don’t think it’s unreasonable for individual nodes to hold recent uncles for at least a while, but it does raise the issue of how to handle GC for old uncles, and how to handle cases where the API isn’t served by just one node.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I am of the belief that in order for a client to correctly process blocks using a stateless protocol with the node, they must maintain their own view of the blockchain back some number of blocks. This must happen in the client failure domain and cannot happen in the node failure domain unless the node is storing (indefinitely) state on behalf of the client (which I agree with you, is bad).

That’s a pretty steep requirement, though - especially since there’s currently no exposed API that facilitates figuring out what events need removing in an easy fashion.

The information in received events ought to be enough to figure out which of them have been reorged, since they contain block numbers and hashes; what’s missing here is an efficient way to query the server to see which ones need to be removed and where it can pick up from.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> In general, I do not find much value in fetching large ranges of logs near head . If you want to fetch a large range of logs, you should fetch up to something like head - 10 and then use something like blockstream to play near head. There are just too many rough edges when fetching logs near head, and in almost all cases you also want to fetch blocks near head and in order to not end up in an inconsistent state I do not think you should be batch fetching logs and batch fetching blocks as separate processes near head.

Can you elaborate on why? In an ideal world, it’d be possible to just say “give me all logs matching this filter from block x onwards” and not have to worry about one means of fetching ‘old’ logs and another for ‘new’ logs as we do at present.

---

**MicahZoltu** (2018-09-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> In an ideal world, it’d be possible to just say “give me all logs matching this filter from block x onwards” and not have to worry about one means of fetching ‘old’ logs and another for ‘new’ logs as we do at present.

The set of dapps where this is the only question you want to ask is pretty limited, and searching by block number is good enough to satisfy the requirement.  However, in most real-world dapps, you want to receive a stream of logs as they come in, with enough additional information to know when they disappear.  I do not believe it is possible to do this entirely in a different failure domain unless that other failure domain is retaining history indefinitely for you (see the issue above of a client asking a node to resume processing from a block that the node doesn’t know about because it has long since been reorged out).

Due to the above, the client must retain its own history that includes things that “may be reorged out” (e.g., have not achieved some level of desired finality).  Since the client is already storing that state, it is easiest to just let the client deal with reorgs in its own failure domain rather than trying to have the node deal with reconciliation of new blocks on behalf of the client.

I believe with the recent addition of being able to fetch filtered logs by block, this problem is fully solvable client side and there already exists tooling to do so (ethereumjs-blockstream).  While it would be nice if we could fully solve the problem node-side, I do not think it is possible to fully solve node side and I would prefer to not introduce/advocate for/support an API that has sharp corners like “this API works unless you lose connectivity for long enough that the node GCs the last block you received which was reorged out”.  Such an edge is one of those that makes it past all QA and then results in random hard to debug errors that end-users experience because they are fairly uncommon, but common enough that they do happen in the wild with some amount of frequency.

---

**Arachnid** (2018-09-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> The set of dapps where this is the only question you want to ask is pretty limited, and searching by block number is good enough to satisfy the requirement. However, in most real-world dapps, you want to receive a stream of logs as they come in, with enough additional information to know when they disappear.

Right, I was assuming that the stream would also include reorged-out events. My point was that dapps shouldn’t have to build different code to handle fetching ‘old’ events and ‘new’ ones, and they shouldn’t have to explicitly poll for new blocks.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I believe with the recent addition of being able to fetch filtered logs by block, this problem is fully solvable client side and there already exists tooling to do so (ethereumjs-blockstream).

Why is being able to fetch logs from a specific block important here? Why not just use a range query?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I do not think it is possible to fully solve node side and I would prefer to not introduce/advocate for/support an API that has sharp corners like “this API works unless you lose connectivity for long enough that the node GCs the last block you received which was reorged out”.

I reluctantly agree.

---

**MicahZoltu** (2018-09-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Right, I was assuming that the stream would also include reorged-out events. My point was that dapps shouldn’t have to build different code to handle fetching ‘old’ events and ‘new’ ones, and they shouldn’t have to explicitly poll for new blocks.

I believe that unless the client retains indefinite history (reasonable in some apps, unreasonable in others) it is not possible to have the same code process old events and new events.  Old events have the properties that they have strong guarantees of finality (unlikely to be reorged out) and the client is unlikely to have retained them (due to the volume of data required to retain all of history).  New events have the properties that they have weak or no finality (likely to be reorged out) but they have the benefit that the client can reasonably store them (can easily fit last 100 blocks with logs in memory).  Given these different properties, I don’t *think* it is possible to write one set of non-branching logic that can work with both.  At best, you can hide the branching inside of a library (this would be a reasonable extension to ethereumjs-blockstream).  However, I believe the branching must happen client side (within its failure domain).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Why is being able to fetch logs from a specific block important here? Why not just use a range query?

Reorgs happen on the block level, and due to the reasons argued above, we need to track reorgs client-side.  It is valuable for the client to always be in an internally consistent state.  Since we are monitoring/managing reorgs (at the block level), we want to make sure that the set of logs that the client is aware of and their order is consistent with the set of blocks the client is aware of and their order.  At any given point in time, the client may be out of sync with the node it is talking to. If we fetch logs by number, we may end up getting back logs that do not match the set of blocks we have, and this can put the client into an inconsistent state.  This is made worse due to the fact that the API doesn’t return details about what blocks it is returning logs for, and in the case where you get back an empty array you don’t know what block that empty array is associated with so you don’t have enough information to ignore the logs if they don’t align with your internal block state.

If instead we just fetch logs by block hash for a block hash that we are aware of every time we see a new block, we can guarantee that we maintain an internally consistent state between blocks and logs.  If the client thinks block hash 0xabcd is the latest block, then it will fetch logs for 0xabcd, it will never get back logs for 0xef01 (which can happen if you fetch by block number).  If you do “range by block hash” and do not use `latest` or number for the `to` block then I think you can reconcile this, though IMO it increases the engineering complexity on the client more than it is worth, since as argued above we have to have two different sets of logic for historic fetching (which can be done by number and over large ranges) and near-head fetching (where you probably are only fetching 1 or 2 blocks at a time anyway, so batching isn’t gaining you much).

---

**Arachnid** (2018-09-25):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Since we are monitoring/managing reorgs (at the block level), we want to make sure that the set of logs that the client is aware of and their order is consistent with the set of blocks the client is aware of and their order. At any given point in time, the client may be out of sync with the node it is talking to. If we fetch logs by number, we may end up getting back logs that do not match the set of blocks we have, and this can put the client into an inconsistent state.

Can you give an example of a sequence of operations that would result in an inconsistent state that isn’t fixed by subsequent passes?

---

**MicahZoltu** (2018-09-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Can you give an example of a sequence of operations that would result in an inconsistent state that isn’t fixed by subsequent passes?

1. Client has block 8 and logs up through block 8, hash 0x08ab.
2. Client polls for latest block and gets block 10, hash 0x10ab in response.
3. Client fetches parent block 9, hash 0x09ab in response.
4. At the same time, the client polls for logs “since block 8/0x08ab” and in response gets logs for block 9 block 0x09ab and an empty array for block 10/0x10cd.  Note: Since it received an empty array for block 10, it has no way to notice that it received logs for block 0x10cd instead of logs for block 0x10ab that it has.
5. Wait for polling interval and poll for latest, receive block 12, hash 0x12ab in response.
6. Fetch parent block 11, hash 0x11ab, get it in response.  Note: block 0x11ab has parent block 0x10ab, which is what we have in our local chain, so we think everything is great.

At this point, we will continue on with incorrect logs for block `10`.  This can happen when speaking to a single node if a block is reorged out, and then reorged back in.  This is uncommon, but it does happen.  If the fetch of logs occurs while the block is reorged out, but the fetch of the block occurs when it is reorged in, then the client will never witness the reorg and thus not realize they need to re-fetch logs for block `10`.

This problem gets significantly worse when you are communicating with multiple backend nodes (e.g., load balanced nodes life Infura) because they very often do not agree on canonical chain near head, and when you fetch you get routed to a random node for each request.  This means you could have both of the block requests in the above example go to node A, while the log request goes to node B.  Node A and node B may disagree temporarily on what the canonical chain is and while they will eventually sync up, the client will never receive information that informs them that there were two live chains, so they do not know to fetch.

This was a pretty major problem in `ethereumjs-blockstream`, particularly when talking to Infura which is random load balanced, so a client would frequently speak to a node with a different canonical chain from the previous request.  Since the addition (very recent) of being able to fetch logs by block hash, this problem has been fully solved as we can simply fetch logs as a reaction to receiving a block, and we are guaranteed to either get the logs for that block, or get an error (in which case we rollback the block).

---

**tjayrush** (2018-10-16):

I very well may not understand exactly what you’re saying, but I look at blocks as being utterly self-contained.

By this I mean that blocks are made up of transactions which hold receipts which hold logs. One big data structure. If a block re-orgs, the entire thing gets thrown out, logs and all, and simply re-queried. Why can’t you just re-query the logs when a block gets reorganized?

Again, I apologize for my ignorance.

---

**charles-cooper** (2019-01-14):

[@tjayrush](/u/tjayrush) I believe what [@MicahZoltu](/u/micahzoltu) is saying is that you might not know that a block has been re-orged, especially if it is re-orged out and then re-orged back in. If I’m not mistaken, however, there is a simple solution which is to just not allow calling `getLogs` with `toBlock = 'latest'` if `fromBlock` is a block hash instead of a number. That being said, there is not much point in range querying by hash when you can just use the `blockHash` parameter of `getLogs` (see EIP234, which I became aware of today as a result of reading this thread). The onus should be on the client to keep track of recent block headers and adjust its internal state wrt reorgs. So a correct client implementation which does not depend on node state should look something like

```auto
init:
  find latest block number
  grab as many blocks back as you would like, say latest - 100
loop:
  poll getBlockByNumber('latest') # note: parity exposes a newHeads subscription
  while received_block.number > latest in-memory block number,
    call getLogs(blockHash=received_block.hash)
    call getBlockByHash(received_block.prev_hash)

```

---

**tjayrush** (2019-02-08):

[@charles-cooper](/u/charles-cooper) I think of it this way. If the block re-orgs, presumably it re-orged because something in the data changed. If something in the data changed, then the block’s hash will have changed.

So, if I get a block at a certain height that is already in my database, and the hash I have in my database is different than the hash for this new block, then I consider the new block canonical (until I get another new block at the same height), and I invalidate all the data associated with that block (including traces, receipts, logs, etc.). I then re-query everything for the new block and put that in my database.

Any process that has already been done with that previous (now-defunct) block (including any processing done on previous now-defunct logs, receipts, etc.) has to be re-done.

Doesn’t that work? Maybe I’m missing something.

---

**charles-cooper** (2019-02-20):

[@tjayrush](/u/tjayrush) that more or less works. You might have to invalidate a block even if you don’t see a different block with the same number in the canonical chain. For instance if the latest is 1002, and then the chain reorgs to a block with number 1001 (which could happen because nodes select the chain with highest difficulty, which is correlated to but not necessarily equal to the longest length). You would have to invalidate 1002 in addition to invalidating 1001.

---

**tjayrush** (2019-02-21):

1002, when it finally comes, would have a different hash and therefore would get re-written, but thanks. I didn’t think about that case.

