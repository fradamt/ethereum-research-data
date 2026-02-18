---
source: magicians
topic_id: 24357
title: "[EIP] RPC Provider Capacity and Service Advertisement"
author: peersky
date: "2025-05-28"
category: EIPs
tags: [interfaces]
url: https://ethereum-magicians.org/t/eip-rpc-provider-capacity-and-service-advertisement/24357
views: 36
likes: 0
posts_count: 2
---

# [EIP] RPC Provider Capacity and Service Advertisement

This EIP proposes a standard mechanism for Ethereum RPC (Remote Procedure Call) providers, including Internet Service Providers (ISPs) or individual network hops, to advertise their RPC service endpoints and their current operational capacity. It defines discovery methods using DNS-based Service Discovery (DNS-SD) for domain-based lookups, and direct IP address querying for IP-specific lookups. It also specifies a schema for a machine-readable Capacity Information API endpoint that provides details about available RPC services, their capabilities, and real-time capacity metrics.

## Replies

**peersky** (2025-05-28):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9832/)














####


      `master` ← `peersky:master`




          opened 12:28AM - 28 May 25 UTC



          [![](https://avatars.githubusercontent.com/u/61459744?v=4)
            peersky](https://github.com/peersky)



          [+192
            -0](https://github.com/ethereum/EIPs/pull/9832/files)







This commit introduces a new EIP that outlines a standard mechanism for Ethereum[…](https://github.com/ethereum/EIPs/pull/9832) RPC providers to advertise their service endpoints and operational capacity. It includes discovery methods using DNS-based Service Discovery and direct IP address querying, along with a structured Capacity Information API for real-time metrics. The EIP aims to enhance decentralization, improve user choice, and reduce reliance on centralized endpoints.

