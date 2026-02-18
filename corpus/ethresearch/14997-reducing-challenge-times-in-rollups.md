---
source: ethresearch
topic_id: 14997
title: Reducing challenge times in rollups
author: edfelten
date: "2023-03-08"
category: Layer 2
tags: []
url: https://ethresear.ch/t/reducing-challenge-times-in-rollups/14997
views: 6041
likes: 21
posts_count: 12
---

# Reducing challenge times in rollups

Optimistic rollups, and some other applications, assume that parties can always get a transaction included on Ethereum within some *challenge period*, which is conventionally seven days. The challenge period needs to be long enough to resist censorship attacks where a malicious actor tries to keep certain valid Ethereum transactions from being included on the chain.

I’ll describe below how we might be able to dramatically reduce the typical challenge period, by taking advantage of the fact that some types of censorship are more detectable under proof-of-stake than they were before. I’ll describe how to build a “censorship oracle” in a contract, which says either (a) there has not been censorship over the last N blocks with high confidence, or (b) no conclusion can be reached.  Then rollup protocols can accept their L2 state assertions more quickly if the oracle is reporting no censorship. If the oracle remains unsure, the rollup protocol would still wait up to seven days.

## Types of censorship

There are two types of censorship to worry about: block-building and forking (sometimes called “weak” and “strong” censorship, respectively).

Block-building censorship is when block builders refuse to include certain transactions in their blocks. Forking censorship is when validators collude to fork the chain so that blocks containing certain transactions are reorged away and don’t become part of the canonical chain.

Of these, forking censorship is the more difficult one to cope with, because it is repeatable. Block-building censorship fails if even one block is made by a non-censoring builder, but forking censorship can be repeated reliably if there are enough colluding validators. So forking censorship is the main reason for the seven-day challenge period in use today.

## Detecting (the absence of) forking censorship

The good news is that in proof-of-stake Ethereum, forking censorship leaves detectable effects: blocks that are forked away will show up as empty slots in the consensus chain. And a contract can detect the number of empty slots over an interval by comparing the change in block number to the number of slots (which is the change in timestamp divided by 12 seconds).

Of course there are other reasons why a slot might be empty, but at least we know that if few slots are empty, then few blocks could have been forked away. In particular, if we know that N non-censoring blocks were created over some time period, but fewer than N blocks are missing, then we can conclude that some non-censored block was included in the chain.

If we assume, for example, that at least 10% of validators will produce non-censored blocks, then each slot will propose a non-censored block with 10% probability, and over a long enough time period the number of non-censored blocks proposed will be close to 10% with high statistical confidence.  If fewer than 5% of blocks are missing during that time, we’ll be able to conclude with high confidence that some non-censored block was included.

The rest is a matter of statistical calculation.

## Formula and examples

Assume that each slot is assigned to a non-censoring validator with probability p.  Then the probability of seeing k or fewer non-censored blocks in n blocks is equivalent to the probability of getting k or fewer heads when flipping a biased coin that comes up heads with probability p.

The cumulative distribution function is

\mathrm{Pr}(X \leq k) = \sum_{i=0}^k {n \choose i} p^i (1-p)^{n-i}

which we can calculate numerically in practical cases.

For example, this implies that with n = 688 and p = 0.1, we can conclude that \mathrm{Pr}(X \leq 34) < 10^{-6}.

In other words, if we see 34 or fewer missing blocks out of 688 slots, we can conclude that a non-censored block was included with very high confidence.  688 slots is about 2 hours, 18 minutes.

Alternatively, if we see 4 or fewer missing blocks out of 225 slots, we can conclude that a non-censored block was included with very high (10^{-6}) confidence. 225 slots is 45 minutes.

### Observed rate of missing blocks

Over a recent series of 500,000 blocks, 3346 blocks were missing, a rate of 0.067%.  We can create a more aggressive test, testing whether fewer than, say, 0.1% of blocks were missing.

### Adding a non-forking assumption

The analysis above assumed that a fixed percentage of validators would not build censoring blocks, but it made no additional assumptions about forking censorship attacks. If we assume additionally a bound on the (stake-weighted) fraction of validators that will participate in forking censorship, we can get tighter bounds.

The reason this helps is that the above analysis assumed that a forking adversary can censor just exactly the blocks they choose. But if the forking collusion is limited, the collusion will sometimes be forced to suppress a run of multiple consecutive blocks, in order to get rid of one targeted block.  Accounting for this can give us a more sensitive test—one that can infer non-censorship with high confidence after a shorter delay.

