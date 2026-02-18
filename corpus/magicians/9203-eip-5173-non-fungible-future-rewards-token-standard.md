---
source: magicians
topic_id: 9203
title: "EIP-5173: Non-fungible Future Rewards Token Standard"
author: ReiSoleil
date: "2022-05-08"
category: EIPs
tags: [nft, token, onchain-payment, gift-economy, giving-circle]
url: https://ethereum-magicians.org/t/eip-5173-non-fungible-future-rewards-token-standard/9203
views: 3370
likes: 5
posts_count: 15
---

# EIP-5173: Non-fungible Future Rewards Token Standard

eip: 5173

title: NFT Future Rewards (nFR) Standard

description: A multigenerational reward mechanism that rewards‌ all ‌owners of non-fungible tokens (NFT).

author: Yale ReiSoleil [yale@iob.fi](mailto:yale@iob.fi), dRadiant (@dRadiant), D Wang, PhD [david@iob.fi](mailto:david@iob.fi)

discussions-to: [EIP-5173: Non-fungible Future Rewards Token Standard](https://ethereum-magicians.org/t/non-fungible-future-rewards-token-standard/9203)

type: Standards Track

category: ERC

status: Draft

created: 2022-05-08

requires: 165, 721

## Abstract

This proposal introduces the Non-Fungible Future Rewards (nFR) framework, extending [ERC-721](https://github.com/untrading/ERCs/blob/master/ERCS/eip-721.md) tokens (NFTs) features to let token holders benefit from value appreciation after transferring ownership. By integrating cooperative game theory, it aligns stakeholder incentives, addressing inefficiencies in asset transactions. The framework fosters collaboration, transparency, and equitable profit sharing. It improves equity and efficiency, recognizes all ownership stages, and establishes a cooperative asset transaction model.

## Motivation

Traditional financial markets are often characterized by inefficiencies, opaque practices, and systemic imbalances, resulting in significant disadvantages for the majority of participants. Although blockchain technology offers transaction transparency, current implementations do not adequately facilitate equitable value sharing or participant alignment. This proposal addresses these gaps by introducing structured collaboration and a fair compensation system, ensuring equitable rewards for contributions to asset value.

### Framework Components

#### The Flow mechanism

Each EIP-5173 token maintains an immutable record of ownership and price transitions, creating a dedicated network of historical token owners. This unique community collaborates to generate additional value and maintains vested interest in the project or token even after selling, ensuring contributors benefit from the asset’s appreciation. This mechanism promotes collaborative value creation, equitable profit sharing, and a connected financial ecosystem, distinct from traditional financial market systems.

#### Cooperative Value (Future Rewards) Distribution

The nFR framework transforms the zero-sum financial equation:

```auto
P(A) + P(B) + F ≤ 0
```

Where:

- P(A): Profit of trader A
- P(B): Profit of trader B
- F: Transaction fees, friction costs, and operational expenses

into a collaborative model:

```auto
P(A) + P(B) + F + FR > 0
```

Where:

- FR: Shared value creation through cooperative mechanisms

This model incentivizes fairness and rewards contributions throughout the asset lifecycle.

https://github.com/dRadiant/EIPs/blob/master/EIPS/eip-5173.md

[Implementation](https://github.com/dRadiant/EIPs/tree/master/assets/eip-5173/Implementation)

## Replies

**ReiSoleil** (2022-05-09):

Friends warned me that nobody was talking about compensating buyers/owners. So this is not a popular topic. The traditional practice is to reward the creators. And that’s exactly the point, isn’t it? To reward those who contributed to the price discovery process as well.

---

**ReiSoleil** (2022-05-12):

The word “Ponzi” is being discussed a lot on Twitter these days. Someone asked me, “doesn’t your future rewards sound like a pyramid scheme?”?

Not at all. A Ponzi scheme is a scheme that promises a constant, high-yield return that is unpredictable and cannot be guaranteed. Our reward system is based on the realization of profit sharing that rewards people for participating in the early stage of price discovery, and being rewarded by future price gains for performing the same function.

Before we make the PR on GitHub, I would appreciate more discussion, questions, and suggestions.

Thank you!

---

**ReiSoleil** (2022-06-21):

PR made. Please comment. Thanks!

---

**ReiSoleil** (2022-06-22):

There aren’t many people “interested” in this topic. Maybe it’s too alien to a lot of people.

If you’ve been doing some trading, you know that markets are designed to transfer wealth from the masses to the rich:

- The exchange that charges transaction fees is acting in its own interest first, and at the expense of its users;
- Exchange rules are designed to maximize profits;
- Most traders lose money in the long run;
- A 3% commission DeFi model shows the same old greed.

That needs to change:

- Everyone’s on the same page with a success-based model;
- Exchanges only get paid when users make money;
- Both buyers and sellers benefit from rules;
- Traders are encouraged to do the right thing instead of “buying, selling, and buying”;
- It’s finally possible thanks to new technology.

We’re building a new trading/investing platform based on this EIP.

In its current format, trading started in Europe several hundred years ago and was designed to rip off its users. 90% of them lost money.

Our goal is to create a new platform where both the exchange and its users have the same interests.

Join us for the discussion.

---

**ReiSoleil** (2022-07-08):

Through the implementation of EIP-5173, the creators, buyers and sellers create a giving circle in trading practice. A giving circle is formed when all participants work in a framework to build greater wealth through each other’s success. One does not expect the same amount of return from the same person when they give someone a portion of their profits. There is no quid pro quo. Rather, they are confident that someone else in the same circle will give them the same benefits, with a smaller or greater monetary value, from other participants in the same circle later on.

Giving circles are groups of people who work together to improve a situation that is typically much larger than it is at the moment. Some of the characteristics of a giving circle are community interdependence and delayed reciprocity.

We embrace and promote a new gift economic model, which is similar to the Copyleft and open-source spirit as opposed to traditional copyrights. The advancement of technology has enabled such implementation in trading for the first time.

As In trading, most traders lose money, but the proposed Future Rewards framework is designed to help average traders do better.

---

**ReiSoleil** (2022-07-13):

Trading is designed in such a way that only the platforms and a few insiders benefit.

Our goal is to inspire more developers to work together to develop on-chain royalty payment methods, and with the implementation of future rewards, build a win-win trading practice based on Ethereum.

This EIP is aimed at building a gift economic model where members pay it forward to end centuries of zero-sum trading.

---

**unicorn** (2022-08-08):

Amazing proposal, I would like to ask a couple of questions.

Does EIP5173 open the door for building a better price discovery mechanism (when compared with bonding curves) in token launches?

Also, by creating a “gift” economy that accounts for both profits and FRs (for any asset that can be tokenized and wrapped), it creates a “hyperstructure relation” between users.

My second question then is, if you have any comments about new design surfaces for governance/tokenomics when 5173 NFTs represent Treasuries.

Thanks

---

**ReiSoleil** (2022-08-08):

Several key features of this EIP were touched upon. The FR distribution giving circle makes the community more cohesive, akin to what you call a “hyperstructural relationship.”

However, this EIP is not directly related to the price or supply. But it is having a similar effect on the community’s bonding. It allows all members to create value together, which we call ‘a giving circle.’ The early buyers may have a slight upside advantage, but all subsequent buyers can benefit from a cascading profit dynamic.

The EIP-5179 tool is one of a series of tools needed to enhance the functionality of ERC721-based trading. You’re not the only one noticing a certain similarity between it and the bonding curve design ([@anett](/u/anett) beat you to it! ;-)). I like the general idea of the bonding curve, but at the interface level, EIP-5173 is designed around the idea of a chain of ownership among the users, which has some fundamental incompatibility with the bonding curve every time there is a new “buy” order that results in a new token insurance.

If you have any suggestions or new ideas to incorporate the bonding curve into this, I would appreciate hearing from you.

As for your second question, obviously it can be used for NFTs, but there are many other applications as well. Once the platform building is complete, we plan to release several other EIPs. One of its advantages is that it fosters a strong community. As of now, many people abandon a project/community once they sell their tokens. With EIP-5173, however, their interest will remain personal. Future Rewards will continue to be paid to them forever. This rotating benefit is enjoyed by everyone.

Moreover, team token offerings can use this mechanism to create an equitable token structure, in which investors own the entire tradable tokens, whereas team members own only the non-tradable o-token (o for originators). Team members receive their income after investors make profits.

As long as the terms of the treasure holding are clear and fair to all investors (such as restricted trading or a time lock), teams can designate some EIP-5173 tokens as treasure holdings. By removing the rug-pulling in cryptos, inequality would be greatly reduced, insider trading would be reduced, and common interests would be aligned.

---

**ReiSoleil** (2023-01-04):

[untrading.org](http://untrading.org) is implementing EIP-5173 to launch a brand-new NFT investment protocol. Its first corporate client will launch its NFT membership program for crypto debit cards and gift cards.

---

**ReiSoleil** (2023-01-04):

# What problem does EIP-5173 solve?

## There is an inherited problem with trading.

One of the biggest problems with trading is trading. Yes, trading itself.

When you trade, you’re playing another person’s game. What happens when you play other people’s games? You’ve got no control. Those in positions of power and influence and… a highly disciplined few, they are the ones who win. Not you. The majority of market participants, casual traders like most of you, are just losers, by design.

It’s likely that Jesse Livermore is the most successful trader in history. But what happened to him in the end? He had to kill himself. The guy who made billions in today’s dollars from trading was unhappy.

## So what’s the problem here?

Traders are forced to operate under a zero-sum mentality. One person’s gain is another’s loss. This can lead to traders being driven by greed and fear constantly when making decisions. A nervous wreck. The result is losing. You know most traders lose everything within 6 to 24 months.

Exchanges are often structured in a way that their function is to transfer wealth from the majority to a small group of winners. It gets worse. There are times when exchanges themselves do unethical or even illegal things against their customers. Platforms are built on conflicts of interest.

### It’s time for a change.

EIP-5173 proposes a revolutionary asset transaction protocol based on gift economy principles to change this dynamic.

Each non-fungible token, or NFT, creates a Giftchain using a protocol based on EIP-5173 we proposed last year.

EIP-5173, a new process of wealth creation, ensures that one person’s success does not hurt another, but rather benefits the entire society. The result is: No more zero-sum trading; no more conflict of interest, and more for you is also more for me. And there is the ability to capture part of the future growth weeks, months, or even years after you sell your token.

By implementing EiP-5173, untrading changes the relationship between creators, buyers and sellers entirely. No more your win is my loss as all users create more value together.

---

**ReiSoleil** (2023-01-10):

As a result of implementing EIP-5173, a new project has been launched called [untrading.org](http://untrading.org).

---

**ReiSoleil** (2024-12-23):

Updated.

An advanced calculator based on this proposal is available at:

https://5173.foundation/

And an implementation demo:

https://demo.untrading.org/

---

**theBigRevolution** (2024-12-24):

Nice implementation and nice explanation too… Good work

---

**Arvolear** (2024-12-26):

Maybe it is a bit of a wild idea, but can the distribution function be expanded with some variable `T` that indicates how long a user has owned an NFT? Then, it would be possible to calculate the overall “hold time” of an NFT through the owners and proportionally adjust the rewards. Won’t such a mechanism be more fair in terms of the NFT value contribution?

