---
source: magicians
topic_id: 24583
title: Portal Implementers Call | call #57 | June 20, 2025
author: system
date: "2025-06-18"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-call-57-june-20-2025/24583
views: 116
likes: 2
posts_count: 2
---

# Portal Implementers Call | call #57 | June 20, 2025

# Portal Implementers Call #57, June 20, 2025

- June 20 2025, 12:30 UTC
- Meeting link: shared in EthR&D#portal-dev

# Agenda

- Present proposal for EL-focused history subprotocol
- Discuss future other Portal subprotocols and infrastructure

 **🤖 config**

- Duration in minutes : 60min
- Recurring meeting : false
- Already a Zoom meeting ID : false # Set to true if you bring your own link – WARNING the bot will not create a zoom ID and a summary or a Youtube video – (make sure your zoom link meeting is auto recording you’ll have to handle this yourself)
- Already on Ethereum Calendar : false # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- display zoom link in invite : true # Set to true to add the Zoom link to the Google Calendar invite description



[GitHub Issue](https://github.com/ethereum/pm/issues/1578)

## Replies

**system** (2025-06-20):

### Meeting Summary:

The meeting focused on refocusing the Portal protocol, prioritizing the integration of its history component into execution clients and simplifying its implementation. Discussions covered technical aspects of the protocol, including content retrieval methods, network structure, and potential improvements to enhance efficiency and scalability. The team also addressed development priorities, testing strategies, and plans for community involvement in creating a production-ready network.

**Click to expand detailed summary**

The team discussed the future of the Portal protocol following the Ethereum Foundation’s layoff of a large portion of the Portal team. They decided to focus on integrating the history portion of the protocol directly into execution clients, rather than maintaining standalone Portal clients. This approach aims to provide immediate value to the execution layer by simplifying the protocol and reducing the need for separate modules like beacon chain and state protocols. The team acknowledged that while they cannot develop all aspects of Portal to the same standards, they need to prioritize the most critical features for execution clients.

The group discussed the refocusing of the Portal Protocol, with Felix explaining that it is being developed as a potential future peer-to-peer protocol for the execution layer, particularly for block body and receipt retrieval. Justin from the Besu team noted a gap in making execution clients able to leverage Portal, and Felix clarified that Portal cannot be implemented on TCP like existing protocols, requiring a different approach. The discussion also touched on concerns about range queries and Turing completeness, with Felix mentioning that Milos has documented proposed changes to the history protocol to address these issues.

The discussion focused on comparing the Portal network protocol with the existing DevP2P protocol, highlighting Portal’s ability to query multiple nodes concurrently and its dynamic sharding system. Felix explained that while full chain synchronization speed is not a current priority, Portal offers better content availability guarantees compared to a simple bit field approach. Kim and FLCL raised concerns about the complexity of implementing sharding without Portal’s advantages, and lightclient suggested focusing on Portal’s core functionality before adding advanced features like state networks and decentralized RPC support for light clients.

The team discussed the development priorities for the portal protocol, focusing on implementing a history sub-protocol before considering range queries. They explored the possibility of creating a testnet environment, with Kim confirming that existing nodes would remain operational for development purposes. Milos presented a research post on the direction of the project’s development, which he planned to share in more detail later. The team also discussed the potential for range requests and the need to redistribute data in the network for this feature.

The team discussed the creation of a new subnetwork for finalized content, distinct from the existing history network. Milos explained that this new subnetwork would focus on storing finalized bodies and receipts without headers, primarily serving execution layer clients. The team also discussed the use of protocol IDs and network identification methods, with Kim and Felix raising concerns about the limitations of current approaches. Finally, they noted that while progress had been made on integration through a Besu plugin by the Samba team, some members of the Besu team were interested in reevaluating their approach to the integration.

Milos explained a method for converting block numbers to content IDs using bit manipulation and a cycle-based approach, where block numbers are split into cycles of 65,536. He demonstrated how this system interleave content across different cycles to optimize storage and retrieval. The discussion concluded with a question about syncing near-head EL nodes post-rolling window, where options for using recent era entries or portal history network were considered.

Milos discussed a protocol for storing and retrieving content in a peer-to-peer network, focusing on batch queries and range queries to improve efficiency. He explained that the protocol currently doesn’t support fetching more than one content piece at a time, but potential extensions could allow for batch operations. Milos also addressed the naming of the network and the potential need to limit data injection to prevent overloading the network. Kim suggested defining a radius for data injection to manage network load, and Milos explained that standalone clients might need a different approach for content retrieval. The discussion concluded with a brief overview of the SOR metric for node IDs and content retrieval, noting that it maintains consistency across the network.

The team discussed changes to the Portal network, focusing on reducing its scope to prioritize the history component and aiming for a production-ready network with community involvement. Felix explained that testing methods would need to change, as standalone portal clients will no longer be developed, and integration with execution layer clients will require synthetic network tests. The team identified three clients (Java, Go, and Nimbus) for continued development, with plans to schedule meetings with Shizui and discuss Java client integration with Besu. They agreed to maintain the current specs repo for now, with plans to move Portal specs to the devp repo in the future, and decided to use a more ad-hoc meeting schedule moving forward.

### Next Steps:

- Milos to publish the updated spec for the finalized chain history portal sub-network on EthResearch.
- Felix to schedule a meeting next week with Shizui to discuss ongoing integration plans.
- Simon and Besu team to discuss and figure out the integration plans for the Java client with Besu.
- Felix to check the Portal Discord server regularly for updates and discussions.
- Portal team to continue iterating on the current specs repo for now, with a long-term plan to move Portal specs into the devp2p repo.
- Portal team to schedule focused meetings on specific topics as needed, such as content ID changes.
- Portal team to use async communication in Portal Dev channel and ad-hoc calls for coordination going forward.
- Execution client teams to consider integrating Portal network functionality into their clients.
- Kim and Nimbus team to continue work on the history network integration.
- Portal team to explore solutions for injecting new data into the network without overloading it.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: BSH=#78V)
- Download Chat (Passcode: BSH=#78V)

