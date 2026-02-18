---
source: magicians
topic_id: 25893
title: All Core Devs - Consensus (ACDC) #168, October 30, 2025 🎃
author: system
date: "2025-10-20"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-168-october-30-2025/25893
views: 264
likes: 2
posts_count: 4
---

# All Core Devs - Consensus (ACDC) #168, October 30, 2025 🎃

### Agenda

- Fusaka

sepolia bpo2
- hoodi fusaka
- confirm mainnet dates: Fusaka & BPO timelines - HackMD  (copied below)
- process PR: Clarify mainnet upgrade date requirement by barnabasbusa · Pull Request #1780 · ethereum/pm · GitHub

Glamsterdam

- will start discussing CL non-headliner scoping

7688 (stablecontainer)
- 8045 (exclude slashed validators from proposer shuffling)
- 8061 (increase churn limits)
- Anders’ EIPs

Prevent consolidations as withdrawals

cell-level deltas in PeerDAS
7805 (FOCIL)

H-star

- Name: Heka is leading candidate

#### Fusaka mainnet dates proposal

| Network | Fork Name | Time UTC | Epoch | Start Slot | Unix Timestamp |
| --- | --- | --- | --- | --- | --- |
| Mainnet | Fusaka | 2025-12-03 21:49:11 | 411392 | 13,164,544 | 1764798551 |
| Mainnet | BPO 1 | 2025-12-09 14:21:11 | 412672 | 13,205,504 | 1765290071 |
| Mainnet | BPO 2 | 2026-01-07 01:01:11 | 419072 | 13,410,304 | 1767747671 |

BPO 1 - (10,15) (target, max blob count)

BPO 2 - (14,21)

**Meeting Time:** Thursday, October 30, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1772)

## Replies

**abcoathup** (2025-10-20):

### Summary

*[[@ralexstokes](/u/ralexstokes) summary (Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1433901674371485716)]*

- Agreed to Fusaka mainnet dates

Refer to the agenda for the dates,
- EF blog post coming Monday with client releases,

Discussed CL non-headliner Glamsterdam EIPs

- check call for discussion,
- Written client opinions due 13 Nov in time for next ACDC,

Will confirm Glamsterdam CFI set (at least on CL side) on next ACDC,
H-star name has been selected: Heka ![:dizzy:](https://ethereum-magicians.org/images/emoji/twitter/dizzy.png?v=15)

### Recordings/Stream

- All Core Devs Consensus #168 - Forkcast
- Live stream on X & audio on Spotify: [x.com/ECHInstitute]

### Writeups

- ACDC #168: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDC #168 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade (December 3):

Upgrade dates: mainnet December 3, BPO1 December 9, BPO2 January 7 2026
- Mainnet releases: November 3 (Prysm will be later)
- Testnet upgrades;  Holešky Oct 1,  Sepolia Oct 14,   Hoodi Oct 28;
- Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam) (2026):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners proposed for inclusion: Consensus layer team scoping writeups due November 13; EIP-7805 FOCIL adds ~2 months to Glamsterdam timeline
- Mascot needed for Glamsterdam upgrade

