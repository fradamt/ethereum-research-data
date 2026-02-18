---
source: magicians
topic_id: 15825
title: Automatically Reset Testnet
author: taxmeifyoucan
date: "2023-09-18"
category: EIPs
tags: [testnet]
url: https://ethereum-magicians.org/t/automatically-reset-testnet/15825
views: 1399
likes: 2
posts_count: 1
---

# Automatically Reset Testnet

EIP specifying a testnet mechanism for client implementations that automatically periodically resets the network back to genesis. This kind of testnet can provide an alternative ephemeral environment to long running testnets or devnets.

PR with the EIP doc: [Add EIP: Automatically Reset Tesnet by taxmeifyoucan · Pull Request #6916 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6916)

EIP is based on previous work on existing network [Ephemery](https://ephemery.dev). The existing network can be used as a custom network in any Ethereum client and has been running for months now.
