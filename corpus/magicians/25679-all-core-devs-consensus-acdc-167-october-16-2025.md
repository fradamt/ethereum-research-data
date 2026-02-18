---
source: magicians
topic_id: 25679
title: All Core Devs - Consensus (ACDC) #167, October 16, 2025
author: system
date: "2025-10-06"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-167-october-16-2025/25679
views: 237
likes: 2
posts_count: 5
---

# All Core Devs - Consensus (ACDC) #167, October 16, 2025

### Agenda

- Fusaka

any callouts on devnet-3?
- holesky BPO2
- sepolia fork
- Fusaka contest: All Core Devs - Consensus (ACDC) #167, October 16, 2025 · Issue #1754 · ethereum/pm · GitHub
- blob APIs

proof change with EL
- getBlob endpoint with CL
- related: All Core Devs - Consensus (ACDC) #167, October 16, 2025 · Issue #1754 · ethereum/pm · GitHub

https://github.com/ethereum/consensus-specs/pull/4657
fusaka mainnet: [All Core Devs - Consensus (ACDC) #167, October 16, 2025 · Issue #1754 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1754#issuecomment-3410763056)
sepolia BPO1 next week!

Glamsterdam

- trustless payments in ePBS
- EIP-7688 PFI’d for Glamsterdam, although will defer inclusion discussion until Fusaka mainnet date is set

All Core Devs - Consensus (ACDC) #167, October 16, 2025 · Issue #1754 · ethereum/pm · GitHub

**Meeting Time:** Thursday, October 16, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1754)

## Replies

**abcoathup** (2025-10-13):

### Summary

*[[@ralexstokes](/u/ralexstokes) takeaways; Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1428470342778617947)]*

- Fusaka testnets going well!

Sepolia BPO1 coming next at 2025-10-21 03:26:24 UTC,

Fusaka mainnet temp check

- We did NOT confirm dates today,
- Attendees were supportive of the following

Mainnet releases: 3 Nov 2025,
- (tentative) Mainnet date: 3 Dec 2025,

Will confirm on next ACDE,

Trustless payments in ePBS

- Some discussion around separating the payments design from EIP-7732,
- Check the call for full color,
- Agreed to leave as is, with no change to the spec

### Recordings/Stream

- All Core Devs Consensus #167 - Forkcast
- Live stream on X & audio on Spotify: [x.com/ECHInstitute]

### Writeups

- ACDC #167: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDC Call #167 by @yashkamalchaturvedi [etherworld.co]
- Quick summary X thread by @poojaranjan

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]
- Testnet schedule;  Holešky Oct 1,  Sepolia Oct 14, Hoodi Oct 28; mainnet proposed for December 3 (not set yet - upgrade processes)
- Fusaka $2,000,000 Audit Contest! | Ethereum Foundation Blog ended, nothing to cause postponing upgrade
- Fusaka Update - Information for Blob users | Ethereum Foundation Blog
- Aztec: Blob retrieval guarantee post Fusaka

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners are being proposed for inclusion: deadline for proposal is Fusaka mainnet releases (assume early November)
- Glamsterdam Upgrade - Forkcast shows EIP champions (primary point of contact)

