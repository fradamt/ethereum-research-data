---
source: ethresearch
topic_id: 14664
title: What would need to change about the EVM language "solidity" to make it asynchronous
author: Econymous
date: "2023-01-22"
category: Layer 2
tags: []
url: https://ethresear.ch/t/what-would-need-to-change-about-the-evm-language-solidity-to-make-it-asynchronous/14664
views: 1240
likes: 4
posts_count: 5
---

# What would need to change about the EVM language "solidity" to make it asynchronous

First of all, I do entirely understand that everything is processed 1 by 1 on layer 1. I’m thinking about a layer 2 network architecture though where unconnected smart contracts can run in parallel, but some contracts that are connected would need to concentrate resources in some part of the network at time of high volume.

With money involved, a valid concern is who get priority on their transaction? In my imagination, I believe this can be settled by this layer 2 network as it is all under the governance of assets on layer 1.

I’ll need to formulate my thoughts a bit more clear. I feel I can only do that  by brute-forcing myself through some discussion.

Let’s assume there are computers in the real world that go untouched because of watchful eyes from layer 1. In other words, a DAO from layer 1 ensures several computers remain untouched. Let’s assume the DAO is fair. These computers don’t need to mine blocks with proof-of-work or proof-of-stake.

Between these computers needs to exist a language for developers to create smart contracts. I believe we’ll eventually be dealing with some sort of “Chinese Postman Problem”. Trying to optimize routes between machines that involve smart contracts that refer to each other.

What critical features to a programming language need to exist in a network like this? Where a smart contract can still refer to any other smart contract, but it must do so asynchronously and of course gas prices are calculated based on the current concentration of demand.

And when I think about tokens, something interesting pops into mind. I would think a very simplistic token “contract” (if it would even remain that with what I’m about to describe) could be sharded across the network. There shouldn’t need to be a bottle neck around keeping track of simple “points” or some type of simple “token”. Balances could be stored in different regions of the network and there should never have to be many different other smart contract trying to funnel into a single token contract to get accurate balances on different users.

Perhaps my wording is a bit cloudy. I appreciate any contribution to this idea. I’m trying to clear things up for myself.

## Replies

**MicahZoltu** (2023-01-23):

Solidity isn’t what would need to change to make something like this happen.  It would require notable architectural changes to the way Ethereum works.

The biggest problem with this sort of design is the DoS vector that is introduced if you allow transactions to sit in “queue” indefinitely.  You would need a mechanism for removing items from this async queue if they sat too long due to prices never reaching the transaction’s target price.

---

**Econymous** (2023-01-23):

When you say Ethereum, you mean the EVM, correct?

Perhaps it would be some sort of bid. Or a bid based on *Time x Offered Gas* (I’m potentially talking non-sense here, there may be more attack vectors I’m not thinking of)

I’ll sit on what you’ve said. There’s plenty I don’t know about what’s under the hood.

---

Somewhat of a side note. I may skip this “dynamic resource allocation” thing and use something closer to an EVM that is controlled by a ‘centralized network’* . Things will still be process 1 by 1. This would only be a stop gap measure until the “dynamic resource allocation” thing can be thoroughly figure out.

---

*centralized in a sense, because the DAO is theoretically supposed to make the network decentralized as far as ownership/control. but the network would have processing capabilities as if it were controlled by a single entity like an AWS or Azure network.

---

but yeah, I’m gonna have to sit on what you said about the  DoS vector. Because it definitely can’t be free, & compute speed on centralized machines is damn-near free.

---

**MicahZoltu** (2023-01-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/econymous/48/11192_2.png) Econymous:

> When you say Ethereum, you mean the EVM, correct?

No, I mean Ethereum.  Transaction management and validation occurs outside of the EVM.

There are alarm clock contracts out there where you can queue a CALL to be made after a certain point in time and anyone can trigger that call.  You could reward the executor to cover their gas costs plus some incentive.  One could do something similar where the call could be executed by anyone willing to pay a certain price, which means the transaction likely won’t be executed until gas prices drop below that value.

---

**Econymous** (2023-01-23):

yeah. I’m gonna have to sit on this for a minute.

Thank you. Very informative for me

