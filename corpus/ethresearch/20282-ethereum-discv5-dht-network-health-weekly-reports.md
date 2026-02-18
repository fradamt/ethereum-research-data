---
source: ethresearch
topic_id: 20282
title: Ethereum discv5 DHT Network Health Weekly Reports
author: yiannisbot
date: "2024-08-15"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/ethereum-discv5-dht-network-health-weekly-reports/20282
views: 217
likes: 6
posts_count: 1
---

# Ethereum discv5 DHT Network Health Weekly Reports

> Work presented here has been carried out by the ProbeLab team and in particular @guillaumemichel @cortze @dennis-tra and Steph.

## High Level Description

The ProbeLab team has developed and deployed infrastructure to monitor several critical metrics for Ethereum’s CL discv5 DHT network. In particular, we have adapted the Nebula crawler ([GitHub - dennis-tra/nebula: 🌌 A network agnostic DHT crawler, monitor, and measurement tool that exposes timely information about DHT networks.](https://github.com/dennis-tra/nebula/)) to be compatible with discv5-based networks and are gathering results that reflect the health of the P2P network at the DHT level.

In this post we’re presenting a summary of what is included in the reports, but for a more complete picture of what’s there, head to: https://probelab.io/ethereum/discv5/2024-29/ for the latest report.

- Reports are produced every Monday for the preceding week.
- The methodology we follow for DHT Crawling, Data Filtering, Node Classification as well as the differences of our tool to alternatives in the space is given in the Methodology section: https://probelab.io/ethereum/discv5/methodology/.
- The crawler used to produce the reports can be found (and can be reused) here: GitHub - dennis-tra/nebula: 🌌 A network agnostic DHT crawler, monitor, and measurement tool that exposes timely information about DHT networks..

## Why you should care

The metrics included in the reports:

- give an overview of the network structure, size and client adoption breakdown. This helps in understanding the robustness and diversity of the network,
- provide accurate geographic distribution of nodes in the network per client implementation over time, which can highlight regional trends and potential vulnerabilities or strengths in specific areas,
- make it easy to spot drastic changes in the structure and setup of the network,
- allow for monitoring of new protocol version uptake/adoption, and provide insights on whether there are adoption barriers,
- reveal the infrastructure setup (e.g., data center-hosted vs non-data center-hosted) and cloud provider distribution per client implementation,
- show the breakdown of nodes supporting particular network-layer protocols,
- depict the percentage of reachable vs unreachable node records in the DHT network.

## Overview of Results

We’re presenting a small fraction of the results given at https://probelab.io to give an idea of the metrics listed. Please head there for the complete reports from Week 11 (mid-March), 2024.

**Client Diversity**

[![discv5-agents-overall](https://ethresear.ch/uploads/default/optimized/3X/4/3/433c4aecd269c5dfd9291dc03bbf58624414061c_2_489x375.png)discv5-agents-overall1568×1200 26.5 KB](https://ethresear.ch/uploads/default/433c4aecd269c5dfd9291dc03bbf58624414061c)

**Client Diversity Over Time**

[![discv5-agents-overall-stacked](https://ethresear.ch/uploads/default/optimized/3X/2/6/2664514f07b9b5aa0f4dea5319bc82fe047fa27b_2_489x375.png)discv5-agents-overall-stacked1568×1200 67.6 KB](https://ethresear.ch/uploads/default/2664514f07b9b5aa0f4dea5319bc82fe047fa27b)

**Agent version adoption over time - Example: Lighthouse**

[![discv5-versions-distribution](https://ethresear.ch/uploads/default/optimized/3X/a/0/a081c5b9376d2f17792caaa6b6d91b9f2e4353a0_2_489x375.png)discv5-versions-distribution1568×1200 80.1 KB](https://ethresear.ch/uploads/default/a081c5b9376d2f17792caaa6b6d91b9f2e4353a0)

[![discv5-agents-versions](https://ethresear.ch/uploads/default/optimized/3X/6/1/61739999c2d736e11817cf8f417008e2c88869dc_2_489x375.png)discv5-agents-versions1568×1200 27.8 KB](https://ethresear.ch/uploads/default/61739999c2d736e11817cf8f417008e2c88869dc)

**Country distribution of all nodes**

[![discv5-geo-agent-all-bars](https://ethresear.ch/uploads/default/optimized/3X/3/4/34aa9fb69b64bdf785073d62f018a4c78cbad033_2_489x375.png)discv5-geo-agent-all-bars1568×1200 28.3 KB](https://ethresear.ch/uploads/default/34aa9fb69b64bdf785073d62f018a4c78cbad033)

**Client-specific country distribution - Example: Prysm**

[![discv5-geo-agents-lines-prysm](https://ethresear.ch/uploads/default/optimized/3X/c/9/c92579370dcf03c6358536d0a358da2d79aeaa51_2_489x375.png)discv5-geo-agents-lines-prysm1568×1200 78.7 KB](https://ethresear.ch/uploads/default/c92579370dcf03c6358536d0a358da2d79aeaa51)

**Cloud provider distribution of all nodes**

[![discv5-cloud-agent-all-bars](https://ethresear.ch/uploads/default/optimized/3X/5/5/55ffef8626b07b1f21845591817184f663c7c88f_2_489x375.png)discv5-cloud-agent-all-bars1568×1200 44.7 KB](https://ethresear.ch/uploads/default/55ffef8626b07b1f21845591817184f663c7c88f)

**Cloud vs non-cloud distribution of nodes over time**

[![discv5-cloud-rate-agent-all-lines](https://ethresear.ch/uploads/default/optimized/3X/4/7/47638e6a177376cd847949f006ddd6ad91a73368_2_489x375.png)discv5-cloud-rate-agent-all-lines1568×1200 35.9 KB](https://ethresear.ch/uploads/default/47638e6a177376cd847949f006ddd6ad91a73368)

**Stale Peer Records over time**

[![discv5-stale-records-mainnet-stacked](https://ethresear.ch/uploads/default/optimized/3X/d/9/d941c8d07f12784b4d26214ce100dcfbb8f1e99e_2_489x375.png)discv5-stale-records-mainnet-stacked1568×1200 48.1 KB](https://ethresear.ch/uploads/default/d941c8d07f12784b4d26214ce100dcfbb8f1e99e)

## How to contribute

Overall, we believe this set of results give an accurate view of the structure and health of the discv5 DHT network. We hope you’ll find the reports useful.

If there are important metrics that you believe should be part of these weekly reports, comment below, or get in touch with the team: [probelab.network/contact](https://www.probelab.network/contact).
