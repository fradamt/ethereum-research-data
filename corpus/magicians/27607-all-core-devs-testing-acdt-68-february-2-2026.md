---
source: magicians
topic_id: 27607
title: All Core Devs - Testing (ACDT) #68, February 2, 2026
author: system
date: "2026-01-27"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-68-february-2-2026/27607
views: 37
likes: 2
posts_count: 4
---

# All Core Devs - Testing (ACDT) #68, February 2, 2026

### Agenda

Fusaka:

- partial cell proofs
- blob-devnet-0

MIN_EPOCHS_FOR_DATA_COLUMN_SIDECARS_REQUESTS field is not being respected by supernodes, and they still hold up to 18d worth of blob data - incorrect

Gas limit testing:

- eth/70 updates
- benchmarking updates - benchmarkoor demo next week

Glamsterdam:

- bal-devnet-2

Add EIP-7928 Block-level Access Lists JSON RPC methods
- engine: define EIP-7928 API methods
- Known blockers:

Besu — Remove gasSpent from Receipt RLP Trie Encoding
- Nethermind — Remove gasSpent from Receipt RLP Trie Encoding
- Nethermind — engine_getPayloadV6 Missing blobGasUsed Field
- Nimbus-EL — Gloas Opcodes Activated at Fulu Instead of Gloas
- Geth — 6 BAL State Transition Bugs (PR state/bal: fix multiple bugs in BAL state transition by qu0b · Pull Request #33735 · ethereum/go-ethereum · GitHub)
- Reth - missing ETH logs, gas refunds, swapn/dupn EIPs
- Geth - missing ETH logs eip
- Erigon - missing ETH logs, gas refunds, slotnum, swapn/dupn EIPs

[epbs-devnet-0](https://notes.ethereum.org/@ethpandaops/epbs-devnet-0)

- Variable PTC deadline by fradamt · Pull Request #4843 · ethereum/consensus-specs · GitHub
- implementation updates?

epbs-devnet-1 spec release: [Release: `v1.7.0-alpha.2` · Issue #4858 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/issues/4858)

Hegota

- headliner proposal deadline approaching, only 2 more days left

**Meeting Time:** Monday, February 02, 2026 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1901)

## Replies

**abcoathup** (2026-01-28):

## Call details

### Video, transcript & chatlog

- All Core Devs Testing #068 - Forkcast - [Forkcast] by EF Protocol Support

### News coverage

- [Ethereal news] edited by @abcoathup
- ACD After Hours: ACDT #68 - [ACD After Hours] by @Christine_dkim
- [Etherworld] by @yashkamalchaturvedi

### Resources

- Glamsterdam Upgrade - Forkcast
- Hegotá Upgrade - Forkcast

---

**system** (2026-02-02):

### Meeting Summary:

The meeting focused on updates and discussions related to various Ethereum development topics, including partial cell proofs, gas-benching, and ePBS implementation. Barnabas led the discussion, highlighting issues with super nodes struggling to handle blob demand due to misalignment between clients and databases, and proposed adjustments to address this. The team discussed the readiness of different clients for the upcoming devnet, with Stefan providing updates on testing and issues across multiple clients. There was consensus to target the new ePBS Alpha 2 specification for devnet zero, with Justin confirming the removal of the variable PTC deadline change to focus on a simpler subset of features. The team also discussed the upcoming headliner proposal deadline and the need for submissions within the next two days.

**Click to expand detailed summary**

The meeting focused on updates and discussions related to various Ethereum development topics, including partial cell proofs, gas-benching, and ePBS implementation. Barnabas led the discussion, highlighting issues with super nodes struggling to handle blob demand due to misalignment between clients and databases, and proposed adjustments to address this. The team discussed the readiness of different clients for the upcoming devnet, with Stefan providing updates on testing and issues across multiple clients. There was consensus to target the new ePBS Alpha 2 specification for devnet zero, with Justin confirming the removal of the variable PTC deadline change to focus on a simpler subset of features. The team also discussed the upcoming headliner proposal deadline and the need for submissions within the next two days.

### Next Steps:

- Daniel: Take a look into the BlobNet Zero issue with minimum epoch for DataColumn sidecar request
- Prysm team: Take a look into respecting the minimum epoch flag for DataColumn sidecar request
- Other CL teams: Begin implementing or finish implementing partial cells to add to BlobNet Zero devnet
- Rafael : Come online next week to showcase benchmarking tool with a 5-10 minute live demo
- Besu: Remove the gas parameter from the receipt
- Nimbus: Fix the issue where activation of some GLOS features is happening too early
- Geth: Work on identified issues
- Toni: Have a look at PRs 726 and 727 and figure out merging async, target merger by Wednesday
- Besu : Merge open PRs for metrics and prefetch today or tomorrow
- Marc : Make the change to move BlockAccessList to the payload
- Jared : Implement the Engine API method and fix bugs in the next few days
- Jen : Review PRs in progress and provide proper update
- Stefan Starflinger: Get BAL test numbers up and add Nimbus into the testing scope
- Justin: Make the Alpha 2 release
- All teams with Hagota proposals: Submit proposals within the next 2 days before the deadline

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: J?juAQ5y)
- Download Chat (Passcode: J?juAQ5y)
- Download Audio (Passcode: J?juAQ5y)

---

**system** (2026-02-02):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=ay6kY5oOIeE

