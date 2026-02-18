---
source: ethresearch
topic_id: 1968
title: Watchtowers may not work in Plasma (Cash)
author: danrobinson
date: "2018-05-10"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/watchtowers-may-not-work-in-plasma-cash/1968
views: 4192
likes: 9
posts_count: 9
---

# Watchtowers may not work in Plasma (Cash)

I recently realized that the kind of watchtowers supported in Lightning may not be fully possible in Plasma Cash. (I believe this is true of classic Plasma and Plasma MVP as well; this fact may be well-known in those contexts, so apologies if this is trivial).

Watchtowers are entities to which a user can outsource the task of watching the chain and challenging invalid attempted withdrawals.

While Plasma Cash would support watchtowers that challenge attempted withdrawals of *spent coins*—since, if the user is cooperating with them, they will be aware of subsequent state that invalidates the prior state—they cannot always challenge attempted withdrawals of *coins with invalid histories* (as can occur if a Plasma Cash chain operator is malicious). If they tried, a Plasma Cash chain operator and user could collaborate to defraud the watchtower (by withholding blocks to prevent the watchtower from determining whether the attempted withdrawal is valid or not).

Watchtowers can still ping users to notify them that there is an attempted withdrawal. However, this still requires the user to be online. Additionally, there is no way to prove that such a notification was or was not sent, so there is no way to punish the watchtower for misbehavior.

The best solution I can see would be to require the watchtower to effectively bear the risk of operator misbehavior, by promising to challenge any invalid withdrawals (and therefore relying on the Plasma Cash operator not to misbehave).

## Replies

**ldct** (2018-05-11):

The user could contract with the watchtower to challenge with specific coins. Then if the specific coins become invalid challenges, the watchtower doesn’t get penalized

---

**danrobinson** (2018-05-11):

You can’t update your on-chain contract with them every tx, though. Otherwise the Plasma chain gives you no scalability advantage. And I think it’s at least difficult, maybe impossible, to atomically update your off-chain watchtower contract with your plasma coin in a way that doesn’t give the watchtower any power over when and how you can spend.

---

**ldct** (2018-05-11):

Your contract with them should be in a state channel so there’s no onchain transaction to update it

---

**danrobinson** (2018-05-11):

The latency bounds on that state channel might cause a problem, though… right? What if the watchtower ceases to respond to me? Am I blocked from safely transacting on the Plasma Cash chain until I close that state channel?

That’s not necessarily that bad (it doesn’t let the watchtower do anything to me that the Plasma Cash chain operator can’t do already). And maybe you can set up the state channel so it isn’t a problem…

---

**ldct** (2018-05-12):

I’m actually not sure exactly how lightning watchtowers work…what recourse do users have if all watchtowers try their hardest not to interact with a user?

> Am I blocked from safely transacting on the Plasma Cash chain until I close that state channel?

It seems to me that it is always safe to transact, but if you can’t get access to watchtower-type services then it is no longer safe to log off (ie stop monitoring the chain for a period longer than the plasma dispute timeout). If you do need to log off, in the worst case you can withdraw your coins.

Here are two (very suboptimal) schemes that analyze the related question “am I blocked from safely logging off while keeping my coins on the plasma chain” in different ways. In both schemes, a plasma chain user opens state channels with multiple watchtower service providers (WSP), and for concreteness, exits do not put up any bond/deposit, and we use the leftmost unspent CFCR. Depending on how exit deposits are constructed other schemes are possible, but I will not discuss those.

**Scheme 1**: A user normally has no contract with any WSP, but right before logging off, he tries to enter a contract with every WSP. The contract specifies c, which is the coin the user claims is the latest coin. The WSP puts up a bond which can be returned after some specified amount of time. While the bond is in effect, however, the contract allows the user to claim the bond by showing that all the following happened:

1. a coin c' with was exited
2. c' and c have the same coin id
3. c' has a higher block number than c
4. the exit did not have a challenge from c

note that in the event that some attempted exit satisfying (1)-(3) happens, the WSP can keep his bond safe just be challenging it with c, even if that challenge fails. Call these contracts type 1 contracts.

