---
source: ethresearch
topic_id: 3294
title: Data Availability Solution for Plasma EVM without Confirmation
author: Dapploper
date: "2018-09-10"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/data-availability-solution-for-plasma-evm-without-confirmation/3294
views: 6202
likes: 8
posts_count: 16
---

# Data Availability Solution for Plasma EVM without Confirmation

This is **a solution for Data availability problem** of [Plasma EVM](https://ethresear.ch/t/plasma-evm-state-enforceable-construction/3025) designed by **Onther Inc.** And I believe this can solve most of the problems. I’m looking forward to get lots of feedback from you.

*This is very simplified version. I highly recommend to read this full version.*

[A proposal for Data availability Solution of Plasma EVM](https://hackmd.io/s/ByeGtM5D7)

[(Korean)A proposal for Data availability Solution of Plasma EVM](https://hackmd.io/s/H1bk0Z-DQ)

## Abstract

This article proposes a model to address the most problematic Data Availability (DA) in [Plasma EVM](https://hackmd.io/m8TXSv2eSkGwsj7ni27Mag?both). This model has a new **‘User Request Block’**, which is a way for ensuring vaild Exit for users in case of data withholding, while leaving the judgment on DA entirely to the individual user. It also introduces a **dynamic fee model** to prevent infinite loop attacks by malicious users pretending to behave as if there were DA problems.

## New Exit model : User Request Block

### Glossary

**Non-Request Block(NRB)**  : Same as nonRequestBlock in Plasma EVM

**User Request Block(URB)**  : Request Block submitted by a user. Unlike the existing Request Block, it contains only transactions that reflect the Exit Request for URB of submitter or other user.

**Operator Request Block(ORB)**  : Request Block submitted by the Operator. It is same as the requestBlock in Plasma EVM.

**Exit Request for ORB(ERO)**  : Exit Request using ORB

**Exit Request for URB(ERU)**  : Exit Request using URB

**Rebase**  : If the URB is submitted based on the most recent finalized block, all child blocks that are submitted but not finalized will be located behind the corresponding URB and transactions that conflict with the URB will be reverted. This is called a  **Rebase** .

Confirmation does not exist anymore in the new model. In addition, whether DA problem occurs or not, is not judged at all in the process of mining and submitting the block. Instead, users who noticed that there was DA problem in child chain can safely exit by committing an URB based on the most recent defined block including their own and other user’s ERUs. Once the URB is committed, then the operator should **Rebase** the unfinalized blocks to reflect the contents of the URB. If it is judged that there are no problems with the user’s perspective, users can wait until the operator includes one’s Exit request, using ERO instead of ERU like the previous model.

(If you want to fully understand the **Rebase**, please check [this](https://hackmd.io/s/ByeGtM5D7#New-Exit-model--User-Request-Block).)

## Fee model against Infinite loop attack

### Infinite loop attack

The new model left the judgment of ‘block withholding’ to the individual users, and in case of a problem, URB can be submitted for safe Exit at any time. However, there is a fatal vulnerability issue in this model. It is a kind of **infinite loop attack using Rebase**.

### Fee model

We have introduced a model to charge fees for URB and ERU to prevent such attacks.

The design objectives of the fee model are as follows.

**1. If the submission of URB is close to the probability that it is an attack by malicious users, the fee should be charged high. And if it is close to the probability that it is an escape from a problem, the fee should be set low.

2. The number of URB commits that generate Rebase should be as low as possible.**

### DA probability

If an independent individual makes one’s own judgment on DA matters, it is the individual’s judgment that is most relevant to the probability of DA problems. That is, the greater the number of users who believe that there is the DA problem, the greater the likelihood of DA occurrence. On the contrary, if there are fewer users who believe there is DA problem, chances are high that there were no problems with the Child Chain. Therefore, we will design a model that estimates the probability of a DA issue and adjusts the fees for the URB and ERU accordingly through user’s judgments about DA problems, i.e.  **the number of ERUs** .

### Cost function

To satisfy the first principle, the higher the number of ERUs in the URB, the lower the URB’s submission costs and the cost of the ERB. In addition, to meet the second principle, it would be desirable to increase the extent of the decreasing cost as the number of ERUs increases.

**C_{URB} : Cost for submitting URB

C_{ERU} : Cost for Exit by ERU

N_{ERU} : The number of ERUs in URB**

As defined above, a cost function meeting the above conditions may be like below.

**Cost of submitting the URB**

[![](https://ethresear.ch/uploads/default/original/2X/0/0380b130db28bfe1a0ecb02dc76f1f0df61dedd5.png)360×297 4.52 KB](https://ethresear.ch/uploads/default/0380b130db28bfe1a0ecb02dc76f1f0df61dedd5)

**Cost of ERU**

[![](https://ethresear.ch/uploads/default/original/2X/c/c80ebf4a243fa1d7bf121f183590a21b66b24013.png)360×287 2.1 KB](https://ethresear.ch/uploads/default/c80ebf4a243fa1d7bf121f183590a21b66b24013)

## Replies

**kfichter** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> Once the URB is committed, then the operator should Rebase the unfinalized blocks to reflect the contents of the URB

What happens if the URB is withheld by the user or is invalid?

---

**Dapploper** (2018-09-15):

First, the URB cannot be withheld. Because the URB will be submitted based on most recently finalized block. And we all know what that is. That means everyone has the pre-state of URB. Also, we can know all transactions included in the URB as well. Since those transactions are based on ERUs submitted on root chain contract.

Second, the URB could be invalid by a malicious user. That is why we need the challenge period for the URB as well. And during this period, anyone can easily challenge it since the URB is not withheld.

Thank you for the good question [@kfichter](/u/kfichter).

---

**kfichter** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> Since those transactions are based on ERUs submitted on root chain contract.

Can these ERUs be challenged as well?

---

**Dapploper** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png)
    [Data Availability Solution for Plasma EVM without Confirmation](https://ethresear.ch/t/data-availability-solution-for-plasma-evm-without-confirmation/3294/4) [Plasma](/c/layer-2/plasma/7)



> Can these ERUs be challenged as well?

We don’t need to have challenge system for ERUs. Because they are reverted in the process of applying transaction in the URB.

---

**kfichter** (2018-09-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> Unlike the existing Request Block, it contains only transactions that reflect the Exit Request for URB of submitter or other user.

Does every user need to submit their own URB if there’s data availability?

---

**Dapploper** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png)
    [Data Availability Solution for Plasma EVM without Confirmation](https://ethresear.ch/t/data-availability-solution-for-plasma-evm-without-confirmation/3294/6) [Plasma](/c/layer-2/plasma/7)



> Does every user need to submit their own URB if there’s data availability?

No. they can do, but don’t need to do. If there is DA problem, many users would submit ERU(Exit Request for URB) on root chain contract. Only a few of users would submit URB including these ERUs. And It is very important to handle users’ Exit with minimum number of URBs as it could be DOS attack against the plasma chain. That’s why we set the cost functions of URB and ERU like in the article.

---

**kfichter** (2018-09-18):

Thanks for taking the time to answer my questions, much appreciated.

![](https://ethresear.ch/user_avatar/ethresear.ch/dapploper/48/2003_2.png) Dapploper:

> If there is DA problem, many users would submit ERU(Exit Request for URB) on root chain contract. Only a few of users would submit URB including these ERUs.

So if I understand correctly, users submit ERUs and other users submit URBs that include these ERUs. This has the effect of moving the transactions “back in time” to before the “bad” (withheld) block (?).

---

**Dapploper** (2018-09-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png)
    [Data Availability Solution for Plasma EVM without Confirmation](https://ethresear.ch/t/data-availability-solution-for-plasma-evm-without-confirmation/3294/8) [Plasma](/c/layer-2/plasma/7)



> Thanks for taking the time to answer my questions, much appreciated.
>
> So if I understand correctly, users submit ERUs and other users submit URBs that include these ERUs. This has the effect of moving the transactions “back in time” to before the “bad” (withheld) block (?).

Right. Users can make a fork to change canonical chain whenever they think that some blocks are withheld by the operator.

Thanks for your interest. What do you think about this model? Any opinion would be appreciated.

---

**keroro520** (2019-01-15):

> The second problem is that the Confirmation model has serious flaws that cannot solve the DA problem. This is because receive Confirm from only the users who send the transactions contained in the block, not the entire user. That is, users who do not send transactions are omitted during Confirmation process, so even if the operator withholds Block data, there is no way to defend it. For example, the Child Chain has Operator O, User A, and User B. Currently, Child Block #1 contains only transactions sent by user A. A and O conspire to create an invalid block #1 and submit it to the root chain. All it takes to do this is Confirm signature of A. Thus, in this process, B has no means of defending against the DA. The existing model did not guarantee the safety of user’s assets because of these problems.

I have read this post [A proposal for Data availability Solution of Plasma EVM](https://hackmd.io/s/ByeGtM5D7). I am confused about the 2nd problem about double confirmation upon. If B cannot access the new block, which caused by withholding by O, he has the choice to exit. And exit mechanism would protect B’s assert to safely exit.

So I don’t understand the problem description. Would you please provide more detail ? Thanks ~

---

**fahree** (2019-01-15):

Are the "URB"s fully published on-chain? If so, the solution is still limited as far as scaling goes to only as many transactions as can be fully published on-chain.

If not, then what if there’s a data availability problem with the contents of the URB?

---

**Dapploper** (2019-01-17):

Originally, we proposed confirmation scheme to handle data availability problem like this: the block is confirmed(or finalized) if all transaction senders confirm it (and this is done by CAS construction). But it is not only inefficient itself, but also cannot protect non-sender of that block. In the example above, User B cannot safely exit because already the invalid block#1 was withheld by the operator and finalized(note that it only needs User A)

See also this: [Plasma EVM 2.0: state-enforceable construction](https://ethresear.ch/t/plasma-evm-2-0-state-enforceable-construction/3025/2)

---

**Dapploper** (2019-01-17):

No, URB is not fully published on-chain. Although, it cannot be withheld by the operator because of its construction.

pre-state of URB: last finalized block (it is already known to all users)

transactions of URB: exit requests for URB (they are all listed on root chain contract, and it means that they are all known too!)

Now you have pre-state(parent block) of specific block and all transactions to be included on that block, you can easily know the post-state of that block(e.g correct stateRoot). This is the reason why the URB cannot be withheld.

---

**fahree** (2019-01-17):

If the URB isn’t published on-chain, can’t the operator manufacture a withheld URB to exit with all the money?

---

**Dapploper** (2019-01-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> If the URB isn’t published on-chain, can’t the operator manufacture a withheld URB to exit with all the money?

More precisely, the URB is published on-chain like other types of block(e.g NRB, ORB), but it’s not fully published  because it’s required to submit only 3 roots: stateRoot, transactionRoot, receiptRoot. Actually, there’s no need to publish transactions included on the URB, since we already had it on root chain contract. All transactions included in request block(ORB, URB) should be ‘requested’ first by the users calling `startEnter`, `startExit`, `makeERU`.

You can see the source code here: [plasma-evm-contracts/contracts/RootChain.sol at c8ce194768afbdecbf53c1d8d6fe13dec18710ae · tokamak-network/plasma-evm-contracts · GitHub](https://github.com/Onther-Tech/plasma-evm-contracts/blob/c8ce194768afbdecbf53c1d8d6fe13dec18710ae/contracts/RootChain.sol)

---

**philosopher** (2019-01-23):

newly written [Plasma EVM 2.1 Paper](https://hackmd.io/s/ryD9NXkXE) published.

User-activated Fork paper is fully merged into this paper

It includes,

- Various cases in submitting URB is added
- Challenge case for URB is added
- Minimum point of cost functions for URB, ERU is modified
- Issues related with UAF model are added

