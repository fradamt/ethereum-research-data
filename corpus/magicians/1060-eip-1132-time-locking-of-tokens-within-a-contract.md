---
source: magicians
topic_id: 1060
title: EIP-1132 - Time-locking of tokens within a contract
author: krakjack
date: "2018-08-14"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1132-time-locking-of-tokens-within-a-contract/1060
views: 1766
likes: 0
posts_count: 2
---

# EIP-1132 - Time-locking of tokens within a contract

My colleague at GovBlocks, Nitika, recently authored an EIP. Thought I’d share it here and get feedback from the community. For context, I’ve pasted the abstract below:

> This proposal provides basic functionality to time-lock tokens within a contract for multiple utilities without the need of transferring tokens. It also allows fetching token balances of locked and unlocked tokens (tokens available for transfer).
>
>
> Time-locking can also be achieved via staking (#900), but that requires transfer of tokens to an escrow contract/stake manager, resulting in the following five concerns:
>
>
> additional trust on escrow contract/stake manager
> additional approval process for token transfer
> increased ops costs due to gas requirements in transfers
> tough user experience as the user needs to claim the amount back from escrow
> inability for the user to track his true token balance / token activity

Link to the EIP - [Extending ERC20 with token locking capability · Issue #1132 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1132)

## Replies

**krakjack** (2018-08-21):

[Update]

The issue has been merged into master ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)


      [github.com](https://github.com/nitika-goel/EIPs/blob/master/EIPS/eip-1132.md)




####

```md
---
eip: 1132
title: Extending ERC20 with token locking capability
author: nitika-goel
type: Standards Track
category: ERC
status: Draft
created: 2018-06-03
discussions-to: https://github.com/ethereum/EIPs/issues/1132
---

## Simple Summary

An extension to the ERC20 standard with methods for time-locking of tokens within a contract.

## Abstract

This proposal provides basic functionality to time-lock tokens within an ERC20 smart contract for multiple utilities without the need of transferring tokens to an external escrow smart contract.  It also allows fetching balance of locked and transferable tokens.

Time-locking can also be achieved via staking (#900), but that requires transfer of tokens to an escrow contract / stake manager, resulting in the following six concerns:
```

  This file has been truncated. [show original](https://github.com/nitika-goel/EIPs/blob/master/EIPS/eip-1132.md)

