---
source: ethresearch
topic_id: 20598
title: RPC Nodes Management Tools
author: JoGetBlock
date: "2024-10-09"
category: Tools
tags: []
url: https://ethresear.ch/t/rpc-nodes-management-tools/20598
views: 207
likes: 3
posts_count: 1
---

# RPC Nodes Management Tools

Hey, Ethereum Community! Today I’d like to tell you how to manage your RPC nodes to get the best performance and the lowest downtimes possible. We will take the GetBlock RPC node provider as an example as they support Ethereum RPC nodes on Mainnet and Testnet. We are gonna learn how they manage their high-speed RPC, and discover some services for node management, handy tools, tips, and tricks

Let’s jump right into it!

#### How GetBlock - RPC Provider Works

When running an RPC node it’s crucial to be always aware of the consistency and availability of your node. To do so, you have to utilize some robust management and monitoring tools. Here’s an example of the tools GetBlock is using:

- Prometheus open-source monitoring system
- Grafana observability platform; (the latter sources data from the first one.)
- The health sidecar
- Alertmanager service in Slack
- Loadservice
- Auto-switching system

Prometheus gathers metrics and databases to display in Grafana. Prometheus is also bonded to Alertmanager service to inform the team in Slack about all events regarding infrastructure status. The health sidecar helps GetBlock monitor the current height and health of the nodes. To get immediate notifications from the monitoring tool GetBlock connected it to the Alertmanager service in Slack. It helps to get the fastest notification if some issue occurs and always double-check when it’s resolved. The health sidecar is also connected to the auto-switching system. So if the block deviation occurs, the unhealthy node is instantly switched to a healthy one. The last but not the least important thing is to keep the node updated to the latest versions. This way GetBlock constantly monitors blockchains’ GitHub repositories and social medias to find out about the upcoming updates first in hand.

All of that helps GetBlock to reach the highest node availability of 99%!

If you don’t wanna experience all the hustles associated with running and maintaining your Ethereum RPC node. You can simply connect to RPC nodes for 50+ blockchains with [GetBlock.io](http://GetBlock.io)

source: [Ethereum Node: RPC ETH nodes API for Web3 | GetBlock.io](https://getblock.io/nodes/eth/)
