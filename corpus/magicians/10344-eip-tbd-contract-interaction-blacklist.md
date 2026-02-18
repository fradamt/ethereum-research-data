---
source: magicians
topic_id: 10344
title: EIP:tbd - contract interaction blacklist
author: DenverCitizen9
date: "2022-08-12"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-tbd-contract-interaction-blacklist/10344
views: 540
likes: 1
posts_count: 3
---

# EIP:tbd - contract interaction blacklist

I was talking to a friend about this and promised to look into it.  Neither of us have submitted an EIP before so I wanted to go through the process and see if this was something that made sense.

While I support a free and open internet, there may be cases where someone would want to intentionally prevent unintended interactions with a known blacklisted entity, such as with OFAC sanctioned addresses.

In short, we would like to define a standard for preventing a list of addresses from interactions (to or from). The idea is that this would be an easily implementable pattern that would also be update-able by a third party who would manage the list.  I suspect we would have “local” lists that were essentially user controlled, as well ad more global lists that could be managed by a single/shared entity.

We have some ideas for how this could be implemented, and are looking to get feedback from the community about the concept, as well as support moving forward if it does make sense as an EIP.

## Replies

**DenverCitizen9** (2022-08-12):

Another way to think about this, is if the OFAC list could be easily implemented, then sanctions against a DEX make less sense.

The dex was not the problem, the people that used the DEX were, but they clearly did not feel like they had any other choice but to prohibit the use of those addresses.

---

**ronaldjmaas** (2022-09-18):

On Aug 15 Eric X posted a poll about considering censorship as an attack on Ethereum. And 61.2% voted to slash any stakers who complied with sanctions. Although this poll is kind of a joke (at least I sincerely hope so), I do think as a community we should put some thought and nuance about how to deal with sanctions in the future.

So I hope we can all agree on the principle that any entity (which could be individuals running a home based node or a big organization like Binance & friends) should be able to operate staking nodes within the bounds of applicable laws and this without incurring an  unreasonable financial loss. Just to clarify, a loss of a mere pennies caused by not including a sanctioned transaction in a proposed block, or by not attesting to a block that contains one or more sanctioned transactions is reasonable. Slashing a node or forcing a node to exit is unreasonable.

Now based on that a few interesting questions:

1. What changes are required in EL / CL clients to allow any staker (large or small) to easily adhere with sanctions? A blacklist of Ethereum addresses is relatively easy to implement and manage from an implementation point of view. But satisfying reporting and / or identifying parties associated with each Ethereum address (KYC) are simply not possible / not practical with Ethereum.
2. Are there ways to make Ethereum sanction resistant in such a way that even a minority of unsanctioned nodes are sufficient to execute all transactions eventually, regardless if these are sanctions by some countries or not? And do we want this as there may be risks involved with such a move?
3. Anyhting else that may be relevant?

