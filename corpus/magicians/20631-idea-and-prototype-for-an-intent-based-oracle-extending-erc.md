---
source: magicians
topic_id: 20631
title: Idea and Prototype for an Intent-based Oracle Extending ERC-4337
author: tomw1808
date: "2024-07-24"
category: Magicians > Primordial Soup
tags: [account-abstraction, erc-4337, oracles]
url: https://ethereum-magicians.org/t/idea-and-prototype-for-an-intent-based-oracle-extending-erc-4337/20631
views: 389
likes: 4
posts_count: 3
---

# Idea and Prototype for an Intent-based Oracle Extending ERC-4337

First time poster on Ethereum magicians, I hope I’m not overstepping here, if so, please let me know…

I’m looking for some early technical feedback on a new oracle solution my team and I are working on, or interested people who potentially want to give it a try.

We were working on a novel oracle solution that leverages ERC-4337 account abstraction to provide real-time on-chain price updates. Unlike traditional pull or push-based oracles, our approach uses an intent system leveraging and extending the already existing infrastructure for erc4337 account abstraction.

Something like this:

[![SCR-20240724-kgpt](https://ethereum-magicians.org/uploads/default/optimized/2X/6/655c1798e1a56badfe68a10060e4e3659781d9f1_2_690x316.jpeg)SCR-20240724-kgpt1920×880 118 KB](https://ethereum-magicians.org/uploads/default/655c1798e1a56badfe68a10060e4e3659781d9f1)

The idea we had was to run a slightly modified erc4337 bundler that listens to a new kind of UserOp, or wraps the actual UserOp in a DataRequestOp and injects updated (price/…/?) information before submitting the actual transaction. From a data-consuming contract perspective, it would be usable very much like a push oracle, just like manually triggering an update before read and would basically ensure accurate and up-to-date data being on chain before a contract reads it. On the other end, the bundler (or whoever is providing data) gets compensated for its services through the same mechanism that erc4337 already uses. So, it would create an additional economic incentive to run a bundler.

We got a prototype for a single bundler and the whole process running on sepolia. It’s of course not decentralized and the end vision is a decentralized network of bundlers or something like aggregated signatures of several bundlers and an open protocol to let anyone run a bundler+dataprovider and potentially a reputation dashboard of some sort.

Anyways, that’s the idea in a nutshell. Thoughts, concerns? Any projects that work on a tangential system and want to collaborate? Anyone who needs access to real time US Equities, Commodities or Forex and want to give it a try? Anyone who is currently running Bundlers and would be interested in implementing it - or spearhead an ERC together?

Thanks,

Thomas

## Replies

**0xTraub** (2024-07-28):

Welcome to the forums. Definitely not overstepping. Always nice to see people bringing original ideas up for debate. It’s an interesting idea for sure. There’s definitely a lot of room for improvements to the AA-stack with 4337. I have some questions, several of which may be answered with more implementation details.

1. What does the workflow for a UserOp express an intent to have a DataRequestOp filled?
2. How does the UserOp ensure that the DataRequestOp is filled within the same bundled ERC-4337 transaction?
3. How can the UserOp ensure that the DataRequestOp is filled by a trusted party or that the data is itself trustworthy?
4. Can a second UserOp “piggy-back” off of the data provided by another UserOp requesting the same data? (I.E two UserOps wanting the same price feed information)?
5. What’s the benefit of adding the complexity of an entirely separate User Op instead of using an existing pull-based oracle and attaching it as data to a user-op (e.g. chainlink data streams)

---

**tomw1808** (2024-07-29):

Hi  [@0xTraub](/u/0xtraub) ,

great questions, let me try and answer them:

Regarding 1. 2.) We’re actually wrapping the UserOp into another type of operation, a DataRequestOp. So, the bundler prototype we created [1] is actually an extension to the current bundler. It takes in a DataRequestOp, runs through the wrapped UserOp to ensure the bundler gets paid for the Data provision (and of course also for the normal bundler operation), then injects another UserOp towards the Entrypoint and sends out both within the same transaction. The UserOp itself should error out if the timestamp in the oracle contract - when reading the data - is anything but the block.timestamp. It’s up to the user to allow a certain wiggle room here, but since both UserOps (one for updating the oracle data and another that actually calls then whatever needs to be called from the UserOp) is in the same TX, the block timestamp should be the same, so it would make sense to restrict it to that. So, in short, its up to the user.

Regarding 4. and 5.) Before answering that question, I want to take a step back here. The problem with a lot of data, but especially financial data, is licensing and data rights. We’re battling quite a bit for our own data feeds to have display rights for our charts and our users (at Morpher, the company I work for). Standard display right licenses don’t even usually include redistribution rights. Getting something like a UDP or a consolidated SIP feed with display and redistribution rights does not come cheap. And the negotiation and setup to get access to this data isn’t straight forward neither, so the barrier of entry is quite high. Another problem with current Push oracles is the delay, I know before the oracle will update - for a great enough certainty - the price of the update and when the update will be. Pull Oracles usually have a lower delay (however, I did get a measurable delay in seconds, long enough that something like high leverage perp markets with the feeds is unfeasible), but then its usually just the attestation service you pay for, not for the data, so you get the data before you actually paid anything at all, it becomes a hard sell to data vendors. E.g. You can hook into Pyth network today and get the price for any feed, if you want the attestation it will cost you something (AFAIK 1 wei currently, subject to change in a future governance if I am not mistaken). One thing that our architecture solves is that someone in possession of data can be *certain* that a payment happened before the data is distributed. Looking at large exchanges or large data vendors, it opens up a huge new market opportunity. Looking at 2nd level distributors, its easy to add in another stream of income through providing data if you want. So, that’s kind-of the angle we’re coming from with the solution, mostly a rights/delay fix to get high quality data on-chain, so that something like delay based arbitrage becomes impossible. Piggy backing off another userOp is both possible and impossible, we haven’t decided on an architecture yet. In the current incarnation of the prototype its impossible, because the data is written for a target contract only into the oracle contract, so reading out the data is only possible for the contract that requested the data in the first place. Changing this is trivial, from an architecture point of view. I think its something we decide on once we have data vendors onboard for a trial phase to run a bundler including something I would call somehow authoritative data provider - where users get the data directly from the source ideally.

