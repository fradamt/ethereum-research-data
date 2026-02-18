---
source: magicians
topic_id: 17007
title: "Draft ERC: Smart Contract Interface to implement confidentiality and legal status transparency to crypto security tokens"
author: hagen
date: "2023-12-05"
category: ERCs
tags: [erc, security-token]
url: https://ethereum-magicians.org/t/draft-erc-smart-contract-interface-to-implement-confidentiality-and-legal-status-transparency-to-crypto-security-tokens/17007
views: 1208
likes: 2
posts_count: 4
---

# Draft ERC: Smart Contract Interface to implement confidentiality and legal status transparency to crypto security tokens

## Abstract

This standard is an extension of [ERC-7551](https://github.com/ethereum/ERCs/pull/85) / Magicians: ([ERC-7551: Crypto Security Token Smart Contract Interface ("eWpG")](https://ethereum-magicians.org/t/draft-eip-erc-7551-crypto-security-token-smart-contract-interface-ewpg/16416)). While ERC-7551 defines a **compliant** transfer, freezing of securities, enforced transfers by operators and machine readable properties of the issuance itself, this standard addresses the additional **regulatory requirements** according to the German Electronic Security Act ([eWpG](https://www.gesetze-im-internet.de/ewpg/index.html)) in terms of confidentiality and transparency of the legal status of a security.

As no current approved standard is supporting the full set of demanded functionality, this standard shall, as an extension of ERC-7551, enable the industry to build applications relying on a fully compliant On-Chain register for securities.

Additionally to the requirements covered in ERC-7551, this standard seeks to fulfil:

### Privacy of Balances

The Smart Contract must check, if the wallet that is calling the report function, is eligible to get the Balance of a given wallet.

### Full descriptive Report of Balances

The smart contract must provide a full set of properties along with the Balance as ruled out in the law.

### Support of different legal statuses of a security

The smart contract must support different statuses of a security and enable transfer restrictions according to certain statuses. This is done by an approach based on ERC-1155.

## Motivation

The German Electronic Security Act aims to be agnostic to the technology that is used to build a Crypto Security Register according to its §16. Although EVM intentionally was designed to be public and permissionless on the level of the blockchain as well as on the level of smart contracts, the regulated market could benefit from the flexibility that come with smart contracts and the potentials that come with a potential combination of securities and utilities.

To overcome the monopole of the Central Securities Depository in traditional finance, there must be a reliable standard that is addressing the regulatory demands for crypto securities.

Additionally, the implementation should embed as much regulation as possible into the smart contract to prevent the rise of siloed solutions developed by each regulated crypto registrar. This enables the different players in the market to integrate these securities in their trading platforms and exchanges independent from the regulated registrar that is managing them.

Under these prerequisites, a security standard should not only address the restrictions based on KYC and AML rules but should also address the dimensions of privacy as well as transparency in terms of completeness of information about the properties and the legal status of a security.

This leads to the following requirements.

Please follow the technical requirements and details on GitHub:

GitHub: [Add ERC: Security token interface for confidentiality and legal status transparency to crypto security tokens by itinance · Pull Request #143 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/143)

## Replies

**drllau** (2024-01-10):

My particular concern is whether establishing an ERC just for Germany sets a bad precedent … numerous countries are now reviewing their digital assets, in particular UK just closed their securities sandbox review and there’s always Singapore offering R&D incentives. I’d like to see a quick survey of comparable jurisdictions and attempt to establish the great common denominator amongst a reasonable set of jursidictions with the few oddball requirements being carved out or opt-in. Legal status is not conferred by the contract but a recognition of a recordat, whether official or not which has a choses-in-action or enforceable by competent authority. If you are incising the legal status within the smart contract, you are heading into the choses-in-rem approach (think ship which allows a debt to be nailed to mast) which requires less supporting infrastructure, but consensus as to the transitions in legal status (including adverse possession).

---

**SamWilsn** (2024-02-12):

> The Smart Contract must check, if the wallet that is calling the report function, is eligible to get the Balance of a given wallet.

I’d be careful with this. All information stored on the blockchain is public, so this may not be sufficient to meet the requirements in the law. That said, I am not a lawyer nor do I speak German, so take this with a grain of salt.

---

**SamWilsn** (2024-02-12):

> Authorization will be done with an ECDSA signature provided along with the original message containing the necessary input parameters.

Limiting authorization to ECDSA signatures excludes smart contract wallets from participating. I’d recommend using `ecrecover` alongside [ERC-1271](https://eips.ethereum.org/EIPS/eip-1271) for offline signatures.

