---
source: magicians
topic_id: 2166
title: "[WhiSpeG] - Follow-Up: Kick-off call on 06.Dec.2018"
author: Ethernian
date: "2018-12-08"
category: Working Groups > Ethereum Architects
tags: [whisper]
url: https://ethereum-magicians.org/t/whispeg-follow-up-kick-off-call-on-06-dec-2018/2166
views: 1136
likes: 0
posts_count: 1
---

# [WhiSpeG] - Follow-Up: Kick-off call on 06.Dec.2018

## Call Summary

[Here is the Work-in-Progress version of the Summary](https://hackmd.io/bCZTqFlbSuq_XDVpqjmqAg).

All Call participants are invited to extend and correct it!

#### Participants

There were clearly two groups of people in the call: Solution Developers and Core Developers.

*SolutionDevs* are using Whisper and Whisper-Clients in their solution for corporate customers.

*CoreDevs* are developing technology (both protocol an client).

Most of communication in the call was between these two groups.

#### Chatham House Rules

I would ask all participants to apply [Chatham House Rule](https://www.chathamhouse.org/chatham-house-rule) to all *WhiSpeG* meetings. This is in respect to all Whisper Devs, who would not like to be exposed in public too  much.

## Discussed Topics

### 1. Specification

*CoreDevs:*

Considering current state of specification as quite solid.

If SolutionDevs need better specs, they should create a PR or an Issues on specs. What is not good enough exactly?

More resources (technnical writers) to improve Specs would be appreciated.

*SolutionDevs:*

What is the current official specs that being maintained? Unclear.

It would be nice to have a spec of a quality of a good IETF level.

Looks like we are missing single source of true for Whisper spec.

### 2. Testnet

*SolutionDevs:*

Is there any testnet? We just don’t know any.

*CoreDevs:*

There is a testnet. We will publish inode’s addresses.

### 3. UseCases

*CoreDevs:*

ask about detailed UseCase descriptions from SolutionDevs. Whisper (like other IM protocol) has different aspects:

- P2P,
- Darkness (conversational and metadata),
- Throughput,
- Reliability.

Which of them are more important for which UseCase?

*SolutionDevs:*

UseCase descriptions can be provided.

### 4. Benchmarking and Comparison

*CoreDevs:*

UseCases provided by SolutionDevs should contains quantitative requirements.

It is hard to solve trade-offs correctly while developing protocols without quantitative requirements to be met.

There is a swarm toolset to benchmark a network. May be it could be applied to Whisper development too.

Different existing IM protocols should be evaluated and compared to each other. It helps to set better development goals.

[@Ethernian](https://ethereum-magicians.org/u/ethernian):

Comparison and Benchmarking can be carried out as part of [Comparative Studies](https://github.com/Ring-of-Ethereum-Architects/knowledge/blob/master/base/ComparativeStudies) made by [Ring of Ethereum Architects](https://github.com/Ring-of-Ethereum-Architects/knowledge) .

### 5. Miscellaneous

Meeting biweekly proposed.

[@Ethernian](https://ethereum-magicians.org/u/ethernian) will create a poll to move existion chat group from telegram to somewhere.
