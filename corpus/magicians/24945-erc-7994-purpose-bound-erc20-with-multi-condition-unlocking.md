---
source: magicians
topic_id: 24945
title: "ERC-7994: Purpose-Bound ERC20 with Multi-Condition Unlocking (Extension of EIP-7291)"
author: 64anushka
date: "2025-07-29"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7994-purpose-bound-erc20-with-multi-condition-unlocking-extension-of-eip-7291/24945
views: 99
likes: 3
posts_count: 3
---

# ERC-7994: Purpose-Bound ERC20 with Multi-Condition Unlocking (Extension of EIP-7291)

Link:

This ERC extends the concept of EIP-7291: Purpose-Bound Money by introducing **multi-condition unlocking** for ERC20 tokens. It enables tokens to be *purpose-bound* to a recipient with programmable restrictions like:

- Time-based unlocking (e.g., after a specific timestamp)
- KYC or identity verification (e.g., Merkle-based proof)
- Use-case restrictions (e.g., only for specific smart contracts or spending categories)
- Arbitrary custom conditions (pluggable checkers)

### Motivation

EIP-7291 introduced a valuable idea: restrict how a token can be spent (e.g., for aid, education, donations). However, real-world use cases often require **multiple overlapping conditions**, not just recipient enforcement.

Use cases that benefit from this proposal:

- Public disbursements: Tokens for subsidies, aid, or education that unlock only if time + KYC conditions are met.
- Enterprise payroll: Tokens that unlock at specific dates, only for verified employees.
- Governance/incentives: Tokens that can be claimed by voters after fulfilling DAO participation.

This ERC proposes a clean, modular extension to ERC20 that supports multiple conditions per transfer, each verifiable via on-chain checkers.

### How It Works

- A bindPurpose() function locks tokens for a recipient with an array of UnlockConditions.
- Each condition includes a conditionType (e.g., “TIME”, “KYC”) and ABI-encoded conditionData.
- A global registry maps each conditionType to a condition checker contract.
- The claim() function verifies that all conditions are met before releasing the tokens.

Example:

Bind tokens to `user` with:

- A TIME condition unlocking after Sept 1, 2024
- A KYC condition with Merkle proof of identity

Tokens are held by the contract until both are satisfied.

## Replies

**jhfnetboy** (2025-07-31):

So how about the progress? I think it is a good idea

---

**Akash** (2025-07-31):

Thanks for the kind words! We’ve just received the EIP number and are currently awaiting further reviews.

