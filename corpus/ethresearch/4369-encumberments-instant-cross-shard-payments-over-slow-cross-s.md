---
source: ethresearch
topic_id: 4369
title: "Encumberments: instant cross-shard payments over slow cross-shard base-layer communication as a layer 2"
author: vbuterin
date: "2018-11-25"
category: Sharding
tags: []
url: https://ethresear.ch/t/encumberments-instant-cross-shard-payments-over-slow-cross-shard-base-layer-communication-as-a-layer-2/4369
views: 5079
likes: 10
posts_count: 9
---

# Encumberments: instant cross-shard payments over slow cross-shard base-layer communication as a layer 2

Suppose that Alice, Bob and Charlie are all users of the sharded Ethereum Serenity blockchain, and all three are on different shards. Each shard has an internal block time of ~6 seconds, but communication between shards takes ~6 minutes because crosslinks between shards only happen once per cycle. Suppose that Alice holds 5 ETH.

Suppose Alice wants to send Bob a payment of 5 ETH. Alice sends a transaction which destroys the 5 ETH on shard A, and creates a receipt (see [here](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#how-can-we-facilitate-cross-shard-communication) for how receipts work) that Bob can then use to claim the 5 ETH on shard B. In order for it to actually be possible for Bob to claim the receipt, shard B must be aware of the state of shard A up until that point, which requires waiting 6 minutes for a crosslink. However, note that **Bob gets *confirmation of ownership* within 6 seconds**; that is, as soon as Alice’s receipt is in the chain on shard A, it becomes clear to Bob that he will be able to claim the funds and (aside from failures of the chain) nothing can happen that can stop him. Hence, after 6 seconds Bob’s wallet can show the funds as belonging to Bob.

Now, suppose that as soon as Bob receives the funds, Bob wants to send 5 ETH to Charlie. Unfortunately, it will take 6 minutes for Bob to actually get the funds and be able to make a receipt.

It turns out that by making a change to Bob’s account contract, we can get around this problem. We add to Bob’s account state a queue of “encumberments”, empty by default. An encumberment is a pair `(recipient, amount)`. While the encumberment queue of an account is nonempty, Bob cannot send any transactions. However, once funds are available to pay for it, anyone can send a transaction that generates a receipt transferring the amount specified in the first encumberment in the queue from the account to the recipient (this transaction is a simple “poke”; it need not even have a signature attached), and removes this encumberment from the queue.

**Now, Bob *can* immediately perform an operation that will transfer the funds to Charlie**. Bob creates an encumberment on his account which transfers 5 ETH to Charlie on shard C. Actually transferring the funds will take 12 minutes: 6 minutes for the ETH to reach shard B, at which point the encumberment can be processed and generate a receipt, and then another 6 minutes for the ETH to reach shard C.

However, within 6 seconds, Charlie’s wallet software can reason as follows: in shard A, a receipt has been included in the chain, which will transfer 5 ETH to Bob on shard B. In the state of shard B, Bob’s account now has an encumberment, the first encumberment in the queue, which will transfer the 5 ETH to Charlie as soon as the funds are available. It is guaranteed that Bob’s account can do nothing until the encumberment is removed, and it is guaranteed that in 6 minutes it will be possible (if Bob has not done so already) for Charlie to send a transaction into shard B which will include the receipt from shard A and add the 5 ETH to the account, which will then consume the encumberment and generate a receipt sending the 5 ETH shard C. 6 minutes after that, Charlie will be able to claim the receipt in shard C to get the funds. **Hence, Charlie’s wallet software can show the funds as belonging to Charlie as soon as Alice and Bob’s original transactions get into their respective shard chains**, and in fact, we can extend the encumberment chain further, so Charlie’s funds are immediately “spendable” within the same system.

If Bob is receiving and sending funds to and from multiple participants, the logic becomes more complex. The wallet software can generate a directed graph where each node is an account, and an outgoing edge gets added under the following conditions:

- If there is a receipt going from A to B of N coins, add an edge from A to B with weight N.
- If there is an encumberment in B going to C of N coins, and this encumberment is in a position where there are M coins in front of it in the queue, then if the incoming edges from A to B have total weight >= M+N, add an edge from B to C of weight N.

The wallet software then adds to the local balance the total weight of incoming edges. Note that the wallet software does not need to scan the whole chain; a payer can send the payee the subset of nodes that prove that an edge incoming to the payee exists.

## Replies

**MihailoBjelic** (2018-11-25):

Nice, simple model.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If Bob is receiving and sending funds to and from multiple participants, the logic becomes more complex.

True. Complexity/overhead increases also for txs with more hops.

I’m speaking off the top of my head, but is there any reason why this/similar model couldn’t be used for arbitrary messages? For example, Alice and Bob have some sort of interaction/relationship formalized through a smart contract X on Alice’s shard → Alice submits a zero tx (value=zero) to the contract X (this tx entitles Bob to do something) → the contracts emits an event and writes a log that will be in the Alice’s tx receipt → Bob can read the receipt and instantly act upon Alice’s tx/message (instead of waiting for the async cross-shard process to finish)? As with your payment model, this “instant arbitrary message” could have several hops.

Also (also off the top of my head ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12)), can we have some default “portal addresses” on each shard where anyone can send zero txs with arbitrary messages/claims, so users from other shards can instantly read (and act upon) them using receipts? Or, these addresses don’t have to be default, they can be account/interaction specific (Alice uses one “portal” address to interact only with Bob)?

---

**vbuterin** (2018-11-26):

The main problem with extending this to a more general-purpose EVM is that you cannot know ahead of time in what order two messages will arrive at some contract, making it impossible to predict the state of any contract where the effect of incoming messages is order-dependent.

---

**MihailoBjelic** (2018-11-26):

Thanks [@vbuterin](/u/vbuterin).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> you cannot know ahead of time in what order two messages will arrive at some contract, making it impossible to predict the state of any contract where the effect of incoming messages is order-dependent

I fail to understand this issue. In my example, Alice submits a tx to a contract on her shard (that tx is final, no need to predict any future state of the contract), the receipt for that tx is generated and Bob can instantly acknowledge and act upon it (instead of waiting for the cross-shard tx to “arrive”).

I guess there could be issues e.g. for a multi-hop txs with a smart contract as a destination (instead of Bob), I’ll have to think about that. Maybe those situations can be solved by locking the incoming txs to the contract until the cross-shard tx arrives? Basically, that would be opposite of your instant payments (the contract can not accept/execute any **incoming** tx before it executes the “encumberment”). Or (the same like with your instant payments) the contract can accept incoming txs, but they are added to the “encumberment” queue (to ensure the order of exec)?

---

**vbuterin** (2018-11-26):

Suppose there are two receipts A and B incoming to a contract C, and this contract C is order-dependent (eg. it’s a decentralized exchange contract, A sells OMG for ETH, B sells KNC for ETH, whichever one arrives later fails). C cannot issue a credible encumberment, because it’s not clear which of the two messages will arrive first until they actually arrive.

---

**MihailoBjelic** (2018-11-26):

Hmm, I see…

But wouldn’t the following be a viable solution in that (and probably any other) case:

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> opposite of your instant payments (the contract can not accept/execute any incoming tx before it executes the “encumberment”)

Of course, this would definitely be slower/less efficient than your payments in many cases (the contract is locked while waiting for the cross-shard tx to arrive and there can not be “queues”), but it might be useful in some/many cases?

The point is that I like your concept and I think you might be on a track to something nice here, so I’m trying to play around with it…

Btw, when you say:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We add to Bob’s account state a queue of “encumberments”, empty by default. An encumberment is a pair (recipient, amount) .

you’re assuming account abstraction, right?

---

**vbuterin** (2018-11-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> you assume account abstraction, right?

Yes. I’m assuming that the only kind of object on layer 1 is contracts that have some fixed-size storage pool, and user accounts are contracts.

---

**MihailoBjelic** (2018-11-26):

Cool, thanks, I’ll try to think about this more…

---

**nherceg** (2018-11-28):

What about the total processing time in case of a long chain/cycle of transactions?

For example, an account could generate a dummy address on another shard to send ETH back and forth using encumberments.

Now if that account wants to send a real payment, it can create another receipt for the desired address, but it will take possibly a long time for funds to arrive. This means that the wallet software should be aware of the process duration and set a threshold for the maximum expected waiting time.

It seems to me that, over time, the centralised solutions to the slow cross-shard transactions problem could emerge. Consider this:

Alice from shard A wants to send 5 ETH to Bob on shard B. Instead of using a crosslink, she can send 5 ETH to the “messenger” contract on the same shard. The contract owner notices that and sends 5 ETH from the messenger account on shard B to Bob.

The incentive for the messenger is additional fees provided by Alice.

The reason for sending to contract on shard A rather than EOA is that maybe protection of funds can be guaranteed by automatically sending back ETH if the proof hasn’t been provided that transaction was really sent on shard B.

This proof can be presented in the form of a periodic cross-link with a long period (to gather more transactions), e.g. every 10 slots, which contains aggregated proofs for multiple transactions from shard A to B. If the proof is not presented in the desired time period, e.g., 20 slots, the funds will automatically return to the owner.

