---
source: magicians
topic_id: 25327
title: QMDB Breakout Call #1, September 8, 2025
author: system
date: "2025-09-02"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/qmdb-breakout-call-1-september-8-2025/25327
views: 73
likes: 0
posts_count: 3
---

# QMDB Breakout Call #1, September 8, 2025

### Agenda

- Presentation about QMDB (Quick Merkle Database) for client devs

**Meeting Time:** Monday, September 08, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1711)

## Replies

**system** (2025-09-08):

### Meeting Summary:

The meeting focused on presenting Qmdb, a new database proposal developed by Layer 0’s research team to address state root amplification challenges in decentralized blockchains. The team discussed Qmdb’s technical features, including its binary tree data structure and optimization strategies, while comparing its performance and storage capabilities against existing solutions like MPT and LevelDB. The discussion concluded with exploring potential migration paths to Qmdb-style formats and addressing concerns about proof systems and historical state verification.

**Click to expand detailed summary**

The meeting began with Sina introducing the purpose of the call, which was to gather information about Qmdb, an exciting proposal. Sina mentioned that the authors of the Qmdb paper and the prototype’s authors were present, along with people from different EL clients and researchers. Raz then took over to present Qmdb, explaining that it was developed by a research team at Layer 0, led by Isaac and Raz, who emphasized their commitment to decentralization.

Raz discussed the challenges of state root amplification in decentralized blockchains, explaining how it leads to I/O bottlenecks and reduced performance. He highlighted that while current solutions like MPT and OMT mitigate the issue, they do not eliminate it. Raz proposed a new approach of using a log-based, append-only database to address this problem, as it would better suit the capabilities of SSDs by reducing random writes and enabling batch sequential writing.

Raz discussed a database optimization strategy involving a binary tree data structure. He explained the use of a binary tree data structure, which includes a fixed-depth binary tree, which is a variation of Merkel mountain range, which is optimized for data storage. The binary tree structure allows for a binary tree data structure, which is a variation of Merkel mountain range, which is optimized for data storage. The binary tree data structure is filled with binary data, and once it’s full, it becomes immutable. The binary tree data structure is filled with binary data, and once it’s full, it becomes immutable.

Raz presented an overview of Qmdb, highlighting its key features and functionalities. He explained that Qmdb is designed to optimize performance and efficiency, offering a unified approach to database management. The discussion emphasized the benefits of the system, including its ability to handle large-scale data and the potential for future growth. The system’s potential for future growth was also discussed, with a focus on its ability to handle large-scale data and the potential for future growth.

The discussion focused on Qmdb, a proposed replacement for both the Merkle Patricia trie and underlying key-value database in Ethereum, which would require a consensus change via the EIP process. Isaac explained that while Qmdb still needs an in-memory indexer, a hybrid approach could reduce memory footprint by reading most data from disk, achieving 6,300 updates per second with 15 billion entries, and the memory cost 2-3 bytes per entry. The conversation also addressed concerns about compaction, with Isaac noting that the compression is sequential and the data is stored in a sequential manner, which is much lighter than the data structure of RocksDB.

The discussion focused on the performance and storage implications of maintaining an index in persistent storage, with Isaac suggesting that while there would be some overhead from existing systems, it wasn’t a major concern and multiple indexing solutions could be explored. They discussed the simplicity and efficiency of the QMDB system, emphasizing its potential for future applications. The discussion also covered the importance of historical node querying for Ethereum’s settlement, highlighting its role in reducing artificial synchrony bounds. Lightclient clarified that Ethereum’s historical state access is not limited to the last 2,256 blocks, thanks to the beacon chain’s historical root accumulator.

The group discussed the challenges and considerations of storing historical state data, comparing QMDB and MPT approaches. They explored the differences in proof systems, with Sina noting that QMDB allows for easier historical verification proofs, while full nodes can verify transactions. Isaac clarified that full nodes only need the latest state to verify the current transactions.

The team discussed pruning logic and reorganization handling in the blockchain system. Isaac explained that pruning occurs in two layers: the compassion layer for cleaning up entries and the tweak layer for operations. He also explained that the system only considers transactions after the finalization of blocks, and transactions are stored in memory for further processing. The team also discussed the process of proving historical state and the cost of operations.

