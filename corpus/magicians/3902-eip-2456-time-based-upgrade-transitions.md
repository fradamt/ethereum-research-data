---
source: magicians
topic_id: 3902
title: "EIP-2456: Time Based Upgrade Transitions"
author: shemnon
date: "2020-01-06"
category: EIPs
tags: [forks, eip-2456]
url: https://ethereum-magicians.org/t/eip-2456-time-based-upgrade-transitions/3902
views: 3494
likes: 5
posts_count: 12
---

# EIP-2456: Time Based Upgrade Transitions

Here’s an EIP to adjust how we designate network upgrade blocks.

- https://github.com/ethereum/EIPs/pull/2456/files
- (original pr) https://github.com/shemnon/EIPs/pull/2/files

For Ropsten and Mainnet both of the last two network upgrades have been off by a large number of days in each direction.  This is because of either the unpredictable amount of hashing power being applied to the network or because of the interaction of the Difficulty Bomb, pushing all of them more than two days off of the intended date.

The cliff notes version (read the draft for the real version) is that network upgrades would activate at the second “round thousand” of blocks after a specific time on the network, as reported in the blockheader.  Why the second round thousand?  In case the first round thousand is within an ommer re-org and to keep miners from playing too many games lying about the block time.

Comments or concerns?  please voice them.

## Replies

**ryanschneider** (2020-01-07):

Sounds reasonable to me.  With ~15 second block times 1999 blocks is about 8 hours, the actual fork should happen roughly 4-8 hours after the specified time, which seems like a reasonable maintenance window for teams to be on alert.  I guess a miner could try to trigger the fork up to two hours early by using a forward timestamp, so the window is really 2-8 hours.

The only real downside I see is that the fork block isn’t fully known ahead of time or explicitly enumerable w/ current JSONRPC methods, so it might be tricky for, say, a block explorer to correctly visualize blocks around the fork, though I can’t think of a concrete example.

---

**lucassaldanha** (2020-01-08):

I like the proposal. Monitoring forks has become crucial and the ~8h windows time in which the upgrade can happen will definitely make our life easier.

On the other hand, I agree with Ryan that not knowing the exact block number ahead of time is kinda of a bummer. However, unless this can introduce any known problems, I’m ok with it.

---

**holiman** (2020-01-10):

Also posted this on the PR, but reposting here.

> An upgrade will activate at a Transition Eligible Block if all of the following are true:
>
>
> The upgrade has not activated already.
> The timestamp of the block is on or after the TRANSITION_TIME.
> The previous Transition Eligible Block was on or after the TRANSITION_TIME.

If `A` is the previous TEB, and `B` is the current `TEB`, and the third bullet dictates that `A` is on or after `TRANSITION_TIME`, then there’s no need for the second bullet, since `B` is already defined to be *after* `A`.

(See EDIT below, the reasoning here is incorrect)

A separate problem, and IMO probably bigger problem, is that `ommer` blocks have no restrictions on time. So it’s fully possible to set an ommer block timestamp to one year in the future. Now, the parent of the `ommer` will be a `canon` block, so if we require the parent to be past the `TRANSITION_TIME`, a (malicious) miner can’t include future-fork ommers at will.

Not until after `TRANSITION_TIME`. After `TRANSITION_TIME`, let’s say there’s another ~week before the next `TEB`. In that period, miners could include forked ommers (meaning: ommer-blocks with future timestamps, which should be interpreted with the new rules) on every block.

It’s a bit unclear how that should be handled, and it may be depending on EIPs. For example, if we have a fork which redefines the PoW, then it means that when importing a block `N` (pre-fork), we might have to use post-fork rules to determine the header validity for the included *ommer* PoW.

These variations never occur on number-based forks, because we always know that block `N` only includes ommers with lower numbers, so the ommer can never be subject to `future` rules. This EIP changes it, so that an ommer can be subject to `future` fork rules.

EDIT:

I misunderstood the proposal. My reasoning above is flawed, since only an ommer with a particular `(block.number % TRANSITION_INCREMENT) == 0` can be a fork. That means a miner can’t litter the chain with fork-enabled ommers.

