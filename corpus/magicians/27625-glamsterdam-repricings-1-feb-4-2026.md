---
source: magicians
topic_id: 27625
title: Glamsterdam Repricings #1, Feb 4, 2026
author: system
date: "2026-01-30"
category: Protocol Calls & happenings
tags: [breakout]
url: https://ethereum-magicians.org/t/glamsterdam-repricings-1-feb-4-2026/27625
views: 33
likes: 1
posts_count: 4
---

# Glamsterdam Repricings #1, Feb 4, 2026

### Agenda

- Timeline and ToDo’s for repricing EIPs (info here) @misilva73
- Status update on EIP-7904: General Repricing @misilva73
- Status update on EIP-8037: State Creation Gas Cost Increase

Current spec from @fradamt
- Failure modes write-up from @anderselowsson
- Aggregation functions and failure modes analysis from @misilva73

[Spec PR](https://github.com/ethereum/execution-specs/pull/2133) for [EIP-7976](https://eips.ethereum.org/EIPS/eip-7976) and [EIP-7981](https://eips.ethereum.org/EIPS/eip-7981) by [@nerolation](/u/nerolation)

**Meeting Time:** Wednesday, February 04, 2026 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1910)

## Replies

**system** (2026-02-04):

### Meeting Summary:

The team reviewed and discussed various EIPs related to compute repricing, state growth, and gas costs, with Maria presenting a timeline and preliminary numbers for February. They examined specific opcode costs and gas accounting mechanisms, including discussions about transaction receipts and enforcement of gas limits. The conversation ended with conversations about gas refunds and their integration with state gas, along with updates on related EIPs and potential collaboration between L1 and L2 teams on benchmarking work.

**Click to expand detailed summary**

The team discussed the timeline and to-dos for EIPs, focusing on compute repricing and state growth. Maria presented a plan to have preliminary numbers by the end of February, with all tooling and specs ready by then. They reviewed the updated EIP 7904, which now focuses on repricing only 13 operations that are current bottlenecks. The team agreed to run more tests and verify the numbers, particularly for state operations and block-level access lists.

The team discussed gas costs for various opcodes, with Justin questioning the rationale behind increased costs for Div and SDiv compared to Add. Maria explained that the numbers came directly from benchmarks, measuring runtime for blocks of opcodes and converting to gas using a rate of 60 million gas per second. Ben noted that point evaluation increases should affect the blob-based fee floor, which Maria agreed to add to the EIP specifications. The conversation ended with Francesco being asked to provide an update on EIP-8037, but his response was not included in the transcript.

Francesco reviewed the current state of the EIP and found it mostly aligned with the specifications, though there were some minor differences in naming and gas costs. He identified several open questions, including how to handle regular gas costs for operations involving state gas, the precise cost of creating a new account, and whether to differentiate between different types of storage operations in regular gas pricing. Francesco also noted a need to clarify how the reservoir mechanism for state gas interacts with the transaction gas limit, suggesting that intrinsic regular gas should be checked against the cap and subtracted from the total allowed gas before execution.

The group discussed gas accounting and transaction receipts, focusing on EIP-7778 and EIP-8037. Toni explained that a proposed new field for gas spent was reverted due to opposition from Erigon, citing additional work. Ben and others debated whether to add a new field or change the semantics of cumulative gas in receipts, with Toni suggesting it might not be necessary to modify receipts at all. The group also discussed transaction max gas limit enforcement, with Francesco proposing to enforce limits on intrinsic gas consumption as well as execution gas. They agreed to add this to the EIP and specs, though questions remained about call data floor costs and the purpose of enforcing limits for non-execution components.

The meeting focused on discussing gas refunds and their integration with state gas. Maria and Francesco debated whether refunds should be subtracted from state gas, with Francesco suggesting it could be more involved but decided it was out of scope for the EIP. Justin proposed a conceptual approach to integrate refunds with state gas, which Maria agreed to consider further. The group also reviewed analyses by Anders and Maria on the impact of gas metering on base fees, discussing potential failure modes and the need for further analysis. Ben and Toni provided updates on EIPs related to transfer pricing and call data costs, respectively. The conversation ended with a brief discussion on collaboration between L1 and L2 teams on benchmarking work, with Josh from OP Labs expressing interest in aligning efforts.

### Next Steps:

- Maria: Keep the timeline and to-dos page updated as needed
- Maria: Add point evaluation increase impact on blob-based fee floor to the EIP
- Maria: Link the EIP PR in the agenda
- Maria/Team: Go back to tests and verify that runtime numbers for operations like AddMod, Div, and SDiv are correct
- Ben: Look at 256-bit mods as they’re used for outputs and are significantly worse than small mods
- Francesco: Write a small recap of open questions in the chat
- Maria: Understand the transaction receipts open question after the call
- Team: Discuss and decide whether to add new field to receipts for gas accounting
- Team: Add intrinsic gas enforcement to transaction max limit in EIP and specs for 8037
- Team: Think more about integrating refunds with state growth EIP and whether refunds should be subtracted from state gas
- Team: Review and provide comments on Anders’ analysis regarding base-fee and resource consumption
- Team: Review and provide comments on Toni’s PR for data EIPs 7976 and 7981
- Ben: Add charging for ETH transfer logs in EIP 2780
- Toni: Create a PR for the 64/64 call data cost harmonization
- Toni: Put the 64/64 call data cost topic on the agenda again in 2 weeks
- Team: Align on best place to share benchmarking findings and tooling with L2 teams
- Ansgar: Reach out to OP Labs once there are thoughts on strengthening collaboration with L2s
- Jochem: Integrate benchmarking tests into the EEST testing suite

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: s%+=85e7)
- Download Chat (Passcode: s%+=85e7)
- Download Audio (Passcode: s%+=85e7)

