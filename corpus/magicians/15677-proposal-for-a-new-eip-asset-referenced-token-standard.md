---
source: magicians
topic_id: 15677
title: "Proposal for a new EIP: Asset-Referenced Token Standard"
author: roinevirta
date: "2023-09-05"
category: EIPs
tags: [erc, token, mica]
url: https://ethereum-magicians.org/t/proposal-for-a-new-eip-asset-referenced-token-standard/15677
views: 1046
likes: 3
posts_count: 4
---

# Proposal for a new EIP: Asset-Referenced Token Standard

# Proposal for a new EIP: Asset-Referenced Token Standard

## Executive Summary

The [Markets in Crypto Assets regulation](https://eur-lex.europa.eu/eli/reg/2023/1114), which came into force in June 2023, implements various requirements for token issuers and centralised exchanges, among others. To ensure that the Ethereum ecosystem implements MiCA-conforming assets uniformly, this EIP proposes a standardised way for issuing and tracking Asset-Referenced Tokens (ARTs) as defined in Title III of the regulation. The specification is derived from the minimal requirements set forth through the regulation and aims to provide a lightweight framework on which more complex ARTs can be built upon, extending ERC-20.

## Definitions

By “MiCA”, “MiCAR”, or “regulation” I mean the *Regulation (EU) 2023/1114 of the European Parliament and of the Council* available at [EUR-Lex - 02023R1114-20240109 - EN - EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/1114) unless otherwise specified.

The definitions below are directly from MiCA (Article 3) for convenience.

- ”crypto-asset”:  means a digital representation of a value or of a right that is able to be transferred and stored electronically using distributed ledger technology or similar technology;
- “asset-referenced token” (or “ART”): means a type of crypto-asset that is not an electronic money token and that purports to maintain a stable value by referencing another value or right or a combination thereof, including one or more official currencies;
- ”official currency”: means an official currency of a country that is issued by a central bank or other monetary authority;
- ”issuer”: means a natural or legal person, or other undertaking, who issues crypto-assets;
- ”reserve of assets”: means the basket of reserve assets securing the claim against the issuer;

## Background

Regulation (EU) 2023/1114 of the European Parliament and of the Council, colloquially known as the Markets in Crypto Assets Regulation (MiCA or MiCAR), came into force in the EU in June 2023. It will be enforceable on asset-referenced token (ART) issuers from June 2024.

While the regulation does not set forth direct technical requirements for ARTs, I believe setting an ecosystem-wide standard for the technical implementation of tokens issued under the regulation as ARTs would be beneficial (see “Objectives” for more information).

## Objectives

The objective of this EIP is to standardise how ARTs are issued within the Ethereum ecosystem. By doing so:

- Application developers can provide & communicate data on ARTs in a uniform fashion, improving customer experience and transparency
- The token issuer’s ability to track fund movements pertaining to particular transaction types is made easier
- Token issuers and the broader ecosystem have programmatically and widely accepted methods for recognising important token characteristics

The primary aim of this EIP is to ensure that ART issuers utilise a common standard and to avoid the situation where a plethora of proprietary ARTs with different interfaces and characteristics exist.

## Specification

This section outlines the suggested specification derived through an analysis of MiCA’s Title III and other relevant articles of the regulation. The specification does not account for other relevant regulations, such as MiFID II. This standard would extend ERC-20.

### Standardised reference asset information

ARTs must reference an asset or a basket of assets. It is therefore critical that the end user of such token can understand the referenced asset(s). By recording this information within the ART itself, it can be read through a standard method and displayed to the end-user in dApps, marketplaces, and other venues.

Therefore, the public immutable string-type variable `referencedAsset` is set at construction.

The issuer should set the value of the `referencedAsset` variable in a manner which describes the referenced asset accurately and with minimal chance of misinterpretation. Therefore, a unique globally accessible and recognised identifier, such as an ISIN is preferred. Examples values are

- ISIN: 000K0VF05-4
- European Patent Register: EP4243592
- TARIC: 1806 10 15
- Chemical element symbol: Au

### Issuer information

ARTs can only be issued by certain legal persons. To improve transparency in regards to who the issuer of the asset is, the data should be available on the blockchain. By recording this information within the ART itself, it can be read through a standard method and displayed to the end-user in dApps, marketplaces, and other venues.

Therefore, the public immutable string-type variable `issuer` is set at construction.

The issuer should set the value of the `issuer` variable in a manner which clearly identifies the issuer. The recommendation would be to use the issuer’s licence number (if applicable) or business ID together with the name of the issuer. Example values are

- Test Ltd (FI​​12345678)
- Registered Company NV (0110223344)

### White paper information

ART issuers must publish a crypto-asset white paper on their website. It must be publicly accessible by the starting date of the offer to the public of the ART of the admission to trading of the token. (MiCA, Article 28). To improve transparency in regards to who the issuer of the asset is, the data should be available on the blockchain. By recording this information within the ART itself, it can be read through a standard method and displayed to the end-user in dApps, marketplaces, and other venues.

Therefore, the public mutable string-type variable `whitepaperURI` is implemented. The variable does not need to be set at construction and can be modified by the issuer. Modifications of the variable should trigger an event so that users can track changes to the white paper.

The value of the `whitepaperURI` should be a URL, IPFS URI, or similar.

Furthermore, the regulation’s Article 19, paragraph 9, states: *“…white paper shall be made available in a machine-readable format.”* Based on this requirement, I would like to open the discussion on how (if necessary) the machine-readable format could be delivered on the smart contract level. Here are a few potential approaches to the machine-readable white paper format:

1. Ignore it – it is not necessary to have this information available at the smart contract level
2. Stipulate a common format for the whitepaperURI variable: for example, a tuple or an array where the first value is the “normal” whitepaper and the second value is machine-readable. Allow leaving either or both empty.
3. Create a new variable, e.g. whitepaperMachineReadableURI, to record the machine-readable data

Here, I would argue against option 1 as, depending on the draft regulatory technical standards, the machine-readable white paper may include information that would be extremely useful to display on a dApp/marketplace/etc. Front-end.

### Circulating token information

Whereas ERC20 already implements a `totalSupply()` -function, the total supply and the circulating supply of an ART may be unequal at times. For example, the issuer could mint 10 tokens but only sell 5 tokens with the intention of later selling the remaining 5 tokens.

Therefore, the public uint-type variable `circulatingSupply` is implemented.

This would improve the accounting and transparency as it pertains to the total amount of circulating tokens and compatibility with Article 30, paragraph 1 (“Issuers of asset-referenced tokens shall… disclose … the amount of asset-referenced tokens in circulation”).

Changing the value of  `circulatingSupply` could happen through a few methods:

1. The issuer has the right to change the value directly; or
2. New functions releaseAndTransfer() and lockAndTransfer() are implemented, which increment and decrement, respectively, the circulating supply. The functions should only be executable by the issuer.

### Aggregate value of means of exchange transactions

MiCA differentiates between “means of exchange” transactions (later, “MET”) and other transactions. This functionality would provide a means for tracking and registering METs.

The motivation for implementing this functionality lies in Article 23, paragraph 1: *”Where, for an asset-referenced token, the estimated quarterly average number and average aggregate value of transactions per day associated to its uses as a means of exchange within a single currency area is higher than 1 million transactions and EUR 200 000 000, respectively, the issuer shall:(a) stop issuing that asset-referenced token; and (b) within 40 working days of reaching that threshold, submit a plan to the competent authority to ensure that the estimated quarterly average number and average aggregate value of those transactions per day is kept below 1 million transactions and EUR 200 000 000 respectively.”*

Currently, there is no way of differentiating between MET and other transaction types. By implementing a new transaction type, the MET transactions could be recorded and accounted for more uniformly. It is critical for the issuers of ARTs to account for METs.

This functionality could be simply implemented as a “clone” of the existing `transfer()` and `transferFrom()` functions, aptly called `MetTransfer()` and `MetTransferFrom()`, respectively. Rest of the applicable logic could be implemented off-chain.

Alternatively, the `transfer()` and `transferFrom()` functions could be extended with similar functions whose inputs are extended as follows:

- function transfer(address _to, uint256 _value) → function transfer(address _to, uint256 _value, uint8 _type); and
- function transferFrom(address _from, address _to, uint256 _value) → function transferFrom(address _from, address _to, uint256 _value, uint8 _type).

…where `_type` encodings would be generally agreed upon (e.g., such that `_type==1` is a MET transaction).

I am keen to hear feedback on whether implementing this functionality would be feasible off-chain or through some other means so as not to interfere with widely used `transfer()` and `transferFrom()` functions.

This functionality, however, is challenged from the beginning. DeFi protocols and other users of ARTs have little incentive to correctly account for METs using the provided methods unless they are coerced into doing so. Therefore, it is unclear whether its implementation would have the intended effect of differentiating between MET and other transactions.

### Optional types

The suggestions below may not necessarily warrant implementation due to the creation of unnecessary “bloat”. These datapoints are already sufficiently available through the implementation of the above. However, I am happy to hear feedback on whether, how, and if at all the below should be implemented.

#### Aggregate value of transactions

The ERC-20 `transfer()` and `transferFrom()` functions could be extended to include information about the value of the given transaction. This stems from Article 43, paragraph 1: *”The criteria for classifying asset-referenced tokens as significant asset-referenced tokens shall be … (c) the average number and average aggregate value of transactions in that asset-referenced token per day during the relevant period, is higher than 2,5 million transactions and EUR 500 000 000 respectively”*.

However, adding this functionality would likely impose unnecessary inter-compatibility challenges while adding little value as the requirements outlined in Article 43, paragraph 1c can also be fulfilled by off-chain indexing & tracking arrangements.

#### Complaints information

Article 31, paragraph 1, of the regulation states: *“Issuers … shall establish and maintain effective and transparent procedures for the prompt, fair and consistent handling of complaints received from holders of asset-referenced tokens and other interested parties.”* Information about these processes could be relayed by recording a URI pointing to the complaints procedures at the smart contract level.

Therefore, the public mutable string-type variable `complaintsURI` could be implemented. There should be no requirement to set the variable at construction and it should be modifiable by the issuer. Event logging would not be necessary.

#### Reserve of assets information

Article 30, paragraph 1, of the regulation states: *“Issuers of asset-referenced tokens shall … disclose … value and composition of the reserve of assets referred to in Article 36. Such information shall be updated at least monthly.”* Information on where the end-user can obtain information related to the backing asset reports could be standardised at the smart contract level.

Therefore, the public mutable string-type variable `reserveOfAssetsInformationURI` could be implemented. There should be no requirement to set the variable at construction and it should be modifiable by the issuer. Event logging could be made available so that new reports could be indexed.

Alternatively, the variable could simply contain an array of tuples with information regarding the value and composition of the reserve of assets (e.g., `[(100,000K0VF05-4),(50,111K1VF16-5)]`)

#### Authorised venues

Article 16 states (paraphrasing) that *an ART may be offered to the public or admitted to trading only by the issuer or by a person who has received written consent from the issuer.* While the issuer can publish this information on a website or similar, the information could also be useful to be available on the smart contract level.

For example, if the addresses of the authorised venues were made available (e.g. `mapping(address => bool) public authorisedVenues`), an actor could verify, through programmatic means, that they are not sourcing the ART from an unauthorised venue. However, the implications to the end-users are unclear, and this method would (it seems) mostly only serve as a way for strongly authenticating authorised venues.

The authorised venues could also be identified through other means, such as an array of venue names of URIs.

#### Significant ART identification

MiCA imposes different rules for how significant and their “normal” counterparts are treated (see MiCA Title III, Chapter 5). Publishing this information at the contract level would improve transparency and could be utilised in other smart contracts to change contract behaviour.

Therefore, the public mutable boolean `isSignificant` could be implemented. The variable should be modifiable by the issuer. Event logging could be made available so that changes could be indexed.

## Recommended reading

To understand the implications of MiCAR, I recommend the following sources (in increasing difficulty/granularity):

- “What is MiCA?”, a brief presentation by Juuso Roinevirta & Patrik Johansson
- “Markets in Crypto-Assets Regulation”, a brief overview on deadlines by ESMA
- “MiCA Regulation: New regulatory framework for Crypto-Assets Issuers and Crypto-Asset Services Providers in the EEA”, a brief overview by White & Case
- “What is MiCA?”, a short blog post by Juuso Roinevirta & Patrik Johansson
- MiCAR in EUR-Lex

## Feedback

I welcome all feedback on this proposal. In particular, I am looking for feedback related to

- my interpretation of the implications of MiCA on ARTs (and other relevant regulations);
- technical feedback and discussion on the best method for implementation;
- feedback related to the “Optional types” under “Specification”; and
- whether some of the variables/methods defined are redundant.

The technical specification provided above is only a starting point and I hope to receive help from a more technically inclined person(s) to ensure the actual implementation would be well thought out, maximally composable, and (gas) efficient. If you are such a person, please get in touch.

I also request feedback on:

1. Would it be beneficial to add a field for recording the issuer’s URI (such as a website). Why yes/no?

While I prefer continuing the discussion on this forum, I can also be reached via X ([@roinevirta](https://twitter.com/roinevirta)) or Telegram.

## Replies

**JoakimEQ** (2023-09-14):

This looks pretty interesting and would be a landmark EIP as the first one created in a kind of “collaboration” with one of the biggest governmental organizations in existance.

Its especially important to see this + [Proposal for a new EIP: Electronic Money Token Standard](https://ethereum-magicians.org/t/proposal-for-a-new-eip-electronic-money-token-standard/15674) because no matter what ethereum does, this WILL be a standard some developers / projects / teams need to adhere to.

So enshrining it as an official EIP would be a great thing to do as soon as possible.

---

**roinevirta** (2023-11-20):

As per the [Draft Regulatory Standards released in EBA’s Consultation Paper](https://www.eba.europa.eu/sites/default/documents/files/document_library/Publications/Consultations/2024/Consultation%20on%20RTS%20on%20the%20use%20of%20ARTs%20and%20EMTs%20denominated%20in%20a%20non-EU%20currency%20as%20a%20means%20of%20exchange%20%28MiCAR%29/1063478/CP%20RTS%20on%20the%20use%20of%20ARTs%20and%20EMTs%20denominated%20in%20a%20non-EU%20currency%20as%20a%20means%20of%20exchange%20under%20Art.%2022%286%29%20MiCAR.pdf) on 8 November, introducing the `MetTransfer()`and `MetTransferFrom()` would help with the implementation of *Option 1* under point 50. Furthermore, it would also make it easier for the relevant authorities to later expand the scope of *Option 2* in a manner following the spirit of the regulation.

While I foresee that similar legislation may be taking place in other jurisdictions and introducing new `transfer()` and `transferFrom()` functions for each jurisdiction may be painful, it may be more prudent to already start considering a more universal transfer tracking function (as suggested in the original post through the use of `_type`.

---

**makemake** (2023-11-20):

*(repost from lobstersdao chat)*

I don’t like compliance Olympics. We can try to attempt to be compliant to all of their rules, but then you’re not really using crypto. If you try to take away what makes crypto great than I don’t see the point in not banking regularly.

From a purely technical POV, things like whitepaperuri are completely useless. All of that information can be queried out of band off chain

