---
source: magicians
topic_id: 25386
title: All Core Devs - Testing (ACDT) #53 | Sep 15 2025
author: system
date: "2025-09-08"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-53-sep-15-2025/25386
views: 119
likes: 2
posts_count: 3
---

# All Core Devs - Testing (ACDT) #53 | Sep 15 2025

### Agenda

Happy Merge 3rd Anniversary! ![:partying_face:](https://ethereum-magicians.org/images/emoji/twitter/partying_face.png?v=15)

![Image](https://github.com/user-attachments/assets/970267b5-6d22-4f2b-b9bf-13f2204842b9)

#### Fusaka

##### Fusaka Devnet Updates

- Devnet-3 update (https://dora.fusaka-devnet-3.ethpandaops.io/).

Regained finalization, but lagging as of 2025-09-15 11:00 UTC.
- ethpandaops will investigate this “unplanned” non-finalization ))

Devnet-5 launched on Wed 2025-09-10 14:00 UTC.

- @felix314159 verified correct EL client configurations pre-launch via eth_config using a new execution-spec-tests command, more info:

Blog: https://steel.ethereum.foundation/blog/blog_posts/2025-09-15_eth-config/
- Docs: Execute Eth Config - Ethereum Execution Spec Tests

Current overview by @barnabasbusa

- 3 BPOs so far (https://dora.fusaka-devnet-5.ethpandaops.io/).
- Next BPO scheduled for Tues 2025-09-16 06:32 UTC
- PSA: tysm ethpandaops diagnostic nodes: Modified Prysm nodes with some additional monitoring.
- PSA: watchtower is not ran for devnet-5: If you need your client image to be updated, reach out to one of the pandas (from #interop).
- @tersec reported nimbus-Nethermind issues. These are on the Nethermind side as confirmed by @flcl42: These involve a complex reorg condition, a fix is WIP.
- Teku non-critical Prometheus exception, a fix is WIP.
- Teku-reth block building issue resolved (reth regression that was almost immediately resolved).
- @tersec brought up a kzg-issue that Nimbus is debugging with Prysm #interop message link, still a WIP.
- @tersec shared that Nimbus can’t currently run consensus-specs release alpha.6 with kzg libraries 2.1.2 (but passes with kzg 2.1.1). @tbenr confirmed the same behavior when testing Teku and these KZG library versions. It’s suspected that a client can’t in general pass the alpha.6 tests fully without a column ID ordering which 2.1.2 (but not 2.1.1) enforce. @jtraglia will check the issue and create a new release.

No Shadow fork testing update.

##### eth_calls and EIP-7825 TX Limit Cap Interaction

- @pk910 brought up the implications of ~16.78mio tx gas limit cap from EIP-7825 following-up from a discussion with @holgerd77 in #execution-devs.
- @pk910 tested eth_call with “unlimited” gas and found issues with geth, erigon and reth #execution-dev message link.

##### New Hive Simulator for  EIP-7934

New Hive Simulator `eest/consume-sync` (live since Wed 2025-09-10) [@fselmo](/u/fselmo)

- Introduced to test EL synchronization capabilities, in particular for EIP-7934 RLP Execution Block Size Limit.
- Overview in docs: Methods of Running Tests - Ethereum Execution Spec Tests

![Image](https://github.com/user-attachments/assets/a36f8ed9-7518-47de-8a49-4b1bc7c2bd79)

##### EL Consensus Test Overview

Fusaka EL Hive results overview by @spencer-tb

- Fusaka Dashboard now contains all EEST and ethereum/tests state tests filled for PragueToOsaka, Osaka and all OsakaToBPO* transition forks, ~20,000 tests.
- Results are good: Mainly non-critical (e.g., exception message matching). Remaining failures should be resolved over the course of next week.
- Subsequently: Focus on results for other forks on the “Generic” dashboard.

### Gas limit testing update

STEEL/EEST:

- A new benchmark test wrapper format ongoing (abstracts out the EIP-7825 tx gas limit for better test dev-ex) :

https://github.com/ethereum/execution-spec-tests/pull/1945

Verifying a bloatnet testing approach via [execute](https://eest.ethereum.org/main/running_tests/execute/eth_config/) is ongoing.

Prototyping:

- XEN gas benchmark tests with mainnet state WIP ethereum/execution-spec-test#2101 @jochem-brouwer.

### Glamsterdam

#### BALs

- Breakout # 2 last Wed 2025-09-10, youtube.

EIP-7928 Breakout #2, Sept 10, 2025 · Issue #1708 · ethereum/pm · GitHub

New test vector release [v1.0.1](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.0.1).

- Addresses issues found in both the specs and tests.

#### ePBS

- Breakouts

### Other Topics

Reth mainnet stall.

- Post Mortem.
- @marioevz has implemented a test for this case. WIP: triggering it via a reorg scenario in the consume/engine simulator.

**Meeting Time:** Monday, September 15, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1719)

## Replies

**system** (2025-09-15):

### Meeting Summary:

The meeting, marked as ACDT 53 and coinciding with “Happy Mergeary,” began with updates on DevNet 5 including recent fork upgrades and ongoing issues with block validation across different clients. The team discussed various technical challenges including re-org problems affecting multiple nodes, issues with the CKSG library, and concerns about DevNet 3 experiencing unplanned non-finality. Updates were also shared on testing frameworks, gas-limit testing, and block-level access lists, with plans for upcoming breaker calls and continued focus on DevNet 5 development.

**Click to expand detailed summary**

The meeting began with participants joining and exchanging greetings. Akash offered assistance with the stream to Dan, and it was confirmed that the AI would take notes automatically. The meeting’s facilitator, stepping in for Mario who was out of office, welcomed everyone and announced that this was ACDT number 53. The agenda was shared, and the meeting noted the significance of the day being “Happy Mergeary,” marking 3 years since the merge.

The team discussed updates on Fusaka devnet 5, including recent fork upgrades and increasing block counts. Barnabas reported issues with orphan blocks and MEV machine rate limiting, which was recently fixed. Dustin explained ongoing problems with the KSG library affecting different clients, particularly Nimbus, though this was confirmed to be a separate issue from Nethermind’s reorg problems. The team also noted that different clients are running various versions of the CKSG library, which may be contributing to the validation inconsistencies.

The team discussed issues with re-orgs causing errors in Lighthouse and Nimbus nodes, which Alexey attributed to incorrect parent block selection when handling consensus client payloads from different forks. Justin Traglia mentioned a separate bug affecting Nimbus’s ability to run Alpha-6 reference tests without version 2.1.2, and committed to fixing this in the ckzg library. Enrico reported that Teku had also experienced similar issues and reverted their ckzg library update. The team also provided updates on DevNet 5, which launched last Wednesday with three BPOs completed so far, and noted that Watchtower updates would not be automatic for this network.

The team discussed issues with DevNet 3, which experienced unplanned non-finality. Barnabas and Parithosh noted that the network had been at around 70-78% completion before dropping to 62-63% due to a client push and Watchtower update causing a restart loop. The team agreed to investigate the cause of this unplanned event, while maintaining focus on DevNet 5 as the current priority.

Felipe introduced a new simulator called ConsumeSync, which was added to Highview to verify client sync after certain tests, specifically for the block RLP limit in Osaka. Spencer provided an update on Execution layer consensus tests, reporting that the Ethereum general state tests have been successfully migrated to the new Execution-spec test framework and are now running in Hive with mostly non-critical fails that can be easily addressed.

The team discussed updates on gas-limit testing and block-level access lists. Jochem reported setting up a test network to research the impact of raising the gas limit to 60 million, particularly focusing on state-heavy contracts like Zen. Toni mentioned that the next breaker call is scheduled for Wednesday next week, with plans to test the first CL implementation once it’s available. PK raised a concern about ETH calls, noting that while the new gas limit applies to transactions, some clients (Geth, Erigon, and Reth) are enforcing a 50 million limit even when none is specified, which affects UIs and should be addressed before any release.

### Next Steps:

- Justin Traglia to fix the issue in ckzg library and publish a new release.
- Nethermind team to test and deploy the fix for the re-org issue.
- Barnabas and Parithosh to investigate the unplanned non-finality issue on DevNet 3.
- Felipe to address the timeout issues in the new ConsumeSync simulator on HiveView.
- Spencer-tb to add more BPO tests and EIP7918 tests to the EL test suite.
- Execution-spec tests team to complete the new test wrapper format for improving test developer experience.
- Jochem to continue setting up the test network for researching 60 million gas limit behavior with Xen contract.
- Geth, Erigon, and Reth teams to fix the ETH calls regression issue where they enforce a limit on read-only methods.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: ZQk=r0c9)
- Download Chat (Passcode: ZQk=r0c9)

---

**system** (2025-09-15):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=CC5XZ834xIc

