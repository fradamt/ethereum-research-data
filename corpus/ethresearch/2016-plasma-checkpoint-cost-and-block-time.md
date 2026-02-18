---
source: ethresearch
topic_id: 2016
title: Plasma checkpoint cost and block time
author: jdkanani
date: "2018-05-16"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-checkpoint-cost-and-block-time/2016
views: 4471
likes: 3
posts_count: 5
---

# Plasma checkpoint cost and block time

**Problem**

Plasma Cash (or XT/MVP) pushes every block root/SMT root to Root chain. As per current average Ethereum block time, one could use minimum block time, say around 15 seconds - not less than that. Block time can go up but the user experience will take a hit. Less than 30 seconds block time introduces the cost and time in terms of ETH fees and ETH block confirmations. In near future, with multiple plasma chains, most of Ethereum transactions will be checkpoint transactions only.

**Alternative**

Small block-time, periodic checkpoints (e.g. Merkle root of recent 100 blocks) and bonded operator or PoS (credit goes to [@alex-miller-0](/u/alex-miller-0)). Idea is to have partial confirmation quickly and achieve finality using checkpoints. Plasma MVP may not work as it requires confirmations but David’s no-confirmation may work.

Two stages can be added while finalizing a checkpoint - propose and commit. Between these two stages, anyone can challenge double spend or invalid TX (or a TX state in state-based plasma) using direct fraud proofs or (bonded) interactive fraud proofs (similar to the third type from Plasma Cash). The proposed checkpoint will be reverted and the operator will be slashed if fraud-proofs are valid.

Block withholding - Operator/Stakers will be slashed if the new checkpoint is not created in a certain amount of time (say, 5 * checkpoint period).

Censorship - One can submit a transaction on root chain and if next 5 checkpoints don’t include the transaction, the operator gets slashed.

**Limitations**

- The time window between “propose” and “commit” stage must be long enough for challenges.
- Chain restart (reorgs) will be required in case of fraud or everyone must exit using the last checkpoint.
- Data availability will be the issue in Plasma Cash/XT while challenging the checkpoint.

Again, thanks [@alex-miller-0](/u/alex-miller-0), [@esteban](/u/esteban) , [@sg](/u/sg) for the ideas.

## Replies

**kfichter** (2018-05-16):

I’m glad people are looking at smaller block times! Agreed that 15-30s is too long for most things, especially if we can guarantee some sense of finality for smaller block times.

Generally it’s possible to have a block time < Ethereum block time, but it requires the operator to be bonded for a large value. Concept is that the operator circulates blocks before submitting to the root chain, can be slashed if someone can prove that the operator has signed two blocks for the same height (equivocated). This way we’re still bound by Ethereum finality, but we can have cryptoeconomic finality for smaller block times. The bond involved might be extremely large (depends on value being transacted in each block).

Figuring out smaller block times with a small bond or some other cryptoeconomic construction would be a great research topic.

Checkpoints work for MVP because we don’t change any assumptions (if checkpoint withheld, everyone must exit within 2 weeks). I think we’ll almost absolutely need checkpoints because the MVP dataset size is absolutely massive otherwise (10s of terabytes/yr). We need the XT construction for Cash because we never want to force a user to act unless they’ll receive a bond.

---

**jdkanani** (2018-05-17):

Agreed.

> The bond involved might be extremely large (depends on the value being transacted in each block).

That one way to do it.

Second is “challenging the checkpoint” - doable in Plasma MVP or account-based plasma. In that case, the challenger will get bonded amount if checkpoint withheld or in case of fraud. I am thinking more towards the implementation where users don’t have to worry about their tokens and sort of “transactions will eventually reach to finality in case of withheld or fraud” solution instead of mass exit.

> Concept is that the operator circulates blocks before submitting to the root chain, can be slashed if someone can prove that the operator has signed two blocks for the same height (equivocated).

Right. But, problem is that ETH fee increases when chain state (storage) keep increasing on Root chain and of course, traffic (minor but still) when multiple plasma chains will be there.

In case of checkpoint,  \frac 2 3  operators can sign the checkpoint and submit it to Root chain (similar to Tendermint). One can take  2 ^ n  blocks for checkpoints, where select  n  such a way that  2 ^ n \le b , where  b  is the number of blocks created from the last checkpoint.

> I think we’ll almost absolutely need checkpoints because the MVP dataset size is absolutely massive otherwise (10s of terabytes/yr)

Yes!

---

**kfichter** (2018-05-17):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/j/4bbf92/48.png) jdkanani:

> In that case, the challenger will get bonded amount if checkpoint withheld or in case of fraud

The difficult part here is to prove that the checkpoint is being withheld.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/j/4bbf92/48.png) jdkanani:

> Right. But, problem is that ETH fee increases when chain state (storage) keep increasing on Root chain and of course, traffic (minor but still) when multiple plasma chains will be there.

Yep, you’d only want to submit a single block that represents very many intermediate blocks.

---

**jdkanani** (2018-06-06):

> The difficult part here is to prove that the checkpoint is being withheld.

One way is to wait for the certain interval (e.g. 5 * normal checkpoint time)

