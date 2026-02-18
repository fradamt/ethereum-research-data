---
source: magicians
topic_id: 27356
title: All Core Devs - Execution (ACDE) #227, Jan 5, 2026 [OFF-CYCLE]
author: system
date: "2025-12-29"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-227-jan-5-2026-off-cycle/27356
views: 98
likes: 1
posts_count: 3
---

# All Core Devs - Execution (ACDE) #227, Jan 5, 2026 [OFF-CYCLE]

### Agenda

- Housekeeping

ACD process updates by @poojaranjan

Glamsterdam

- scoping decisions

updated CFI / DFI candidate EIPs
- comment from last ACDE regarding EIP-8051 and related EIPs by @rdubois-crypto

Other

- EIP-8077 and EIP-8094 by @cskiraly

**Meeting Time:** Monday, January 05, 2026 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1854)

## Replies

**system** (2026-01-05):

### Meeting Summary:

The meeting focused on scoping decisions for the Glamsterdam project, including discussions about contract size limits and various Ethereum Improvement Proposals (EIPs). The team reviewed and made decisions on several EIPs, including considerations for ACDG rebranding, EIP template upgrades, and gas cost modifications, while deferring some items to future meetings. The group concluded by discussing the status of various EIPs for the Glamsterdam hard fork, with some proposals being delayed or withdrawn due to implementation concerns and lack of client support.

**Click to expand detailed summary**

The meeting began with Akash confirming his ability to screen share and Ansgar deciding to start the meeting live. Ansgar announced that this was an out-of-turn ACDE meeting, clarifying the regular schedule starting from the next day. The primary focus was on continuing the scoping decisions for the Glamsterdam project, as it was nearing completion. Pooja provided updates on various topics, but the details were not specified in the transcript.

The meeting focused on several key proposals and updates. Pooja introduced the concept of ACDG (Ethereum Account Data Governance), a rebranding of the existing EIPIP meeting to improve process clarity and decision-making. She also proposed adding an optional upgrade field to the EIP template to help users better understand protocol evolution. The team discussed contract size limits, with options ranging from doing nothing to implementing a simple size bump or the more complex EIP 7907. Given concerns about scope and implementation complexity, the group decided to postpone the final decision on EIP 7907 to next week’s ACDE meeting, while encouraging interested parties to work on prototypes in the meantime. The conversation ended with a brief update on EIP 37 regarding estate creation gas cost increases, which was also deferred to the next meeting.

The team discussed several EIPs, focusing on decisions about contract size limits and testing. They agreed to bump EIP-7907 to 32 and not implement gas accounting, with a final decision to be made next week. For EIP-7903, Marius explained that removing the init code size limit is not possible due to JUMP text issues. The team decided to DFI EIP-7997 as there was limited client feedback. Carlos confirmed he was present and did not want to withdraw EIP-8058.

The team discussed EIP-7997, with Łukasz and Ben Adams from Nethermind supporting its inclusion as a useful feature for L2s despite it not being a priority. Andrew expressed skepticism about the EIP due to potential implementation complexities with precompiles. The group also revisited EIP-7923, with an unknown speaker advocating for its inclusion and against EIP-8024. Barnabas suggested CFIing the EIP to assess its implementation difficulty.

The team discussed two EIPs for the Glamsterdam hard fork. For EIP-8097, they decided to include it in Glamsterdam as a simple community request, with Barnabe agreeing to implement it as a CFI. For EIP-8058, which proposes a gas cost discount for contract code deduplication, Han explained the UX benefits but noted lack of developer feedback. Guillaume, speaking for the Stateless team, decided to withdraw this EIP for now, suggesting it could be revisited in H-star with potential improvements. Regarding EIP-7668 to remove bloom filters, Felix raised concerns about potential encoding variances and implementation challenges, while alternative proposals were discussed to maintain compatibility. The team concluded that while removing bloom filters was technically feasible, they should proceed with caution due to potential hash logic changes in clients.

The team discussed two Ethereum Improvement Proposals (EIPs): EIP 7668 (removing bloom filters) and EIP 7745 (trustless log index). While there was general agreement that EIP 7668 should be included in the upcoming “Glamsterdam” fork, concerns were raised about EIP 7745, with some clients (Nethermind and Erigon) opposing its inclusion due to complexity and potential consensus issues. The team decided to defer EIP 7745 to the next fork (H-star), as more time would be needed for implementation, testing, and inter-team communication. Zsolt, the proposal’s author, expressed disappointment but agreed to continue working on it independently.

The team discussed the status of several EIPs and decided to DFI (Delay For Implementation) some items for Glamsterdam, including conditional transactions (EIP-7793) and payout changes, as there wasn’t enough client support. Ansgar suggested organizing a breakout call with Nick to further discuss these topics, as direct changes during AllCoreDevs calls were unlikely to succeed. The team agreed to finalize the scope for Glamsterdam by the end of next week’s call, with a focus on protocol-changing EIPs and state growth handling.

### Next Steps:

- Pooja: Collect feedback asynchronously on ACDG proposal, EIP upgrade field proposal, and call for input process changes
- All participants: Review and provide async feedback on governance proposals in the document shared by Pooja
- State growth EIP team: Continue work on EIP 37 estate creation gas cost increase for decision next week
- Contract size EIP  proponents: Work on EIP 7907 implementation and analysis during the week before next ACDE, or it will be out of consideration
- Carlos : Officially withdraw EIP 8058 for Glamsterdam
- Marc : Share thread explaining EIP 7793 in next agenda and collect feedback before next week’s call
- EIP 7793 champion: Convince Geth team asynchronously before next week to improve chances of inclusion
- Zsolt : Coordinate with Nick to organize an ACD breakout call on trustless log index after Glamsterdam scoping is complete
- All client teams: Prepare final decisions on remaining EIPs  for next Thursday’s call
- Akash: Stream next Thursday’s ACDC meeting

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: A5pHcK?0)
- Download Chat (Passcode: A5pHcK?0)
- Download Audio (Passcode: A5pHcK?0)

---

**system** (2026-01-05):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=1B03r5t03bU

