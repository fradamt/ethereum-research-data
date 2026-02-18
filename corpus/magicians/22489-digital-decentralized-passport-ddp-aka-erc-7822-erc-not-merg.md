---
source: magicians
topic_id: 22489
title: Digital Decentralized Passport (DDP) aka erc-7822 ( erc not merged into master so it is not official at time of posting )
author: Atenika.Protocol
date: "2025-01-10"
category: ERCs
tags: [identity, decentralized]
url: https://ethereum-magicians.org/t/digital-decentralized-passport-ddp-aka-erc-7822-erc-not-merged-into-master-so-it-is-not-official-at-time-of-posting/22489
views: 86
likes: 0
posts_count: 4
---

# Digital Decentralized Passport (DDP) aka erc-7822 ( erc not merged into master so it is not official at time of posting )

[github.com](https://github.com/atenika/ERCs/blob/atenika-erc-7822/ERCS/erc-7822.md)





####



```md
---
EIP:
Title: Digital Decentralized Passport
Author:
Status: Draft
Type: Standards Track
Category: ERC
Created: 2025-01-08
---

## Abstract

This proposal introduces the concept of a **Digital Decentralized Passport (DDP)**, designed to store personal information analogous to a traditional passport. The DDP includes fields for names, surnames, unique identifiers (e.g., residency or citizenship numbers), and optionally encrypted sensitive data. The passport integrates credibility points earned through social verification, endorsements from government representatives, and validations by certified organizations.

The DDP uses a multi-step verification process to establish trust and legitimacy, reflecting real-world laws and relationships. It has potential applications in voting systems, public tenders, and other scenarios requiring identity verification, aiming to mitigate fraud and increase accountability.

## Motivation

Identity fraud and unauthorized actions in critical systems (e.g., elections, corporate transactions) pose significant risks. A tamper-proof, traceable, and decentralized identity solution can address these issues. The **Digital Decentralized Passport** offers the following benefits:

```

  This file has been truncated. [show original](https://github.com/atenika/ERCs/blob/atenika-erc-7822/ERCS/erc-7822.md)










Abstract

This proposal introduces the concept of a Digital Decentralized Passport (DDP), designed to store personal information analogous to a traditional passport. The DDP includes fields for names, surnames, unique identifiers (e.g., residency or citizenship numbers), and optionally encrypted sensitive data. The passport integrates credibility points earned through social verification, endorsements from government representatives, and validations by certified organizations.

The DDP uses a multi-step verification process to establish trust and legitimacy, reflecting real-world laws and relationships. It has potential applications in voting systems, public tenders, and other scenarios requiring identity verification, aiming to mitigate fraud and increase accountability.

Motivation

Identity fraud and unauthorized actions in critical systems (e.g., elections, corporate transactions) pose significant risks. A tamper-proof, traceable, and decentralized identity solution can address these issues. The Digital Decentralized Passport offers the following benefits:

```
Fraud Prevention: Makes identity forgery and unauthorized voting significantly more difficult.
Traceability: Fraudulent activities are visible and traceable, even if hacking occurs.
Participation Verification: Ensures voting legitimacy by confirming citizenship and eligibility without compromising vote anonymity.
Integration: Can include digital signatures for contracts, citizenship status, document details, official photos, and last activity indicators to verify an individual’s activity and existence.
```

Definitions

```
Digital Decentralized Passport (DDP): A blockchain-based digital representation of an individual’s identity, validated by multiple authorities.
Unique Identifier: A country-specific or organization-specific number used to distinguish citizens or members (e.g., national ID, passport number).
Credibility Points: A decentralized metric representing trustworthiness based on social and administrative validations.
Social Verification: Confirmation of identity through connections and interactions within a decentralized network.
Administrative Validation: Verification provided by government or certified entities.
```

Specification

Structure

The DDP will be implemented as a standardized ERC (Ethereum Request for Comment) with the following structure:

Passport Fields

```
Basic Information:
    firstName: String
    lastName: String
    birthDate: Timestamp
    nationality: String (ISO 3166-1 alpha-3 code)
    uniqueIdentifier: String (encrypted or plain)

Verification Data:
    credibilityScore: Integer (cumulative score from verifications)
    verifiers: Array (list of addresses of verifying entities)
    verificationTimestamps: Array (timestamps of verifications)

Activity Indicators:
    lastActivity: Timestamp
    digitalSignature: Array (hashes of signed documents or agreements)

Optional Fields:
    profilePhoto: IPFS hash or equivalent decentralized storage reference.
    citizenshipHistory: Array (records of citizenship changes).
```

Verification Process

```
Multi-Step Verification:
    Initial data is provided by the individual.
    Verified by:
        Social Network (trusted peers sign off).
        Government or Organization (certified representatives sign off).
    Verification hashes are stored on-chain for traceability.

Credibility Points:
    Points are earned based on:
        Number of verifiers.
        Weight of the verifier (e.g., government entities > individual peers).
```

Use Cases

```
Voting Systems:
    Ensure only eligible citizens vote without linking votes to identities.

Tenders and Contracts:
    Validate identity before bidding or signing agreements.

Proof of Life:
    Activity indicators demonstrate recent interaction, reducing risks of fraud.
```

Smart Contract Methods

registerPassport

```
Inputs:
    firstName (string)
    lastName (string)
    birthDate (timestamp)
    uniqueIdentifier (string, encrypted)
    profilePhoto (optional, IPFS hash)
Outputs:
    passportId (unique on-chain ID)
```

verifyPassport

```
Inputs:
    passportId (unique ID)
    verifier (address)
    signature (hash)
Outputs:
    credibilityScore (updated score)
```

updateActivity

```
Inputs:
    passportId (unique ID)
    activityTimestamp (timestamp)
Outputs:
    Updated lastActivity
```

getPassport

```
Inputs:
    passportId (unique ID)
Outputs:
    All fields associated with the passport.
```

Security Considerations

```
Privacy: Ensure sensitive data (e.g., unique identifiers) can be encrypted.
Tamper Resistance: Use blockchain immutability to secure verification history.
Anonymity in Voting: Maintain vote secrecy while confirming eligibility.
```

Appendix: Example Implementation

pragma solidity ^0.8.0;

contract DigitalDecentralizedPassport {

struct Passport {

string firstName;

string lastName;

uint256 birthDate;

string nationality;

string uniqueIdentifier;

uint256 credibilityScore;

address verifiers;

uint256 verificationTimestamps;

uint256 lastActivity;

string profilePhoto;

}

```
mapping(uint256 => Passport) public passports;
mapping(address => bool) public trustedVerifiers;
uint256 public passportCounter;

modifier onlyTrustedVerifier() {
    require(trustedVerifiers[msg.sender], "Not a trusted verifier");
    _;
}

function registerPassport(
    string memory firstName,
    string memory lastName,
    uint256 birthDate,
    string memory nationality,
    string memory uniqueIdentifier,
    string memory profilePhoto
) public returns (uint256) {
    passportCounter++;
    passports[passportCounter] = Passport(
        firstName,
        lastName,
        birthDate,
        nationality,
        uniqueIdentifier,
        0,
        new address[](0),
        new uint256 ,
        block.timestamp,
        profilePhoto
    );
    return passportCounter;
}

function addTrustedVerifier(address verifier) public {
    trustedVerifiers[verifier] = true;
}

function removeTrustedVerifier(address verifier) public {
    trustedVerifiers[verifier] = false;
}

function verifyPassport(uint256 passportId, address verifier) public onlyTrustedVerifier {
    Passport storage passport = passports[passportId];
    passport.verifiers.push(verifier);
    passport.verificationTimestamps.push(block.timestamp);
    passport.credibilityScore += 1; // Simplified scoring mechanism
}

function updateActivity(uint256 passportId) public {
    Passport storage passport = passports[passportId];
    passport.lastActivity = block.timestamp;
}
```

}

This implementation demonstrates a basic structure for the Digital Decentralized Passport, which can be extended to meet additional requirements.

Verification should be done by authority like goverment, local district representative or similar entity with high credibility, in Poland authoverification will be possible after signing proper code with ePUAP in one of first live implementation of this ERC concept.

## Replies

**MASDXI** (2025-01-11):

You should care about storing sensitive information on-chain.

---

**Arvolear** (2025-01-11):

I get the point but this is exactly why passports are not like that.

First, the problem of issuance. There has to be someone (government in our case) that you must trust to be sure that data in a passport is legit. Here I can claim that I am Satoshi Nakamoto and the system will just believe that.

Second, the problem of privacy. If I disclose my passport data, how can a system be sure that I am not being impersonated? Confidential data must remain confidential. That’s why protocols like Rarimo and OpenPassport exist. They use Zero Knowledge Proofs (ZKP) to maintain that confidentiality.

Third, how can integrations actually benefit from that standard? Proof of humanity is impossible (impersonation), KYC is impossible (no trusted issuance), no described real-world functionality. Why should this ERC exist?

---

**Atenika.Protocol** (2025-02-08):

its to standarize public visible and verifable signatures from profiles verified by authorities. Anonymity is not delivered at the begining but further in process.

At first poeple need to recognize this profile as 100% legit for participation in discussion and voting without 3rd party as confirming that data comes prom this particular profile X1.

In this concept some data will be public, especially of authorities which validating profiles and emitting list of hashes of profile id’s legit for some actions in system or not legit for such actions.

use Zero Knowledge Proofs (ZKP) is to compelx for many people, they need to be able verify some initial actions that it is done by profile X1 not any other using comon sense and having little mathematical skills and very little knowlege about technology.

