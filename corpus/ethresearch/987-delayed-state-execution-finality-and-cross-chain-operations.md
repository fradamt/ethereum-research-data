---
source: ethresearch
topic_id: 987
title: Delayed state execution, finality and cross-chain operations
author: vbuterin
date: "2018-02-02"
category: Sharding
tags: [stateless, execution, state-execution-separation]
url: https://ethresear.ch/t/delayed-state-execution-finality-and-cross-chain-operations/987
views: 6018
likes: 7
posts_count: 8
---

# Delayed state execution, finality and cross-chain operations

CC [@JustinDrake](/u/justindrake) [@vlad](/u/vlad) as this builds on a lot of ideas you’ve worked on.

In the sharding spec as it currently exists, and in the current ethereum blockchain, consensus on transaction ordering and state calculation are tightly coupled together. A block contains both a set of transactions, and a post-state root, so it represents a claim about both what the current transaction history is and the state after executing this history. This is convenient in many ways, but also has some significant drawbacks, which we will get into in this post.

The purpose of this post is to explore a different paradigm, one where the consensus process happens only on transaction ordering, and then a *separate* process exists to incentivize calculating state roots; that is, making claims of the form “the post-state root of the block with hash X is Y”; correct claims are rewarded and incorrect claims are penalized. The state execution process is at all times aware of the state roots at all block heights that it has already processed, so the state execution process itself is responsible for calculating incentive payouts/penalties for these claims.

Note that this implies that state execution is not a consensus game; even if 90% of executors say that the state root is Y1, from the point of any node that actually has done the calculations themselves (or received a SNARK proving them, or went through a truebit game proving them), if that node sees that the actual root is Y2 != Y1, then the majority of the executors get penalized and their result is thrown out.

### Some old research

