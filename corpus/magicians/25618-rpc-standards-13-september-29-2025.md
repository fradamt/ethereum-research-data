---
source: magicians
topic_id: 25618
title: RPC Standards #13 | September 29, 2025
author: system
date: "2025-09-29"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rpc-standards-13-september-29-2025/25618
views: 26
likes: 0
posts_count: 3
---

# RPC Standards #13 | September 29, 2025

### Agenda

1. Review of Proposed Changes on Error Codes and Standardization

- EIP Draft: Add execution-errors.yaml  https://github.com/simsonraj/execution-apis/blob/527bb9af49ba12bbed37cc36d4cfe42048cd114e/src/extensions/README.md
- Pull Request: JSON RPC Error codes standardization using open-rpc extension specs by simsonraj · Pull Request #650 · ethereum/execution-apis · GitHub

1. Improving Hive RPC Compatibility Tests

**Meeting Time:** Monday, September 29, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1746)

## Replies

**system** (2025-09-29):

### Meeting Summary:

The team discussed error code standardization across different blockchain clients, with Simsonraj presenting a proposal for reserving specific error codes and predefining numbers for common errors. The group debated the complexity of error codes and their potential inconsistencies between clients, while also considering the need to balance legacy error codes with new standards. They concluded by agreeing to expand the scope of the proposal to include more error codes and test suites, with an emphasis on getting RPC providers to comply with the standard.

**Click to expand detailed summary**

The team discussed error codes and their review process. Simsonraj shared a README file with proposed error codes, and the group agreed to review it internally before presenting it to core developers. Mercy suggested getting feedback from client teams like Nethermind before taking it to the core dev call. Keri provided an update on RPC Compact, mentioning a recent PR merge and ongoing work on spec-only flags. The team also touched on the need to standardize error codes and address issues with block timestamps and Simulate V1 across different clients.

The team discussed standardizing error codes across different blockchain clients to provide reliable error reporting for dApps and clients. Simsonraj explained the proposal to reserve specific error codes for different categories and predefine numbers for common errors like “nonce too low.” Łukasz raised concerns about the complexity of error codes and the potential for inconsistencies between clients. They discussed the need for a more explicit specification of when certain errors should be thrown and agreed that the proposal could be expanded to include overlapping error codes for different validation levels. Łukasz suggested looking at a recent PR for insights on aligning error handling with Geth, as there had been issues with reverse-engineering Geth’s error messages.

The team discussed standardizing error codes across Ethereum clients. Simsonraj presented a proposal for standardizing error codes, which Łukasz found generally acceptable but suggested expanding the scope to include more error codes and providing a test suite to ensure compliance. The group agreed that basic error codes could be standardized relatively easily, while more complex error codes related to virtual machine execution would be more challenging. They discussed the need to balance legacy error codes with new standards, potentially using a reserved range for legacy codes. The team also touched on the importance of getting RPC providers to comply with the standard. Mercy mentioned the need for regular updates on the RLPC test suits for CINA.

### Next Steps:

- Simsonraj to conduct more extensive testing of error codes across different clients, focusing on execution-based error cases.
- Simsonraj to update the error codes proposal based on feedback received.
- Simsonraj to share the updated error codes proposal with the JSON RLPC Discord and tag core developers for feedback.
- Keri to share her spreadsheet tracking RPC compatibility issues with Mercy.
- Mercy to follow up with client teams to get feedback on the error codes proposal.
- Team to present the error codes proposal to core developers after incorporating feedback.
- Keri to provide regular updates to CINA about the progress in resolving RLPC test suite issues.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 6V9HrqF.)
- Download Chat (Passcode: 6V9HrqF.)

---

**system** (2025-09-29):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=khBTOMMqKnU

