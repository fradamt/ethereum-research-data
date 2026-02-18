---
source: magicians
topic_id: 8971
title: "Proposal: Distributed ledger database to reduce the data storage requirements"
author: aicetea
date: "2022-04-20"
category: EIPs > EIPs core
tags: [database]
url: https://ethereum-magicians.org/t/proposal-distributed-ledger-database-to-reduce-the-data-storage-requirements/8971
views: 600
likes: 0
posts_count: 1
---

# Proposal: Distributed ledger database to reduce the data storage requirements

eip:

title: Rotura ledger database

description: Sync data to distributed database in real time to reduce the storage requirements for nodes

author: Larry Liu [@AIcetea](/u/aicetea) [AIcetea (Larry Liu) · GitHub](https://github.com/AIcetea)

discussions-to: [Proposal: Distributed ledger database to reduce the data storage requirements](https://ethereum-magicians.org/t/proposal-a-new-distributed-ledger-database/8971)

status: Draft

type: Standard Track

category (*only required for Standards Track): Core

created: 2022-04-19

requires (*optional):

**ABSTRACT**

Rotura Ledger Database introduces a whole new architecture for blockchain and decentralized web. The technology brings reliability, performance and scalability. The blockchain will be limited by its storage. The developer will be equipped with a powerful arsenal to build more powerful web3 application. The RLDB will become the center of the data for the whole world.

**Motivation**

In most of blockchains, the ledger related data is stored in levelDB which is a KV store. In general all blockchain nodes need to store all the ledger data locally. Each node has limit storage but the ledger grows with no limit. Besides, each block and transaction need to be broadcasted throughout the network in order to get verified and added to blockchain. This causes the major performance issue that a lot of talented engineers and scientists are trying to improve since blockchain was born.

In current decentralized environment, the network, node are not reliable. So the data is not kept safely. And if the network is available – great! All goes as expected. But of course, we all know we can never expect the network to always work. Once you start experiencing slow networks, then you start experiencing slow apps. So while the network can contribute to the problem, what this really is is a data locality problem.

As we all know about the blockchain trilemma. The blockchain trilemma is a concept coined by Vitalik Buterin that proposes a set of three main issues **decentralization** , **security and scalability** that developers encounter when building blockchains, forcing them to ultimately sacrifice one “aspect” for as a trade off to accommodate the other two.

Overall, the current blockchain storage solution is a waste of storage, slow and badly architected. It is becoming the limitation for the current and future development of blockchain.

**Specification**

***Data Strategy***

The data location strategy is unique and the solution for blockchain to store the ledger data. You need data local, which you get with RLDB Lite. And you need data remote, which you get with RLDB cluster. And you need something that’s going to keep those two data stores in sync, which you get with Gateway.

***Embedded Database - RLDB Lite***

RLDB Lite is an embedded, NoSQL JSON Document Style database.

***Work locally***

- RLDB Lite is designed to work with data stored locally and includes

The ability to write queries with semantics based on SQL
- Full-Text Search queries on documents stored locally.
- The ability to store document attachments (blobs), for example images or PDF files.

***Sync at the peer***

- It manages data sync automatically through:

A replication protocol built over WebSockets to synchronize data with Gateway.
- A Peer-to-Peer sync implementation to synchronize data between RLDB Lite clients

**Sync - Gateway**

Gateway is the synchronization server in RLDB for blockchain node deployment. It is designed to provide data synchronization for blockchain and web3 applications.

Sync Gateway assures secure access control using:

- User authentication , which ensures that only authorized users can connect to Gateway.
- Data Routing , which ensures that authorized users can only access documents in those Channels assigned to them and only in accordance with their assigned privileges. You can set those privileges to confer Read Access and-or Write Access as required.

Gateway is also responsible to get the full topology of the RLDB network. It determines the which RLDB cluster to connect based on multiple metrics.
