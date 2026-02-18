---
source: ethresearch
topic_id: 20946
title: Multilane Sequencing
author: tkstanczak
date: "2024-11-08"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/multilane-sequencing/20946
views: 241
likes: 5
posts_count: 2
---

# Multilane Sequencing

# Multilane Sequencing

Thanks to Conor McMenamin for the review and comments (and yes, he said it needs to be better before I post it here but there is a limit to my research skills)

### Intro

L2 interoperability / L2 bridging is the subject of major discussion now. It is worth noting that L2 interop touches all the important aspects of Ethereum scaling—security of L2s, atomicity of transactions, cost of moving assets between chains, etc.

Any solutions bringing us closer to a standardization of the bridging, or at least a standardization of how we describe them, would likely help with cross-chain risk management, better comparability of L2s, and better scaling UX.

Below, I am proposing a multilane sequencing model for L2s on Ethereum that aims at addressing these problems (or rather not really solving them but creating ways of talking and thinking about tradeoffs and classification).

### How do we construct Lanes?

First, we construct the lanes based on their settlement frequency measured as an L1 blocks multiplier. We make the construction binary, so the lanes are Lane-1, Lane-2, Lane-4, Lane-8, Lane-16, and so on. Lane-8 settles to Ethereum every 8 blocks. Lane-1 settles to Ethereum on every Ethereum block. For every chain, we place it on a corresponding lane depending on how often it settles on L1. And so, Ethereum mainnet trivially lands on Lane-1. Any rollup that produces a block every N Ethereum blocks lands on Lane-N. A rollup targeting Lane-256 settles on Ethereum L1 every ~50 minutes (12 seconds × 256 blocks / 60 seconds is 51.2).

We call Lanes ‘lower’ or ‘faster’ if they settle more often. We call Lanes ‘higher’ or ‘slower’ if they settle less often.

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/d/4d021fa96f3e6052958ff4bf3860fab4c1b38d09_2_690x480.png)image1248×869 54.1 KB](https://ethresear.ch/uploads/default/4d021fa96f3e6052958ff4bf3860fab4c1b38d09)

### Details

Any chain on Lane-M can serve as a bridge between chains on Lane-N as long as N > M. So any of the below can be a bridge:

- L1 for any two L2s
- Any generic L2 for other L2s that are settling less often

specifically any ‘bridge rollup’ that settles on Ethereum more often than the rollups that it facilitates bridging between

Why so? On Lane N, every N blocks we lock the state of the entire Lane N using Ethereum security. Any special lane-settling contracts, atomic operations, etc., can be executed on blocks with numbers being a multiple of N.

Rollups on Lane-N naturally produce blocks more often than N (which is practically the rollup sequencer or group of sequencers acting as preconfirmers in the context of L1 settlement—the user trusts the L2 sequencer layer that it will settle user transactions on L1 in the future).

Separately, any independent preconfirmer can offer even more fine-grained guarantees and split rollup blocks even further (for example, rollup-boost can act as the Unichain block preconfirmer by splitting the block into 250 ms chunks).

At any Lane-N, there may exist alternative settlement chains with their own security guarantees. As such, you can imagine a Layer-1/8th which allows for settlements up to every 1.5 seconds. These may include, for example, DA layers.

Any state of a rollup can, at a given time, be settled at various different lanes with varying security guarantees. If I have an account entry on a Rollup X on Lane-N, then I can take timestamps of the state at times modulo various multiples of 12 seconds (1.5 seconds, 3 seconds, 6 seconds, 12 seconds, etc.) and find any settlement layer to which the rollup settles at the given lane. Then I can say that my state at that time is secured to that layer’s security level. For example, if Ethereum’s security level is $100 B, and there is a DA layer secured by $10 B that the rollup settles to every 3 seconds, and my account had $1000 at time 12k and $1500 at time 12k + 3, then I have $1000 secured by $100 B and an additional $500 ($1500 − $1000) secured by a $10 B settlement layer until time 12(k+1) when (assuming the balance does not change) it will get secured by $100B as well.

Now, security itself may actually be seen as a bit more tricky, as it is affected by the security of the layer that the rollup settles to, as well as the security of the rollup’s enshrined bridge. It defines how likely the rollup may be seen as a pure security settlement route from higher lanes all the way to Lane-1 (Ethereum mainnet). Simply speaking, if you have a pure security route (absolutely no-risk bridge—theoretical), then bridging through a Lane-256 rollup between two Lane-512 rollups is as secure as bridging directly via L1.

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/a/5aa4e2fdbcd321b475f68565850baf3ca3cd8b56_2_642x500.jpeg)image1213×944 107 KB](https://ethresear.ch/uploads/default/5aa4e2fdbcd321b475f68565850baf3ca3cd8b56)

### Composability-Security-Price Trade-off

Why would a rollup ever choose to be placed on higher lanes? Because lower lanes (Lane-1, Lane-2, etc.) are much more expensive—settling on Ethereum mainnet is expensive as it has to pay for the borrowed security. Also, the higher the Lane level, the higher the price of atomic composability—I can atomically compose with any other rollup at the same or higher Lane, but to compose with a rollup on a lower Lane I need to settle to at least one of the lower Lane rollups—borrowing security from Ethereum mainnet for that Lane settlement or finding another settlement layer on the Lane. Hence, we have a trade-off between the price of composability and the price of security—Composability-Security Trade-off (CST). This seems to be an intuition from all economic activity—the more different markets I want to access, the more I have to pay for access to the markets that everyone uses for settlement or to access alternative, more shady settlement venues.

### Multilane Sequencing

Now, interestingly, any rollup may participate in native multilane sequencing, allowing for some kind of Lane sharding. The rollup allows assets to move between the Lane shards with the following rules—you can move assets from Lane-N to another Lane only at the time when Lane-N settles. This means that I can move assets quite often to slower settling lanes, but I can only move assets back to the faster lanes every now and then. And so, if Rollup X supports sequencing on Lane-8 and Lane-32, then I can move assets from Lane-32 to Lane-8 at blocks 32k, but I can move assets from Lane-8 to Lane-32 at blocks 32k, 32k+8, 32k+16, 32k+24. Moving assets to a faster lane means that I will be ready to pay more for any transactions involving these assets (I settle more often to Ethereum mainnet), but I am getting more composability natively. Solutions like this should be a relatively simple state sharding for L2s, and application developers could even choose which Lane shard they deploy their smart contract to, hence deciding the level of security the application guarantees and the cost of transactions. So, for example, Rollup X could offer a 16-day Lane for gaming, a 6-minute Lane for asset transfers, or a 1-minute Lane for large cross-rollup swaps.

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/b/5bdbad3ebd2cea676dc51e6f20ec41f9b7a6db65_2_689x318.png)image1212×559 54.9 KB](https://ethresear.ch/uploads/default/5bdbad3ebd2cea676dc51e6f20ec41f9b7a6db65)

## Replies

**14mp4rd** (2024-11-08):

How is this different from L3s? If it is cheaper and faster to settle to a lower lane L2, then higher lane L2s will less likely to settle to Ethereum (except fallback, because they will eventually settle to Ethereum via the intermediary lower land L2).

