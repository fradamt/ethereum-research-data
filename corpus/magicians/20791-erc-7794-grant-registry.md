---
source: magicians
topic_id: 20791
title: "ERC-7794: Grant Registry"
author: ownerlessinc
date: "2024-08-13"
category: ERCs
tags: [erc, standards-adoption, standardization, grant-program]
url: https://ethereum-magicians.org/t/erc-7794-grant-registry/20791
views: 218
likes: 1
posts_count: 8
---

# ERC-7794: Grant Registry

https://github.com/ethereum/ERCs/pull/680

**Introduction**

In the Ethereum ecosystem, various grant programs play a crucial role in funding innovative projects that drive our decentralized future. However, the lack of standardization across these programs has led to inefficiencies, confusion, and difficulties in managing and tracking grants across different protocols and networks. Hence I propose the creation of a unified Grant Program Standard, comprising a standardized interface and a grant registry contract. This standard aims to harmonize the processes around grant issuance, management, and tracking, ensuring a seamless experience for all participants and contributors involved.

**Problem Statement**

Currently, each grant program operates with its own set of rules, interfaces, and management protocols, leading to a fragmented landscape that hinders interoperability. This lack of uniformity creates several issues:

1. Inconsistent Grant Tracking: Different standards make it challenging to track grants across various platforms, leading to missed opportunities, duplicated efforts, and weak backward compatibility.
2. Complex Management: Grantees and program managers struggle with keeping the communication of their grants updated, increasing the administrative burden and potential for errors.
3. Limited Transparency: Without a common on-chain standard, it is difficult for the community to monitor, aggregate, and audit grant programs, which can impact trust and accountability.

To address these issues, I propose the adoption of a standardized interface based on the most common fields that are crucial for the grant lifecycle.

**Proposed Interface**

This interface will serve as the foundational layer for all grant programs, ensuring that key information is recorded and accessible in a consistent manner across the Ethereum ecosystem:

```auto
/// Grant Interface
id: uin256           // Grant unique identifier
network: uint256     // Blockchain network where the grant is being developed
grantee: address     // Address of the person responsible for delivering and receiving the grant award
protocol: string     // Name of the protocol/community that issued the grant
project: string      // Name/Title of the project or company that received the grant
externalLinks[]: string // Link that redirects to the grant proposal, discussion or relative
startDate: uint256   // Start date for the grant development
endDate: uint256.    // Expected completion date for the grant
status: enum(Status) // Current status of the grant
disbursements: Disbursement // Disbursement stages based on milestones
```

```auto
/// Disbursement Struct
fundingTokens: address[]   // Tokens that will be disbursed in this stage
fundingAmounts: uint256[]  // Amounts of tokens to be disbursed in this stage
disbursed: bool[]          // Indicates if the disbursement has been made in this stage
```

```auto
/// Status Enum
Proposed,        // The grant has been proposed but not yet approved (Default)
Approved,        // The grant has been reviewed and approved
InProgress,      // The project is actively being worked on
Completed,       // The project has been completed and deliverables submitted
Cancelled,       // The grant was cancelled
Rejected         // The grant proposal was reviewed and rejected
```

**Grant Registry Contract**

To complement the standardized interface, I propose the development of a Grant Registry Contract. This contract will act as a universal registry where all grants, regardless of the issuing protocol or network, can be registered, tracked, and managed. Similar to how the multicall3 works.

**Key Features:**

1. Universal Registration: Allows any grant program to register their grants using the standardized interface.
2. Grant Management: Provides functionalities for program managers to update the status of grants, track progress, and manage funding distribution.
3. Transparency and Audibility: Enables the community to view grant details, track funding allocations, and monitor progress, enhancing trust and accountability.
4. Interoperability: Facilitates cross-chain and cross-protocol grant management, breaking down silos and enabling seamless interaction between different grant programs.

**Consideration: Use of Ethereum Attestation Service (EAS)**

