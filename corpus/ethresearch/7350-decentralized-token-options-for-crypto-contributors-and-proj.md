---
source: ethresearch
topic_id: 7350
title: Decentralized Token Options for Crypto Contributors and Projects
author: bvl
date: "2020-05-04"
category: Applications
tags: []
url: https://ethresear.ch/t/decentralized-token-options-for-crypto-contributors-and-projects/7350
views: 1223
likes: 1
posts_count: 2
---

# Decentralized Token Options for Crypto Contributors and Projects

We can see a lot of DeFi projects working on more generic options and futures projects, such as Opyn, Hegic, and Nexus. While these projects work on the trading aspect of decentralised derivatives, I can’t seem to find projects that more specifically concentrate on providing a simple decentralised service for protocol contributors.

Any “hot” open source project in the crypto space usually attracts a lot of open source contributors. Many of these contributors simply want to help, some might want to do bounties through Gitcoin. A fraction actually get an offer from the foundation / company. The foundations usually allocate part of their tokens to incentivise development (something like 30%).

The Problem:

While the protocol might be fully decentralised and open source, the foundation is usually tied to a local jurisdiction, such as in Switzerland, Estonia, BVI or Cayman Islands. In this sense, a globally accessible decentralised protocol still has to rely on local pen and paper contracts to enforce vesting schedules (1-year cliffs, strike prices and exercise periods). I’m interested in how much great talent outside of EU might be fearful of signing options contracts that are tied to foreign jurisdictions?

Solution:

Create a simple interface and smart contract logic on top of Ethereum where each ERC20 token project can let their contributors receive and exercise token options in a provably secure and transparent way. While the jurisdiction papers might have a reference to the smart contract and the counterparties, the smart contract will be setup in a way where it has on-chain vesting schedules, strike prices and exercising options. This might even produce a very flexible model where “micro-options” can be granted to promising developers that the foundation / project doesn’t want to hire yet:

1. contributor gets extra motivation and can trust that the locked token options are theirs (within vesting rules)
2. project ensures the contributor stays motivated even without getting paid initially

Example:

1. Alice is a contributor, Bob is a token project
2. Bob’s token T has 30mil tokens allocated for the foundation
3. Bob sees that Alice is contributing to the project intensively and wants to make sure Alice is motivated
4. Bob wants to allocate 10k T tokens to Alice at a strike price that’s defined by the foundation and locks it in the contract for 4 years with a 1 year cliff at strike price X nominated in DAI
5. 1.5 years go by and Alice wants to jump into a new project. Alice buys DAI or exchanges their other tokens to DAI and gets to exercise their token T at a rate that should be way under the price of the token at that given time in the optimistic scenario. They can now choose to sell that token on an open market or HODL.

I’m curious whether this would be a useful way to motivate more people in the Ethereum project and the broader DeFi space?

## Replies

**alexander** (2020-05-26):

This is one area I am working on and this is a problem that would be solved by a permissionless instrument designed to match the specification of an option.

So far, what are some current ways to allocate a `foundation` token over time to a contributor? The first that comes into mind would be a money stream. Maybe that stream could be customized with a 1-year cliff.

A token option that you describe here would need to have these properties:

(1) An exercise window (1-year cliff, 4 years after that until the strike date)

(2) A way for the holder (Alice) to purchase the underlying tokens T within the exercise window

Do we want this option to be transferable?

Assuming we want the token T to be received by Alice, a party we want invested in the project, we most likely don’t want it to be accumulated by another party.

Will the foundation have control over the option?

You say (within vesting rules), so would these powers over the option come with limitations?

I’d want the option to be handled in the most permissionless way possible, but I concede that could be left to the ultimate issuer, the foundation.

I’m trying to get a sense of the properties you desire for this option.

This is all very exciting, would love to hear more from you!

