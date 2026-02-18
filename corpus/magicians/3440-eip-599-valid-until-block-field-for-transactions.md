---
source: magicians
topic_id: 3440
title: "EIP-599: Valid-until block field for transactions"
author: kevinsimper
date: "2019-07-04"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-599-valid-until-block-field-for-transactions/3440
views: 1341
likes: 1
posts_count: 4
---

# EIP-599: Valid-until block field for transactions

## Simple Summary

This EIP adds a new field to transactions, `valid_until_block`. Transactions containing this field may only be included in blocks with numbers less than or equal to the value in this field.

## Motivation

Presently, transaction eviction is a significant problem for nodes; if a node’s transaction pool fills up, resulting in the eviction of a transaction, it may receive the same transaction from another node immediately afterwards. Without tracking evicted transactions, nodes cannot determine that they’ve seen the transaction before, and if they do track evicted transactions, an attacker can compel them to waste space keeping track of them. The result of this is that even legitimate transactions may stick around in a busy pool indefinitely, while an attacker can deliberately seek to bloat the network’s transaction pools.

Further, in cases where the network is busy, or a transaction is published with a low gas price, or with a nonce gap or other problem that prevents it from being mined immediately, the transaction may be executed at any time in the future. This can cause trouble for users, where an effect can take place much later than intended, with no clean way to cancel it.

This proposal addresses both of these issues by allowing nodes to place a hard limit on how long they will retain and propagate transactions, limiting the impact of transaction pool bloat and allowing smarter eviction strategies, while also providing users with a way to submit transactions that self-destruct if not mined within a fixed time period.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/599)














####


      `master` ← `Arachnid:txttl`




          opened 03:48PM - 10 Apr 17 UTC



          [![](https://avatars.githubusercontent.com/u/17865?v=4)
            Arachnid](https://github.com/Arachnid)



          [+61
            -0](https://github.com/ethereum/EIPs/pull/599/files)







This EIP adds a new field to transactions, `valid_until_block`. Transactions con[…](https://github.com/ethereum/EIPs/pull/599)taining this field may only be included in blocks with numbers less than or equal to the value in this field. This improves the transaction eviction strategies available to nodes, which improves spam handling, while also making it possible for users to issue transactions that expire if not included by a certain time.

## Replies

**xinbenlv** (2022-05-04):

Hello from 2022

Looking at this proposal from 2022 and its relevant proposals

- EIP 2711, it’s withdrawn, and
- EIP 2718 diverted from the purpose of expiring transactions.
- EIP 1681 stagnant and I don’t think there is a reliable way to use clock/ timestamp

Is anyone still looking at a way to ensure block-number expiration?

[@Arachnid](/u/arachnid) [@kevinsimper](/u/kevinsimper), [@MicahZoltu](/u/micahzoltu)  would consider revive this proposal? If you are not at capacity, I am interested in following up on this. Because I think the possibility to protect against replay attack on a signed message is as critical as what #155 was trying to do, if not even more critical.

---

**MicahZoltu** (2022-05-04):

Expiring transactions run into the problem of opening up an attack vector against the chain because someone can submit a transaction (which results in it being propagated around the network, which is not free) and then they end up not having to pay anything in the end.  In general, we want every transaction that is propagated to result in a non-trivial cost to the sender.

One option to work around this is to have an expired transaction still be includable, but it would just cost 21,000 gas and otherwise do nothing.  The 21,000 gas is to cover signature validation, cold account loading, balance read, and balance write.  Maybe it could be a little less, since there is guaranteed to be no second account loaded (recipient).

---

**xinbenlv** (2022-05-09):

I started a [EIP-5081] to continue pursuing this idea [Create eip-5081.md Expirable Transaction by xinbenlv · Pull Request #5081 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5081). Feedback is welcomed!

