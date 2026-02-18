---
source: magicians
topic_id: 25573
title: All Core Devs - Consensus (ACDC) #166, October 2, 2025
author: system
date: "2025-09-23"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-166-october-2-2025/25573
views: 337
likes: 2
posts_count: 5
---

# All Core Devs - Consensus (ACDC) #166, October 2, 2025

### Agenda

- Fusaka

any devnet updates?
- holesky fork activation
- holesky BPO1 coming up next week!
- Add Fusaka pm docs by ralexstokes · Pull Request #1749 · ethereum/pm · GitHub

Glamsterdam

- check-in on devnet progress
- trustless payments in epbs
- non-headliner EIP proposal: 1 week after we set fusaka mainnet date

Other

- Update EIP-7723: Include primary point of contact in proposal by wolovim · Pull Request #10391 · ethereum/EIPs · GitHub
- All Core Devs - Consensus (ACDC) #166, October 2, 2025 · Issue #1740 · ethereum/pm · GitHub
- H-star name

**Meeting Time:** Thursday, October 02, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1740)

## Replies

**abcoathup** (2025-10-02):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #166, October 2, 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-166-october-2-2025/25573/5) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #166 Summary
> Fusaka
>
> Devnet 3 had non-finality for ~2 days, then healed and resumed finalizing
> Holesky fork activation went well overall despite some turbulence
>
> Participation dropped initially due to missed client updates
> Unexplained participation drop below 66% later in day, then recovered
> Theories include late blocks, CPU spikes, spamming of blobs
> Most validators run ~10,000 keys per beacon node on Holesky which could factor in
>
>
> First Holesky BPO update scheduled at 2025-10-07 01:20:0…

#### Action Items

*[Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1423432284723482686)]*

- Continue monitoring Holesky deployments to assess progress of Fusaka fork,
- Holesky Fusaka BPO 1 is at 2025-10-07 01:20:00 UTC in just a few days!,
- See ⁠epbs channel (on Eth R&D Discord) if you want to follow the conversation on trustless payments

### Recordings/Stream

- All Core Devs Consensus #166 - Forkcast
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- ACDC #166: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDC Call #166 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]
- Fusaka $2,000,000 Audit Contest! | Ethereum Foundation Blog
- Testnet schedule;  Holešky Oct 1, Sepolia Oct 14, Hoodi Oct 28; mainnet in December (at the earliest)
- Add Fusaka pm docs by ralexstokes · Pull Request #1749 · ethereum/pm · GitHub

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners are being proposed for inclusion: deadline for proposal is Fusaka mainnet releases (assume early November), proposed EIPs need a primary point of contact (EIP champion)
- Call for Discussion on Trustless Payments - Google Präsentationen

