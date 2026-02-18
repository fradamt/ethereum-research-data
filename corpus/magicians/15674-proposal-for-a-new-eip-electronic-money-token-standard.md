---
source: magicians
topic_id: 15674
title: "Proposal for a new EIP: Electronic Money Token Standard"
author: roinevirta
date: "2023-09-05"
category: EIPs
tags: [erc, token, mica]
url: https://ethereum-magicians.org/t/proposal-for-a-new-eip-electronic-money-token-standard/15674
views: 566
likes: 0
posts_count: 1
---

# Proposal for a new EIP: Electronic Money Token Standard

# Proposal for a new EIP: Electronic Money Token Standard

## Executive Summary

The [Markets in Crypto Assets regulation](https://eur-lex.europa.eu/eli/reg/2023/1114), which came into force in June 2023, implements various requirements for token issuers and centralised exchanges, among others. To ensure that the Ethereum ecosystem implements MiCA-conforming assets uniformly, this EIP proposes a standardised way for issuing and tracking Electronic Money Tokens (EMTs) as defined in Title IV of the regulation. The specification is derived from the minimal requirements set forth through the regulation and aims to provide a lightweight framework on which more complex EMTs can be built upon, extending ERC-20.

## Definitions

By “MiCA”, “MiCAR”, or “regulation” I mean the *Regulation (EU) 2023/1114 of the European Parliament and of the Council* available at https://eur-lex.europa.eu/eli/reg/2023/1114 unless otherwise specified.

The definitions below are directly from MiCA (Article 3) for convenience.

- ”crypto-asset”:  means a digital representation of a value or of a right that is able to be transferred and stored electronically using distributed ledger technology or similar technology;
- “electronic money token” (or “EMT”): means a type of crypto-asset that purports to maintain a stable value by referencing the value of one official currency;
- ”official currency”: means an official currency of a country that is issued by a central bank or other monetary authority;
- ”issuer”: means a natural or legal person, or other undertaking, who issues crypto-assets;

## Background

Regulation (EU) 2023/1114 of the European Parliament and of the Council, colloquially known as the Markets in Crypto Assets Regulation (MiCA or MiCAR), came into force in the EU in June 2023. It will be enforceable on electronic money token (EMT) issuers from June 2024.

While the regulation does not set forth direct technical requirements for EMTs, I believe setting an ecosystem-wide standard for the technical implementation of tokens issued under the regulation as EMTs would be beneficial (see “Objectives” for more information).

## Objectives

The objective of this EIP is to standardise how EMTs are issued within the Ethereum ecosystem. By doing so:

- Application developers can provide & communicate data on EMTs in a uniform fashion, improving customer experience and transparency
- The token issuer’s ability to track fund movements pertaining to particular transaction types is made easier
- Token issuers and the broader ecosystem have programmatically and widely accepted methods for recognising important token characteristics

The primary aim of this EIP is to ensure that EMT issuers utilise a common standard and to avoid the situation where a plethora of proprietary EMTs with different interfaces and characteristics exist.

## Specification

This section outlines the suggested specification derived through an analysis of MiCA’s Title IV and other relevant articles of the regulation. The specification does not account for other relevant regulations, such as MiFID II. This standard would extend ERC-20.

### Reference currency information

Users of an EMT should have strong guarantees as to which currency the EMT references. By standardising a method for recording this data, dApps, marketplaces, block explorers, and other applications could show the data directly to the end-user, allowing them to make better-informed choices.

Therefore, the public immutable string-type variable `referenceCurrency` is set at construction.

The issuer should set the value of the `referenceCurrency` to equal the string defined [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217), table A.1. For example, an EMT referencing the euro would have its `referenceCurrency` variable set to `EUR` while an EMT referencing the Swedish krona would have its `referenceCurrency` variable set to `SEK`.

### Issuer information

EMTs can only be issued by certain legal persons. To improve transparency in regards to who the issuer of the asset is, the data should be available on the blockchain. By recording this information within the EMT itself, it can be read through a standard method and displayed to the end-user in dApps, marketplaces, and other venues.

Therefore, the public immutable string-type variable `issuer` is set at construction.

The issuer should set the value of the `issuer` variable in a manner which clearly identifies the issuer. The recommendation would be to use the issuer’s licence number (if applicable) or business ID together with the name of the issuer. Example values are

- Test Ltd (FI​​12345678)
- Registered Company NV (0110223344)

### White paper information

EMT issuers must publish a crypto-asset white paper on their website. It must be publicly accessible by the starting date of the offer to the public of the EMT of the admission to trading of the token. (MiCA, Article 48). To improve transparency in regards to who the issuer of the token is, the data should be available on the blockchain. By recording this information within the EMT itself, it can be read through a standard method and displayed to the end-user in dApps, marketplaces, and other venues.

Therefore, the public mutable string-type variable `whitepaperURI` is implemented. The variable does not need to be set at construction and can be modified by the issuer. Modifications of the variable should trigger an event so that users can track changes to the white paper.

The value of the `whitepaperURI` should be a URL, IPFS URI, or similar.

Furthermore, the regulation’s Article 51, paragraph 9, states: *“…white paper shall be made available in a machine-readable format.”* Based on this requirement, I would like to open the discussion on how (if necessary) the machine-readable format could be delivered on the smart contract level. Here are a few potential approaches to the machine-readable white paper format:

1. Ignore it – it is not necessary to have this information available at the smart contract level
2. Stipulate a common format for the whitepaperURI variable: for example, a tuple or an array where the first value is the “normal” whitepaper and the second value is machine-readable. Allow leaving either or both empty.
3. Create a new variable, e.g. whitepaperMachineReadableURI, to record the machine-readable data

Here, I would argue against option 1 as, depending on the draft regulatory technical standards, the machine-readable white paper may include information that would be extremely useful to display on a dApp/marketplace/etc. Front-end.

### Optional types

The suggestions below may not necessarily warrant implementation due to the creation of unnecessary “bloat”. These datapoints are already sufficiently available through the implementation of the above. However, I am happy to hear feedback on whether, how, and if at all the below should be implemented.

#### Authorised venues

Article 48 states (paraphrasing) that *an EMT may be offered to the public or admitted to trading only by the issuer or by a person who has received written consent from the issuer.* While the issuer can publish this information on a website or similar, the information could also be useful to be available on the smart contract level.

For example, if the addresses of the authorised venues were made available (e.g. `mapping(address => bool) public authorisedVenues`), an actor could verify, through programmatic means, that they are not sourcing the EMT from an unauthorised venue. However, the implications to the end-users are unclear, and this method would (it seems) mostly only serve as a way for strongly authenticating authorised venues.

The authorised venues could also be identified through other means, such as an array of venue names of URIs.

#### Significant EMT identification

MiCA imposes different rules for how significant and their “normal” counterparts are treated (see MiCA Title IV, Chapter 2). Publishing this information at the contract level would improve transparency and could be utilised in other smart contracts to change contract behaviour.

Therefore, the public mutable boolean `isSignificant` could be implemented. The variable should be modifiable by the issuer. Event logging could be made available so that changes could be indexed.

#### Aggregate value of transactions

The ERC-20 `transfer()` and `transferFrom()` functions could be extended to include information about the value of the given transaction. This stems from Article 43, paragraph 1 (which also applies to EMTs): *”The criteria for classifying asset-referenced tokens as significant asset-referenced tokens shall be … (c) the average number and average aggregate value of transactions in that asset-referenced token per day during the relevant period, is higher than 2,5 million transactions and EUR 500 000 000 respectively”*.

However, adding this functionality would likely impose unnecessary inter-compatibility challenges while adding little value as the requirements outlined in Article 43, paragraph 1c can also be fulfilled by off-chain indexing & tracking arrangements.

## Recommended reading

To understand the implications of MiCAR, I recommend the following sources (in increasing difficulty/granularity):

- “What is MiCA?”, a brief presentation by Juuso Roinevirta & Patrik Johansson
- “Markets in Crypto-Assets Regulation”, a brief overview on deadlines by ESMA
- “MiCA Regulation: New regulatory framework for Crypto-Assets Issuers and Crypto-Asset Services Providers in the EEA”, a brief overview by White & Case
- “What is MiCA?”, a short blog post by Juuso Roinevirta & Patrik Johansson
- MiCAR in EUR-Lex

## Feedback

I welcome all feedback on this proposal. In particular, I am looking for feedback related to

- my interpretation of the implications of MiCA on EMTs (and other relevant regulations);
- technical feedback and discussion on the best method for implementation;
- feedback related to the “Optional types” under “Specification”; and
- whether some of the variables/methods defined are redundant.

The technical specification provided above is only a starting point and I hope to receive help from a more technically inclined person(s) to ensure the actual implementation would be well thought out, maximally composable, and (gas) efficient. If you are such a person, please get in touch.

I also request feedback on:

1. Would it be beneficial to add a field for recording the issuer’s URI (such as a website). Why yes/no?

While I prefer continuing the discussion on this forum, I can also be reached via X ([@roinevirta](https://twitter.com/roinevirta)) or Telegram.