**Scheme 2**: Same as scheme 1, but the user has an additional existing contract with the WSPs (set up long ago) that the WSP must enter type 1 contracts.

**Analysis**

In scheme 1, the user can log off without exiting if at least one WSP enters a contract. If all WSPs don’t enter into a contract, the user cannot do so.

In scheme 2, the user can log off without exiting if at least one WSP enters a contract. If all WSPs don’t enter into a contract, the user has to enforce his right to enter type 1 contracts on-chain, which requires paying transaction fees and waiting out the state channel timeout period.

---

**stonecoldpat** (2019-07-15):

Hi all,

I’ve had some thoughts around this (esp since we want to build and run a watching service for whenever it emerges).

OK. So when a customer is going to hire a watch tower, the job should only get accepted when the checkpoint is accepted in the blockchain and the “checkpoint data” is publicly available / verified by the watch tower. Essentially, only “limbo exits” should be accepted. In practice I imagine a two-step process:

- Customer notifies watch tower that a coin will be accepted into checkpoint
- When checkpoint is accepted + data available, watch tower will forward a signed receipt to customer (lets say via email).

Now the above guarantees that a watch tower can always respond with an exit challenge and the customer has some signed receipt to acknowledge watch tower is hired.

To the point of the post; the main issue is what happens if the operator cheats (lets say customer is offline, same scenario as customer colluding)?

- Operator posts a list of checkpoints and does not make the data available to the watch tower.
- In every checkpoint, there is some “fake transfer” with the coin in question. Lets say there are several fake transfers.
- Operator withdraws based on the checkpoint with the final fake withdrawal.

The watch tower can see the coin was transferred to the operator, but it looks like a legit withdrawal.

In the above scenario,  **the watch tower must always respond with an exit challenge.**

Why? The watchtower could not verify if the coin’s transfer history is well-formed/correct/legit since the checkpoint data is not publicly available. i.e. this is malicious behaviour.

This is potentially a FDoS (financial denial of service lol) for a watching service. To counter it:

- Customer should “pay up front” cost of executing an exit challenge (or we assume % fraud and price it in)
- All appointments should eventually expire (i.e. you hire PISA for 5 days for 5 cents).

Generally, I think for the most part, most customers are going to trust plasma operators (we see this already in lightning with bitrefil, eclaire, etc). I foresee a watching service being hired by the plasma operator (and not customers) to guarantee their customers are protected from each other. If a plasma operator lets a bad coin exit get accepted, they lose their reputation and potential future business. So they have a lot to lose, thus a watching service is “insurance” for them.

---

**adlerjohn** (2019-07-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/stonecoldpat/48/609_2.png) stonecoldpat:

> OK. So when a customer is going to hire a watch tower, the job should only get accepted when the checkpoint is accepted in the blockchain and the “checkpoint data” is publicly available / verified by the watch tower. Essentially, only “limbo exits” should be accepted.

I’m not really sure what you’re saying here. What’s a checkpoint? How is it related to a “limbo exit?” The nomenclature around Plasma has changed a bit over the past 6 months, so let’s make sure we’re all on the same page.

In Plasma you can make two kinds of challenges:

1. Non-interactive: exit is spending an old coin, for which you can prove you’re a newer owner.
2. Interactive: exit is spending a newer coin than the one you have. You ask for them to provide a valid signature for your coin being spent. This can be responded to or not.

