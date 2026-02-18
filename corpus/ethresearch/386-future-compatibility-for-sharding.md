---
source: ethresearch
topic_id: 386
title: Future-compatibility for sharding
author: vbuterin
date: "2017-12-28"
category: Sharding
tags: []
url: https://ethresear.ch/t/future-compatibility-for-sharding/386
views: 18576
likes: 28
posts_count: 17
---

# Future-compatibility for sharding

In my opinion, the current sharding spec as described here https://github.com/ethereum/sharding/blob/develop/docs/doc.md is basically already good enough to get us to thousands of transactions per second with reasonable security properties, as well as the ability to add cross-shard transactions as a not-that-difficult second step [do people agree?]. The demand for scaling is urgent, so it seems reasonable to just build this possibly with minor changes, launch it as fast as safely possible and go from there.

That said, I’d like to make sure that the design decisions we make also give us freedom to upgrade the design over time, and don’t end up hamstringing us in unexpected ways. Here are some ways in which we’ve been hamstrung so far:

- The lack of a chain ID in transactions made replay protection hard
- The lack of a version number in transactions made upgrading harder
- The fact that a transaction can access arbitrary parts of the state makes upgrades that facilitate parallelization hard
- The presence of synchronous cross-contract calls makes parallelization harder and makes re-entrancy attacks an issue
- The fact that code can be so large, and code is not in a Merkle tree-like structure, makes it hard to make reasonable bounds on the size of Merkle proofs

In sharded systems, there are many more tradeoffs. Here are ways that we could get hypothetically hamstrung:

- We agree to the 2L in 1L design (which commenters here seem to be positive on), but then decide that we want to switch to a design where contract storage is abstracted away entirely (eg. see Justin Drake’s proposals). Grandfathering in old-style contracts becomes a challenge.
- We start off with the stateless model, and make assumptions around it (eg. instant shuffling), but then decide that we want to switch to a model where the top level of the tree (ie. accounts but not storage or other accumulators) is guaranteed to be stored by clients/miners.
- We start off with the current “N shards” model, with synchronous calls within each shard, but then decide that we want to switch to a “one contract per shard” model. However, cross-shard calls can only be asynchronous, so we’d have to make synchronous calls retroactively not work.

Are there any other such gotchas we should be worried about? Are there quick tweaks we can make to the current proposal to limit them? I’d be willing to consider switching to the actor model for v1 (it’s not hard; basically, CALLs get processed only after all other CALLs, including the context that created them, end).

## Replies

**JustinDrake** (2017-12-28):

I agree with everything you write other than one critical thing, namely that Phase 1 as described in the current sharding spec should be the starting point. In my opinion, we should start with “Phase 0” which is the same as Phase 1 but with `SHARD_COUNT == 1` (as opposed to `SHARD_COUNT == 100`). I have arrived at this conclusion from the following four loose claims:

1. 10x scaling is sufficient:

In the short term (say, < 12 months) the best we can do for concrete scaling as a community is incremental (e.g. dev team addresses client bottlenecks and ships Casper, miners increase the gas limit and refine IT operations, application developers optimise contracts and experiment with offchain solutions, wallets optimise handling of fees).
2. In the medium term (say, < 24 months) thousands of transactions per second (100x scaling) is overkill. Combined with the above incremental solutions, 10x onchain scaling is enough to satisfy the urgent demand and give us breathing space to implement longer term scaling solutions achieving 100x and beyond.
3. The stateless model is a requirement:

Realistically sharding requires statelessness for reasonably-fast shuffling.
4. Phase 1 as described in the sharding spec includes the stateless model, so implementing statelessness is a strict subset of the current sharding roadmap.
5. The stateless model provides 10x scaling:

Even in the mildest form of partial statelessness where the top level of the trie is stored by miners, we will be addressing the key current bottleneck of I/O, yielding the desired 10x scaling.
6. This is especially true if we combine statelessness with basic parallelisation (e.g. the actor model) to leverage multi-core processors without being bogged down by I/O.
7. SHARD_COUNT == 1 is much easier than SHARD_COUNT == 100:

Shuffling and resynching across shards becomes a non-issue.
8. Cross-shard calls (between children shards) becomes a non-issue.
9. The existing networking stack around a single gossip feed can be reused.
10. Less design tradeoffs need to be made early on, yielding better future-compatibility for future sharding (the original point of this post) and accelerating the design phase.
11. Simpler spec, simpler VMC, less things to go wrong, less things to test.
12. All in all, I think we can hit production with SHARD_COUNT == 1 at least 6 months (probably closer to 12 months) compared to with SHARD_COUNT == 100.