This is a rabbit hole that I actually went down two years ago, which you can still find [in this Casper PoC 1 repo](https://github.com/ethereum/research/tree/master/old_casper_poc1). The idea there was even more radical: not only is state execution a separate process, but *consensus on the block at each height* is a distinct and separate process, so for example block 378224 could conceivably finalize before block 378223.

I used a quadratic scoring rule to incentivize claims on state; any validator could bet that the state root at height H is Y, and specify odds U (eg. odds 5 means that the state root is 5 times more likely to be Y than not, so in general odds U means probability \frac{U}{U+1}). If a validator makes a correct claim, they are rewarded U, and if they make a false claim they are penalized \frac{U^2}{2}; the maximum U is the one where the penalty for loss is a validator’s entire deposit. The purpose of this mechanism is to allow validators to make state commitments at various probability levels before the transaction history is even finalized, giving partial info to light clients as quickly as possible.

That said, at this point I favor keeping block consensus chain-based, and allowing claims on state roots with only a single (very high) level of confidence; we can avoid subjecting executors to uncertainty about consensus by making the claims *conditional* on the result of the block consensus process, so an executor submitting a claim (H, X, Y) would be incentivized as follows:

- Reward of R if the block hash at height H (which represents the entire history up until that point) is X and the state root is Y
- Large penalty of -D if the block hash at height H is X but the state root is NOT Y
- No reward and no penalty if the block hash at height H is not X.

The nice thing about the separation between execution and consensus is that it allows clients to take advantage of alternative ways of learning the state, like verifying SNARK proofs, playing different kinds of truebit games, calculating it yourself, having a “trust the executors by default but if one of N trusted service providers tells me something’s fishy execute it yourself” setup, etc.

### Consequences for sharding

This has several kinds of consequences for sharding. First of all, at least theoretically it’s possible to validate without having any state calculation logic whatsoever. However, realistically validators will want to learn the state so that they know what transactions they can include that would give them rewards. **A collator must have (approximate) knowledge of the up-to-date state** for this reason. They would also still want to have witnesses with transactions so that they can fully execute the transactions and know what their end state is. The infrastructure would thus end up being very similar in many respects, and if this was the end off the story it’s not clear separating the two has large benefits.

However, this is not the end of the story. It is highly desirable that in the sharding system we have a notion of cross-shard transactions. The usual way that cross-shard transactions are conducted is simple:

1. An operation on shard A creates a receipt on shard A (note: receipts are calculated as part of the state calculation process, so think of receipts as being kind of part of the state)
2. The receipt on shard A gets confirmed
3. An operation on shard B incorporates a proof that the receipt on shard A was confirmed, and performs some execution based on this.

However, there is a risk: what if, after this happens, shard A has a large reorg (ie. many blocks get reverted) but shard B does not, and in the new main chain of shard A the original receipt no longer exists? Then, you have a “dangling effect” in shard B without a cause, which is very dangerous and could lead to things like money being created out of nowhere.

We could simply have the reorg on shard A trigger a reorg on shard B, but that would be dangerous as it would be a DoS vulnerability: a small number of attackers reorging shard A could conceivably reorg *every* shard, if there is much cross-shard communication going on. The “dependency cone” of A will likely grow quickly. To prevent this, we can only go for the dumb solution: wait for the receipt on shard A to finalize, so that reorgs are simply not possible.

But separating state execution gives us another way out: if shard A does a reorg, then we don’t reorg any *transactions* on shard B, but rather we simply let the executors recalculate the state roots. Any operations on shard B that actually do depend on activity on shard A would have their consequences reorg’ed, but any operation on shard B that is *not* part of the dependency cone of the receipt would be left alone. Furthermore, it should be possible to calculate ahead of time that some operation on shard B is not part of the dependency cone of something in shard A simply by looking at the access lists of transactions (the access lists would be extended so that transactions can also access historical receipts on other shards), and so users would have private knowledge that their operation on shard B is safe and sound without waiting for confirmation from the global state root. With this kind of approach, we could allow cross-shard transactions to happen very quickly, possibly even allowing transactions to reference receipts from the most recent collation in some other shard.

### Statefulness and statelessness

As discussed above, validators in this model do need to be stateful, though it’s more acceptable for them to rely on partial guarantees, as if they use a wrong state root the only bad thing that will happen is that they will lose some fee revenue as they’ll include some transactions that are invalid (and will in this model be no-ops); there’s less systemic risk to the protocol if this happens sometimes, because there will be (stateful) executors on each shard and various kinds of interactive verification games can clean up any mess even if 90% of the players are dishonest.

Validators *could* use “see what the executors say about the state 25 blocks ago and execute the state after that point” as a heuristic for determining state, though it would be likely more optimal to use a hybrid strategy like “do that for the last 5 blocks, then download the last 100 blocks without witnesses to verify that they’re valid and available”.

In this model, transaction senders would need to propagate transactions with witnesses for validators’ benefit, though blocks could be broadcasted without witnesses if we rely on executors to be stateful. Note that this would once again imply that state size control is an issue, and so rent or other kinds of storage fees may be optimal.

## Replies

**JustinDrake** (2018-02-04):

I love the insight around cross-shard operations ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> validators will want to learn the state so that they know what transactions they can include that would give them rewards. A collator must have (approximate) knowledge of the up-to-date state

I want to push back on the bold part of the statement. The only thing collators care about is getting paid for including logs into collations. As such they only need partial statefullness to extend so far as to guarantee payment. A minimal stateful setup for this is a payment channel where payment is conditional on a Merkle proof of log inclusion.

In that scenario the collator couldn’t care less about the concrete up-to-date application state. It suffices for the collator to know the state of a single payment channel. (I’d argue the cleanest setup is to combine a log shard with a Plasma/Raiden/Lightning-like pay-for-inclusion system in a separate chain.)

---

**ihlec** (2018-02-12):

I see some similarities to the Execute-Order-Validate approach chosen by the Hyperledger Fabric platform (Linux Foundation).

Fabric is a private chain and lacks penalties, though the project provides inspirational value and plenty of experience, useful to a possible Execute-Order-Validate approach inside Ethereum.

Their architecture is best described in their recent paper. (https://arxiv.org/pdf/1801.10228v1.pdf)

---

**kladkogex** (2018-02-12):

I think separation of ordering of messages from the execution of smart contracts makes lots of sense, and Hyperledger already does a similar things.

For high-performance applications, an interesting “lazy update” possibility exists where the system does not by default maintain state roots for all blocks.

Instead, the state root is calculated only for, say, each 1000th block. This will make execution much faster since it is expensive to update Merkle trees all the time.

In this case, the state validation will be performed by the user.  If a user wants to find out the value of variable X, the user will make, say 32 parallel connections to 32 independent executors. If all of them report the same value of X, then the user will accept this value, since the probability of 32 nodes being Byzantine is (1/3)^32, which is 10^{-16}  If there is a discrepancy (which is not supposed to happen frequently), then the user will report it and each of the nodes will work starting from the last agreed state root to identify bad guys in Truebit-style and punish them.

Arguably Merkle trees introduce lots of overhead, a simple calculation like x = x + 1  leads to several expensive cryptographic hashes, so calculating state roots lazily can potentially speed up things a lot.

---

**djrtwo** (2018-03-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> No reward and no penalty if the block hash at height H if not H.

Should be “if the block hash at height H is not X”

---

**stri8ed** (2018-03-05):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> the user will make, say 32 parallel connections to 32 independent executors

No way to ensure executors are in fact different entities. Best you can do you (trustlessly), is require state claims to be backed by stake, which can be slashed on false claims. This would also require some reward for the valid claims, to incentivise participation.

Couldn’t the user just wait a few hundred blocks, until the state root is updated? What use cases are prevented, by not having immediate access to the latest state root? If I want to prove a more recent state where X = Y, I can provide proof of the transaction inclusion, and this can be used until the state is explicitly updated.

---

**vbuterin** (2018-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Should be “if the block hash at height H is not X”

Yep, thanks a lot!

> No way to ensure executors are in fact different entities.

You can if you find the executors by sampling from a global set.

---

**kladkogex** (2018-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/stri8ed/48/1493_2.png) stri8ed:

> No way to ensure executors are in fact different entities.

Since executors are randomly picked in order to have a significant number of identical executors (bad guys) you have a significant proportion of your network to be identical executors claiming different identities.

As some people suggested here, you could also have smart contracts compiled into things like logic circuits that allow for multiple optimized binaries, so that each node would run a unique binary.   You could then mutate the binaries from time to time and slash nodes that return the same results.

