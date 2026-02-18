---
source: magicians
topic_id: 25910
title: EIP Editing Office Hour (EIP Only) Meeting #76, Oct 21, 2025
author: system
date: "2025-10-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-only-meeting-76-oct-21-2025/25910
views: 23
likes: 0
posts_count: 4
---

# EIP Editing Office Hour (EIP Only) Meeting #76, Oct 21, 2025

### Agenda

Editor: @g11tech

### To Review

- Update EIP-7916: Move to Review by etan-status · Pull Request #10526 · ethereum/EIPs · GitHub

### Misc

- Update EIP-7799: Validate systemLogsRoot in engine_newPayloadVx instead of forkchoiceUpdated by MozirDmitriy · Pull Request #10529 · ethereum/EIPs · GitHub
- Update EIP-7898: add normative Specification details and RFC 2119 note by MozirDmitriy · Pull Request #10550 · ethereum/EIPs · GitHub

### Force merge

- Update EIP-7773: sort PFI'd EIPs by adietrichs · Pull Request #10564 · ethereum/EIPs · GitHub

### To Draft

- Add EIP: Exclude slashed validators from proposing by fradamt · Pull Request #10547 · ethereum/EIPs · GitHub
- Add EIP: FOCIL with ranked transactions (FOCILR) by anderselowsson · Pull Request #10554 · ethereum/EIPs · GitHub
- Add EIP: Precompile for ML-DSA signature verification by simonmasson · Pull Request #10557 · ethereum/EIPs · GitHub
- Add EIP: Precompile for Falcon support by simonmasson · Pull Request #10560 · ethereum/EIPs · GitHub
- Add EIP: Inter-Block Temporal Locality Gas Discounts by benaadams · Pull Request #10579 · ethereum/EIPs · GitHub

### Review from

**Meeting Time:** Tuesday, October 21, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1775)

## Replies

**system** (2025-10-21):

### Meeting Summary:

The meeting focused on reviewing Ethereum Improvement Proposals (EIPs) and associated pull requests, with participants discussing technical changes, documentation requirements, and process improvements. The team addressed concerns about reference implementations in the EIP repository and agreed to explore better solutions for managing code references. They also discussed the need for clearer documentation and testing processes, with plans to create a consolidated document outlining all test requirements for future discussion at the EIPIP meeting.

**Click to expand detailed summary**

The meeting focused on reviewing Ethereum Improvement Proposals (EIPs) and their associated pull requests (PRs). Pooja explained that the meeting would be recorded and summarized by an AI bot, and shared the agenda which included PRs related to EIPs. She noted that some proposals were in the draft category and suggested reviewing them after addressing issues from the EIP board. Participants were encouraged to share links to their EIP-related PRs in the chat for review during the meeting.

Gajinder reviewed several PRs related to technical changes and EIPs, noting that some were not within the scope of EIP editing. He mentioned that he had co-authored an EIP and provided feedback on others, while also unblocking a CIP that had been merged. Gajinder discussed the need to address the handling of reference implementations in the EIP repo, as there was a concern about the repository becoming too bulky with active code. He suggested raising this issue at the next EIPIP meeting to determine the best approach for managing reference implementations.

The team discussed the need for a better solution to reference implementations in EIPs, with agreement to allow GitHub code references with fixed commit numbers. They reviewed several pending PRs, noting that most were stuck waiting for author responses rather than editorial review. Gajinder and Pooja agreed to bring attention to Alex regarding PR 9395 since Stimp is unavailable, and Rohan raised concerns about the lack of documentation for the EIP submission process, to which Pooja responded by sharing the existing eip-template.md and EIP-1 documentation.

Gajinder and Rohan discussed issues with the EIP and ERC submission process, particularly regarding unclear test cases and documentation. Rohan highlighted that certain formatting checks, such as hyperlinking ERCs, are not well-documented, leading to long wait times for test results. Gajinder suggested running tests locally to expedite the process and confirmed that CI tests are based on documented rules in EIP1 and ERC1. Rohan proposed creating a consolidated document outlining all test requirements, and Gajinder agreed this could be a valuable addition. They decided to add this topic to the EIPIP agenda for further discussion.

The team discussed the process of replicating and documenting proposals, with Pooja suggesting to use EIP1 instead of ERC1 for consistency and better documentation. Rohan agreed this made sense and mentioned the need for clear notes and samples in the Git repo. Ben joined to highlight his EIP and expressed interest in adding it to the Meta EIP 8007, which focuses on Glamsterdam gas-free pricing.

The team reviewed EIPs and PRs, with Gajinder providing feedback to Ben on indentation and test cases placement in the specification. Ben agreed to move test cases into the specification rather than security considerations, and Gajinder approved of this change. Pooja reported that there are 36 PRs on the EIP board, most of which are on the consensus side and require further review. The team decided to conclude the session early, with the next Editing Office Hour scheduled for Tuesday at 1600 UTC.

### Next Steps:

- Pooja: Add PR 10557  to the next EIPIP meeting agenda
- Pooja: Add discussion about creating a sample EIP/ERC with all features to the EIPIP meeting agenda
- Gajinder: Wait for author response on PR 9354 before proceeding
- Gajinder: Bring PRs related to EIP 7569 to Alex’s attention to clarify who is in charge
- Gajinder: Review and approve Ben’s PR 10579 after Ben completes requested changes
- Ben: Fix external image link issue in PR 10579
- Ben: Remove manual indentation/new lines in PR 10579 text
- Ben: Move test cases and reference implementation sections into specification section in PR 10579
- Rohan: Create a PR to update README with condensed documentation about CI tests and formatting requirements

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 6F@G@&4g)
- Download Chat (Passcode: 6F@G@&4g)

---

**system** (2025-10-21):

YouTube recording available: https://youtu.be/WfOKPNfGF-o

---

**system** (2025-10-22):

YouTube recording available: https://youtu.be/9UHRSnMbgTM

