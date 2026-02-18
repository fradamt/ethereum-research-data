---
source: magicians
topic_id: 2181
title: Alternative method to rent for alleviating the 'large and growing data' problem
author: tjayrush
date: "2018-12-10"
category: Working Groups > Data Ring
tags: []
url: https://ethereum-magicians.org/t/alternative-method-to-rent-for-alleviating-the-large-and-growing-data-problem/2181
views: 1205
likes: 2
posts_count: 11
---

# Alternative method to rent for alleviating the 'large and growing data' problem

I’ve read as deeply as I can into the not-yet-formally-proposed ‘rent’ model, and I wonder if there has been much discussion about alternative methods of alleviating the problem that rent is trying to solve.

I understand that rent is trying to solve the ‘long-term’ storage problem, but perhaps the promise of long-term storage itself is the problem. If the (implicit?) promise of long-term storage were removed, dApp developers would be forced to respond to that context by providing long-term storage themselves. In other words, they would have to write their smart contracts knowing that the data stored there had a lifetime. Instead of providing a rent mechanism, which seems wildly complicated (from a user perspective, not so much a developer perspective), perhaps a simple “old-data-will-be-evicted” policy would suffice.

If this were the case, the size of the chain data would stop growing at a certain point (all the blocks are full – new data is added to the head, old data falls off the tail).

Perhaps it’s a less useful system, but at least it won’t suffer from a problem that I foresee if a rent model prevails. My concern is that, over time, under a rent model, the entire chain will become “pay-to-play” making usage by those with lower resources more and more out of reach. This will create two sets of participants (haves and have-nots), which will kill any chance of building systems that maximize benefit for each individual and all participants at the same time (perato-optimal systems).

Yes – it’s likely I don’t know what I’m talking about, but I haven’t seen anyone else ask, so I thought I would.

Were alternatives to the rent model discussed and rejected? Or was the rent model the only alternative suggested to solve the ‘data is growing too fast’ problem? Are there other ideas to solve the problem?

## Replies

**samlavery** (2018-12-10):

I think state rent is simply a proposal that is being tested, I don’t think it’s officially going to be implemented on the main chain.  https://en.wikipedia.org/wiki/Cache_replacement_policies has a list of cache eviction policies, if they were going to implement one, I’d imagine it would be the least frequently used data policy, as it’s the most consumer friendly.

That said, a block chain is not a cache, it should be immutable and data should never be changed or removed without a secured and recorded transaction driving it.  If it doesn’t meet that standard, you can’t really trust it.  There is really only one solution to this problem, distributing the data.  That covers things like off-chain processing, lightning, plasma, sharding, IPFS, etc.  It’s a hard problem, but it’s been solved in other contexts before, it will be solved again in the crypto space.

We aren’t that far away from standards that allow blockchains to interact, cooperate, and affect change… state arbitrage is possible. Seriously, this is a smaller issue than people are making it out to be.

---

**AlexeyAkhunov** (2018-12-10):

First of all, thank you for reading the rent proposal! The next revision should be much simplified.

Alternatives to rent certainly exist. I must admit that I did not spend a lot of time searching for them, because I figured that if I did that, I would not have produced rent proposal yet. And also I thought that other people will kindly point me to the alternatives (which is what you are trying to do, thank you!)

After thinking about your proposed model, I realised that I briefly thought about it before, and came to the conclusion that it is roughly equivalent to rent, but with two differences. If someone really wants their data to be kept on the blockchain, they will keep “touching” or “modifying” it (whatever the rules of not getting “old” require). That would be accomplished by sending transactions, and effectively paying rent to miners (instead of burning it, as in the state rent proposal). That was the first difference (paying miners vs burning). The second difference is that the state rent proposal implies that you can pay rent upfront for long time, saving on number of transactions. If you use transactions to prevent things from getting old, that is equivalent to only being able to pay rent in small portions.

To the questions of pricing people out of the blockchain. You are right, there is a risk of diverging from parent-optimal system. What I would say to that - alas, we are think that the prioritising the survival of the platform over it demonstrating to everyone else what happens if the state grows too quickly (which is also a very useful experiment if you ask me). So I guess when the proposal is more well-formed and has PoC, and some specification, and some data behind it (that will take some time), we shall see if there is another viable alternative - I am sure most of people will be open to that. Currently we have a plan and we are working on it, until a better plan is found ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**tjayrush** (2018-12-16):

