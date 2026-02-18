---
source: ethresearch
topic_id: 1972
title: How to transfer the information of the token when transmitting RPC communication
author: james0277
date: "2018-05-11"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/how-to-transfer-the-information-of-the-token-when-transmitting-rpc-communication/1972
views: 1433
likes: 0
posts_count: 1
---

# How to transfer the information of the token when transmitting RPC communication

I have difficulties during the project and ask you questions. Please help me

situation

1. Create an ERC20-based token and try to create a transaction.
2. Communication with geth is RPC communication.
3. How do I send and receive information from the token when communicating with RPC?

question

1. Create an ERC20 token wallet with the function “personal_newAccoun” t, where you need to put the token information
2. When sending token, “eth_sendTransaction, eth_sendRawTransaction” should be used to send the token information here
3. How to load the eth_getBalance token information when checking balance (balance)
“id”: 1 “}” {“jsonrpc”: “2.0”, “method”: “eth_getBalance”, “params”: [“0x502af56ded80f54fac9920010180dcc6f228306d”, “latest”
The above code is an Ethernet balance inquiry. How do I do a token lookup?
