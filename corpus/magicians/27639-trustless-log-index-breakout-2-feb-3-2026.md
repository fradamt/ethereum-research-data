---
source: magicians
topic_id: 27639
title: Trustless Log Index Breakout #2, Feb 3, 2026
author: system
date: "2026-02-02"
category: Protocol Calls & happenings
tags: [breakout]
url: https://ethereum-magicians.org/t/trustless-log-index-breakout-2-feb-3-2026/27639
views: 23
likes: 0
posts_count: 3
---

# Trustless Log Index Breakout #2, Feb 3, 2026

### Agenda

- Presentation of the latest, further simplified log index proposal: eip-7745b.md · GitHub
- General Q&A
- Discussion: log index parameters, using a ZK-friendly hash function, etc (optional, if there is enough time)

**Meeting Time:** Tuesday, February 03, 2026 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1911)

## Replies

**system** (2026-02-03):

YouTube recording available: https://youtu.be/kXJfWaFsrfU

---

**system** (2026-02-03):

### Meeting Summary:

The team discussed a new data structure called index tables that efficiently stores and indexes events like block and transaction hashes through ordered lists and tree-hashing. They explored the efficiency of this approach compared to bloom filters for proving inclusion, with the new method demonstrating significant improvements in storage and processing efficiency. The discussion concluded with a review of a database design for storing and indexing receipts and log entries, focusing on chronological organization and proof generation methods.

**Click to expand detailed summary**

Zsolt presented a new data structure called index tables, which are ordered lists of events such as block hashes, transaction hashes, log addresses, or log topics. He explained how these tables are generated from blocks, sorted, and tree-hashed for efficient searching and proving. Łukasz suggested that the event type might not be necessary as it could be inferred from the block, transaction, or log data. Zsolt agreed this was a possibility and mentioned that in some cases, the transaction index or log index might not be applicable, leaving those fields as zeros in the encoding.

Zsolt presented a proposal for efficient log indexing and proof generation. He suggested using smaller tables (e.g., 64-block tables) in consensus and larger tables (up to millions of blocks) proven with zero-knowledge (ZK) proofs for long-term history. The system would allow efficient search and proof generation, with proof costs ranging from 1 kilobyte for a single exclusion proof to around 40 kilobytes for a full history proof. Zsolt emphasized that this approach balances update efficiency with long-term history storage, avoiding the high complexity of his original proposal.

The discussion focused on comparing the efficiency of a new data structure with bloom filters for proving inclusion of certain criteria. Łukasz explained that their new approach is more efficient than current bloom filters, as it can handle 10 million blocks in a single kilobyte, while a 100,000-bit bloom filter would still require 100,000 bits per block. Zsolt clarified that inclusion proofs are generally easier than proving complete sets of matches, and Łukasz confirmed that their new method is significantly more efficient than any bloom-filter-based design they have considered.

The team discussed a database design for storing and indexing receipts and log entries. Zsolt explained that while previous versions used a linear log value index, the current design simplifies storage by using actual receipts for inclusion proofs and organizing data chronologically and by content. They agreed that while deduplication could be implemented locally for efficiency, it wasn’t necessary for consensus generation. The discussion concluded with Sixto confirming the complexity of the design was manageable.

### Next Steps:

- Zsolt: work on presentation skills
- Zsolt: present this proposal multiple times
- Zsolt: figure out the optimum number of blocks for consensus tables
- Zsolt: determine the most ZK-friendly hash functions for the hashing scheme
- Zsolt: finalize the 64 byte encoding optimization for efficiency
- Zsolt: add proof cost calculations to the slides
- Zsolt: figure out how bigger tables with ZK proofs will be generated and shared

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: i%7+4H1s)
- Download Chat (Passcode: i%7+4H1s)
- Download Audio (Passcode: i%7+4H1s)

