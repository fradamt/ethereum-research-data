---
source: ethresearch
topic_id: 21102
title: QUIC Support Among Ethereum Consensus Layer Clients
author: guillaumemichel
date: "2024-11-28"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/quic-support-among-ethereum-consensus-layer-clients/21102
views: 508
likes: 7
posts_count: 1
---

# QUIC Support Among Ethereum Consensus Layer Clients

**TL;DR**: We ([ProbeLab](https://probelab.io)) analyzed the adoption of QUIC among Ethereum Consensus Layer (CL) clients using the Nebula Crawler. Approximately 42% of CL nodes support QUIC, primarily because Lighthouse has it enabled by default. While QUIC support is growing, mainly over IPv4, there’s minimal adoption over IPv6. This post details our findings and encourages monitoring future trends on [probelab.io](http://probelab.io).

---

The Ethereum network is continually evolving to improve performance, scalability, and security. One of the recent advancements is the integration of QUIC support in Ethereum Consensus Layer clients. This post examines the current state of QUIC adoption among these clients, based on data collected and analyzed using the Nebula Crawler on [probelab.io](http://probelab.io).

## Introduction to QUIC and libp2p

QUIC is a transport protocol built on top of UDP, designed to enhance the performance of connection-oriented applications. It offers several benefits:

- Reduced Latency: QUIC integrates the handshake processes, reducing connection establishment times.
- Improved Congestion Control: It adapts effectively to network conditions, enhancing throughput.
- Stream Multiplexing: Allows multiple streams within a single connection without head-of-line blocking.

In the Ethereum ecosystem, libp2p provides QUIC support, enabling Consensus Layer clients to leverage these advantages for peer-to-peer communication.

## Incorporating QUIC into Ethereum’s ENR

An open pull request recommends including QUIC entries in Ethereum Node Records (ENRs): [ethereum/consensus-specs#3644](https://github.com/ethereum/consensus-specs/pull/3644). Sigma Prime has been driving this initiative by adding QUIC addresses to ENRs proactively.

To facilitate this integration, we implemented ENR QUIC entry parsing in [go-ethereum](https://github.com/ethereum/go-ethereum): [ethereum/go-ethereum#30283](https://github.com/ethereum/go-ethereum/pull/30283). This enhancement allows clients like Prysm and tools like the Nebula Crawler to recognize and utilize QUIC addresses effectively.

## Data Collection Methodology

At ProbeLab, we conduct two crawls per hour of the Ethereum CL network using the Nebula Crawler. We are able to identify which clients support QUIC and quantify the number of nodes for each client. The Nebula Crawler achieves this by:

- Parsing ENRs: Extracting QUIC addresses present in the node records.
- Using libp2p’s Identify Protocol: Discovering QUIC addresses advertised by the node after opening a libp2p connection.

## Findings on QUIC Support

Our analysis reveals insightful trends in QUIC adoption among Ethereum CL clients. Below are the key observations, with full results available at [probelab.io](https://probelab.io/ethereum/discv5/2024-46/#discv5-quic-support-plot).

### Overall QUIC Support

- Total QUIC-enabled Nodes: Approximately 42% (~3,700 nodes) of the CL nodes support QUIC.
- Client Distribution: Out of these QUIC-supporting nodes, the vast majority are running Lighthouse.

[![all-nodes](https://ethresear.ch/uploads/default/optimized/3X/b/7/b74e093c7d745ae0143431f134bc7cd69477d5c7_2_489x375.png)all-nodes1568×1200 73.1 KB](https://ethresear.ch/uploads/default/b74e093c7d745ae0143431f134bc7cd69477d5c7)

### Client-Specific Insights

### Lighthouse

- QUIC Support: An impressive 98% (~3,600 nodes) of Lighthouse nodes have QUIC enabled. Lighthouse has QUIC support enabled by default.
- Observation: Lighthouse nodes constitute the majority of QUIC-supporting nodes in the CL network.

[![lighthouse](https://ethresear.ch/uploads/default/optimized/3X/4/1/4199a1bec6478bd55e3f58f8fa4a14a3d287552e_2_489x375.png)lighthouse1568×1200 72.5 KB](https://ethresear.ch/uploads/default/4199a1bec6478bd55e3f58f8fa4a14a3d287552e)

### Prysm

- QUIC Support: Around 2% (~75 nodes) of Prysm nodes support QUIC.
- Note: QUIC support isn’t enabled by default in Prysm, but the presence of these nodes is encouraging for future adoption.

[![prysm](https://ethresear.ch/uploads/default/optimized/3X/0/7/07f6ba2a90041d626df4cd63689d76e2be95ea95_2_489x375.png)prysm1568×1200 67.7 KB](https://ethresear.ch/uploads/default/07f6ba2a90041d626df4cd63689d76e2be95ea95)

### Grandine

- QUIC Support: All nodes are advertising QUIC addresses.
- Comment: Grandine has QUIC enabled by default since it uses Lighthouse network stack, but doesn’t constitute a significant portion of the network yet.

[![grandine](https://ethresear.ch/uploads/default/optimized/3X/2/c/2ca613916198d295e29411a662fb9339008d0ffa_2_489x375.png)grandine1568×1200 46 KB](https://ethresear.ch/uploads/default/2ca613916198d295e29411a662fb9339008d0ffa)

### Other Clients

- Clients: Teku, Nimbus, Lodestar, Erigon.
- QUIC Support: Currently, none of these clients support QUIC.
- Expectation: With recent spec changes, we expect that these clients will incorporate QUIC support in upcoming releases.

### QUIC over IPv6 vs. IPv4

Despite the growing support for QUIC, primarily due to Lighthouse, there are only a few nodes supporting QUIC over IPv6. The overwhelming majority of QUIC-enabled nodes operate over IPv4. This indicates an area for potential growth in IPv6 adoption.

## Conclusion and Future Outlook

The integration of QUIC into Ethereum’s networking stack represents a significant step toward enhanced network performance. While Lighthouse leads in adoption, we are encouraged by the initial support seen in Prysm and Grandine. As the specification matures, we anticipate broader adoption across other clients.

At ProbeLab, we will continue to monitor and report on QUIC adoption trends. Our [discv5 CL Weekly Reports](https://probelab.io/ethereum/discv5/) will provide ongoing insights, so we encourage stakeholders to stay tuned for further updates.

---

*For detailed data and interactive charts, please visit* [probelab.io](https://probelab.io/)*.*
