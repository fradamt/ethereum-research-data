---
source: magicians
topic_id: 25624
title: All Core Devs - Execution (ACDE) #222, October 9, 2025
author: system
date: "2025-09-29"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-222-october-9-2025/25624
views: 176
likes: 2
posts_count: 5
---

# All Core Devs - Execution (ACDE) #222, October 9, 2025

### Agenda

- Fusaka

devnets update?
- Holesky status
- blob submission APIs

Scaling Updates

- state access benchmarks by @jochem-brouwer

Glamsterdam

- devnets update?
- testing update
- non-headliner EIP proposal: 1 week after we set fusaka mainnet date
- update on repricing EIPs by @misilva73
- EIP-8032 PFI by @gballet
- EIPs 7791, 7923, 5920, and 7907/7903 by @charles-cooper

**Meeting Time:** Thursday, October 09, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1748)

## Replies

**abcoathup** (2025-10-02):

### Summary

*[[@adietrichs](/u/adietrichs) action items copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1426794486595452958)]*

- @bbusa confirm decision on removing named forks after Prague from the blob schedule in the genesis files. see ⁠execution-dev,
- clients: look into BALs metrics support, check with Katya,
- @misilva73 look into whether EIP-2926 should be included in repricings meta EIP,
- (implicit action item) @adietrichs merge PRs to add PFI EIPs to Glamsterdam meta EIP

### Recordings/Stream

- All Core Devs Execution #222 - Forkcast
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- ACDE #222: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]
- ACDE #222 summary tweet thread by @poojaranjan
- Highlights from ACDE #222 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]
- Fusaka $2,000,000 Audit Contest! | Ethereum Foundation Blog
- Testnet schedule;  Holešky Oct 1, Sepolia Oct 14, Hoodi Oct 28; mainnet in December (at the earliest)

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners are being proposed for inclusion: deadline for proposal is Fusaka mainnet releases (assume early November)

Presentations:

Glamsterdam Repricings - ACDE \#222 - HackMD
- EIP-8032 Tree-Depth-Based Storage Gas Pricing
- EIP-7791 GAS2ETH

