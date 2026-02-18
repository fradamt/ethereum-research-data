---
source: ethresearch
topic_id: 20639
title: "Hermes: a monitoring light node for Ethereum's Gossipsub network"
author: yiannisbot
date: "2024-10-14"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/hermes-a-monitoring-light-node-for-ethereums-gossipsub-network/20639
views: 289
likes: 7
posts_count: 3
---

# Hermes: a monitoring light node for Ethereum's Gossipsub network

The [ProbeLab team](https://probelab.io) is happy to announce [Hermes](https://github.com/probe-lab/hermes), built primarily by [@dennis-tra](/u/dennis-tra) and [@cortze](/u/cortze). *Hermes is a [GossipSub](https://docs.libp2p.io/concepts/pubsub/overview/) listener and tracer for [libp2p](https://libp2p.io/)-based networks.* We hope that the tool will see wide use by the community and contributions to include more features and support for other networks.

## What is Hermes and what can you do with it

Hermes behaves like a light-node and connects to other participants in the network. It relies on a trusted local node that ensures we can reply to any incoming requests and maintain stable connections.

Hermes-based experiments aim to measure the efficiency and performance of the GossipSub message broadcasting protocol in any libp2p-based network. Hermes can help developers tune their network’s protocols based on the message propagation latency and control message overhead.

The tool currently supports any [Ethereum](https://ethereum.org/en/) network (at the Consensus Layer), although there will be more networks supported in the future.

## How does it work

### Components

Hermes operates as a single component, the **light-node**, for each network it is deployed in. However, it has two major requirements to work: 1) a **trusted local node** that will provide the right view of the chain’s state and 2) an **event consumer** that will receive all the libp2p traces and will store them. The light-node is responsible for discovering peers, maintain connections with them, and monitor the internal events at the libp2p host.

### Light-node

Hermes operates like a standard libp2p node, discovering and connecting to the network while supporting all libp2p protocols to ensure reliable and secure communication. It connects to a trusted local, or remote node for certain RPCs that require chain state information, leveraging these trusted sources to enhance its capabilities.

Hermes subscribes to all available GossipSub topics, allowing it to comprehensively receive, unveil and trace all the interactions with the network. This enables the tool to keep track of network activity efficiently.

Additionally, Hermes can submit these traces to any defined consumer, with current support for [AWS Kinesis](https://aws.amazon.com/kinesis/) and [Xatu](https://github.com/ethpandaops/xatu) from the Ethereum Foundation (EF). This feature facilitates the integration of network data with analytics and monitoring tools, aiding in the overall security and functionality of the network.

### Deployment

Hermes has been developed to run continuously. However, to increase the steadiness of the light-node’s connectivity, the node must successfully respond to chain-oriented RPC calls that remote peers might ask. Since Hermes has been designed to be chain-agnostic, we must rely on an external trusted node to serve that information.

Hermes must be paired with one chain client: in our case and for Ethereum’s Consensus Layer, we used Prysm. Giving Hermes the HTTP API and the gRPC host’s endpoints, Hermes can add itself as a “whitelisted” node, in order to later forward most of the chain- or state-related RPC calls. However, the same Prysm node could be connected to several Hermes instances as the following graph shows, which helps reduce the deployment requirements.

[![hermes-arch](https://ethresear.ch/uploads/default/optimized/3X/f/9/f9928f77c5bd3d905868ad64c330545ef157b990_2_690x238.png)hermes-arch3484×1204 229 KB](https://ethresear.ch/uploads/default/f9928f77c5bd3d905868ad64c330545ef157b990)

Hermes has been extended to support a different set of data consumers or data streams. Since all the event traces need to be persisted somewhere, the tool offers three different options:

- AWS Kinesis (our deployment)
- Xatu callbacks (used by the EF)
- Trace logger to stdout (for local dev-testing)

If you are interested in using or upgrading the tool to support other networks or data streams, [reach out to us](https://probelab.network/contact).

## What data does Hermes gather

As Hermes maintains stable connections with the rest of the network nodes, it can emit debugging traces of how libp2p and GossipSub work in the wild.

Hermes gathers the following information out of the box from the libp2p host and the GossipSub protocol:

- Connections and Disconnections from the libp2p host
- Control GossipSub messages:

Subscriptions from other nodes to topics
- GRAFT and PRUNE control messages
- GossipSub peer scores
- IHAVE and IWANT control messages
- the recent IDONTWANT control messages

Sent and received messages
Protocol RPCs

This is a very valuable set of data to have, as it covers a large footprint of the behaviour of Gossipsub in a given network. Relatively simple data analysis can reveal very important metrics and inform engineers of the healthy (or not) operation of the protocol. For cases where Gossipsub serves as the block propagation protocol of a blockchain network, having deep insights into these metrics is critical!

## How have we used it so far

Hermes has helped the ProbeLab team carry out an extensive study on Gossipsub’s operation on the Ethereum network. Here are the links to the relevant [ethresear.ch](http://ethresear.ch/) posts:

- Gossip IWANT/IHAVE Effectiveness in Ethereum’s Gossipsusb network
- Gossipsub Network Dynamicity through GRAFTs and PRUNEs
- Number Duplicate Messages in Ethereum’s Gossipsub Network
- Ethereum Node Message Propagation Bandwidth Consumption
- Gossipsub Message Propagation Latency

Furthermore, it helped uncover bugs in the operation of Gossipsub across implementations and provided supporting evidence regarding the need for `IDONTWANT` message adoption.

## Future plans & how to contribute

Hermes is open-source - its Github repository is: [GitHub - probe-lab/hermes: A Gossipsub listener and tracer.](https://github.com/probe-lab/hermes). We welcome Github Issues to discuss with the community, receive feature requests and hear feedback. We also welcome Pull Requests to improve the tool and add features or support for other networks. If you are interested in data from other networks and would like Hermes to support those, [reach out](https://probelab.network/contact).

We hope you’ll enjoy playing around with Hermes. We would love to hear how you’ve used it and any improvements you’ve made.

[Originally posted at: [Hermes: A monitoring light node for GossipSub-based Networks - Blog | ProbeLab Analytics](https://www.probelab.network/blog/hermes-a-monitoring-light-node-for-gossipsub-based-networks)]

## Replies

**abcoathup** (2024-10-16):

Original blog post:


      ![](https://ethresear.ch/uploads/default/original/3X/f/5/f55b40b52263f4b865a4924563464520fc447cd1.svg)

      [ProbeLab Analytics – 21 Oct 24](https://probelab.io/blog/hermes-a-monitoring-light-node-for-gossipsub-based-networks/)



    ![](https://probelab.io)

###



Meet Hermes - a light node for the Ethereum network and hopefully soon for several others










[@yiannisbot](/u/yiannisbot) can you fix the link

---

**yiannisbot** (2024-10-16):

Apologies, fixed now. Thanks for the nudge ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

