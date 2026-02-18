---
source: magicians
topic_id: 2710
title: GraphQL interface to Ethereum node data
author: Arachnid
date: "2019-02-21"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/graphql-interface-to-ethereum-node-data/2710
views: 10842
likes: 21
posts_count: 62
---

# GraphQL interface to Ethereum node data

This topic is for discussion of [EIP-1767](https://eips.ethereum.org/EIPS/eip-1767), GraphQL interface to Ethereum node data.

The goal of this EIP is to provide a new API for accessing Ethereum node data that’s more efficient and flexible than the current JSON-RPC interface, with the eventual goal of replacing it. An implementation of the standard so far will be in the next release of geth.

I’m keen to collaborate with developers on other clients to get this adopted as widely as possible, so your feedback is greatly appreciated - as is reaching  out to your favourite client developers!

## Replies

**Ethernian** (2019-02-22):

Great proposal!

One question: could you compare the [EIP-1767](https://eips.ethereum.org/EIPS/eip-1767) with the [TheGraph](https://thegraph.com)’s approach?

---

**Arachnid** (2019-02-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> One question: could you compare the EIP-1767 with the TheGraph’s approach?

The Graph provides a way to create custom ETL schemas over Ethereum events, making it possible to efficiently index and query contract-specific data.

In contrast, this EIP specifies a GraphQL schema for presenting the node data that’s already stored and indexed by nodes and provided via the JSON-RPC interface, with the ultimate goal of replacing JSON-RPC. This is particularly useful for tools that consume blockchain data en-masse, like The Graph.

---

**Ethernian** (2019-02-22):

RFE: I would like to have an ability to get a public key for address (without intermediary explicit tx lookup and ecrecover call).

---

**Arachnid** (2019-02-22):

There’s not any way to do this efficiently, unfortunately.

---

**Ethernian** (2019-02-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> There’s not any way to do this efficiently, unfortunately.

hmm… is it really no way for a node to maintain internally an efficient index from ethereum address to [blockNr, txNr] of some of Tx signed by this address (and recover a public key from this Tx upon request)?

---

**Arachnid** (2019-02-22):

Sure, that’s possible, but:

1. It  would require new index datastructures on disk.
2. It wouldn’t work for transactions sent before the node was fast-synced without changes to the fast-sync protocol.
3. It wouldn’t work for light nodes without changes to the LES protocol.

And for all of the reasons above, it’s totally out of scope for this EIP. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**ryanschneider** (2019-02-22):

I think `call` and `account` should also be options on a `block` just like how `logs` is done.  That way I could do:

```auto
block(hash: "0xblockHash") {
    account( "0xaddress") { balance }
}
```

To do the equivalent of `eth_getBalance("0xaddress", "0xblockHash")`, which actually isn’t actually supported by JSONRPC (the 2nd param is always a block number, not a hash).

This would access the snapshot of state from that block, so would be useful for people indexing data from archive nodes, and by allowing lookup by hash it solves the issue of possible reorgs happening under your feet between two queries.

The top-level `call` and `account` should stay, they would just continue to reference the canonical head’s state root.

---

**Arachnid** (2019-02-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanschneider/48/945_2.png) ryanschneider:

> I think call and account should also be options on a block just like how logs is done.

Good call. Perhaps it would make more sense to remove them from the top level query in that case? One way of doing things is generally clearer than multiple, and I don’t think `block { account("0xaddress") { balance } } ` for a query against the latest block is unclear.

---

**pipermerriam** (2019-02-23):

I don’t know enough about GraphQL to know if this will be a problem (nor have I had the time to do my research) but…

It would be ideal if we could loosen the spec from requiring the JSON-RPC endpoint be exposed over HTTP.  The Trinity client only exposes JSON-RPC over an IPC socket.  Our plans are to provide websockets and HTTP using https://github.com/ethereum/dopple .  That tool will proxy an IPC socket based JSON-RPC server over either HTTP or websockets, allowing the Trinity codebase to not worry about HTTP servers of any kind.  Ideally we’d expose the graphQL API through the same mechanism with the option of proxying it over HTTP if desired.

---

**Arachnid** (2019-02-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pipermerriam/48/65_2.png) pipermerriam:

> It would be ideal if we could loosen the spec from requiring the JSON-RPC endpoint be exposed over HTTP. The Trinity client only exposes JSON-RPC over an IPC socket. Our plans are to provide websockets and HTTP using https://github.com/ethereum/dopple  . That tool will proxy an IPC socket based JSON-RPC server over either HTTP or websockets, allowing the Trinity codebase to not worry about HTTP servers of any kind. Ideally we’d expose the graphQL API through the same mechanism with the option of proxying it over HTTP if desired.

I’m certainly happy to loosen the spec to allow for that - but we’d need to specify an encapsulation and encoding schema. As far as I can tell, dopple just takes the POST body and sends it raw over the socket, then returns the response. This is fine, if you don’t need any metadata or headers, but I’m fairly sure GraphQL does; for instance, it supports query parameter substitution, which requires sending a query and a separate map/dict of parameters.

What’s the motivation behind using such a bare-bones transport? I can understand wanting to avoid some of the complexities of HTTP, but couldn’t you expose a very basic HTTP service over IPC instead, which would preserve useful features like headers and content encoding, and use a reverse proxy to serve it to clients?

---

**pipermerriam** (2019-02-24):

Hrm, I need to go read up a bit on GraphQL.  I wasn’t aware that it leveraged HTTP apis like query params.

---

**Arachnid** (2019-02-24):

Looks like I was mistaken; an HTTP binding is provided which encapsulates both the document and any query parameters in one blob: https://graphql.org/learn/serving-over-http/

---

**kshinn** (2019-02-25):

I’ve been through the respective differences between the EthQL and this standard a few times and it looks like a lot of work has been done to align them. On the EthQL side, there are some things that can be done to align some of the more minor differences. There are also some comments I wanted to rehash from previous conversations.

There were a few comments made in previous conversations that seemed like the biggest differences that I wanted to align on.

> Big integers should probably have their own scalar type, not just String
> Likewise, hex-encoded byte strings other than addresses and hashes should have their own types.

Agreed. The additional specificity is needed for standards.

There are a number of “conveniences” that EthQL layers on top of the raw output to give to dApp developers. Among them, you mentioned additional transaction filters, expressing values in selectable base units, and decoding things like Solidity storage layout. For something baked into a node, the additional complexity / overhead for that is not needed and as we work with EthQL it does feel like there is a Standard API and an Extended API that provides the type of application side processing one would do.

Suggestions:

For arguments that reference a block, the EIP limits to blockNumbers. What about adding back the string based references of “latest”, “earliest”, and “pending”?

Also, are there small conveniences we could bake into the standard? For transaction status, the `1`, `0`, `null` values feels like an enum. EthQL has them defined as `SUCCESSFUL`, `FAILED`, `PENDING`.

There are some methods that went unimplemented in this EIP `eth_newFilter` and the like. Are you thinking that Subscriptions would be included in a future EIP?

---

**Arachnid** (2019-02-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kshinn/48/2143_2.png) kshinn:

> For arguments that reference a block, the EIP limits to blockNumbers. What about adding back the string based references of “latest”, “earliest”, and “pending”?

`"earliest"` is redundant, since you can specify it as `0` instead, and the EIP specifies that omitting any block number or hash operates on the latest block. For `"pending"`, if we make the change I suggested earlier of putting all operations such as `call` and `balance` in a `Block` object, perhaps the top level query can have a `pendingBlock` field?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kshinn/48/2143_2.png) kshinn:

> Also, are there small conveniences we could bake into the standard? For transaction status, the 1 , 0 , null values feels like an enum. EthQL has them defined as SUCCESSFUL , FAILED , PENDING .

Good point - let’s make this an enum.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kshinn/48/2143_2.png) kshinn:

> There are some methods that went unimplemented in this EIP eth_newFilter and the like. Are you thinking that Subscriptions would be included in a future EIP?

Designing a filtering API that makes good use of GraphQL’s subscription functionality and doesn’t just replicate the JSON-RPC filter mechanism seemed like a project all of its own; I didn’t want to cram in something that just kind of worked into this spec. I think it makes the most sense as a separate EIP.

---

**ryanschneider** (2019-02-25):

> Good call. Perhaps it would make more sense to remove them from the top level query in that case? One way of doing things is generally clearer than multiple, and I don’t think  block { account("0xaddress") { balance } }  for a query against the latest block is unclear.

I agree, the only reason I proposed keeping `account` and `call` at the high-level was compatibility with earlier versions of the spec, but IMO the more we can do to educate web3 developers on the interaction between blocks and state the better, and tying these actions to a specific block does that.

As an added plus, this forces multiple calls to be explicit on what block they operate on, previously `account("0xa..."){} account("0xb...."){}` could have a small chance of being resolved on separate blocks if a new block came in mid-resolver, and so the spec would need to define that behavior.  Now, that behavior is up to the query writer (if they write `block(){ account(a){} account(b){} }` vs. `block{ account(a){} } block{ account(b){} }`.

> Designing a filtering API that makes good use of GraphQL’s subscription functionality and doesn’t just replicate the JSON-RPC filter mechanism seemed like a project all of its own

I agree 100%.  That said, we should perhaps have some informal discussions on where we see the subscription support in EthQL going before this EIP is finalized?  Just so to minimize the chance of baking something in at the query level that will conflict with later subscription ideas?

Over the winter holiday I spent a little time toying with an addition to the EthQL schema to add support for checking the confirmation of a sent transaction via a subscription, I got a very messy proof-of-concept version working locally using `parity_subscribe`.  The code isn’t really in a state to be shared yet, but here’s a gist where I outlined how I imagine it working:



      [gist.github.com](https://gist.github.com/ryanschneider/e7819ff02256138b780969ddf114a0e7)





####



##### flow.graphql



```
# offline, sign a transaction to generate it's raw bytes 0xRAWTX
# connect to our new transaction websocket endpoint
# send the graphql mutation:
mutatation {
    sendRawTransaction(data: "0xRAWTX") {
        hash
    }
}
# get back the hash or an error
{
```

   This file has been truncated. [show original](https://gist.github.com/ryanschneider/e7819ff02256138b780969ddf114a0e7)










Anyways, just mentioning this to show my interest in subscriptions in later iterations of EthQL, for now I agree 100% we should be focused on the query aspects.

---

**ryanschneider** (2019-02-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> For "pending" , if we make the change I suggested earlier of putting all operations such as call and balance in a Block object, perhaps the top level query can have a pendingBlock field?

I like this idea.  It also reinforces that the `pending` block is special, which it is (there’s no guarantee that your nodes pending block will match in any way what actually gets mined by the miners).

Also if we get to the point where the `txpool` RPCs have any exposure over graphQL I could see `pendingBlock` living there (e.g. `txpool { pendingBlock }` ) to further hammer home the point that it’s a local best-effort at guessing what might be mined next, but I think that could wait.  I’d also personally be fine with not support pending blocks at all in the baseline graphQL spec since they are such a special beast.

---

**kshinn** (2019-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> For "pending" , if we make the change I suggested earlier of putting all operations such as call and balance in a Block object, perhaps the top level query can have a pendingBlock field?

I was originally suggestion that we have some reference to “pending” because of the JSON-RPC spec and how it treats the “earliest”, “latest”, and “pending” ideas. Based on some of the discussion in [@ryanschneider](/u/ryanschneider)’s responses I wonder if it could be confusing to the end user? That said, I don’t have any problem with the proposed field on the `Block` object.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ryanschneider/48/945_2.png) ryanschneider:

> That said, we should perhaps have some informal discussions on where we see the subscription support in EthQL going before this EIP is finalized? Just so to minimize the chance of baking something in at the query level that will conflict with later subscription ideas?

One of the things I like about the EIP is that (as far as I understand) it keeps things simple and close to the storage implementation in the node.  Most of the use cases for subscription I’ve had in my mind (and that I’ve heard in conversations) are around event subscriptions which look like a natural extension to the filtering functionality here. Are there particular cases you are worried about in subscriptions that could conflict? I think that the subscription conversation could go pretty deep and pull this discussion off topic.

---

**ryanschneider** (2019-02-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kshinn/48/2143_2.png) kshinn:

> Are there particular cases you are worried about in subscriptions that could conflict? I think that the subscription conversation could go pretty deep and pull this discussion off topic.

Very valid point.  I think the obvious ones are subscriptions on new blocks and logs (to match the functionality of the `eth_subscribe` RPC).  While `eth_subscribe` also supports subscribing to pending transactions, IMO that’s a bit too much of a firehose on public networks, I feel like the graphQL equivalent should have some sort of required filter (address(es), etc.) to limit the scope of data being sent.

The less obvious ones are:

- transaction confirmation: currently there’s no way to see that your transaction was mined and has stayed mined for N blocks short of polling the JSONRPC layer.
- parity_subscribe (https://wiki.parity.io/JSONRPC-parity_pubsub-module.html#parity_subscribe) I haven’t looked at all into how this is implemented but I assume they are basically re-running the RPC every time a new block is imported into the chain (and additionally possibly on every new change to the txpool).  I think this can be emulated pretty well if there’s a block subscription and call and address are available from the block like we’ve discussed.

Anyways, I agree this is all out of scope for the EIP, I just wanted to think through it some to make sure we’re not baking in anything that will make subscriptions harder down the road, but so far I haven’t seen anything that would do that.

---

**kshinn** (2019-03-01):

What do we think about adding an ID primitive field?

https://facebook.github.io/graphql/draft/#sec-ID

The hash reference (or some encoded version of it) could be used for this purpose. It presents a bit more complexity and arguably redundant representation of data, but from what I understand the graphql clients use this primitive type to decide how to cache and resolve data. I can see a lot value in this for highly connected graph structures where parts of the query tree can be cached/reused without having to refetch it upstream. However, outside of account relationships I don’t know if the data is highly connected enough to really take advantage of the concept.

I think there are 2 possible ways of going about this:

1. Change the type of *.hash and account.address from Bytes32 to ID. This drawback is it obscures the underlying datatype and starts moving it away from the Ethereum spec.
2. Keep the fields the way they are and add an additional id field with the Type ID. This gives some flexibility to define IDs that don’t have hashes (for example logs IDs could be defined as keccak256(block.hash + log.index). Drawback is that it adds a new field to the data type that is not really part of the underlying node storage.

---

**Arachnid** (2019-03-01):

Good thought. I hadn’t recognised the significance of using `ID` to other generic graphql tools.

I think your option 2 is better - make IDs opaque to callers, with no guarantees except they’re unique.


*(41 more replies not shown)*
