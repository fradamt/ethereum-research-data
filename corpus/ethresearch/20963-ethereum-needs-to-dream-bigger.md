---
source: ethresearch
topic_id: 20963
title: Ethereum Needs to Dream Bigger
author: MaxResnick
date: "2024-11-12"
category: Proof-of-Stake
tags: [mev]
url: https://ethresear.ch/t/ethereum-needs-to-dream-bigger/20963
views: 715
likes: 8
posts_count: 4
---

# Ethereum Needs to Dream Bigger

**Ethereum Needs to Dream Bigger**

Ethereum was conceived in 2013 to change the world. Since then, the original vision of a blockchain that would serve as the backbone for a new world order—a permissionless financial substrate with endless possibilities—has been ground to dust by the harsh realities of developing bulletproof production software and navigating core developer politics. In other words, Ethereum is jaded and burnt out. Our most “ambitious” proposals are five-year megaprojects to ship marginal improvements, and progress is slowing incrementally with each hard fork.

Reversing these trends requires accepting two hard truths:

1. We are no longer the only game in town; Ethereum is now competing in a marketplace of blockchains. Other teams with different visions are credible threats to Ethereum’s dominance.
2. Making decisions on five-year timescales doesn’t make sense when cryptography, consensus, engineering, and mechanism design are advancing at an extreme pace. State-of-the-art technology today may not be state-of-the-art in five years.

But enough with the diagnosis; how can we treat this ailment? First, we need to agree on and articulate a clear vision for what we are trying to build. In my opinion, this doesn’t require changing course; it requires doubling down on the core values that we started with in 2013:

> “Ethereum should be a global compute platform that provides developers all the tools they need to solve the world’s hardest coordination problems.”

In many ways, we have achieved, at least partially, this vision already, but to complete the project we have a long way to go. Smart contracts on Ethereum are Turing complete, but fees on the blockchain are too high for many applications, and block times are long enough that Ethereum isn’t the ideal place to host financial applications. Moreover, Turing completeness means we can write arbitrary smart contract programs that execute logic on their inputs, but if app developers can’t trust the quality of their inputs, then they can’t trust the outputs either.

Ethereum today is credibly neutral and censorship-resistant if given enough time, but when you zoom in to millisecond timescales, it looks a lot more centralized. Within each 12-second block, a single proposer must approve every transaction. This temporary proposer monopoly distorts markets and makes many mechanisms that app developers want to build completely intractable on Ethereum.

With that said, here are the goals for the next five years on Ethereum:

- 1-second block times
- Single-slot finality
- Vastly increased throughput (>1000 TPS)
- Multiple concurrent proposers

**1-Second Block Times**

A round trip from NYC to Tokyo takes less than 200 ms. You can round-trip a message from NYC to Tokyo five times in one second. If anything, 1-second block times are not ambitious enough. Implementing them would be a major unlock for applications on the L1 and would improve the speed to L1 confirmation for L2 transactions.

**Single-Slot Finality**

Single-slot finality is important for rollup interoperability. In five years, all rollups will be ZK rollups. Bridging will happen in the span of two slots on the L1. But this requires single-slot finality because a ZK rollup cannot allow funds to be withdrawn before finality, even with a valid proof.

**Vastly Increased Throughput**

Fees on Ethereum L1 are too high. Even if we think rollups are going to be where Ethereum activity takes place, L1 fees will still be a multiplier in those fees. We also need to credibly signal to app developers that Ethereum is a place they can safely build their apps—that we will continue to scale as new technologies become available—so there is no possibility that their app, if it becomes successful, will outgrow the capacity of Ethereum.

**Multiple Concurrent Proposers**

Of all these proposed changes, Multiple Concurrent Proposers may be the highest lift but also the highest potential reward. While the other items on the list are parameter changes (which will require a lot of work to accomplish, no doubt), MCP unlocks capabilities that no blockchain has had ever before: real-time censorship resistance guarantees. The types of applications that can be built with this technology are purely theoretical today. MCP is the capstone that brings Ethereum’s market microstructure—which today is extremely centralized and extractive—in line with its broader macro vision of credible neutrality and decentralization.

## Replies

**MicahZoltu** (2024-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> navigating core developer politics

This is why we should ossify Ethereum and everyone can build something new.  A lot of the ideas I hear shared here I think are great ideas, I just don’t think we should be futzing with Ethereum’s rules.  All of the changes have caused me to seek other places to store my assets because I do not feel comfortable storing my assets on a blockchain where the rules change every 6 months.  I want to store my assets on something stable, not a playground for a bunch of smart people.

---

**LoadingALIAS** (2024-11-13):

I think you’re confusing Ethereum with a centralized system or tech company. It doesn’t work that way - even if we all want it to.

The researchers and engineers involved in the day to day need consensus on anything that happens - it’s the design. This led to politics and a shit show in some cases where ego mattered more than code.

Also, at this point, Ethereum is a living, breathing system. It’s the second largest blockchain in the world and millions of people rely on non-breaking changes or changes that don’t introduce bugs that cause them to lose money.

I agree with the sentiment, but organizing the entire developer ecosystem to get on the same page is like… well, kind of like doing the same with a world government. People just don’t always agree and until they do - nothing gets done.

---

**matthewkeil** (2024-11-25):

Your ambition is notable but I think your vision is misguided.  The secret sauce of Ethereum is security through decentralization.  What you mention should be part of the L2 ecosystem.  Being a root of trust is the CRITICAL piece for what we do with L1.  That is all that matters.  Its the core competency.  Everything else is a nice bonus but should not be attempted at the expense of decentralization.  The blockchain tripod is real and consensus, both head of chain and direction of development, takes time…