Raz, Sina, and others discussed the simplification of their data structure, which has been optimized for performance and scalability. They highlighted that their hybrid indexer is six times faster than previous solutions and can handle up to 280 billion entries on a single server, far exceeding the capabilities of other databases. Sina raised concerns about state expiry in Ethereum, and Raz explained that this could be managed similarly to how it would work in QMDB, requiring application-level logic to delete expired states. Raz also mentioned the potential for synergy in supporting state expiry at a lower level, which Isaac noted as an interesting area to explore.

The team discussed the advantages of Qmdb over MPT, including its uniform constraint system, balanced tree structure, and improved proofing efficiency. Isaac explained that Qmdb allows for smaller block proofs, which can enhance latency and reduce financial settlement times. The group also touched on the potential for integrating Qmdb into existing clients, with Raz mentioning a prototype implementation that achieved 1 million TPS on EVM. The discussion concluded with a brief exploration of exclusion proofs and the possibility of benchmarking ZK components against MPT for comparison.

The team discussed concerns about the self-contained nature of a proof related to index structures. Csaba expressed a feeling that he could build a contradictory proof, which he planned to present the following week. The group explored the implications of assuming ordered indices and debated the potential for creating invalid structures. Isaac offered to help formalize the proof in writing after the call, as it was difficult to discuss verbally.

The team discussed QMDB, a high-performance key-value database, as a potential alternative to their current LevelDB implementation. Sina explained that Gary had been investigating QMDB to address performance limitations, and the team agreed it would be beneficial to migrate Ethereum to QMDB-style formats. Isaac and Raz offered to provide support and share open-source code, while Isaac also explained the similarities between QMDB and Aztec’s indexed merkle tree. The team agreed to follow up if they needed further assistance with the migration process.

### Next Steps:

- Gary to continue investigating Qmdb as a potential solution for the key-value database limitations in Ethereum clients.
- Csaba and Isaac to follow up offline about the proof validation concerns raised during the meeting.
- Kev to benchmark the ZK components of Qmdb and compare against MPT.
- Raz and Isaac to be available for further questions and assistance if the Ethereum team decides to pursue Qmdb implementation.
- The unnamed team  to continue their work on integrating Qmdb into Reth.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: kAF6m$9X)
- Download Chat (Passcode: kAF6m$9X)

---

**system** (2025-09-09):

### Meeting Summary:

The meeting focused on presenting Qmdb, a new database proposal developed by Layer 0’s research team to address state root amplification challenges in decentralized blockchains. The team discussed Qmdb’s technical features, including its binary tree data structure and optimization strategies, while comparing its performance and storage capabilities against existing solutions like MPT and LevelDB. The discussion concluded with exploring potential migration paths to Qmdb-style formats and addressing concerns about proof systems and historical state verification.

**Click to expand detailed summary**

The meeting began with Sina introducing the purpose of the call, which was to gather information about Qmdb, an exciting proposal. Sina mentioned that the authors of the Qmdb paper and the prototype’s authors were present, along with people from different EL clients and researchers. Raz then took over to present Qmdb, explaining that it was developed by a research team at Layer 0, led by Isaac and Raz, who emphasized their commitment to decentralization.

Raz discussed the challenges of state root amplification in decentralized blockchains, explaining how it leads to I/O bottlenecks and reduced performance. He highlighted that while current solutions like MPT and OMT mitigate the issue, they do not eliminate it. Raz proposed a new approach of using a log-based, append-only database to address this problem, as it would better suit the capabilities of SSDs by reducing random writes and enabling batch sequential writing.

Raz discussed a database optimization strategy involving a binary tree data structure. He explained the use of a binary tree data structure, which includes a fixed-depth binary tree, which is a variation of Merkel mountain range, which is optimized for data storage. The binary tree structure allows for a binary tree data structure, which is a variation of Merkel mountain range, which is optimized for data storage. The binary tree data structure is filled with binary data, and once it’s full, it becomes immutable. The binary tree data structure is filled with binary data, and once it’s full, it becomes immutable.

