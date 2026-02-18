---
source: ethresearch
topic_id: 2413
title: The case for block level sharding
author: dlubarov
date: "2018-07-02"
category: Sharding
tags: []
url: https://ethresear.ch/t/the-case-for-block-level-sharding/2413
views: 1095
likes: 0
posts_count: 3
---

# The case for block level sharding

By block level sharding I mean having a single chain with large blocks, which are broken up into shards. Validators would run a cluster of servers, and each server would be assigned a range of shards. Validators could scale without any practical limits using traditional distributed systems technologies, like sharded databases. If clusters grow very large and fault tolerance is desired, validators could use consensus-based storage systems with strong consistency, such as Spanner or CockroachDb; I elaborated a bit [here](https://ethresear.ch/t/scaling-via-full-node-clusters/1358).

This would lead to some centralization, but I’d like to explore those concerns a bit, since I don’t find any of them very compelling. I wonder if there are stronger arguments that I’m missing.

# Benefits

The main benefit is keeping the protocol simple. There’s no need for locking/yanking, and no signature aggregation. It’s trivial to find servers with data for a certain shard, since servers never switch shards. There’s only one type of chain, rather than one main chain and many collation chains.

The lack of locking/yanking also keeps the EVM model simple, saving contract authors some pain. It also reduces the latency of regular payments, since there’s no need to wait for lock/yank operations to finalize. For certain contracts requiring lots of cross-shard communication, block level sharding could give vastly better performance.

# Centralization concerns

Obviously, block sharding would raise the barrier to running a validator node. One of the rationalizations for small block sizes, e.g. in the Lightning Network paper, is that it lets small players fully validate the blockchain. However, this becomes a non-issue with Casper FFG or any BFT consensus algorithm. Only validators need to download transaction data; light clients can download just the votes along with Merkle proofs that specific transactions are included. In either model, we assume that an invalid block will never get 2/3 votes.

There would be some increase in centralization, though a degree of centralization seems inevitable. In the long term, regardless of protocol design, the vast majority of coins will likely be held by specialized custodians, exchanges, banks and other large institutions. But for the sake of argument, let’s suppose that block-level sharding would significantly increase centralization.

Centralization could make 34% attacks somewhat easier to coordinate. On the other hand, with chain-level sharding we would have `SHARD_COUNT` random samples of the validator pool at each block height, rather than just one. That means more opportunities for an attacker with <34% stake to get lucky and get 34% representation for a single block height and shard ID. We can use the binomial CDF to calculate the probabilities.

Another risk of centralization is that it makes soft forks, such as censoring a certain account, easier to coordinate. With BFT consensus systems, however, we can design the protocol such that once honest validators see a valid block, they will always vote for it (or its descendants) unless they see a conflicting supermajority. This way, soft forks would require a sustained 67% supermajority. This would be even less of a concern with systems like Zcash, where censorship is impractical since account data is private. There could still be soft forks based on public fields like transaction fees, but that’s less of a concern.

## Replies

**nootropicat** (2018-07-02):

I agree a bit with the first part. Full PoS + parallelism on one chain could increase throughput ~100x and still run comfortably on medium to high-end home PCs, while being much simpler to develop and develop on.

The main problem with not stopping there and going full data center mode is that it never stops. As hardware and bandwidth requirements get higher and higher, more validators would have to either stop staking or use someone else’s pool. Eventually the network inevitably ends up under control of very few entities, each running a node comprised of thousands of powerful servers. If the cooperate they could do *anything*, as there would be no way for anybody outside to verify anything. Basically EOS, only in a very roundabout way.

Sharding appears to be the only currently practical approach that allows a scalable and decentralized network to exist in the long run.

---

**dlubarov** (2018-07-02):

It’s a good point if we’re talking about smart contract platforms which want to support very high-volume applications, like chat apps. I was thinking more about “payment only” currencies. Since global electronic payment volume peaks around 10k TPS, I figure processing that would never be cost-prohibitive even for smaller businesses and institutions.

Let’s say we’re using ec2 hosting. If the protocol is designed with efficiency in mind, e.g. with BFT consensus after each block to eliminate forking, a t2.medium VM could probably handle a few hundred transactions per second. With $1000/month in instance fees, we could rent 30 of them to handle global payment volume. Bandwidth might be another $700/month or so, assuming 500 bytes per transaction and $0.05/gb.

Of course the costs can come down a lot if you rent racks in a datacenter, buy servers, join a major peering exchange, and use a backbone provider like Level 3 to talk to non-peers. But even with cloud hosting prices, the costs seem pretty insignificant to me.

I realize there’s also an economic argument for letting individuals run validators on their home PCs, in order to give everyone access to the same interest rate. But how many individuals would really want to keep their PC running 24/7 to run a person node, rather than delegating the task to a custodian with better security and efficiency? Maybe a few thousand individuals, but that’s not significant in macroeconomic terms.

