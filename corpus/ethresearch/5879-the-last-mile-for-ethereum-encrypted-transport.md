---
source: ethresearch
topic_id: 5879
title: "The last mile for Ethereum: encrypted transport"
author: rumkin
date: "2019-07-26"
category: Networking
tags: []
url: https://ethresear.ch/t/the-last-mile-for-ethereum-encrypted-transport/5879
views: 1583
likes: 0
posts_count: 1
---

# The last mile for Ethereum: encrypted transport

Today Ethereum users depends on centralized infrastructure while loading clients, communicating with nodes or sending transactions. Some of users can setup VPN. But anyway all of them should to use domains and SSL certificates created by centralized/trustful organizations of pre-blockchain era. It makes Ethereum UX incomplete and ENS itself not a real NS. Also it slow down the progress. We need to make Ethereum fully independent. The solution is creation of Ethereum’s CA which will be trustles, distributed and use blockchain. It will be good if it will use existing infrastructure. After my research I found a solution how to create such CA and implement Ethereum TLS. I have working prototype and will publish it soon after some cleanup. Also I’m working on browser which can use both networks.

This solution allows to use ENS as complete domain name system and connect regular web sites to such network without any modifications, If they configurable. However this network requires a pool of DNS servers which should be trustles. And now we come to the questions part:

1. Is there any other projects which works on it?
2. Could shardes became a DNS servers in Ethereum 2.0?
3. Current SSL certificates are using obsolete ASN.1 encoding and TLS has legacy protocols which shouldn’t be supported never. So maybe it’s make sense to reimplement TLS using Ethereum 2 solutions?
4. What name should this TLS have (and should it)?
5. What name should such network have (and should it)?
6. What protocol name should be used instead of https://?
