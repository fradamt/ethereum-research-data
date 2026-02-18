---
source: magicians
topic_id: 16474
title: Exploring the Potential of Multiple RPC Node Providers
author: Allyn
date: "2023-11-06"
category: Magicians > Tooling
tags: [json-rpc, rpc, load-balancing, api]
url: https://ethereum-magicians.org/t/exploring-the-potential-of-multiple-rpc-node-providers/16474
views: 735
likes: 0
posts_count: 2
---

# Exploring the Potential of Multiple RPC Node Providers

Hello Ethereum Magicians! ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

I wanted to start a discussion about the advantages and challenges of using multiple RPC node providers for blockchain requests. This approach can significantly enhance the reliability and performance of blockchain applications.

Here are a few points to consider:

- How can multiple RPC node providers improve the uptime and scalability of your applications?
- What challenges have you faced when working with multiple RPC providers?
- Are there any specific use cases where you see the most benefit from this approach?

I’m eager to hear your thoughts and experiences. Let’s dive into this exciting topic together! ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

Please share your insights and join the conversation!

## Replies

**ake** (2024-06-18):

Just stumbled on this. Mostly on your first point, the biggest problem I had is being able to reliably receive smart contract events as they come in. This one always has issues no matter the RPC provider. And when you need to reliably receive the events, they are most of the time are critical or almost critical to your setup.

The best way to go about this seems to be to set up a redundant event listener with multiple RPC node providers, eg with the top ones.

Here’s examples with web3.py, web3.js & ethers that we built at our Chainstack developer portal.

- Ethereum: How to set up a redundant event listener with Python
- Ethereum: BUIDLing a redundant event listener with ethers and web3.js