[EIP-7870: Hardware and Bandwidth Recommendations](https://eips.ethereum.org/EIPS/eip-7870)
[H-star name for Consensus Layer upgrade after Glamsterdam](https://ethereum-magicians.org/t/h-star-name-for-consensus-layer-upgrade-after-glamsterdam/24298)
[Testnet name needed for Sepolia replacement](https://ethereum-magicians.org/t/testnet-name-needed-for-sepolia-replacement/23221)

---

**system** (2025-10-02):

### Meeting Summary:

The team addressed technical challenges with meeting coordination and discussed updates on testnets including Fusaka and Holesky, with some network issues and participation drops noted during the Holesky fork activation. The group had an extensive discussion about ePBS development, focusing on trustless payments and payload separation, with different opinions expressed about whether to separate these features into distinct proposals. The conversation ended with discussions about process improvements including a champion system for communication, hardware requirements, and naming conventions for H-star.

**Click to expand detailed summary**

The team experienced a mix-up with Zoom meeting links, with some participants joining the wrong room. Nixo offered to move to the other meeting and direct attendees to the correct room. Despite the confusion, Stokes decided to proceed with the meeting once enough participants had joined the correct room. Josh confirmed he was helping with the stream, and Stokes began to review the agenda for ACDC meeting number 166.

The team discussed updates on the Fusaka and Holesky testnets. Parithosh reported that nonfinality was tested on the Fusaka Devnet 3, which was successfully healed after two days. The Holesky fork activation was generally successful, though there were some participation drops and unexplained network behavior that was attributed to missing updates. The team scheduled a meeting to discuss the upcoming VPO on Monday, and Ameziane noted a significant drop in network activity on Holesky validators after the fork, which the team agreed to investigate further. Stokes also mentioned a PR for a PeerDAS readiness document that includes a set of metrics and a process for readiness documentation.

The team discussed the status of ePBS development, with Potuz reporting no changes to the specs but noting ongoing discussions about payment systems and their implementation. The group agreed to be more careful about merging production code rather than using hacky branches, following issues with PeerDAS, and decided to wait for a more stable version of the Fusaka branch before proceeding with ePBS. Lin presented a quick overview of trustless payments in ePBS, though the details of this presentation were not captured in the transcript.

The discussion focused on the separation of trusted business payments in ePBS, which introduces two key changes: payload separation and process payments. Lin proposed either keeping trusted payments within the current EIP or creating a separate EIP to discuss these features independently, as they have different stakeholders and levels of complexity. The conversation highlighted the need for further discussion on the impact of trustless payments on the ecosystem, including potential challenges for builders and staking protocols.

The team discussed whether to include trustless payments in the ePBS proposal, with Lin expressing concerns about potential bypassing of in-protocol justice payments and advocating for separation due to controversy in the ecosystem. Ansgar supported splitting the proposal into two parts, citing historical context where ePBS morphed from focusing on trustless payments to scalability, and suggested making the decision separately from the headliner EIP. The group agreed that a decision should not be made immediately, as many people are likely strongly opposed to separating the headliner EIP into two parts.

The meeting focused on the discussion of separating payload blocks operation and proposer-builder separation into two distinct features, with Greg from Lido agreeing that this would be a leaner approach. Potuz emphasized that trustless payments are easier to implement with the current ePBS specification, and the group discussed the potential removal of MEV-boost support. Ansgar suggested that the conversation about unconditional payments should happen offline, and Lin raised questions about bypassibility with trustless payments. The group agreed that further research and discussion are needed before making any decisions.

The team discussed the Glamorous process of Glamsterdam, focusing on design decisions, and the need for a written document outlining trade-offs. They agreed to keep the conversation moving, with next steps including an upcoming ePBS breakout and a decision on the headliner split in two weeks. The team also refined the process for non-headliner EIPs, setting a deadline for proposals after the mainnet date is set. Additionally, they addressed a proposal for a champion system to improve communication, simplified the language, and agreed to move forward with it. The conversation ended with discussions on hardware requirements and naming conventions for H-star, with a suggestion to use the popular option “Etios.”

### Next Steps:

- Core developers to continue monitoring Holesky after the fork activation, particularly the participation rate fluctuations.
- Parithosh to generate and share bandwidth analysis report clustered per client by tomorrow.
- Stokes to continue working on the PR for Fusaka readiness documentation and process.
- Core developers to prepare for the first VPO  scheduled in a few days.
- Core developers to create a written document outlining the trade-offs between payload separation and trustless payments in ePBS to drive further discussion.
- Interested parties to join the ePBS breakout call next Friday to discuss the potential separation of payload separation and trustless payments.
- Wolovim’s PR about specifying a primary point of contact for EIPs to be merged within 24 hours.
- Core developers to move EIP 7870  from interview to live status.
- Community members to provide input on H-star naming in the ETH Magicians thread, with “Etios” currently being the most popular option.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: .ebkh@6?)
- Download Chat (Passcode: .ebkh@6?)

---

**system** (2025-10-02):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=d-uG-anQWA0

---

**ralexstokes** (2025-10-02):

**ACDC #166 Summary**

Fusaka

- Devnet 3 had non-finality for ~2 days, then healed and resumed finalizing
- Holesky fork activation went well overall despite some turbulence

Participation dropped initially due to missed client updates
- Unexplained participation drop below 66% later in day, then recovered
- Theories include late blocks, CPU spikes, spamming of blobs
- Most validators run ~10,000 keys per beacon node on Holesky which could factor in

First Holesky BPO update scheduled at 2025-10-07 01:20:00 UTC

Glamsterdam

- Shifting focus back to Glamsterdam development now that Fusaka is moving towards mainnet
- ePBS updates:

No spec changes recently, adding tests
- Only Teku has passing tests on main branch
- Prysm has passing tests on separate branch
- Other clients waiting for stable Fusaka before merging ePBS work

Process reminder: non-headliner EIP deadline will be one week after Fusaka mainnet date is set

ePBS Trustless Payments

- linoscope presented case for separating payload separation from trustless payments:

Two different stakeholder groups: core devs (scaling experts) vs ecosystem (builders/validators)
- Different complexity profiles and ecosystem impact
- Risk of EOF-like outcome if bundled together
- Bypassability concerns - rational actors might use off-protocol payments anyway

Supporting arguments from Greg (Lido) and others for separation
Decision deferred - needs written trade-off analysis before next discussion
ePBS breakout call scheduled for next Friday; check in there if you want to follow along

Administrative Items

- EIP process updates:

Champion/primary point of contact requirement being simplified and merged

Update EIP-7723: Include primary point of contact in proposal by wolovim · Pull Request #10391 · ethereum/EIPs · GitHub

EIP-7870 (minimum hardware requirements) moving from review to live status

H-fork naming: community poll favors “Helvetios” - decision by Fusaka mainnet launch

