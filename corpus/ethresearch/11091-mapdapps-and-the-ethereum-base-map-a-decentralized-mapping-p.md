---
source: ethresearch
topic_id: 11091
title: "MapdApps and the Ethereum Base Map: A decentralized mapping protocol for spatial coordination and metaversal applications"
author: annemnemosyne
date: "2021-10-24"
category: Applications
tags: []
url: https://ethresear.ch/t/mapdapps-and-the-ethereum-base-map-a-decentralized-mapping-protocol-for-spatial-coordination-and-metaversal-applications/11091
views: 1942
likes: 2
posts_count: 2
---

# MapdApps and the Ethereum Base Map: A decentralized mapping protocol for spatial coordination and metaversal applications

**Introduction**

The crypto community has been anxiously awaiting the development of the metaverse, an interoperable virtual world where users can interact with one another through gaming, art, finance, and more. What startup, tech firm, or gaming company will be the first to create a product suitable for on-boarding millions — if not billions — of users? Centralized and decentralized platforms alike have made attempts to create spatial representations of the metaverse using 3D graphics and virtual reality. This approach ostracizes a large percentage of the population who are not comfortable with 3D graphics or who cannot afford expensive VR equipment. Rather than waiting for developers to simply build an extra big video game engine and open their floodgates to the masses, what if each individual user had the ability to create a piece of the metaverse in the world around them? The unified product would form a human-centered digital map that anyone with an internet connection could contribute to. That map would have the inherent utility of improving tools for navigation, searching for addresses, and spatially coordinating with others while conveniently forming a virtual world on which other applications could be built.

Centralized providers of digital maps have the resources and digital infrastructure to build quality products, but they have incentives to favor profitable map features such as businesses and they exploit the privacy of their users. Open source map services have the potential to have greater accuracy because they are created by users with the goal of representing reality as closely as possible. Volunteers create, validate, and moderate map features themselves using their own time and labor. Unfortunately, open source maps suffer from a lack of community engagement and rely on a handful of dedicated contributors. Cryptocurrencies have the potential to disrupt this industry by creating opportunities for users to earn a profit from contributing to a map by creating and moderating the map’s features. The Ethereum ecosystem in particular has the security and governance structures necessary to create a decentralized mapping protocol that is self-sustaining as a public good.

The purpose of this article is to provide a model for how a modular decentralized digital map protocol could be constructed using the Ethereum blockchain for security, governance, and hosting applications built around spatial coordination. It is my hope that such a protocol can serve as a foundation for metaversal applications that bridge Web 3 to the real world by providing opportunities for peer-to-peer labor, supporting public goods, and creating a vast ecosystem for economic and cultural coordination.

**Challenge statements**

- Centralized providers of digital maps are profit-oriented and largely neglect public goods
- Open source mapping applications suffer from lack of community engagement
- The Web 3 community lacks applications that connect users to the real world
- Current spatial representations of the metaverse are inaccessible to many potential users

**Phase 0: Protocol construction**

The data availability requirements of a decentralized digital map are complex and intensive. Whereas digital ledgers must be secure and immutable, a digital map must be organic and subject to constant state changes in order to more accurately reflect reality. The storage requirements of such a system would rise exponentially with more adoption. This obstacle may be mitigated with modular architecture that relies on a decentralized base layer for consensus. A vector layer constructed of points, lines, polygons, and object metadata would serve as the protocol’s basemap. I will refer to this layer as the Ethereum Base Map (EBM) in order to avoid confusion with stylized basemaps commonly used in geographic information systems. The EBM must be as decentralized and censorship-resistant as possible in order to serve as a credibly neutral platform for spatial consensus.

