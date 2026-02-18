---
source: ethresearch
topic_id: 8993
title: Off-chain commitments for rollups
author: samueldashadrach
date: "2021-03-23"
category: Layer 2
tags: [zk-roll-up, rollup]
url: https://ethresear.ch/t/off-chain-commitments-for-rollups/8993
views: 3547
likes: 12
posts_count: 18
---

# Off-chain commitments for rollups

Have written a bit on how you can remove MEV, provide fast finality and other stuff using off-chain commitments on rollups (both ZK and optimistic).


      ![image](https://cdn.substack.com/icons/substack/favicon.ico)
      [noma.substack.com](https://noma.substack.com/p/off-chain-commitments-in-rollups)




###

A ZK rollup or optimistic rollup has an operator who batches transactions and publishes them to L1. MEV (technically, operator-extractible value) exists because the operator has the ability to change the order in which those transactions are...

## Replies

**Nickoshi** (2021-04-15):

This is a very brilliant idea!

But I think this can’t completely remove MEV on L2.

Here’s the thing: If the operator commits to include Alice’s transaction in X blocks with an order of O(K), where O(K) states that Alice’s transaction is in order #150. Then this won’t guarantee the operator can’t conduct a sandwich attack on Alice’s transaction because for each block, the operator can choose whether to confirm the ordered rollup immediately by adjusting the gas fee higher, or to postpone them to the next block as long as within X blocks.

If Alice submits a transaction on L2 to swap 10 ETH to DAI on Uniswap v2, the operator can use another address to submit two parts of a sandwich attack. When the first part of the sandwich attack is confirmed, the operator increases the rollup confirmation gas and the second sandwich transaction gas higher to ensure they can be quickly confirmed and the 2nd sandwich bread tx is behind Alice’s transaction. In this way, Alice’s transaction’s MEV is maximized and extracted.

Another concern is: the operator can cheat on the L2 transaction order. It’s hard to generate a random number to decide Alice’s transaction order. Then the operator can use the same MEV strategy to pre-allocate Alice’s order #.

As a summary: off-chain commitments for rollups can not remove MEV opportunities if X>1.

However, off-chain commitments can prevent operators from actively attacking Alice’s transactions. In this way, operators can only set up “MEV traps” in advance and wait for Alice or Bob to submit transactions.

I don’t know whether I made myself clear. Please let me know if I am wrong.

---

**samueldashadrach** (2021-04-18):

Okay so the way it’ll work is:

User 1 submits tx 1 with some fees. Operator guarantees user 1 that this tx is tx 1

User 2 submits tx 2 with some fees. Operator guarantees user 2 that tx 1 and tx 2 are first two txs.

User 3 … guarantees that tx 1, tx2, tx 3 are first three txs.

The operator can still insert transactions - but atleast at the time of commitment you get a guarantee as to what is going to happen. Better user experience, and it’ll be transparent if the operator is sandwiching you.

---

**Nickoshi** (2021-04-19):

Yeah make sense now

thanks!

---

**ethgcm** (2021-04-19):

If you submit the Tx first prior to getting the operators commitment, you cannot be sure the operator did not include a transaction prior to your tx.  What may benefit instead from a commit reveal scheme;

You can breakdown the epoch into the 2 phases (commit and reveal):

1 operator bases sequencing based on user n batched submitted hash(txn) then publishes a commitment.  Operator signs the root hash thus enabling a bond against reordering

2, users reveal their  tx

of course you would further have to consider per user sequencing via nonce etc.  This can be processed with batchSize = 1 for the same workflow described above

---

**samueldashadrach** (2021-04-19):

True, this works better ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**pmcgoohan** (2021-04-21):

Nice idea [@samueldashadrach](/u/samueldashadrach) and nice refinement [@ethgcm](/u/ethgcm). It’s simple and clean and a lot better than the total miner/validator/operator dominance that the MEV-Is-Inevitable crowd seem inexplicably happy with.

The weakness as it stands is that it incentivizes withholding.

User withholds their reveal:

- this gives them an advantage as the user can effectively cancel their transaction after it has been committed if conditions go against them
- withholding in this way also delays the operator, so you are incentivizing users to delay the system

Operator withholds accepting a reveal:

- you cannot prove cryptographically that they have done this. Perhaps it was a dropped connection beyond their control etc…
- this allows the operator to censor any transaction they don’t like once they have seen it

I designed the [Alex protocol](https://github.com/pmcgoohan/targeting-zero-mev/blob/00b51b08001446a76204ad6c05e1481dd14c3ca3/content-layer.md#withholding) to have zero incentives to withhold for every participant.

My suspicion is that once you’ve plugged all the leaks with withholding/incentives you’ll end up with something that looks like Alex, at which point you won’t need the encryption.

Encrypted txns are still useful for dark forest attacks though (which Alex does not address), so I think it’s worth pursing these ideas.

---

**samueldashadrach** (2021-04-21):

Alex Protocol seems a lot like having consensus over the mempool. How do you prevent getting DDOSed?

---

**pmcgoohan** (2021-04-21):

Nicely put! That is **exactly** what Alex is.

DDOS is avoided the same way as with the mempool itself. If a message is not valid it is not relayed by the network…

Roles are allocated by the scheduler on L1 for each content chunk so every node knows which nodes are meant to be sending messages and which aren’t. If you send a message that you are not scheduled to send, everyone skips it. It’s not even worth slashing, it’s just ignored.

---

**samueldashadrach** (2021-04-21):

You can DDOS using valid transactions too, as long as the pay zero gas.

---

**pmcgoohan** (2021-04-21):

I don’t see that it’s any more of a problem for Alex than for the mempool itself.

It is at each picker’s discretion which txs to include. Honest ones will try to include all the txs they can see, but if there are 100000 from a single address the standard picker logic can be set to only include say 1 (or none) of them. They can also filter out txs with zero gas.

There will also be a global chunk size limit so no single chunk can overload the system, although this will be set high to maintain good throughput.

Does that solve it, or is it something else your’re thinking of?

---

**samueldashadrach** (2021-04-21):

Restricting based on address doesn’t work cause anyone can create more addresses. Filtering zero gas doesn’t work cause you can send one gwei then.

Pickers need to have an incentive to only pick the transactions with highest gasprices. What are the incentives for pickers or shufflers to operate?

---

**pmcgoohan** (2021-04-21):

Got it! Yes you’re quite right…

As long as you reward pickers/shufflers/etc based on the total gas price of the chunk they contribute to then they are aligned with the miner/validator/sequencer rewards and DDOS is mitigated, right?

Obviously there will need to be an efficient way of doing this.

---

**samueldashadrach** (2021-04-21):

Should work ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

There might still exist probablistic frontrunning opportunities. There may exist transactions that you can insert that generate high profit if in the right order and only pay gas if in the wrong order. The more profit on the table, the more of your own transactions you can insert to increase odds of success.

Also what about *anyone can access* MEV such as DeFi hacks? I’ll submit the transaction as if I was the hacker not the other person.

---

**pmcgoohan** (2021-04-21):

Good! Let’s celebrate… [96% of MEV is DEX arbitrage](https://explore.flashbots.net/) and we’ve just dealt with that at a minimum.

I am considering other order manipulations at the moment and may have some more on this soon.

![](https://ethresear.ch/user_avatar/ethresear.ch/samueldashadrach/48/6197_2.png) samueldashadrach:

> the more of your own transactions you can insert to increase odds of success

One thing to say here is that unlike with miners you are no longer alone as a picker in being able to add txs. If adding multiple txs is +ev for you, it is also +ev for the other pickers. In this case, the efficacy of your txs is diluted by the other pickers but with the same fixed gas cost.

---

**samueldashadrach** (2021-04-21):

i thoughts pickers rotate in a schedule. how are pickers picked?

---

**pmcgoohan** (2021-04-21):

Yes they are, and it’s cheap to rotate pickers as they have no preparatory work to do. The scheduler selects random sets of them, one set for each chunk, many chunks in a block. Picker lists are ORed together.

So if you have say 4 pickers in a chunk, they at least have to battle each other now for the statistical frontrun and they only get do to it for perhaps 1/12 of a block. I don’t see a huge opportunity for a MEV auction around this.

Honestly though, total miner control of transaction inclusion/ordering as it stands now is the *literal worst case* of block content fairness and this beats it hands down.

I just cannot understand how so many intelligent people are talking about that 96+% of MEV like it’s a law of nature and not a bug.

---

**swampstream** (2022-05-19):

How is this unfolding. Update might be nice. Or have we gone another route.

