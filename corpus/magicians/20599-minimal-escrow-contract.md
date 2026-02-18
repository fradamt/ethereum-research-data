---
source: magicians
topic_id: 20599
title: Minimal escrow contract?
author: MidnightLightning
date: "2024-07-19"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/minimal-escrow-contract/20599
views: 316
likes: 1
posts_count: 2
---

# Minimal escrow contract?

I’m in the process of searching for possible solutions to a need I think many DAOs/teams/groups have: the ability to provably have a reward/bounty on some action, and have others be able to contribute to it.

Many groups have “task lists” that they can set up with items they want accomplished. Tools like [Dework](https://dework.xyz/) or [CharmVerse](https://charmverse.io/) already exist to have cryptocurrency bounties put on the tasks. However, in both those tools the bounty is not verified/guaranteed. Visitors need to trust the group organizers to properly pay out when the task is complete, and also have to do their independent verification of whether the organizers actually have those funds to pay out (if there’s five tasks posted and each has a reward of 5 ETH, is there really enough in the treasury to pay all them out? Sorting the list of [all Dework bounties](https://app.dework.xyz/bounties) by largest reward, I’m really skeptical the top listings would actually pay out…). Because systems like that rely on trust of the organizers, it’s hard to have other community members contribute to the bounty.

I think if there were a lightweight way for community members to pool financial incentives, it would take some of the weight off the community organizers to manage. **The goal is to have a list of tasks that are given rewards by many people contributing a little (grassroots-style, Kickstarter-style), rather than a single sponsor giving a grant (organizers figuring out rewards from community funds).** Being able to do that in a provable way (the funds are put in escrow on-chain in an easily-inspect-able way) would encourage people to apply to do the task, and I think getting community involvement in bounty-funding is helpful because the financial reward intrinsically scales with how popular an item is to be implemented.

There’s still a level of trust placed in the organizing group to do the reviews of task submissions and fairly trigger the payouts, but I think that’s an acceptable level of trust needed, given the current systems require that too. A more advanced setup could include the ability for a global governance group like [Kleros Court](https://kleros.io/governance) to allow end-users to appeal if the organizing group turns unresponsive.

[Bountysource](https://twitter.com/Bountysource) had a system like this, but seems to have gone stagnant. Any other platform already done this?

My thoughts on how to make a platform to support this functionality:

# Individual Lockboxes

Create a smart contract that is a factory that group organizers can trigger to stamp out a new “lockbox/escrow” contract.

The lockbox contract acts as a smart contract wallet that starts with an owner of the address that triggered its creation. It then exists as a separate space that anyone can send funds to (it’s now the “reward wallet” for a single task item). When someone does the task, the organizer transfers ownership to the awardee.

Example implementation: [Basic Escrow ($3733032) · Snippets · GitLab](https://gitlab.com/-/snippets/3733032)

## Downsides

Assuming that groups/projects generate lots of tasks, but only a few get elevated to have bounties, the group organizers probably don’t want to create a lockbox for every single task (as that costs gas to stamp out another smart contract, just for it to not get used), so either the address the lockbox gets created at needs to be deterministic (community members can send funds to an “empty” address to show interest, and if the wallet’s balance is non-empty, the organizers can trigger deploying the smart contract logic to it), or the first community member to donate to the bounty has an increased cost of creating the lockbox too.

People are likely to donate lots of different types of tokens (a single bounty may end up with a mishmash of DAI, USDT, USDC, FRAX, WETH, and ETH), so “sweeping” the wallet may be pretty gas-intensive. It may be beneficial then for the recipient to just keep the funds where they are, and spend from that wallet directly. Though if a single contributor wins several bounties, they’d then have multiple of these lockboxes, with potentially multiple different “dust” values in each to then try to manage.

# Merged Pool

Alternatively, rewards could be pooled into one main “pot” and the individual bounties annotated as how much allocation they get of the main pot.

This is pretty similar to a DAO’s treasury and how Proposals can typically claim portions of the treasury. But a DAO would likely want to keep “bounty” funds separate from their main treasury (as a way to show those funds are earmarked/promised to be spent already, and cannot be used for other proposals).

This is now easier on the recipient, who if they receive multiple bounties, their “dust” combines into a single allowance to be able to withdraw. It also minimizes the gas use for repeated actions (there’s just an initial setup cost of creating the pool, and setting up allowances).

## Downsides

Having a central pool means it’s a little more complicated for end-users to contribute: they cannot just send funds to the address, they need to also somehow annotate which bounty the contribution is for. That likely means they’d need to use the “Approve” process for ERC20- and ERC721-style tokens and call specific functions on the pool contract to do it properly. But it’s possible for users to make mistakes, and some funds may get blindly transferred to the pool address, making the total holdings of the pool larger than the combined allocations for the individual bounties.

The pool could be coded to deal with that surplus somehow (e.g. it acts as a form of “quadratic funding” extra balance that bounties that already have some value allocated then get an additional part of the “bonus” in the pool?), but would likely add a lot of complication to the process.

Having the funds in a central pool is more of a honeypot to draw in attackers, and one weakness could result in losing the whole pot of funds. That can be mitigated somewhat by not having a single global bounty pool, but each organizing group having their own individual pool for their bounties.

# Next steps

Is there any project that’s already doing this sort of escrow setup? If not, what do we think is the best way to structure the base layer (individual smart contract lockboxes, or centralized bounty pools)?

## Replies

**MidnightLightning** (2024-07-26):

Additional project I found that’s related to this idea: [Bountycaster](https://www.bountycaster.xyz/) operates on Warpcast as an automated bot that parses conversations its mentioned in. This helps in advertising the bounties, but doesn’t allow for others to contribute to a bounty that was started by someone else (if you start a bounty, you do get editing rights to change the interpreted value of the bounty in the Bountycaster interface).

