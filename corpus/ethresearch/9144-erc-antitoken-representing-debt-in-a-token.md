---
source: ethresearch
topic_id: 9144
title: "ERC: Antitoken - Representing debt in a token"
author: hazae41
date: "2021-04-10"
category: Economics
tags: []
url: https://ethresear.ch/t/erc-antitoken-representing-debt-in-a-token/9144
views: 1014
likes: 0
posts_count: 3
---

# ERC: Antitoken - Representing debt in a token

**Simple Summary**

Representing debt in a token. Like an ERC-20 but with `receive` instead of `transfer`. Thus, the token has a negative value: the less you have, the better.

**Abstract**

Imagine a anti-currency blockchain where, instead of signing the sending, you sign the receival.

You cannot send the currency to an address, you can only receive it from the given address.

Thus, the incentive is to spend it, nobody wants it, the currency has a negative value.

This ERC uses a smart contract to emulate an anti-currency on the Ethereum ecosystem.

**Motivation**

An antitoken can be used to represent debt, bad reputation, or anything negative in relation to its owner.

The incentive is to spend it and to have a balance of zero.

**Technical specification and reference implementation**

See [Pull request #3476](https://github.com/ethereum/EIPs/pull/3476)

**Your feedback is appreciated ![:eyes:](https://ethresear.ch/images/emoji/facebook_messenger/eyes.png?v=9)**

## Q/A

**What prevents me from receiving the token on a random address I own?**

This operation would be visible on the blockchain.

Also, the contract MAY only allow transfers to known addresses.

## Replies

**kristofgazso** (2021-04-10):

Thank you for the suggestion, sounds interesting. From a technical point of view this makes sense, however, my initial worry is what is stopping users from simply creating a new account in case they have too many negative tokens? Could you suggest scenarios that counteract this or disincentivise this to the point where creating a new account will not be rational?

---

**hazae41** (2021-04-10):

Thanks for your feedback, the contract MAY only allow transfers to known addresses