[![image](https://ethresear.ch/uploads/default/optimized/2X/4/4dfcbc3dfeec5170d0bbd1da1071c858ab2e0a68_2_690x254.png)image700×258 29.6 KB](https://ethresear.ch/uploads/default/4dfcbc3dfeec5170d0bbd1da1071c858ab2e0a68)

Decentralized mapping applications, or MapdApps, will be developed to provide the user interface for accessing and contributing to the EBM. MapdApps will have a similar look and feel to modern Web 2 mapping applications, visually rendering the vector features of the EBM and providing functions for navigation and searching. In addition to providing traditional mapping services using the EBM, MapdApps will access several Application Layers for specialized functions. Application Layers might include gaming layers, virtual and augmented reality layers, and layers for social, cultural, and economic coordination. Application Layers will be trivial to construct relative to the EBM, as they can be deployed on any number of data availability chains provided they refer to the EBM for spatial consensus and their data is accessible to a MapdApp. Referencing the EBM turns each Application Layer into a digital map in and of itself, enabling the composability of layers while maintaining strong spatial consensus.

**Phase 1: Building the Ethereum Base Map**

With the infrastructure for the EBM in place and the first MapdApps released, it is time for users to begin adding features to the map. As in traditional mapping, this will be performed in two perpetual tasks: feature tracing and field validation. Feature tracing can be performed by users located anywhere in the world by tracing land features, roads, and buildings seen in geo-referenced satellite imagery onto the EBM as points, lines, and polygons. These features must then be validated by users *in situ* using GPS-enabled devices. Together, these two techniques can be performed continuously to ensure that the EBM is current and accurately represents the real world.

These two tasks could be incentivized with tokens that would bear unique properties seldom seen in crypto assets. Feature tracing would be accessible to anyone in the world with an internet connection, assuming high-resolution satellite imagery is made readily available by the user’s MapdApp. An individual located in Cameroon could help trace features of the EBM in Colombia and vice-versa. Users would be compensated in tokens proportional to the number of features they trace that have been verified to be accurate. Field validators would visit these traced features in-person and verify their accuracy using a GPS-enabled smartphone. A greater sum (or perhaps a premium/governance token) would then be awarded to field validators for their efforts as this task is restricted by a user’s geography. Such a token for field validation would have the unique property of scaling in distribution with population density, as urban areas have more complex and numerous features to be accounted for. Together, these two tokens bear the attractive property of being very difficult to hoard, as they require time, labor, fresh satellite imagery, and involve insurmountable geographic constraints (one user cannot field-validate the whole world).

**Phase 2: Smart contracts as metaversal bounty vaults**

An important attribute of Application Layers will be smart contract bounty vaults, which will allow users to post bounty rewards for generalized tasks with spatial components. MapdApps will provide the interface for users to create vaults at specified locations using the EBM as a reference to write the vault’s state to the Application Layer. MapdApps would then display the locations of all bounty vaults contained within the selected Application Layer so that other users can locate them. The vault’s reward may be released to a claimant either at the owner’s discretion or following verification by a third-party arbitration service after reviewing evidence submitted by the claimant.

[![image](https://ethresear.ch/uploads/default/optimized/2X/9/9e6d9574f5bb300386ecc5e6d64b7d889f2a856a_2_552x500.jpeg)image700×634 163 KB](https://ethresear.ch/uploads/default/9e6d9574f5bb300386ecc5e6d64b7d889f2a856a)

Location data in Latitude, Longitude, and Elevation will be passed to the contract directly through the MapdApp, abstracting it from the user. An expiration date would ensure that funds in the vault are returned to the creator in the event that no claims are made on the bounty after a set time. MapdApps will provide a visualization of bounty vaults deployed on Application Layers as an overlay displayed on top of the EBM. Bounty vaults could be issued as incentives for other users to make updates to the EBM (through tracing or field validation) or as a reward for completing real-world tasks. As each Application Layer will have its own governance and rules for how they integrate with the EBM, style guides can be developed for how and where users deploy bounty vaults in order to not be filtered out as spam by their MapdApp interface.

Bounty vaults will play a key role in the construction of the EBM by facilitating the rewarding of tokens to contributors. The governance mechanisms being pioneered by Decentralized Autonomous Organizations in the Ethereum ecosystem will play a key role in coordinating changes to the base map and the applications built around it. The EBM itself could be maintained by a DAO, and DAOs could launch their own MapdApps catered towards their communities’ needs. DAOs formed at a local level could vote to provide additional incentives for contributors to complete sections of the map that have a high degree of real-world demand. On-chain arbitration and conflict resolution platforms will also fulfill an important role in providing compensation for labor performed for the protocol. Experienced mappers could serve as jurors to resolve contested or inaccurate contributions to the EBM.

**Phase 3 — The Metaverse is *here***

As the EBM grows to a global scale, Application Layers will provide exciting opportunities for spatial coordination. Location-based mobile gaming has become increasingly popular in recent years, and this presents a host of opportunities to develop a decentralized metaverse in the world around us. Application Layers would provide their own data availability, so in-game assets could be displayed in a MapdApp alongside real-world features referenced by the EBM. Not only could location-based games created as MapdApps utilize Application Layers as digital real-estate, but the construction of the EBM itself could be gamified. For example, the user of a location-based game may encounter a feature in the real-world that does not yet exist on the EBM. MapdApps would provide an interface for the user to commit any needed changes to the EBM while collecting a reward from the protocol or in-game tokens and achievements.

Social Application Layers might provide options for users to create their own permissioned map layers to share with their friends. Messaging platforms could have spatial components that link to a pin on the map like a digital bulletin board. Zero-knowledge attestations could be used by users to prove they have visited a given location while maintaining privacy. Art Application Layers could be used to cover the streets in (opt-in) digital graffiti using NFTs. More advanced Application Layers could provide 3D models of cities as a platform for virtual or augmented reality.

Smart contract bounty vaults created on various Application Layers need not be restricted to contributions to the EBM. Bounty vaults may simply reference the EBM in order to coordinate a request for general labor at a given location anywhere in the world. The accessibility of contributing to the EBM means that users from any location can earn tokens and create their own bounty rewards for general tasks. Arbitrating compensation for peer-to-peer labor will require a robust governance structure that provides incentives for users to fairly evaluate their peers’ completion of each task. The economy created by this protocol will be open to all users with an internet connection, and it will provide convenient on-boarding to the wider Ethereum ecosystem without the need for fiat on-ramps.

It is my hope that a protocol developed using this model will prioritize decentralization and the improvement of public goods.

## Replies

**buddy-von-doodle** (2021-10-26):

I was excited to see this in my RSS feed. The Facebook Reality Labs [LiveMaps proof of concept](https://www.youtube.com/watch?v=JTa8zn0RNVM) has always stood out to me as an important step for the “metaverse” (whatever that ends up being), but I think it would be better housed on a platform like Ethereum instead of Facebook (for obvious reasons). If something like this proposal gains traction, I would definitely be interested in contributing (code, resources, or data collection)

It looks like a lot of the big problems were left unaddressed in your proposal though. Like how would you approach the oracle problem? How do you know contributors are submitting data that reflects the real world, when they’re incentivized to spam fake data for tokens? You mentioned having validators verify data in person, but how do you prevent them from spoofing their GPS and approving spam edits all over the world?