---

**system** (2026-02-04):

### Meeting Summary:

The team reviewed and discussed various EIPs related to compute repricing, state growth, and gas costs, with Maria presenting a timeline and preliminary numbers for February. They examined specific opcode costs and gas accounting mechanisms, including discussions about transaction receipts and enforcement of gas limits. The conversation ended with conversations about gas refunds and their integration with state gas, along with updates on related EIPs and potential collaboration between L1 and L2 teams on benchmarking work.

**Click to expand detailed summary**

The team discussed the timeline and to-dos for EIPs, focusing on compute repricing and state growth. Maria presented a plan to have preliminary numbers by the end of February, with all tooling and specs ready by then. They reviewed the updated EIP 7904, which now focuses on repricing only 13 operations that are current bottlenecks. The team agreed to run more tests and verify the numbers, particularly for state operations and block-level access lists.

The team discussed gas costs for various opcodes, with Justin questioning the rationale behind increased costs for Div and SDiv compared to Add. Maria explained that the numbers came directly from benchmarks, measuring runtime for blocks of opcodes and converting to gas using a rate of 60 million gas per second. Ben noted that point evaluation increases should affect the blob-based fee floor, which Maria agreed to add to the EIP specifications. The conversation ended with Francesco being asked to provide an update on EIP-8037, but his response was not included in the transcript.

Francesco reviewed the current state of the EIP and found it mostly aligned with the specifications, though there were some minor differences in naming and gas costs. He identified several open questions, including how to handle regular gas costs for operations involving state gas, the precise cost of creating a new account, and whether to differentiate between different types of storage operations in regular gas pricing. Francesco also noted a need to clarify how the reservoir mechanism for state gas interacts with the transaction gas limit, suggesting that intrinsic regular gas should be checked against the cap and subtracted from the total allowed gas before execution.

The group discussed gas accounting and transaction receipts, focusing on EIP-7778 and EIP-8037. Toni explained that a proposed new field for gas spent was reverted due to opposition from Erigon, citing additional work. Ben and others debated whether to add a new field or change the semantics of cumulative gas in receipts, with Toni suggesting it might not be necessary to modify receipts at all. The group also discussed transaction max gas limit enforcement, with Francesco proposing to enforce limits on intrinsic gas consumption as well as execution gas. They agreed to add this to the EIP and specs, though questions remained about call data floor costs and the purpose of enforcing limits for non-execution components.

The meeting focused on discussing gas refunds and their integration with state gas. Maria and Francesco debated whether refunds should be subtracted from state gas, with Francesco suggesting it could be more involved but decided it was out of scope for the EIP. Justin proposed a conceptual approach to integrate refunds with state gas, which Maria agreed to consider further. The group also reviewed analyses by Anders and Maria on the impact of gas metering on base fees, discussing potential failure modes and the need for further analysis. Ben and Toni provided updates on EIPs related to transfer pricing and call data costs, respectively. The conversation ended with a brief discussion on collaboration between L1 and L2 teams on benchmarking work, with Josh from OP Labs expressing interest in aligning efforts.

### Next Steps:

- Maria: Keep the timeline and to-dos page updated as needed
- Maria: Add point evaluation increase impact on blob-based fee floor to the EIP
- Maria: Link the EIP PR in the agenda
- Maria/Team: Go back to tests and verify that runtime numbers for operations like AddMod, Div, and SDiv are correct
- Ben: Look at 256-bit mods as they’re used for outputs and are significantly worse than small mods
- Francesco: Write a small recap of open questions in the chat
- Maria: Understand the transaction receipts open question after the call
- Team: Discuss and decide whether to add new field to receipts for gas accounting
- Team: Add intrinsic gas enforcement to transaction max limit in EIP and specs for 8037
- Team: Think more about integrating refunds with state growth EIP and whether refunds should be subtracted from state gas
- Team: Review and provide comments on Anders’ analysis regarding base-fee and resource consumption
- Team: Review and provide comments on Toni’s PR for data EIPs 7976 and 7981
- Ben: Add charging for ETH transfer logs in EIP 2780
- Toni: Create a PR for the 64/64 call data cost harmonization
- Toni: Put the 64/64 call data cost topic on the agenda again in 2 weeks
- Team: Align on best place to share benchmarking findings and tooling with L2 teams
- Ansgar: Reach out to OP Labs once there are thoughts on strengthening collaboration with L2s
- Jochem: Integrate benchmarking tests into the EEST testing suite

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: s%+=85e7)
- Download Chat (Passcode: s%+=85e7)
- Download Audio (Passcode: s%+=85e7)

---

**system** (2026-02-04):

YouTube recording available: https://youtu.be/U2R-AI_F9t0

