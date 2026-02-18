---
source: ethresearch
topic_id: 10703
title: Does a bridge always necessitates creating an intermediate token?
author: naddika
date: "2021-09-11"
category: Applications
tags: []
url: https://ethresear.ch/t/does-a-bridge-always-necessitates-creating-an-intermediate-token/10703
views: 1130
likes: 0
posts_count: 3
---

# Does a bridge always necessitates creating an intermediate token?

When one creating a so-called **bridge** in order to exchange a coin on one blockchain to a coin on a **different blockchain**, how does it work? Does it **always necessitate creating an intermediate** token issued by a DEX?

A scheme is:

**user A:**

send KSM → receive INTermediate token, 1:1

then

**user B:**

send SOL → receive KSM

then

**user A:**

send INTermediate token  → receive SOL

In all the steps the tokens that get sent and received, sent and received from and to a smart contract of a DEX. Right?

Does it work this way?

## Replies

**blockchain-develop** (2021-09-11):

Cross-chain bridge mapping an asset from one chain to another. This is cross-chain communication. There are many protocol implementations.

After mapping, you can do something, such as swap.

User A mapping KSM to Solana chain by cross-chain protocol.

Swap to SOL with some defi contracts on Solana chain.

User A receive SOL on Solana chain or mapping SOL to kusama chain by cross-chain protocol.

The bridge is responsible for transmitting messages from one chain A to another B, and verifying the messages at B to ensure that the messages can be trusted. This can be implemented through the light client protocol.

The asset mapping and asset swap is application based on bridge.

---

**naddika** (2021-09-11):

Very unclear explanation.

