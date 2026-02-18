---
source: magicians
topic_id: 6687
title: Permissionless, Sybil-Resistant dType/Tagging system
author: Ethernian
date: "2021-07-19"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/permissionless-sybil-resistant-dtype-tagging-system/6687
views: 488
likes: 0
posts_count: 3
---

# Permissionless, Sybil-Resistant dType/Tagging system

Hello Friends,

I am looking for some decentralized type system, maybe similar to **dType** developed by [@loredanacirstea](/u/loredanacirstea) (?). It should…:

1. be permissionless
2. be sybill resistant
3. not assume for any of the actors to have indisputable right to set the truth.
4. provide game-theoretical incentives…
a) to collapse semantically identical types into the single one
b) to split one type into two and more semantically different types.

Any ideas?

## Replies

**loredanacirstea** (2021-07-20):

[@Ethernian](/u/ethernian)

1, 2 and 3 are solved by continuous voting: https://youtu.be/9ljWZgQT2q4

This is a better version of dType than the one described in the EIPs:

https://youtu.be/XMCgL99noYY?t=499. And now we are working on a 3-rd version. So I don’t know yet what will suit you best.

In what ways do you want to use dType on-chain, and in what ways off-chain?

Regarding a) we had already a version where types were defined by structure, hence collapsible if the structure was the same.

Regarding b) we also had a version where you could create two different names for types with the same structure.

We could probably have a mix.

When do you expect to use dType?

---

**Ethernian** (2021-07-20):

Hello [@loredanacirstea](/u/loredanacirstea),

thank you for your prompt reply!

We need to adopt some decentralized type system ASAP, but I need to spend diving dType few days more to understand how (and if) it could fit our requirements.

Our UseCase is to tag the off-chain data with type information and request data records based on the attached type info. We need to determine if one type is assignable to another one, but I see no further on-chain operations. Maybe even this operation can be defined off-chain, then we don’t need on-chain processing at all.

We see two challenges:

1. type system should allow building efficient indexes in the swarm network to retrieve the data (swarm uses decentralized KV storage).
2. preventing the creation of different types with identical semantic. Preventing spam.

I need to check if our domains are close enough…

anyway a lot of thanks for prompt reply!

