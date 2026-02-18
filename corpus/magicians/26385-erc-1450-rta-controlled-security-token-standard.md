---
source: magicians
topic_id: 26385
title: "ERC-1450: RTA-Controlled Security Token Standard"
author: devender-startengine
date: "2025-11-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-1450-rta-controlled-security-token-standard/26385
views: 122
likes: 3
posts_count: 5
---

# ERC-1450: RTA-Controlled Security Token Standard

Hello Magicians! I’m excited to share our work on regulated security tokens.

## Abstract

This EIP introduces a token standard for securities that require regulatory compliance under SEC regulations (Reg CF, Reg D, Reg A+). The standard enforces Registered Transfer Agent (RTA) exclusive control over all token operations, implementing a request/review/execute workflow that ensures compliance checks before any transfers occur.

## Motivation

Current token standards like ERC-20 were designed for utility tokens and lack the necessary controls for regulated securities. Direct peer-to-peer transfers bypass compliance requirements, creating regulatory risks. Security tokens need enforced KYC/AML checks, transfer restrictions, recovery mechanisms, and complete audit trails.

This standard is based on StartEngine’s operational experience with $1B+ in compliant security token offerings, addressing real-world requirements from 5+ years of production usage.

## Specification

Check out the full specification on GitHub:

**ERC Draft**: https://github.com/ethereum/ERCs/pull/1335

The complete reference implementation can be found [here](https://github.com/StartEngine/erc1450-reference).

## Key Features

- Transfer request system with RTA approval workflow
- Multi-sig security through RTAProxy pattern
- Court order execution and lost wallet recovery
- Configurable fee management
- Account freezing for compliance

Would love to see an insightful discussion rolling!

## Replies

**devender-startengine** (2025-11-11):

Hello everyone,

Following our initial post, we’ve made significant enhancements to the ERC-1450 reference implementation based on early feedback and production requirements. Here’s what’s new:

1. UUPS Upgradeability Pattern
We’ve added fully upgradeable versions of both contracts:
2. Security Improvements

- Fixed critical vulnerabilities in transfer request processing
- Added replay attack protection
- Implemented time-lock features for sensitive operations
- Multi-sig bypass vulnerabilities patched

1. Fee Function Improvements

- Updated getTransferFee() to match specification exactly
- Better handling of fee collection in transfer requests
- Support for batch operations with fee optimization

![:memo:](https://ethereum-magicians.org/images/emoji/twitter/memo.png?v=12) Links

- GitHub: GitHub - StartEngine/erc1450-reference
- NPM Package: npm install @startengine/erc1450
- Python Package: pip install startengine-erc1450
- EIP PR: Update ERC-1450: Move to Draft by devender-startengine · Pull Request #1335 · ethereum/ERCs · GitHub

Best,

Devender

---

**devender-startengine** (2025-12-23):

Hello everyone,

Quick update on ERC-1450’s progress:

PR Status ([Update ERC-1450: Move to Draft by devender-startengine · Pull Request #1335 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1335)):

- All CI checks passing (EIP Walidator, CodeSpell, Markdown Linter, HTMLProofer, Link Check)
- John Shiple (@johnshiple), the original 2018 author, has reviewed and approved the PR
- Currently awaiting editor review from @g11tech, @SamWilsn, or @xinbenlv

Reference Implementation Update:

Since our last post, the [GitHub - StartEngine/erc1450-reference](https://github.com/StartEngine/erc1450-reference) has matured significantly:

- 643 passing tests across 38 test files
- 86%+ branch coverage
- Active security audit underway with Halborn
- Clean static analysis (Mythril, Slither)

We believe the specification is ready for review. The standard addresses a real gap in the ecosystem—there’s currently no ERC that properly handles SEC-regulated securities with RTA-exclusive control, which is a legal requirement for compliant security tokens in the US.

We’d welcome any technical feedback from the community, and respectfully request editor attention when bandwidth permits.

Thank you!

---

**devender-startengine** (2025-12-23):

We’d love community feedback on a few design decisions:

1. RTA-Exclusive Control vs Shared Control: ERC-1450 gives the RTA
exclusive control over transfers. ERC-3643 uses a validator system.
What are the tradeoffs for US-regulated securities specifically?
 @TokenySolutions - curious about your experience here.
2. Fee Token Design: We use a single fee token (e.g., USDC) rather
than multiple accepted tokens. This simplifies validation but reduces
flexibility. Thoughts?
3. Recovery Mechanism: We rely on controllerTransfer() for
court-ordered transfers rather than a separate recovery system.
Is this sufficient for regulatory requirements?
4. Compatibility with ERC-3643: Has anyone explored interoperability
between RTA-controlled (ERC-1450) and validator-controlled (ERC-3643)
security tokens?

Reference implementation (643 tests, Halborn audit in progress):

[GitHub - StartEngine/erc1450-reference](https://github.com/StartEngine/erc1450-reference)

cc [@adamdossa](/u/adamdossa) @vladimirfomene

---

**devender-startengine** (2026-01-06):

Subject: ERC-1450 Update: Halborn Audit Complete ![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=15)

Hello everyone,

Exciting update on ERC-1450:

Security Audit Complete

The Halborn security audit has been finalized (December 2025) with 100% of findings addressed:

| Severity | Count | Status |
| --- | --- | --- |
| Critical | 1 | Solved |
| High | 0 | - |
| Medium | 0 | - |
| Low | 6 | 3 Solved, 3 Risk Accepted |
| Informational | 11 | 1 Solved, 10 Acknowledged |

The critical finding (fee bypass vulnerability) was resolved by implementing a single ERC-20 fee token design. Full report will be published by Halborn shortly.

Key Remediations:

- Single ERC-20 fee token design (simplified, more secure)
- .transfer() → .call() for ETH transfers
- 7-day expiration for multisig operations
- Double rejection prevention

Reference Implementation: [GitHub - StartEngine/erc1450-reference](http://github.com/StartEngine/erc1450-reference)

- 643 tests passing
- 86%+ branch coverage
- Production-ready

PR #1335 is updated and ready for editor review.

Thank you!

