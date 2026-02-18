---
source: magicians
topic_id: 12334
title: "EIP-6239: Semantic Soulbound Tokens"
author: JessicaC
date: "2022-12-30"
category: EIPs
tags: [erc, nft, sbt, semantic, social-recovery]
url: https://ethereum-magicians.org/t/eip-6239-semantic-soulbound-tokens/12334
views: 3314
likes: 4
posts_count: 4
---

# EIP-6239: Semantic Soulbound Tokens

EIP-6239: Semantic Soulbound Tokens

description: Adding RDF triples to EIP721 and EIP5192 metadata to capture the social meaning of the Token.

author: Jessica Chang [j.chang@relationlabs.ai](mailto:j.chang@relationlabs.ai)

status: Draft

type: Standards Track

category (*only required for Standards Track): ERC

requires (*optional): 165, 721, 5192

**Abstract**

This proposal extends EIP-721 and EIP-5192 by introducing a standard for adding RDF triples to Soulbound Tokens (‘SBTs’) metadata.

Soulbound Token represents the commitments, credentials, and affiliations of accounts. Resource Description Framework (‘RDF’) is a standard data model developed by the World Wide Web Consortium (‘W3C’) and is used to represent information in a structured, machine-readable format in triples consisting of a subject, a predicate, and an object (the ‘RDF triple’). These triples can be combined and linked together to represent more complex information and relationships. Semantic SBTs are built on existing EIP-721 and EIP 5192 standards to include RDF triples in metadata to capture and store the meaning of social metadata as a network of accounts and attributes.

Semantic SBT provides a foundation for publishing, linking, and integrating data from multiple sources, and enables the ability to query and retrieve information across these sources, using inference to uncover new insights from existing social relations. For example, form the on-chain united social graph, assign trusted contacts for social recovery, and supports fair governance.

**Motivation**

While the existence of SBTs can create a decentralized social framework, there still needs to be a way to create the connectedness of SBTs through relationships on-chain. Current NFTs and SBTs are hosting data off-chain, some even on centralized servers, let alone the linking of social data.  And to further fuel the boom of the SBTs ecosystem, we need a bottom-up and decentralized way to maintain people’s social identity related information.

Semantic SBTs address this by storing social metadata, attestations, and access permissions on-chain to bootstrap the social identity layer and a linked data layer natively on Ethereum, and bring semantic meanings to the tons of bits of on-chain data.

**Connectedness**

Semantic SBTs store social data as RDF triples in the Subject-Predicate-Object format, making it easy to create relationships between accounts and attributes.  RDF is a standard for data interchange used to represent highly interconnected data. Representing data in RDF triples makes it simpler for AI systems to identify, clarify, and connect information.

**Linked Data**

Semantic SBTs allow the huge amount of social data on-chain available in a standard format (RDF) and be reachable and manageable. The interrelated datasets on-chain can create the linked data layer that allows social data to be mixed, exposed, and shared across different applications, providing a convenient, cheap, and reliable way to retrieve data, regardless of the number of users.

**Social Identity**

Semantic SBTs allow people to publish or attest their own identity-related data in the bottom-up and decentralized way, without reliance on any centralized intermediaries while setting every party free. The data is fragmentary in each Semantic SBT and socially interrelated. RDF triples enable various community detection algorithms to be built on top.

This proposal outlines the Semantic data modeling of SBTs standard that allows implementers to model the social relations among Semantic SBTs, especially in the social sector.

**Specification**

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The token MUST implement the following interfaces:

a.	EIP-165’s ERC165 (0x01ffc9a7)

b.	EIP-721’s ERC721 (0x80ac58cd)

c.	EIP-721’s ERC721Metadata (0x5b5e139f)

d.	EIP-5192’s ERC5192(0xb45a3c0e)

**Contract Interface**

