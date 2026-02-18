---
source: magicians
topic_id: 22818
title: "New ERC: Wallet Call Simulation API"
author: jxom
date: "2025-02-11"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/new-erc-wallet-call-simulation-api/22818
views: 71
likes: 1
posts_count: 1
---

# New ERC: Wallet Call Simulation API

This ERC proposes a new JSON-RPC method for simulating the execution of calls on a Wallet. The method is designed to be used by Wallets to simulate the execution of calls before sending them to the network, allowing for gas estimation, log extraction, and call validation.

Applications are reliant on JSON-RPC communication to Wallets in order to execute actions (ie. wallet_sendCalls and/or eth_sendTransaction). A seemingly core functionality for “offline” Applications (Servers, etc) is the ability to simulate if an action will succeed or fail and/or estimate the total fee and/or calculate balance changes, prior to signing and broadcasting to the network.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/892)














####


      `ethereum:master` ← `jxom:jxom/simulate-calls`




          opened 12:36AM - 11 Feb 25 UTC



          [![jxom](https://avatars.githubusercontent.com/u/7336481?v=4)
            jxom](https://github.com/jxom)



          [+223
            -0](https://github.com/ethereum/ERCs/pull/892/files)
