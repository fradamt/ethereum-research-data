---
source: magicians
topic_id: 9208
title: "EIP-5081: Expirable Transaction"
author: xinbenlv
date: "2022-05-08"
category: EIPs > EIPs core
tags: [gas]
url: https://ethereum-magicians.org/t/eip-5081-expirable-transaction/9208
views: 3435
likes: 3
posts_count: 20
---

# EIP-5081: Expirable Transaction

Hi all, I started a draft for 5081 as a re-pursueing the transaction expiration.

Please find the draft content here: [Create eip-5081.md Expirable Transaction by xinbenlv · Pull Request #5081 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5081)

Here is a list of previous attempt to pursue the transaction expiration.

- EIP pull request 599
- EIP-2711: Separate gas payer from msg.sender #2711, it’s withdrawn
- EIP-2718: Typed Transaction Envelope #2718 diverted from the purpose of expiring transactions.
- Add temporal replay protection #1681 stagnant and I don’t think there is a reliable way to use clock/ timestamp
- EIP pull request 773
- Transaction Expiration Init EIP

Please conment in this trhead.

TODO: consider creating a follow up network EIP to add `gosspi_ttl`

## Replies

**xinbenlv** (2022-05-09):

In response to [@MicahZoltu’s comment about DoS attack](https://ethereum-magicians.org/t/eip-599-valid-until-block-field-for-transactions/3440/3) in which I quote here:

> Expiring transactions run into the problem of opening up an attack vector against the chain because someone can submit a transaction (which results in it being propagated around the network, which is not free) and then they end up not having to pay anything in the end. In general, we want every transaction that is propagated to result in a non-trivial cost to the sender.
> One option to work around this is to have an expired transaction still be includable, but it would just cost 21,000 gas and otherwise do nothing. The 21,000 gas is to cover signature validation, cold account loading, balance read, and balance write. Maybe it could be a little less, since there is guaranteed to be no second account loaded (recipient).

One solution I can think if is to suggest (but not require) propagating nodes initialize a `gossip_ttl` and deduct at their choice in the unit of `blocknum`. The node will only propagate `tx` that is far enough away from the `expire_by` blocknum (at least `gossip_ttl` blocks ahead).

1. In this way, a malicious transaction signer will risk causing transaction fees should their tx are executed within blocknum
2. A malicious transaction signer’s tx will not be include for propagation if it’s after or too close from expiring.
3. A malicious node who ignores gossip_ttl from other node will be waiting their network / processing resource because their receipient of propagation might drop that tx.
4. Choosing the unit of gossip_ttl to be in blocknum so that propagating nodes with different network behavior protocols can make their choice in this unified way, because gossip_ttl is not network protocol-specific.
5. Giving control of initializing and deducting gossip_ttl to nodes also gives flexibility for them to come up with dynamic solutions for their network nature.

Credit to: [@Arachnid](/u/arachnid) who originally think a concept of `gossip_ttl`.

---

**MicahZoltu** (2022-05-09):

I have two problems with a suggested TTL:

1. If the default behavior is to drop transactions, then the attack vector exists even if people can choose to not drop the transaction.
2. Currently, miners could choose to drop transactions that fail but they don’t, because it is profitable to include them.  This would still be true after this change and it is against a miner’s interest to drop a transaction that they could include.

---

**xinbenlv** (2022-05-09):

Thank you Micah. I could understand Point 1

> If the default behavior is to drop transactions, then the attack vector exists even if people can choose to not drop the transaction.

But could you help me better understand the Point 2 why it’s profitable to include them for miners?

> Currently, miners could choose to drop transactions that fail but they don’t, because it is profitable to include them. This would still be true after this change and it is against a miner’s interest to drop a transaction that they could include.

If we say that any tx.expire_by **can** be included in a block, but with a **failed** status and charged fee, then yes, miners are incentivized to include that tx that fails. But this is not what we choose. In EIP-5081, I intend to rule this type of tx out completely as invalid tx.

Help me understand in this case is miner still incentive to keep expired tx? It’s not very obvious to me so. I humbly believe no.

---

**MicahZoltu** (2022-05-09):

Sorry, (1) applies if the transactions become invalid, (2) applies if the transactions remain valid.

If the transaction becomes invalid, then the attack vector is that someone can submit a bunch of transactions that they know won’t be included and the network has to pay to gossip them but the attacker doesn’t have to pay anything other than the cost to construct and send them.

If the transaction remains valid, then miners will include them because it is profitable.

---

**xinbenlv** (2022-05-09):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> (1) applies if the transactions become invalid

Let me clarify: Yes the [current snapshot of EIP-5081](https://github.com/ethereum/EIPs/commit/76c2db02094194d3ae39438d2a9e1cadcd668808#diff-e44cf8c77cce97a42bfa55f629a8c237e2cf12010da9a6e5b445d1ccd16c8b55)’s intended behavior is (1) that tx becomes invalid.

Plus suggesting but not require that node not only drop already invalid tx, but also drop soon-to-expire tx. The *threshold of how soon* can be decided by implementation of that particular instance of gossip-protocol that the node run.

If that node decide that current block num is *too close* to the expire blocknum. In this case, the tx will be dropped.

The introducing of `expire_by` creates three scenarioes worth of discussion:

1. that attackers could send many already-expired tx e.g. specify a expire_by that is smaller than the current block number: to my understanding, a tx being invalid due to expiration, is no different other scenarios that renders a tx invalid, e.g. colliding nonce. I’d assume our network protocol is already well handling this problem as a solved one. (I will come back with a question about knowledge of the current network protocol though)
2. that attackers could send many soon-to-expire tx: In this case, since some of these TXs will expire during the time of propagation, but also some of these TXs will arrive and be mined un-expired, that causes some costs for attackers. The risk is that the sooner these TX set for the blocknum, the more often such TX expiration happens during propagation. Now if we suggest each node to at least set some threshold before which they will stop propagating the TXs, but it’s up-to-them to decide how big such threshold to be.
3. that attackers sends too many not expiring soon TXs, e.g. with a very large blocknum. These TXs are no different than not specifying an expire_by, just like today’s valid TXs.

Now comes back to my question about the gossip protocol: what’s the current way of incentive for nodes to propagate tx? What incentives do nodes get that motivates them to choose whether or not to propagate a tx? The best reference I could find is the [devp2p/eth.md#transaction-exchange](https://github.com/ethereum/devp2p/blob/26e380b1f3/caps/eth.md#transaction-exchange)

> When new transactions appear in the client’s pool, it should propagate them to the network using the Transactions and NewPooledTransactionHashes messages. The Transactions message relays complete transaction objects and is typically sent to a small, random fraction of connected peers.

It seems all tx *will be* propagated is just because the protocol mandates conveniently that all tx in the node’s local pool shall be querieable by that node’s connected peers.

But it doesn’t seem obvious to me will there ever be any mechanism that stops specific version of implementation of nodes to ignore a transaction outright and reject propagating a particular transaction.

Technical, dropping a tx can happen in the following stage

[source[([devp2p/caps/eth.md at 26e380b1f3a57db16fbdd4528dde82104c77fa38 · ethereum/devp2p · GitHub](https://github.com/ethereum/devp2p/blob/26e380b1f3/caps/eth.md#transaction-exchange))

> On receipt of a NewPooledTransactionHashes announcement, the client filters the received set, collecting transaction hashes which it doesn’t yet have in its own local pool.

Maybe one way is to in addition to maintain just one transaction pools, also maintain a separate pools of tx that a node is *aware of*, but decided not worthy of propagating because of too soon to expire, let’s call it `TooSoonToExpireTxPool` (TSTETP). So any request to get a hash fall in that TSTETP will be rejected with some status code and hence stops propagation.

---

**MicahZoltu** (2022-05-09):

The problem is that users can construct transactions that are valid to gossip but unlikely to be mined.  For example, you can set the max fee to something small.  With never expiring transactions, you will *eventually* have to pay for that transaction (or a more expensive one).  With expiring transactions, the same transaction would gossip and then expire out of the mempool and no fee would be paid.

---

**xinbenlv** (2022-05-10):

that is scenario #2 which is resolved by node maintaining its “drop in advance” threshd(gossip_ttl) to reduce such risk, i wonder if I made my argument clear.

If attacker set a low price but a very far away expire date, as if it will next expire, it is essentially scenario 3 which already exists in today’s case: attack risks such tx to actually be executed and incurs costs?

Maybe we could have a live discussion if that helps? I’ve apply to sign up this EIP for May 13 coredev meeting, will you be there this week?

---

**MicahZoltu** (2022-05-10):

The cost is born as soon as the transaction is gossiped across the network, which only takes a handful of seconds.  If the transaction is dropped from the pool later, the network has already eaten the majority of the operational cost of that transaction.

You are correct that someone can lowball a transaction today and then *hope* that it falls out of the mempool.  However, mempool sizes are incredibly variable between different node operators, with some running mempools that are *incredibly* large and they will rebroadcast (or include in a block) transactions that fell out of many people’s mempools.  This gives some attack protection because it is not possible for the transaction author to know whether their transaction has in fact been dropped from the pool or not, so they may not be able to replace their transaction *without* a fee increase across the network.

With expiring transactions, the transaction author knows with certainty when a transaction is no longer valid and this occurs at a well defined point in time across the whole network.  This gives an attacker a huge advantage over the current situation because they know exactly when they can submit a new transaction (without a gas price bump) and have it override their previous transaction.

---

**xinbenlv** (2022-05-12):

Agreed and understand that even low ball transactions today and hope it falls out. How do you like the idea of suggest / require client implement some approach to **drop near-expire transaction**?

E.g. if propagation takes about O(10s) max, make any TX to be dropped in Mempool from (expired_by - gossip_ttl) whereas gosspi_ttl = 2 ~ 4 (blocks)

---

**MicahZoltu** (2022-05-13):

I think you still end up with the same problem that someone can just game the expiration time.  Make a transaction that will expire a few seconds after whatever expiration would allow the attacker to be confident that the transaction has propagated across the whole network.

---

**xinbenlv** (2022-05-13):

A presentation for further the discussion of EIP-5081



      [docs.google.com](https://docs.google.com/presentation/d/1XuXuF-TFVKT1Q_GEd0lOS8o7Ff2RmUG_rjF63JQlF_Y/edit#slide=id.g12a091fd80b_0_35)



    https://docs.google.com/presentation/d/1XuXuF-TFVKT1Q_GEd0lOS8o7Ff2RmUG_rjF63JQlF_Y/edit#slide=id.g12a091fd80b_0_35

###

EIP-5081 Expirable Transaction First Feedback Requested Zainan Victor Zhou (xinbenlv@github) 2022-05-13 for Ethereum Core Devs Meeting










Please comment here in the ethereum-magician thread

---

**xinbenlv** (2022-05-15):

[@MicahZoltu](/u/micahzoltu) hey Micah, thank you for your feedback, while I am still working on resolving the security issue, since you previously have pursued this issue, do you mind to consider co-author or advice this EIP?

---

**MicahZoltu** (2022-05-17):

Lets wait to add me as an author until the EIP is further along so I can decide whether it is something I support or not.  ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)  I’m a big fan of expiring transactions, but I *am* concerned about the denial of service vector introduced and at the moment I would still rather see expiring transactions still end up on-chain, just at very low gas cost (less than 21,000 gas for expired transaction).  It is possible I could be convinced that free expiration could work, but at the moment I’m not.

---

**Brayton** (2022-05-17):

I think there’s two questions at heart here:

1. Should users be charged for included/attempted expired transactions?
2. Does it matter if the charge is  21,000 gas?

Imposing a non-zero cost will penalise spam and generally internalise the externalities: post-1559 miners are unlikely to receive much benefit from intentionally included these tx if they’ve been holding onto them for quite some time and let them expire. The user is harmed more than the miner benefits. This perhaps prevents miners/validators from including very short-lived transactions, then propagating them, such that they’re valid for the originating miner yet invalid for all others.

Given that users who benefit from expiring transactions will likely benefit quite a bit, I’d guess they’ll be fine if the cost is much greater than 21,000 gas. If post-London 5% of Uniswap tx revert, costing perhaps ~60,000 gas, then it should be fine if expiring tx are more expensive than non-expiring. It’s less fun, since the whole purpose of expiring tx are to expire some of the time.

I’d rather get them as low as safe of course.

---

**MicahZoltu** (2022-05-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/brayton/48/4895_2.png) Brayton:

> Given that users who benefit from expiring transactions will likely benefit quite a bit, I’d guess they’ll be fine if the cost is much greater than 21,000 gas. If post-London 5% of Uniswap tx revert, costing perhaps ~60,000 gas, then it should be fine if expiring tx are more expensive than non-expiring. It’s less fun, since the whole purpose of expiring tx are to expire some of the time.

I think we can do less than 21,000 gas.  21,000 gas covers signature validation, loading two accounts from storage, updating the nonce and balance of one account and the balance of the other account, and then writing both accounts back to storage.

An expired transaction needs to cover signature validation and loading, updating, and storing one account.  I don’t know what the exact cost would end up being, but it should be strictly *less* than 21,000 because we only need to load/store a single account.

It is worth noting that an expired transaction can also be used as a cancellation transaction that costs less than current cancellations (21,000 gas), so we would kill two birds with this one change.

---

**xinbenlv** (2022-05-17):

> Lets wait to add me as an author until the EIP is further along so I can decide whether it is something I support or not.  I’m a big fan of expiring transactions, but I am concerned about the denial of service vector introduced and at the moment I would still rather see expiring transactions still end up on-chain, just at very low gas cost (less than 21,000 gas for expired transaction). It is possible I could be convinced that free expiration could work, but at the moment I’m not.

Thanks Michah! I understand that you like the idea of tx expiration, but unconvinced if it can go free of charge to avoid DoS.

Can I try to summarize the current question of design and the (partial) consensus among us?:

1. Priority: Is Expirable Transaction high priority?  My understand is that you @MicahZoltu and I @xinbenlv  have consensus that it’s relatively high. Other core developers needs convince or proof that the cost to implement is lower than the priority. I am a bad writer of motivation, and since you @MicahZoltu  authored Typed Transaction (2718), can you help with your experience to write / suggest better motivation use-cases / argument for this EIP?
2. Cost: Should we let expired TX stay on chain or can we leave it out free? Can I try to validate if we have the following consensus among us: @Brayton @MicahZoltu, @xinbenlv

- a) we should charge as little as possible Gas for expired transaction, if it that’s required for avoiding DoS
- b) if the assumption holds that it’s possible to avoid DoS and other side-effects of free expiration, we should allow transaction to go expired free.

Are these statements a good assumption of our current consensus? If so, I can further do the research on whether counter-DoS requires on-chain costs and come back. Any help is apprecated too.

---

**MicahZoltu** (2022-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Priority: Is Expirable Transaction high priority? My understand is that you @MicahZoltu and I @xinbenlv have consensus that it’s relatively high. Other core developers needs convince or proof that the cost to implement is lower than the priority. I am a bad writer of motivation, and since you @MicahZoltu authored Typed Transaction (2718), can you help with your experience to write / suggest better motivation use-cases / argument for this EIP?

It is often easier to show that an EIP is incredibly simple, rather than showing that it is incredibly valuable.  I suspect either solution for (2) would be quite easy to implement in any major client, and validating that with a reference implementation may be a good first step.  Perhaps this would be a good opportunity to give the new executable spec a try?

---

**xinbenlv** (2022-05-19):

Sounds good, I will give it a try.

I will start with the reference of the [commit](https://github.com/ethereum/go-ethereum/commit/bbfb1e4008a359a8b57ec654330c0e674623e52f)

---

**MaxResnick** (2023-07-16):

Hey all wanted to suggest that we upgrade priority of this, since it seems like there is consensus that this is useful but given some events that have transpired since may 22, importantly the low carb attack and the renewed focus on single slot finality as a potential mitigation tactic, I think it is more useful than we realized. This proposal, if implemented would prevent the multi block version of the low carb attack which is still theoretically possible after the patches made to MEV boost.

Also I’d like to suggest we switch from block based timeout to slot based timeout now that the merge has happened.