But it’s also a more complicated analysis.  We’re planning to follow this post with a separate, longer piece that analyzes what is possible by adding non-forking assumptions.

## Proposed Implementation

A censorship oracle, implementing a procedure like the one described above, could be deployed as a mainnet contract for anyone to use.  Here is a strawman interface for such a contract:

```auto
interface CensorshipOracle {
    function testParameters(
        uint64 percentNoncensoringValidators,
        uint64 inverseConfidenceLevel,
    ) pure returns (
			uint64,  // test duration
			uint64,  // max missing blocks allowing test to pass
	);

    function startTest(
        uint64 percentNoncensoringValidators,
        uint64 inverseConfidenceLevel,
    ) returns (bytes32, uint64, uint64);

    function getTestInfo(
        bytes32 testId,
     ) view returns (
        uint64,  // percent non-censoring validators
        uint64,  // inverse confidence level
        uint64,  // test start timestamp
        uint64,  // test result available timestamp
        bool,    // test has finished
        bool     // (test has finished) && (non-censored block was included)
     );

    function finishAndGetTestInfo(bytes32 testId) returns (
        bytes32 testId,
     ) returns (
        uint64,  // percent non-censoring validators
        uint64,  // inverse confidence level
        uint64,  // test start timestamp
        uint64,  // test result available timestamp
        bool,    // test has finished (will be false if result not available yet)
        bool     // (test has finished) && (non-censored block was included)
     );
}
```

*Thanks to [@potuz](/u/potuz) and @terencechain for their contributions to this work and feedback on this post.*

## Replies

**jiayaoqijia** (2023-03-08):

Good post to discuss about shortening the challenge period. A quick question: how do we distinguish the censoring validators from non-censoring ones but missing blocks unintentionally due to network latency/other reasons?

---

**edfelten** (2023-03-08):

For rollup security purposes we have to assume the worst, that any missing block *might* be censorship.

So if too many blocks are missing due to non-censorship reasons, fast confirmation might not be possible.

---

**stonecoldpat** (2023-03-08):

I’ve seen people use the terms:

- Transaction filtering. A block builder is excluding transactions from their block.
- Block filtering. A block builder is excluding / deciding not to extend certain blocks due to their content.

That may help explain it a bit better.

For the transaction filtering, it would be interesting to see how it can be combined with the statistically analysis.

i.e., if you assume 99% of block producers are filtering the transaction, but only 20% are filtering blocks, then what is the ideal challenge window for that.

99% == 1 in every 100 blocks will contain the block, but then followed on by the chance of that being re-orged out.

But otherwise, really neat to see how PoS slots can be used to detect block filtering.

For the implementation, I imagine it could be a new opcode to fetch the slot data, perhaps similar to the sliding windows idea we had here:


      ![](https://ethresear.ch/uploads/default/original/3X/7/7/7737f9c766957e34da6871902e1e7a9d2aca40f3.png)

      [arXiv.org](https://arxiv.org/abs/2201.09009)



    ![](https://ethresear.ch/uploads/default/optimized/2X/b/b356ac871b8f89f8c62a235f06172c7d8cffe1f3_2_500x500.png)

###



Many prominent smart-contract applications such as payment channels, auctions, and voting systems often involve a mechanism in which some party must respond to a challenge or appeal some action within a fixed time limit. This pattern of...

---

**bbuddha** (2023-03-08):

Very interesting! The explicit statement of a minority trust assumption on validators seems to be pretty powerful.

One question I have is about the assumption that block proposers are chosen at random. This is true, ideally but there have been discussions of [RANDAO takeover](https://eth2book.info/bellatrix/part2/building_blocks/randomness/#randao-takeover). In such a case, there is a non-negligible probability that all of the proposers of a certain epoch were censoring, and they may be able to grind their RANDAO contributions together in order to only choose censoring block proposers over the next few epochs.

This would eventually be detected in the case of a longer challenge period, but these proposals look valid and ordinary to honest validators over short timescales.

I haven’t worked out the probabilities myself, but is this something that’s been considered/is it a realistic threat to the above protocol?

---

**potuz** (2023-03-09):

RANDAO Takeover is only feasible by

a) A very large stake (way above 50%) and

b) Witholding blocks

Even in a situation where a) holds, under b) the proposed algorithm would revert back to a 7 day challenge period.