[@samlavery](/u/samlavery) Can you provide some pointers to “It’s been solved in other contexts…”?

[@AlexeyAkhunov](/u/alexeyakhunov) Thanks. I worry about unintended consequences as these, I think, tend to dominate in the long run.

---

**charles-cooper** (2018-12-27):

I’m not sure if this has been proposed before, but I’ve noticed that one of the biggest issues with syncing a node is RAM size. The larger the page cache, the less the node has to go out to fetch pages from disk, alleviating I/O pressure which is the biggest cost. Currently there is no incentive for dapp developers/users to be cache-friendly, which is why nodes need large SSDs - basically all the data needs to be in ‘warm’ storage. However, real-world machines use hierarchical storage (e.g. from hot to cold, CPU cache -> RAM -> SSD -> HDD), so creating an incentive structure to match that would enable node operators to make better use of hardware. The proposal is basically to make reads which go out to colder and colder storage to be more and more expensive.

Here’s a simple accounting model which is meant to model a hierarchical LRU cache. Define a global value, `READ_COUNTER`. Each value in the state database has a piece of metadata associated with it, `LAST_READ_COUNTER`. Each time a value is read or written to (i.e. `SLOAD/SSTORE`), `READ_OPS` is calculated as `log2(READ_COUNTER - LAST_READ_COUNTER + 1)`. `READ_COUNTER` is incremented by `READ_OPS`, and `LAST_READ_COUNTER` for that value is set to the new value of `READ_COUNTER`. The gas cost for the read is proportional to `READ_OPS` (e.g. `200 * (READ_OPS + 1)` would be the same as the current cost for `SLOAD` of a hot value, although the minimum could start out even lower at the cost of `MLOAD` assuming the value is already in memory).

`READ_OPS` is meant to represent the number of cache levels which need to evict words in order to read the new word, but perhaps it should have some sort of relation to growing block size for larger and larger storage. Another alternative is to model real hardware more closely, so instead of assuming infinite levels of caching, just 3 or 4 and having a specific gas cost for each of those levels. What do you think? I could be going down a complete garden path here but adjusting the gas cost for `SLOAD` seems very non-invasive compared to state rent and could significantly reduce storage costs for node operators.

---

**samlavery** (2019-01-08):

That’s kind of a neat idea, but it would be totally up to the miner to make up that cost.  That automatically makes it a non-starter.  Not all miners are equal, if I were sending tons of transactions, I would want my own node to have enough ram to fit the whole ethereum tree.  And if I’m running one of these super-nodes, I certainly don’t want to mine somebody else’s transaction, unless I have an open spot.  This breaks the notion of ethereum net neutrality, decentralization and democratization of public blockchains.

As for ‘alternative contexts’, look into the services offered by amazon and google.  There are lots of options for distributed/replicated databases.  Cassandra, mysql, postgresql all support some form of sharding, there is even an acronym: DDBMS.  Pied Pipers middle out compression is allegedly amazing, but I haven’t trialed it yet.

---

**charles-cooper** (2019-01-08):

[@samlavery](/u/samlavery) Thanks for the feedback! I’m not quite sure I understand why it would be up to the miner to make up the cost though. The idea is to make it more expensive for users to access cold storage, not less, so that accessed state is more likely to be in RAM/cache, making it more feasible to run a full node using off-the-shelf hardware. From a miner’s perspective, their revenue would go up. If users demand that miners have hot storage for their transaction, the miners need to purchase the hardware anyways, but in a universe where reads are more expensive they would actually get compensated for that directly.

---

