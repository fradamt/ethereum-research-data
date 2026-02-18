---
source: magicians
topic_id: 25564
title: EIP-7732 Breakout Room Call #24, September 26, 2025
author: system
date: "2025-09-23"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-24-september-26-2025/25564
views: 51
likes: 0
posts_count: 5
---

# EIP-7732 Breakout Room Call #24, September 26, 2025

### Agenda

#### Specifications & testing

New spec release: [v1.6.0-beta.0](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-beta.0)

##### Open

- eip7732: add tests for process_withdrawals block processing
- eip7732: add fork choice tests (part1)

##### Merged

- Clean up Gloas’s presets
- Add helper functions for slot time deadlines
- eip7732: remove latest_execution_payload_header
- eip7732: clean up get_attestation_participation_flag_indices
- eip7732: add attestation processing tests
- eip7732: add tests for execution payload availability reset
- eip7732: rename execution payload header to execution payload bid

#### Implementation updates from client teams

- Prysm
- Lighthouse
- Teku
- Nimbus
- Lodestar
- Grandine

#### Plans for epbs-devnet-0

- Devnet-0 will be based on v1.6.0-beta.0 specifications
- Try to provide an epbs-devnet-0 branch for ethpandaops by the end of October

#### Does  need a slot field?

![Image](https://github.com/user-attachments/assets/2ff0a41f-a68e-4992-b287-27f93d606354)

See: [the discord message](https://discord.com/channels/595666850260713488/874767108809031740/1420736448893812779)

#### It’s impossible to keep latest_execution_payload_header in

![Image](https://github.com/user-attachments/assets/0ad6eeda-661d-48f5-ae64-98843bde0aef)

See: [the discord message](https://discord.com/channels/595666850260713488/874767108809031740/1420161430497398956)

**Meeting Time:** Friday, September 26, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1735)

## Replies

**system** (2025-09-26):

### Meeting Summary:

The ePBS Breakout Call 24 was led by Justin, who managed the meeting and discussed a new specs release beta.0, while team members provided updates on various implementations including ePBS testing, DevNet Zero progress, and beacon chain changes. The team addressed concerns about KCG commitments and SSZ fork-choice container issues, with plans to investigate further and continue development in the next meeting scheduled for two weeks.

**Click to expand detailed summary**

Justin led the ePBS Breakout Call 24, with Pooja noting she might have to leave early and introducing Akash from the ECH Team to handle streaming duties. Justin confirmed he would manage the call and shared the agenda in the chat. The meeting began with greetings and brief discussions among participants, including Terrence mentioning Dave’s expected late arrival.

Justin announced a new specs release beta.0 with updates for ePBS. Terence discussed open testing PRs for ePBS, mentioning that the only one not yet addressed is process withdraw, which he is hesitant to work on due to its complexity. He expressed a willingness to continue working on it but invited others to take it up if they wish. Terence also highlighted the importance of ForkChoice Pass testing, noting its relevance to edge cases involving anti-slot and PTC status. He requested feedback from experts like Mikael and Roberto on the edge cases he had previously shared.

The team discussed implementation progress for DevNet Zero, with Terence reporting on PR reviews and Stefan noting completion of containers and reference tests. NFLaig shared updates on BPS changes and container work for Lodestar, while Subhasish reported progress on beacon chain changes and state transition functions. The team agreed to provide an ePBS-devnet-0 branch by the end of October, and Stefan clarified that DataComs in Teku currently uses a slot field, which is not an immediate issue for DevNet0.

The team discussed concerns about the implementation of KCG commitments in Fuloop, noting that accessing commitments from the beacon block may not work with ePBS. Potuz raised a notice about keeping the latest execution payload header in the beacon state, explaining that the current solution reuses the position due to circular dependencies. The team also addressed a potential issue with SSZ fork-choice container in static tests, which Justin agreed to investigate. The conversation ended with the team merging to develop and agreeing to meet again in two weeks.

### Next Steps:

- Terence to continue working on the process withdraw PR or find someone to pick it up.
- Terence to continue implementing Prism for DevNet Zero.
- Justin to talk with Stokes about refactoring of process withdrawals timing.
- Potus to provide an ePBS-devnet-0 branch for ETH PandaOps by the end of October.
- Justin to look into converting fork-choice note to a data class instead of an SSZ object.
- Client teams  to continue implementation of ePBS Beta Zero specifications.
- Client teams to address the issue of KCG commitments access in the context of Fusaka and ePBS integration.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 939Dj#f$)
- Download Chat (Passcode: 939Dj#f$)

---

**system** (2025-09-26):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=DSXg_aFK44I

---

**system** (2025-09-27):

### Meeting Summary:

The ePBS Breakout Call 24 was led by Justin, who managed the meeting and discussed a new specs release beta.0, while team members provided updates on various implementations including ePBS testing, DevNet Zero progress, and beacon chain changes. The team addressed concerns about KCG commitments and SSZ fork-choice container issues, with plans to investigate further and continue development in the next meeting scheduled for two weeks.

**Click to expand detailed summary**

Justin led the ePBS Breakout Call 24, with Pooja noting she might have to leave early and introducing Akash from the ECH Team to handle streaming duties. Justin confirmed he would manage the call and shared the agenda in the chat. The meeting began with greetings and brief discussions among participants, including Terrence mentioning Dave’s expected late arrival.

Justin announced a new specs release beta.0 with updates for ePBS. Terence discussed open testing PRs for ePBS, mentioning that the only one not yet addressed is process withdraw, which he is hesitant to work on due to its complexity. He expressed a willingness to continue working on it but invited others to take it up if they wish. Terence also highlighted the importance of ForkChoice Pass testing, noting its relevance to edge cases involving anti-slot and PTC status. He requested feedback from experts like Mikael and Roberto on the edge cases he had previously shared.

The team discussed implementation progress for DevNet Zero, with Terence reporting on PR reviews and Stefan noting completion of containers and reference tests. NFLaig shared updates on BPS changes and container work for Lodestar, while Subhasish reported progress on beacon chain changes and state transition functions. The team agreed to provide an ePBS-devnet-0 branch by the end of October, and Stefan clarified that DataComs in Teku currently uses a slot field, which is not an immediate issue for DevNet0.

The team discussed concerns about the implementation of KCG commitments in Fuloop, noting that accessing commitments from the beacon block may not work with ePBS. Potuz raised a notice about keeping the latest execution payload header in the beacon state, explaining that the current solution reuses the position due to circular dependencies. The team also addressed a potential issue with SSZ fork-choice container in static tests, which Justin agreed to investigate. The conversation ended with the team merging to develop and agreeing to meet again in two weeks.

### Next Steps:

- Terence to continue working on the process withdraw PR or find someone to pick it up.
- Terence to continue implementing Prism for DevNet Zero.
- Justin to talk with Stokes about refactoring of process withdrawals timing.
- Potus to provide an ePBS-devnet-0 branch for ETH PandaOps by the end of October.
- Justin to look into converting fork-choice note to a data class instead of an SSZ object.
- Client teams  to continue implementation of ePBS Beta Zero specifications.
- Client teams to address the issue of KCG commitments access in the context of Fusaka and ePBS integration.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 939Dj#f$)
- Download Chat (Passcode: 939Dj#f$)

---

**system** (2025-09-27):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=DSXg_aFK44I

