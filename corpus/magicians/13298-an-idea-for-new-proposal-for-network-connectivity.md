---
source: magicians
topic_id: 13298
title: An idea for new proposal for network connectivity
author: 0xOZ
date: "2023-03-14"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/an-idea-for-new-proposal-for-network-connectivity/13298
views: 357
likes: 1
posts_count: 1
---

# An idea for new proposal for network connectivity

## Introduction

The Ethereum network relies on a set of validators to maintain its decentralized nature. These validators come to a consensus about the nodes that will have specific IP addresses on the network. The current process of connecting to the network involves trusting specific nodes that come with the node binary. This can lead to connectivity issues and security concerns. In this article, we propose an improvement to the process of connecting to the network without modifying the protocol.

## Proposed Solution

We propose that the validators on the network choose the nodes that will have specific IP addresses on the network based on a set of rules such as reputation, weight, and other factors. These chosen nodes would act as the trusted nodes for connecting to the Ethereum network. However, instead of requiring clients to have a list of trusted nodes in their configuration, they would simply connect to one of the static IP addresses that are designated for the Ethereum network.

This approach would eliminate the need for clients to trust specific nodes that come with the node binary, as well as the need for them to search for trusted online clients to connect to. Additionally, it would reduce the risk of connectivity issues and security concerns that arise when trusted nodes go offline or get compromised.

## Implementation

The implementation of this proposed solution would require the validators on the network to reach a consensus about the nodes that will have specific IP addresses on the network based on the set of rules mentioned earlier. These chosen nodes would then be designated as the trusted nodes for connecting to the Ethereum network.

Next, a list of static IP addresses for the Ethereum network would be made available to clients. When clients wish to connect to the network, they would simply choose one of the available IP addresses to connect to. The network workflow would remain unaffected, as the validators would continue to validate transactions and maintain the decentralized nature of the network.

## Conclusion

In conclusion, the proposed solution offers an improvement to the process of connecting to the Ethereum network without modifying the protocol. By eliminating the need for clients to trust specific nodes that come with the node binary and reducing the risk of connectivity issues and security concerns, the proposed solution would improve the overall user experience and enhance the security of the network. The implementation of this solution would require the validators on the network to reach a consensus about the nodes that will have specific IP addresses on the network and for a list of static IP addresses for the Ethereum network to be made available to clients.
