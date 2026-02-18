---
source: magicians
topic_id: 25311
title: "ERC-8017: Payout Race"
author: kyle
date: "2025-09-01"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8017-payout-race/25311
views: 69
likes: 2
posts_count: 3
---

# ERC-8017: Payout Race

This ERC proposes a minimal pattern for turning a stream of protocol revenue into another asset at or near market price. It is inspired by the “payout race” mechanics described within the Uniswap Foundation’s Unistaker proposal.

**How it works:** Value flows into the contract, filling a “bucket.” The first caller who pays the fixed required amount in the desired payment asset receives the entire current bucket balance.

This simple interface assumes a single payout asset and single desired payment asset (each can be ETH or ERC-20). ETH to ETH is not allowed.

[Draft ERC](https://github.com/ethereum/ERCs/pull/1194)

This is my first time opening up an ERC.  All feedback is welcome!

## Replies

**kyle** (2025-09-02):

I’ll add some context for why this exists. This patches a common tokenomics gap I see in the wild.

In a healthy decentralized protocol, it’s usually best if the service is paid in the protocol’s own token. That naturally creates buy pressure that can offset inflation elsewhere.

The problem is user friction. Asking people to pay each service in its native token is clunky, so many protocols accept ETH or stables. That choice is practical, but it breaks the loop and forces a separate buyback mechanism to route revenue back into the native asset.

After surveying patterns, the simplest and most predictable approach I found is the payout race. Unistaker described a version inside a larger Uniswap-specific system, where anyone could watch fees accrue and call `claimFees()` on a V3 pool, effectively swapping UNI for the pool’s fee assets. This ERC generalizes that core idea into a minimal, reusable primitive: stream value in, and let anyone who pays a fixed price pull the entire current balance.

I tried to fold broader, Unistaker-style needs into this standard, but that added complexity to what works best as a small, auditable mechanism. This draft keeps the surface tiny and leaves policy to upstream controllers.

---

**SamWilsn** (2025-11-25):

Have you seen [ERC-7528: ETH (Native Asset) Address Convention](https://eips.ethereum.org/EIPS/eip-7528) ? I’m not saying it’s a good or bad idea, but it is relevant.

