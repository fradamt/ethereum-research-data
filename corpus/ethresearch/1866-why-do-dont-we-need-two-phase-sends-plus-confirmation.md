---
source: ethresearch
topic_id: 1866
title: Why do/don't we need two phase sends plus confirmation
author: JChoy
date: "2018-04-29"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/why-do-dont-we-need-two-phase-sends-plus-confirmation/1866
views: 4174
likes: 9
posts_count: 17
---

# Why do/don't we need two phase sends plus confirmation

Hi ethresear.chers! These days, I’m reading Plasma and Plasma Cash. I saw the transaction on Plasma chain is complicating. Let’s assume a transaction A->B. Correct me if I’m wrong.

On Plasma, the process should be:

- A makes transaction and send to operator.
- Operator makes a block including above transaction and update on parent chain.
- A is waiting for the information to be included in Root chain
- After that, A signs and sends to B
- B signs and the transaction is confirmed

I’m wondering why A should sign and send it to B. I think B could use the tokens(utxos in MVP) without extra signing after he/she checks that Rootchain contains the information about the transaction similar to Ethereum/Bitcoin transaction process.

On Plasma Cash, Karl said that

> Transactions no longer require a two phase send plus confirmation. Instead, once a transaction is included on the main chain it can be spent.

I don’t know why these two have different confirmation process.

## Replies

**vbuterin** (2018-04-29):

Plasma Cash makes up for it by having a withdrawal process where you need to specify the last two transactions in a coin’s history in order to exit it. This withdrawal process leans heavily on the fact that in Plasma Cash every coin is a separate unit and they are not fungible with each other; for example, one of the challenging procedures is that a challenger can challenger with an older UTXO of the same coin, and the responder would be required to provide the child, and the child cannot be after the coin exited. In Plasma, however, there is no such thing as “the same coin”, so you can’t use this technique.

---

**JChoy** (2018-04-29):

Thanks for replying. It is clear to do withdrawal process.

But I still don’t understand why receiver needs to sign on Plasma.

In transaction A->B in same chain, when after B sees that transaction is on Root chain, why B has to sign?

- A makes Tx that A sends 1PETH to B
- B waits for confirmation (waits for the transaction to be on Root chain)
- after that, B just uses it whenever he wants

I think above process is sufficient on Plasma(not Plasma Cash), too.

---

**vbuterin** (2018-04-29):

The problem is, what if the Plasma chain attacks while A->B is inflight? Then, the Plasma chain could include a series of fake withdraws between A and B, and A cannot withdraw because B exists, but B also cannot withdraw because it’s lower priority than all the fake outputs. In Plasma Cash this problem does not exist because of how each coin is separate from all the other coins.

---

**JChoy** (2018-04-29):

Please correct me if I’m wrong.

So, in Plasma, if we allow the transaction valid after 2 phase+confirmation process, A can withdraw when Plasma chain attacks while A->B is inflight.

In Plasma Cash, above process is not required because the tokens are separated. Then also, we don’t have to consider priority, just consider history of tokens.

---

**vbuterin** (2018-04-29):

Not A can withdraw, the Plasma chain operator can steal coins for themselves if they start issuing invalid blocks while A->B is inflight.

> In Plasma Cash, above process is not required because the tokens are separated. Then also, we don’t have to consider priority, just consider history of tokens.

Yes.

---

**JChoy** (2018-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Not A can withdraw

Oh, so 2 phase sends + confirmation process can’t solve the attacks during inflight. Then question still remains. Why was this process necessary on Plasma, not Plasma Cash?

Plus, I want to make the defination of “inflight” certain. Does this mean A->B tx is going up to Rootchain?

And Good morning ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**huangyg11** (2018-04-30):

I don’t read the plasma spec yet, but I can share my understanding to the plasma spec.

In plasma, you deposit to the contract in the root chain. And the eth is you’s when you can exit it.

So when the withdraw function allow you to exit without the confirm sig, the operator can steal your money in the following way:

1) A want to send eth to B so A send tx to the operator

2) the operator withhold the tx and submit some invalid block to the root chain.

At this point:

1) A try to withdraw

2) the operator submit the tx and challenge A

3) challenge success and A is punished to double-spend

4) B try to withdraw

5) The operator also submit withdraw and he has high priority

---

**JChoy** (2018-04-30):

Alright,

