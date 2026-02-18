---
source: ethresearch
topic_id: 12914
title: Use 1559 base fees to incentivize composability
author: madhavanmalolan
date: "2022-06-21"
category: Economics
tags: [fee-market]
url: https://ethresear.ch/t/use-1559-base-fees-to-incentivize-composability/12914
views: 2059
likes: 5
posts_count: 6
---

# Use 1559 base fees to incentivize composability

From what i understand, to make the system game theoretically sound, we must give the base fee to anyone but the miners.

I understand that burning the gas fees is the most neutral thing to do, and optimism uses the fees to do retro active funding of public goods - which i think is awesome.

I’ve been playing with the idea that we use the base fees and distribute it to the deployers of the contracts that were called in the block.

The premise for this is as follows

1. Ethereum gets a lot of value from dapp & contract developers, but not sharing the profits
2. It will create a huge incentive for people to build things that will be used by other contracts upstream. I.e. incentivize composability.

This is like retroactive funding but with no governance or human intervention.

Just-in-time public goods funding.

What would stop us from doing this?

## Replies

**Pandapip1** (2022-07-21):

I would like this proposal if it weren’t for two things:

1. It incentivizes developers to make their contracts as inefficient as possible.
2. How would one update the address?

(2) has a simple solution though: send the ETH to the contract instead of the deployer, and add a pull functionality.

---

**levs57** (2022-07-21):

I think for (1) if contract is inefficient, anyone could fork it and provide more efficient version?

---

**Pandapip1** (2022-07-21):

Yes, I suppose so. But it has a very large initial cost.

---

**MicahZoltu** (2022-07-22):

What is to stop users from just routing all of their transactions through their own contract to save money?  For example, I could use `MyCustomUniswapRouter` (which is just a copy of `UniswapRouter` but where I can withdraw ETH from it) so my calls are cheaper.

Alternatively, searchers could provide incentives to users who use their contracts as an entrypoint, effectively kicking back to the user.

---

**madhavanmalolan** (2022-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> searchers could provide incentives to users who use their contracts as an entrypoint, effectively kicking back to the user

I think this is a legit concern ![:white_check_mark:](https://ethresear.ch/images/emoji/facebook_messenger/white_check_mark.png?v=12)

Not just searchers - contract authors themselves could give the kickback to the user - and the user uses that kickback to just bid with more gas.

Though this is true, it would need non-trivial social coordination between the user and the contract author. I wonder if most dapp users will go this far.

Also, if you as the owner of the contract are willing to pass on the kickback, that should be perfectly fine imho.

I feel this is one of those experiments which we won’t know till we do it