Which brings me to 3) The trust problem. And that is something we’re currently looking into and something we’re actively researching. There are a few ideas floating around. One is, you have different data providers with different lists of data which have a certain reputation for providing data. That is then either something like a (on-chain, decentralized?) reputation dashboard, or registry of some sort, where you say “I want the current price of Nasdaq:AAPL” and it spits out a list of urls for bundlers who have a stake/proven track record/reputation score/price/… Another idea is to make it an on-chain aggregate of signatures, something like a BLS aggregation signature scheme where a data point is requested with at least X off-chain attestations from Y data providers and it only passes the oracle update if all the signatures are valid. Problem here is the delay, which we would like to keep well under 1 second at all times.

Lots of text, I still hope I could answer a few things. We’re currently working on a demo that will probably make it all a bit more accessible - always better to have something to play around with…

Thomas

[1] [GitHub - Morpher-io/dd-voltaire: Modular and lighting-fast Python Bundler for Ethereum EIP-4337 Account Abstraction, modded to support oracle data injection](https://github.com/Morpher-io/dd-voltaire) and the new endpoint would be this one: [dd-voltaire/voltaire_bundler/rpc/rpc_http_server.py at dc57add61bffaa0e9532aa494dbb5952df474e00 · Morpher-io/dd-voltaire · GitHub](https://github.com/Morpher-io/dd-voltaire/blob/dc57add61bffaa0e9532aa494dbb5952df474e00/voltaire_bundler/rpc/rpc_http_server.py#L141)