In short, I think we should focus our design and implementation efforts on the stateless model (as opposed to sharding with more than 1 child shard).

---

**vbuterin** (2017-12-28):

Interesting. There is also a compromise where we take something like SHARD_COUNT = 8, where it’s actually reasonable for a high-bandwidth high-powered computer to run a super-full-node that tracks all shards.

I’m skeptical that stateless clients alone can really get us 10x with just one shard without serious sacrifices. For example, right now, a block full of simple transactions has 380 txs, and each tx has two Merkle branches, and at the 1 billion account size you get 380 * 2 * 1000 bytes = 760 kB, or 51 kB/s (or 400 kbps with a little b). If we go up 10x, that becomes 4 Mbps, and that’s *before* inefficiencies involving downloading the same data twice. A worst-case scenario where all gas is used on witness data might go up to 8-12 Mbps, plus overhead. That’s already going to make a full node unusable in probably the great majority of internet connections I use.

---

**JustinDrake** (2017-12-28):

Right, so the first bottleneck with stateless clients will likely be bandwidth. 380 simple transactions per block corresponds to 25tx/s, so let’s aim for 250tx/s. I think we may be able achieve that with a single child shard on a standard internet connection with the following considerations. (I use bits instead of bytes below for easy bandwidth comparisons.)

1. Multi-tries: This is an idea I call “accumulator sharding” in other posts. Basically instead of having a single trie we have multiple tries (say, 2^18 tries) each responsible for different 18-bit account prefixes. Instead of storing just one trie root (256b to sync and keep in RAM), stateless clients store 2^18 roots (256b * 2^18 = 8MB; no big deal to sync and maintain in RAM). What this means is that witnesses can be 18 * 256b shorter compared to if we had just one trie. (As a nice side benefit, multi-tries allow for easier parallelism. A monolithic trie is a global sequential bottleneck.)
2. Account onramp: The highest increase in new accounts recorded to date was 260,035 on December 21, 2017 (see here). Let’s 10x that to 2.6 million new accounts per day and assume we get that many new accounts starting form launch day T0. It will still take over a year to reach 1 billion accounts (365*2.6 million is less than 1 billon). So for example at T0 + 3 months we will have less than 250 million accounts, yielding a discount per witness of 2 * 256b compared to the 1 billion accounts straight-up assumption. (This discount is small and ignored in the final calculation.)
3. Today’s bandwidth: The state of the internet report for Q1 2017 lists Egypt as having the worst average connection speed of 2Mb/s, with a global rank of 143 (see page 40 of the report). Let’s use Egypt’s average connection speed as a conservative baseline.
4. Nielsen’s law: Connection speeds grow 50% per year, so the Q1 2017 number is already outdated by 50%. Realistically it would take at least a year for stateless clients to reach production (say, T0 = Q1 2019), giving us another 50% more bandwidth at T0. Finally, we’d then get another 50% bandwidth increase in the year during which accounts onramp to 1 billion. So our 2Mb/s Egyptian baseline is actually 6.75Mb/s at T0 + 1 year (Q1 2020).
5. Total bandwidth: Multiplying everything up, I get a bandwidth usage of 250tx/s * 2/tx * 256b * (log(1 billion) - 18) = 1.5Mb/s at T0 + 1 year, giving over 4x breathing space for inefficiencies and overheads relative to the 6.75Mb/s Egyptian baseline.

(It’s possible we can make further optimisations, like partial witnesses made possible by partial statelessness, and hash functions with a smaller bit size e.g. BLAKE-224 with 224b hashes.)

---

**vbuterin** (2017-12-28):

(1) and partial statelessness seem to be approximately the same thing, or at least similar in function. They’re also fairly similar to having N shards but giving each shard a lower gas limit, expecting clients to keep synced with all shards.

I’d also like to avoid the trap of spending substantial resources on achieving a 2x gain, when we can instead spend those resources on speeding up progress toward the 100x gain. There probably are 2x gains we can grab at low effort (like binary tries, which we’ve already implemented, and likely partial statelessness, and also E-WASM) but going for a bunch of little things like 224-bit hashes doesn’t seem like the best use of our time.

Though I do think the broader idea that we can achieve about an order of magnitude in gains while still having a large portion of the network processing all transactions is potentially valuable.

---

