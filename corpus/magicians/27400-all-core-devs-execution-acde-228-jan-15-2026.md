---
source: magicians
topic_id: 27400
title: All Core Devs - Execution (ACDE) #228, Jan 15, 2026
author: system
date: "2026-01-07"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-228-jan-15-2026/27400
views: 109
likes: 3
posts_count: 4
---

# All Core Devs - Execution (ACDE) #228, Jan 15, 2026

### Agenda

- Glamsterdam

devnets

devnet-2 scope

EIP clarifications

- EIP-7778: Block Gas Accounting without Refunds

Clarifications on CumulativeGasUsed, gasUsedForPaying, & gasUsedForBlockLimit

EIP-8024: Backward compatible SWAPN, DUPN, EXCHANGE

- Clarification on behavior when code ends before immediate operand
- Proposal for simpler version

EIP-7708: ETH transfers emit a log

- pending PR with open questions

Remaining Glamsterdam PFI decisions

- EL PFI’d EIPs status doc

postponed last ACDE

EIP-8037: State Creation Gas Cost Increase

@MariusVanDerWijden will explain the recommended approach: slides here

no time last ACDE

- EIP-7793: Conditional Transactions
- EIP-5920: PAY opcode
- EIP-8051: Precompile for ML-DSA signature verification

delayed decision last ACDE

- EIP-7971: Hard Limits for Transient Storage
- EIP-8032: Size-Based Storage Gas Pricing
- EIP-7907: Meter Contract Code Size And Increase Limit

benchmarks & analysis by @CPerezz

EIP-7903: Remove Initcode Size Limit

EIPs without protocol changes

- EIP-7610: Revert creation in case of non-empty storage
- EIP-7872: Max blob flag for local builders
- EIP-7949: Genesis File Format

Misc

- Request for client review on execution API items

**Meeting Time:** Thursday, January 15, 2026 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1867)

## Replies

**poojaranjan** (2026-01-15):

Quick Summary on [Twitter](https://x.com/poojaranjan19/status/2011833637369757829).

TL;DR

| Status | EIP | Title / Topic | Notes / Decision |
| --- | --- | --- | --- |
| CFI | EIP-7954 | Increase Maximum Contract Size | Preferred over complex metering; conservative 80/20 improvement; includes initcode size adjustment |
| DFI | EIP-7793 | Conditional Transactions | Insufficient client support; consider for H-Star |
| DFI | EIP-5920 | PAY Opcode | No client consensus |
| DFI | EIP-8051 | Precompile for ML-DSA Signature Verification | PQ crypto discussion; client uncertainty; defer to H-Star; breakout planned |
| DFI | EIP-7971 | Hard Limits for Transient Storage | No progress; deferred |
| DFI | EIP-8032 | Size-Based Storage Gas Pricing | Performance concerns; insufficient data |
| DFI | EIP-7907 | Meter Contract Code Size and Increase Limit | Replaced by simpler bump approach |
| DFI | EIP-7903 | Remove Initcode Size Limit | Explicitly deferred |
| Delayed | EIP-8037 | State Creation Gas Cost Increase | Decision deferred to ACDT (Jan 19) |
| Pending (Devnet 2 spec) | EIP-7778 | Block Gas Accounting without Refunds | Async PR discussion |
| Pending (Devnet 2 spec) | EIP-8024 | Backward compatible SWAPN / DUPN / EXCHANGE | ACDT decision pending |
| Pending (Devnet 2 spec) | EIP-7708 | ETH Transfers Emit a Log | General agreement; PR pending |
| Pending (Devnet 2 spec) | EIP-7843 | SLOTNUM opcode | CL coordination concern; revisit at ACDT |

---

**system** (2026-01-15):

### Meeting Summary:

The team discussed and made preliminary decisions about various EIPs and their inclusion in the DevNet 2 and Glamsterdam fork, including block gas accounting, immediate operand encoding, and state growth solutions. They agreed to revisit several decisions on Monday when Lodestar representatives return from holiday, particularly regarding the scope of DevNet 2 and the state growth pricing proposal. The team ultimately decided to delay implementation of certain EIPs that would require more complex solutions, opting instead for simpler immediate changes to allow for more comprehensive repricing in future forks.

**Click to expand detailed summary**

The team discussed the scope of DevNet 2, with a preliminary decision made on Monday that may need revision due to potential CL changes. They agreed to revisit this decision on Monday when Lodestar representatives return from holiday. The group also addressed several EIP clarifications, including EIP 7778 regarding block gas accounting and EIP 8024 on SWAPN DUPN exchange opcodes. Toni and Andrew clarified that cumulative gas used in receipts should be consistent with block gas accounting, and agreed to continue the discussion asynchronously under the relevant PR.

The team discussed two versions of an EIP related to immediate operand encoding, with the main debate being between a postfix push approach and the current EIP specification. Dragan expressed a preference for the postfix push version, while Daniel confirmed Besu’s implementation aligns with the current EIP. The team agreed to gather feedback asynchronously, with Frangio monitoring both Discord and the Ethereum EIP repository, and decided to aim for a decision by Monday ACDT, with the current implementation to be used if no consensus is reached.

The team discussed EIP-8037, which proposes a solution for state growth by making it dependent on the block gas limit, aiming to harmonize state creation across operations and limit state growth to approximately 100GB per year. Andrew expressed concerns about the “hacky” nature of the solution, preferring a more comprehensive multidimensional gas approach, while Ansgar emphasized the urgency of addressing state growth to enable higher gas limits in the Glamsterdam update. The team agreed to finalize the scope for devnet-2 on Monday, with a potential launch date of January 28th, and to continue discussions on state growth solutions.

The meeting focused on discussing several EIPs and making decisions about including them in the Glamsterdam fork. The team decided to DFI (Delay to Future Implementation) EIP 7907, which proposes metering contract code size and increasing the limit, in favor of a simpler bump to 32 kilobytes for contract size as proposed in EIP 7954. They also decided to DFI EIP 7903, which would remove the init code size limit, and to delay the decision on state growth pricing (EIP 8037) to the next ACDT meeting on Monday. The team discussed concerns about the impact of increasing contract sizes on scalability and transaction costs, but ultimately opted for the simpler solution to allow for more complex repricing in future forks.

### Next Steps:

- Lodestar team: Discuss EIP7843  inclusion in DevNet 2 on Monday when team member returns from holiday
- Andrew: Review PR on EIP7778  regarding cumulative gas used clarification and provide feedback
- Toni: Continue async discussion with Andrew under the PR for EIP7778 clarifications
- Client teams: Review and provide feedback on EIP8024  encoding options by Monday ACDT
- Stefan: Assess DevNet 2 readiness on Monday and decide on launch date
- Client teams: Finalize DevNet 2 scope decisions on Monday ACDT
- Spencer: Finalize execution tests for DevNet 2 after specs are finalized
- Client teams: Review init code size adjustment in EIP7954  and provide any feedback on the proposed bump from 48KB to 64KB

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: KVHJ&4dY)
- Download Chat (Passcode: KVHJ&4dY)
- Download Audio (Passcode: KVHJ&4dY)

---

**system** (2026-01-15):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=SMC83TdqgLY

