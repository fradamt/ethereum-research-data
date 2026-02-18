---
source: magicians
topic_id: 27616
title: "ERC-8144: Multi-Chain Product Identifier Resolution for GS1"
author: Apriloracle
date: "2026-01-29"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8144-multi-chain-product-identifier-resolution-for-gs1/27616
views: 30
likes: 0
posts_count: 3
---

# ERC-8144: Multi-Chain Product Identifier Resolution for GS1

**Abstract**

This EIP describes an open, multi-chain infrastructure for resolving product identifiers that follow GS1 standardized formats (such as GTINs) to publicly available product information. The architecture uses deterministic contract deployment across multiple EVM-compatible networks to provide redundant, token-free access to product data from sources including Open Food Facts and other open databases.

The system is designed as public digital infrastructure, providing non-discriminatory resolution services without requiring token ownership or payment.

## Motivation

Current product identifier resolution typically relies on centralized services operated by standards bodies or commercial entities. This creates several challenges:

1. Single points of failure: Centralized resolvers can experience downtime or service discontinuation.
2. Access restrictions: Some resolver services require membership, fees, or authentication.
3. Geographical limitations: Services may not be equally accessible across all jurisdictions.
4. Lack of transparency: Resolution logic and data sources may not be publicly auditable.

A decentralized, multi-chain resolver mesh addresses these challenges by:

*   Providing redundant resolution paths across multiple networks.

*   Ensuring open, non-discriminatory access without tokens or fees.

*   Creating transparent, auditable resolution logic.

*   Enabling global accessibility independent of any single jurisdiction or organization.

This approach is particularly relevant for supply chain transparency, food information systems, and digital product passports where open access to product data serves public interest. Further we have published research paper supporting this EIP: [Decentralized Multi-Chain Infrastructure for GS1 Product Identifier Resolution](https://zenodo.org/records/18332235)

## Replies

**Apriloracle** (2026-02-05):

[@abcoathup](/u/abcoathup)

For our pull request to move forward do we need to remove all the errors mentioned here?



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1508)














####


      `master` ← `Apriloracle:master`




          opened 04:20PM - 02 Feb 26 UTC



          [![](https://avatars.githubusercontent.com/u/86314121?v=4)
            Apriloracle](https://github.com/Apriloracle)



          [+144
            -0](https://github.com/ethereum/ERCs/pull/1508/files)







This PR introduces a new Informational EIP describing a decentralized, multi-cha[…](https://github.com/ethereum/ERCs/pull/1508)in architecture for resolving GS1 product identifiers to publicly available product information.

The proposal is informational only and does not introduce protocol changes or application-level standards.

Discussion thread: https://ethereum-magicians.org/t/eip-xxxx-multi-chain-product-identifier-resolution-for-gs1/27616

---

**abcoathup** (2026-02-05):

All validator errors need to be resolved AND it needs to be reviewed by an ERC editor (which I am not).