[H-star name for Consensus Layer upgrade after Glamsterdam](https://ethereum-magicians.org/t/h-star-name-for-consensus-layer-upgrade-after-glamsterdam/24298)
[Testnet name needed for Sepolia replacement](https://ethereum-magicians.org/t/testnet-name-needed-for-sepolia-replacement/23221)

---

**system** (2025-10-09):

### Meeting Summary:

The team reviewed updates on the Fusaka Shadow Fork and discussed changes to the BPO schedule configuration, including debates about blob parameter consistency across clients. Performance testing and benchmarking efforts were discussed, with ongoing work to investigate slow blocks on the mainnet and evaluate client behavior regarding blob proof conversions at the fork boundary. The conversation ended with detailed discussions about Ethereum repricing efforts, including various EIP proposals related to state growth, storage costs, and contract efficiency, with plans to further discuss implementation details at the next AllCoreDevs meeting.

**Click to expand detailed summary**

The team discussed updates on the Fusaka Shadow Fork, which was launched on Sepolia and reported to be running smoothly with no missed blocks. Barnabas raised concerns about the BPO schedule in the Gnosis.json file, proposing to remove redundant fields for named forks, which led to a debate about the consistency of blob parameter changes across clients. The team agreed to proceed with the proposed changes to the blob schedule configuration, despite Marius’s reservations, as it aligns with the original intention of the EIP. Ansgar, filling in for Tim, ended the conversation by moving on to discuss the Holesky status, but the transcript ended before this topic was addressed.

The team discussed the status of BPO1 deployment and resource constraints with Holesky library performance issues on testnet nodes, particularly around the 9-15 BPO change. They reviewed client behavior regarding blob proof conversions at the fork boundary, with Geth continuing conversion support for one or two releases while other clients like Erigon and Nethermind plan to drop support, though Marius noted they would maintain conversion functionality until further notice to accommodate L2s. The conversation ended with a brief mention of scaling updates and state access benchmarks.

Jochem discussed ongoing work with Camille from Nerdsmind on executing spec tests against state snapshots to perform performance benchmarks. They are investigating slow blocks on the mainnet and trying to reproduce these issues in isolation. Ameziane suggested running tests on the same hardware specs as the mainnet nodes to rule out hardware-related issues. Parithosh noted the importance of using real-world data from contributor nodes rather than optimizing for a specific architecture. The team agreed to follow up on getting data on execution layer clients from the database.

The team provided updates on BlockNexis Access List (BAL) development, with Toni reporting that Besu, Geth, Reth, and Nethermind clients are close to interop, while Stefan shared progress on individual Execution DAI client testing. Raxhvl reported that 26 tests were released with 80% passing rate across Geth, Nethermind, and Reth clients, with 54 more tests ready for BAL, and Katya mentioned work on metrics for block-level access lists. The team discussed upcoming EIP proposals for Glamsterdam, noting that once the Fusaka mainnet date is set, there will be a one-week proposal window for non-headline EIPs before the deadline at the next Devs call.

Maria presented an overview of ongoing repricing efforts for Ethereum, highlighting the need to harmonize costs across EVM operations and address scaling bottlenecks. She discussed several EIPs, including EIP-7904 which aims to reduce compute prices, EIP-8037 which increases state creation costs, and EIP-8038 which adjusts state access costs. Maria emphasized the importance of ensuring consistency between these EIPs and conducting thorough analysis to avoid introducing mispricings or breaking existing contracts. The next steps involve finalizing EIPs, updating parameters, implementing price changes across clients, and investigating backward compatibility issues.

Maria suggested Telegram as the best platform for reaching out to her for feedback on topics, and she mentioned that analysis on backward compatibility issues, particularly concerning state growth and state access, is still ongoing. Guillaume raised concerns about the redundancy between EIP-2926 and EIP-8037, which both address state growth, and he sought clarification on whether the version presented was the final one. Maria confirmed that the version shared was the most updated one, explaining that while EIP-8037 focuses on harmonizing state growth for all operations, it can work alongside EIP-2926, which also addresses state growth but in a broader context. Guillaume planned to follow up with Carlos to resolve discrepancies in the reviewed documents. Ansgar noted that the pricing assumptions in EIP-8037 were conservative and suggested adjustments before inclusion.

The meeting focused on discussing the repricing of EIPs and the technical details of EIP-8032, which aims to limit state growth by penalizing contracts that exceed a specified storage depth. Guillaume presented the EIP’s formula for calculating gas costs based on storage depth and proposed a variant that also considers the total state size. The group discussed potential concerns about the EIP’s vulnerability to attacks and its impact on contract efficiency, with some participants suggesting that splitting contracts into smaller units could lead to less efficient storage access. The team agreed to further discuss the EIP’s implementation and activation process at the next AllCoreDevs meeting in two weeks.

The meeting focused on discussions about EIPs and their implications for Ethereum. Guillaume explained the concept of splitting contract data across multiple contracts to manage state growth efficiently. Charles presented EIPs related to increasing contract size limits and a new gas-to-ETH opcode for on-chain payments. The group discussed potential issues and concerns with the gas-to-ETH opcode, including its interaction with transaction limits and gas estimation. The conversation ended with a brief discussion about PFI’d EIPs for Glamsterdam and the collection of primary point of contact information.

### Next Steps:

- Client teams to continue working on Fusaka implementation and testing.
- Parithosh to continue monitoring the Sepolia Shadow Fork for Fusaka.
- Client teams to align on the approach for handling blob submission API conversion between old proof format and new one.
- Jochem and Camille to continue research on state access benchmarks and investigate slow blocks.
- Maria to continue work on repricing EIPs and coordinate with client teams on parameter updates.
- Guillaume to continue implementation of EIP-8032 in Geth and determine appropriate constant values.
- Client teams to review and provide feedback on the proposed repricing EIPs before the next ACDE call.
- Charles to create a Telegram group for further discussion on EIP-7791 .
- Protocol support team to collect primary points of contact for PFI’d EIPs going into Glamsterdam.
- All participants to prepare for Glamsterdam EIP discussion in the next ACDE call in two weeks.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 2W5?ICt&)
- Download Chat (Passcode: 2W5?ICt&)

---

**system** (2025-10-09):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=OxvLP6cstSE

---

**poojaranjan** (2025-10-09):

Summary Tweet [thread](https://x.com/poojaranjan19/status/1976286529728225628).

