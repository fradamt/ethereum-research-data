---
source: magicians
topic_id: 20846
title: Pectra testing call #1, August 19 2024
author: abcoathup
date: "2024-08-21"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/pectra-testing-call-1-august-19-2024/20846
views: 74
likes: 1
posts_count: 1
---

# Pectra testing call #1, August 19 2024

#### Summary

Update by [@parithosh](/u/parithosh) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1275363861012283393))*

`pectra-devnet-2`:

- pectra-devnet-2 status as well as a question about if the blockhash opcode was being tested.
- ethPandaOps is going to write up some local consolidation tests with kurtosis, they should be merged in this week and can help test the latest spec release and devnet-2 bug
- Erigon gave an update on potential reasons for missed proposals with teku. We will try a resync and increasing memory limits, the Erigon team will look into improving performance at the tip of the chain
- Prysm team gave us an update on their blob issue, post resync the prysm nodes are now working

#### Additional info

- Weekly testing calls won’t be streamed/recorded
- cast supports EIP7702: feat(cast): `cast wallet sign-auth` + `cast send --auth` by klkvr · Pull Request #8683 · foundry-rs/foundry · GitHub