The Ethereum Attestation Service (EAS) offers a decentralized, trustless, and on-chain method to create verifiable attestations, making it an attractive option. By utilizing EAS, we could theoretically record and verify key events, such as grant approvals, disbursements, and project completions, directly on the blockchain. However, one significant challenge in applying EAS within this context is the lack of mutability due to its reliance on static schemas.

In the proposed grant management system, flexibility is crucial, especially regarding the management of disbursement stages, milestone achievements, and potential changes in project scope or funding requirements. The static nature of EAS schemas limits the ability to modify attestations once they are created, which conflicts with the dynamic needs of a typical grant lifecycle where adjustments are often necessary.

**Next Steps**

1. Community Feedback: I encourage feedback on the proposed interface and grant registry contract. Any suggestions for improvements or additional features are welcome.
2. Implementation Draft: Upon reaching a consensus, the next step will be to draft a detailed EIP and begin the implementation process.

Looking forward to your thoughts and contributions!

## Replies

**ownerlessinc** (2024-08-15):

- The ID inside the grant structure might be useful in case the grant program has a system with unique IDs, tracking their grants by such. On the other hand, grant programs that don’t implement a linear ID system for their grant won’t use this variable. Better to take it off and let the external link provide better descriptions
- The Disbursements should not be done by the registry, by all means, focusing on status updates should be more likely to work out. Grant Program can still can the Registry to update after a successful.
- Maybe ‘project’ should become ‘grantTitle’, ‘projectTitle’ or ‘projectName’

---

**ownerlessinc** (2024-08-15):

- Approved / InProgress kinda feels the same, once it’s approved the team starts to mobilize towards completion, hence “in progress”. Can a grant be approved but not start progression?

---

**ownerlessinc** (2024-08-21):

Realized that we need another kind of identification of the grant program to easily find it on-chain via event emission.

I propose to rebrand the `protocol` field which firstly was thought of as a response like the chain name itself, but this would repeat the network field, therefore renaming it to `grantProgramLabel` could be clearer to the readers, although big it was the best I found so far. i.e.: Alchemy Startup Program, Aleo Developer Grants Program, Ajna Grant Coordination Fund, etc.

Also proposing renaming the `network` field into `chain`

---

**ownerlessinc** (2024-08-21):

I regret what I said, I think we need a grant identifier inside the Grant structure.

The reason is because of the simplicity of fetching the grant from the off-chain perspective.

The grant can be edited in some aspects, but the grant ID first generated by all the initial data will remain the same, therefore generating it again would be relatively hard. Providing attributes in it to facilitate the identification would come in handy.

Imagine that you are a platform that has multiple grants. You have your index of grants in your database. Registering those and emitting them via event would make them easily trackable.

Things like `grantee`, `chain`, `grantProgramLabel` wouldn’t change easily and they can still be a good approach to fetch using SubGraph but still, those might change or end up having duplicated names.

I propose adding an `uid` field similar to what EAS did, but allowing it to be different to grant ID the mapping key. This value would be a bytes32 and in the case the grant registration have no personal indexation, it should be 0 instead.

---

**rpunkt** (2024-08-21):

Thank you for sharing this! It’s an interesting approach to a problem we’ve also been working on at bleu.

We recently submitted a grant proposal for Optimism that addresses some of these same challenges. I’m particularly excited because the ideas here could help shape our work in this grant as well!

I think the largest overlap is concerned with on-chain grant lifecycle management and using EAS as an on-chain registry. A few questions came to mind:

1. Have you considered how your Grant Registry Contract might be implemented or mirrored across different networks? Do you think it makes sense for this registry to be multichain at all (esp. considering that one could just build on top of EAS)?
2. Regarding adoption, do you see this as a bottom-up (grantee-driven) or top-down (grantor-driven) process? Or perhaps a combination? Asking because it’s also something we’re grappling with.
3. Would your proposal be opinionated with regards to how the grant system works (e.g., adopting some sort of milestone tracking)? How would it handle potential changes in project scope or other actors in grants apart from grantees?

Looking forward to your thoughts on these points!

---