**AlexeyAkhunov** (2019-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> Here’s a simple accounting model which is meant to model a hierarchical LRU cache. Define a global value, READ_COUNTER . Each value in the state database has a piece of metadata associated with it, LAST_READ_COUNTER . Each time a value is read or written to (i.e. SLOAD/SSTORE ), READ_OPS is calculated as log2(READ_COUNTER - LAST_READ_COUNTER + 1) . READ_COUNTER is incremented by READ_OPS , and LAST_READ_COUNTER for that value is set to the new value of READ_COUNTER . The gas cost for the read is proportional to READ_OPS (e.g. 200 * (READ_OPS + 1) would be the same as the current cost for SLOAD of a hot value, although the minimum could start out even lower at the cost of MLOAD assuming the value is already in memory).

I am assuming `LAST_READ_COUNTER` would need to become part of the state, otherwise it would not be possible to verify the gas cost of `SLOAD` with just having the snapshot of the state.

Firstly, it does add more data to store, though not much.

But more importantly, under this proposal, SLOAD will become a mutating operation (i.e. it will modify the state). The implications of this need to be analysed. As my analysis shows [here](https://medium.com/@akhounov/looking-back-at-the-ethereum-1x-workshop-26-28-01-2019-part-3-cc162ca04e9f), we have more than 10x “naked” SLOADs in the block than “naked” SSTOREs. Therefore, the number of state mutations of the state will likely grow quite a lot. That, in turn, will slow down block sealing, and will require SLOAD to be at least as expensive as SSTORE.

---

**charles-cooper** (2019-03-04):

[@AlexeyAkhunov](/u/alexeyakhunov) thanks for the insights! An idea I had for reducing the storage overhead is to have the counter be per 128 words (4096 bytes) rather than per 1 word.

Also, that is a good point about SLOAD becoming a mutating operation. Maybe though, SLOAD is underpriced and SSTORE is overpriced. Both leveldb and rocksdb use LSM trees, so the extra writes might have a very cheap marginal cost (amortized over all writes in a block) because they are sequential, while reads are always random. The original paper on LSM trees has some interesting performance insights



      [cs.umb.edu](https://www.cs.umb.edu/~poneil/lsmtree.pdf)



    https://www.cs.umb.edu/~poneil/lsmtree.pdf

###



119.65 KB










> However,  indexed  finds  requiring  immediate  response  will  lose  I/O  efficiency  in  some  cases,  so  the  LSM-tree  is  most  useful  in  applications  where  index  inserts  are more  common  than  finds  that  retrieve  the  entries.

Some data that could be relevant is presented in [this article](http://www.benstopford.com/2015/02/14/log-structured-merge-trees/). The author is just talking about sequential vs random reads, but the point is that random reads can be quite expensive.

> … somewhat counter intuitively, sequential disk access is faster than randomly accessing main memory. More relevantly they also show sequential access to disk, be it magnetic or SSD, to be at least three orders of magnitude faster than random IO.

---

**AlexeyAkhunov** (2019-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/charles-cooper/48/1308_2.png) charles-cooper:

> Both leveldb and rocksdb use LSM trees, so the extra writes might have a very cheap marginal cost (amortized over all writes in a block) because they are sequential, while reads are always random. The original paper on LSM trees has some interesting performance insights

Thank you, I am aware of this. Although designs based on LSM reduce the time it takes to create a write, they introduce so-called “write amplification”, where the same piece of data gets re-written multiple times (in background thread, during compaction), as it moves between the levels. That is one of the reasons (but not the only one) I have opted to change the database in Turbo-Geth, from leveldb to boltdb. It is based on more old-fashioned B+trees. Writes are slower, but there is less of write amplification. Reads are faster. There is no background compaction, there is transactional (ACID) behaviour (which reduced the risk of DB corruption). It does not use tons of file descriptors as leveldb does (because it does not need to have thousands of file).

If you look at my explanation in [here](https://medium.com/@akhounov/looking-back-at-the-ethereum-1x-workshop-26-28-01-2019-part-2-d3d8fdcede10), the state writes aren’t just DB writes, they actually generate quite a lot of DB reads (because the state root needs to be recalculated), therefore simply improving performance of DB writes won’t cut it, unfortunately.

---

**charles-cooper** (2019-03-05):

> I have opted to change the database in Turbo-Geth, from leveldb to boltdb. It is based on more old-fashioned B+trees. Writes are slower, but there is less of write amplification. Reads are faster. There is no background compaction, there is transactional (ACID) behaviour (which reduced the risk of DB corruption). It does not use tons of file descriptors as leveldb does (because it does not need to have thousands of file).

That’s neat! Is Turbo-Geth something I can help with? I once tried using bcache with parity and got terrible performance. I didn’t look into it too deeply but read/write amplification seemed to be the big problem (since writes get compacted two times, once by rocksdb and once by bcache). But maybe under your Turbo-Geth architecture bcache would actually work.

