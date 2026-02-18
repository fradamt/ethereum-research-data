---
source: magicians
topic_id: 27403
title: Trustess Log Index Breakout #1, Jan 20, 2026
author: system
date: "2026-01-09"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/trustess-log-index-breakout-1-jan-20-2026/27403
views: 23
likes: 0
posts_count: 3
---

# Trustess Log Index Breakout #1, Jan 20, 2026

### Agenda

- Quick intro
- Questions and suggestions about the specs and the general design
- Discussion of simplified alternative design: eip-7745-simplified.md · GitHub
- Updates on implementation status, blocker issues
- Plans for cross-client testing

**Meeting Time:** Tuesday, January 20, 2026 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1869)

## Replies

**system** (2026-01-20):

### Meeting Summary:

The meeting focused on discussing a new proposal for implementing Ethereum Improvement Proposal (EIP) logging, which aims to address performance issues with the original implementation through a simpler and more efficient approach. The team explored various technical aspects of the new design, including data structures for log indexing, event handling, and search functionality, with detailed explanations of how the system would operate using sorted lists, binary trees, and hierarchical structures. While the new proposal offers improved performance and efficiency, the team acknowledged the need for better documentation and simpler explanations to make the complex design more accessible, with plans to continue discussions and review the proposal in the coming weeks.

**Click to expand detailed summary**

The meeting began with Zsolt and Tamaghna discussing the original EIP implementation and its challenges, including performance issues with log indexing and hash computations. Zsolt shared his efficient Go implementation of the original EIP, noting that while it could be optimized, the new proposal offers a simpler approach with reduced complexity. The group agreed to continue exploring the new proposal due to its advantages over the original, though Zsolt acknowledged that further work would be needed to make it production-ready.

Zsolt discussed the development of a new data structure for log indexing, which he began working on in early November. He explained that the original proposal aimed to minimize the state size of the log index, achieving a compact representation of around 20 megabytes with the proposed parameters. However, Zsolt recently published a simpler structure that might be more feasible, though it requires a larger minimal amount of data for consensus hashing. The new proposal can represent the index with position indexes and logs, but it still needs to be evaluated for performance compared to the original design.

Zsolt explained a method for generating and sorting log values, using a linear index space that assigns positions for addresses and topics. He shared a drawing and document to illustrate the concept, which involves a global index pointer that grows with each new log entry. Łukasz asked questions about the process, and Zsolt clarified that each log operation occupies four spaces in the linear index space, with an index entries tree referencing all events.

Zsolt explained the data structure for indexing events, which assigns unique positions to each event, including transactions, block boundaries, and log events. He described how the system uses sorted lists and a binary tree to facilitate value-based lookups and generate inclusion and exclusion proofs. Zsolt emphasized that while longer sorted lists would be more efficient for proofs, generating them in consensus is impractical due to the computational burden on clients.

The discussion focused on how reorganizations work with the new sorted lists structure, where Zsolt explained that operations can be performed in reverse by removing items from the index. They discussed the search functionality, with Zsolt describing how local representations can be efficiently stored using intermediate index chunks that form a search tree, allowing for faster lookups than binary search. The conversation also touched on the relationship between index entries and receipts, noting that local storage can reference positions directly rather than storing the full index entries tree.

Zsolt explained a new database design involving a tree structure of searchable chunks, where each chunk is hashed and sorted, allowing for logarithmic-time value lookups. Despite Zsolt’s detailed explanation, Łukasz struggled to understand the concept, prompting Zsolt to acknowledge the complexity of the design and his need to improve his explanation method, potentially with visual aids.

The team discussed the implementation of a tree-based data structure for efficient search and proof generation in Ethereum logs. Zsolt explained how the structure represents addresses and topics in a hierarchical manner, allowing for quick lookup and proof generation of index values. Łukasz focused on understanding the current functionality of the logs and suggested simplifying the explanation by using example addresses and topics. They agreed to focus on the current functionality of logs before delving into the proof generation aspect.

The team discussed a new design for handling log index references, replacing filter maps with merged sorted lists. Zsolt explained how the system works by creating lists of index positions for each topic, address, and transaction, which can then be matched against each other to find potential matches. Tamaghna raised a question about the size of the data structures, and Zsolt clarified that while the new design requires 2GB of RAM, the previous filter map system had a much smaller initialization size of 20MB. Zsolt also mentioned that the new design is simpler and more efficient for processing, though it requires more memory to initialize.

The team discussed a complex EIP proposal that Łukasz found difficult to understand due to its technical complexity and lack of clear documentation. Zsolt acknowledged the need to simplify the design and provide more step-by-step examples to make it more approachable. Tamaghna agreed to review the proposal further in two weeks to better understand the differences between the current and proposed data structures. The group decided to continue discussions and improve the documentation in the meantime.

### Next Steps:

- Zsolt: Create step-by-step examples with drawings showing how the log index lookup works, including how values are searched and combined
- Zsolt: Improve documentation to make the new proposal more approachable, with detailed walkthroughs of the data structures
- Zsolt: Create drawings explaining how the search tree of chunks works for local representation
- Zsolt: Document the three main parts: what happens on NewBlock , how search works, and exactly how proving works
- Tamaghna: Read up on the new alternative proposal to understand the differences compared to the previous data structure
- All participants: Review the new proposal and provide feedback between meetings
- Zsolt: Ping participants when new documentation material is available
- All participants: Schedule follow-up meeting in two weeks to discuss after everyone has reviewed the new proposal

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: D341==Hw)
- Download Chat (Passcode: D341==Hw)
- Download Audio (Passcode: D341==Hw)

---

**system** (2026-01-20):

YouTube recording available: https://youtu.be/MiEeqRj3N3E

