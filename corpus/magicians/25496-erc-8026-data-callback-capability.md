---
source: magicians
topic_id: 25496
title: "ERC-8026: Data Callback Capability"
author: lsr
date: "2025-09-17"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8026-data-callback-capability/25496
views: 48
likes: 0
posts_count: 2
---

# ERC-8026: Data Callback Capability

## Abstract

This proposal defines an EIP-5792 capability that allows apps to request user data. Additionally, this proposal specifies how wallets communicate with an app-provided callback URL so apps can check users’ information and optionally modify transaction requests before users approve them.

## Motivation

Apps often need user data such as contact and shipping information as part of a transaction request. Today, there is no standard for:

- How apps describe the data they need from wallets.
- How apps can validate user information before allowing them to proceed with a transaction (for example, ensuring a merchant can ship to a user’s address before allowing them to complete a payment).
- How wallets provide app-requested information, both during pre-signing validation and after a transaction request has been signed and submitted by a user.
- How apps can update transaction requests based on user-provided information (for example, updating a payment request to include a shipping fee).

This capability provides a way for apps and wallets to communicate about this information.

## Replies

**lsr** (2025-09-17):

draft here: [Add ERC: Data Callback Capability by lukasrosario · Pull Request #1216 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1216)

