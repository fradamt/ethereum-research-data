---
source: ethresearch
topic_id: 20488
title: "The Portable Web: Hackable, No Data Lock-in, and Crypto-native Web World"
author: fjm2u
date: "2024-09-25"
category: Applications
tags: []
url: https://ethresear.ch/t/the-portable-web-hackable-no-data-lock-in-and-crypto-native-web-world/20488
views: 221
likes: 1
posts_count: 1
---

# The Portable Web: Hackable, No Data Lock-in, and Crypto-native Web World

# About this post

[![Comparison of Web Paradigms: Privacy, User Rights, and Monopoly](https://ethresear.ch/uploads/default/optimized/3X/7/7/7736a1481d1296569277c270b8dc598d5fb8e52d_2_690x353.png)Comparison of Web Paradigms: Privacy, User Rights, and Monopoly1786×914 67.1 KB](https://ethresear.ch/uploads/default/7736a1481d1296569277c270b8dc598d5fb8e52d)

In the current web environment, users find it difficult to manage their own data and are often locked into specific services. The **Portable Web** operates as a parallel web alongside the existing one, aiming to provide users with greater control over their data and the ability to make choices. Applications on the Portable Web are primarily envisioned to serve as public infrastructure.

In this post, I will introduce the core ideas of the Portable Web. Detailed specifications unrelated to its feasibility are not included. This is still a rough draft, but I’m submitting this because if I waited for it to be perfect, I’d never finish.

# Summary

[![Cluster Architecture Overview](https://ethresear.ch/uploads/default/optimized/3X/b/4/b45eddabc00a7701fa71566c6cb4ae00604da350_2_690x389.png)Cluster Architecture Overview2000×1128 246 KB](https://ethresear.ch/uploads/default/b45eddabc00a7701fa71566c6cb4ae00604da350)

[![An Example of Incentive Mechanisms in the Portable Web](https://ethresear.ch/uploads/default/optimized/3X/6/7/67bcae0547fa80eec667beeca99468609b846e79_2_690x359.png)An Example of Incentive Mechanisms in the Portable Web1846×962 85.7 KB](https://ethresear.ch/uploads/default/67bcae0547fa80eec667beeca99468609b846e79)

- Hackable: Users Can Customize Web Applications

A cluster represents a single application unit.
- Anyone can create a cluster, and within the cluster, entities other than the creator can create their own clients, provide servers, define API schemas, and write migration scripts.
- Clients and servers are loosely coupled and connected through an API schema, allowing different developers to create them independently.
- For example, users can create customized UIs to tailor applications to their specific needs, making them easier to use. Additionally, they can develop their own API schemas and host servers to extend particular features. In this way, the Portable Web allows not only developers but also regular users to actively contribute to the evolution of applications.

**No Data Lock-In: Users Have Control Over Their Data**

- A client caches the user’s data.
- By using a server that conforms to the API schema, clients can share cached data across different servers.
- Cached data on a client can also be migrated using migration scripts.
- A client caches the data that a user sends and receives, but by transmitting this data to a server chosen by the user, it is managed in a decentralized manner. If needed, users can migrate their data to other servers, ensuring that their data is not locked into any particular entity.

**Crypto-Native: Crypto-Economics as an Incentive Mechanism**

- In the Portable Web, cluster providers issue tokens and are incentivized by offering clusters that create real demand for those tokens.
- All payments within a cluster are made using the issued tokens.
- The presence of new participants contributes to the growth of the cluster, so the original cluster providers do not exclude them.
- While Web2 operates as a monopoly and winner-takes-all game, the Portable Web promotes a collaborative and inclusive approach.

# Background

## Web2

The Web3 community has extensively discussed the problems of Web2, so I won’t delve deeply into that here. However, it is important to emphasize that **the root of Web2’s problems lies in its architecture**—specifically, the way browsers directly access target URLs.

In the Web2 architecture, users submit the content they generate directly to the service, without retaining ownership or local copies. User accounts and content exist within the service, and the service accumulates this data. This accumulation accelerates the creation of new data. It is extremely difficult for users to switch to another service and achieve the same level of utility. To do so, users would need to transfer their content, and other users would also need to migrate en masse.

The existing Web architecture leads to content lock-in and account lock-in, which in turn fosters the concentration of power and a winner-takes-all dynamic.

## Web3

While Web3 often claims to challenge existing power structures and maximize user rights, in reality, it is currently just adding a blockchain layer on top of Web2.

[![Web3 as a marketing word](https://ethresear.ch/uploads/default/optimized/3X/1/c/1cbf70828e9cfde6ab305afa732da5b326b710fa_2_690x322.png)Web3 as a marketing word2014×940 90 KB](https://ethresear.ch/uploads/default/1cbf70828e9cfde6ab305afa732da5b326b710fa)

Although blockchain is decentralized, the fact that existing Web3 applications are built on top of the current Web architecture undermines its potential

# Portable Web Architecture

To solve the above issues and achieve a decentralized web while maximizing user rights, it is necessary to build a new architecture. The proposed solution is the **Portable Web**. This new web architecture provides an environment where users have complete control over their data and identity and enables developers and service providers to collaboratively evolve a single application.

[![Portable Web Architecture](https://ethresear.ch/uploads/default/optimized/3X/b/9/b9ffee4e26b1460e627f2401db4b0003f784a8cc_2_690x437.png)Portable Web Architecture1622×1028 54.1 KB](https://ethresear.ch/uploads/default/b9ffee4e26b1460e627f2401db4b0003f784a8cc)

## Components of the Portable Web

### Portable Web Browser

The browser plays several key roles in enabling the Portable Web.

1. Controlled Server Communication: It limits the servers with which the client can communicate. Clients cannot interact with servers unless explicitly intended by the user.
2. Currency Restriction: It restricts the currency used for payments in applications. The browser contains a wallet, ensuring that payments can only be made using the currency initially set by the cluster. By default, the browser interacts with an internal exchange (DEX or CEX), so the user is unaware of the currency being used.
3. Identity Management: It manages the user’s identity as a Self-Sovereign Identity (SSI), preventing servers or clients from locking in the user’s identity.
4. Built-In Support for Bootstrapping: It comes with built-in client and server information for the index cluster to support bootstrapping. Users can later connect to other clients or servers.
5. Data Migration and Updates: It executes migration scripts specified by the client to transfer data and manages client updates.

### Cluster

A cluster represents a single application, identified by its purpose document.

The components that make up a cluster are:

- Purpose Document
- API Schema
- Migration Script
- Client
- Server

Anyone can contribute components other than the purpose document to help develop and evolve the cluster.

### Index cluster

The index cluster functions like an App Store within the Portable Web (although anyone can provide it).

Providers of cluster components register their data with the index cluster. The index cluster hosts this registered data, offering users information and software. Additionally, the information includes details such as version and compatibility.

The index cluster knows which components belong to which clusters and understands the relationships between servers and API schemas, clients and API schemas, as well as clients and migration scripts.

## Components of a Cluster

[![The relationships between components](https://ethresear.ch/uploads/default/optimized/3X/e/4/e49d0d3e46a311053e744c69bc9f63c792601554_2_690x378.png)The relationships between components1520×834 27.4 KB](https://ethresear.ch/uploads/default/e49d0d3e46a311053e744c69bc9f63c792601554)

### Purpose Document

The purpose document serves to enable and promote community-driven development. It defines:

1. The Ultimate Goal: The overarching objective that the cluster aims to achieve.
2. Tokens Used: The specific tokens to be utilized within the cluster.

This document is made public upon the cluster’s creation and remains immutable thereafter. While the ultimate goal stated in the purpose document does not have any systemic function, the community uses this document as a basis for improving and adding features.

### API Schema

The API schema is a protocol that defines the communication methods between clients and servers. It needs to be in a developer-readable format. By adhering to this schema, clients and servers created by different developers can communicate with each other.

If there is compatibility between API schemas, servers and clients can support multiple Web API schemas.

### Migration Script

A migration script assumes that the client has a specific data model. It allows data transfer and synchronization between clients that refer to the same migration script.

### Client

A client consists of static content like HTML or JavaScript and can operate independently without relying on constant internet connectivity or specific servers. The client can only communicate with destinations specified by the user. It should not be implemented to depend on a specific server.

The client can cache data that the user sends to or receives from the server. It must specify a particular migration script and cache data in a data structure that allows data migration by executing that script.

### Server

A server provides APIs that conform to the API schema. Any functionality that can be defined in the API schema can be provided.

## Versioning

In the Portable Web, a cluster is a single application unit, but it can behave differently depending on which components are used. Since anyone can create components such as migration scripts, API schemas, clients, and servers, various versions coexist within a cluster.

### Migration Script

[![Version control of Migration Script](https://ethresear.ch/uploads/default/optimized/3X/8/1/816f44d7982b94d6c1e4e466919907be66f633b5_2_690x251.png)Version control of Migration Script1784×650 18 KB](https://ethresear.ch/uploads/default/816f44d7982b94d6c1e4e466919907be66f633b5)

Version management of migration scripts is represented using a Directed Acyclic Graph (DAG) and can be updated by anyone. When creating a new migration script, you must specify a backward-compatible migration script. The new migration script must be able to migrate data by transforming the data structure, even when executed from clients that supported the specified backward-compatible migration script. Since anyone can create migration scripts, they may branch but can also merge.

By executing the appropriate number of migration scripts, data can be migrated from older clients to clients that support the latest migration script. For example, a client that supports migration script ‘a’ can migrate data to a client that supports migration script ‘e’ by executing migration scripts three times（b→c→e or b→d→e）.

### API Schema

A new API schema does not carry information about relationships with other API schemas, such as backward compatibility. Clients and servers can support multiple API schemas, so compatibility management is handled individually by clients and servers. They can support additional API schemas as long as compatibility is not broken.

### Client

Client updates are mainly divided into three types. For all types of updates, the user can choose whether to accept the update.

1. Type 1: Updates that do not change either the migration script or the API schema.
2. Type 2: Updates that change the API schema.
3. Type 3: Updates that change the migration script.

Type 1 does not affect other components.

In the case of Type 2, compatibility with the servers that the user usually uses may be lost unless the server also updates to the corresponding API schema.

In the case of Type 3, the client can update to a new migration script that specifies the current migration script as backward-compatible. Data can be migrated from a client supporting the previous migration script, but since it’s only backward-compatible and not fully compatible, data cached in the client that has updated the migration script cannot be migrated back to other clients still using the older migration script. In such cases, as shown in the diagram below, other clients need to either support the updated migration script or create a new one to ensure compatibility.

[![Resolve Migration Script Compatibility](https://ethresear.ch/uploads/default/optimized/3X/3/f/3fe644e9f22f77184275a467cfb51593e41bafad_2_690x215.png)Resolve Migration Script Compatibility1784×558 37.9 KB](https://ethresear.ch/uploads/default/3fe644e9f22f77184275a467cfb51593e41bafad)

### Server

A server update means changing or adding the corresponding API schema. You can update by registering the updated API schema information in the index cluster.

# The Economics of the Portable Web

For the Portable Web to function sustainably and for developers and service providers to actively participate, economic incentives are essential. This section explains the economic system that supports this architecture.

## Incentives for Participants

### Cluster Creators

Cluster creators launch new applications within the Portable Web ecosystem. They can issue tokens specific to their clusters, which become the foundation of the cluster’s economy. By designing tokens that encourage widespread adoption of their applications, cluster creators can earn revenue through seigniorage (profit from token issuance).

As the cluster gains popularity and more users join, the demand for these tokens increases. This heightened demand raises the value of the tokens, providing economic incentives for cluster creators to continue developing and improving their applications. The success of the cluster is directly linked to the value of the tokens, aligning the interests of cluster creators with those of users and other participants.

### Server Providers

Servers within the Portable Web host data and provide APIs that conform to the cluster’s API schema. Server providers can monetize their services through various billing models, such as subscription fees, pay-per-use charges, or offering premium features. Since users manage their own data and can choose which servers to interact with, service providers are encouraged to offer high-quality, reliable services to attract and retain users.

By accepting payments in the cluster’s tokens, service providers also participate in the cluster’s economy. If the token’s value increases, the potential revenue for service providers grows as well. In this way, a symbiotic relationship is formed where service providers contribute to the cluster’s growth while profiting from its success.

### Client Developers

Client developers create software that provides the cluster’s user interface and caches data sent to and received from servers. They can monetize their efforts by selling premium clients or offering additional features for a fee—all transacted in the cluster’s tokens.

Anyone can provide clients, and because of the interoperability within the cluster’s ecosystem, developers are encouraged to innovate and offer more valuable user experiences. They are motivated to continuously improve the products they provide.

### Users

By using the Portable Web, users enjoy greater control over their data and the ability to customize their application experience. They participate in the cluster’s economy by using tokens to access premium features and more. Additionally, users who hold tokens may see their value increase as the cluster grows, providing an incentive to support and promote the cluster.

By engaging in the cluster’s economy, users have more opportunities to actively participate, provide feedback, and contribute to the community. Their involvement is expected to help develop the ecosystem further.

# Discussions

Here, I briefly outline concerns and future challenges.

## Versioning

With the current version management method, there’s a risk that migration scripts and API schemas could proliferate uncontrollably, negatively impacting user experience and data portability.

At present, it might be desirable for the initial cluster creator to have initiative over specifications while still allowing anyone to customize.

## Incentives for Data Lock-in

The initial cluster creators have a disincentive against implementing data lock-in. This is because their goal is to profit from token seigniorage rather than from data lock-in (if they aimed to profit from data lock-in, they would not choose the Portable Web architecture). To profit from token seigniorage, they need to increase the real demand for the token, thereby boosting its price. To increase this demand, cluster creators must offer more attractive applications to users. Applications that appeal to users typically offer:

- No data lock-in
- Customizability by anyone, fostering diversity and rapid development.

Given this, cluster creators are likely to see remaining open as more beneficial than implementing data lock-in.

In other words, within the cluster, at least one component set (server, API schema, client, and migration script) must support data portability.

Service providers who join later and are not token stakeholders have a positive incentive for data lock-in, similar to conventional web environments. However, since users can choose components from the cluster, the most user-preferred components will be utilized. In an environment without data lock-in, if users still choose a locked-in component, it is a result of their own decision. This is also part of the value the Portable Web offers, and it cannot deny this choice.

## Economics

If payments can be made through methods other than those provided by the browser’s standard, the system’s economy could collapse, rendering this architecture unviable.

## When the Purpose of a Cluster Changes

The components of a cluster must align with its purpose. If functionalities that do not follow the cluster’s purpose are implemented, the cluster will lose its distinct identity—the symbol that differentiates it from other clusters. This would be similar to Facebook and LinkedIn—which have different purposes—losing their boundaries and becoming inconvenient applications. Moreover, if a feature does not align with users’ objectives, it is unlikely to gain their support.

# Q&A

**
Is the Portable Web feasible?**

I have made [a prototype](https://www.youtube.com/playlist?list=PLXrS06DyEi7EdjXKeUbnJWrAt6bZs3CHg) and confirmed that it is feasible to some extent.

Challenges remain in the functioning of the crypto-economics model, large-scale user testing, and the complex version management of API schemas and migration scripts, and these will need to be addressed moving forward.

**
What is the difference between Fediverse?**

At first glance, clusters may seem like web applications offered in the Fediverse format (e.g., Mastodon), but there are several key differences:

1. Economic Incentives: In the Fediverse, there is no built-in economic incentive for instance providers, whereas in the Portable Web, such incentives are designed. This allows for greater sustainability and potential for growth.
2. Data Portability Scope: In the Fediverse, the scope of data portability is predetermined (by W3C) and limited, as outlined in ActivityPub. In contrast, with the Portable Web, cluster providers can flexibly expand the range of data portability by modifying data migration scripts.
3. User Data Sovereignty: In the Fediverse, data may be shared between servers regardless of the user’s intent. In the Portable Web, users can choose their servers, giving them greater sovereignty over their data.

**
Why am I posting this here?**

- I initially submitted this proposal to ESP’s small grant program, but unfortunately, it was not selected for support. They kindly recommended that I share it here instead.
- I highly respect the expertise and insights of this community and look forward to engaging in thoughtful discussions.

**
Is this post the final version?**

This post is the beginning, and I plan to refine it based on the community’s feedback and interest.

I welcome your feedback and collaboration to further develop and refine the Portable Web concept.
