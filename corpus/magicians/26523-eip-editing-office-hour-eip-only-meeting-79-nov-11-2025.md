---
source: magicians
topic_id: 26523
title: EIP Editing Office Hour (EIP only) Meeting #79, Nov 11, 2025
author: system
date: "2025-11-11"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-only-meeting-79-nov-11-2025/26523
views: 28
likes: 0
posts_count: 3
---

# EIP Editing Office Hour (EIP only) Meeting #79, Nov 11, 2025

### Agenda

Editor: @g11tech

### To Review

- Update EIP-7495: Move to Review

### To Draft

- Add EIP: Precompile for Falcon support by simonmasson · Pull Request #10560 · ethereum/EIPs · GitHub
- Add EIP: ZKMeta Metadata Interface by zwowo1997 · Pull Request #10768 · ethereum/EIPs · GitHub
- Add EIP: Precompile for NTT operations
- Add EIP: Milli-gas for High-precision Gas Metering
- Add EIP: Dynamic State Pricing for Steady Growth
- Add EIP: Precompile for Falcon support

#### Other

- fix undefined variable `el` in Optional.value_byte_length() method by kianjib7 · Pull Request #10311 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/10524
- Create SECURITY.md by Reality2byte · Pull Request #10204 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/10698
- Update EIP-7594: correct sign in probability table for ε=0.01 by MozirDmitriy · Pull Request #10736 · ethereum/EIPs · GitHub
- Remove unused assignments in deposit snapshot tests by MamunC0der · Pull Request #10571 · ethereum/EIPs · GitHub
- Drop unused ABC import in deposit snapshot by wedjob0X · Pull Request #10572 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/10576
- Remove unused helper from deposit snapshot tests by wedjob0X · Pull Request #10577 · ethereum/EIPs · GitHub

Close?

- CI: Create python-package-conda.yml (Spam)
- Bump webrick from 1.8.1 to 1.8.2 (No longer needed)
- Update EIP-5003: Move to Stagnant by Tsukimarf · Pull Request #10567 · ethereum/EIPs · GitHub

# Announcement

- Meet editors and authors in EIP Summit ARG
- Next Office Hour is on Nov 25th at 16:00 UTC

**Meeting Time:** Tuesday, November 11, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1809)

## Replies

**system** (2025-11-11):

### Meeting Summary:

The EAP Editing Office Hour meeting was hosted by Pooja, who introduced Gajinder as the EIP editor for the session, with the focus on reviewing various proposals and pull requests on the Ethereum PM GitHub repository. The team discussed several pull requests, addressed issues with PR tagging and documentation, and clarified the distinction between motivation and rationale sections in EIP proposals. The conversation ended with discussions about deposit snapshot proposals and potential spammy PRs, along with announcements about an upcoming EIP Summit in Argentina and the cancellation of the next office hour.

**Click to expand detailed summary**

Pooja hosted the EAP Editing Office Hour meeting and introduced Gajinder as the EIP editor for the session. Gajinder confirmed readiness to review proposals on the Ethereum PM GitHub repository, with the meeting focusing on issue #1809.

Pooja and Gajinder reviewed several proposals, noting that one was not for Fusaka but might be for Glamsterdam. They discussed moving a proposal to the review status and identified another as potentially an ERC metadata interface, deciding to leave a comment for the author to move it to ERC Depot. They also reviewed PR 9374 on entity operations, observing that many of Gajinder’s comments hadn’t been addressed by the author.

The team discussed PRs 10311 and 6475, with Pooja noting that some drafts had been addressed while Gajinder believed none had been addressed. They identified an issue where authors were not being tagged in multiple PRs, particularly when only assets were modified. Csaba joined the conversation briefly but did not contribute significantly to the discussion.

The team discussed reviewing a peer and agreed to move the discussion to the EIPIP meeting, where they will address a pull request related to documentation improvements. Pooja suggested creating an issue to list all relevant pull requests, and Gajinder mentioned that the author had been asked to create an issue for their PRs. The team also briefly touched on the format of motivation and rationale sections in proposals.

Csaba sought clarification on the differentiation between motivation and rationale in EIP proposals, with Gajinder explaining that motivation addresses the pain points being solved, while rationale covers the reasoning behind design choices. Csaba also inquired about the necessity of including version numbers in EIPs, to which Gajinder clarified that version numbers are typically updated before moving to review, especially when there’s a high chance of inclusion in a hard fork. Pooja mentioned that networking proposals are now included in Meta EPs, though this is not a requirement if consensus among clients is not achieved.

The team discussed issues with PR tagging, noting that a bot was not properly tagging authors when asset changes occurred, and agreed to investigate this problem. They reviewed several PRs related to deposit snapshot proposals, deciding to batch them together for easier tracking. Pooja and Gajinder also discussed some potentially spammy or unnecessary PRs, with Gajinder suggesting they consult Sam for clarification. The conversation ended with announcements about an upcoming EIP Summit in Argentina on November 21st and the cancellation of the next office hour, scheduled for November 25th at 1600 UTC.

### Next Steps:

- Pooja/Gajinder: Leave a comment on PR 10768 for the author to move the proposal to ERC Depot
- Gajinder: Address comments on PR 9374  as many comments don’t seem addressed
- Gajinder: Follow up on PRs where only assets are modified and authors are not being tagged
- Pooja: Move documentation improvement PRs to EIPIP meeting
- Gajinder: Wait for PR author to create an issue listing all PRs for improving documentation
- Csaba: Update version number before moving proposal to review status
- Pooja: Investigate and fix bot issue where authors are not being tagged when changes are made to assets
- Gajinder: Tag authors manually on deposit snapshot related PRs
- Sam: Review and confirm whether PRs 10567 and other flagged PRs are needed or should be closed
- Gajinder: Ask user on PR 10567 if they want to champion the withdrawn EIP

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: *#ObS5r0)
- Download Chat (Passcode: *#ObS5r0)
- Download Audio (Passcode: *#ObS5r0)

---

**system** (2025-11-11):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=Ke7nVNqsu8Q

