---
source: magicians
topic_id: 6602
title: State Management Review
author: norswap
date: "2021-07-05"
category: Magicians > Primordial Soup
tags: [state-expiry]
url: https://ethereum-magicians.org/t/state-management-review/6602
views: 1264
likes: 5
posts_count: 4
---

# State Management Review

Hey everyone,

I’m taking part in the core developer apprenticeship, and as a part of that I did a deep dive on the various concerns and proposals connected to state management in Ethereum.

[Link to the review](https://www.notion.so/norswap/State-Expiry-Statelessness-in-Review-8d531abcc2984babb9bf76a44459e611)

I thought I’d post it here for exposure. I’m very open to comments / suggestions / contributions!

## Replies

**matt** (2021-07-05):

Nice write up [@norswap](/u/norswap)! In the future if you wouldn’t mind, it’s generally preferable to write the text in the post itself. It makes quoting easier ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> To give you an idea, a full node (which maintains the state, but does only keeps the N (usually N=128) latest blocks) must currently store > 400 GB (or more than double that if using Geth). This is still better than archive nodes (who keep the whole block history), which must store a whopping 7.5 TB.

Generally the state is one of the smaller portions of data fast synced nodes store. Depending on the exact storage model, should be something like 30-60 GB. Headers, block bodies,

receipts, and caches take up a lot of the rest of the data. Not sure how much keeping the last N blocks worth of state takes up, but generally these aren’t simple copies, they’re state diffs.

> or more than double that if using Geth

Geth nodes I’ve synced recently are closer to 430 GBs.

> A Merkle tree is a radix tree (a compressed trie)

I think you mean a *Modified Patricia* Merkle Tree ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> a contract might not know in advance which state it is going to access — which makes it impossible to provide proof for

This is called [Dynamic State Access](https://ethresear.ch/t/state-provider-models-in-ethereum-2-0/6750) (DSA)!

> If a transaction wants to access older state, it must use a special instruction to regenerate the state, supplying the state’s value, along with a witness (proof) for that value.

I don’t think an instruction (as in an EVM instruction) would be the main mechanism that hydrates a state element. I expect a new transaction type will support witnesses and at the beginning of the transaction the state will be inserted into the current active state.

> First, it requires some nodes to keep the checkpointed state. This can be a significant amount of data (twice the size of the normal state if implemented naively). Because it’s so much data, nodes will keep at most the state of a single checkpoint — meaning you’ll have to download the hundreds of GB of the checkpoint state before your source nodes move on to the next checkpoint.

I don’t think this is true. Fast sync isn’t checkpointed like warp sync or something, the db you’re syncing is always changing under you. The network isn’t storing old checkpoints AFAIK. It’s just using the pivots that are inherent to geth’s handling of block reorgs.

–

Overall, awesome write up. Thank you for sharing!

---

**norswap** (2021-07-06):

Thanks, this is exactly the kind of review I was looking for!

> In the future if you wouldn’t mind, it’s generally preferable to write the text in the post itself. It makes quoting easier

Noted!

Edit: wouldn’t have worked, as I can only put two links in a post as a “new user” ![:cry:](https://ethereum-magicians.org/images/emoji/twitter/cry.png?v=12)

> Generally the state is one of the smaller portions of data fast synced nodes store. Depending on the exact storage model, should be something like 30-60 GB. Headers, block bodies,
> receipts, and caches take up a lot of the rest of the data. Not sure how much keeping the last N blocks worth of state takes up, but generally these aren’t simple copies, they’re state diffs.

Amended that section to be more precise. Can the size of the state be tracked somewhere, short of running a node with custom code and measuring it there?

> Geth nodes I’ve synced recently are closer to 430 GBs.

Do you know what explains the discrepancy with https://etherscan.io/chartsync/chaindefault ?

> I think you mean a Modified Patricia Merkle Tree

Got to push back a bit here - a patricia tree is a radix tree! In fact, the wikipedia page for radix tree says:

> Donald R. Morrison first described what Donald Knuth, pages 498-500 in Volume III of The Art of Computer Programming, calls “Patricia’s trees” in 1968.[6] Gernot Gwehenberger independently invented and described the data structure at about the same time.[7] PATRICIA trees are radix trees with radix equals 2, which means that each bit of the key is compared individually and each node is a two-way (i.e., left versus right) branch.

“modified patricia tree” is a term that is almost 100% associated with Ethereum. For someone that’s not into blockchains but has a CS background, you can immediately tell what a radix tree, whereas a patricia tree is a much more obscure term.

I’ll add the term though, it’s good to have it mentionned.

> This is called Dynamic State Access  (DSA)!
> I don’t think an instruction (as in an EVM instruction)  …

True, included!

> I don’t think this is true. Fast sync isn’t checkpointed like warp sync or something, the db you’re syncing is always changing under you. The network isn’t storing old checkpoints AFAIK. It’s just using the pivots that are inherent to geth’s handling of block reorgs.

You’re right, I must have gotten warp & fast sync conflated. I’ll read up & update that section. Tell me if you know a good writeup on this.

> Overall, awesome write up. Thank you for sharing!

Thanks ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**matt** (2021-07-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> Can the size of the state be tracked somewhere, short of running a node with custom code and measuring it there?

Geth added some db introspection with v1.10.0, maybe that helps? I think Erigon also has similar tools.

> Do you know what explains the discrepancy with https://etherscan.io/chartsync/chaindefault ?

Usually if you compare a recently fast synced node to a full node that was fast synced awhile ago, you’ll see a discrepancy. This is because [pruning is really hard](https://blog.ethereum.org/2021/03/03/geth-v1-10-0/). There may also be things that are generated for newly full synced blocks (after fast sync completes) that you don’t have for pre-fast-synced blocks.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/norswap/48/4243_2.png) norswap:

> Got to push back a bit here - a patricia tree is a radix tree! In fact, the wikipedia page for radix tree says:

Yes absolutely, but a merkle tree itself is not a radix trie. That is a very specific flavor.