[PeerDAS cell-level deltas](https://github.com/raulk/research/blob/main/eth/talks/251030-acdc-peerdas-cell-deltas.md): unlocks next tranche of BPOs, increase blobs from 21 max to 72 max at least
**Heka** chosen as [H-Star name](https://ethereum-magicians.org/t/h-star-name-for-consensus-layer-upgrade-after-glamsterdam/24298)

---

**system** (2025-10-30):

### Meeting Summary:

The team reviewed updates on various testnets and discussed bug fixes, with particular attention to the Prism client issue that will require a delayed release. They examined several Ethereum Improvement Proposals (EIPs) related to validator consolidation, staking incentives, and network optimization improvements, with ongoing discussions about their implementation and potential impacts. The conversation ended with discussions about the Glamsterdam upgrade, including the inclusion of Fossil and the naming of the H-star upgrade, while emphasizing the importance of balancing scaling efforts with other EIPs.

**Click to expand detailed summary**

The team reviewed updates on the Sepolia and Hoodi forks, noting that Sepolia BP02 went smoothly with no issues, while Hoodi saw a small drop in participation due to operator issues and a Reth bug that has since been patched. They discussed the specific combination of conditions that triggered the bug and agreed to explore adding a static test for it. The team confirmed the mainnet release date for Fusaka as November 3rd, with the Fork scheduled for December 3rd and BPO1 on December 9th, with BPO2 set for January 7th of the following year.

The team discussed a bug in the Prism client that was not present in testnets, causing non-prism peers to be kicked out after a few hours. They decided to proceed with the mainnet dates but delay the Prism release, with Manu noting that a fix might not be ready by Monday. The team agreed to keep an eye on the issue and adjust if necessary. They also discussed setting up a point person per team for incident responses and reviewed a process document for the Fusaka hard fork.

The team discussed the timing and process for reviewing EIPs related to the CL layer, with a focus on having client teams submit written proposals by November 13th for review at the next ACDC meeting. They reviewed EIP-7688, which introduces stable containers, and EIP-8045, which modifies proposer shuffling to exclude slash validators, with Barnabas noting that the proposer lookahead feature would make this relatively straightforward to implement. The team agreed to continue scoping discussions over the next two weeks, with client teams preparing proposals for the CL side of the fork.

The meeting discussed two Ethereum Improvement Proposals (EIPs): 8045 and 8061. EIP 8045 is a simple one-line change to prevent issues with ExLC/validators, while EIP 8061 proposes increasing churn limits for entries, exits, and consolidations, which would improve staking UX but reduce the time for weak subjectivity to around 6 days. Ansgar raised concerns about the implications of EIP 8061 on issuance changes, suggesting it could lead to faster, unanticipated changes in staking dynamics. The group agreed to further consider the proposal’s implications and potential modifications to address these concerns.

The team discussed two EIPs related to validator consolidation and staking incentives. Anders presented EIP-8062, which adds a small fee to SWAP withdrawals to incentivize moving from skimming to compounding validators, and EIP-8068, which adjusts the effective balance calculation to make compounding validators more favorable. The group debated whether these changes would actually encourage consolidation, with some members suggesting that larger staking providers might not be held back by these incentives. Mikhail raised concerns about the low adoption of compounding validators and questioned whether the proposed changes would have a meaningful impact on adoption rates.

The team discussed two main topics: a proposed fix for validator consolidation issues (EIP-8062) and network optimization improvements. Mikhail explained that the consolidation fix is a “nice-to-have” UX improvement rather than a security issue, while Raúl presented Peer DAS CL-level deltas, a network optimization that would allow increasing the maximum number of blobs from 21 to 72, with implementation expected by February. The team agreed to align this optimization work with the Glamsterdam release, with Raúl proposing a timeline that would see full interoperability by November and production-grade implementations by December, allowing for formal testnet journeys leading to mainnet.

The meeting focused on scaling efforts for Ethereum, particularly the Glamsterdam initiative. Participants discussed the importance of scaling and the need to balance it with other EIPs. There was a question about whether client teams felt comfortable with three more BPOs while finishing Glamsterdam, to which Stokes responded that it could be manageable if non-consensus changes on the networking layer are considered. The group also discussed the partial message extension and its potential merge into libp2p. The conversation ended with a brief mention of EIP7805, which was CFI’d but could be reconsidered for the fork scope.

The meeting focused on the inclusion of Fossil in the Glamsterdam upgrade, with participants discussing the trade-offs between shipping cadence and potential risks to censorship resistance. Soispoke outlined the considerations around Fossil’s importance and timing, while Ansgar highlighted the challenge of balancing timeline impacts with the need for Fossil. The group agreed to move forward with HECA as the name for the H-star upgrade, and participants were encouraged to refine their forkcast data for better presentation.

### Next Steps:

- Prism team : Release mainnet-ready version as soon as possible
- stokes: Reach out to all teams to get a point person per team for incident response and add to Fusaka process doc PR
- Reth team: Continue work on patched testlist for the bug found on Hoodi
- Testing team : Create explicit static test for the Reth bug scenario
- All client teams: Submit written proposals for Glamsterdam CL scoping by next ACDC
- EL implementers: Prepare to rehash and merge GetBlobsB3 Engine API PRs by November for PeerDAS cell-level deltas
- CL implementers : Review and comment on PeerDAS specs, start planning implementation by November
- CL implementers : Begin implementation of PeerDAS by December
- Lighthouse team: Continue PeerDAS implementation and conduct interop tests with Prism prototype
- Raul: Share PeerDAS presentation materials publicly after the call
- stokes: Work with Raul to get PeerDAS information posted somewhere public for reference
- stokes: Consider better language for the process doc regarding testnet requirements before setting mainnet dates
- All teams: Review EIP-7688  and specs PR 4630
- All teams: Review EIP-8045
- All teams: Review EIP-8061  considering weak subjectivity implications
- All teams: Review EIP-7805  for potential Glamsterdam inclusion
- Community: Submit proposals for Fusaka mascot if desired

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: ai+0ZY8$)
- Download Chat (Passcode: ai+0ZY8$)

---

**system** (2025-10-30):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=JelYN_iyU84

