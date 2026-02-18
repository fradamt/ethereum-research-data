---
source: ethresearch
topic_id: 12930
title: Off-chain/L2 NFT Auction Protocol Idea
author: 0xkl1mt
date: "2022-06-24"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/off-chain-l2-nft-auction-protocol-idea/12930
views: 2372
likes: 1
posts_count: 4
---

# Off-chain/L2 NFT Auction Protocol Idea

TLDR: High demand NFT Auctions almost always fall back to a first priority auction via max priority fee and proof of personhood/general purpose roll ups don’t seem to be the answer. Could we create a system to 1) compute  auction results and settle on L1 and 2) build on top of a data availability layer that has burst capacity?

## What

It’s well known NFT auctions/mints cause massive negative externalities for network participants. There seems to be two schools of thought for solving this dilemma:

1. Scaling solutions such as roll ups which have higher throughput and therefore minimize impact.
2. Proof of personhood protocols which can be used to enforce restrictions on bidders to prevent gas wars. [1]

Approach 1 is potentially a short term solution as demand will eventually grow to consume additional L2 capacity(some NFTs may solely live on app specific roll ups, but many will not). The Othersides Otherdeeds NFT launch implemented a version of Approach 2 where users were required to KYC + were restricted to a max number of mints per wave, but this launch still negatively impacted regular ethereum users. [[2](https://mirror.xyz/0x3ae401F245034dAe25af1e2f9b9Bb8F006b1Dc6e/ErZMh-0TTwMrAKPJ1hlDcjvNfZvQ998G-B-oTS6BVQk)].

These points led me to a few questions:

1. In the medium term, is it futile to think high demand auctions will be able to cleanly fit into the ethereum tx fee market?
2. Do these auctions need the full security of ethereum and if not, could they be computed in a more favorable environment with minority trust assumptions and then settled on L1 or a major roll up?

## How

This post is intended to get initial feedback but a simple sketch of a protocol like this would look something like snapshot + CoW protocol:

1. Users can submit bids which are signed messages to a highly available data layer
2. At auction end time, bonded auction solvers could compute final results
3. Create merkleroot of results and submit to contract on L1

There are a lot of implementation details such as how to avoid spam on the data layer but because bidding is free, this could open up many fun aspects and avenues for bidding while also avoiding failed gas fees + extremely large miner/validator tips. Additionally, is this essentially a roll up for auctions? Would love to hear any thoughts on this!

I also meme-ified my argument:

[![Screen Shot 2022-06-24 at 1.05.10 AM](https://ethresear.ch/uploads/default/optimized/2X/7/7a4b1d0c8465d07503e311615931bc2d22f3bba9_2_336x500.jpeg)Screen Shot 2022-06-24 at 1.05.10 AM696×1034 49.9 KB](https://ethresear.ch/uploads/default/7a4b1d0c8465d07503e311615931bc2d22f3bba9)

## Replies

**alcalawil** (2022-07-30):

I like the meme. I’m working on solving this problem, is tricky

---

**Raunaque97** (2023-02-24):

Will changing the auction format to a sealed bid auction remove the issues related to gas?

no need to submit multiple bids, no bidding war, no last-minute snipping.

---

**monkeyontheloose** (2023-03-28):

hey, seems like an interesting problem, did you have any updates on the topic?