```auto
Solidity
/**
 * @title Semantic Soulbound Token
 * Note: the EIP-165 identifier for this interface is 0xfbafb698
 */
interface ISemanticSBT{
    /**
     * @dev This emits when minting a Semantic Soulbound Token.
     * @param tokenId The identifier for the Semantic Soulbound Token.
     * @param rdfStatements The RDF statements for the Semantic Soulbound Token. An RDF statement is the statement made by an RDF triple.
     */
    event CreateRDF (
        uint256 indexed tokenId,
        string  rdfStatements
    );


    /**
     * @dev This emits when updating the RDF data of Semantic Soulbound Token. RDF data is a collection of RDF statements that are used to represent information about resources.
     * @param tokenId The identifier for the Semantic Soulbound Token.
     * @param rdfStatements The RDF statements for the semantic soulbound token. An RDF statement is the statement made by an RDF triple.
     */
    event UpdateRDF (
        uint256 indexed tokenId,
        string  rdfStatements
    );

/**
     * @dev This emits when burning or revoking Semantic Soulbound Token.
     * @param tokenId The identifier for the Semantic Soulbound Token.
     * @param rdfStatements The RDF statements for the Semantic Soulbound Token. An RDF statement is the statement made by an RDF triple.
     */
    event RemoveRDF (
        uint256 indexed tokenId,
        string  rdfStatements
    );

    /**
     * @dev Returns the RDF statements of the Semantic Soulbound Token. An RDF statement is the statement made by an RDF triple.
     * @param tokenId The identifier for the Semantic Soulbound Token.

     */
    function rdfOf(uint256 tokenId) external view returns (string memory);

}
```

ISemanticRDFSchema, an extension of ERC721 Metadata, is OPTIONAL for this standard, it is used to get the Schema URI for the RDF data.

```auto
Solidity
interface ISemanticRDFSchema{

    /**
     * @notice Get the URI of schema for this contract.
     * @return The URI of the contract which point to a configuration profile.
     */
    function schemaURI() external view returns (string memory);
}

```

ISemanticSBTUpdate is an extension interface, that is OPTIONAL for this standard, used to update the RDF data for the Semantic Soulbound Token.

```auto
Solidity
interface ISemanticSBTUpdate{
    /**
     * @notice Update the RDF data for Semantic Soulbound Token. Implementors can assign updaters as needed, for example, the token issuer.
     * @dev Emits the UpdateRDF event.
     * @param tokenId The identifier for the Semantic Soulbound Token.
     * @param rdfData RDF data is a collection of RDF statements that are used to represent information about resources.
     */
    function updateRDF(uint256 tokenId, RDFData memory rdfData) external;

}
```

**Rationale**

**Method Specification**

