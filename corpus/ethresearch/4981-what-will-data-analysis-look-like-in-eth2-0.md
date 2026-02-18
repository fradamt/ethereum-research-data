---
source: ethresearch
topic_id: 4981
title: What will data analysis look like in ETH2.0?
author: d-ontmindme
date: "2019-02-11"
category: Data Science
tags: []
url: https://ethresear.ch/t/what-will-data-analysis-look-like-in-eth2-0/4981
views: 2608
likes: 7
posts_count: 7
---

# What will data analysis look like in ETH2.0?

There have been a lot of cool new projects within the industry focused on parsing ‘meaningful data’ from blockchains (the most useful currently is the blockchain-etl project imho: https://github.com/blockchain-etl/ethereum-etl). However, it’s clear that the architecture of ETH2.0 is noticeably different from that of ETH1.0; how will this likely affect data analysis projects like blockchain-etl?

Most data analysis of this ilk requires one to parse through the whole state of a given blockchain from genesis and then transform that data into a more convenient format. Given that there could be around 1,024 shards in ETH1.0 plus the beacon chain AND I remember reading that the legacy chain could – in theory – exist on a single shard; it seems inconceivable that a single data analyst could run all shards in order to have access to all the data ETH2.0 may bring, lest we allow all ETH2.0 data analysis to happen on Google BigQuery.

Questions:

Is this problem something that anyone has thought about?

Is this actually an important concern or am I mistaken? If so, why?

Thanks!

## Replies

**quickBlocks** (2019-02-11):

I think this is a hugely important concern. I’ve been thinking about this, writing about this, and writing code trying to anticipate this problem for two and a half years. My project is called QuickBlocks. We did exactly the opposite of ETL which (as you say) extracts the entire chain database and shoves it into an ever-growing database. That technique almost forces a centralized system. Plus, as I’ve been saying for a year, it won’t scale when there’s 1,000 times more chains.

The other really important issue that no-one ever addresses is that the ‘full data’ doesn’t even exist on- chain. The chain stores enough data to ‘recreate’ or ‘rerun’ the transactions. It does not store ‘every trace’ which is actually needed to do a full-detail audit of an address. Some blockchain explorers that I’m familiar with require more than seven or eight TB to hold all the extracted data. This is because they extract and store traces and state data. We chose to leave that data on the node.

Our project focuses on extracting the absolute minimum amount of data needed to make the chain  queryable. We have a couple of different ways of doing that ranging across the speed/size tradeoff.

We call the least impactful solution Enhanced Adaptive Blooms which takes about 10 GB of additional data (the last time I checked) and speeds up searches about 15 times over raw queries on the node without QuickBlocks.

We have another version that builds an index of transactions per address which takes up about 70 additional GB over the node data but speeds up the search many, many times over than that. In some cases, we’ve seen 100,000 times faster than scanning querying the chain without an index.

You can learn more at https://github.com/Great-Hill-Corporation/quickBlocks.

And before anyone accuses me of shilling, the entire code base is open source. Every time I mention QuickBlocks, I get accused of shilling.

---

**naterush** (2019-02-12):

I don’t think any version of “scan the chain and extract some information to make future scans faster” is going to work with sharded blockchains, whether this information is stored in a database or just an optimized index.

Pretty much by definition, sharded blockchains process can process more transactions than a single piece of consumer hardware can - so running through traces to extract information pretty much is not gonna work if you’re interested in contracts on (lots of) different shards.

As a very-relevant side note, I don’t think bloom filters + events should be apart of ETH2.0. For one, logs end up being way-to-cheap permanent storage. For two, bloom filters aren’t too expensive to exploit. Finally, the blooms aren’t really ever going to be properly sized for the optimal amount of false positives.

---

Here’s a basic proposal that mitigates some of these problems: each block header maintains a hash `touched_address_root`. The  `touched_address_root` is the root hash of a merkle tree that contains a sorted list of all addresses “touched” in that block. “Touched” here means that the address was a “to” or “from” in the external transaction or any internal call.

This allows a user to remain a light client of all shard chains, while still being able to efficiently check if the contracts they care about are touched during some block.

---

**quickBlocks** (2019-02-12):

Hi Nate,

I think we can both agree that the way things work today (i.e. blockchain explorers extracting the entire database) will never work. In the best of all possible worlds, a `touched_address_root` in the block headers would be great. I think it needs to be more than just the `to` and `from` addresses though. At the very least, it would have to include `contract creations` and `suicides`, but addresses appear in many places other than `to` and `from`. They appear throughout the chain being used as data in other smart contracts (i.e. black/white lists, airdrops, etc.)

I agree that blooms shouldn’t be in the block header (at the least). The blooms take up a lot of space. Would the `touched_address_root` allow you to accomplish the same filtering task?

In general, regular users won’t care about the deep details, but auditors will (especially forensic auditors who are trying to untangle some unforeseen legal entanglement).

Call you mom.

---

**naterush** (2019-02-12):

Contract creations seem reasonable. Suicides are probably the same as death-from-lack-of-rent, and so can be included as well.

But I don’t know about addresses that are used in data in other smart contracts. It’s pretty easy to write a smart contract that “hides” the addresses it uses - and so including extra data seems like a very temporary and totally unsatisfactory solution for the auditors anyways.

---

**vbuterin** (2019-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/quickblocks/48/406_2.png) quickBlocks:

> In the best of all possible worlds, a touched_address_root in the block headers would be great

In the design that I am thinking of, the state root would have a section of the state that gets overwritten every block, which contains receipts associated with each transaction. I would definitely support us including more data into receipts this time around, including logging all touched addresses. Possibly logging all transactions and internal calls as well because why not (unless the latter leads to too much extraneous hashing; maybe stick to non-static calls or something like that).

---

**quickBlocks** (2019-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> But I don’t know about addresses that are used in data in other smart contracts. It’s pretty easy to write a smart contract that “hides” the addresses it uses - and so including extra data seems like a very temporary and totally unsatisfactory solution for the auditors anyways.

There’s two different reasons for auditing. There’s auditing for nefarious behaviour and there’s auditing for perfectly legitimate behaviour. To penalize the legitimate audit needs of legit users because someone can do nefarious things or because a programmer wants to get fancy doesn’t seem very satisfactory either.

An example of why you would want to be more inclusive rather than less inclusive when building the list of addresses follows: During a token airdrop, you can become the real-world owner of a thing of value (a token) without knowing it. If, later, you learn of your ownership and sell that token, you need to know when you first acquired it (to calculate cost basis). Without a reference to the ‘minting’ (which many token contracts don’t note with an event – the ERC 20 spec doesn’t require it), you can’t calculate cost basis. If you only record `touched` addresses, you won’t meet all the needs of the users.

We’ve found (using QuickBlocks) about 35% of the addresses that `appear` in a block are not `touched` (if `touched` means involved directly in a transaction). These `appearing-but-not-touched`  addresses (addresses used as data in other smart contracts) show up in the `input` field of the transaction, in the `topics` and `data` of the event logs, and in the `output` field of Parity’s traceResult.

Before we decide we don’t need them, we should understand the implications of excluding them (especially if they’re easy to find, as they are).

