---
source: magicians
topic_id: 22432
title: Client testing call #19, January 6, 2025
author: parithosh
date: "2025-01-06"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/client-testing-call-19-january-6-2025/22432
views: 112
likes: 1
posts_count: 1
---

# Client testing call #19, January 6, 2025

**Pectra**

- Final call for EIP-7840, Details here.
- EIP-2935 updates have been made over the holidays, the current status can be found here. The aim is to conclude the topic this wee.
- EELS and test releases went out over the holidays, please use pectra-devnet-5@v1.1.0 for testing your EL.
- There was a test regarding empty bytes that requires some discussion, please find it happening in this thread.
- Hive instance for pectra-devnet-5 can be found here. The devnet goes live once hive showcases most tests passing on most clients.
- On the CL front, there seems to be some issues with the minimal preset for the latest devnet. Information can be found in the interop channel.
- In order to make mev-workflow testing easier, Pawan has written a mock builder found here. This mock builder is almost fully integrated into kurtosis, once done, all clients should be able to locally test the mev-workflow.

**Progress/Open PRs for [pectra-devnet-5](https://notes.ethereum.org/@ethpandaops/pectra-devnet-5)**

**PeerDAS**

- Rebase work is ongoing. Local kurtosis configs will be provided over the next days.
- There are some open topics such as activation and v3 req/resp for blob sidecars found here. Please join the peerDAS breakout session to discuss the topic.

**EOF**

- Rebase work is ongoing, should go better now that pectra specs are fixed.
- Fuzzers from Danno and a few others are being used to find bugs.
- EOF aims to have a devnet once the rebase work has made some headway.