rdfOf (uint256 tokenId): Query the RDF data for the Semantic Soulbound Token by tokenId. The returned RDF data format conforms to the W3C RDF standard. RDF data is a collection of RDF statements that are used to represent information about resources. An RDF statement, also known as a triple, is a unit of information in the RDF data model. It consists of three parts: a subject, a predicate, and an object. The data format reference can be found [here](https://www.w3.org/2011/rdf-wg/wiki/Main_Page#Deliverables).

updateRDF (uint256 tokenId, RDFData rdfData): This OPTIONAL method is used when it needs to update the RDF data for Semantic SBT. Use this method to find the RDF data for Semantic SBT by tokenId and perform the update. The input RDF data MUST conform to W3C RDF standards. When implementing this method, SHALL assign updaters as needed, for example, the token issuer can be assigned as an updater. When calling this method, the UpdateRDF event MUST be triggered to notify the listener for performing relevant business update.

schemaURI(): This OPTIONAL method is used to query the URIs of the schema for the RDF data. RDF Schema is an extension of the basic RDF vocabulary and provides a data-modelling vocabulary for RDF data. It is RECOMMENDED to store the RDF Schema in decentralized storage such as Arweave or IPFS. The URIs are then stored in the contract and can be queried by this method.

**Event Specification**

CreateRDF: When minting a Semantic Soulbound Token, this event MUST be triggered to notify the listener to perform operations with the created RDF data. When calling the event, the input RDF data MUST be RDF statements, which are units of information consisting of three parts: a subject, a predicate, and an object. The data model reference can be found [here](https://www.w3.org/2011/rdf-wg/wiki/Main_Page#Deliverables).

UpdateRDF: When updating RDF data for a Semantic Soulbound Token, this event MUST be triggered to notify the listener to perform update operations accordingly with the updated RDF data. When calling the event, the input RDF data MUST be RDF statements, which are units of information consisting of three parts: a subject, a predicate, and an object. The data model reference can be found [here](https://www.w3.org/2011/rdf-wg/wiki/Main_Page#Deliverables).

RemoveRDF: When burning or revoking a Semantic Soulbound Token, this event MUST be triggered to notify the listener to perform operations with the removed RDF data for the Semantic SBT. When calling the event, the input RDF data MUST be RDF statements, which are units of information consisting of three parts: a subject, a predicate, and an object. The data model reference can be found [here](https://www.w3.org/2011/rdf-wg/wiki/Main_Page#Deliverables).

**Backwards Compatibility**

This proposal is fully backward compatible with [EIP-721](https://eips.ethereum.org/EIPS/eip-721) and [EIP-5192](https://eips.ethereum.org/EIPS/eip-5192).

**Test Cases**

Our sample implementation includes [test cases](https://github.com/JessicaChg/semanticSBT/blob/main/test/SemanticSBT.test.js) written using Hardhat.

**Reference Implementation**

A reference implementation can be found [here](https://github.com/JessicaChg/semanticSBT/blob/main/README.md).

**References**

1. Resource Description Framework (RDF) RDF - Semantic Web Standards
2. RDF Schema RDF Schema 1.1
3. W3C RDF recommendation RDF Working Group Wiki

**Security Considerations**

There are no security considerations related directly to the implementation of this standard.

**Copyright**

Copyright and related rights waived via CC0.

## Replies

**JessicaC** (2023-01-07):

[@axic](/u/axic) [@SamWilsn](/u/samwilsn) [@Pandapip1](/u/pandapip1)

---

**SamWilsn** (2023-01-24):

Couple non-editor related comments (meaning you can ignore them and it won’t affect your PR getting merged):

- Why extend EIP-5192 and not EIP-5114?
- Why separate the CreateRDF and UpdateRDF events? Shouldn’t a single UpdateRDF be sufficient?
- You define an update interface, but not a remove interface. Is that intentional? Should the update interface also contain a remove method?

---

**JessicaC** (2023-06-26):

- Why extend EIP-5192  and not EIP-5114 ?
When considering why EIP-5192 is chosen for extension over EIP-5114, the reason is that the transfer function of SBT can be controlled through a switch mechanism, allowing for flexible definitions of transfers. In contrast, EIP-5114 does not provide a method to unbind or untether an NFT, meaning that once an NFT is bound, it cannot be transferred again. Therefore, the ability to control transfers and unbind NFTs makes EIP-5192 a more suitable option for extension in this particular scenario.
- Why separate the CreateRDF and UpdateRDF events? Shouldn’t a single UpdateRDF be sufficient?
Separating the CreateRDF and UpdateRDF events serves a purpose and provides benefits that a single UpdateRDF event alone may not fulfill. The decision to have two distinct events is driven by the need to differentiate between the creation and subsequent updates of RDF statements associated with a token.
The CreateRDF event is triggered specifically when a token is generated, capturing the initial RDF statements. This event conveys the initial state of the RDF data and provides relevant information to applications or listeners.
Conversely, the UpdateRDF event is triggered when modifications or updates are made to the existing RDF statements of a token. This event signifies changes or additions to the RDF data associated with the token.
By having separate events, there is a clear distinction and chronological order between the token’s creation and subsequent updates. It provides a more structured approach to managing token lifecycle events, allowing for easier tracking and enabling specific actions based on the event type. A single UpdateRDF event alone may not adequately fulfill the need for distinct handling of token creation and subsequent updates.
- You define an update interface, but not a remove interface. Is that intentional? Should the update interface also contain a remove method?
In EIP 6239, we have made the decision to remove the ISemanticSBTUpdate interface. Therefore, the concerns regarding the absence of a remove interface have been addressed.

