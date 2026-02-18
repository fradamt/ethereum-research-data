---
source: magicians
topic_id: 639
title: Child pays the Parent in Ethereum - Help Build this EIP!
author: GriffGreen
date: "2018-07-02"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/child-pays-the-parent-in-ethereum-help-build-this-eip/639
views: 4719
likes: 15
posts_count: 9
---

# Child pays the Parent in Ethereum - Help Build this EIP!

**Problem:**

The extreme fluctuations in Gas Price make it very hard for super users to send multiple transactions from the same account. Accounts get locked up when poor gas estimation causes a transaction’s gas price to be too low, and the transaction’s gas price and therefore transaction hash must change before more transactions can be made with that account (because of the nonce).

**Background:**

Improving gas estimation has been looked towards in the past to solve these issues. **This is not going to work** and actually exacerbates the issue because what super users do is just multiply the estimated gas price and by some factor (often 1.5) and then post it, paying extra gas unnecessarily. In [the past](https://twitter.com/thegrifft/status/951167619851145216) this has caused a runaway reaction and gas price has shot upward unnecessarily.

The fact is using the past to predict the future market on gas is not enough of a solution for the problem. As the use of Ethereum increases more and more often a random some smart contract is going to flood the network with transactions on some random block number and this strategy is in capable at mitigating this event (e.g. ICOs).

This of course is most impactful to exchanges processing withdrawals every second, this is horribly needed for them.

But let’s imagine a normal user, Yalor that sends Kris 1 ETH with a gas price of 4 Gwei. Yalor sends the etherscan transaction link to Kris and then checks back an hour later to find the transaction has been dropped completely from the tx pool because the gas price has gone up!

Right now Yalor needs to replace his transaction which then changes the tx hash, and the etherscan link… Kris in the mean time is confused and doesnt understand why the tx hash is changing, might even think Yalor is scamming.

**Solution!**

Bitcoin had a very similar problem, which was solved by: https://nulltx.com/what-is-child-pay-for-parent/

**Alexey Akhunov** of turbo Geth proposed we do something similar, where we allow clients to understand if an account has multiple transactions in the tx pool and the miners can average their Gwei when sorting transactions to include in the block.

In this solution, miners win, users win, and gas prices should be lower in general because super users can be more efficient in designing a technical solution for gas price fluctuations.

And in this scenario, for the average user, instead of Yalor needing to reach out to Kris and explain the intricate details of gas, gas price and the free market that exists around transaction selection, he can just make a second transaction from the same account with a dramatically higher gas price (In todays market maybe 200 Gwei) and Kris will see the original transaction go through with out issue.

I have no idea how feasible this is and sadly I am only able to be a cheerleader for this initiative. **Parity? Geth? Can this be implemented? What is the best way to go?**

## Replies

**MicahZoltu** (2018-07-02):

I believe this can be implemented on a per-client basis as an optimal mining strategy without any need for consensus/standardization.  I’m mildly surprised that it isn’t already implemented this way, as it does seem to be a better strategy than the current strategy.

---

**AtLeastSignificant** (2018-07-03):

I’m not so sure it’s actually better than the current strategy, but what the “current strategy” actually is remains completely undefined/unknown to me.  There’s enough traffic that the optimal mining strategy is still to pick transactions with the highest gas price and lowest gas limit, gas price being a much bigger factor.

---

**GriffGreen** (2018-07-05):

If the miner were able to group transactions by account, they would be able to better maximize profit. If the network is loaded with 20 gwei transactions and i sent one tx from my account with a nonce of 5, gas 21000 and a gas price of 5 gwei, and then a second tx from my account with a nonce of 6, gas 21000 and a gas price of 50 gwei, the miner would make a nice profit by including both transactions into their next block… but right now they can’t see that they have this opportunity.

The other big piece is that this creates a really nice feed back loop so that a user can react to a spike in the network’s gas cost.

---

**MicahZoltu** (2018-07-05):

Ah, you are saying that the problem is that the 5 nanoeth transaction may be dropped and not propagated because the strategy for populating the global pending queue for most clients is “highest gas” ordering?

I still feel like each client could make this change independently and improve the quality of the system without agreeing in advance of the change.  Though, you are right that the benefits are limited if most of the nodes continue to follow the old strategy, while if most of the nodes follow the proposed strategy then everyone benefits.

---

Personally, I would prefer to address the gas price issue via functional gas prices (as I described over at https://ethresear.ch/t/first-and-second-price-auctions-and-improved-transaction-fee-markets/2410/7 (last paragraph)

---

**karalabe** (2018-07-13):

Hey all,

There are a few issues with this proposal, hence why it’s not *that* obvious as to how it could be implemented.

The primary issue is transaction propagation. The current logic of propagating and queuing transactions only takes into account the gas price. This gives the transactions a full ordering, so given arbitrary transactions in the network, you can always decide which ones fit into your pool (and propagate) and which ones to drop. This is an essential invariant to prevent DoS attacks on the network via spam transactions.

If we however allow later transactions to influence the propagation and queuing of earlier ones, then we all of a sudden need to handle batches of transactions (opposed to singleton ones), otherwise a node cannot know if a transaction will be “supported” by a later child one or not. I’m afraid that this opens up an attack vector as adding a single transaction can modify the entire order within the pool.  It may possibly be doable, but it’s much much harder than it looks and the txpool is a critical DoS failure point, also potentially an amplification attack. Hence why we must be very conservative of what we allow there.

---

A second issue is that this logic only works for plain value transfers. I.e. even if a transaction requests 1M gas * 50gwei, the miner can only ever assume that it will use 21000, since the only way to see the actual gas usage (and inherently fee) is to execute the transaction. This means that we’d be changing the entire transaction propagation and pooling protocol for something that will not be able to help the generic use cases, only maybe some large exchanges which do plain transfers.

A third issue is that if I “group” a batch of transactions together to be executed at once, I also need to ensure the account will have enough balance to cover the execution of all of them, I can’t just check whether there’s enough for the next, since then I could attack the miner by “running out of balance” by the time we get to the expensive tx. A naive solution would be to ensure the account’s balance is larger than all the transactions’ gas limit * gas price, but that doesn’t cover refunds, or receiving ether, etc.

---

My point really being that this optimization is non trivial to pull off due to Ethereum transactions being much more powerful than Bitcoin ones. It could work for plain transactions, but is the complexity worth it? Perhaps.

Just another random thought, if we ever get to implement the EIP where a contract pays for the transaction instead of the sender, all this logic will go belly up massively. Point being, it’s not that trivial.

---

**karalabe** (2018-07-13):

Oh, and to answer the original issue of Yalor’s transaction being dropped. First, it will not be dropped if Yalor is running his own node (haha, now you see why running you own node (even if light client) makes sense).

If however Yalow still wants to use Infura, it might be a lot easier to make his wallet a bit smarter and have it detect that the transaction was dropped and support resubmitting it with a higher gas fee. You could even pre-sign multiple gas-price-points of the same transaction, and automatically submit higher ones if you detect it doesn’t go through. All this can be done automatically client side without having to mess with the protocol.

---

**GriffGreen** (2018-07-15):

First off, wow! Peter! Thx for such a detailed response!

i assumed this was more difficult than it sounded because other wise it would have been done a long time ago i’m sure.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> The primary issue is transaction propagation. The current logic of propagating and queuing transactions only takes into account the gas price. This gives the transactions a full ordering, so given arbitrary transactions in the network, you can always decide which ones fit into your pool (and propagate) and which ones to drop. This is an essential invariant to prevent DoS attacks on the network via spam transactions.
>
>
> If we however allow later transactions to influence the propagation and queuing of earlier ones, then we all of a sudden need to handle batches of transactions (opposed to singleton ones), otherwise a node cannot know if a transaction will be “supported” by a later child one or not. I’m afraid that this opens up an attack vector as adding a single transaction can modify the entire order within the pool.  It may possibly be doable, but it’s much much harder than it looks and the txpool is a critical DoS failure point, also potentially an amplification attack. Hence why we must be very conservative of what we allow there.

Transaction Propagation will definitely be an issue. This might be a feature that only works well if you have your own node to push all the txs you need out…

As far as potential for DoS attacks, it sounds like a valid concern. I hope mitigations can be engineered away in the implementation though because i think it would lower the DoSing that happens when there are black swan events that raise the gasPrice for the whole network effectively denying service to normal and super users.

Normal users can get their tx served by making one new tx and super users could implement more complicated strategies with this feedback mechanism that would allow them to reduce their standard transaction prices (which would allow the whole network to save money on gas)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> A second issue is that this logic only works for plain value transfers. I.e. even if a transaction requests 1M gas * 50gwei, the miner can only ever assume that it will use 21000, since the only way to see the actual gas usage (and inherently fee) is to execute the transaction. This means that we’d be changing the entire transaction propagation and pooling protocol for something that will not be able to help the generic use cases, only maybe some large exchanges which do plain transfers.

Definitely, you would have to assume the higher nonce transactions are only good for 21000 when you do the second calculation for average gasPrice, this doesn’t seem like a deal breaker and @todr:matrix.org and I have been chatting about it

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> A third issue is that if I “group” a batch of transactions together to be executed at once, I also need to ensure the account will have enough balance to cover the execution of all of them, I can’t just check whether there’s enough for the next, since then I could attack the miner by “running out of balance” by the time we get to the expensive tx. A naive solution would be to ensure the account’s balance is larger than all the transactions’ gas limit * gas price, but that doesn’t cover refunds, or receiving ether, etc.

This is also a big issue IMO figuring out how to mitigate this and the various other ways it can be gamed or along with the first issue, how it can be used to DoS the network… if we have to limit the scope where it applies only to ETH transactions… does it lose it’s value?

The biggest DoS attack i see goes a long these lines.

**Account i, tx1**: gp=1 gwei, value=0, data=calls a contract, that calls a contract, that calls a contract that empties the account completely

**Account i, tx2**: gp= 10000 gwei, value=0, will not give the miner and money because it has no ETH in the account

**Account i+1, tx1**: gp=1 gwei, value=0, data=calls a contract, that calls a contract, that calls a contract that empties the account completely

**Account i+1, tx2**: gp= 10000 gwei, value=0, will not give the miner and money because it has no ETH in the account

**Account i+2, tx1**…

I assume there are more too ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12) and if contracts could pay for gas, or gasPrice could be an equation, or some hard fork made some other magic happen… that would be great! But i’m not holding my breath… we need a better solution “NOW!” to mitigate black swan events that spice the gasPrice… this itself ends up being a DoS attack to your average user.

We need to allow a feedback loop that doesn’t involve replacing a transaction and I hope this can move us in that direction.

---

**GriffGreen** (2018-07-15):

Parity made an issue in their client’s repo:

https://github.com/paritytech/parity/issues/9118

We will see if we can use their scoring implementation to make this happen ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