**JustinDrake** (2017-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> (1) and partial statelessness seem to be approximately the same thing

Yes! I made a comparison [here](https://ethresear.ch/t/multi-tries-vs-partial-statelessness/391) arguing that multi-tries are the way forward. Do you agree with my assessment?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> going for a bunch of little things like 224-bit hashes doesn’t seem like the best use of our time

Absolutely. The last two ideas in my original post (partial statelessness and 224-bit hashes) I added only for completeness. I *do* think that multi-tries are probably a simple and worthwhile thing to do, because they can provide a ~3x reduction in witness size, and have the additional parallelism benefits.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> They’re also fairly similar to having N shards but giving each shard a lower gas limit

In general, I think it is a very worthy endeavour to have somewhat “fat” shards with generous gas limits. The reason is that I expect cross-shard communication to be at least an order of magnitude more expensive than intra-shard communication. We want related to applications to fit in a single shard, and we want to avoid splitting large applications into too many shards.

---

**kladkogex** (2017-12-28):

> In my opinion, the current sharding spec as described here https://github.com/ethereum/sharding/blob/develop/docs/doc.md129 is basically already good enough

The spec does not talk much about cross-shard transfer …  In your talk at devcon3 you mentioned that the first iteration of sharding will only support one way transfers of ETH from the main blockchain to shards … Is this correct ? There will be no way to transfer ETH from shards to the main chain?

---

**vbuterin** (2017-12-29):

> Yes! I made a comparison here arguing that multi-tries are the way forward. Do you agree with my assessment?

It’s an interesting argument; seems reasonable but I feel like it’s worth thinking about all the different ways to implement it, especially in the context of an actor model.

> I do think that multi-tries are probably a simple and worthwhile thing to do, because they can provide a ~3x reduction in witness size, and have the additional parallelism benefits.

As much as 3x? How? Are you planning on having O(N^(2/3)) state roots?

> The reason is that I expect cross-shard communication to be at least an order of magnitude more expensive than intra-shard communication. We want related to applications to fit in a single shard, and we want to avoid splitting large applications into too many shards.

That’s true, though I think that as soon as cross-shard gasprice disparities emerge we’ll see equilibria where everything that doesn’t need network effects moves into the cheaper shards (“suburbs”) and everything that does stays in the more expensive shards that other dapps are in (“cities”). Also, I personally do not expect the process for making a cross-shard transaction to move your tokens into the same shard as a dapp to be that much more cumbersome than the process for, say, converting ETH to WETH as is required by dapps like Maker and Etherdelta. It will also help the community get used to asynchrony.

---

**vbuterin** (2017-12-29):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The spec does not talk much about cross-shard transfer …  In your talk at devcon3 you mentioned that the first iteration of sharding will only support one way transfers of ETH from the main blockchain to shards … Is this correct ? There will be no way to transfer ETH from shards to the main chain?

I *believe* that it should actually not be too hard to support relatively quick transfers from one shard to another. The thing that we need to be more careful about is transfers from shards back to the main chain; that really should require a longer withdrawal delay.

---

**turb0kat** (2017-12-29):

As an engineering manager, this “V1” project looks extremely ambitious.  It attempts to invent three entirely new engineering systems which have thus far only been in ‘research’ mode:  sharding, POS & stateless clients.

I think Justin’s suggestion to make V1 (V0) a single-shard version of this system is a fantastic one, because you can punt a lot of the engineering complexities of cross-shard management into future phases of work.

My initial gut reaction was to punt stateless clients out of V1 because I think this is where most of the engineering complexity lies.  Stateless clients create unpredictability in the system which will require significant engineering to mitigate.  What do I mean by this?  Bandwidth between archival nodes and collator nodes will be sporadic depending on the utilization of state.  Gas prices to do transactions will be unpredictable for application developers, who will have to closely monitor the usage of state, making the programming model significantly more complicated.  These engineering problems will make it dificult to get a smoothly functioning system off the ground and difficult for developers to adopt as a result of the added complexity.

Frankly I like the idea of getting a stateful client POS solution out with single shard.  This could be built very quickly, and sets up for a rapid release of multi-shard capability shortly thereafter.

One of the concepts that I think is missing from the longer term vision is the concept of dynamic shards.  With dynamic shards, application developers could, in the fullness of time, select shards with properties that best match with their application:  high collation cadence, high statefulness, large transaction payload, large collation size, etc.  With this concept introduced into the vision for the platform, it might even make sense to launch POW shards to unlock the scaling bottlenecks of the system very quickly.

---

**vbuterin** (2017-12-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/turb0kat/48/294_2.png) turb0kat:

> It attempts to invent three entirely new engineering systems which have thus far only been in ‘research’ mode:  sharding, POS & stateless clients.

Base chain PoS is independent of sharding. Do you see risks in the PoS implemented in the validator manager contract? To me personally, it seems totally fine; it’s very similar in form to existing naive PoS systems like ppcoin that have existed for years.

Practically speaking, we have resources and can parallelize; the code for one shard and many shards isn’t too different, and there are multiple teams that are interested in building implementations that could run different testnets. We’ll also get more info on the difficulty of implementing this once our python team makes more progress (they’re already quite far along!).

---

**turb0kat** (2017-12-31):

The PoS seems fairly well proven and doesn’t alter the programming model.  Stateless clients seem to introduce more uncertainty in behavior.  Separation of data and compute is a significant paradigm shift and one where you will want a lot of bake time on test net to empirically prove out the behavior under different workloads.  Hopefully front-load the stateless client test net and a robust suite of workload tests which push the limits of both stateless and state-heavy applications.

Executing these vaious aspects in parallel would be really impressive from a decentralized global programming organization, and really set ethereum’s ecosystem apart from many other smart and ambitious single-team initiatives.   Comparing to similarly scoped initiatives, this one looks somewhat akin to lightning, which has extended into a multi-year effort without delivering incremental value along the way.  So that has me worried and wondering what can be done to mitigate that risk up front.

In terms of testnets it will also need to be integrated with Casper, not sure what additional complexity that introduces but it seems like a lot of moving parts.

What is your sense for the timeframe in which this shard build could be completed and running against  main net?  Are you ok if it takes over a year?  Can ethereum retain its platform lead without a major scaling upgrade in 2018?

---

**JustinDrake** (2018-01-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> As much as 3x? How? Are you planning on having O(N^(2/3)) state roots?

As much as 3x reduction using ~N/1000 state roots overall. I define an “active contract” one that pays storage rent. (So dust contracts would get garbage collected away from the trie. On November 1, 2016 there were about [500,000](https://github.com/ethereum/EIPs/issues/168) dust addresses, which was about 2/3 of [all addresses](https://etherscan.io/chart/address).) Concretely (at least for the next few years), I expect a single shard to handle ~1 billion active accounts and not much more. So if we have 2^20 state roots per shard we get 3x reduction in witness size. With O(N) shards, we get O(N) state roots overall (specifically, ~N/1000) but validators only maintain a constant number of state roots at any given time (specifically, a small multiple of 2^20).

---

**turb0kat** (2018-01-04):

What is the incentive for “archival nodes”?  They seem to be responsible for maintaining all the state with no incentive as the validators are the only ones getting paid.

---

**vbuterin** (2018-01-05):

See the thread on Merkle branch provision markets: [Merkle branch provision markets for stateless clients](https://ethresear.ch/t/merkle-branch-provision-markets-for-stateless-clients/300)

---

**skilesare** (2018-01-06):

Re: Chain IDs

If we think forward to a potential sharing system where shards -> a very large number where some of these shards may be somewhat independent, could eip 155 (https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md) be used for chain ids if we adopt some kind of namespace system like chainID = uint256(keccak256(“eth.mainnet.shard.2345”))?

I may be mis reading but I think 155 works by manipulating v and v is a bytes4, right? So maybe we ave a much smaller space to work with?  Although function digs seem to use the first bytes4 of a 256 hash without much regard for collisions. So maybe we’re still ok? Maybe with the smaller space we can calculate collisions and reject those names?

If not I guess we are looking at having to add a chain I’d to the protocol. How much is that going to break?

EDIT: Whoops, looks like the max value of V is 255.  Boo.  Looks like right now you’d just need to be hyper careful about not using addresses across shards.

---

**turb0kat** (2018-01-07):

The archival bounty incentive seems interesting for true archival use cases.  My concern was in the context of sharding.  With the proposed PoS, only archival nodes keep state.  Let me try to clarify:

Users of archival nodes:

1. retrieving old merkle or state data
2. support of lightweight nodes / clients wallets
3. supporting collators in real time to build the chain (without which the shard is dead assuming stateless clients)

Focusing on #3:

1. why would archival nodes do all the work to support thousands of validators?  Bounty program doesnt seem to apply.
2. what is to prevent them from misbehaving given they have no stake?  Spamming bad merkle data seems a cheap DoS.  Delaying or ignoring collators that they don’t like seems a viable attack vector.