![](https://ethresear.ch/user_avatar/ethresear.ch/huangyg11/48/1248_2.png) huangyg11:

> A try to withdraw
>
>
>
>
> the operator submit the tx and challenge A
>
>
>
>
> challenge success and A is punished to double-spend
>
>
>
>
> B try to withdraw
>
>
>
>
> The operator also submit withdraw and he has high priority

to solve that problem with 2-phase signs + confirmation, we have to set that A->B is not valid before they do 2-phase signs+confirmation. So then, A can withdraw because operator’s A->B tx is not yet confirmed by A and B. I think this is rational.

But, I wonder why this can’t be.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Not A can withdraw,

---

**danrobinson** (2018-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Plasma Cash makes up for it by having a withdrawal process where you need to specify the last two transactions in a coin’s history in order to exit it.

Why do you have to specify the last two transactions in a coin’s history in order to exit it? Can’t you just specify the latest transaction? It isn’t clear to me how revealing two transactions adds anything, since a malicious operator can create two new invalid transactions just as easily as they can create one. Seems to me that there are only two kinds of invalid exits: “spent coin” and “invalid history,” the latter of which includes any coins with double spends in their history. (I discussed this a little with [@karl](/u/karl).)

I think Plasma Cash avoids the need for confirm signatures just because of the non-fungibility.

---

**ldct** (2018-05-01):

I’m still working through the details, but I think the two-transaction exit is needed to handle a case like this:

Blocks: 1, 2, 3, 4

Transactions (labelled by letters for reference):

a: 1 -> 2

b: 2 -> 4

c: 1 -> 3

a chronology that could lead up to this is: blocks 1 and 2 are comitted, and transaction a has been included. transaction b is in flight. then, the plasma operator becomes byzantine, and commits block 3 along with transaction c. then, it commits block 4 along with transaction b.

In this case, the rightful owner of the coin is the recipient of it in transaction b, however, this coin has “invalid history” by your definition, and determining that this is “not really invalid history” requires examining blocks 2 and 4

also I might have understood it wrongly but your definition of “invalid history” might declare as invalid all coins in the following scenario. it depends on the definition of “double-spend in a history”.

Blocks: 1, 2, 3

Transactions:

1 -> 2

1 -> 3

---

**kfichter** (2018-05-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> I think Plasma Cash avoids the need for confirm signatures just because of the non-fungibility.

I’m still not sure that this entirely avoids the need for confirmation signatures. We could still potentially have the case where Alice sends a coin to Bob, tx is included in block N, N is withheld. The coin can’t be stolen by the operator w/ invalid txs placed “in front” of Alice’s tx (as per MVP), but Alice and Bob still don’t know if the tx was included or not.

I guess Alice could attempt to exit from the old tx and be challenged by the operator, but that doesn’t seem satisfying. The other solution is probably “limbo exits” (concept via Piotr Dobaczewski) where Alice effectively completes the transaction as a special type of exit on-chain.

So confs aren’t required for security per se, but they might still have some use.

---

**danrobinson** (2018-05-02):

Yes, not having a confirm signature does allow the chain operator to modestly grief users (and collect bounties from them) by forcing them to make an invalid withdrawal attempt. This is a reason to make the bounty on unsuccessful attempted exits relatively modest (particularly when the challenge is a “spent coin” challenge rather than an “invalid history” challenge.)

But I think confirm signatures cause a more significant griefing issue, if you have multicoin transactions where two of the inputs are controlled by different parties, such as a trade of one token for another. Either party could withhold their confirm signature and force the other party to attempt an invalid withdrawal. So in this case *any* party would be able to successfully grief a counterparty, which seems worse than the alternative, where only the Plasma chain operator can grief users.

Is there a description of limbo exits? The fisherman’s dilemma here seems difficult to resolve.

---

**kfichter** (2018-05-02):

[@JChoy](/u/jchoy) Generally, there are two major reasons why it’s necessary to have the two-phase send + conf in Plasma.

The first reason is specific to Plasma MVP and arises because Plasma MVP allows for fungible coins/tokens. Basically, if we don’t have confirmations, then an operator can place a user’s valid transactions *after* the operator’s invalid transactions in a block. This is a problem because exits in Plasma MVP are processed in time order. I published a brief write-up on why this time-order processing is necessary [here](https://github.com/omisego/research/blob/master/plasma/plasma-mvp/explore/priority.md).

Let’s illustrate this first problem with a scenario where the operator steals funds. Assume the contract only holds 10 ETH in total.

1. Alice broadcasts a transaction spending 10 ETH to Bob.
2. The operator creates an invalid transaction creating 10 ETH for themselves “out of nowhere” and places it at the first index in a block (“transaction #0”).
3. The operator places Alice’s transaction at the second index in the block (“transaction #1”).
4. The operator publishes this block.
5. Bob sees the invalid transaction and submits his exit.
6. The operator submits an exit for the invalid transaction.
7. The operator’s exit processes before Bob’s exit, so the contract is now empty.
8. Bob’s exit cannot be processed because the contract has no funds remaining.

Now, let’s see what happens when we require confirmations:

1. Alice broadcasts a transaction spending 10 ETH to Bob.
2. The operator creates an invalid transaction creating 10 ETH for themselves “out of nowhere” and places it at the first index in a block (“transaction #0”).
3. The operator places Alice’s transaction at the second index in the block (“transaction #1”).
4. The operator publishes this block.
5. Alice sees the invalid transaction and refuses to sign a confirmation on her transaction to Bob.
6. The operator submits an exit for the invalid transaction.
7. Alice exits from her (still technically unspent) 10 ETH UTXO which existed before the operator’s invalid UTXO.
8. The operator’s exit cannot be processed because the contract has no funds remaining.

Note that this situation is *not* a problem in Plasma Cash because coins are unique and non-fungible - the operator can’t just create valid UTXOs “out of nowhere” like they can in Plasma MVP. The operator could create a transaction that appears to give them ownership of a specific coin, but that doesn’t impact the ability for the owners of any other coin to exit.

Now let’s talk about the other potential scenario. This is basically what I mentioned in my reply to Dan above, and it’s less of an attack vector than an annoyance:

1. Alice broadcasts a transaction spending 10 ETH to Bob.
2. The operator places Alice’s transaction somewhere in the block.
3. The operator publishes the root of this block to the root chain but withholds the actual block information.
4. Alice doesn’t know if her transaction to Bob was actually included in the block or not. Bob doesn’t have enough information to exit because he doesn’t know the index of the transaction in the block.
5. Alice must attempt to exit from her old UTXO.
6. The operator knows that Alice’s old UTXO is spent, so they challenge Alice’s exit with her transaction to Bob (revealing the index).
7. Bob now knows the transaction index, so Bob can exit.

This doesn’t change anything security-wise, but it’s not particularly convenient to have this exit-challenge-exit process. Additionally, Alice will always lose her bond for her original exit. Here’s how it plays out with confirmations:

1. Alice broadcasts a transaction spending 10 ETH to Bob.
2. The operator places Alice’s transaction somewhere in the block.
3. The operator publishes the root of this block to the root chain but withholds the actual block information.
4. Alice doesn’t know if her transaction to Bob was actually included in the block or not. Alice doesn’t broadcast a confirmation signature.
5. Alice exits from her old UTXO.
6. The operator cannot challenge with Alice’s spend to Bob because the operator doesn’t have the required confirmation signature.

I hope that makes sense. Please let me know if I can clarify anything and I’ll try to make edits!

---

**kfichter** (2018-05-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> Is there a description of limbo exits

Sure thing.

The original quick sketch was:

- limbo_exit alternative to exit.
- Alice => Bob, funds are stuck in “limbo” (as per described scenario above).
- Alice calls limbo_exit by sending normal exit info + her potentially included tx to Bob. Gives Bob N days to exit, Bob must be the one to place bond.
- If Bob doesn’t exit within N days, then Alice is entitled to the exit and can’t have her exit blocked via her tx to Bob.
- In either case, exit has priority of Alice’s original UTXO.

I think there are some improvements to be made. Namely, it’s iffy for me to allow the Alice to initiate limbo exit (some grieving opportunities here). Might be better if Bob has to initiate the limbo exit along with a signature to Alice or vice versa (meaning Bob could also permit Alice to exit, “nullifying” the later tx). This is also nice because it means the giving party doesn’t need to spend gas to initiate the limbo exit.

If both parties are cooperating, this is fine. If both parties are not cooperating, then limbo exits aren’t really the correct choice anyway (why would Alice allow Bob to take the exit if they aren’t cooperating? Alice would probably just attempt to exit and hope that the tx was not included, maybe figure out an external solution if Bob receives the exit).

Let me know if you can pick out any issues with this, I think it’s a pretty cool construction but I haven’t spent enough time thinking about it.

---

**danrobinson** (2018-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> I think there are some improvements to be made.

This is a cool idea but I don’t quite see the whole picture. If you’re a malicious exiter spending an old (spent) coin, you could always call `limbo_exit` rather than `exit`, couldn’t you? That would allow you to avoid ever posting a bond.

What if you had a `manual_transfer` method on the parent contract instead? Alice could call this with respect to her coin A and transaction B, and post a bounty. This would initiate the following process:

1. for X days, anyone would be able to challenge and claim Alice’s bounty by revealing a spend of coin A that is not transaction B,
2. after that point, if nobody has challenged, transaction B is considered confirmed, as if it was included in the same block as block A. Bob can initiate an exit, initiate a challenge, or respond to a challenge by revealing his transaction B, despite not having a proof of that transaction’s inclusion in the Plasma Cash chain. (If transaction B actually WAS included in the chain, and someone has proof, they can still use that instead; there’s no conflict between the tx B confirmed on the main chain and the one confirmed on the Plasma chain.)

---

**JChoy** (2018-05-03):

Thanks for super nice Explanation!! ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9)

