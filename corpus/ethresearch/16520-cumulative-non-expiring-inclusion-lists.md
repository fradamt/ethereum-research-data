---
source: ethresearch
topic_id: 16520
title: Cumulative, Non-Expiring Inclusion Lists
author: Nero_eth
date: "2023-08-31"
category: Proof-of-Stake
tags: [censorship-resistance]
url: https://ethresear.ch/t/cumulative-non-expiring-inclusion-lists/16520
views: 3771
likes: 12
posts_count: 15
---

# Cumulative, Non-Expiring Inclusion Lists

# Cumulative, Non-Expiring Inclusion Lists

The following starts with a quick analysis of the [current inclusion list (IL) design by Vitalik and Mike](https://ethresear.ch/t/no-free-lunch-a-new-inclusion-list-design/16389) and is followed by a suggestion to better align it with the economic incentives of big staking pool operators such as Lido, Coinbase, Kraken or Rocketpool.

Get familiar with the current design [here](https://ethresear.ch/t/no-free-lunch-a-new-inclusion-list-design/16389).

Special thanks to [Matt](https://twitter.com/lightclients) for the great input.

## Background

**ILs are constraining.**

ILs force a certain transaction to be included if there is still enough space in the block.

This means that builders are constrained by not being able to freely decide upon the content of their blocks but must align with the IL in order to produce a valid block.

Furthermore, by having an IL, the amount of value that can be extracted from a block can only become less as the set of possibilities a non-censoring builder has when constructing blocks shrinks.

A second effect that proposers using ILs (and their successors) could initially face is that certain builders might stop building for certain slots if the ILs force them to include, e.g., an OFACed transaction. This is cool as it provides non-censoring parties strong competitive advantages.

> As a thought experiment: we should revive Martin’s Censorship-Detection contract. The contract allows the builder to claim some free MEV while sending 1 wei to the Tornado Cash Gitcoin Grants Donation contract. We can use/fund it to make sure that every single block contains a sanctioned interaction. Eventually, we may force censoring parties to entirely leave the block building market.

Notably, as pointed out by [Barnabé](https://twitter.com/barnabemonnot), censoring builders wouldn’t be forced to exit if they can otherwise ensure that their block is full. Thus they would have an incentive to sponsor certain transactions for users just to fill up their blocks.

## Same slot, next-slot, cumulative…

As a recap. Having proposers set ILs for their own blocks doesn’t make much sense and it relies purely on altruism to include censored transactions into one’s own blocks.

Having forward-ILs makes sense, allowing the current proposer to constrain the next proposer. This means that the current proposer could create an IL that either the current proposer itself or the next proposer must satisfy.

The problem with one-slot-forward ILs is that **parties with multiple validators have an economic incentive to not constrain the next proposer in the case the next proposer is controlled by the same entity.**

![il_forward_2](https://ethresear.ch/uploads/default/original/2X/2/26aa1947f6a6720fcf00af6da09776e66aa06ce4.png)

Party C has two consecutive slots and therefore leaves the IL empty in the third slot

This means, if I have two slots in a row, I would probably leave my ILs empty for my first proposer. Thereby I’d make sure to not constrain the builders in the next slot and thus act profit-maximizing. Centralization.

[![ILs_centralization](https://ethresear.ch/uploads/default/original/2X/5/579d4ce3e26e4b75fb68736bd235a08dc4125124.png)ILs_centralization388×186 5.21 KB](https://ethresear.ch/uploads/default/579d4ce3e26e4b75fb68736bd235a08dc4125124)

Assuming there is an OFACed transaction in every block then the number of consecutive slots a certain entity determines how often it can allow builders to work without constraints (=IL). Importantly, having no constraints doesn’t only mean being able to include some negligible TC transaction. It’s more about having access to the most profitable block builders in the ecosystem.

> In the past month, censoring builders such as beaver, builder69 or rsync offered proposer payments of around 0.061 ETH. Titan Builder, the largest non-censoring builder had 0.05 ETH.

## Potential Impact

Lido currently proposes blocks in around 30% of the slots. The chances of Lido having two consecutive slots are 9% (0.3**2). This can be confirmed by looking at the slots of the past month (2023-08-01 - 2023-08-28):

Lido had around 31% market share and the observed likelihood of consecutive slots of 9.5%.Assuming we have censored txs in every block and every honest validator puts them on their IL then 9.5% of the slots could have an empty ILs, potentially opening up the market for censoring builders.

#### How many slots would have empty ILs assuming that it’s economically rational for an entity to not constrain itself in consecutive slots?

Looking at data from the past month, it’s 10.5%, assuming the Lido Node Operators collude in order to maximize the profits for Lido as a whole.

Having the Lido Node Operators act independently and constrain each other with ILs, then only 1.9% of the slots would have empty ILs.

10% is very likely too high and an excessively large centralizing force.

2% is better but still not great as even every little advantage can have cascading effects and eventually harm decentralization.

#### The crux is, how to make sure that even those entities with consecutive slots are constrained and constrain others.

So, we need a way to have 100% filled ILs in the case that there is an e.g. OFAC sanctioned transaction paying enough to be included in the next block(s) (… and has not been included for xy seconds).

This can be achieved by having a cumulative Summary. The Summary, as described in the [IL post by Mike and Vitalik](https://ethresear.ch/t/no-free-lunch-a-new-inclusion-list-design/16389), consists of pairs of addresses and gas amounts that tell the proposer which transaction they’d have to include in their block.

By removing the one-slot expiry and allowing summaries to merge, a more aggressive design can be achieved.

## Forward-cumulative ILs

The construction of the cumulative IL would then also contain a third value which is the block number deadline. Transactions on the IL would be validated in the same way as in the original IL design post, but the gas must satisfy the block number deadline specified such that it is still paying enough to be included in a block at the specified deadline.

The base fee can increase by 12.5% per block. Thus, a transaction that should still be valid in, let’s say, 2 blocks.

**As an example:**

Increase per block d = 1.125.

Set of valid transactions tx \in txs.

Gas paid per transaction gas(tx_i).

Blocknumber deadline to include a tx k.

The basefee base(t_0).

So, in order to include a block k slots in the future, the block must at least pay base_{t+k} where base_{t+k} = base_{t0}*d^k, assuming the basefee increases in every block.

Thus, the maximum deadline k specified for each entry as a block number by the creator of the IL must satisfy the following:

gas(tx) \geq  base_{t_0+k} for every transaction.

This ensures that the transaction can still cover the base fee even if it is included k slots in the future.

Of course, there’s a conflict between including a txs sometime in the future and strong inclusion guarantees. Wouldn’t you still feel censored if your tx gets included even though someone put it on their IL 32 slots earlier?

That’s why k must be kept small (thinking of something between 2 and 5).

| Share | 2 consecutive slots | 3 consecutive slots | 4 consecutive slots | 5 consecutive slots |
| --- | --- | --- | --- | --- |
| 30% | 9% | 2.7% | 0.81% | 0.24% |
| 25% | 6.3% | 1.6% | 0.39% | 0.097% |

The probability that an entity with 30% validator share has 3 consecutve blocks is 2.7%, so may occur around 194 times a day. 4 consecutive slots occur 58 times a day and 5 consecutive slots occur 17 times a day.

[![Screenshot from 2023-08-31 19-23-00](https://ethresear.ch/uploads/default/optimized/2X/b/ba2c00713c3be3513c4955b5b5751e2fb081c510_2_690x268.png)Screenshot from 2023-08-31 19-23-00951×370 38.9 KB](https://ethresear.ch/uploads/default/ba2c00713c3be3513c4955b5b5751e2fb081c510)

Having forward-cumulative ILs with a k of 3 slots - thus the creator of the IL can have txs in its IL that must be included in slot n+k at the latest - would then bring the following adavantages:

- The IL doesn’t expire until the specified deadline of the entry is reached or the tx has been included
- More ILs because entities with consecutive slots can also constrain others further in the future if there’s a censored tx that pays enough.

This idea comes with one quite radical aspect. In the case that the Summary doesn’t expire but cumulates and aggregates over time, censoring validators with consecutive would be forced to miss their slot/get reored for their slots.

Let’s go through a quick example:

In this example, we deal with 5 different validators that are controlled by 4 different entities.  The validators in slot n+2 and n+3 are controlled by the same entity.

- Validators can specify a deadline for a fromAddress (and a gas value) to be included.
- Entries in the IL do not expire until the tx is included or until it reached the specified deadline.
- Validators accumulate and merge ILs from previous validators with their own. The merging works by grouping the extended list of summaries and grouping it by fromAddress while taking the min deadline.

By doing so validators can be precisely targeted to include a certain tx and only in very exceptional cases, when validators have more than k slots where k is the number of slots in the future the validator is allowed to specify in its IL.

## Conclusion

By spamming the mempool with censored transactions while having some kind of default client behavior that puts tx into an IL if they weren’t picked up by the previous validator (…or satisfy some other condition such as not being picked up for 5 blocks in a row), censoring validators would be completely kicked out of the ecosystem. For builders that stick to not building blocks that contain tx put on ILs, the landscape would change drastically because they would not be able to compete for most of the slots anymore. The same applies to relays that only allow blocks without certain txs.

## Replies

**potuz** (2023-08-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Notably, as pointed out by Barnabé, censoring builders wouldn’t be forced to exit if they can otherwise ensure that their block is full. Thus they would have an incentive to sponsor certain transactions for users just to fill up their blocks.

This assumes an IL design where the builder is allowed to not fulfill the IL if the block is full. You could instead cap the gas limit of the IL and force the builder to include it no matter what.

---

**Nero_eth** (2023-09-01):

Oh yeah. I think both designes have their advantages and disadvantages.

If builders must strictly follow the ILs and cannot stuff their blocks with other transaction it would be even more drastic against censoring buinlers as there’s no escape hatch left for them.

Allowing stuffing blocks to circumvent an IL would mean that for determining the head of the chain - I guess - one would need to be able to determine if a block was truely full or if one of the IL entries’ txs could still have been included. This sounds more complex than just strictly enforcing the IL.

---

**potuz** (2023-09-01):

Fwiw with a group of EP fellows we are specifying this and will have a PoC hopefully working in the coming months. The spec is completely broken right now but it’s advancing at a good pace



      [github.com/potuz/consensus-specs](https://github.com/potuz/consensus-specs/pull/1)














####


      `dev` ← `epbs`




          opened 02:28PM - 07 Aug 23 UTC



          [![](https://ethresear.ch/uploads/default/original/2X/5/57c38e1a2cefa95de639b5fe857cdd332c311c69.jpeg)
            potuz](https://github.com/potuz)



          [+2157
            -0](https://github.com/potuz/consensus-specs/pull/1/files)







Eventually this PR will become a full ePBS implementation. Main ingredients are
[…](https://github.com/potuz/consensus-specs/pull/1)

- In protocol staked builders.
- All Max EB changes from [this PR](https://github.com/michaelneuder/consensus-specs/pull/3) including execution layer trigerable exits.
- Forced inclusion lists.

Some design notes as the PR advances will be put in [this file](https://github.com/potuz/consensus-specs/tree/epbs/specs/_features/epbs/design.md)

EDIT: some items are outdated as we finalize the design of ILs. For example we will commit the summary to the beacon block and gossip only the transactions, this simplifies a bit some of the containers in this PR that are currently signed envelopes.

---

**mteam88** (2023-09-12):

I may be wrong about this, but doesn’t this rely on the assumption that there will be an honest proposer in the next `k` slots? Or else the proposer of slot `n+k` would essentially bear the burden of including the censored txns.

i.e. Proposer n creates an IL and the builders for slots n + (1…k) don’t include the censored txns (they are censoring builders) then the responsibility would fall on proposer n+k  to include them. Isn’t the odds still XX% that proposer n+k is operated by the same pool operator?

Maybe I am missing something, but I believe there is a significant chance that node operators still constrain themselves unless a vast majority of proposers are honest. In my model, the node operators have the following chance of limiting themselves:

Let s = operator share, j = ratio of proposers who include all txns present in IL (even when they don’t have to):

P(\text{self constrain}) = s * (1-j)^{k-1} + s^k

because (1-j)^{k-1} is the probability that no proposers have already included the txns on the IL.

Here is a table with my findings when share is 30%:

| k | j = 25\% | j = 50\% | j = 75\% | j = 85\% | j = 95\% |
| --- | --- | --- | --- | --- | --- |
| 2 | 22.5% | 15% | 7.5% | 4.5% | 1.5% |
| 3 | 16.875% | 7.5% | 1.875% | 0.675% | 0.075% |
| 4 | 12.66% | 3.75% | 0.47% | 0.10% | 0.004% |
| 5 | 9.5% | 1.88% | 0.12% | 0.015% | 0.0002% |

***Note:*** that this table doesn’t consider the possibility that the proposer is proposing for each consecutive block, so it isn’t complete. **I left out the probability of producing every block (s^{k}) to show the difference between the current model.** A complete table:

| k | j = 25\% | j = 50\% | j = 75\% | j = 85\% | j = 95\% |
| --- | --- | --- | --- | --- | --- |
| 2 | 31.5% | 24% | 16.5% | 13.5% | 10.5% |
| 3 | 19.575% | 10.2% | 4.575% | 3.375% | 2.775% |
| 4 | 13.47% | 4.56% | 1.28% | 0.91% | 0.814% |
| 5 | 9.74% | 2.12% | 0.36% | 0.255% | 0.2402% |

Extra note: as j approaches 100%, the above table approaches the current assumed values.

Just wanted to point out a pretty heavy reliance on honest proposers here.

I may be completely wrong about this, but would love some input! Please check my math ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Further research: calculate EV of a staking pool node operator based on difference between censoring or not censoring with these percentages to see if creating an IL makes sense.

---

**Nero_eth** (2023-09-14):

I think that’s exactly the point of having IL entries that are valid over a certain number of slots.

![](https://ethresear.ch/user_avatar/ethresear.ch/mteam88/48/20361_2.png) mteam88:

> i.e. Proposer n creates an IL and the builders for slots n + (1…k) don’t include the censored txns (they are censoring builders) then the responsibility would fall on proposer n+k to include them.

In this case, the builder’s censored block would not be chosen by the proposer (and not even forwarded by the relay) as it doesn’t obey the IL and therefore can’t make it into the canonical chain. So a censoring builder would have to fill up their blocks or they would not be able to participate in that slot. Censoring validators would have to chose a censored-but-full block or miss their slot.

**Let’s go through an example:**

We have 5 slots, n, …, n+4.

- I’m the proposer in slot n.
- Censoring party X is the proposer of n+1, n+2, and n+3.
- Censoring party Y is the proposer of n+4

I put a to-be-censored (bc, f.e. sanctioned) on my IL in slot n but don’t include it in my block yet. (We assume that the tx pays enough gas to be included in slot n+4, despite the base fee increasing 4 slots in a row).

**Scenario 1: No cumulative (thus expiring) IL:**

If party X wants to censor in slot n+1 and thus not follow my IL entry, they can fill their block with other txs until it’s full. Then, for their proposer in n+2 the IL would be empty/expired so that the proposer in n+2 doesn’t have any constraints.

The proposer in slot n+2 would also not create an IL to not constrain the proposer in n+3, as this slot is also controlled by party X. The proposer in n+3 however would put something into its IL in order to constrain party Y in slot n+4.

Eventually, if there are not enough txs to fill up the block, party X would only miss one block but since the IL expired, they would still be able to propose (censored) blocks in n+2 and n+3.

**Scenario 2: Cumulative, non-expiring IL:**

Here, party X, with their proposer in slot n+1 can do the same as previously, which is filling up the block to not be forced to follow the IL.

For slot n+2 the IL would still be valid such that the proposer in n+2 would also have to fill up its block to avoid including the tx on the IL. The same applies for the proposer in n+3. This means that party X must either include the tx on the IL or make sure to fill up it’s blocks 3 times in a row and if it can’t, e.g. because there are not enough tx that pay at least the base fee, then they would have to miss their slot.

This means, by including a to-be-censored tx in my IL, I force the following proposers to either have full blocks, miss their slots, or obey my IL and include the respective tx.

**Outcome:**

As a consequence, my IL entry cannot simply expire after one slot. Censoring validators with consecutive slots that can’t fill up all their blocks and also don’t want to include sanctioned txs are forced to miss their slots. In the above example, assuming there aren’t enough tx to fill up blocks, party X would miss all of their 3 slots. Same for party Y.

**Instead of proposing a block, the censoring parties would then have time thinking about if a censorship-resistant blockchain is the right place for them to participate or if they better move somewhere else.**

In a scenario where there’re always some txs in the mempool that certain parties would like to censor, censoring parties are forced to produce full blocks or miss their slot. The latter would hurt them economically and these parties would not be able to compete for a high APY anymore.

---

**mteam88** (2023-09-14):

Thank you! This definitely clarifies. I was under the impression that it was optional to include the censored txns until the slot where they expire. This makes a lot more sense!

---

**Nero_eth** (2023-11-21):

What are your thoughts on the centralizing impact of having only ‘next-slot ILs’, compared to those that don’t expire? This is particularly relevant when considering consecutive slots that large staking pools possess, which solo stakers do not. If we assume there are sufficient ‘sanctioned transactions’ to include one in every IL, then validators with consecutive slots could operate under fewer constraints (since they are not limiting themselves), while also having access to top builders (who are currently all engaging in censorship, with the exception of Titan Builder).

If censoring builders continue their operations but shift their focus to slots lacking sanctioned content in the IL, entities with consecutive slots could gain an economic advantage. This advantage could lead to staking pools being able to offer higher APYs, which constitues a centralizing force.

I believe that certain “games” will be inevitable (big staking pools constraining each other for higher yield). To counter centralization through IL games, we could consider allowing ILs to remain valid beyond a single slot. Specifically, an IL would stay valid as long as it can cover the base fee. Consequently, if I, as a solo staker, include some sanctioned content in my IL, and then am followed by, for example, two consecutive slots of entity X, this entity wouldn’t gain any benefits. This is because the content of my IL would remain valid for both slots, leveling the playing field.

---

**potuz** (2023-11-22):

The design I linked will make it a validity condition to actually include in full the IL, so not only are inclusion lists but forced inclusion lists, so no way around including those txs in N+1, no matter how many consecutive blocks you have.

---

**Nero_eth** (2023-11-23):

yeah right, I like this type of “strict ILs” that cannot be circumvented.

Though, having them only valid for the next slot helps large staking pools to gain even more power.

For the following, I assume that every IL will contain sanctioned content. Then, if you’re a large enough staking pool that has consecutive slots, you can leave the IL empty for the second/third/fourth consecutive slots to not constrain yourself (and have access to the best but censoring builders).

As a quick example:

An entity with 30% of stake will have 5 consecutive slots around 17 times a day. Thus, this entity will be able to “activate” censoring builders in 4 of the 5 consecutive slots. As the most profitable builders are censoring, this gives that entity huge advantages. Then, the IL has centralizing forces as this entity will achieve a higher APY.

In other words, if this 30% entity is censoring, they’ll only loose 1 out of 5 consecutive slots but then the IL empties/expires and the other 4 slots of that entity get away without constaints.

If the proposer of the slot before would be allowed to specify a deadline (or we just don’t empty the IL if the following slot is missed, this entity would miss all of their consecutive slots - which is, imo, an appropriate punishment for censoring and, in the long run, forces that entity to quit.

My proposal would be to not “expire” the IL after one slot but keep it valid/cumulate it until the txs is eventually included or until it cannot cover the basefee anymore.

---

**potuz** (2023-11-23):

I don’t see the point here: if you have forced ILs then the pool will not be able to avoid including the transactions in the first block of the sequence, then every next block will be able to censor since their proposers will not include an inclusion list. If you have non-forced ILs, then the pool will be able to censor in all blocks if they fill them or will have to include the transactions that were present in ILs from before. So nothing really changes here.

But also fundamentally the issue is that Inclusion lists are a mechanism for honest proposers to force that censored transactions are included on-chain. This is always under the assumption that honest proposers do want to force include these transactions. Of course if a large portion of the chain is not honest then the network will be a censoring network.

In general I tend to believe that this aims to solve a non-existing problem: defaults are sticky and if we ship clients that by default include inclusion lists with whatever heuristic, and make it so that the honest validator guide clearly states that the validator has to call the EL to request this IL, then validators will actively have to deviate from the honest validator spec to avoid including inclusion lists. If we live in a world where a large stake of validators are willing to censor and are willing to deviate from the spec, then the network is already broken to start with.

---

**Nero_eth** (2023-11-23):

Let me provide a better example:

We have the slots s_{t+1} ... s_{t+5}.

I control slot s_{t+1}.

The slots s_{t+2} ... s_{t+4} are controlled by an entity with 30% stake.

Slot s_{t+5} is controlled by a solo staker.

In s_{t+1}, I see a transaction in the mempool that is censored (was not included in x amount of block although the blocks weren’t full and it pays more than enough - propably because it touches a certain sanctioned entity).

I put that transaction into my IL.

Now if the censoring proposer in s_{t+2} has a problem with that transaction and wants to censor it, then it can simply miss the slot (this hurts, but, MEV will accumulate to large extents).

The same censoring proposer can also leave it’s IL empty, so that the proposer in s_{t+3} has no constraints.

Then, in s_{t+3}, again the same entity, having nothing in the IL because the transaction I put in the IL before “expired” after one slot, can build a block and use the help of all builders (not just one out of the 8 most profitable ones, as [7 out of the top 8 builders are currently censoring](https://censorship.pics)).

As already before, the proposer leaves it’s own IL empty so that the next has no constraints too.

In s_{t+4}, the proposer builds a block having access to the best set of builders and then puts a transaction into its IL that 7 out of the 8 best/largest builders don’t want to touch.

In s_{t+5}, the solo staker must obey the IL and can therefore only use the help of those builders that are willing to touch tranactions involving some sanctioned entity.

The outcome would be that my transaction was not included until s_{t+5} or s_{t+6}.

The entity that had 3 consecutive slot had to miss only one slot but was able to constrain other proposers while having access to the full set of builders for 2 out of 3 slots.

I fully agree with your point that this behavior is strictly bad and harms Ethereum, though, people will not be happy with sticking to the default. I wouldn’t be if I was in the US and had to force others to include certain transactions by default.

Also, I’d agree that defaults are sticky. I just think there will be demand to defect from the the default and I also think there will be supply for that. At least in Austria, the one who did something intentionally is in charge - I guess it’s similar elsewhere.

In the above example, if we allow the transaction that I put into my IL in slot s_{t+1} to not expire, then this entity controlling the slots s_{t+2}...s_{t+4} would lose all 3 slots if it wants to censor.

I’m just for handling censoring much stricter by, more or less, forcing those entities that doesn’t obey ILs to not only miss one slot, but all of their consecutive slots. Otherwise we could have a game where it’s more profitable to miss the first out of x consecutive slots while making all back in the following slot(s) (especially since the MEV will just cumulate and the set of builders is much larger).

That missing one slot out of many consecutive slots might not be that bad [was recently hinted](https://x.com/uriklarman/status/1726711420853870616?s=20) by [@uri-bloXroute](/u/uri-bloxroute) and I think, even though it might not compensate for missing multiple slots, it might be worth it if the consequence is missing only one slot.

Big validating entities will play with that part of the software, and currently they might get away for censoring too cheap. And missing a slot means that my IL expires and the transaction I put into it has no guarantee of a timely inclusion.

We should not rely on the default setting but instead make it very unpracticable to defect from the default.

---

**potuz** (2023-11-23):

> Now if the censoring proposer in s_{t+2}  has a problem with that transaction and wants to censor it, then it can simply miss the slot (this hurts, but, MEV will accumulate to large extents).
> The same censoring proposer can also leave it’s IL empty, so that the proposer in  s_{t+3} has no constraints.

This is not the way forced ILs work, if s_{t+1} included an IL no block is valid until the next proposer includes it, so if slot s_{t+2} doesn’t propose (or in ePBS if the builder for t+2 does not fullfill the IL of t+1 and therefore the payload is invalid) then at t+3 the IL that has that censored transaction is still valid.

---

**Nero_eth** (2023-11-23):

Oh nice! That’s exactly what I meant!

Kinda, a missed slot should not cause the IL to expire.

Thanks for clarifying that - we meant the same and I thought that in the current design an IL is only enforced for at max one slot in the future, no matter if that block is proposed or missed.

---

**potuz** (2023-11-23):

Take a look at the above linked PR for ePBS, it does include this exact design for forced ILs, it gets a little trickier in ePBS in which you now need to enforce that if say proposer for N had an IL, builder for N does not reveal (he should have satisfied the IL for N-1), so now the network has two ILs around the one for N-1 that has to be satisfied next and the one just released for N. The builder of N+1 needs to satisfy the IL for N-1, not that of N in this case, and the proposer of N+1 is not allowed to add an IL (so that the system catches up)

