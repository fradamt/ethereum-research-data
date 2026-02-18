---
source: magicians
topic_id: 4911
title: How will shards interact on ETH 2.0?
author: Hikari
date: "2020-11-04"
category: Magicians > Primordial Soup
tags: [consensus-layer, sharding]
url: https://ethereum-magicians.org/t/how-will-shards-interact-on-eth-2-0/4911
views: 1646
likes: 0
posts_count: 3
---

# How will shards interact on ETH 2.0?

Hello. I had read about ETH 2.0, and am still unable to understand how shards will work.

I see that Beacon blocks will have a reference to latest known block of each shard and each shard blocks will have the same for Beacon. I suppose that’s used so that a Beacon block indicates the state it recognizes and uses on each shard.

But how exactly will shards interact?

In example. Say that somebody wanna create TokenA. Will he be able to choose on which shard the creation tx will be commited? And once it’s done, will TokenA balance on all address be stored to that shard, or will we be able to move some balance to other shards?

If we wanna swap TokenA which is on shard1 for TokenB that’s on shard3, how will that happen? Using atomic swap?

And how about features like liquidity pools. If a smartcontract deployed on shard5 wanna use a pool on shard11, how will it happen?

Sorry for so many questions and tnx for any answer ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

## Replies

**alwintech** (2020-11-12):

[Ethereum 2. 0 Shard Chain](https://alwin.io/blog/ethereum-2.0-notes-for-beginners)

Shard chain in ethereum 2.0 store and process transactions. These shard chains are an important part of increasing the number of transactions ethereum can handle per sec. As per official beacon chain statement, Ethereum 2.0 will support 1024 Ethereum shard chains, each of which will be secured by a committee size of 128 validators. It is also important to note that transactions are only executed and validated within a shard, and that state is only stored at the shard level. These beacon chains to make sure every shard has the most up-to-date data with the help of validators who communicate the state of shard chains to the beacon chain. Like, this shard chain helps the network enhance performance in transactions scalability and securities.

To know more about **[Ethereum 2.0](https://alwin.io/blog/ethereum-2.0-notes-for-beginners)** details, visit our blog now @ https://alwin.io/blog/ethereum-2.0-notes-for-beginners

Looking for start your own [DeFi](https://alwin.io/) or staking platform in Ethereum visit us today!

---

**Hikari** (2020-11-12):

I think it was reduced from 1.024 to 128 shards.

Still, it doesn’t explain how shards will interact as I asked.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/35a633/48.png) Hikari:

> In example. Say that somebody wanna create TokenA. Will he be able to choose on which shard the creation tx will be commited? And once it’s done, will TokenA balance on all address be stored to that shard, or will we be able to move some balance to other shards?
>
>
> If we wanna swap TokenA which is on shard1 for TokenB that’s on shard3, how will that happen? Using atomic swap?

