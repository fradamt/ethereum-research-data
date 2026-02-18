---
source: ethresearch
topic_id: 8581
title: "Hop: Send Tokens Across Rollups"
author: chris.whinfrey
date: "2021-01-27"
category: Layer 2
tags: []
url: https://ethresear.ch/t/hop-send-tokens-across-rollups/8581
views: 11309
likes: 31
posts_count: 4
---

# Hop: Send Tokens Across Rollups

The Hop protocol provides a trustless and scalable rollup-to-rolllup bridge. The protocol aims to:

1. Allow tokens to be quickly and easily sent from one rollup to the next
2. Enable fast-exits from rollups
3. Eventually support cross-rollup contract calls

We believe this is a viable solution to cross-rollup composability for the majority of use cases. The Hop protocol achieves this using a two-pronged approach:

1. Create a cross-network bridge token that can be quickly and economically moved from rollup to rollup or claimed on layer-1 for its underlying asset.
2. Use an Automated Market Maker to swap between each bridge token and its corresponding Canonical Token on each rollup in order to dynamically price liquidity and incentivize the rebalancing of liquidity across the network.

Looking for constructive feedback around the design and to discuss future areas of exploration.

Paper: https://hop.exchange/whitepaper.pdf

[@miguelmota](/u/miguelmota) [@shanefontaine](/u/shanefontaine) and I have put together a fully functional demo that bridges Arbitrum’s and Optimism’s rollups and the Kovan testnet.

Contracts: https://github.com/hop-exchange/contracts

Demo: https://hop.exchange

## Replies

**vbuterin** (2021-01-30):

Interesting!

I’ll attempt to restate and summarize in my own words; is this description correct?

1. There is a method by which tokens can be transferred en masse from rollup A to rollup B (this requires a base layer transaction and potentially waiting a week)
2. Users would not use this method directly. Instead, they would transfer their tokens into a contract on the rollup, and some third party called a Bonder would immediately give them tokens on the destination rollup and in exchange capture that slot in a contract.

Questions:

1. Is it really necessary to have a distinct notion of hop tokens? Why not just work with tokens inside the rollup directly?
2. One issue I see with (2) is that potentially two bonders could front the funds to the user in the second rollup at the same time. This could be resolved if you require bonders to register their intent before they can front a transfer, and only the first to register would get paid back once the mass transfer completes. Are these the kinds of issues that you’re concerned about when you talk about challenges extending to multiple bonders?
3. Do both sides need smart contract capability? Ideally, it would be nice to have a scheme that requires only one side to have smart contract capability (and for that side to be able to be either the sending or receiving side). This way Optimism and/or Arbitrum could serve as hubs, and allow fast transfers not just between each other but also into Loopring, Zksync and other non-EVM rollups.

---

**chris.whinfrey** (2021-01-30):

Thanks! Your description is spot on.

> Is it  really  necessary to have a distinct notion of hop tokens? Why not just work with tokens inside the rollup directly?

There’s a piece of the system that’s implemented, but I didn’t touch on it in the paper because I considered it more of an optimization for our particular implementation. I now realize it’s important to answering this question. In short, we implemented Hop tokens to have a more aggressive exit time than the 7 day period that Optimism chose. Hop Tokens also allow the primary pricing mechanism to be kept on-chain in the form of AMMs. I’ll add a new section for this to the paper but will explain this in a follow-up response for now.

> One issue I see with (2) is that potentially two bonders could front the funds to the user in the second rollup at the same time. This could be resolved if you require bonders to register their intent before they can front a transfer, and only the first to register would get paid back once the mass transfer completes. Are these the kinds of issues that you’re concerned about when you talk about challenges extending to multiple bonders?

Yes, this is the main challenge that needs to be solved to extend to multiple bonders.

> Do both sides need smart contract capability? Ideally, it would be nice to have a scheme that requires only one side to have smart contract capability (and for that side to be able to be either the sending or receiving side). This way Optimism and/or Arbitrum could serve as hubs, and allow fast transfers not just between each other but also into Loopring, Zksync and other non-EVM rollups.

Currently, both sides need smart contract capability. It would be great to expand to a model like this. I’ll add a section to “Areas for Further Research” and we’ll start thinking about this.

---

**chris.whinfrey** (2021-01-30):

**Hop Tokens exit time and challenge mechanism:**

We implemented Hop tokens to have a more aggressive exit time than the 7 day period that Optimism chose. It works by using a simple challenge mechanism that piggybacks on the rollup’s challenge mechanism. For example:

1. A bundle of Hop ETH Transfers is sent from the rollup down to layer-1. This payload will reach layer-1 after the rollup’s 7 day exit time but will primarily be used to resolve challenges.
2. On layer-1 the Bonder immediately attests that the bundle payload will show up in 7 days and puts up collateral so that the bundle can be propagated up to its destination rollups immediately.
3. If the Bonder’s attestation is fraudulent, it can be challenged. The challenge mechanism simply waits 7 days to see if the bundle payload will show up on layer-1 in order to resolve the challenge.
4. If the Bonder’s attestation goes unchallenged for the duration of the Hop exit time, their collateral is unlocked.

The reason for using a more aggressive exit time is that there’s a different set of tradeoffs for Hop Bridge participants when compared to rollup participants. While rollups expose users to the risk of the rollup challenge mechanism failing at all times, end users using a Hop Bridge are only exposed to Hop-related-risk for the brief period they are using the bridge to transfer tokens. It’s in the best interest of the rest of the Hop participants (Bonder, AMM liquidity providers, arbitrageurs) to take on some long-tail risk of the Hop challenge mechanism failing in exchange for a much more capital efficient system.

Another nice aspect of the Hop token setup is that it keeps the primary pricing mechanism on-chain in the form of an AMM. Because tokens on each rollup are not 100% fungible, their prices will fluctuate relative to each other based on market demand to exit. Using AMMs to price tokens across rollups with a common intermediary asset (e.g., Hop ETH) allows the relative pricing of rollups’ tokens to remain on-chain instead of being determined by the Bonder. If there’s a lot of demand to exit a given rollup, tokens on that rollup will be trading at a discount, and arbitrageurs can come fill that demand and profit off of the discount by buying the discounted token from the AMM. Without the AMMs, it would be completely up to the Bonder to dynamically adjust fees off-chain and do all the rebalancing themselves.

We currently have the Hop exit time set to 1 day, with the thought being that it is long enough to survive a decently long censorship attack, but not long enough to protect against longer consensus failures or a more extreme censorship attacks that requires a user activated soft fork. I’m curious if you think 1 day makes sense here and if this tradeoff seems reasonable in general.

An alternative direction could be to remove Hop Tokens and the AMMs from the system and do the batched transfers using the rollups tokens directly as you mentioned. I think this is worth keeping in mind as we figure out how to decentralize the Bonder role but it seems less optimal with the current single Bonder set up.

