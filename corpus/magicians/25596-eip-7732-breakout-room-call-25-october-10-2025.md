---
source: magicians
topic_id: 25596
title: EIP-7732 Breakout Room Call #25, October 10, 2025
author: system
date: "2025-09-26"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-25-october-10-2025/25596
views: 45
likes: 0
posts_count: 3
---

# EIP-7732 Breakout Room Call #25, October 10, 2025

### Agenda

#### Specifications & testing

##### Open

- eip7732: add tests for process_withdrawals block processing
- eip7732: add fork choice tests (part1)
- Small fixes to Gloas spec
- TODO: Remove merkle proof tests in Gloas (reference)
- TODO: Add pending payment withdrawal epoch asserts (reference)

##### Merged

- Fix output for gloas test

#### Implementation updates from client teams

- Prysm
- Lighthouse
- Teku
- Nimbus
- Lodestar
- Grandine

#### Trustless payments

Quick writeup: [Builder payment configuration for eip7732 - HackMD](https://hackmd.io/@tchain/payment-config)

- Should we have trustless payments in the current EIP in the first place? Is it possible to separate so we don’t have to decide the following points right now?
- If we are to keep trustless payments, how would that look in-protocol? E.g., should bids go through the withdrawal queue directly? What are the tradeoffs?
- How would off-protocol bids be supported? How and what should we standardize?

Some discord threads from after the discussion on ACD:

- Discord
- Discord

#### Attestation container refactoring

- EIP-7732 Breakout Room Call #25, October 10, 2025 · Issue #1744 · ethereum/pm · GitHub

Reusing the same container adds complexity & confusion.

**Meeting Time:** Friday, October 10, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1744)

## Replies

**system** (2025-10-10):

### Meeting Summary:

The team reviewed implementation progress across various projects including Prism, Teku, Nimbus, and Lighthouse, with most members reporting partial completion of features while expressing concerns about meeting the end of October deadline. The group discussed technical changes to DevNet including adding slot numbers to sidecars and debated the inclusion of process payments in the current EIP, with significant discussion around trustless payments and state builders. The conversation ended with discussions about attestation data indexing concerns and plans to address staked builders and validator infrastructure in next week’s ACDC call.

**Click to expand detailed summary**

The meeting began with Justin preparing to share his screen and Pooja noting they were pre-streaming, with instructions to move to the stream after 14. Justin greeted several participants, including Lance, POTUS, Terrence, and NFLAIG, and confirmed he could hear everyone. The meeting was set to start in two minutes.

The team discussed ongoing PRs and implementation progress for DevNet Zero. Terence reported that Prism has implemented most of the beacon DAO MD features and is waiting for a stable Fusaka release before merging PRs. He expressed concern about the end of October launch timeline being rushed. Stefan confirmed that Teku has passed all relevant SPAT tests. The team agreed to follow up with Lighthouse for their implementation status.

The team discussed implementation progress across different projects, with Stefan reporting minimal work done beyond passing reference tests, while expressing uncertainty about the end of October deadline due to pending decisions on CIP splitting. Nico shared that Nimbus has work in progress on state transition code, passing static tests but not reference tests yet. Shane provided an update on Lighthouse, noting progress on PTP and validator client work, but highlighted that payload processing separation would require significant refactoring and was unlikely to meet the October deadline.

The team discussed adding a slot number to the sidecars for DevNet, with Saulius advocating for immediate implementation to avoid future refactoring. They decided to create a PR to add the slot to the Datacom sidecar, targeting DevNet1 rather than DevNet0, while keeping the current DevNet0 specs unchanged. The group agreed this change would not affect DevNet0 since they are targeting no blobs for that release anyway.

The team discussed the inclusion of process payments in the current EIP, with Lin highlighting the need for careful coordination and design review. Potuz raised concerns about removing trustless payments, emphasizing the complexity of redesigning the system without state builders and the need for a detailed specification. Ansgar suggested considering a base version of ePBS without unconditional payments and state builders, arguing that this package should go through the general EIP process to avoid adding extra implementation complexity to Glamsterdamdam.

The group discussed concerns about changes to the SFI EIP, with Potuz emphasizing that the original discussion on trustless payments and state builders was already completed two years ago. Lin inquired about the relationship between state builders and pipelining, while Ansgar suggested separating the discussion into two concerns: the specification viability and the governance process. Ansgar noted that while he is agnostic about the spec, he believes the governance process should be reconsidered, as the headliner’s primary motivation was scaling, and additional features like staking should be addressed through non-headliner EIPs.

The team discussed the scaling EIP and trustless payments implementation, with Potuz explaining that trustless payments were already covered in the existing specification and represented only minor additions. Terence emphasized that the current design supports both trusted and trustless payments, and highlighted the need for more feedback from builders regarding the stake-pushing requirement. Lorenzo raised concerns about the potential impact of stake builders on builder competition and relay competition, noting that the off-protocol market currently responsible for 95% of Ethereum blocks might not be fully considered in protocol changes.

The discussion focused on the implementation of off-protocol payments for builders in Ethereum Proof of Stake (ePBS). Lorenzo and Potuz clarified that the proposed changes would not require significant modifications for node operators or proposers, as builders could continue using existing payment methods. Lin emphasized the importance of easy off-protocol payment support to minimize disruption and reduce arguments against the change. Potuz stressed that ePBS should offer builders an option, not a requirement, for off-protocol payments, while maintaining trustless payment routes for safety and fallback mechanisms.

The team discussed the removal of trustless payment routes, with Potuz opposing the removal and emphasizing the importance of a fallback P2P stack. Lin and others raised concerns about operational challenges for node operators and the need for software upgrades to handle trustless payments. The group agreed that while trustless payments should remain, there should be strong support for on-protocol payments. Greg from Lido confirmed that the withdrawal part of the specification had been settled, avoiding the need for on-chain infrastructure updates.

The team discussed the implications of changing the payment system, with potuz explaining that Lido requested a simpler system but might still use trusted payments. They debated the necessity of staked builders for pipelining, with potuz and others questioning the safety of allowing signatures from non-staked entities. The group also considered the possibility of reducing builder staking requirements, though potuz noted this would require changes to the protocol. The discussion concluded with potuz stating the need to go back to the drawing board to specify these changes further.

The team discussed concerns about changes to attestation data indexing, where Mehdi raised an issue about the index field no longer being hardcoded to zero, which could create compatibility problems between Electra and global attestation systems. Justin suggested discussing this further on Discord and requested Mehdi to create a PR as a proposal for review. The team agreed to save decisions about staked builders and validator infrastructure for next week’s ACDC call led by Stokes.

### Next Steps:

- Mehdi to create a PR proposing a solution for the attestation container issue in GLOS where the index field is now used to signal payload status.
- Client teams to continue implementation work for DevNet Zero.
- Saulius/Grandine to make a PR to add slot to Datacom Sidecar for future DevNet implementation.
- Client teams to discuss and standardize out-of-the-box support for off-protocol payments.
- Justin to post a recap of the meeting.
- All participants to continue the trustless payments discussion on Discord before the next ACDC call.
- Potus and NC to discuss open PRs that need to be merged soon.
- Someone to pick up the to-do items: removing tests no longer relevant in GOSS and adding missing asserts pointed out by Terrence.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: Pb3Rj%Y5)
- Download Chat (Passcode: Pb3Rj%Y5)

---

**system** (2025-10-10):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=9JfEYNi6ikI

