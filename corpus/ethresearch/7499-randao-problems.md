---
source: ethresearch
topic_id: 7499
title: Randao problems?
author: ERC20s
date: "2020-06-02"
category: Sharding
tags: []
url: https://ethresear.ch/t/randao-problems/7499
views: 3397
likes: 3
posts_count: 3
---

# Randao problems?

I’ve been waiting for eth 2 to integrate the randao into my casino project.

My project is built in solidity and i’d like to know:

Will solidity be supporting randao requests?

(Currently prylabs has a ‘randao reveal’ but it’s in GO)

How will the requests work?

Cost estimations?

And general purpose use cases..

I’m also wondering how it can be manipulated by users skipping their turn if they do/don’t like a number to persuade a result..

For example:

If a fruit machine has a 100x potential reward..

There were 50,000 validators

Say attacker has 100 validators..

And wants to produce a number between 99-100 to receive 100x gains..

Could a user increase his chance of winning by 500 to 1 adding a 0.2% chance of winning?

By turning off their nodes at the right time if the user doesn’t support the given number?

Any clarity about randaos is much appreciated..

The website hasn’t been updated for 2 years ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=14)

Love you all!

Sources:

(randao website: https://www.randao.org)

(randao reveal: https://beacon.etherscan.io/slot/324063)

## Replies

**HAOYUatHZ** (2020-06-02):

RANDAO can be biased.

- Avalanche RANDAO – a construction to minimize RANDAO biasability in the face of large coalitions of validators
- RANDAO beacon exploitability analysis, round 2
- Limiting Last-Revealer Attacks in Beacon Chain Randomness
- https://hackmd.io/@Zergity/UnbiasableRNG#Biasability-of-Distributed-RNGs
- https://quantstamp.com/blog/presenting-quantstamps-ethdenver-beacon-chain-implementation

---

**HAOYUatHZ** (2020-07-15):

[github.com](https://github.com/ethereum/eth2.0-specs/blob/7b43a3d7724f9b51c373eefe7c047a01c8e55634/specs/phase0/beacon-chain.md#randao)




####

```md
# Ethereum 2.0 Phase 0 -- The Beacon Chain

**Notice**: This document is a work-in-progress for researchers and implementers.

## Table of contents

- [Introduction](#introduction)
- [Notation](#notation)
- [Custom types](#custom-types)
- [Constants](#constants)
- [Configuration](#configuration)
  - [Misc](#misc)
  - [Gwei values](#gwei-values)
  - [Initial values](#initial-values)
  - [Time parameters](#time-parameters)
  - [State list lengths](#state-list-lengths)
```

  This file has been truncated. [show original](https://github.com/ethereum/eth2.0-specs/blob/7b43a3d7724f9b51c373eefe7c047a01c8e55634/specs/phase0/beacon-chain.md#randao)








why eth2.0 is using RANDAO instead of [RANDAO++](https://www.reddit.com/r/ethereum/comments/4mdkku/could_ethereum_do_this_better_tor_project_is/d3v6djb/) proposed by vitalik?

The timeline is RANDAO -> RANDAO++ -> ETH2.0, isn’t it? RANDAO++ should already exist when eth2.0 design started?

