---
source: magicians
topic_id: 25400
title: PQ Interop #9, September 10, 2025
author: system
date: "2025-09-09"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/pq-interop-9-september-10-2025/25400
views: 127
likes: 0
posts_count: 2
---

# PQ Interop #9, September 10, 2025

### Agenda

- leanView related to Build a visualization app for devnet · Issue #40 · leanEthereum/pm · GitHub (Jun)
- Grafana update (Guillaume)
- leanSSZ (Thomas) leanSpec/src/lean_spec/subspecs/ssz at main · leanEthereum/leanSpec · GitHub
- Quadrivium updates (Kamil) GitHub - qdrvm/qlean-mini: Lean Ethereum PQ devnet client implementation in C++
- Devnet-0 spec one pager

This needs to be updated w/ a list of Functionality/spec PRs + spec test version

Devnet-0 update
Devnet-1 spec update

**Meeting Time:** Wednesday, September 10, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1722)

## Replies

**system** (2025-09-10):

### Meeting Summary:

The team discussed the development of a Rust client for upcoming PQ devnets and reviewed a web application called Link View that provides a dashboard for blockchain network interaction. They explored various technical aspects including Zoom node integration, monitoring application development, and endpoint specifications, while also discussing progress on interop testing between different clients. The conversation ended with updates on various ongoing projects and a discussion about creating a consolidated document for Devnet 0 specifications and testing information.

**Click to expand detailed summary**

The team discussed the development of a Rust client for upcoming PQ devnets, with Jun presenting a demo of the leanView project. Will mentioned that they are working on specs for devnet 0 and moving towards devnet 1, with the goal of having a live devnet 0 in the near future. The team also briefly touched on the importance of collaboration and communication in their development process.

Jun presented a web application called Link View that provides a dashboard for developers and researchers to interact with a blockchain network. The app is built on a Go backend and React frontend, with functionality to display live network status and historical data. Jun demonstrated the app’s current features, which include endpoint monitoring and a basic blockchain explorer interface, and invited feedback on potential additional features and improvements.

The team discussed adding Zoom node integration to an explorer interface. Jun explained that the explorer can handle large node networks and will include specialized features for the PQ Devnet, such as signatures and aggregate signatures in future versions. Guillaume inquired about creating mock endpoints to test functionality, and Jun confirmed that empty responses from nodes would be handled appropriately by the explorer. The team agreed to start with basic HTTP endpoints and build up functionality over time, with Jun requesting only one or more endpoints running Zoom nodes that are compatible with the existing RPC structures and responses.

The team discussed the development of a monitoring application, focusing on optimizing performance for handling multiple nodes. Jun explained plans to separate the monitoring page into a new page to reduce load on other clients and mentioned the need for further optimization. Mercy inquired about the endpoints for the project, and Jun clarified that four endpoints, including block, block header, versions, and state, would be necessary for the current phase. Gajinder suggested focusing on determining the head of each node using Traceroute, as it might not be necessary to implement 3SF in the tool. Jun agreed to share a document outlining the endpoint definitions to aid in implementing the RPC.

The team discussed several updates and ongoing projects. Jun mentioned sending a Zoom link and being available for questions via DM. Guillaume reported progress on setting up a Grafana instance with Victoria metrics, which should be ready by the next day. Thomas provided an update on work with Felipe on lean SSZ things, including implementing types in Python with modern practices. Kamil shared information about the qlean-mini devnet client, which is written in C++ and has block production capabilities. The team also discussed interop testing and potential naming changes for the qlean client. Will concluded by mentioning a one-pager document for the next meeting.

Will proposed creating a document to consolidate information about Devnet 0, following a design pattern used in the primary ACD repo. He suggested gathering links to relevant specs, PRs, and test versions, and tracking interoperability between clients. Gajinder agreed this document would be useful as a starting point for anyone interested in the test specs or client participation. They discussed extracting functionality details from the lean specs repo and potentially maintaining this information in both locations. Will expressed willingness to update the document regularly, noting it would become increasingly important as they focus more on interoperability.

The team discussed progress on interop between Reem and Zoom, with Gajinder reporting that the Genesis file generator is ready and implementation of Fokchoice changes is near completion. Jun and Cassandra shared updates on the Lachain spec implementation, which is nearly done on the Ring side with only optimization work remaining. The team agreed to develop a simple shell tool using Docker images to spin up nodes for local interop testing, with Kamil suggesting the use of shadow compatibility for network simulation. They decided to postpone the full implementation of Kurtosis for 2-3 weeks while focusing on basic interop testing, with plans to add Lean view to the testing environment.

The team discussed the status of a PR that Jun confirmed could be merged by Friday, with Gajinder reviewing the implementation and making minor changes to the specification over the next few days. Will noted that the team was “hitting our stride” and mentioned that they were seeing “early growing pains,” while expressing optimism about their future progress. The conversation ended with Will welcoming new participants and expressing confidence that the team would “start turning some heads soon.”

### Next Steps:

- Jun to share clean documentation about the definition of endpoints used in Lean View with Zoom team.
- Guillaume to test and finalize the Grafana instance setup by tomorrow.
- Will to update the Devnet 0 one-pager with links to all pertinent information, spec sections, and PRs.
- Gajinder to share research on node configuration files and ENR generation with Jun for local interop.
- Gajinder to aim to merge the forks PR by Friday.
- Zoom and Reem teams to start figuring out interop between their clients next week.
- Client teams to work on implementing a shell tool for spinning up nodes in Docker for local interop testing.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: cfCJ6?#%)
- Download Chat (Passcode: cfCJ6?#%)