A checkpoint in the current nomenclature is an “exit followed by an immediate deposit,” ([can be implemented quite efficiently](https://plasma.build/t/rollup-plasma-for-mass-exits-complex-disputes/90)) which has the effect of truncating coin history. In that sense, it’s no different than an exit in terms of the exit games that must be played.

Which of these cases can the watchtower watch for? I think only the first, non-interactive, exit case. If so, then there’s no problem. The problems only arise if you try to cover the second case.

![](https://ethresear.ch/user_avatar/ethresear.ch/stonecoldpat/48/609_2.png) stonecoldpat:

> (lets say customer is offline, same scenario as customer colluding)

Or, the operator *is* the customer.

![](https://ethresear.ch/user_avatar/ethresear.ch/stonecoldpat/48/609_2.png) stonecoldpat:

> This is potentially a FDoS (financial denial of service lol) for a watching service.

[I agree!](https://twitter.com/jadler0/status/1141555326136836097)

![](https://ethresear.ch/user_avatar/ethresear.ch/stonecoldpat/48/609_2.png) stonecoldpat:

> Customer should “pay up front” cost of executing an exit challenge (or we assume % fraud and price it in)

Now you’re trying to have watchtowers cover the second exit case (the interactive one). The problem with your suggestion here is that the exits can be *valid* but not immediately available to the watchtower. Now you have a FDoS attack on customers: the operator can make a bunch of checkpoints (all valid), forcing the watchtower, and therefore the customers, to pay for challenges that do nothing since the checkpoints are all valid.

I think if you restrict the watchtower to watching:

1. Non-interactive exits and checkpoints, and
2. Interactive exits for which the customer has paid the cost (which would require refilling sometimes?)

then you’re fine.

![](https://ethresear.ch/user_avatar/ethresear.ch/stonecoldpat/48/609_2.png) stonecoldpat:

> Generally, I think for the most part, most customers are going to trust plasma operators (we see this already in lightning with bitrefil, eclaire, etc).

Ehhh I don’t think following the fundamentally broken LN model and their user’s expectations is a good idea. If you want to go that route then you don’t even need Plasma, just use unqualified side chains.

---

**stonecoldpat** (2019-07-15):

> I’m not really sure what you’re saying here. What’s a checkpoint? How is it related to a “limbo exit?” The nomenclature around Plasma has changed a bit over the past 6 months, so let’s make sure we’re all on the same page.

I don’t know the official term people use. I call the checkpoint just the hash that is periodically posted to the blockchain. i.e. commitment to all transfers for a given period of time.

A limbo exit is just when the commitment (checkpoint) is posted to the blockchain and the receiver has verified the data is publicly available + includes their transaction. (perhaps I’m wrong? this is what I understood by the term). Main point I’m making here is that a watch tower shouldn’t accept a job unless it is 1. accepted into a commitment and can verify that and 2. confirm it isn’t a double-spend.

> Non-interactive: exit is spending an old coin, for which you can prove you’re a newer owner.
> Interactive: exit is spending a newer coin than the one you have. You ask for them to provide a valid signature for your coin being spent. This can be responded to or not.

OK it would be good to clear this up. Generally when a user is withdrawing their coin - there is “always a challenge period”. There are two type of responses a watch tower can make:

1. Non-interactive proof (already spent, double-spend): Watch tower can respond with proof a coin was double-spent or it was already spent. No need for any challenge period here. (Ideally this should shut down plasma service. To avoid countless challenges).
2. Interactive proof (invalid history): Watch tower thinks there is somethingy fishy, so it posts a challenge where the withdrawer of the coin must prove it was spent.

The non-interactive case is pretty straight forward. The withdrawer must say “I am spending coin x, and it was previously with Alice”. So the non-interactive proof should be sent in both cases.

The point of the above post by Dan was to talk about the invalid history case. i.e. what if the operator cheats, and they make it look like the coin really does belong to the new owner (because of the invalid history). Here, the watch tower should ALWAYS respond with an interactive proof (i.e. prove this coin was spent by Alice) - since it cannot independently verify the history - as the data is not available.

> Now you’re trying to have watchtowers cover the second exit case (the interactive one). The problem with your suggestion here is that the exits can be  valid  but not immediately available to the watchtower. Now you have a FDoS attack on customers: the operator can make a bunch of checkpoints (all valid), forcing the watchtower, and therefore the customers, to pay for challenges that do nothing since the checkpoints are all valid.

Yup. basically if the plasma operator doesn’t make data available (even if its valid), then a watch tower has no choice but to do it. Customers shouldn’t care, if the checkpoint is indeed valid - then there can never be an invalid withdrawal - and thus the customer doesn’t need to respond. (only care if they hired watch tower* lol)

