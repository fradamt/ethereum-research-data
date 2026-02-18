---
source: magicians
topic_id: 13964
title: "ERC: Subscription Based ERC20 Token"
author: 0xRobinR
date: "2023-04-25"
category: EIPs
tags: [token, erc-20, subscription]
url: https://ethereum-magicians.org/t/erc-subscription-based-erc20-token/13964
views: 1742
likes: 3
posts_count: 13
---

# ERC: Subscription Based ERC20 Token

Discussion thread for new EIP, **Subscription based ERC20 Token**, an extended form of EIP20

## Replies

**abcoathup** (2023-04-25):

Suggest reading: [Guidelines on How to write EIP. Do's and Don'ts including examples | by Anett | The Fellowship of Ethereum Magicians | Medium](https://medium.com/ethereum-magicians/guide-on-how-to-write-perfect-eip-70488ad70bec)

EIP editors assign an EIP number (generally the PR number, but the decision is with the editors) (from: [EIP-1: EIP Purpose and Guidelines](https://eips.ethereum.org/EIPS/eip-1#eip-numbers)), so you can’t just pick your own, e.g. ERC360

---

**0xRobinR** (2023-04-25):

Apologies for that, I had read the guidelines, thought I could “propose” the number. Nevermind.

---

**0xRobinR** (2023-05-02):

Any views/comments on this proposal ?

---

**0xRobinR** (2023-05-22):

[github.com](https://github.com/360core/EIPs/blob/master/EIPS/eip-6932.md)





####



```md
---
eip: 6932
title: Subscription-Based Token
description: access to a service or product that requires recurring payments.
author: 360 Core , Robin Rajput (@0xRobinR)
discussions-to: https://ethereum-magicians.org/t/erc-subscription-based-erc20-token/13964
status: Draft
type: Standards Track
category: ERC
created: 2023-04-25
requires: 20
---

## Abstract

The subscription-based [ERC-20](./eip-20.md) token extends the basic [ERC-20](./eip-20.md) token standard with a `subscribe` and `unsubscribe` function, which allow users to subscribe or unsubscribe from the subscription service. The `subscriptionFee` and `subscriptionFrequency` variables define the cost and frequency of the subscription. The `nextPaymentDate` mapping keeps track of the next payment date for each subscriber.

This EIP also proposes adding `renewSubscription` functions to the token contract, that can be used by token holders to renew their subscription to a service or product that requires recurring payments in the form of the token.

## Motivation
```

  This file has been truncated. [show original](https://github.com/360core/EIPs/blob/master/EIPS/eip-6932.md)










link to the eip proposed

---

**0xRobinR** (2023-06-01):

a working implementation on auto-debit subscription-based erc20 token - [EIP 6932](https://github.com/360core/eip-6932)

---

**SamWilsn** (2023-09-20):

Why use this over using [approve](https://eips.ethereum.org/EIPS/eip-20#approve) with a subscription contract? This explanation should probably also appear in your Motivation section.

---

**0xRobinR** (2023-09-21):

sure, will add that too, here’s a quick glance -

if you use simple `approve` with a subscription contract, the contract will have to call again and again to fetch the subscription amount from the `subscribers`. in our EIP, this will not have to be the solution, it will be `auto-debited` and `auto-credited` without doing any single transaction. check the contracts for more info.

---

**SamWilsn** (2023-09-21):

I’m not sure I follow (and I’ll be the first to admit my Solidity isn’t the best.) It looks like `subscribe` is supposed to lock an amount of tokens depending on the duration of the subscription?

---

**0xRobinR** (2023-09-23):

It’ll lock the tokens of the recurring subscription amount, and not all the tokens at once. For example, if there’s a `20 tokens` per `month` frequency, for a total period of `12 months`, the contract will

1. lock the first month amount
2. then it will check for the 2nd month subscription amount,
3. if the user holds the amount, it’ll be again locked (auto-debit) or,
4. their subscription will be void/cancelled.

this will all happen behind the curtains, all the values will be updated auto, no transaction needed.

---

**SamWilsn** (2023-09-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xrobinr/48/9258_2.png) 0xRobinR:

> then it will check for the 2nd month subscription amount,

Does this happen as part of the first transaction? When does the 3rd month get locked/debited?

---

**0xRobinR** (2023-09-23):

no, after the subscribe transaction, the contract will update the state of the account, and then it all depends on the subscription `start time (info.start)` and `period elapsed (block.timestamp)`, all in a calculation

```auto
uint256 intervals = ( block.timestamp - info.start ) / info.frequency;
uint256 amount = info.amount * intervals;
```

for continuation of the subscription, the account must hold, greater than the `amount` tokens

the current balance will be the `actual balance` - `subsription amount(s)`, when he transfers (normal transfer) the tokens, the `actual balance` gets updated

---

**MMujtabaRoohani** (2025-10-14):

too late to the party but I think the proposal has two major lackings,

1. User has to buy and maintain the required balance of subscription tokens to subscribe instead of using stables or any other ERC20 token to purchase a subscription.
2. User subscriptions needs to be private, keeping it on-chain will make this data public.

No doubt, that a standardized way to manage subscriptions in crypto is essential but I don’t think any proposal can gain mass adoption without solving these 2 simulatneously.

