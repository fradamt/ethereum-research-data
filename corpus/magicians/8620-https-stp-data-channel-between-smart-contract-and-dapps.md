---
source: magicians
topic_id: 8620
title: HTTPs (STP) data channel between smart contract and Dapps
author: hileamlakB
date: "2022-03-15"
category: EIPs
tags: [evm, eip-191]
url: https://ethereum-magicians.org/t/https-stp-data-channel-between-smart-contract-and-dapps/8620
views: 721
likes: 1
posts_count: 1
---

# HTTPs (STP) data channel between smart contract and Dapps

Down the road, there will be a growing number of DApps build on Ethereum. Some of which will probably need an encrypted communication channel between their smart contracts and their use facing UI’s. If something like this already exists correct me, but a standard protocol to establish something like `HTTPs` (obvious called something else for Ethereum, possibly `STP` for secure transfer protocol) would be very useful. For instance, if a smart contract gives out unique secrete ids to its users, to be stored offline and retrieved for future use, an encrypted channel is necessary.

This EIP will build of EIP-191. Using the encryption scheme as a starting point.
