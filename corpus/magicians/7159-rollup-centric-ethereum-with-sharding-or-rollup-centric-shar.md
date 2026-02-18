---
source: magicians
topic_id: 7159
title: Rollup-centric ethereum with sharding or rollup-centric sharding?
author: samueldashadrach
date: "2021-09-29"
category: Uncategorized
tags: [ethereum-roadmap, layer-2]
url: https://ethereum-magicians.org/t/rollup-centric-ethereum-with-sharding-or-rollup-centric-sharding/7159
views: 5367
likes: 2
posts_count: 9
---

# Rollup-centric ethereum with sharding or rollup-centric sharding?

Vitalik’s [rollup-centric roadmap for ethereum](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698/1) provides a vision for ethereum that separates rollups and shards as playing two distinct but critical roles in scaling ethereum. While I am generally in favour of all the concepts involved, I would like to argue as to why I feel **there needs to be tighter coupling between rollups and shards**, than is likely to be seen in the current roadmap.

Before that I’d like to briefly summarise the insights underlying rollups and shards.

## Insights

**It’s all social consensus** - If you accept that social consensus is what governs blockchains, you can accept that nodes don’t need to be able to sync all the way to genesis. Social consensus is slow, but it can be established over the time-period of some weeks or months. Economic consensus (PoW, PoS) is very fast but backstopped by slow-moving social consensus.

Once you accept social consensus can established over say a 6-month scale, a node needs two things to sync. 6-month old state (on which you have social consensus) and 6-months of history.

**Social consensus is n-of-N not 1-of-N** - A single node can’t credibly fork the system, a few nodes are required to fork and establish their own network effect. Once you accept that, you don’t need every single node to store all data (state and history) - you can split it amongst n nodes. You now have n processors, n hard disks, n times the internet bandwidth to use in order to sync the network and be able to credibly fork it.

**Rollups split state among n nodes** - Not everyone cares about all state. Each user cares only about the state of only their own accounts and the contracts they wish to interact with. Rollups provide a natural way to split state. Each rollup has its own state and nodes of a rollup need to remain in sync with state of only that rollup, and not all the other rollups there exist.

**Sharding splits history among n nodes** - Not everyone needs to store all history. Accordingly, ethereum is split into n shards, with nodes of each shard storing history of that shard. Shards collectively become a giant “history dumping ground” for rollups. I’m just gonna refer to these nodes as shard nodes here onwards, to distinguish them from rollup nodes.

## What are the differences?

Clearly there are some differences between the way rollups split state and shards split history.

**1. Rollup nodes care more about the state they store, than shard nodes care about the history they store.**

Rollup nodes are storing and syncing state of specifically the rollups on which they personally have assets and find other state objects interesting. Shard nodes on the other hand are storing chunks of history from both rollups they care about and rollups they don’t care about. Even for the rollups they care about, they may not have the complete history, as it could be spread across multiple shards. While I completely agree that both types of nodes (rollup nodes and shard nodes) require some degree of altruism to exist - it is easier to be altruistic when dealing with objects you personally care about, such as your accounts. There is personal bias in this statement ofcourse, but I do feel it generalises. And that more people will run rollup nodes than shard nodes in the current system.

**2. Rollup designers have more flexibility to manage state, than shard designers have to manage history.**

