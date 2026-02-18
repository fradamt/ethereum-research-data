---
source: magicians
topic_id: 24556
title: ERC Non Economic Token Standard
author: sewing848
date: "2025-06-15"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/erc-non-economic-token-standard/24556
views: 96
likes: 4
posts_count: 3
---

# ERC Non Economic Token Standard

ERC-7974 is a proposed standard for **Non-Economic Tokens** (NETs) - fungible tokens designed to resist financialization and speculation.

The goal is to provide a token standard for use cases where traditional ERC-20 tokens create unwanted economic incentives. NETs are designed to be consumed or expire rather than accumulated as assets.

You can find the draft here: [Add ERC: Non-Economic Token by sewing848 · Pull Request #1088 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1088)

This ERC complements my recently proposed [Stateless Encrypted Communication Standard](https://ethereum-magicians.org/t/erc-stateless-encrypted-communication-standard).

A working prototype of a decentralized messaging application has informed the development of these ERCs, as I seek to improve the blockchain-based components of the system. In this particular context, the Non-Economic Token is meant to provide user control over incoming messaging channels, and the Stateless Encrypted Communication contract provides the mechanism for fast, inexpensive, encrypted communication.

The current prototype uses a conventional ERC-20 token for the mechanism that gives users control over incoming messages, but I am in the process of refactoring the code to incorporate this Non-Economic Token standard instead. The app is functional on macOS but not yet production-ready. (More info: https://www.pyrrhoproject.com)

Some of the features of the Non-Economic Token standard include:

- Built-in decay properties to simulate impermanence and reduce utility as a store of value
- Naming conventions that explicitly avoid financial semantics
- Interfaces and contracts without approve() or transferFrom() to prevent decentralized exchange listings
- Open or permissioned creation and distribution mechanisms not tied to payments or supply limits

While both ERCs are closely related within my project, they address distinct needs - one providing a standard protocol for encrypted communication, and the other a fungible resource that is clearly distinguishable in design, behavior, and intent, from financial blockchain assets. I have therefore created two discussion topics to allow for comments on each one separately.

All feedback and discussion points are welcome. I am particularly interested in thoughts on the decay mechanism implementation, potential circumvention scenarios, and how this might integrate with other applications beyond messaging.

Thanks for your input.

Scott

## Replies

**angrymouse** (2025-06-16):

I think the same can be achieved by just assigning inflationary properties to ERC20s. This is similar to how governments just increase monetary supply to make it a bad investment and ensure that money is consumed. Decaying properties might require iterating through owners and decreasing balances, or recomputing balances each transfer/balanceOf check, which isn’t efficient. Absence of approve() and transferFrom() might indeed prevent some listings, but it will also prevent “consuming” the tokens, I’m not sure if making it just simply unusable is a way to go when ensuring economic non-viability.

---

**sewing848** (2025-06-20):

Thank you [@angrymouse](/u/angrymouse) for taking the time to review the proposal and provide feedback. You raise some important points that I’d like to address.

## Inflation vs decay

While inflation does discourage hoarding, it operates differently from decay. Inflation dilutes value through supply expansion, but individual holdings remain nominally stable. Decay directly reduces holdings over time. Tokens literally disappear when unused. This better represents temporary permissions or time-sensitive signals than inflationary tokens, where old holdings persist indefinitely.

## Efficiency concerns

The proposed implementation uses lazy evaluation - decay is only calculated when `amountAt()` is called or during transfers, avoiding iteration through all holders. While this adds overhead compared to ERC-20, the gas cost is predictable and bounded.

## The absence of approve() and transferFrom()

This is deliberate. Applications can still receive NETs via direct `move()` calls. In my messaging app, for example, users send tokens directly to service contracts to open communication channels. No approval mechanics are needed. This design ensures NETs cannot be listed on DEXs or integrated with DeFi protocols.

## Whether a separate standard is needed

While one could modify ERC-20 to include these features, a distinct standard establishes a clear conceptual framework. Just as we distinguish between ERC-20 and ERC-721, distinguishing between economic and non-economic tokens at the standard level signals intent and purpose.

The proposal creates multiple independent barriers against financialization:

- No approve and/or transferFrom prevents exchange listings,
- A unique interface prevents confusion with financial tokens,
- Unlimited supply caps prevents scarcity value, and
- Decay discourages holding as investment.

NETs function as virtual substances - resources that exist and behave according to defined rules rather than arbitrary control. While transferable between addresses, they lack the characteristics that enable trading or investment. This creates space for blockchain applications requiring transferable units without the regulatory complexity and speculative dynamics inherent to financial tokens.

