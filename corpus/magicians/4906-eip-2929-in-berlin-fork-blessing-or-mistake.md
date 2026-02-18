---
source: magicians
topic_id: 4906
title: EIP-2929 in Berlin fork blessing or mistake?
author: kladkogex
date: "2020-11-03"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-2929-in-berlin-fork-blessing-or-mistake/4906
views: 1007
likes: 9
posts_count: 7
---

# EIP-2929 in Berlin fork blessing or mistake?

I think EIP-2929 is going to affect many DeFi apps that were designed under the assumption that gas fees were set in stone.

This will make dapps that access lots of memory during a transaction impossible to implement.

Changing gas fees after the fact is a questionable practice in IMO.   There are zillions of ways to innovate to make things fast without affecting the users.

This is especially true for SLOAD operation since it does not change the state.

One could think about progressively complex and efficient ways of caching that would improve things.

I think before adopting EIP-2929 Ethereum Foundation should explore issuing bounty to people that improve the current SLOAD implementation.

## Replies

**timbeiko** (2020-11-10):

[@kladkogex](/u/kladkogex) have you reviewed [EIP-2930](https://eips.ethereum.org/EIPS/eip-2930)? It is meant as a mitigation for the breakage from 2929.

---

**esaulpaugh** (2020-11-16):

gas fees will be set in stone when hardware and software can no longer be optimized. so any century now…

gas prices need to change with every hard fork until people understand how ethereum works

---

**matt** (2020-11-16):

[@kladkogex](/u/kladkogex) do you have any concrete examples of this? It has been considered bad practice for quite a while now to expect that gas fees are set in stone.

---

**kladkogex** (2021-01-13):

Tim - definitely I think EIP-2930 is a good thing.

We are lucky at SKALE that our contracts are still upgradeable, so we will be able to mitigate this.

Projects invest money in software engineering and audits and optimize algorithms having specific gas fees. When gas fees change projects need to invest money to optimize algorithms in a different way and then do audits again.

We at SKALE feel very pissed because it affects our engineering schedule.

The root cause of the problem that the decisions are made in non-transparent way, community has no way to comment/vote in a way that the comments are heard.  The decision to change gas fee should have been made at least 6 months in advance and voted upon.

The core ETH dev team does not treat the rest of the community as customers.

I believe EIP-1559 follows pretty much the same pattern of making sudden non-transparent decisions and there will be much more discontent because miners will lose lots of money.  I personally think the decision to burn gas fees is wrong.  Many other people think the same, they have no way to vote or affect things.

We did not even evaluate EIP-1559 at SKALE. If will definitely greatly affect our product and force us to re-engineer things. We need time to engineer and QA this.

The way ETH is governed is against the idea of blockchain and decentralization. It is a simulation of democracy.

I believe this increases the hidden conflict where many people are unhappy, especially having that many other projects have great governance and vote.

---

**matt** (2021-01-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> Projects invest money in software engineering and audits and optimize algorithms having specific gas fees

We have asked developers for a long time to not write contracts that depend on specific gas schedules, as they are subject to change.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> The root cause of the problem that the decisions are made in non-transparent way, community has no way to comment/vote in a way that the comments are heard. The decision to change gas fee should have been made at least 6 months in advance and voted upon.

This EIP was authored 01/09/2020 and was first discussed in the All Core Devs call 04/09/2020. It’s inclusion has been transparent since it was authored. The ACD call is open to the public and you are more than welcome to join it and share your thoughts on how Ethereum should progress.

---

**CryptoBlockchainTech** (2021-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kladkogex/48/8349_2.png) kladkogex:

> I believe EIP-1559 follows pretty much the same pattern of making sudden non-transparent decisions and there will be much more discontent because miners will lose lots of money. I personally think the decision to burn gas fees is wrong. Many other people think the same, they have no way to vote or affect things.

As a miner we agree 100%. Just watch what happens over the next few months as we mobilize thousands of miners to oppose 1559. It will never leave the testnet if the devs don’t start working with the mining community to come up with a compromise.

Miners are are able to vote, we can make or break hard forks.