Raz presented an overview of Qmdb, highlighting its key features and functionalities. He explained that Qmdb is designed to optimize performance and efficiency, offering a unified approach to database management. The discussion emphasized the benefits of the system, including its ability to handle large-scale data and the potential for future growth. The system’s potential for future growth was also discussed, with a focus on its ability to handle large-scale data and the potential for future growth.

The discussion focused on Qmdb, a proposed replacement for both the Merkle Patricia trie and underlying key-value database in Ethereum, which would require a consensus change via the EIP process. Isaac explained that while Qmdb still needs an in-memory indexer, a hybrid approach could reduce memory footprint by reading most data from disk, achieving 6,300 updates per second with 15 billion entries, and the memory cost 2-3 bytes per entry. The conversation also addressed concerns about compaction, with Isaac noting that the compression is sequential and the data is stored in a sequential manner, which is much lighter than the data structure of RocksDB.

The discussion focused on the performance and storage implications of maintaining an index in persistent storage, with Isaac suggesting that while there would be some overhead from existing systems, it wasn’t a major concern and multiple indexing solutions could be explored. They discussed the simplicity and efficiency of the QMDB system, emphasizing its potential for future applications. The discussion also covered the importance of historical node querying for Ethereum’s settlement, highlighting its role in reducing artificial synchrony bounds. Lightclient clarified that Ethereum’s historical state access is not limited to the last 2,256 blocks, thanks to the beacon chain’s historical root accumulator.

The group discussed the challenges and considerations of storing historical state data, comparing QMDB and MPT approaches. They explored the differences in proof systems, with Sina noting that QMDB allows for easier historical verification proofs, while full nodes can verify transactions. Isaac clarified that full nodes only need the latest state to verify the current transactions.

The team discussed pruning logic and reorganization handling in the blockchain system. Isaac explained that pruning occurs in two layers: the compassion layer for cleaning up entries and the tweak layer for operations. He also explained that the system only considers transactions after the finalization of blocks, and transactions are stored in memory for further processing. The team also discussed the process of proving historical state and the cost of operations.

Raz, Sina, and others discussed the simplification of their data structure, which has been optimized for performance and scalability. They highlighted that their hybrid indexer is six times faster than previous solutions and can handle up to 280 billion entries on a single server, far exceeding the capabilities of other databases. Sina raised concerns about state expiry in Ethereum, and Raz explained that this could be managed similarly to how it would work in QMDB, requiring application-level logic to delete expired states. Raz also mentioned the potential for synergy in supporting state expiry at a lower level, which Isaac noted as an interesting area to explore.

The team discussed the advantages of Qmdb over MPT, including its uniform constraint system, balanced tree structure, and improved proofing efficiency. Isaac explained that Qmdb allows for smaller block proofs, which can enhance latency and reduce financial settlement times. The group also touched on the potential for integrating Qmdb into existing clients, with Raz mentioning a prototype implementation that achieved 1 million TPS on EVM. The discussion concluded with a brief exploration of exclusion proofs and the possibility of benchmarking ZK components against MPT for comparison.

The team discussed concerns about the self-contained nature of a proof related to index structures. Csaba expressed a feeling that he could build a contradictory proof, which he planned to present the following week. The group explored the implications of assuming ordered indices and debated the potential for creating invalid structures. Isaac offered to help formalize the proof in writing after the call, as it was difficult to discuss verbally.

The team discussed QMDB, a high-performance key-value database, as a potential alternative to their current LevelDB implementation. Sina explained that Gary had been investigating QMDB to address performance limitations, and the team agreed it would be beneficial to migrate Ethereum to QMDB-style formats. Isaac and Raz offered to provide support and share open-source code, while Isaac also explained the similarities between QMDB and Aztec’s indexed merkle tree. The team agreed to follow up if they needed further assistance with the migration process.

### Next Steps:

- Gary to continue investigating Qmdb as a potential solution for the key-value database limitations in Ethereum clients.
- Csaba and Isaac to follow up offline about the proof validation concerns raised during the meeting.
- Kev to benchmark the ZK components of Qmdb and compare against MPT.
- Raz and Isaac to be available for further questions and assistance if the Ethereum team decides to pursue Qmdb implementation.
- The unnamed team  to continue their work on integrating Qmdb into Reth.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: kAF6m$9X)
- Download Chat (Passcode: kAF6m$9X)