[H-star name for Consensus Layer upgrade after Glamsterdam](https://ethereum-magicians.org/t/h-star-name-for-consensus-layer-upgrade-after-glamsterdam/24298)
[Testnet name needed for Sepolia replacement](https://ethereum-magicians.org/t/testnet-name-needed-for-sepolia-replacement/23221)

---

**poojaranjan** (2025-10-16):

Summary Tweet thread - https://x.com/poojaranjan19/status/1978823244493865116

---

**system** (2025-10-16):

### Meeting Summary:

The meeting covered updates on various testnets and projects, including progress reports on DevNet 3 and discussions about recent changes to Blob APIs that caused some confusion among roll-ups. The team explored solutions for blob retrieval under PureDOS and storage optimization strategies, while also discussing the timeline for the mainnet release and concerns about trustless payments. The group concluded by addressing the governance and implementation of trustless payments and block payload separation features, ultimately deciding to keep the current design despite added complexity.

**Click to expand detailed summary**

The meeting focused on updates and discussions about various testnets and projects. Barnabas reported that DevNet 3 is progressing well, with a few bugs related to database usage being resolved. Enrico mentioned a bug discovered in the subscription process for subnets in Teku, which was working reliably despite the issue. Fredrik provided an overview of the Fisiana contest, which concluded on the 13th, and confirmed that there were no findings that would delay the hard fork. The team expressed satisfaction with the progress of the testnets, particularly noting the absence of issues seen in previous tests like Pectra.

The meeting discussed recent changes to Blob APIs, particularly the transition from 4544-style blobs to dust-style blobs, which caused some confusion among roll-ups. Stokes explained that while the EIP claimed backward compatibility, there were some miscommunications about the changes, and some roll-ups only learned about them this week. The group agreed that better communication and testing on staging environments could help prevent similar last-minute changes in the future. Nixo and others suggested using shadowfork networks for testing instead of redeploying on devnets, and Marius proposed adding information about RPC filters to future EIPs to avoid miscommunication.

The meeting discussed concerns about blob retrieval under PureDOS, particularly for decentralized sequencers, with Koen highlighting bandwidth constraints requiring everyone to run super nodes. The group explored solutions including light super nodes and custom tooling, with Enrico suggesting a middle ground where nodes could custody a minimal subset of columns to reconstruct blobs. The discussion also covered storage optimization strategies, with Manu proposing storing 64 cells but 128 proofs to save space, and the team noted that most L2s use builder APIs to publish blobs rather than relying on the public mempool.

The team discussed the timeline for the mainnet release, with a proposal to aim for November 3rd for client releases and December 3rd for the mainnet launch. While there was general support for this timeline, Fredrik raised concerns about following the established process, which states that the mainnet upgrade date should not be set until all testnets have been upgraded. The team agreed to further discuss and potentially formalize the dates at the next ACD meeting, with Stokes planning to reach out to client teams asynchronously for any additional concerns. They also noted the upcoming Sepolia BPO for Fusaka next week.

The team discussed concerns about trustless payments, with Lynn expressing that the feature should have been separated from EIPs but now supports off-protocol payments as a standard, which was welcomed by core developers. Enrico emphasized the importance of keeping the specification separate after deciding to ship EPPS without trustless payments, to avoid wasted effort. The group agreed to accept the current state and continue discussions, with a focus on properly supporting off-protocol payments.

The team discussed the governance and implementation of trustless payments and block payload separation (EPBS) features. Enrico suggested treating them as separate for governance but keeping them together in EIP/spec unless a decision is made to remove staked builders from Glamsterdam. ethDreamer expressed that while separating these features would be complex, the current design is workable for version 1, with potential improvements for version 2. Dmitry raised concerns about the added complexity for staking protocols like Lido, noting that monitoring both off-chain and on-chain markets would require significant additional effort.

The team discussed the potential separation of trustless payments from the current EIP, with Francesco clarifying that such a split was technically feasible but not necessarily beneficial at this stage. Sophia and others expressed concerns about delays in shipping the hard fork if the EIP were split, while Lin emphasized that the free option problem should be discussed independently from payments. The group agreed to keep the current design, acknowledging the added complexity but deciding to move forward with the implementation rather than spending more time on potential changes.

The team discussed the status of trustless payments in the EIP, ultimately deciding to leave it as is. They also addressed concerns about the scope of the Glamsterdam fork, particularly regarding the inclusion of FOCIL and other EIPs. The group agreed to focus on getting Fusaka out the door before discussing the rest of the Glamsterdam scope in detail. They noted that there are 29 EIPs in the MetaEIP list that will need to be considered for inclusion in the fork.

### Next Steps:

- All client teams to prepare for Fusaka mainnet releases by November 3rd, targeting December 3rd for mainnet deployment.
- Client teams to prepare for Sepolia BPO1 next week .
- Core developers to continue implementation work on ePBS with trustless payments for Glamsterdam.
- Client teams to work toward having Glamsterdam DevNets sometime this year.
- Prism team to implement the “light super node” feature to help with blob retrieval for L2s.
- stokes to bring the Fusaka mainnet date proposal  to next week’s ACD for formal approval.
- stokes to reach out to each client team async to confirm the feasibility of the Fusaka timeline.
- Core developers to review Jimmy’s RFC regarding changing a condition in the spec from “should” to “may” to reduce bandwidth requirements for non-super nodes.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: f4rzX3B%)
- Download Chat (Passcode: f4rzX3B%)

---

**system** (2025-10-16):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=XBvBEHPqGhM

