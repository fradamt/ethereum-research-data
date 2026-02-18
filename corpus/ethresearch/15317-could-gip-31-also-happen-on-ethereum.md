---
source: ethresearch
topic_id: 15317
title: Could GIP-31 also happen on Ethereum?
author: pcaversaccio
date: "2023-04-16"
category: Security
tags: []
url: https://ethresear.ch/t/could-gip-31-also-happen-on-ethereum/15317
views: 1607
likes: 6
posts_count: 2
---

# Could GIP-31 also happen on Ethereum?

[GIP-31](https://forum.gnosis.io/t/gip-31-should-gnosis-chain-perform-a-hardfork-to-upgrade-the-token-contract-vulnerable-to-the-reentrancy-attack/4134) was a hard fork on Gnosis Chain that changed an existing, “should-be-immutable” contract code with a new bytecode to fix a reentrancy issue (517 tokens were impacted). I haven’t seen any broader discussion about this incident, nor have I seen many callouts. I think it’s time to change that (and by that, I mean having a productive discussion). Could such an incident also happen on Ethereum? Do we need further governance mechanisms to prevent such an incident completely (e.g. disallowing such EIP proposals etc.). Please drop your thoughts here.

Two similar incidents:

- Polygon:

Polygon Lack Of Balance Check Bugfix Review — $2.2m Bounty | by Immunefi | Immunefi | Medium
- https://polygon.technology/blog/all-you-need-to-know-about-the-recent-network-upgrade

Binance

- Release v1.1.16 · bnb-chain/bsc · GitHub

## Replies

**pcaversaccio** (2023-04-20):

Two scenarios where I deem such a scenario plausible:

- The Beacon Deposit Contract has a (maybe compiler) bug that a black hat exploits and withdraws all staked ETH (at the time of this writing 18,833,884 ETH).
- The EF Multisig contract gets exploited (maybe due to a compiler bug) (in that scenario the overall stolen funds of course matter; currently the multisig holds around 1bn of dollar value).

