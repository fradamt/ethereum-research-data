---
source: magicians
topic_id: 27437
title: "ERC-1643: Document Management Standard (ERC-1400)"
author: AccessDenied403
date: "2026-01-14"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-1643-document-management-standard-erc-1400/27437
views: 44
likes: 0
posts_count: 1
---

# ERC-1643: Document Management Standard (ERC-1400)

> This ERC allows documents to be associated with a smart contract and a standard interface for querying / modifying these contracts, as well as receiving updates (via events) to changes on these documents.
> Examples of documentation could include offering documents and legends associated with security tokens.
>
>
> GitHub issue

This ERC is part of ERC-1400 and it was created in 2018.

ERC-1400 is still a popular RWA standards even if the ERC has never been finalized.

So what we should finalize ERC-1643?

1. This standard is independent from the underlying token (ERC-1400, ERC-20, ERC-721) and can be finalized even if it is not the case for ERC-1400
2. It has already been used in production by all ERC-1400 based token. At some point, it makes sense to finalize a standard used in production.
3. This standard offers a lightweight version for on-chain document management, which is important for tokenization and RWA.

For ERC-1400, see also [Why is ERC-1400 not listed on eips.ethereum.org?](https://ethereum-magicians.org/t/why-is-erc-1400-not-listed-on-eips-ethereum-org/20280) and [ERC-1400 and ERC-1410 - Security Token and Partially Fungible Token](https://ethereum-magicians.org/t/erc-1400-and-erc-1410-security-token-and-partially-fungible-token/1314)
