---
source: magicians
topic_id: 22759
title: Client testing call #23, February 3, 2025
author: parithosh
date: "2025-02-03"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/client-testing-call-23-february-3-2025/22759
views: 124
likes: 3
posts_count: 1
---

# Client testing call #23, February 3, 2025

## Key Decisions & Next Steps

- Devnet 6 Deployment:
Announcement in Interop channel; client teams should prepare for testing.
- EIP-7702 Implementation:
More documentation needed; community contributions welcome.
- Tx Pool Tests:
Address specific cases, integrate with EEST and Hive testing, review test list.
- PeerDAS:
Continue edge case syncing; prioritize after Pectra completion.
- EOF Testing:
Prepare for Kurtosis-based testing after Pectra Devnet 6.
- ePBS & IL Testing:
Proceed with standalone domain testing before considering mainnet inclusion.

## Devnet 5 & 6 Updates

### Devnet 5

- Nethermind BLS issue fixed; nodes restored.
- Finalizing Devnet 5; focus shifted to Devnet 6.

### Devnet 6

- ACD meeting suggested address change; new EEST release is out.
- Kurtosis is updated; most clients are passing the Hive test.
- Execution spec test running; one bug in Assertor fixed.
- Since interop went well, Pari set up a node for Devnet 6. Genesis file setup complete;
- Lido also reached out to test.
- Erigon Caplin request – Pari to follow up after the call.
- MEV will be included with Devnet 6; sanity check will be completed before release.

> Note: Devnet 6 announcement will be made on the Interop Channel.

## EIP-7702 Implementation Resources

- Documentation needed; contributions welcome.
- Delegation Signing (Forge Test): Guide
- Viem 7702 Support: Docs
- rafting 7702 Transactions (Cast): Guide and example

## Client Updates

### Geth

- Most PRs merged; stable release expected this week.
- Testnet updates by next week.

## Tx Pool Testing Plans

- Matt Garnett asked if there will be testing for critical cases.
- PK is working on tx invalidation tests.
- Mario’s Team:

Creating tx tests for EEST and Hive.
- Looking for community feedback on Execution Spec Test Discussion.

## PeerDAS

- Interop completed last week.
- PeerDAS Devnet 4 spec testing for clients is ongoing.
- 2 clients are fully ready, 3 are partially ready.
- Once launched, high success probability is expected.
- Out-of-memory bug in Prysm; PeerDAS test scheduled for tomorrow.
- Edge case syncing needed.
- Full focus after Pectra completion.
- Peerdas devnet 4 spec

## EOF Testing

- Fuzzing progressing well; N/M added.
- Reth-N/M Besu integration.
- Next Steps:

Conduct Kurtosis-based testing post-Pectra Devnet 6.
- Ensure execution transaction test coverage.
- EOF support from Reth now merged into the main branch.
- Testing team available for Kurtosis support.

Client Docker Image Builder

## ePBS & Inclusion List (IL) Testing

- IL and ePBS testing support added.
- Running local devnet between Prysm & Geth; Lighthouse to be added.
- Tested both Fulu and Electra forks.
- Consensus: It is premature to include ePBS in the Fulu fork.
- Preferred approach: Create an own fork & separate epoch for measuring impact.
- Standalone domain testing for IL & ePBS is ongoing.