Rollups are completely free in terms of how they manage state. They can implement state expiry with any time period, or state rent, or auction out state or offer it first-come-first-serve. They can rely on any model of [state providers](https://ethresear.ch/t/state-provider-models-in-ethereum-2-0/6750) to help rollup nodes sync and prove state as needed. They can implement account-based state model, UTXO model, or any other model that parallelises creation and validation of state or state transitions [in different ways](https://twitter.com/_prestwich/status/1151740902848622593). They can make different tradeoffs on assumptions of processing power or altruism. It is even possible for rollups to fall out of use, and have not a single node left who cares enough to sync the state of the rollup. This can happen without harming the overall system.

Shards however are being designed in a central fashion. All shards store the exact same amount of data being written at the same rate using the same opcodes and the same auction model by which it is allocated. All shards assume the same time period beyond which history is no longer stored (and social consensus is sufficient). This does not allow different subsystems to make different tradeoffs over altruistic assumptions. It does not allow different execution environments to make different design choices for their data availability model that fit in more closely with other execution-related choices they may have made. It provides them limited flexibility as to how their data is split amongst multiple shard nodes. Communication between nodes happens in a uniform hierarchial way, be it peer scoring, bandwidth management and privacy. There may be constructions where multiple shard nodes strategically agree on who stores what and communicates it when - that are more beneficial for the overall system than splitting everything equally.

**3. Rollup design is funded privately, sharding design is funded publicly.**

Rollups have investors who may wish to extract returns by various means. Sharding however is being driven by core devs and researchers, whose sources of funding are more altruistic. Their values and culture are different. Clearly there are advantages and disadvantages to both models that I will not get into here, but on the face of it I cannot see a fundamental reason why one kind of design *should* be privately funded and the other *should* be publicly funded.

## How to bring in tighter coupling between rollups and shards?

I have not spent too much time on this question - it is indeed an open one - I was hoping to get answers in the replies.

Regarding 1, it might make sense for rollups to register themselves to specific shards, assuming we retain the centrally-designed 64-shard model. That way there is clear mapping as to which shards are used by which rollups, and users running rollup nodes can naturally also run shard nodes for those specific shards.

Regarding 2, I think it is fairly open question as to how you “open up” the design of sharding, and let rollup and protocol designers define their own nodes and subnets and everything, with their own assumptions over altruism, compute power, bandwidth etc. There is a clear social component here as - the distinction between a user running an ethereum node and one running a bitcoin node is purely cultural. If you erode the socially unifying notion of an “ethereum node”, and instead allow 10 different types of ethereum data nodes to be created by 10 different protocol design teams, they will all compete for the same mindshare and same altruistic node operators who will have decide which nodes they want to run and which history they want to store. Ofcourse, this form of opening up has already happened when it comes to rollup nodes. Opening this up might also run the risk of some history being stored by no nodes, depending on how it is implemented. Which is again true with rollups, it is possible for there to exist rollups whose state is being synced by no one because nobody cares to.

Assuming some form of opening up of sharding design is attempted, one will have to carefully draw the line as to which design choices are opened up and which one are centrally retained by the current core devs.

Regarding 3, I don’t have much thoughts as to what *should* be done. What I know is rollup design *can* be publicly funded, and sharding design *can* be opened up to private funding and maintenance. And what should or should not be done is a meta-discussion that should be had.

## Replies

**l2intern** (2021-09-29):

Tight coupling between rollups and shard nodes may make rollups more vulnerable to data availability attacks.

Normally, an attacker would need to control a large fraction of *all* validators, but now, only needs to control a large fraction of validators on that rollup’s designated shards. This could be dangerous, as sharding uses a few-of-N trust model, where there must be enough data availability sampling requests by honest shard nodes so that at least half the data in a blob is available.

And if the beacon block proposer and shard nodes were to collude to create unavailable blobs, normally the rest of the network would not accept these blobs. However, if these unavailable blobs were to be confined to one rollup, even if there was an honest minority of shard nodes rejecting them, it is much harder to fork, as it would require coordination from all the other shard nodes for all other rollups.

---

**vbuterin** (2021-09-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samueldashadrach/48/3500_2.png) samueldashadrach:

> This does not allow different subsystems to make different tradeoffs over altruistic assumptions.

The reason why this was not allowed is because the entire sharding model depends on a property called “[tight coupling](https://vitalik.ca/general/2021/04/07/sharding.html)”. Quoting my previous post:

> Tight coupling: if even one shard gets a bad block, the entire chain reorgs to avoid it. There is a social contract (and in later sections of this document we describe some ways to enforce this technologically) that a chain with even one bad block in even one shard is not acceptable and should get thrown out as soon as it is discovered. This ensures that from the point of view of an application within the chain, there is perfect security: contract A can rely on contract B, because if contract B misbehaves due to an attack on the chain, that entire history reverts, including the transactions in contract A that misbehaved as a result of the malfunction in contract B.

Note that tight coupling is a security property that survives even in the face of 51% attacks. Unfortunately, it’s a pretty binary thing; I don’t know of any useful abstraction that would represent “80% tight coupling” or “50% tight coupling”; as soon as application devs even have to think about the possibility of coupling breaking, a lot of the advantages of sharding go out the window.

Another reasons why shards cannot easily be made heterogeneous is that many systemic risks, particularly centralization, are across the whole system. If there are 32 shards with a 12s block time and low returns to centralization, and 32 shards with a 0.5s block time and high returns to centralization, then the high returns to centralization in the second slice cause the entire system to have fairly high returns to centralization, increasing the risk of highly centralized stake pooling across the entire system and weakening the whole thing, including the slower shards.

**So in general, I think heterogeneous sharding has more risks than benefits**. What could be done, though, is more pathways for *heterogeneous ways of using shards* (BTW at this point, I should mention, “shard” is a very loose abstraction; slot N of shard 1 and slot N+1 of shard 1 are in practice almost as disconnected from each other as slot N of shard 1 and slot N+1 of shard 63, so it’s best to just think of it as homogeneous “data availability verification as a service”).

One example of heterogeneous ways of using shards is that if shards have staggered block times, so on average you’d expect ~5 new shard blocks coming in every second, then rollups that really care about speed could use many shards, at the cost of being harder for clients to follow along (because a client following along the rollup state would need to check more places for potential rollup blocks).

Another thing that could be done is the chain providing more types of public functionality than just data availability and beacon chain execution. One example of this would be some kind of built in recursive STARK functionality, so different STARK-based rollups could coexist and instead of all their proofs going on-chain and consuming gas, there would just be one commonly generated proof verifying the existence of all the other proofs.

> What I know is rollup design can be publicly funded

I would say many aspects of rollup design *are* at least partially publicly funded. EF and other general ecosystem players are putting resources into ZKPs (including ZK EVM), EVM rollups are all reusing geth (EF funded) and other Ethereum clients, all of them are reusing Metamask and other existing wallets (with various funding models). The parts that are privately funded are more the parts that actually are unique experiments that differ between the rollup projects.

> Which is again true with rollups, it is possible for there to exist rollups whose state is being synced by no one because nobody cares to.

I would say the key difference between rollups and shards is that if historical rollup state is lost and people notice, someone can re-process the shards and recover it, whereas if historical shard state is lost, we’re screwed. So the trust model on rollup state availability is even more lenient than the trust model for shard data availability.

---

**samueldashadrach** (2021-09-30):

Thank you so much for answering! I think I should have thought more about what decisions can be opened up and what cannot, before making the post. Sorry for that.

You’re right that opening up design choices for how validators are elected and behave etc is difficult to do without risking centralisation. But most of the tight coupling seems to be only for validators not for nodes. So maybe nodes can be opened up? I mean teams can create nodes that have their own networking layer, and handle their own specific blocks (say history of rollup A) that they deem useful to them.

> a chain with even one bad block in even one shard is not acceptable and should get thrown out as soon as it is discovered.

Just to confirm, does this property apply only at the time of block inclusion or even say 3 months after? For instance if nodes have lost the history of a shard 3 months later, can anything be done? And if not, would it be a good idea if rollup nodes store history instead of shard nodes?

> contract A can rely on contract B

> whereas if historical shard state is lost, we’re screwed

Let’s assume the history of rollup A is lost, and a contract on rollup B relies on a contract on rollup A. Only users of that contract should be affected, if I understand correctly. Any damage faced is opt-in? Users on rollup B not using this contract, or users on rollup C are unaffected if history of rollup A is lost.

---

**samueldashadrach** (2021-09-30):

You’re right, opening up on how to elect validators is hard. Have replied to [@vbuterin](/u/vbuterin)

---

**samueldashadrach** (2021-09-30):

> if historical rollup state is lost and people notice, someone can re-process the shards

This will only work for until whatever period shard history is available though (if someone has fast enough processor). I assume shard nodes are typically not going to store history until genesis.

> slot N of shard 1 and slot N+1 of shard 1 are in practice almost as disconnected from each other as slot N of shard 1 and slot N+1 of shard 63

There are still differences though, such as how nodes are typically attached to one shard and one subnet, which has a uniform broadcast mechanism etc.

---

**samueldashadrach** (2021-09-30):

I felt bad about this post so I made a new post that has a clearer proposal.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samueldashadrach/48/3500_2.png)
    [Should rollups custody their own history?](https://ethereum-magicians.org/t/should-rollups-custody-their-own-history/7173)



> Off-shoot from my earlier post requesting tighter integration between rollups and shards
> Here’s a simple (not necessarily best) way of doing this.
> Validators follow the 64-shard spec as designed. 64 subnets exist and shard nodes exist for each subnet, same as always. Shard nodes defend security as they always do. Tight coupling exists, there is social pact to not accept chain if blocks from even one shard are unavailable.
> However, rollup nodes also exist. Rollup nodes only store those L1 bloc…

[@vbuterin](/u/vbuterin)

---

**vbuterin** (2021-10-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samueldashadrach/48/3500_2.png) samueldashadrach:

> Just to confirm, does this property apply only at the time of block inclusion or even say 3 months after?

I think we’re heavily relying on an assumption that this is extremely unlikely (ie. not going to happen). The amount of data that even a sharded chain will store is not *that* large (projected launch stats: 256 kB per 12 sec * 64 shards = 1.33 MB/sec = 40 TB per year). Block explorer companies, altruistic whales, etc can very easily afford to store 40 TB per year of data (you can buy the hard drives to store that yourself for [$880 per year](https://www.amazon.com/Seagate-Portable-External-Hard-Drive/dp/B07VS8QCXC?th=1)), so there’s a wide margin of safety even if we increase shard data further.

To encourage *practical easy availability* of that data, I think the most realistic answer is either block explorer companies providing paid APIs (if we’re lazy), or a proper decentralized data marketplace protocol paid for with channel payments (if we’re less lazy). The latter would incentivize anyone to store parts of history, and in that case the data storing nodes could configure themselves to specialize in eg. history of specific shards or relevant to specific rollups.

But from a practical point of view, the data availability consensus property is only expected to be directly enforced at point of block inclusion.

---

**samueldashadrach** (2021-10-04):

Thanks a lot for replying. Launch parameters seem reasonable. (Although, just to nitpick - the bandwidth costs in my country for residential region might be higher than that of buying the SSDs).

I probably did a poor job expressing myself so I’ll try again. If I understand correctly **Permissible number of shards is a direct function of the altruistic capacity of users**. Whether or we attain this number of shards right on launch I don’t know, just talking of ultimate limit. By altruistic capacity is just mean the amount of computational and storage resources being altruistically provided and the number of distinct users who cared to provide them.  And hence we should be doing anything and everything to get more users to “care”. Naive blockchain doesn’t benefit too much from 1000 nodes versus 100,000 nodes - sharded system benefits a lot.

And hence grouping blocks or networks by semantic content or economic value might make it easier to care. It’s easier for me to care about “OptimismPBC Mainnet 2” than it is for me to care for “Ethereum shard #43”, because the former is associated with distinct branding, economic activity etc. Bitcoin, Cardano, Solana, Polkadot all have different sets of users running nodes because they have different people caring about them for different reasons. Hence they’re not as tightly competing for the same pool of altruistic capacity the way ethereum’s shards are competing among each other.

Hence made the second post. [Should rollups custody their own history?](https://ethereum-magicians.org/t/should-rollups-custody-their-own-history/7173)

