---
source: ethresearch
topic_id: 10259
title: A model for cumulative committee-based finality
author: vbuterin
date: "2021-08-05"
category: Consensus
tags: []
url: https://ethresear.ch/t/a-model-for-cumulative-committee-based-finality/10259
views: 32235
likes: 34
posts_count: 18
---

# A model for cumulative committee-based finality

This is a proposed alternative design for the beacon chain, that could be switched to in the longer term (replacing the current planned CBC switch), that tries to provide some key properties:

- Deliver meaningful single-slot economic finality (ie. Tendermint-like properties) under normal circumstances

Make even single-slot reorgs much more expensive for even a colluding majority to execute, reducing consensus-extractable value (CEV)

Move away from heavy reliance on LMD GHOST fork choice, avoiding [known](https://ethresear.ch/t/decoy-flip-flop-attack-on-lmd-ghost/6001) [flaws](https://arxiv.org/pdf/2102.02247.pdf) and the need to introduce [complicated hybrid fork choice rules](https://notes.ethereum.org/6EAsltAXSIeMHeRztEGRdg) to fix the flaws.
Potentially allow a lower min deposit size and higher validator count
Preserve the property that economic finality eventually approaches a very large number (millions of ETH)

## Preliminaries

Let `CONSENSUS` be a asynchronously-safe consensus algorithm (eg. Tendermint, Casper FFG…). We assume that the consensus algorithm has some notion of slots or views where it makes one attempt at coming to consensus per fixed time period. We also assume that it takes as input a *weighted* validator set (existing BFT consensus algorithms are trivial to modify to add this property).

In the below design, we modify `CONSENSUS` so that during each view, the set that is required to finalize is different. That is, `CONSENSUS` takes as input, instead of a validator set, a function `get_validator_set(view_number: int) -> Map[Validator, int]` (the int representing the validator’s balance) that can generate validator sets for new views. `get_validator_set` should have the property that the validator set changes by at most \frac{1}{r} from one view to the next, where r (eg. r = 65536) is the recovery period length. More formally, we want:

\mathrm{
\Bigl\lvert\
diff(get\_validator\_set(i),\ get\_validator\_set(i+1))
\ \Bigr\rvert
\le
\frac{\bigl\lvert\ get\_validator\_set(i)\ \bigr\rvert}{r}
}

Where \lvert x\rvert returns the sum of absolute values of the values in x, and diff returns the per-key subtraction of values (eg. `diff({a: 0.1, b:0.2}, {b:0.1, c:0.3}) = {a: 0.1, b: 0.1, c: -0.3}`).

In practice, the diference between two adjacent validator sets would include existing validators leaking balance, and new validators being inducted at a rate equal to the leaked balance.

**Note that the \frac{1}{r} maximum set difference only applies if the earlier validator set did not finalize. If the earlier validator set did finalize, the `CONSENSUS` instance changes and so the `get_validator_set` function’s internal randomness changes completely; in that case, two adjacent validator sets can be completely different.**

Note that this means it is now possible for `CONSENSUS` to double-finalize without slashing if the view numbers of the two finalizations are far enough apart; this is intended, and the protocol works around it in the same way that Casper FFG deals with inactivity leaks today.

## Mechanism

We use a two-level **fork choice**:

1. Select the LATEST_FINALIZED_BLOCK
2. From the LATEST_FINALIZED_BLOCK, apply some other fork choice (eg. LMD GHOST) to choose the head

A view of the `CONSENSUS` algorithm is attempted at each slot, passing in as an input a validator set generating function based on data from `get_post_state(LATEST_FINALIZED_BLOCK)`. A valid proposal must consist of a valid descendant of `LATEST_FINALIZED_BLOCK`. Validators only prepare and commit to the proposal if it is part of the chain that wins the fork choice.

If `CONSENSUS` succeeds within some view, then the proposal in that view becomes the new `LATEST_FINALIZED_BLOCK`, changing the validator set for future rounds. If it fails, it makes its next attempt in the next slot/view.

[![consensus](https://ethresear.ch/uploads/default/optimized/2X/c/cbe1120fc5028aeca872be3713059acbdd8d9dce_2_690x296.png)consensus1116×479 63.7 KB](https://ethresear.ch/uploads/default/cbe1120fc5028aeca872be3713059acbdd8d9dce)

*Note: the slot should always equal the current view number plus the sum of the successfully finalizing view number in each previous validator set.*

We have the following **penalties**:

- Regular slashing penalties as determined by the consensus algorithm
- Inactivity penalties: if the chain fails to finalize, everyone who did not participate suffers a penalty. This penalty is targeted to cut balances in half after \frac{r}{2} slots.

### Alternative: single-slot-epoch Casper FFG

An alternative to the above design is to use Casper FFG, but make epochs one slot long. Casper FFG works differently, in that it does not attempt to prevent the same committee from finalizing both a block and a descendant of that block. To adapt to this difference, we would need to enforce (i) a \frac{1}{4} safety threshold instead of \frac{1}{3} and (ii) a rule that, if a slot finalizes, the validator set changes by a maximum of \frac{1}{4} instead of changing completely.

Note that in such a design, reorgs of one slot (but not more than one slot) can still theoretically be done costlessly. Additionally, “slots until max finality” numbers in the chart at the end would need to be increased by 4x.

## Properties

If a block is finalized, then for a competing block to be finalized one of the following needs to happen:

- Some committee is corrupted, and \ge \frac{1}{3} of them get slashed to double-finalize a different block
- The most recent committee goes offline, and after \frac{r}{3} slots the committee rotates enough to be able to finalize a different block without slashing. However, this comes at the cost of heavy inactivity penalties (\ge \frac{1}{3} of the attackers’ balance)

In either case, reverting even one finalized block requires at least `DEPOSIT_SIZE * COMMITTEE_SIZE / 3` ETH to be burned. If we set `COMMITTEE_SIZE = 131,072` (the number of validators per slot in ETH2 committees at the theoretical-max 4 million validator limit), then this value is `1,398,101` ETH.

Some other important properties of the scheme include:

- The load of validators would be very stable, processing COMMITTEE_SIZE transactions per slot regardless of how many validators are deposited
- The load of validators would be lower, as they could hibernate when they are not called upon to join a committee
- Validators who are hibernating can be allowed to exit+withdraw quickly without sacrificing security

## Extension: chain confirmation with smaller committees

If, for efficiency reasons, we have to decrease the `COMMITTEE_SIZE`, we can make the following adjustments:

- We rename “finalization” to “confirmation”, to reflect that a single confirmation no longer reflects true finality
- Instead of selecting the latest confirmed block, we select the confirmed block that is the tip of the longest chain of confirmed blocks (but refuse to revert more than COMMITTEE_LOOKAHEAD confirmed blocks, so COMMITTEE_LOOKAHEAD confirmations represents true finality)
- get_validator_set should only use information from the state more than COMMITTEE_LOOKAHEAD confirmations ago
- The view number should just be the slot number (this makes it easier to reason about the case where attempts to come to consensus are happening with the same validator set in different chains, which can only happen if breaking a few confirmations is possible)

This preserves all of the above properties, but it also introduces a new property: if a block gets *multiple* confirmations (ie. that block gets finalized, and a chain of its descendants gets `k-1` more confirmations, for a total of `k` sequential confirmations that affect that block), then reverting that block requires violating the consensus guarantee in multiple committees. This allows the security level from multiple committees to stack up: one would need `COMMITTEE_SIZE * DEPOSIT_SIZE * k / 3` ETH to revert `k` confirmations, up to a maximum of `k = COMMITTEE_LOOKAHEAD`, at which point the committees diverge.

Note also that the lookahead mechanic is worth doing anyway for p2p subnet safety reasons, so it’s probably a good idea to design the system with it, and if desired leave it to clients to determine how they handle confirmation reversions.

## Examples of concrete values

| COMMITTEE_SIZE (compare current mainnet: ~6,300) | COMMITTEE_LOOKAHEAD (= slots until max finality) | DEPOSIT_SIZE (in ETH) | ETH needed to break single confirmation | ETH needed to break finality |
| --- | --- | --- | --- | --- |
| 4,096 | 128 | 32 | 43,690 | 5,592,405 |
| 8,192 | 512 | 4 | 10,922 | 5,592,405 |
| 16,384 | 1,024 | 1 | 5,461 | 5,592,405 |
| 16,384 | 64 | 32 | 174,762 | 11,184,810 |
| 8,192 | 512 | 1 | 2,730 | 1,398,101 |

Note that the “ETH needed to break finality” numbers assume an attacker that has control over an amount of validators equal to well over half the total amount staking (ie. many millions of ETH); the number is what the attacker would lose. It’s *not* the case that anyone with 2,730 - 174,762 ETH can just come in and burn that ETH to revert a single-slot confirmation.

## Replies

**fradamt** (2021-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This preserves all of the above properties, but it also introduces a new property: if a block gets multiple finalizations (ie. that block gets finalized, and a chain of its descendants gets k-1 more finalizations, for a total of k sequential finalizations that affect that block), then reverting that block requires violating the finality guarantee in multiple committees. This allows the security level from multiple committees to stack up: one would need COMMITTEE_SIZE * DEPOSIT_SIZE * k / 3 ETH to revert k finalizations, up to a maximum of k = COMMITTEE_LOOKAHEAD, at which point the committees diverge.

Since the committee does not change much from block to block, can’t the attacker reuse most of the same validators for multiple finalizations? Does the requirement to burn `COMMITTEE_SIZE * DEPOSIT_SIZE * k / 3`  only hold if we assume that slashing messages won’t be temporarily censored during the attack?

---

**vbuterin** (2021-08-10):

> Since the committee does not change much from block to block, can’t the attacker reuse most of the same validators for multiple finalizations? Does the requirement to burn COMMITTEE_SIZE * DEPOSIT_SIZE * k / 3 only hold if we assume that slashing messages won’t be temporarily censored during the attack?

The committee changes 100% if it finalizes, it only changes by 1/r if it does not finalize.

---

**djrtwo** (2021-08-10):

To be clear: In the event of non “finality” of a slot for `N` slots, this results to the end user as a chain with zero capacity / no progress for `N` slots. Correct?

(example wrt diagram): we *cannot* build a `D'` on `C` unless `C` is finalized, right? Thus why `D` extends `B` and the work done in `C` is thrown out.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The most recent committee goes offline, and after \frac{r}{3} r3\frac{r}{3} slots the committee rotates enough to be able to finalize a different block without slashing. However, this comes at the cost of heavy inactivity penalties (\ge \frac{1}{3} ≥13\ge \frac{1}{3} of the attackers’ balance)

The attacker’s balance here only has to be a sufficient amount to disrupt progression of `CONSENSUS` for the slot, so this “heavy penalty” is only in relation to `COMMITTEE_SIZE`. Correct?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> reverting even one finalized block

By the use of “reverting” here, are you implying that this does not have the same notion of finality that we see in the beacon chain’s FFG today? That is – even if something is “finalized”, a node can locally revert without manual intervention (just that a minimum amount of ETH will be burned if such a reversion occurs)?

(example wrt diagram) If `C` and `D` were both finalized, we’d see slashing on something like 1/3 of set minus the potential 1/r delta. But in this case, we’d then revert to a fork choice rule to find the head? Or would nodes just be stuck on the branch they saw finalize first?

If fork choice between “finalized” blocks, then we might have two conflicting COMMITTEEs, right? or I suppose that depends on the randomness lookahead, if from N-1 for N, then you could, but it might be safer to do a much deeper randomness grab (even on the simpler of the two consensus designs).

If “finalized” items can be reverted without manual intervention, I might suggest we find an alternative term. “economically committed” or something…

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The load of validators would be very stable, processing COMMITTEE_SIZE transactions per slot regardless of how many validators are deposited

Ah, `COMMITTEE_SIZE` is *fixed* even as the validator set size grows. I didn’t catch that on first read. This would be parametrized based on assessed viable beacon chain load on consumer hardware (in concert with attempting to maximize per-slot security).

Validator per-slot attestation load *not* scaling with the size of the validator set is a very desirable property, imo. The network continues to grow and we daily continue to test our assumptions about the load we are able to handle here. For what it’s worth, I suspect that 100k+ validators per slot is probably *too* much. You can potentially slice the p2p network into many more subnets (`SUBNET_COUNT`), but we don’t currently know the limit to our current subnet/aggregation strategy (or how it is affected by total network node count).

As far as beacon block attestation load, we probably want to ensure that attestations can be aggregated as a final step by the block proposer into `SHARD_COUNT` types rather than having the payload only allow like-message aggregatability into `SUBNET_COUNT` types (assuming `SHARD_COUNT < SUBNET_COUNT`). Essentially, if I am on a sub-committee with duty to shard-N, even though I am sending on a sub-committee subnet, all subcommittees of shard-N should be able to be aggregated. This will ensure that beacon block attestation load remains roughly the same as today.

Assuming, we can carve out *many* more aggregation subnets, at that point the primary additional load will be the global aggregate attestation channel (which looks like roughly `TARGET_AGGREGATOR_COUNT * SUBNET_COUNT` messages per slot rather than `TARGET_AGGREGATOR_COUNT * SHARD_COUNT`.

---

**vbuterin** (2021-08-10):

> In the event of non “finality” of a slot for N slots, this results to the end user as a chain with zero capacity / no progress for N slots. Correct?

The chain would still progress, it would just merely have LMD-GHOST-level (or whatever other fork choice rule we use) security assurances

> The attacker’s balance here only has to be a sufficient amount to disrupt progression of CONSENSUS for the slot, so this “heavy penalty” is only in relation to COMMITTEE_SIZE. Correct?

Correct. The absolute size of the penalties is the second-from-right column in the table at the end of the original post.

> If “finalized” items can be reverted without manual intervention, I might suggest we find an alternative term. “economically committed” or something…

This is a good suggestion; I like “committed” (it fits together with BFT terminology, which is good).

> assuming SHARD_COUNT < SUBNET_COUNT

This depends a lot on what the subnet structure ends up being. For example, one possible subnet structure is to have 2048 subnets, where subnets `64*s.....64*s+63` (where `0 <= s < 32`) represent the 64 shards for dynasties `32r + s`. In this case, there would only be 64 subnets “active” in a particular slot. Each subnet would only have `COMMITTEE_SIZE / 256` validators, which seems like a manageable number for all proposed committee sizes.

---

**kladkogex** (2021-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Tendermint

Tendermint is actually synchronous or eventually synchronous

https://hal.archives-ouvertes.fr/hal-01881212/document

As the paper shows, even under these models, Tendermint needs to be tweaked to be provably secure

SKALE is an example of a provably secure asynchronouss consensus.

---

**kladkogex** (2021-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Inactivity penalties: if the chain fails to finalize, everyone who did not participate suffers a penalty. This penalty is targeted to cut balances in half after \frac{r}{2} r2\frac{r}{2} slots.

Penalty for short-term non-participation may be dangerous because it may be caused by outside events (for instance by network problems that split validators into groups). Or a bug in a particular majority client may prevent interaction with minority clients, ending up with punishment of minority clients)

---

**vbuterin** (2021-08-15):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Tendermint is actually synchronous or eventually synchronous

It’s safe under asynchrony but not live under asynchrony; same as Casper FFG, or for that matter Casper CBC.

Personally I don’t think live-under-asynchrony consensus is worth it; I remember looking at how those algos work, and they all rely on fairly complex machinery like common coins…

> Penalty for short-term non-participation may be dangerous because it may be caused by outside events (for instance by network problems that split validators into groups). Or a bug in a particular majority client may prevent interaction with minority clients, ending up with punishment of minority clients)

Agree! Hence why r needs to be fairly long (I propose 1-3 eeks).

---

**ittaia** (2021-08-15):

1. I think live-under-asynchrony consensus protocols have gotten less complex and more efficient over the last few years. In the happy path they (almost) as efficient as FFG. In the non-happy path, when asynchrony hits, they do need some source of randomness (like a random beacon say based on BLS threshold signatures) to make progress against an adaptive attack.
2. Rotating the committee each round of confirmation has many benefits, the shorter the committee exists, the harder it is to setup a collusion mechanism between its members. There more tricks to improve security and reduce collusion  (like making the committee members hidden until they speak and making them speak just once etc).
3. In the end if you bury a block by protecting it via a cumulative punishment slashing of x eth (over all the buried voting), then you will still be susceptible to a CEV that can extract significantly more than x eth. So the goal should be to protect blocks via fear of slashing both as quickly as possible and with as much total value as possible over time.

---

**kladkogex** (2021-08-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I remember looking at how those algos work, and they all rely on fairly complex machinery like common coins…

Yes - thats what we do at SKALE - use a common coin. There are very few viable common coins.  One of them is based on BLS threshold signatures - essentially hash of BLS signature of a counter is a common coin.

Another way to do a common coin is to use a VDF.

---

**samueldashadrach** (2021-08-21):

I’m not very convinced this should be implemented because:

- I do not wish the Merge to be delayed
- Once the Merge has completed, I’d prefer ossification and reduced centralisation of the network via developer control (any major network upgrade induces centralisation)

More specifically I’m not convinced the following reasons are worth it:

- reduce finality from 2 slot to 1 slot - I don’t think waiting 2 slots is that major a UX degradation.
- reduce complexity of code and fork choice rules  - Ethereum codebase is complex as it is and will always need full-time committed developer teams to rewrite, upgrade or manage. The proposed reduction in complexity does not change this.

A reason that might convince me is:

- Lower min deposit and higher validator count

But I’d still like to see more details on how significant the gains are. I would also like to more work on proposals such as [0x03](https://ethresear.ch/t/0x03-withdrawal-credentials-simple-eth1-triggerable-withdrawals/10021) to reduce control that staking pools have. This is arguably more important for validator decentralisation than reducing deposit size from 32 ETH to say 8 ETH, it is also a lot less work.

---

**gakonst** (2021-08-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> I do not wish the Merge to be delayed

I didn’t think that this was proposed as something to be included pre-merge?

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> reduce finality from 2 slot to 1 slot - I don’t think waiting 2 slots is that major a UX degradation.

The time to finality is 2 epochs, not 2 slots. During these 2 epochs reorgs can still happen today.

---

**vbuterin** (2021-08-21):

> I didn’t think that this was proposed as something to be included pre-merge?

Correct. My preferred timing for this path if we choose to take it is “after the high-priority changes to the beacon chain are done”. Meaning post-merge and even post-data-sharding.

---

**samueldashadrach** (2021-08-21):

Sorry, I got confused, I thought this proposal reduces it from 2 epochs to 1 epoch. I will read more on how likely <2 epoch reorgs are today, and whether the probability is high enough for this to be worth implementing.

---

**samueldashadrach** (2021-08-21):

There are people who are opposed to data sharding as well. (I’m not opposed but I have questions)

Sorry if this is blunt but is there value in discussing this proposal today? Considering we are yet to have sufficient data on what validator centralisation will look like in practice, or how likely reorgs will be in practice, both post-Merge and post-sharding. Or any other more critical problems that come up by then.

---

**mratsim** (2021-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> Sorry if this is blunt but is there value in discussing this proposal today?

Discussion about PoS started 7 years ago ([On Stake | Ethereum Foundation Blog](https://blog.ethereum.org/2014/07/05/stake/)) and sharding a long time ago as well.

The solutions that got out of those are constantly reevaluated and refined as new knowledge and usage are acknowledged, for example BLS signatures or the rollup-centric roadmap for sharding.

---

**fradamt** (2021-09-18):

I am wondering if there are situations where a committee might be incentivized to coordinate to purposefully not finalize just to keep being “in charge” and use this power to extract value

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> COMMITTEE_SIZE (compare current mainnet: ~6,300)
> COMMITTEE_LOOKAHEAD (= slots until max finality)
> DEPOSIT_SIZE (in ETH)
> ETH needed to break single confirmation
> ETH needed to break finality
>
>
>
>
> 4,096
> 128
> 32
> 43,690
> 5,592,405
>
>
> 8,192
> 512
> 4
> 10,922
> 5,592,405
>
>
> 16,384
> 1,024
> 1
> 5,461
> 5,592,405
>
>
> 16,384
> 64
> 32
> 174,762
> 11,184,810
>
>
> 8,192
> 512
> 1
> 2,730
> 1,398,101

Given the values in this table, the single-block inactivity leak would at most be 16384*32/r = 16384*32/65536 = 8 (and probably less, since it seems sensible to have the leak get worse as the time without successful consensus increases), which isn’t very high under certain circumstances. This might be the case during an MEV spike, for example we have recently seen an NFT drop which caused most blocks to have 100-200 ETH in miner rewards, for about 30 blocks. In such a situation, one could for example imagine a committee coordinating to not finalize and to force proposers to give up some of that revenue to avoid being censored.

To be clear, trying to get proposers to give up revenue from highly valuable blocks through threat of censorship is something that could also happen with Gasper, the main difference would be that the same committee could keep doing it, and that it would prevent finalization, which would be a bigger issue in a world where blocks normally finalize immediately.

Even assuming that this “forced smoothing by censorship” could happen, this specific avenue in which a committee does so for a while by stopping finalization is not very likely, because committees will probably (unless the stake becomes “too decentralized”) always statistically well-represent many entities in the whole validator set, and these would have no reason to prefer one committee to another. Still, just wanted to throw it out there and see if people have other scenarios in mind where it might make sense for a committee to pay the cost of the inactivity leak to keep being in charge

---

**vbuterin** (2021-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> I am wondering if there are situations where a committee might be incentivized to coordinate to purposefully not finalize just to keep being “in charge” and use this power to extract value

Interesting! One argument against this attack is that it’s extremely unlikely that a committee will be a coordinated group among themselves but not have a stake in the rewards of the other validators. Realistically, for *any* committee attack the be possible, there needs to be an attacker with the ability to control a near-majority of validators, and even though they could increase revenue for the committee, they would lose revenue in the non-committee validators that they control. Still a good argument for keeping the committee size not too low though!

(Edit: just realized that my reply is basically the same as your own last paragraph)

