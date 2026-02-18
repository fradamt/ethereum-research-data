---
source: magicians
topic_id: 8499
title: ERC20 with built in fee structure?
author: Bschuster3434
date: "2022-03-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/erc20-with-built-in-fee-structure/8499
views: 1084
likes: 1
posts_count: 6
---

# ERC20 with built in fee structure?

Hey folks,

I’m looking to see if there are any standards or proposals around a token that upon sending pays a fee to another address? An example would be a token that automatically pays 1% of the total transaction amount to a predetermined contract or wallet.

I did some searching through the EIP standards but didn’t see much.

As a reference, here is my solidity code with an early implementation of this idea: [GitHub - Bschuster3434/Comrade-Token: Open Source Repository for the Automatically Redistributing Comrade Token](https://github.com/Bschuster3434/Comrade-Token)

Here’s an example of what this looks like on Polygon: [Contract Address 0x70e4a39e46695c42f5dd7821b3c32af4b4a8253a | PolygonScan](https://mumbai.polygonscan.com/address/0x70e4a39e46695c42f5dd7821b3c32af4b4a8253a)

Any thoughts for feedback would be appreciated.

## Replies

**auryn** (2022-03-03):

The [CULT token](https://github.com/cultdao-developer/cultdao/blob/main/contracts/cult.sol) does this.

I’m not aware of any standard for this type of fee collection though.

Worth pointing out that it’s trivial to circumvent this type of fee, simply by wrapping the token. If the token gains any kind of traction, there will almost certainly emerge a market for a wrapped version of this token that circumvents the fee.

---

**wjmelements** (2022-03-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bschuster3434/48/5591_2.png) Bschuster3434:

> Any thoughts for feedback would be appreciated.

It doesn’t make sense to take a fee on all transfers. It breaks the assumptions of ERC20 users. Don’t ever do it.

And, 1% is a lot. I will wrap your token.

---

**Bschuster3434** (2022-03-04):

Very new to this platform, so sorry if I just double messaged you. Here’s what I replied:

“It breaks the assumptions of ERC20 users”

Yes, I agree. My preference would be that your wallet would let you know what exactly you’re paying up front before the fee is sent. We don’t have anything that resembles this today, which is why a standard on how fees are paid would be a logical first step to allow for transparency.

“And, 1% is a lot”

The fee, of course, is arbitrary. It can be a flat fee on all transactions. It can be progressive, regressive or flat. But I have to imagine if you’re using this token (given how many choices you have in payment), you would only be using this token if you had some reason to want to support the community these funds are being distributed to.

Thank you for your feedback!

---

**wjmelements** (2022-03-24):

[@Bschuster3434](/u/bschuster3434) I don’t think you understood one part of my reply:

> I will wrap your token.

You cannot charge a fee on transfer because I don’t have to use your contract directly. I can deposit it into a wrapper token contract and use that instead. Fees on transfer therefore cannot be your business model.

---

**Bschuster3434** (2022-03-25):

No, I did understand your response. That’s a threat to this particular model, I agree.

