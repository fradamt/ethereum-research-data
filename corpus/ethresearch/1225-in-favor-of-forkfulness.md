---
source: ethresearch
topic_id: 1225
title: In favor of forkfulness
author: vbuterin
date: "2018-02-25"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/in-favor-of-forkfulness/1225
views: 9085
likes: 9
posts_count: 7
---

# In favor of forkfulness

There is a line of thinking that argues in favor of mechanisms that are fork-free; that is, mechanisms that immediately go from zero consensus to some definitive kind of finality, and do not have the possibility of “reorganizations” where partially confirmed blocks can get reverted. This post will argue that:

1. The whole notion of forkful vs fork-free protocols is meaningless
2. The faster confirmations of fork-free algorithms seen in practice are actually because they pick a different point on the finality time / overhead tradeoff curve
3. If we fix a particular point among the tradeoff curve, “forkful” (which actually really means chain-based) algos outperform “fork-free” (ie. a specific kind of non-chain-based) algos in terms of a certain kind of concrete efficiency. Specifically, Casper FFG fundamentally has a better tradeoff frontier (in fact, 20% better) than PBFT-style algos, and Casper CBC is potentially even better (in fact, 20-50% better than PBFT-style algos).
4. In the context of non-consensus applications that have surface similarities to consensus, like randomly sampled honest-majority votes, similar arguments apply. Is an randomly sampled honest-majority vote on some property of ongoing data (eg. transactions) is called for, a forkful chain-based system is in fact the best way to conduct such a vote.

---

Regarding forkfulness in general, the key thing to understand is fundamentally what forkfulness *is*. In any consensus algorithm, transactions (or collations, blocks, proposals, whatever) start off fully unconfirmed, and at some point become fully confirmed, at which point they cannot be changed without a large number of equivocations. But transactions don’t go from one state to the other immediately; at any time in between, clients can make intelligent guesses about the probability that transactions will get confirmed, and this probability for any given transaction goes toward 0% or 100% over time. This ability to make probabilistic guesses **is** partial confirmation, just like blocks in chains with a small number of blocks on top of them. And by definition of probability, these partial confirmations can, at least sometimes, get reverted.

Hence, *all* consensus algos (except dictatorship, where the dictator *can* provide a 100% guarantee immediately) are forkful. **It is entirely a client-side decision whether or not to expose the partial confirmation to users**; if a client does not, then the user will see a protocol state that always progresses forward and never (unless the threat model is violated) moves backward, and if a client does, then the user will see new protocol states more quickly, but will sometimes see reorgs.

---

To understand the next part, we need to brush up on the finality / overhead / node count tradeoff curve. Recall the funamental inequality:

\omega \ge 2 * \frac{n}{f}

Where \omega is protocol overhead (messages per second), n is the number of nodes, and f is the time to finality. Also expressed in Zamfir’s triangle:

