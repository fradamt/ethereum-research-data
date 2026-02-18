---
source: ethresearch
topic_id: 8102
title: Homomorphic encryption on Ethereum and Ethereum likes
author: miohtama
date: "2020-10-12"
category: Cryptography
tags: []
url: https://ethresear.ch/t/homomorphic-encryption-on-ethereum-and-ethereum-likes/8102
views: 1406
likes: 2
posts_count: 2
---

# Homomorphic encryption on Ethereum and Ethereum likes

I am researching if it is yet viable to do [homomorphic encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption) on Ethereum, or any of Ethereum sister chains. I am especially interested in [secret sharing](https://en.wikipedia.org/wiki/Homomorphic_secret_sharing) that would enable secret ballot voting and similar applications.

- Is it possible on Ethereum mainnet yet or any time soon (I assume not - I would probably heard about it)? Any research going on this?
- Are there any other EVM chains that are actively working on this area of research?

## Replies

**samueldashadrach** (2020-12-06):

Private zero knowledge rollups may be the closest thing to what you’re looking for. They follow a UTXO model so transactions are private. [Aztec](https://aztec.network/) does this.

You could mint a token into each person’s wallet and then ask them to send it to the person they want to vote or delegate to. At the end of voting, people can prove how many tokens they own, or exit the rollup to prove this.

