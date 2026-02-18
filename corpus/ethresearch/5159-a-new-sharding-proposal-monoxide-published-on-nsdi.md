---
source: ethresearch
topic_id: 5159
title: A new sharding proposal "monoxide" published on nsdi
author: simanp
date: "2019-03-14"
category: Sharding
tags: []
url: https://ethresear.ch/t/a-new-sharding-proposal-monoxide-published-on-nsdi/5159
views: 2783
likes: 0
posts_count: 3
---

# A new sharding proposal "monoxide" published on nsdi

I have seen an interesting project focused on sharding, can you guys tell me whether it is a legit solution, thank you so much for your help. the link is here:https://medium.com/breaking-the-blockchain-trilemma/monoxide-nsdi19-a-solid-solution-to-blockchain-sharding-f7a7d89c1f5a

In recent NSDI’ 19 conference, monoxide was acknowledged as the first feasible solution to achieve scalability of blockchain system in the world. This disruptive research presents the first approach to achieving scalability in blockchain technology without weakening the security and the decentralization.

As introduced previously, the root cause of the scalability issue of blockchain systems is the current system design, which makes every node duplicating the workload of the entire network. It is nothing to do with consensus algorithms nor cryptography.

“Different groups of nodes working on a different partition of the network” is the fundamental idea of our design. This is the key to achieving the scalability of any distributed systems including blockchain. Besides the design, new technologies are developed to ensure security and decentralization.

The paper was attached here: https://www.usenix.org/conference/nsdi19/presentation/wang-jiaping

## Replies

**tawarien** (2019-03-15):

I read the paper and the problem I see (if I did not miss something) is that they assume that mining facilities / mining pools dominate the hash power, and that they have powerful enough systems to participate in each zone, where as individuals mine only one (or a few) zones and provide a small fraction of the mining power. This incentivices to join mining pools as these get fees / rewards from all zones but an individual miner only get fees from a few zones. This leads to a situation where their are a few pools with very strong computers that have enough ressources to produce and validate blocks for each zone and everybody with a computer not strong enough to process all zones will join a pool. This is a reduction in decentralization. It is a similar trade off to what dPoS systems makes but for PoW. This basically leads to a dPoW where the number of delegates is not fixed and in the worst case could degrade to an unacceptable low value (As more shards/zones their are as less mining pools that can process each shard/zone will exist).

They provide some sort of remedy to this with the suggestion that mining pools can delegate the validation and creation of candidate blocks for each tone to their participants but they do not describe how to reach consensus between the delegates, if they delegate just to one node then that single node inherits the full power of the mining pool which he can use to start an attack on his zone. If they delegate to multiple nodes the question of consensus arrives again on another level, which then reduces the security to whatever consensus and number of delegates is used for that process. If the mining pool checks the blocks produced by the delegates to ensure they do not cheat, then we are back to square one where the pool processes all shards/zones. But the biggest problem with that is that it is not part of the protocol and the pool can do whatever he likes. So in the end they either have reduced the decentralization or they have delegated the problem to another consensus mechanism

---

**vijayantpawar** (2022-08-31):

Hi I won’t able to understand chi-ko-nu mining algorithm. Can you explain if possible