[![DROeWQSXcAEbdzu](https://ethresear.ch/uploads/default/original/1X/2be4cb3506c0b8358bd54806704d3744ad0d88a6.jpg)DROeWQSXcAEbdzu386×296 14.6 KB](https://ethresear.ch/uploads/default/2be4cb3506c0b8358bd54806704d3744ad0d88a6)

The argument is simple: in all algorithms of the class that we are considering, you need at least two rounds of messages from every node to finalize something, and at that point there’s simply the choice of how often a round of every node sending a message takes place. Whatever is that period length p, finality takes twice that time, and the overhead in that period is \frac{n}{p}, so \omega = \frac{n}{p}, and since f \ge 2p, \omega \ge  2 * \frac{n}{f}. [see footnote]

Now we can better understand the different points on the tradeoff curve. In PBFT-style algorithms, there is some block time B (eg. 5 seconds), and for any block, f = B, so the overhead \omega = 2 * \frac{n}{B}. In a purely chain-based algorithm (eg. think Casper FFG, but where blocks are votes), you need n blocks or n * B time to go through every node to do a round of voting, so (for a checkpoint) f = n * 2B, and \omega = \frac{1}{B}. These are the most extreme points on the curve, though there are ways to get something in the middle (eg. f = \frac{n * 2B}{50}, \omega = \frac{50}{B}).

So we see that “non-forkful” algorithms can only get low finality time by accepting either high \omega or low n, and in reality they are simply one end of a tradeoff curve that has other possibilities. However, as we will see below, at *any* point on the tradeoff curve, we can improve performance by adding a chain-based structure.

Above, we looked at the finality time of PBFT and Casper FFG from the point of view of *blocks* (or rounds). But what if we look at it from the point of view of *transactions*? On average, each transaction has to wait 0.5 rounds to get into a round; hence, PBFT’s average finality time is actually 1.5* B, or 3 * \frac{n}{\omega}.

[![The-normal-operation-of-the-PBFT-algorithm](https://ethresear.ch/uploads/default/optimized/1X/b10769b8623d916b2b673e77610bbf9e4ce87a6e_2_690x178.png)The-normal-operation-of-the-PBFT-algorithm1300×337 30.1 KB](https://ethresear.ch/uploads/default/b10769b8623d916b2b673e77610bbf9e4ce87a6e)

In Casper FFG, data is finalized two epochs after it is included in a checkpoint, and on average a transaction needs to wait 0.5 epochs to get into a checkpoint; hence, Casper FFG’s average finality time is 2.5 * E, or 2.5 * \frac{n}{\omega}. Notice that it is specifically Casper FFG’s chain-based approach that allows a “commit” for older data to serve double-duty as a “prepare” for newer data and thereby speed up confirmations in this way.

![drawing-1](https://ethresear.ch/uploads/default/original/1X/94527e89ab4d5dfbc8c79d446e76e5e9e9619c19.svg)

I suspect Casper CBC may in fact have even stronger performance, at least in the case where the interval between checkpoints is longer than one block, as there is no need to wait for a checkpoint; as soon as a transaction is included in a block, two rounds of messages from all validators suffice to include it. This is because the safety oracle gets calculated on all blocks in the chain simultaneously, so a vote performs multiple duty in confirming every block behind it in the chain. Hence, average finality time is 2 * \frac{n}{\omega}, exactly the theoretical optimum.

Note also that because Casper CBC’s chain selection uses a GHOST-based algo, it is fully compatible with fancy DAG algorithms, and in any case other techniques can be used as well to fully explore the tradeoff curve in terms of target time to finality.

---

Another use case for this kind of reasoning is data availability voting on collations. Suppose you have a scheme where in order for a collation to be accepted into the main chain, we need signatures from N voters; the purpose of this is to enable “internal-fork-free” sharding where inclusion into the main chain immediately implies final inclusion within that history, while having an honest majority vote as an additional backstop on top of data availability proofs and fraud proofs to ensure that invalid or unavailable chains don’t get included in the history.

Suppose collations come once every T seconds, and we want N voters. Then, the overhead to the main chain is \frac{N}{T}, and a transaction needs to wait 1.5 * T to be finalized (half a collation round expected waiting time to be included in a collation, and then a further T to collect the votes). But instead, suppose that we had a forkful sharding model, where collations are organized into a chain, there is a collation once every \frac{T}{N} seconds (so same \frac{N}{T} overhead), and a collation can no longer be reverted once it is N confirmations deep in the chain. This has the same voting effect, but a transaction needs only to wait 0.5 * \frac{T}{N} + T time to be finalized, because of how the chain data structure allows the different stages of finalization to be interleaved with each other. And from a client’s point of view, a client can, if it wishes, only look at finalized collations, not see any reversions or forks.

---

Footnote: yes, threshold signatures, client-side random sampling and similar tech exists, but we are considering protocols that provide *cryptoeconomic incentivization*, which you can’t do with such schemes because you have to actually process everyone’s messages in order to reward or penalize them. Fancy algorithms that achieve consensus in one round of messaging in optimal conditions at the cost of large reductions in fault tolerance also exist, but we’re not willing to accept those reductions in fault tolerance ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

## Replies

**JustinDrake** (2018-02-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Is an randomly sampled honest-majority vote on some property of ongoing data (eg. transactions) is called for, a forkful chain-based system is in fact the best way to conduct such a vote.

Disagree! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I argue below that internally fork-free voting has *significantly* lower time to finality than forkful voting.

**Forkful voting**

Let’s first look at the forkful voting scheme. For concreteness we assume 2048 voters so that N = 1024. An eligible voter has the right to cast a single vote per period. Following [this spec](https://github.com/ethereum/sharding/blob/develop/docs/doc.md) for concreteness, let’s say a period is 5 blocks in the main chain, so a vote is cast every 5*15 = 75 seconds.

To be conservative let’s assume a best-case scenario where there are:

1. No gaps: The eligible voter always votes.
2. No forks: The eligible voter always votes consistently with the previous voter.
3. No repetitions: No two eligible voters within N periods are the same. (Notice none of the proposal mechanisms discussed so far on ethresear.ch have this property. Even perfect fairness does not guarantee no repetitions at the epoch boundaries.)

Given the above idealised setup we have achieved the following:

- Main chain overhead: The voting overhead on the main chain is 1 message per 75 seconds.
- Finality throughput: One final vote occurs every 75 seconds.
- Finality latency: From the point of view of ongoing data, finality happens in 75/2 seconds + 1024 * 75 seconds, i.e. 21.34 hours.

If gaps, forks and repetitions are taken into account, my guess is that time to finality would be over one day.

**Internally fork-free voting**

Let’s now look at the internally fork-free voting scheme. We set the same finality throughput of one final vote per 75 seconds, and also get the same main chain voting overhead of 1 message per 75 seconds. With such a setup what is the finality latency from the point of view of ongoing data?

Notice that in the internally fork-free scheme the casting of votes is done offchain. This has two significant messaging consequences:

1. Latency: We are not constrained by the 75 seconds onchain messaging latency per vote. Instead, the gathering of N votes can be done at full wire speed.
2. Parallelism: We are not constrained by the sequential nature of the forkful voting scheme. Instead, the gathering of N votes can be done in parallel.

Let’s conservatively assume that offchain latency with honest voters is as bad as onchain voting latency. That is, requesting a vote (a signature) from an honest voter and receiving the corresponding vote takes less than 75 seconds. Because of parallelism and the honest-majority assumption, a final vote can still occur in 75 seconds.

If in any given period voters finalise ongoing data from the previous period then finality from the point of view of ongoing data occurs in 1.5 * 75 seconds, which is less than two minutes.

**Conclusion**

We compared two honest-majority voting schemes with the same main chain overhead (1 message per 75 seconds) and the same finality throughput (1 final vote per 75 seconds). Assuming 2048 voters, the finality latency of forkful voting is on the order of one day, and the finality latency of internally fork-free voting is on the order of two minutes.

---

**vbuterin** (2018-02-26):

> Main chain overhead: The voting overhead on the main chain is 1 message per 75 seconds.

I think that depends entirely on what you mean by “main chain”. If you’re referring to overhead incurred by *clients*, sure, you’re correct. But that’s not the case when it comes to the overhead incurred by the proposer themselves. The proposer would still have to verify 1024 votes within 75 seconds in order to verify any collation they are including in their own blocks, and if they want to have, say, a windback of 10 blocks, then that goes up to 10240 votes within 75 seconds (reminder that this is all per-shard).

Basically what you’ve done is created a two-tiered random-sample vote system, where the first tier verifies the data directly, and then the second tier verifies the votes of the first tier. That does reduce the overhead of clients, but the second tier of voting still needs to fully verify the first tier of voting.

So you’ve found a loophole that can reduce *sustained* overhead, but not *burst* overhead. I suppose there is some margin for doing this, as the sustained overhead we’re willing to tolerate is lower than the burst overhead we’re willing to tolerate, but not that much.

---

**kladkogex** (2018-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The proposer would still have to verify 1024 votes within 75 seconds in order to verify any collation they are including in their own blocks, and if they want to have, say, a windback of 10 blocks, then that goes up to 10240 votes within 75 seconds (reminder that this is all per-shard).

If a threshold signature would be used, then a proposer would only need to verify a single threshold signature per collation …

---

**JustinDrake** (2018-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think that depends entirely on what you mean by “main chain”. If you’re referring to overhead incurred by clients, sure, you’re correct.

By “main chain overhead” I mean the overhead measured in messages (per second) that hit the main shard’s blockchain. Measuring the overhead this way is meaningful because onchain messages are the truly costly ones (one has to pay gas for messaging). The “main chain” is its own entity and all participants (clients, validators, voters, etc.) incur the same overhead of 1 message per 75 seconds to verify final votes.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The proposer would still have to verify 1024 votes within 75 seconds in order to verify any collation they are including in their own blocks

I’ll assume that “proposer” means anyone who wants to verify final votes. (There is no notion of “proposer” or “collation” in the abstract voting model.) To verify a final vote, a proposer has to download a single message. With BLS aggregation that message is 20 bytes and takes marginal time to verify.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> and if they want to have, say, a windback of 10 blocks, then that goes up to 10240 votes within 75 seconds (reminder that this is all per-shard).

BLS aggregation shines here because aggregation can be done across different messages. So a windback of 10 blocks is *still* a single 20 bytes message verified in marginal time, assuming the existence of “aggregators” that aggregate the final votes posted to the main chain. Without aggregators, a proposer has to download 200 bytes and verify 10 signatures for a windback of 10 blocks.

And the same trick can be done across shards. That is, assuming aggregators, all finals votes across all shards can be simultaneously verified in marginal time with a single 20 bytes message.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So you’ve found a loophole that can reduce sustained overhead, but not burst overhead.

Assuming aggregators, the burst overhead is constant and marginal, regardless of the burst!

**BLS signatures at the protocol-level**

I think [@vbuterin](/u/vbuterin)’s most likely rebuttal (![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12) !) is that BLS signatures are not quantum secure hence we can’t have them at the protocol level. I have a post with an approach to [safely deploying fancy crypto](https://ethresear.ch/t/cryptographic-canaries-and-backups/1235). In our case, the super-efficient BLS scheme can be backed by a less efficient signing scheme without aggregation, or be backed by the forkful voting scheme with higher finality latency.

---

**vbuterin** (2018-02-27):

In general, most of the efficiency upper bounds I argue are not hard theorems, and do have an asterisk that says “this can be overridden, but only with nontrivial fancy technology”; the scalability/decentralization/safety tradeoff that sharding itself breaks through is one example. And BLS signatures *are* nontrivial fancy technology ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

My other objection to BLS signatures though is that they have more complex overhead including distributed key generation, and are harder to incentivize.

> By “main chain overhead” I mean the overhead measured in messages (per second) that hit the main shard’s blockchain. Measuring the overhead this way is meaningful because onchain messages are the truly costly ones (one has to pay gas for messaging)

We’re talking about post-tight-coupling here, so these messages may not even cost any gas at that stage at all. What matters is the overhead incurred by the various actors in the system.

> I’ll assume that “proposer” means anyone who wants to verify final votes

At least in my own model, someone who proposes a block would need to include 20 collations in that block, and for each of those collations they would have to verify 1024 availability votes (I personally think 2048 is overkill, and a random sample of 50 suffices, but oh well), and they’d have to do all of that within 75 seconds, as that’s the time between when the collations are published and when the block needs to be published. I do agree that BLS can compress an arbitrary number of votes into a 32 byte sig (though I’d have to look at the overhead of generating the shared public key; you would probably not be able to reshuffle quickly and retain efficiency).

So in short, yes, with BLS you’re 100% right, and without BLS I think my point stands unaltered.

---

**kladkogex** (2018-02-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> hough I’d have to look at the overhead of generating the shared public key;

Here is a paper  [describing DKG for BLS systems](https://link.springer.com/content/pdf/10.1007/3-540-48910-X_21.pdf)

[and source code …](https://www.cryptoworkshop.com/ximix/coverage/org.cryptoworkshop.ximix.common.crypto.threshold/index.html)

