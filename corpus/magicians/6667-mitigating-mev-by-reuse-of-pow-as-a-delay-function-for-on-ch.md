---
source: magicians
topic_id: 6667
title: Mitigating MEV by reuse of POW as a delay function for on-chain, probabilistic, transaction re-ordering
author: pankaj
date: "2021-07-16"
category: EIPs
tags: [mev, pow]
url: https://ethereum-magicians.org/t/mitigating-mev-by-reuse-of-pow-as-a-delay-function-for-on-chain-probabilistic-transaction-re-ordering/6667
views: 1814
likes: 0
posts_count: 20
---

# Mitigating MEV by reuse of POW as a delay function for on-chain, probabilistic, transaction re-ordering

# DOST (Delayed Ordered Sequence of Transactions) — An on-chain, probabilistic, transaction re-ordering proposal to mitigate MEV by reusing POW as a delay function

**This is a Request for Comments for a proposal to mitigate MEV. All comments and feedback are very much appreciated.**

## Proposal

The basic idea is that the POW calculation is already a cheap, on-chain probabilistic delay function — while theoretically not a [Verifiable Delay Function (VDF)](https://eprint.iacr.org/2018/601.pdf), POW could be practically reused to create an unpredictable, probabilistic transaction ordering in the mined block to mitigate MEV.

The proposal is for the Block Proposer (aka Miner) to do the same POW calculation steps as today, but change a few steps after that to achieve at the final transaction ordering as follows:

### Steps same as today:

1. The Block Proposer chooses any sequence of transactions they wish to include in the block B
2. The Block Proposer runs the proof-of-work algorithm Ethash to come up with a block nonce H_n as usual

### New Proposed Steps:

1. For each transaction t in the block B, compute Slot_t = KEC(H_n, TransactionHash) where KEC is the Keccak-256() hash function, H_n is the Block Nonce calculated from POW in Step 2 and TransactionHash is the hash of the transaction t
2. Order the transactions in increasing order of Slot_t. Let’s call this new sequence of transactions as DOST (DelayedOrderedSequence of Transactions)
3. The mined block will be considered enshrined in the blockchain with the transactions in the new DOST order
4. Note that the state (“World State”, gasUsed, stateRoot etc.) in the block header and the various hashes now technically need to change because of the changed transaction ordering. The key observation is that all these can be deterministically calculated independently by anyone based on the above DOST ordering steps. There are a few choices we have regarding what to include in the mined block header:

 Don’t change anything in the block - Other miners can recompute the changes required to the state and the block header deterministically using Nonce and the set of transactions. These don’t need to be stored on chain, just as many other deterministically computable things are not stored on the chain but are present as miner’s data structures
5. Let the block proposer recompute the block header based on the DOST transaction ordering. Store a single new hash H_DOST = KEC(new block header). Other miners can verify this hash H_DOST as part of their block verification process. This adds some data (32bytes at the most, though we can probably go with a truncated hash) but stores a commitment of the current state in the blockchain that all miners can verify
6. Note that because the transaction ordering anyway changed after POW, there is no point in computing some fields of the original block header that was input into the POW calculation (eg the original stateRoot, gasUsed etc. will all change after the DOST ordering). So an optimisation is that those fields are zeroed out (or we use BLOCKHASH) before POW, and then after POW and after the DOST ordering is known, those fields are populated based on the final DOST ordering. This saves the need to store any new data in the block header as well as saves the work of block proposer calculating the world state pre-POW

### Notes

(A) MEV fundamentally originates from the miner being able to dictate the exact sequence (ordered set) of transactions in the blockchain. The basic idea in this proposal is to remove this deterministic control. How to do so permissionlessly on L1 and unpredictably so that it can not be easily gamed by the miner? Luckily, POW itself presents a possible solution to the dilemma - we just use the Block Nonce *H_n* computed as part of the POW algorithm as the source of pseudo-randomness.

(B) Another way to look at this proposal is that POW is already a cheap on-chain probabilistic delay function — technically not identical to a [Verifiable Delay Function (VDF)](https://eprint.iacr.org/2018/601.pdf) as VDFs are theoretically defined to be sequential and deterministic, while POW is parallelizable and probabilistic. But POW is good enough and practical for our purpose of introducing a non-trivial time delay in being able to predict the transaction ordering in a block, making the final ordering unpredictable and thus non-gameable.

(C) At the same time, it is completely deterministic *post-facto* for any other miner or client to reconstruct the ordering steps and validate the block. Yet the ordering is non-deterministic from the miner POV at the time they are assembling the block. The block proposer could not easily (computationally) predict the final ordering of the transactions because of the effort required in doing POW in the first place. They an not simply try all combinations because trying out a single combination will need them to solve the POW first.

(D) It is reasonable to assume that the DOST mechanism (doing the Keccak hash based on Nonce and content-hash of the transaction) is *effectively doing a random permutation of the order of transactions in the block*. We can empirically check for this randomness historically.

(E) **Gas Usage**: Note that it is a very small amount of gas to do the extra DOST ordering work, so it is not much cost overhead. After the DOST ordering, recalculating the state and hashes does add extra work - where optimisation mentioned in Step 6.3) above will be useful.

(F) **Block data usage:** See choices under Step 6 above. The worst in terms of extra space used is Step (6.2) which still only adds a single 32B hash to the block. Other choices don’t add anything to the block.

## How DOST helps mitigate MEV

1. The proposal brings unpredictability to the final ordering of transactions. Let’s say the miner wanted to front-run a victim transaction Tv by inserting a new MEV transaction Tn in front of Tv. With DOST ordering, it is equi-probable whether Tv will end up in front of Tn or vice-versa. There is no way for the miner to know upfront, only by running POW and finding the block nonce. Likewise for a backrunning transaction. (Note that the miner can try to play probability games - e.g. by inserting two MEV transactions to increase their chances. All of this increases their cost and lowers expected reward so should disincentivize reordering).
2. Similarly for a sandwich transaction where the outer transactions T1 and T2 are sandwiching a victim transaction Tv, the probability is ⅙ that the exact sequence of transactions T1->Tv->T2 happens in the final DOST ordering

### Where DOST doesn’t help

MEV comes in various forms and DOST won’t help in some of them, for example:

1. This proposal only works on the ordering of transactions that have been already selected by the miner. The miner can still choose to censor (“delete”) a victim transaction and/or insert their own transaction.
2. The block proposer is free to not publish a block once they find that DOST ordering does not give them a favourable ordering. In that case, they might be forgoing the POW award which was theirs for the taking since they have already solved the POW puzzle for the block. If all miners do this, it could affect the overall effective hashrate of the network and block mining times. Mitigations could potentially include adjusting Difficulty to account for this system behaviour.

---

## Replies

**cgst** (2021-07-16):

Hi Pankaj,

One potential issue with this approach is that reordering may render some of the transactions invalid because of incorrect account nonces or insufficient funds for implicit gas purchases.

If one transaction is invalid, the entire block is invalid and thus ignored by the network, leading to wasted work. In other words, a miner may perform work only to discover the implied ordering invalidates the block. Under adversarial conditions, this scenario may occur with near certainty.

---

**pankaj** (2021-07-17):

## Same Sender Address Transactions

Jaynti has pointed out that as transactions sent from the same sender in a block need to be ordered by transaction nonce *nonce_t*, ordering by *Slot_t* as mentioned here won’t work for them. This is fixed easily by the following tweak:

- We still first order by Slot_t to get a random ordering of transactions across all txns as in Step 4.
- (Step 4.2) For each sender address, check if there are multiple transactions – then order them by nonce_t within the set of slots assigned to those transactions. For example, if the transactions with Slot_t values of 10,20 and 30 belonged to the same sender address with nonce_t values of 6,3 and 4 respectively – we would in this step do this reordering tweak and ensure that Slots 10, 20 and 30 have transactions reordered as the ones with nonce_t of 3,4 and 6 respectively. This still ensures non-gameability of the global txn ordering while preserving the requirement of nonce_t based ordering within same-sender transactions.

---

**pankaj** (2021-07-17):

Hi cgst,

Thanks for your comments. Please see the reordering tweak re respecting account nonces posted later.

Agreed that some txns may be rendered invalid because of gas or any other reason. This is somewhat addressed by Step 6 in the sense of how much explicitly we want the miner to record the changes because of the changed txn ordering, but to specifically talk about valid/invalid txns - the miner could indicate using a valid bit per transaction whether the txn is still valid, or we can roll that information into the the single hash *H_DOST* mentioned in Step 6.2

---

**cgst** (2021-07-17):

Masking out transactions invalidated by reordering might be problematic because it wastes block space, potentially close to 100% of block space under adversarial conditions.

I agree ordering may be tweaked to avoid invalid account nonces, but avoiding gas purchase failures post reordering seems much harder because it reels in arbitrarily complex EVM logic.

---

**pankaj** (2021-07-17):

> Masking out transactions invalidated by reordering might be problematic because it wastes block space, potentially close to 100% of block space under adversarial conditions.

1. Invalid transactions should be compressible, perhaps just to the information that was required as input to the POW, which could be as little as just the TransactionHash if we did the optimisation of Step 6.3 for instance and did not compute the complete state and the full block-header
2. Not sure why this would be a big deal though in the first place. We can certainly simulate this on past blocks and calculate the space overhead. Further, the randomized ordering should help overcome consistent adversarial examples – any adversarial examples you can think of that will consistently beat a randomized ordering and are undetectable prior to POW?

> I agree ordering may be tweaked to avoid invalid account nonces, but avoiding gas purchase failures post reordering seems much harder because it reels in arbitrarily complex EVM logic.

Yes, we won’t be able to and should not seek to detect potential gas failures that might happen after the reordering. I think these would be occasional failures anyway as per above.

---

**Arachnid** (2021-07-18):

Isn’t this trivially evaded by a miner? If a miner has a transaction they want included in a specific spot, and there are 100 transactions in a block, they only need to mutate the transaction ~50 times to find one that hashes to the place they want it to be.

Also, what happens if the block, after reordering, exceeds the gas limit?

---

**pankaj** (2021-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Isn’t this trivially evaded by a miner? If a miner has a transaction they want included in a specific spot, and there are 100 transactions in a block, they only need to mutate the transaction ~50 times to find one that hashes to the place they want it to be.

No, each time a transaction is mutated, the miner will have to redo the POW calculations to find the block nonce again first. Or am I misunderstanding your question?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Also, what happens if the block, after reordering, exceeds the gas limit?

Yes, this can happen. Similar to the preceding discussion with cgst about txns that might get invalidated post reordering, we can allow the miner to mark the reordered txn list in a few limited ways - eg we can allow them to mark transactions invalidated post reordering because of gas limit. This invalidation can be verified by the other miners too. Please also see Step 6 on discussion about some of the optimisations regarding this.

---

**Arachnid** (2021-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> No, each time a transaction is mutated, the miner will have to redo the POW calculations to find the block nonce again first. Or am I misunderstanding your question?

Ah, good point.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> Yes, this can happen. Similar to the preceding discussion with cgst about txns that might get invalidated post reordering, we can allow the miner to mark the reordered txn list in a few limited ways - eg we can allow them to mark transactions invalidated post reordering because of gas limit. This invalidation can be verified by the other miners too. Please also see Step 6 on discussion about some of the optimisations regarding this.

This seems like a problem. If the block is invalid if the max gas limit is exceeded, an attacker can force a miner to waste resources on invalid blocks. If the block is still valid, the miner can deliberately generate blocks that exceed the block gas limit. And if the miner can choose which transactions to invalidate to keep the block under the limit, they can cause it to deliberately exceed the limit, then ‘cancel’ transactions they do not want included in the block.

---

**pankaj** (2021-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> This seems like a problem. If the block is invalid if the max gas limit is exceeded, an attacker can force a miner to waste resources on invalid blocks. If the block is still valid, the miner can deliberately generate blocks that exceed the block gas limit. And if the miner can choose which transactions to invalidate to keep the block under the limit, they can cause it to deliberately exceed the limit, then ‘cancel’ transactions they do not want included in the block.

> If the block is invalid if the max gas limit is exceeded, an attacker can force a miner to waste resources on invalid blocks.

This is same as today, anyone can propose invalid blocks.

> If the block is still valid, the miner can deliberately generate blocks that exceed the block gas limit.

This would be deterministically verifiable, as today. All the info is still there in the block (or can be added as mentioned in Step 6)

> And if the miner can choose which transactions to invalidate to keep the block under the limit, they can cause it to deliberately exceed the limit, then ‘cancel’ transactions they do not want included in the block.

1. Since a miner can decide which txns to include in the first place, ‘cancel’ later does not seem to give any additional power to them in the first place
2. In any case, if this checking is needed, it can be done – since the ordering is deterministic after POW, another miner can verify whether the txns were canceled because of the exceeding of gas limit.

---

**Arachnid** (2021-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> This is same as today, anyone can propose invalid blocks.

It’s not the same as today, because today nobody can force a miner to propose an invalid block.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> This would be deterministically verifiable, as today. All the info is still there in the block (or can be added as mentioned in Step 6)

All you can determine is that the block was valid before reordering and invalid afterwards. You can’t determine if the miner did that deliberately or not.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> Since a miner can decide which txns to include in the first place, ‘cancel’ later does not seem to give any additional power to them in the first place

It absolutely can. They can insert a transaction that will use up more gas if it’s not the first in the block, to create a situation where they have to delete transactions. Then, they can insert a bunch of MEV transactions, and use the fact that the block is over-limit as an excuse to cancel all but the ones that are useful to them in the final ordering.

---

**cgst** (2021-07-19):

> Not sure why this would be a big deal though in the first place. We can certainly simulate this on past blocks and calculate the space overhead. Further, the randomized ordering should help overcome consistent adversarial examples – any adversarial examples you can think of that will consistently beat a randomized ordering and are undetectable prior to POW?

You can poison the mempool such that any valid ordering of N malicious transactions pre-POW will turn into almost N invalid transactions after reordering. Certainly, you can give the miners the ability to “mask out” some transactions post-POW, but you will have denied access to legitimate transactions in the first place. (I can elaborate on this adversarial example if you think it’s useful; in short, txns are signed by different accounts and coordinate intra-block with a shared contract to determine their relative order and decide to induce gas purchase errors.)

In essence, DOST may enable DoS attacks at a fraction of today’s cost because the attacker need not pay gas for “masked out” transactions.

---

**pankaj** (2021-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> All you can determine is that the block was valid before reordering and invalid afterwards. You can’t determine if the miner did that deliberately or not.

We shouldn’t need to. The mechanism needs to be robust.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> It absolutely can. They can insert a transaction that will use up more gas if it’s not the first in the block, to create a situation where they have to delete transactions. Then, they can insert a bunch of MEV transactions, and use the fact that the block is over-limit as an excuse to cancel all but the ones that are useful to them in the final ordering.

Let’s try to get concrete for clarity - let’s say we have 9 txns T1,T2,…, Tn included by the miner pre-POW. Let’s say T1 will use up more gas if it’s not the first in the block. When you say “Then, they can insert a bunch of MEV transactions”, you probably mean pre-POW because as mentioned earlier in our thread, miner will need to redo POW calculation otherwise. Now, because of the re-ordering the block is over the block’s gasLimit. Now, can you explain your scenario? Thanks

---

**pankaj** (2021-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cgst/48/4293_2.png) cgst:

> You can poison the mempool such that any valid ordering of N malicious transactions pre-POW will turn into almost N invalid transactions after reordering. Certainly, you can give the miners the ability to “mask out” some transactions post-POW, but you will have denied access to legitimate transactions in the first place. (I can elaborate on this adversarial example if you think it’s useful; in short, txns are signed by different accounts and coordinate intra-block with a shared contract to determine their relative order and decide to induce gas purchase errors.)

So to understand, somebody has (via a shared smart contract) constructed a sequence of N transactions T1, T2, … Tn which - if they are not in this precise order - cause nearly all of them to become invalid. Few questions:

1. Today a miner is free to choose the transactions in whatever order they want. How can an attacker be sure that this is the order their submitted transactions will get included in the block today? If an attacker submits such a set of txns, they have to be prepared to accept even today that this order is not respected by a miner, yes? They can give hints by setting txn gas fees etc, but those are just hints, no?
2. What happens today if an attacker floods the mempool with such a set of txns? The miner checks and can discard them, right?
3. If so, here’s a simple tweak to detect this - the miner can try out a couple of random txn reorderings before POW and ensure nothing drastically different happens that will change the state post a random reordering…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cgst/48/4293_2.png) cgst:

> In essence, DOST may enable DoS attacks at a fraction of today’s cost because the attacker need not pay gas for “masked out” transactions.

Let’s not jump to conclusions until we have agreed on the construction of the adversarial examples ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Arachnid** (2021-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> Let’s try to get concrete for clarity - let’s say we have 9 txns T1,T2,…, Tn included by the miner pre-POW. Let’s say T1 will use up more gas if it’s not the first in the block. When you say “Then, they can insert a bunch of MEV transactions”, you probably mean pre-POW because as mentioned earlier in our thread, miner will need to redo POW calculation otherwise. Now, because of the re-ordering the block is over the block’s gasLimit. Now, can you explain your scenario? Thanks

T1 is set to use a lot of gas if it’s not the first transaction in the block. This provides the “excuse” the miner needs to mask out transactions to bring the block back under the limit.

T2…Tn are potential MEV-earning transactions; they are profitable if they randomly get placed in the right position. The miner uses T1 to disable the ones that aren’t profitable.

Thinking about this more, this probably doesn’t actually save any gas over just including T2…Tn and having them revert if not profitable. That option certainly seems viable, though, and reproduces the state of the art pre-Flashbots, where much block space was taken up by bots competing for MEV opportunities. It could still be profitable for a miner to do this, but at the significant detriment to the throughput of the chain.

---

**cgst** (2021-07-20):

> if they are not in this precise order - cause nearly all of them to become invalid.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> Today a miner is free to choose the transactions in whatever order they want. How can an attacker be sure that this is the order their submitted transactions will get included in the block today? If an attacker submits such a set of txns, they have to be prepared to accept even today that this order is not respected by a miner, yes? They can give hints by setting txn gas fees etc, but those are just hints, no?

Precise ordering and inclusion would be too much to ask; instead, you’d devise a validation rule over the space of all ordered subsets (consisting of your malicious transactions) such that for any given subset of malicious transactions, only ~X% permutations are considered valid. Additionally, the rule has to overlap with tx selection heuristics (e.g., usually higher gas first) such that pre-POW ordering has a good chance to be valid.

> What happens today if an attacker floods the mempool with such a set of txns? The miner checks and can discard them, right?

The pre-POW selection is not impacted by these malicious transactions. A miner can greedily append one valid transaction at a time from the mempool to the candidate block. You can flood the mempool with many potential transactions such that a miner’s greedy search will likely find a valid pre-POW ordering of your malicious transactions. (By way of analogy, imagine you had to guess a secret permutation (hard), but you can validate prefixes of your guesses one character at a time (easy!).)

> If so, here’s a simple tweak to detect this - the miner can try out a couple of random txn reorderings before POW and ensure nothing drastically different happens that will change the state post a random reordering…

Certainly, you may sample random shuffles pre-POW to determine which transactions appear to be order-sensitive, and I agree the addition of this rule makes it more difficult to craft an adversarial example. By this point though, it’s getting  bit complicated because we have 3 tweaks in place (account nonce ordering tweak, post-order tx mask tweak, and now the shuffle sampling tweak), and these open up more questions:

1. The adversarial example can be triggered only for select miners as a function of block.coinbase (Ethereum Virtual Machine Opcodes). Thus, a malicious miner can force competitors to expend more time and effort on pre-POW selection. How much are we slowing down miners if they have to do pre-POW shuffle sampling? Will this lead to all other miners poisoning the mempool in a similar way?
2. Might miners be incentivized to spend incremental resources on finding better nonces (i.e., more advantageous to them) instead of just the first nonce? (e.g., double the hashing power and use it for finding two nonces and pick the one that pays highest MEV post-reorder)
3. Should miners have the privilege to choose the post-reordering tx mask (i.e., which transactions to remove)? If yes, it opens the door to a different kind of MEV.

Perhaps these questions too can be figured out, but the level of complexity/unknowns exceeds my confidence. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

A different adversarial example, perhaps easier to analyze: say there’s a CDP liquidation opportunity at current chain tip. I can send N transactions from different accounts and hope at least one will be randomly ordered early enough in the block to liquidate the CDP. All other transactions remain valid but bail out early if the opportunity is not available anymore. Best case: I capture the opportunity and waste gas for N-1 transactions; worst case: I waste gas for N transactions. You can afford a large N for high enough rewards… and so can everyone else. Isn’t this going to lead to blocks stuffed with useless front-running attempts?

---

**pankaj** (2021-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Thinking about this more, this probably doesn’t actually save any gas over just including T2…Tn and having them revert if not profitable.

This is possible today, right? The proposal does not make it worse - as mentioned in the proposal, it is not meant to solve all forms of MEV.

---

**pankaj** (2021-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cgst/48/4293_2.png) cgst:

> Certainly, you may sample random shuffles pre-POW to determine which transactions appear to be order-sensitive, and I agree the addition of this rule makes it more difficult to craft an adversarial example.

Exactly. A soft claim (hard to prove, but will try) is that randomized ordering is strictly better than status quo (a fixed ordering) with the same cost and some other conditions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cgst/48/4293_2.png) cgst:

> By this point though, it’s getting bit complicated because we have 3 tweaks in place (account nonce ordering tweak, post-order tx mask tweak, and now the shuffle sampling tweak),

If you zoom out, this is actually pretty simple and the tweaks are principled.

Besides, did we really think that a foundational problem as big as MEV will be solved by a 1-liner DOST reordering formula? ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cgst/48/4293_2.png) cgst:

> How much are we slowing down miners if they have to do pre-POW shuffle sampling?

I don’t have a good sense. Depends on how much is the POW calculation as a fraction of their total mining time? I would imagine POW takes almost all the time in terms of mining a block. If POW took 95% on average e.g., trying out 3 random shuffles will increase the rest of the 5% to at most 15%, or overall increase in work by only 10%

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cgst/48/4293_2.png) cgst:

> Might miners be incentivized to spend incremental resources on finding better nonces (i.e., more advantageous to them) instead of just the first nonce? (e.g., double the hashing power and use it for finding two nonces and pick the one that pays highest MEV post-reorder)

Totally possible, but we have just doubled their cost of something that can be done much easier today and the miner still has only a probabilistic MEV benefit even with double the cost.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cgst/48/4293_2.png) cgst:

> A different adversarial example, perhaps easier to analyze: say there’s a CDP liquidation opportunity at current chain tip.

But this can be done today at 1/Nth the cost. As clearly mentioned, the proposal is not meant to solve all forms of MEV. Will it lead to new forms of probabilistic attacks? Likely, but at a much higher cost than today. Let’s continue to find more adversarial examples, but randomization really helps I think.

---

Overall, the invalidating of transactions post-reordering is indeed a new modality and needs to be thought over more to get maturity. But this whole discussion shows that whatever adversarial examples one can think of, they seem to be either:

1. Easier and cheaper to do already today, so the DOST ordering only makes it more costly to do so plus making it harder (probabilistic) for the attacker to collect the reward
2. Unaffected by DOST ordering - as mentioned, the proposal is only meant to handle certain forms of reordering based MEV

---

**Arachnid** (2021-07-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pankaj/48/4277_2.png) pankaj:

> This is possible today, right? The proposal does not make it worse - as mentioned in the proposal, it is not meant to solve all forms of MEV.

No, but if it eliminates efficient flashbots-style MEV and only leaves inefficient ‘shotgun’ MEV, we may all be worse off than the status quo.

---

**pankaj** (2021-07-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> No, but if it eliminates efficient flashbots-style MEV and only leaves inefficient ‘shotgun’ MEV, we may all be worse off than the status quo.

I could be wrong but Flashbots-style MEV seems like corrective action to me. This proposal is in contrast an attempt at preventive action on MEV.

Philosophically, not trying to prevent extraction so that “efficient extraction” can happen seems backwards to me.

Overall, seems like both prevention and correction approaches should happen because this problem is so multi-faceted and complex.

