---
source: magicians
topic_id: 5957
title: "ERC: Antitoken - Representing debt in a token"
author: hazae41
date: "2021-04-10"
category: ERCs
tags: [token, defi]
url: https://ethereum-magicians.org/t/erc-antitoken-representing-debt-in-a-token/5957
views: 765
likes: 2
posts_count: 1
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

**Your feedback is appreciated ![:eyes:](https://ethereum-magicians.org/images/emoji/twitter/eyes.png?v=15)**

## Q/A

**What prevents me from receiving the token on a random address I own?**

This operation would be visible on the blockchain.

Also, the contract MAY only allow transfers to known addresses.
