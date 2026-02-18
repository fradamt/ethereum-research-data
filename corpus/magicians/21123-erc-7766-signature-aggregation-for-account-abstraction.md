---
source: magicians
topic_id: 21123
title: "ERC-7766: Signature Aggregation for Account Abstraction"
author: alex-forshtat-tbk
date: "2024-09-18"
category: ERCs
tags: [erc, account-abstraction, signatures, erc-4337]
url: https://ethereum-magicians.org/t/erc-7766-signature-aggregation-for-account-abstraction/21123
views: 412
likes: 0
posts_count: 1
---

# ERC-7766: Signature Aggregation for Account Abstraction

The core ERC-4337 previously included the specification for signature aggregation.

However, as this feature is not required for the functioning of the Account Abstraction, it is being extracted from the core ERC-4337 into a standalone specification.

This specification is currently identical to the one previously implemented in ERC-4337 and does not require any modifications to the deployed ERC-4337 contracts.

However, being a standalone proposal, “ERC-7766: Signature Aggregation” will continue evolving separately from ERC-4337 on its own timeline.

This is the PR to create the new ERC:

https://github.com/ethereum/ERCs/pull/626

This is the PR to remove the Signature Aggregation specification from ERC-4337:

https://github.com/ethereum/ERCs/pull/627