---

**bbuddha** (2023-03-09):

Thanks for the response, I was going off of the numbers in the post of the censoring validators holding 90% of the stake. If the censoring validators took over RANDAO for the period described above, would they need to withhold blocks? If the only proposers were censoring, then wouldn’t they just need to not include fraud proof transactions? Perhaps I’m misunderstanding the beacon chain proposer selection mechanism…

---

**potuz** (2023-03-10):

If they didn’t need to withhold blocks it means that pure randomness assigned them blocks for the entire period, which is accounted statistically by the algorithm. RANDAO takeover requires you to omit some blocks in the end of the epoch to adjust the next epoch proposers. The number of bits necessary are higher themselves than the 1.6 that this algorithm requires missing per Epoch

---

**gMoney** (2023-03-15):

[@edfelten](/u/edfelten) Cool idea - what happens if the censorship oracle contract is itself being censored? Fall back to worst case (current challenge period)?

Outside of the censorship attack, would using a faster zk-based bridge for withdrawals (general messaging) to mainnet from optimistic rollups also shorten the challenge time or is the challenge period strictly required to guard against incorrect state transitions on the L2?

---

**edfelten** (2023-03-17):

The main idea is that you can do a transaction that accesses the censorship oracle, and if it says the chain has been censorship-safe, then your transaction proceeds to do some action.  So if your transaction is censored (which is the only way to prevent it from accessing the oracle, which is just another contract), then your transaction won’t do the final action–that’s a safe result.

---

**AndreP3Sigma** (2023-03-22):

> Good post to discuss about shortening the challenge period

It is indeed a good post to reawake the discussion about reducing challenging periods.

With the purpose of further discussing it, [@daniFi](/u/danifi) and I have proposed a model for dynamic challenging periods, which take into account the batch aggregated value, the fee competition in case of a DoS attack and sequencer decentralization. With our model, we can reduce the challenging periods up to 23h!

We divided ou proposal in a two-part article. Check our posts in the forum (and if you are curious, the corresponding articles in Three Sigma website) in:

Part I - [Challenging Periods Reimagined: Road to dynamic challenging periods - #2 by AndreP3Sigma](https://ethresear.ch/t/challenging-periods-reimagined-road-to-dynamic-challenging-periods/15077/2)

Part II - [Challenging Periods Reimagined: The Key Role of Sequencer Decentralization - #2 by AndreP3Sigma](https://ethresear.ch/t/challenging-periods-reimagined-the-key-role-of-sequencer-decentralization/15110/2)

---

**shotaronowhere** (2023-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/edfelten/48/11460_2.png) edfelten:

> Over a recent series of 500,000 blocks, 3346 blocks were missing, a rate of 0.067%. We can create a more aggressive test, testing whether fewer than, say, 0.1% of blocks were missing.

You’re off by an order of magnitude. Loots like ~% 1 of ethereum mainnet blocks missing on average.

During the Eth Tokyo hackathon my team and I made an attempt at an [implementation](https://github.com/shotaronowhere/CensorshipOracle/blob/5f18659c8fd4e73769ca48f90cf5ec5945fc64b0/contracts/src/censorshipOracle/CensorshipOracleEthereum.sol) of the censorship oracle and applying it to an optimistic bridge on Gnosis, a chain with the same consensus mechanism as Ethereum, except the slot time is 5 seconds, and the epochs are a different length (a couple more differences, but the point is the censorship test applies to Gnosis equally well).

Here’s a [dashboard](https://ethereumverse.vercel.app/) of weekly averages of missing blocks on Ethereum and Gnosis.

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/fc63a2408bde25a51984bdfae84e298a00f2d424_2_690x474.jpeg)image2064×1418 208 KB](https://ethresear.ch/uploads/default/fc63a2408bde25a51984bdfae84e298a00f2d424)

Notice that the shapella hardfork caused >10% of missing blocks in the first 24 hours (the daily resolution is not shown here, but if you check it’s ~10%). That’s the first “bump”. The second “bump” is the recent inactivity leak issue.

---

We also made this censorship test parameter [calculator](https://colab.research.google.com/drive/1-hcsqzQZX2OZouVfJZJ7tCjSQJ9Dh5Ay?usp=sharing) in google colab. The calculator uses the [mpmath](https://mpmath.org/doc/current/basics.html#setting-the-precision) library for arbitrary precision. The sample calculation matches the examples you provided.

