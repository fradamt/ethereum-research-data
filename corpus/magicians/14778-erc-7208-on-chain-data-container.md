---
source: magicians
topic_id: 14778
title: "ERC-7208: On-chain Data Container"
author: galimba
date: "2023-06-21"
category: ERCs
tags: [nft, token, erc-721, metadata, odc]
url: https://ethereum-magicians.org/t/erc-7208-on-chain-data-container/14778
views: 11534
likes: 373
posts_count: 120
---

# ERC-7208: On-chain Data Container

UPDATE January 2025 -

The [ERC-7208](https://eips.ethereum.org/EIPS/eip-7208) is pushing to FINAL

The audit report is [here](https://omniscia.io/reports/nexera-minimalistic-eip-7208-implementation-672a297b911e5e00191801b5/)

An example implementation can be found [here](https://github.com/Nexera-Foundation/Minimalistic-ERC-7208), where an ERC-1155 and many ERC-20 share storage

Other implementations and tools will be posted [here](https://docs.nexera.network/nexera-standard/overview), thanks to the [Nexera Network](https://www.nexera.network/)

Special thanks to [Omniscia](https://omniscia.io/) for their contributions.

/******************* About This ERC ********************************/

Hello Magicians,

Today we are excited to introduce [ERC-7208](https://eips.ethereum.org/EIPS/eip-7208), a set of interfaces that we call the On-Chain Adapters:

- DataIndex (DI) → indexes information and approvals of DataManagers to DataPoints through DataObjects
- DataManager (DM) → interfaces with user, implements business logic or “high-level” data management
- DataObject (DO) → logic implementing "low-level data storage management
- DataPoint (DP) → indexed low-level data pointer (bytes32)
- DataPoint Registry (DPR) → defines a space of data point compatibility/access management

[![overview](https://ethereum-magicians.org/uploads/default/optimized/2X/d/d708b87ee78894cc3f966f5f0007f550bb8b4a48_2_690x417.jpeg)overview744×450 35.3 KB](https://ethereum-magicians.org/uploads/default/d708b87ee78894cc3f966f5f0007f550bb8b4a48)

## Abstract

This ERC defines a series of interfaces for the abstraction of storage of on-chain data by implementing the logic functions that govern such data on independent smart contracts. “On-chain Data Containers” (ODCs) refer to the separation and indexing of data storage away from data management. We propose that on-chain data can be abstracted and stored in smart contracts called “Data Objects” (DO), which answer to external data indexing mechanisms named “Data Points” (DP). This data can be accessed and modified by implementing (one or many) separate smart contracts identified as “Data Managers” (DM). We introduce two mechanisms for access management: first, through a “Data Index” (DI) implementation, the “Data Managers” (DM) can be gated from accessing “Data Objects” (DO); second, a “Data Point Registry” (DPR) implementation manages the issuance of “Data Points” (DP). Lastly, we introduce the concept of data portability (horizontal data mobility) between implementations of “Data Index” (DI), enabling massive updates to the logic without affecting the underlying data storage.

## Motivation

As the Ethereum ecosystem grows, so does the demand for on-chain functionalities. The market encourages a desire for broader adoption through more complex systems and there is a constant need for improved efficiency. We have seen times when an explosion of new standard token proposals was solely driven by market hype. While ultimately each standard serves its purpose, most of them require more flexibility to manage interoperability with other standards. A standard adapter mechanism is needed to enhance interoperability by driving the interactions between assets issued under different ERCs.

Without such mechanisms, most projects have implemented bespoke solutions for interoperability. This is an inefficient approach and leads to a fragmented ecosystem. We recognize there is no “one size fits all” solution to solve the standardization and interoperability challenges. Most assets - Fungible, Non-Fungible, Digital Twins, Real-world Assets, DePin, etc - have multiple mechanisms for representing them as on-chain tokens through the use of different standard interfaces and the diversity of standards spurs innovation.

However, for these assets to be exchanged, traded, or otherwise interacted with, protocols must implement compatibility with the relevant interfaces to access and modify on-chain data. This is especially challenging when considering the previously mentioned bespoke solutions for interoperability. Additionally, the immutability of smart contracts complicates the ability of already deployed protocols to adapt to new tokenization standards, which is critical for future-proofing implementations. A collaborative effort must be made to enable interaction between assets tokenized under different standards. The current ERC provides the tools for developing such on-chain adapters.

We aim to abstract the on-chain data handling from the logical implementation, exposing the underlying data independently of the ERC interface. We propose a series of interfaces for storing and accessing data on-chain in contracts called “Data Objects” (DO), grouping the underlying assets as generic “Data Points” (DP) that may be associated with multiple interoperable and even concurrent “Data Manager” (DM) contracts. This proposal is designed to work by coexisting with previous and future token standards, providing a flexible, efficient, and coherent mechanism to manage asset interoperability.

- Data Abstraction: We propose a standardized interface for enabling developers to separate the data storage code from the underlying token utility logic, reducing the need for supporting and implementing multiple inherited -and often clashing- interfaces to achieve asset compatibility. The data (and therefore the assets) can be stored independently of the logic that governs such data.
- Standard Neutrality: A neutral approach must enable the underlying data of any tokenized asset to transition seamlessly between different token standards. This will significantly improve interoperability among other standards, reducing fragmentation in the landscape. Our proposal aims to separate the storage of data representing an underlying asset from the standard interface used for representing the token.
- Consistent Interface: A uniform interface of primitive functions abstracts the data storage from the use case, irrespective of the underlying token’s standard or the interface exposing such data. Data and metadata can be stored on-chain, and exposed through the same primitives.
- Data Portability: We provide a mechanism for the Horizontal Mobility of data between implementations of this standard, incentivizing the implementation of interoperable solutions and standard adapters.

### Terms

- Data Point: A uniquely identifiable reference to an on-chain data structure stored within one or many Data Objects and managed by one or many Data Managers. Data Points are issued by a Data Point Registry.
- Data Object: A Smart Contract implementing the low-level storage management of information indexed through Data Points.
- Data Manager: One or many Smart Contracts implementing the high-level logic and end-user interfaces for managing Data Objects.
- Data Point Registry: One or many Smart Contracts used for managing the issuance of Data Points. Additionally, a Data Point Registry defines a space of compatible or interoperable Data Points.
- Data Index: One or many Smart Contracts used for managing the access of Data Managers to Data Objects.
overview-tec1374×731 95.2 KB

## Replies

**Ridgestarr** (2023-12-17):

BOSS moves. Confidence in this team only growing. No mercy.

---

**Howee** (2023-12-17):

Great breakdown and technical overview of the overall vision of the AllianceBlock project, very exciting to see it at this stage ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**D_Ddefi** (2023-12-17):

Amazing work the #NXRA team is doing!

---

**kamelion** (2023-12-17):

Man! this provides a comprehensive and insightful overview of ERC-7208 , particularly highlighting the innovative approach of On-Chain Data Containers (ODC) in enhancing data management and interoperability across various token standards. I think tht its impressive how this delves into the technicalities while also considering practical use cases like the tokenization of real-world assets. RWA needs this in my opinion.

I’m curious about the potential impact of ERC-7208 on the broader Ethereum ecosystem. how might the introduction of ERC-7208 and its On-Chain Data Containers influence the development and deployment of decentralized applications (DApps), particularly in terms of scalability and user experience?

---

**Howee** (2023-12-17):

…a comprehensive and well-thought-out proposal! The concept of On-Chain Data Containers (ODCs) and ERC-7208’s focus on standardization and interoperability make a lot of sense, especially in a rapidly evolving Ethereum ecosystem with a constant influx of ERC proposals.

I appreciate the attention to detail, especially the abstraction of logic from storage, the versatility of Properties, and the role of Property Managers. The use case examples, like the luxury car rental scenario, add practical context to how ERC-7208 can streamline complex interactions.

The approach to expose Properties as procedurally generated Metadata JSON on-chain is a smart move, addressing the limitation of off-chain metadata storage. The variety of Property Managers, such as Identity and Rules Engine, showcase the flexibility and extensibility of the proposed standard.

…examples of real-world asset tokenisation using ODCs and the default implementation with added features demonstrate a thoughtful consideration for efficiency, scalability, and compliance. Overall, ERC-7208 seems like a promising step towards a more cohesive and adaptable on-chain data management solution. Kudos to the team!

---

**Hairoun** (2023-12-17):

Love how projects keep innovating, the RWAs sector is critical to DeFi.

---

**Leon_S** (2023-12-17):

Very informative read on ODC’s. Thanks for giving insight on the topic. Love to see this as the new standard!

---

**farzad** (2023-12-17):

Unlocking seamless interoperability, abstraction of logic from storage, and empowering dynamic tokenization scenarios. Innovation in the Ethereum ecosystem always exciting ![:raised_hands:](https://ethereum-magicians.org/images/emoji/twitter/raised_hands.png?v=12)

---

**Hunty** (2023-12-17):

A great read, thanks for the informative information.

---

**jaws** (2023-12-17):

I too think that this is not necessarily restricted to real-world asset tokenization. it could enable some wider-reaching applications.

A good example would be digital asset tokenization in on-chain gaming applications. Think of a character or avatar as an ODC with the PMs managing all the various abilities, powers, or assets of that avatar. I also wonder if the generated JSON metadata could be harnessed to render certain assets in digital space and thus removing the need to store assets in centralized cloud storage.

---

**Nellykhan** (2023-12-17):

This is very smart. No mercy!

---

**AndyVi** (2023-12-18):

ODC can replace a wallets of all sorts eventually, can it?

---

**RWAfan** (2023-12-18):

As someone who talks with a lot of companies that are looking into RWA tokenization, I can safely say that ODCs are much needed and will open op a wide range of new business opportunities to the Ethereum community and beyond. From a professional and business perspective, I see this as the next much needed evolution of NFTs. I have explored ODCs with businesses from different industries, from creative businesses looking into creative NFT use cases, all the way to dynamic licensing companies, real-estate and carbon credit projects.

All these businesses have one thing in common, they want this!

As I am personally very biased, in favour of this proposal. I would also like to hear from the community what potential ‘drawbacks’ could be. In what scenario would you prefer a different standard instead of this one? And when would you use ERC-7208?

---

**AndyVi** (2023-12-18):

How does ERC-7208 ensure compatibility and interoperability with existing ERC standards, particularly those that are widely adopted in the Ethereum ecosystem? Can you provide examples of how ERC-7208 would enhance or integrate with popular standards like ERC-20 or ERC-721?

---

**AndyVi** (2023-12-18):

Could you elaborate on specific real-world use cases where ERC-7208 would be particularly advantageous? How does this standard address the challenges faced in these scenarios more effectively than existing solutions?

---

**galimba** (2023-12-18):

Exactly like Jaws says: the concept of the Metadata being a composition of on-chain Properties provides not just backwards compatibility with previous NFT use cases where you would just store the `uri` as a string Property, but also for new use cases that require the Metadata to be updated “in real time”, like in videogames

---

**borovvvviec** (2023-12-18):

I have some Scalability Concerns… How does ERC-7208 plan to manage scalability challenges associated with storing large volumes of mutable data on-chain, especially in light of Ethereum’s current limitations in terms of block size and gas fees?

---

**Mike1** (2023-12-18):

How does in ERC-7208 propose the efficient on-chain data retrieval, especially when dealing with complex data structures and large data sets?

---

**galimba** (2023-12-18):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/a/49beb7/48.png) AndyVi:

> How does ERC-7208 ensure compatibility and interoperability with existing ERC standards, particularly those that are widely adopted in the Ethereum ecosystem? Can you provide examples of how ERC-7208 would enhance or integrate with popular standards like ERC-20 or ERC-721?

Hey Andy! Thanks for the question… Most tokens that follow a standard like the ones you mention have the storage integrated within the same interface as the functions that govern the logic for how to manage that storage. We see this as a limitation, where the logic and storage are bound to one another by the standard itself.

This ERC standardizes the interfaces that abstract the implementation from the storage. To give you a clear example:

Let’s say you have `100 DAI` on your account. This value is stored on a mapping within the ERC-20 contract, and you modify or access it by using the other functions listed on the standard (`transfer()`, `balanceOf()`, etc)

Now, in this scenario the assets are represented by a `uint` number, associated with your account. Your account has `100` DAI, whenever this storage says you do.

What we propose, is that the functions that modify this storage can be abstracted away from the data. For instance, you keep the storage on one contract and apply the logic on a different contract.

Back to the question: how does this work in ERC-7208? You can have Properties with storage values within the ODC contract, and you can have Property Manager contracts that implement the logic. Why is this a desired thing? Because by separating the logic, you get more versatility, at the cost of a `delegate` or `delegateCall`. Example of this would be: we can store a Property with value `uint= 100` for your address, and then this Property is managed by two different Property Managers contracts, each of them implemented with a different interface. i.e. ERC-1155 and ERC-20. This is a theoretical scenario, of course… but it would mean that you both simultaneously own an NFT (1155) and 100 of an ERC20 token. Each Property Manager works as its own token contract, it just delegates the storage to the ODC.

Hope this makes things clear(er)

---

**CryptoBeast** (2023-12-18):

This is really great, especially in the RWA sector. Good work guys


*(99 more replies not shown)*
