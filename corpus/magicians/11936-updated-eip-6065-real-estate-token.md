---
source: magicians
topic_id: 11936
title: "Updated! -- EIP-6065: Real Estate Token"
author: Alex-Klasma
date: "2022-11-30"
category: EIPs
tags: [nft, rwa]
url: https://ethereum-magicians.org/t/updated-eip-6065-real-estate-token/11936
views: 14134
likes: 32
posts_count: 21
---

# Updated! -- EIP-6065: Real Estate Token

**Old** EIP pull request [here](https://github.com/ethereum/EIPs/pull/6065)

Updated EIP [here](https://github.com/ethereum/EIPs/pull/6939)

*Note: We have completely overhauled this EIP, and have made things drastically simpler and easier to implement. We would love feedback and your honest opinion on our EIP6065, aka Real Estate Token. Klasma Labs has the vision of bringing real estate to the blockchain, like USDT/C brought us the digital dollar!*

---

## eip: 6065
title: Real Estate Token
description: An interface for real estate NFTs that extends EIP-721
author: Alex (), Ben Fusek (@bfusek), Daniel Fallon-Cyr ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-11-29
requires: 721

## Abstract

This proposal introduces an open structure for physical real estate and property to exist on the blockchain. This standard builds off of EIP-721, adding important functionality necessary for representing real world assets such as real estate. The three objectives this standard aims to meet are: universal transferability of the NFT, private property rights attached to the NFT, and atomic transfer of property rights with the transfer of the NFT. The token contains a hash of the operating agreement detailing the NFT holder’s legal right to the property, unique identifiers for the property, a debt value and foreclosure status, and a manager address.

## Motivation

Real estate is the largest asset class in the world. By tokenizing real estate, barriers to entry are lowered, transaction costs are minimized, information asymmetry is reduced, ownership structures become more malleable, and a new building block for innovation is formed. However, in order to tokenize this asset class, a common standard is needed that accounts for its real world particularities while remaining flexible enough to adapt to various jurisdictions and regulatory environments.

Ethereum tokens involving real world assets are notoriously tricky. This is because Ethereum tokens exist on-chain, while real estate exists off-chain. As such, the two are subject to entirely different consensus environments. For Ethereum tokens, consensus is reached through a formalized process of distributed validators. When a purely-digital NFT is transferred, the new owner has a cryptographic guarantee of ownership. For real estate, consensus is supported by legal contracts, property law, and enforced by the court system. With existing asset-backed ERC-721 tokens, a transfer of the token to another individual does not necessarily have any impact on the legal ownership of the physical asset.

This standard attempts to solve the real world reconciliation issue, enabling real estate NFTs to function seamlessly on-chain, just like their purely-digital counterparts.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

In order to meet the above objectives and create an open standard for on-chain property ownership we have created a token structure that builds on the widely-used ERC-721 standard.

### Token Components:

1. Inherits ERC-721 - Allows for backwards compatibility with the most widely accepted NFT token standard.
2. operatingAgreementHashOf - immutable hash of the legal agreement detailing the right to ownership and conditions of use with regard to the property
3. Property Unique Identifiers - legal description (from physical deed), street address, GIS coordinates, parcel/tax ID, legal owning entity (on deed)
4. debtOf - readable debt value, currency, and foreclosure status of the NFT
5. managerOf - readable Ethereum address with managing control of property

### Interfaces

The ERC-6065 inherits the ERC-721 NFT token standard for all transfer and approval logic. All transfer and approval functions are inherited from this token standard without changes. Additionally, the ERC-6065 also inherits the ERC-721 Metadata standards for name, symbol, and metadata URI lookup. This allows an NFT under the ERC-6065 standard to become interoperable with preexisting NFT exchanges and services, however, some care must be taken. Please refer to [Backwards Compatibility](#backwards-compatibility) and [Security Considerations](#security-considerations).

#### IERC6065.sol

```auto
pragma solidity ^0.8.13;

import "forge-std/interfaces/IERC721.sol";

interface IERC6065 is IERC721 {

	// This event MUST emit if the asset is ever foreclosed.
	event Foreclosed(uint256 id);

	/*
	Next getter functions return immutable data for NFT. You may implement in a struct like:

	struct EIP6065Immutable {
		string legal_description_of_property;
		string street_address;
		string geo_json;
		string parcel_id;
		string legal_owner;
		bytes32 operating_agreement_hash;
	}

	and store that in a mapping, however this specific storage method is left to the implementor.
	*/
	function legalDescriptionOf(uint256 _id) external view returns (string memory);
	function addressOf(uint256 _id) external view returns (string memory);
	function geoJsonOf(uint256 _id) external view returns (string memory);
	function parcelIdOf(uint256 _id) external view returns (string memory);
	function legalOwnerOf(uint256 _id) external view returns (string memory);
	function operatingAgreementHashOf(uint256 _id) external view returns (bytes32);

	/*
	Next getter function returns the debt denomination token of the NFT, the amount of debt (negative debt == credit), and if the underlying
	asset backing the NFT has been foreclosed on. This should be utilized specifically for off-chain debt and required payments on the RWA asset.
	It's recommended that administrators only use a single token type to denominate the debt. It's unrealistic to require integrating smart
	contracts to implement possibly unbounded tokens denominating the off-chain debt of an asset.

	If the foreclosed status == true, then the RWA asset can be seen as severed from the NFT. The NFT is now "unbacked" by the RWA.

	You may implement in a struct like:

	struct EIP6065Mutable {
		address debt_token;
		int256 debt_amt;
		bool foreclosed;
	}

	and store that in a mapping, however this specific storage method is left to the implementor.
	*/
	function debtOf(uint256 _id) external view returns (address debtToken, int256 debtAmt, bool foreclosed);

	// Get the managerOf an NFT. The manager can have additional rights to the NFT or RWA on or off-chain.
	function managerOf(uint256 _id) external view returns (address);
}
```

## Rationale

### Introduction

Real world assets operate in messy, non-deterministic environments. Because of this, validating the true state of an asset can be murky, expensive, or time-consuming. For example, in the U.S., change of property ownership is usually recorded at the County Recorder’s office, sometimes using pen and paper. It would be infeasible to continuously update this manual record every time an NFT transaction occurs on the blockchain. Additionally, since real world property rights are enforced by the court of law, it is essential that property ownership be documented in such a way that courts are able to interpret and enforce ownership if necessary.

For these reasons, it is necessary to have a trusted party tasked with the responsibility of ensuring the state of the on-chain property NFT accurately mirrors its physical counterpart. By having an Administrator for the property who issues a legally-binding digital representation of the physical property, we are able to solve for both the atomic transfer of the property rights with the transfer of the NFT, as well as institute a seamless process for making the necessary payments and filings associated with property ownership. This is made possible by eliminating the change in legal ownership each time the NFT changes hands. An example Administrator legal structure implemented by Klasma Inc. for property tokenization in the U.S. is provided in the [Reference Implementation](#reference-implementation). While an ERC-6065 token must have a legal entity to conduct the off-chain dealings for the property, this implementation is not mandatory.

### Guiding Objectives

We have designed this EIP to achieve three primary objectives necessary for creating an NFT representation of physical real estate:

#### 1. Real Estate NFTs are universally transferable

A key aspect to private property is the right to transfer ownership to any legal person or entity that has the capacity to own that property. Therefore, an NFT representation of physical property should maintain that universal freedom of transfer.

#### 2. All rights associated with property ownership are able to be maintained and guaranteed by the NFT

The rights associated with private property ownership are the right to hold, occupy, rent, alter, resell, or transfer the property. It is essential that these same rights are able to be maintained and enforced with an NFT representation of real estate.

#### 3. Property rights are transferred atomically with the transfer of the NFT

Token ownership on any blockchain is atomic with the transfer of the digital token. To ensure the digital representation of a physical property is able to fully integrate the benefits of blockchain technology, it is essential the rights associated with the property are passed atomically with the transfer of the digital token.

The following section specifies the technological components required to meet these three objectives.

### operatingAgreementHashOf

An immutable hash of the legal document issued by the legal entity that owns the property. The agreement is unique and contains the rights, terms, and conditions for the specific property represented by the NFT. The hash of the agreement attached to the NFT must be immutable to ensure the legitimacy and enforceability of these rights in the future for integrators or transferees. Upon transfer of the NFT, these legal rights are immediately enforceable by the new owner. For changes to the legal structure or rights and conditions with regard to the property the original token must be burned and a new token with the new hash must be minted.

### Property Unique Identifiers

The following unique identifiers of the property are contained within the NFT and are immutable:

`legalDescriptionOf`: written description of the property taken from the physical property deed

`addressOf`: street address of the property

`geoJsonOf`: the GeoJSON format of the property’s geospatial coordinates

`parcelIdOf`: ID number used to identify the property by the local authority

`legalOwnerOf`: the legal entity that is named on the verifiable physical deed

These unique identifiers ensure the physical property in question is clear and identifiable. These strings must be immutable to make certain that the identity of the property can not be changed in the future. This is necessary to provide confidence in the NFT holder in the event a dispute about the property arises.

These identifiers, especially `legalOwnerOf`, allow for individuals to verify off-chain ownership and legitimacy of the legal agreement. These verification checks could be integrated with something like Chainlink functions in the future to be simplified and automatic.

### debtOf

A readable value of debt and denoted currency that is accrued to the property. A positive balance signifies a debt against the property, while a negative balance signifies a credit.

The `debtOf` function also returns the boolean foreclosure status of the asset represented by the NFT. A true result indicates the associated property is no longer backing the NFT, a false result indicates the associated property is still backing the NFT.

There are no standard requirements for how these values are updated as those details will be decided by the implementor. The ERC-6065 does however standardize how these values are indicated and read for simplicity of integration.

### managerOf

A readable Ethereum address that can be granted a right to action on the property without being the underlying owner of the NFT.

This function allows the token to be owned by one Ethereum address while granting particular rights to another. This enables protocols and smart contracts to own the underlying asset, such as a lending protocol, but still allow another Ethereum address, such as a depositor, to action on the NFT via other integrations, for example the Administrator management portal. The standard does not require a specific implementation of the manager role, only the value is required. In many instances the managerOf value will be the same as the owning address of the NFT.

## Backwards Compatibility

The ERC-6065 standard is backwards compatible with ERC-721. However, it is important to note that there are potential implementation considerations to take into account before any smart contract integration. See [Security Considerations](#security-considerations) for more details.

## Reference Implementation

Klasma Labs offers a work in progress reference implementation (*see pull request above*). The technical implementation includes the following additional components for reference, this implementation is not required.

Summary of Klasma Inc. ERC-6065 implementation:

- NFT burn and mint function
- Immutable NFT data (unique identifiers and operating agreement hash)
- Simple debt tracking by Administrator
- Blocklist function to freeze asset held by fraudulent addresses (NOTE: to be implemented in the future)
- Simple foreclosure logic initiated by Administrator
- managerOf function implementation to chain this call to other supported smart contracts

### Legal Structure Implementation

This section explains the legal structure and implementation Klasma Inc. employs as an Administrator of ERC-6065 tokens. The structure detailed below is specific to property tokenization in the U.S. in the 2023 regulatory environment.

This section details an implementation of the legal standard by Klasma Inc. specifically for property tokenization in the U.S. in the 2022 regulatory environment.

[![corporate-structure](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1c20675aacd08f33d33235f7fa72b8d2167a26ec_2_690x388.jpeg)corporate-structure1920×1080 224 KB](https://ethereum-magicians.org/uploads/default/1c20675aacd08f33d33235f7fa72b8d2167a26ec)

The Klasma Inc. legal structure for U.S. ERC-6065 tokens is as follows:

- Klasma Inc., a parent company and property Administrator, owns a bankruptcy remote LLC for each individual property they act as Administrator for.
- The bankruptcy remote LLC is the owner and manager of a DAO LLC. The DAO LLC is on the title and deed and issues the corresponding NFT and operating agreement for the property.
- This structure enables the following three outcomes:

Homeowners are shielded from any financial stress or bankruptcy their physical asset Administrator encounters. In the event of an Administrator bankruptcy or dissolution the owner of the NFT is entitled to transfer of the DAO LLC, or the sale and distribution of proceeds from the property.
- Transfer of the rights to the property are atomic with the transfer of the NFT. The NFT represents a right to claim the asset and have the title transferred to the NFT owner, as well as the right to use the asset. This ensures the rights to the physical property are passed digitally with the transfer of the NFT, without having to update the legal owner of the property after each transfer.

Security note: In the event of a private key hack Klasma will not be able to reissue a Home NFT. Klasma home NFT owners who are not confident in their ability to safely store their home NFT will have varying levels of security options (multi-sigs, custodians, etc.). For public, large protocol hacks, Klasma may freeze the assets using the Blocklist function and reissue the home NFTs to the original owners.

## Security Considerations

The following are checks and recommendations for protocols integrating NFTs under this standard. These are of particular relevance to applications which lend against any asset utilizing this standard.

- Protocol integrators are recommended to check that the unique identifiers for the property and the hash of the operating agreement are immutable for the specific NFTs they wish to integrate. For correct implementation of the ERC-6065 standard these values must be immutable to ensure legitimacy for future transferees.
- Protocol integrators are recommended to check the debtOf value for an accurate representation of the value of the ERC-6065 token.
- Protocol integrators are recommended to check the foreclose status to ensure an ERC-6065 token is still backed by the asset it was originally tied to.
- For extra risk mitigation protocol integrators can implement a time-delay before performing irreversible actions. This is to protect against potential asset freezes if a hacked NFT is deposited into the protocol. Asset freezes are non-mandatory and subject to the implementation of the asset Administrator.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**Alex-Klasma** (2022-11-30):

*[post removed, EIP has been dramatically slimmed down]*

---

**dfalloncyr** (2022-12-04):

Including [@fusek](/u/fusek), the third author of EIP-6065.

We realize EIP-6065 is quite lengthy and has a lot of moving parts, so providing pointed feedback may not be particularly easy. To simplify our ask for feedback, here are three specific areas/questions we are looking for critical feedback on:

**1. Token Structure & Scalability:** Our aim is for this structure to be broad/malleable enough to scale across all jurisdictions and property types. We anticipate fractionalization models, rental protocols etc. to exist as a smart contract Eth address “owner” on top of this base layer of on-chain ownership. **Do you see issues with the scalability of the proposed structure with regard to varying jurisdictions or property types?**

**2. Legal Requirements & Digital Transferability:** With EIP-6065 we are introducing a new legal concept for property ownership. An ERC-6065 token would approximate property ownership in a new and digitally transferable form. Rather than an ERC-6065 token being an exact 1 to 1 replica of the title/deed to a property, it is a new construct for legal ownership grounded in contract law that is comprised in a digitally-transferable yet legally enforceable way. **Do you see issues with the legal rights being guaranteed with an ERC-6065 token? Do you see an issue with the digital and universal transferability? Do the legal requirements approximate property ownership accurately?**

**3. Implementation of the Administrator:** We would like the Administrator role to be as decentralized as possible. In order to provide legally enforceable ownership with every instantaneous transfer of the NFT, an Administrator role is necessary. **Do you have ideas for how to make the Administrator at decentralized as possible?**

Thanks for all of your critical feedback, it is much appreciated!

We hope that EIP-6065 can be adopted and start to contribute to the list of Ethereum tokens that will eventually provide legally enforceable rights in the digital economy ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12) ![:classical_building:](https://ethereum-magicians.org/images/emoji/twitter/classical_building.png?v=12)

---

**Theo6890** (2022-12-06):

[REPOST from Discord server]

We concluded the same back then at [@Omnia-DeFi](https://github.com/Omnia-DeFi) that you need to create an SPV that owns the house and then sell NFT of the SPV.

Otherwise, turning the house into an NFT itself is a way more heavier legal process https://twitter.com/KlasmaLabs/status/1571907145385517058?s=20&t=DhKo7sAMZsMFQy-zn7jeNg

Then the question is why choosing ERC-721 and not ERC-1155?

As you can have many types of shares, ERC-1155 might better suited as you can mint many times the same amount of the same share (same id). Obviously if you own some share you will have more rights than others, meaning a different access.

Then, you can even leverage IPFS submarine and give access based on an ERC-1155 id instead

---

**dfalloncyr** (2022-12-07):

Hi [@Theo6890](/u/theo6890) great question!

The main thinking behind relying on an ERC-721 vs. an ERC-1155 ultimately came down to legal flexibility.

Here in the US, and in many other jurisdictions, the fractionalization of real estate is enough to justify the securitization of an asset. A core goal of our proposal was to allow for the free (in a legal sense) and universal transferability of each tokenized asset, a fundamental right granted in private property ownership. **If the tokenized asset was structured in such a way that justified an argument for securitization, then the asset would be at risk of needing to comply with the regulations that apply to securities in various jurisdictions.** For the vast majority of the countries where both customers and real estate reside, this would mean complying with AML/KYC and possibly accreditation checks with every instantaneous transfer of the NFT.

You can imagine a world where someone has a DeFi loan against their home, and that loan was then packaged and lent against in various ways to multiple people. In the event of a default you NEED the home to be able to pass freely from creditor to creditor until it reaches its rightful owner without getting hung up by checks and gates. Especially if this transaction is happen in a number of seconds!

Homes, property, and real estate are one thing in our world that is fundamentally non-fungible. No two properties are the same whether it be physically or geographically/spatially. The ERC-1155 solves for this and allows for additional token structures to be easily attached to the asset. However, it also put’s the base layer on-chain ownership at risk of being deemed a security.

**We believe the foundational base layer of on-chain ownership for property and real estate needs to approximate the rights granted in private property ownership** to truly function as private property is meant to function, in a legal sense.

We think all of the fractionalization and other benefits provided by the ERC-1155 can be easily attached to a property with an additional layer of ownership, and we encourage people to build on top of our idea for a base layer on-chain deed/title!

With lawmaker’s antiquated and rudimentary understanding of crypto/financial technologies, with think it’s best to go this route in the near-term. However, maybe someday they will understand the technologies better and we can operate on an even simpler and updated token standard! We don’t see that happening for a while though…

---

**Alex-Klasma** (2022-12-08):

As the more tech-focused member of the team, I’m just not sure that ERC-1155 is worth the added complexity. It’s hard to believe that users will need to efficiently batch-transfer NFT homes, as homes or pieces of real estate more generally are so valuable.

Supporting other types of tokens, like fungible or semi-fungible with ERC-1155 is interesting, but also unclear the use-case for that is worth the complexity. Natively supporting real estate fractionalization seems a bit risky, and like the standard is doing too much. For that, we would suggest a “lego blocks” approach and building another smart contract that issues “shares” when a ERC-6065 NFT token is deposited. This would be similar to most fractional art apps available currently.

If there is a specific use case you’d like for these NFTs where ERC-1155 is better suited than 721, please let us know and we can discuss further!

---

**dfalloncyr** (2023-01-25):

**Updated structure based on discussion & feedback**

Over the past two months we have been discussing EIP-6065 in the community. Following feedback and discussion, we have arrived at a slimmed down version of the proposal for the token that optimizes for simplicity and composability with existing applications. This token standard is based on ERC-721 and contains several minor but important additions to support real estate. Given that these changes from ERC-721 are minor, we believe it is more apt to think of this standard as an **ERC-721 Real Estate Extension**. We have included a concise summary of the token structure proposal and use cases below. We will update the pull request following this additional round of feedback and discussion.

**Primary changes:**

- Removed payment and repossession functions
- Added simple payee field for receiving rental income
- Added signaling call for bridging asset off the blockchain
- Added blocklist capability
- Simplified metadata

**NFT Structure & Components**

***1. Backwards compatible with ERC-721***

***2. Hashed operating agreement***

- Hashed to ensure the immutability of the terms and conditions granted to the NFT owner with regard to the property (simply attaching the legal documents in the metadata do not guarantee the permanence of the rights for the NFT holder or future holders)
- Approximated property rights

The right to: hold, occupy, rent, alter, resell, or transfer the property

Legal recourse for home ownership

- Legal rights recognized in the property’s jurisdictional court of law to take ownership of the physical title to the property represented by the NFT from the Administrator - i.e. bridge the property off-chain

***3. Payee field***

- Editable Ethereum address field that receives any rental income payment from the Administrator sent by property management partners
- On token transfers, this field is automatically set to the new owner. Upon deposit, protocol integrations will need to revert it back to depositor address or retain the payments

***4. Bridge off-chain/change admin call***

- Public timestamp/record of the owner signifying the exercise of their right to bridge the property off-chain
- It is recommended that integrations add an alert when an owner calls this function

***5. Blocklist function***

- Administrators have the ability to block individual Ethereum addresses from sending and receiving home NFTs

**NFT Metadata - Updated by Administrator**

*1. NFT Occupier State*

1. Unoccupied
2. Owner-Occupied
3. Partner Tenant-Occupied

Current lease end date
4. Lease payment amount
5. Payment frequency
6. Property expenses

*2. Outstanding debt amount*

- Repossession threshold (note: this repossession occurs off-chain)

*3. Name and address of Administrator*

- Operating Agreement template and details

**Details of Occupier State (metadata):**

*1. Unoccupied: The Administrator has verified the home is vacant and replaced locks & keys*

- This would be the desired state before selling the NFT
- Owner is required to pay property taxes & homeowner’s insurance
- Owner may not have any outstanding balance when switching a home from Owner-Occupied to Unoccupied

*2. Owner-Occupied: Owner is occupying the home or renting it out off-chain*

- Owner is required to pay property taxes & homeowner’s insurance
- Amount of debt/unpaid balance will show in the metadata of the NFT
- Unpaid balances will be time-sensitive and trigger a repossession of the asset in the event they go unpaid. In a repossession, the home will be removed from the NFT and sold. The NFT will then have the home asset replaced with USDC from the sale to back its value.

*3. Partner Tenant-Occupied: NFT owner contracts property manager, payments managed by Administrator*

- Property taxes & homeowner’s insurance are covered by rental income; owner is required to pay any remaining tax or insurance costs not covered by rental income
- NFT owner selects property management partner; property manager pays rental income to Administrator; Administrator pays necessary property expenses (e.g. tax & insurance); Administrator sends remainder of rental income to NFT payee ETH address
- NFT owner is notified and required to pay for repairs and property expenses
- Option for “Set & Forget” program whereby the Administrator covers property expenses and fees but does not pay out rental income.

The legal structure remains the same (see “Specifications: Token Legal Requirements” and “Reference Implementation” above).

[![Klasma Legal Structure](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b5a8758f7ae29a29156b659717a842bbe986e3c2_2_690x388.jpeg)Klasma Legal Structure960×540 35.6 KB](https://ethereum-magicians.org/uploads/default/b5a8758f7ae29a29156b659717a842bbe986e3c2)

---

**Alex-Klasma** (2023-02-03):

Thanks for the proposed update, and an outline of the EIP. I agree that removing some complexity, especially around the payment logic is beneficial. I also agree that it’s important to be 100% compatible with ERC-721, as this will drastically boost adoption.

I am thinking that the *NFT Occupier State* section is perhaps a little too simplistic. What about multi-unit properties? What about different rental arrangements like short-term rentals? I think it’s hard to encompass much functionality with these three states. Perhaps these sort of states can be defined per-asset by the NFT contract issuer? Or perhaps it’s better left out of the NFT, or can be an additional document or otherwise submitted when a user is trying to sell the NFT (ie: property for sale, one tenant, lease expires at *date*, etc.)

I think RWA projects have the most issues trying to mesh the “messyness” of RWAs with the necessary certainty of smart contract applications. Smart contracts (as implemented these days), need to know the exact value, and exact specifications of any asset they are onboarding. Bad price data, or other data can lead to catastrophic failures and hacks. Where RWAs have so many states, it’s really impossible or unlikely to be able to encompass them in smart contract code. I would argue that things like this are best left out of the contracts, as it seems prone to error and problems when developers over-rely on these states for their applications.

Maybe rental contracts should be implemented by other smart contracts. Then users can customize the logic far more than you can implement in an EIP. Maybe this EIP should focus on *specifically* implementing an on-chain deed. On a home deed, you don’t need to update it with rental data, or update it when you decide to list on airbnb for a few weeks when you’re off vacationing.

I may work on another proposal to simplify this further. It seems best that we focus on the digital home deed, and de-emphasize the almost endless states the home can be in.

---

**dfalloncyr** (2023-02-23):

Thanks for the detailed review and refinement!

I agree that the suggested states above are far too specific for a token standard. RWA projects do encounter the hurdle of reconciling what is true and exists in the real world, and the digital state of the asset. The more complexity and detail in the relationship between a RWA token and the RWA itself, the more likelihood for error/misalignment and thus breaks in ecosystem infrastructure.

Focusing on creating a digital deed and enabling digital transfer of property ownership is definitely the most important aspect of this token proposal, however, it is important to not overlook the potential benefits digitization enables. One of the primary benefits of having a digital deed in the first place is the ability for a deed to act as living, breathing document of the real-time state of the property in question. Having that information in a reliable and up-to-date form will enable a whole host of future opportunities for builders and integrators of the ERC-6065. Real-time ownership is probably the most important aspect of the “state of a property”, but then there are additional attributes that are consistent across all properties and would be incredibly beneficial to have digitized and up-to-date.

All property has the following attributes and states:

- Geographical details
- Building details
- Occupancy state

In addition to those, any property operating under the ERC-6065 standard will also have:

- Administrator details
- Outstanding debt (this could be solved for in different ways, but due to the administrators requirement to keep the title of the property clean and being the liable taxpayer for the property, this probably makes sense to have.)

Having some basic standardization for the metadata of the NFT will enable more seamless collaboration and integrations across the ecosystem in the future, however, it is important to avoid being prescriptive and design a schema that is malleable enough to adapt to any property in the future.

For that reason **I suggest we update the PR with the previously mentioned component changes, and a metadata bucket requirement of: geographical details, building details, occupancy state, outstanding debt, and administrator details.** Those loose requirements will provide a good starting point for bucketing data and attributes of a property, without being too constrictive. For an example of how Klasma Labs has implemented these requirements interested parties can refer to the Klasma docs for the home NFTs they administer.

---

**Alex-Klasma** (2023-02-24):

Thanks for the response.

First, I think it will be best to explore what exactly is represented by a standard property title, and how we can get that into a digital format. What are the edge cases and pitfalls there?

Second, once we have the base layer “on-chain title”, we can expand this by adding additional metadata categories like building details, tenancy details, maintenance history. It’s important to note that these details will be opt-in by the NFT owner, they don’t need to upload anything if they don’t want to/want to remain private.

The most important thing in my mind is representing a property title on-chain AND the fact that anyone that owns this on-chain NFT has rights to the underlying title. So let’s get to that point and then expand the scope if we’d like to.

---

**dfalloncyr** (2023-03-03):

Update on required on-chain data fields & NFT components:

| Property Data Fields | Who Can Change | Where it Exists | Required for ERC-6065 |
| --- | --- | --- | --- |
| Legal Description of Property, Street Address | Cannot be changed | On-chain | Required |
| GIS Coordinates | Cannot be changed | On-chain | Required |
| Property Tax Identification Number | Cannot be changed | On-chain | Required |
| Hashed Operating Agreement for Property | Cannot be changed | On-chain | Required |
| Administrator Details | Cannot be changed | On-chain | Required |
| Blocklist of Fraudulent Addresses | Admin Only | On-chain | Required |
| Physical Deed | Admin Only | Stored in off-chain metadata | Best practice, not required |
| Easements on the Property | Admin Only | Stored in off-chain metadata | Best practice, not required |
| Covenants, Restrictions, HOA | Admin Only | Stored in off-chain metadata | Best practice, not required |
| Title Insurance provided upon Bridging | Admin Only | Stored in off-chain metadata | Best practice, not required |
| Homeowners Insurance | Admin Only | Stored in off-chain metadata | Best practice, not required |
| Building Description | Editable by owner, verifiable by Admin | Stored in off-chain metadata | Best practice, not required |
| Occupancy Status | Editable by owner, verifiable by Admin | Stored in off-chain metadata | Best practice, not required |

---

The non-required data stored off-chain and accessible via the metadata will likely function as a dynamic NFT ([dNFT](https://chain.link/education-hub/what-is-dynamic-nft))

[Chainlink functions](https://blog.chain.link/introducing-chainlink-functions/) (in beta) should enable the ability for ERC-6065 tokens to interact with existing price feed AVMs and other web2 APIs.

**This final implementation eliminates the previously discussed components: Rent Payee Ethereum Address, ChangeAdmin/Bridge Property Off-Chain.**

---

**MerkleTreeOfLife** (2023-03-04):

Awesome work here. This is the most comprehensive proposal I’ve seen for the tokenization of a physical  asset. I agree with the work you’ve done to simplify the structure from the initial write-up. In my view, optimizing for maximum composability give the asset the greatest chance of becoming widely adopted and developed upon by the community.

---

**dfalloncyr** (2023-03-07):

Thanks for your support [@MerkleTreeOfLife](/u/merkletreeoflife)! Please join the Klasma Labs [discord](https://discord.gg/eZc4gXpX) if you haven’t already ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

Updating visual of legal structure & on-chain token components.

[![Screen Shot 2023-03-07 at 12.48.16 PM](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c4bf7577ec058495117d50c738591c640e67fcc7_2_690x388.jpeg)Screen Shot 2023-03-07 at 12.48.16 PM1920×1080 264 KB](https://ethereum-magicians.org/uploads/default/c4bf7577ec058495117d50c738591c640e67fcc7)

---

**MerkleTreeOfLife** (2023-03-08):

From the new photo it looks like the legal structure is the same, but some parts of the NFT have changed?

---

**dfalloncyr** (2023-03-10):

Hi [@MerkleTreeOfLife](/u/merkletreeoflife), yes we have reduced the complexity of the NFT by moving state management for the home to the metadata, and just keeping the unique identifiers on-chain.

In the post above we lay out the on-chain components and the data that could be (best practice) stored in the metadata of the NFTs. This change removes a lot of the complexity introduced while we were originally trying to solve state management of the home with the on-chain token/NFT implementation. (Some of the points that [@Alex-Klasma](/u/alex-klasma) brought up above).

All of the on-chain components of the NFT are now immutable, and specific to the 1 of 1 individual home/parcel. The only on-chain component that has some “fluctuation” is the blocklist function which will refer to a living database of fraudulent addresses that are unable to accept or transfer the NFT (similar to Circle’s implementation for USDC).

**Note:** in the original post we were thinking the legal rights guaranteed in the hashed operating agreement would be updatable after consent from both the owner and the Administrator, however, we have reversed that decision. In the current implementation the hashed operating agreement will be created upon the tokenization of the home and will remain unchanged and unique to the parcel described in the: address, GIS coordinates, tax ID, etc… If this legal agreement needs to be updated for any reason the administrator will provide a burn function to replace the NFT with a new legal agreement.

As for the state management of the home we see this being separate from an EIP/ERC standard. There are countless benefits to having an accurate and detailed digital state of a home (building details, occupancy, etc.), however, baking this into the standard seems far too restrictive.

For Klasma Labs, we plan to implement a state management system within the metadata of the NFT in-line with the table above. Updating the metadata would not be mandatory and would be handled through both: a backend service by the Administrator, and through a frontend experience by the home owner. These states could have varying degrees of certainty/validity.

With regard to integrating these metadata states into the ecosystem we plan to use, and recommend integrators use, the [dynamic NFT](https://chain.link/education-hub/what-is-dynamic-nft) and [Chainlink functions](https://docs.chain.link/chainlink-functions/) to both automate decisions based on the current state of the home and verify the validity of the state.

We will be updating the PR with these new changes once we feel we have gotten adequate feedback on the implementation. We are collecting this feedback through this forum as well as by other means.

---

**Alex-Klasma** (2023-04-26):

Hello everyone! We have made some dramatic improvements to this EIP. The [first post](https://ethereum-magicians.org/t/updated-eip-6065-real-estate-token/11936) has been edited to reflect the most recent version of the EIP, which has been majorly edited for length, and is far simpler than before.

We would love your comments and feedbacks on this EIP bringing real estate to the blockchain via an open standard. If you’d like to read more about us, check out [Klasma Labs](https://www.klasmalabs.com/)!

---

**drllau** (2024-01-10):

Perhaps a stupid question but should this be an ERC (application interface) rather than EIP (which seems to be more focused on technical)

---

**abcoathup** (2024-01-11):

It is an ERC as it is application layer.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6065)





###



An interface for real estate NFTs that extends ERC-721

---

**drllau** (2024-01-11):

Whilst I specialise in IP law, there is a group (apart from MakerDAO) that is looking at legal title of real-property, [RWAC](https://rwaconsortium.com/). My general (admittedly non-expert) observations

1. are you solving for just one narrow (for continental size of narrow) use case?
2. is this a metadata problem (read BIM) and not DLT? as @Theo6890  pointed out, you can contain all the subagreements like property management, council connections, etc into a legal SPV in which case you then adopt all the existing DeFi infostructure for securities.
3. what additional steps are needed to evolve from a BIM to recordat to indefeasible title system?

---

**anilkondaveeti** (2024-05-12):

The standard 6065 is very interesting for our use case. Just wanted to know if 6065 move to the final state anytime sooner or still stay in the draft state. Please let us know if we can support the implementation of the standard because we have a real opportunity to use it. Thank you for your efforts and guidance.

---

**peersky** (2024-10-30):

Can this be built on top of ERC1155 as well?

