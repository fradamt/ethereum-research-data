---
source: ethresearch
topic_id: 9604
title: Chronicle market
author: echopolice
date: "2021-05-24"
category: Economics
tags: []
url: https://ethresear.ch/t/chronicle-market/9604
views: 869
likes: 1
posts_count: 1
---

# Chronicle market

One of the problems with scalability in the blockchain is related to the fact that each node is required to store information about the entire transaction history of the network. Let’s dream about whether it is possible to build a market for history, similar to the existing market for predictions. Instead of storing many gigabytes of information on your hard drive, is it possible to get by with tokens with chunks of history that would be sold on the market, for example, using a well-known mechanism with a binding curve?

Imagine that you can purchase a piece of history in the market starting from block *n* and ending with block *n+k*, while the market itself offers a tool for checking the consistency of the history. Then the public consensus would reduce the economy to the fact that the true transaction history of the network would be sold on the market, since it would be profitable for rational players to buy tokens from exactly the history that the majority would support. For example:

*minimal_lenght*=  L_{min};

*maximum_lenght* = L_{max} (all history at time t);

*Price of a history token with a length of l* ~  \sum_{i=L_{min}}^l w_i \cdot f(numberOfTokenHolders_i)\cdot 1( chunk \; of \; i  	\subset l ) \cdot \frac{(chunk \; of   \; i)}{i}, where w_i = l/i

However, I don’t have a clear picture in my head of how this could be implemented without introducing additional vulnerabilities for malicious attacks. It is also important to prevent the weakening of the network’s decentralization.