**ownerlessinc** (2024-09-06):

Hey [@rpunkt](/u/rpunkt), thank you so much for those inputs! Let’s work them out!

1. Multi-chain Registry: It makes a lot of sense for the registry to be multi-chain. The two biggest use cases for having grants on-chain are reputation and analytics. Ensuring all chains adhere to the same standard would streamline data collection and insights generation.

- The registry should be similar to how multicall3 is deployed on all networks at the same address.
- For example, it doesn’t make sense for an Arbitrum grant program to register its grant on Optimism, and vice versa.
- The problem with using EAS is the immutability of the data attested, making it impossible to update the grant during its course under the same attestation.uid, for instance, the external URL pointing to the grant description or milestones dates could vary from time to time. The other problem with using EAS is that not all EVM chains have EAS, which could delay adoption. But talking with Mahesh from Karma we had an insight into using arbitrary encoded data for EAS, making the resolver decode such data, then registry/update a grant directly in the Registry. This also brings the potential need for a resolver for the Registry itself alongside an arbitrary data field to allow grant programs to create custom properties for edge cases.

Ultimately, the primary goal of this standard should be to identify the common data shared by all grant programs.

1. Grantee and Grantor Perspectives: From the grantor’s perspective, the benefits of this system are clear. For the grantee, the main value is the reputation generated on-chain, with potential perks like certificates or tokenization. Strong candidates will likely embrace the transparency of having their contributions on-chain, while weaker candidates may shy away. Grant programs, however, stand to gain even more:

- Increased transparency and easier-to-audit grants.
- Data integrity and censorship resistance.
- Potential for automated milestone payments.
- Integration with other contracts across the ecosystem.
- Improved insights into fund distribution and grantee performance.
- Enhanced competition between grant programs.

From a community perspective, there’s huge potential for improving cross-protocol reputation systems. When community-made dashboards (like **Dune**) start tracking grant stages, we’ll see real momentum from both sides. Currently, communities are unable to create advanced reputation and incentive mechanisms because the necessary data is fragmented and not on-chain.

1. Mutability of the Registry: The registry definitely needs to be mutable. I don’t think on-chain checkpoints are necessary—instead, emitting events and overwriting data should suffice. However, milestones and disbursements should function more like checkpoints or a story mode. The address registering the grant should be stored as a Grant Manager, with the authority to edit the grant. This could be a single address, multiple addresses, a multi-sig, or even a DAO.

I’ve also considered changing the grantee into an array of addresses, especially if referring to a team so that all members can build their reputation.

---

**ownerlessinc** (2024-10-18):

Thinking a lot about the mutability and modularity of this registry and some conclusions I achieved by talking to friends sharing the same context:

1- This is more of a Grant Registry than actually a Grant Program Registry, because the main usage is managing grants (from grant programs), so although the grant programs will manage such grants, they are not registering themselves hence I’m changing the name into Grant Registry.

2- The updated structed proposed goes as follow:

```solidity
 struct Grant {
    uint256 id;
    uint256 chainid;
    string community;
  }

  struct Participants {
    address grantManager;
    EnumerableSet.AddressSet grantees;
  }

  struct Milestones {
    uint256 startDate;
    EnumerableSet.UintSet milestonesDates;
    mapping(uint256 => Disbursements) disbursements;
  }

  struct Disbursements {
    address fundingToken;
    uint256 fundingAmount;
    bool isDisbursed;
  }
```

This modularity allows huge gas optimization and updates as the grant moves forward. Eventually, things like delaying the start date or changing milestone dates, among other issues often happen, therefore mutability is important to consider.

1. The grantID as a bytes32 keccak256 is hashed between the main Grant struct, which hosts immutable data about the grant. The internal id field in the struct is made specially for the DAOs that have their own internal grant identification. If that is not the case, 0 should be used instead. But to create more randomness and avoid repetition-- specialy because the registry is supposed to live in more than one network, I propose using the block.timestamp in the hash generation, as well as avoiding registering duplicated entries.

