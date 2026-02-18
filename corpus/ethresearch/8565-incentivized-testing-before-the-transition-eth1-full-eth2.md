---
source: ethresearch
topic_id: 8565
title: Incentivized testing before the transition eth1 -> full eth2
author: greg7mdp
date: "2021-01-23"
category: The Merge
tags: []
url: https://ethresear.ch/t/incentivized-testing-before-the-transition-eth1-full-eth2/8565
views: 1459
likes: 0
posts_count: 8
---

# Incentivized testing before the transition eth1 -> full eth2

Currently, the beacon chain is just a testnet, since it doesn’t affect the data stored in the eth1 chain, and any exploit, possibly affecting validator balances, can be reversed without serious consequences. As a result, I believe it is not aggressively targeted by bad actors, and the fact that it is running smoothly may provide a sense a false confidence.

However, at one point we will need to migrate the eth1 state into the POS beacon chain, and any exploit after this would be catastrophic.

I think that, once this transition is ready to be activated, it would be advantageous to have a test period where both the POW eth1 chain and the POS eth2 chain would run simultaneously, processing the same transactions, with the expectation that they would finalize to the same state (if maybe not at the exact same time).

If we assume that the ETH1 chain is secure and bug free, any exploit in the ETH2 chain would allow a transaction to create a different finalized state in the eth2 chain when compared to the eth1 chain.

We could establish a testing period of maybe 1 month, where a reward of say 1000 eth would be granted to anyone who can find an exploit allowing to change the eth2 chain finalized data to a state different from the eth1 data produced with the same transactions.

Possibly, every time an exploit is found, it would be patched and the eth2 chain resynchronized with the eth1 chain, and then the testing period would reset to 1 month, and the reward amount multiplied by 1.5.

This would provide a strong incentive for people to stress-test the eth2 chain before it is live.  I think this testing period is necessary to stress-test the consensus layer, in a mode where finding an exploit would provide a significant material reward.

PS: my knowledge of Ethereum is very rudimentary, so apologies if this is not expressed well, I just wanted to share this idea.

## Replies

**mkalinin** (2021-01-25):

Thanks for posting the idea. The problem is that if two networks run simultaneously even with the same transaction set their state will diverge due to various factors, like latency, differences in block production between PoW and PoS and many others, making the comparison infeasible.

---

**greg7mdp** (2021-01-25):

Thanks for the answer! Sure, I understand that the transactions would be packaged in blocks differently, but shouldn’t at least the wallet balances be exactly the same. That could be a good comparison point.

---

**greg7mdp** (2021-01-25):

OK, I think I understand. Because of the difference in timing of transaction inclusions in blocks, there is no way to take matching snapshots of the two different networks, and reconciling differences would be very difficult.

---

**mkalinin** (2021-01-25):

If the same set of transactions is applied in another order it may result in another state root because of transactions that are dependent on each other, i.e. modifying and reading the same slots of the state.

---

**greg7mdp** (2021-01-26):

> If the same set of transactions is applied in another order it may result in another state root because of transactions that are dependent on each other, i.e. modifying and reading the same slots of the state.

Really? This seems like a problem. Couldn’t then switching to the new consensus mechanism cause timing differences, which may cause subtle behavior differences in dapps?

---

**mkalinin** (2021-01-26):

The problem is not in consensus switch but in running two chains with different characteristics in parallel. One of these chains is treated as canonical and user transactions will be submitted upon updates of the canonical chain. Since blocks may carry different sets of transactions it may result in different state roots at the same height and affect transactions submitted after. And it will definitely happen at some (not that far from common ancestor) point.

---

**Rafael1306** (2021-01-27):

Great ideia. I agree with you.

