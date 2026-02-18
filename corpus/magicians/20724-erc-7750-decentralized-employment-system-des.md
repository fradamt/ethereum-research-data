---
source: magicians
topic_id: 20724
title: "ERC-7750: Decentralized Employment System (DES)"
author: jamesavechives
date: "2024-08-06"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7750-decentralized-employment-system-des/20724
views: 241
likes: 0
posts_count: 4
---

# ERC-7750: Decentralized Employment System (DES)

### Body:

**Link to PR**: [ERC-7750 Pull Request](https://github.com/ethereum/ERCs/pull/573)

---

### Introduction:

This topic is dedicated to the discussion of ERC-7750: Decentralized Employment System (DES). The ERC proposes a blockchain-based employment system that records employment history, allows the creation of companies, labor contracts, salary deposits, and includes a review system for both companies and employees.

The motivation behind this ERC is to bring transparency, immutability, and trust to employment by leveraging blockchain technology. By recording employment history on-chain, enabling decentralized company creation, and automating contract enforcement, DES aims to promote a fairer and more transparent employment ecosystem.

### Key Features:

1. Employment History Recording: Immutable and publicly accessible employment records.
2. Decentralized Company Creation: Users can found new companies on the blockchain.
3. Labor Contracts: Standardized contracts between companies and employees, enforceable by smart contracts.
4. Automated Salary Payments: Companies deposit salaries in escrow, and payments are automated according to the contract terms.
5. Review System: Public and on-chain review system for both companies and employees.

### Purpose of This Discussion:

We welcome feedback, suggestions, and discussions on the following aspects:

- The overall design and scope of the ERC.
- Potential improvements or additional features.
- Security considerations.
- Compatibility with existing standards.
- Implementation strategies.

Please feel free to contribute to the discussion and help refine ERC-7750.

## Replies

**SamWilsn** (2025-02-04):

I’m curious, are you building a product/project on top of this standard? From a quick read, this doesn’t seem… substantive enough to be used as a full on-chain replacement for a payroll system, especially in the international sense. I’m just concerned this is a purely theoretical standard with no path to implementation.

---

**jamesavechives** (2025-02-09):

We do intend to build or inspire real-world applications on top of this proposed standard. That said, **ERC-7750** isn’t meant to be a one-size-fits-all, *immediate* replacement for every aspect of an international payroll system. Instead, it lays the groundwork for core on-chain functionalities—managing company records, employee identities (via Soulbound Tokens), contracts, escrow-based payments, and dispute resolution—leaving ample room for extensions or custom modules to handle more specialized requirements (like multi-currency payments, local compliance, and taxation).

Here’s how we envision moving toward practical adoption:

1. Core On-Chain Framework:
The ERC defines universal functions and events (e.g., createContract, depositSalary, raiseDispute) that can be relied upon by dApps or platforms wanting a tamper-proof record of employment and payment obligations.
2. Modular Extensions for Local Needs:
Because employment laws, tax codes, and payroll structures vary by jurisdiction, the standard is designed to be extensible. Projects can integrate off-chain or Layer 2 compliance modules, payment rails for specific currencies, or KYC/AML layers to satisfy local regulations—without compromising the primary, on-chain contract logic.
3. Interoperability with Existing Services:
Realistically, many payroll aspects (tax withholdings, benefits, insurance) still require partnerships or APIs to off-chain services. ERC-7750 can act as the source of truth for employment relationships and payment triggers, while specialized providers handle localized compliance and disbursements.
4. Community-Driven Implementations:
We expect third-party developers to build products on top of ERC-7750—ranging from HR dApps that track employee credentials on-chain to payroll solutions that incorporate stablecoins or fiat on/off-ramps. By standardizing the contract interfaces, we reduce friction for any project wanting to hook into these employment records and payment flows.
5. Incremental Migration:
Rather than instantly replacing entire international payroll systems, projects can adopt ERC-7750 for more trust-sensitive or high-level tasks at first (like verifying work completion or recording disputes), then gradually integrate deeper payroll features as they mature and gain regulatory clarity in their regions.

In short, **ERC-7750** is neither purely theoretical nor intended to singlehandedly solve every global payroll challenge. It aims to **standardize** the essential on-chain components of employment—identity, contracts, payments, reputation, and dispute resolution—so innovators can build more specialized solutions on top. This layered approach is how we see a path toward tangible, real-world usage.

---

**jamesavechives** (2025-04-15):

I think you are right! It is really hard to form a common decentralized employment standard, the real purpose of mine is to build a system to record employment history on the blockchain.