---

**shemnon** (2020-01-10):

One way to think of this is instead of developers picking a block number in an ACD call months in advance the protocol picks a block number 1000-1999 blocks in the future when the timestamp rolls over.  So the upgrade still transitions on a block number.

---

**carver** (2020-01-21):

I’m ![:-1:](https://ethereum-magicians.org/images/emoji/twitter/-1.png?v=9) on an implementation of time-based upgrades that requires looking up a bunch of historical headers to decide which VM version applies to a given header. (But I really like the goal of time-based upgrades)

Block-number-forking is conceptually clear, and lends itself to an API we’re happy with in Trinity: `get_vm(header)`. It would be a shame to lose that, and be forced to `get_vm(header, previous_headers=load_previous_headers(header))`. Especially when there might still be other options.

As far as I know, the two main concerns about direct timestamp forking are:

1. It opens new uncle validation edge cases
2. Some risk that miners will have a new incentive to manipulate timestamp away from current “true” time

So before we commit to making the VM application rules a lot more complex, let’s see if we can directly address these concerns, instead.

For example, maybe adding a rule that “uncles must have a timestamp older than the header that includes them” would get us most of the way there. (So we don’t have to deal with uncles on a future fork when the including header is on an old fork). Also, we probably need to formalize that we only validate uncle PoW, instead of validating all state transitions, and that the PoW validation happens according to the rules of the uncle header’s VM.

Also, my intuition is that the small-time timestamp gaming that might happen is not catastrophic. Any larger deviation would require a majority coalition of miners, as far as I can tell. I think the main concern is that miners might be incentivized to delay a fork (say, one that reduces block reward) and choose to increment the timestamp by 1 instead of to the current time.

One counterweight is that the difficulty would go up, also reducing their rewards. Another is that miners have similar operational needs for the predictability of the fork. If some miners start using this “strategy”, then the timestamp can by “caught up” to the “true” time in a single block. So as long as a majority of miners chooses to maintain current timestamp, any effect of a series of short-timed blocks can be erased quickly/easily. Obviously, it’s worth spending a little more time on this, and probably talk to some miners.

---

**carver** (2020-01-28):

Timestamp manipulation might actually be a bigger concern than I originally thought. I also think it affects all the implementations we have discussed so far.

Say that an upcoming fork cuts the block rewards in half. Miners have incentive to squeeze as many blocks as possible from the chain before the rewards are cut, even at the cost of doubling the difficulty. For simplicity, say that >50% of miners coordinate a strategy.

One strategy is a “time-squeeze” attack. Miners alternate between incrementing the timestamp by 1s and 18s (and avoid including uncles). [This would keep the difficulty steady](https://github.com/ethereum/py-evm/blob/f5c934173f53f72ae59fe8fd0ef21625ba8936b7/eth/vm/forks/byzantium/headers.py#L54), and reduce the average timestamp delta to 9.5s, no matter how long they actually take to produce. The header timestamp would drift further and further behind the “true” time. (The miner coalition would censor any blocks that try to make the timestamp “catch up” to the true time).

Compared to an average block time of ~14 real seconds, over a period of say 6 months (when the fork is announced to when the block rewards drop), they can squeeze out an extra ~47% more blocks, and cause the timestamp to drift ~58 days behind the true time.

Some problems from that are:

- Unnecessary block rewards (sad, but least worrying)
- Fork time is unpredictable again (back to status quo, ugh)
- Contracts that require a “near-true” timestamp would break (I don’t have any examples, but it seems problematic)

One possible mitigation is to wait to announce the fork timestamp until a few weeks before the desired fork date.

A late announcement gives less time for miners to apply the attack, so they can’t delay it in total as far. We still lose predictability: we would see the timestamp lag by ~7 days over a three week period. A three week announce period is already pretty tight for the upgrade cycle of: timestamp announcement, build, release, and operator upgrades. Though hopefully the benefit of the attack is small enough that it’s less likely to happen at all.  We would only have to consider this “late announce” mitigation on forks that reduce block reward.

---

**shemnon** (2020-01-28):

One mitigation that is already in place is that major clients do not consider blocks valid if they are too far in the future.  IIRC too far is 15 seconds.  So long as the clients don’t propagate these invalid blocks it would require the selfish cartel to meter out the blocks at an appropriate time.

I am also skeptical that it would take anything less than 51% of the miners participating in the mine-ahead approach would make enough money to overcome the development cost of executing the attack.  Although I haven’t run the numbers on this scenario.  This is presuming rational actors too, another potential flaw.

---

**carver** (2020-01-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> One mitigation that is already in place is that major clients do not consider blocks valid if they are too far in the future.

The time squeeze attack causes the time to drift backward. I don’t know of any constraint about the timestamp being too far in the past.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I am also skeptical that it would take anything less than 51% of the miners participating in the mine-ahead approach would make enough money to overcome the development cost of executing the attack.

I agree that it’s much easier to see that the attack is possible at >50%. At <50%, any miner can “fast-forward” the block time to the current time. Without the coalition of >50% needed to censor that “fast-forward” block, hopefully fast-forwards happen often enough that the drift never gets too large.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> This is presuming rational actors too, another potential flaw.

Sure, although the closer you get to the big revenue, the more effective rational behavior analysis seems to be. If you consider a situation where *all* block rewards are removed (like a switch to PoS), then it gets even stronger, and I think you might see a “soft” coalition of >50%, even if there’s not direct collaboration. The altruism effect is probably not very strong when the mining rigs are of zero value on Ethereum after a fork.

---

**carver** (2020-02-04):

On the uncle question: future uncles happened rarely, at least in the first 1 million blocks of mainnet.

~0.035% of uncles have a timestamp higher than the timestamp of the including header. 28 uncles were ahead, out of 80,364 total. The furthest ahead uncle was 82 seconds ahead of the including block.

Of note: the “ahead uncles” are tightly clustered, with all of them happening in block numbers 140,000-220,000. The 10k blocks starting at 170000 have an “ahead uncle” rate of ~2.1%.

At some point, I’d like to get data for the rest of the blocks, but it’s not at my fingertips right now.

---

**shemnon** (2020-02-16):

One thing I’ve been considering with my initial proposal is perhaps modifying the “lookback” to see if the fork acivates.  Possibly reeling it in from 1000 blocks to 10.

My principal motivation for such a large number was to keep a chain re-org from causing the fork to launch then  pull back.  However I think we could handle an abandoned activation.

What a lookback of 10 would accomplish is it would keep ommers from containing conflicting activation blocks that may or may not activate.  Clients should be keeping at least 10 blocks in memory to deal with possible chain re-orgs.  (IIRC geth handles up to 300 before issues start developing).

Keeping the activation at 1000 blocks reduces the search space that clients would need to examine if they are searching for the activation without any configuration hints.  The EIP would continue to be updated with the observed block for clients to work off of.  Once we get a finality gadget these observed blocks numbers would be as final as the gadget makes the chain.

So at `x%1000 = 0` we fork if the time of block `x%1000=990` is past the activation time.

---

**carver** (2020-03-12):

Just to tie off my previous comments: I’m in favor of immediate timestamp-based forking.

I don’t think the time squeezing attack is likely to be effective without 51% collusion.

Time spreading is already informally prevented, when clients reject blocks that are more than 15-seconds ahead of their wall clock. We can just formalize this across clients, and test for it in Hive. (traditional consensus testing doesn’t help here)

We ought to formalize some things about uncles:

- Uncle bodies are not used for validation, only the header. We validate the PoW, difficulty update, etc, but not transactions.
- Uncles may belong to a fork ahead of the including block. Validation is based on the uncle’s block time. The uncle rewards are based on the including block’s rules.

Last, we need to limit how far an uncle can be ahead of its including block, by timestamp. Allowing an uncle to be as much as 300 seconds in the future should be plenty of flexibility, while still preventing any “fork reassignment” in the future.

---

Note that in this approach, client devs can’t “refactor” the timestamp fork to a block number fork after activation. Activation needs to permanently be based on time. Refactoring to block number doesn’t play nicely with the p2p fork IDs anyway, so no big loss.

