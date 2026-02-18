---
source: magicians
topic_id: 25913
title: EIPIP Meeting #122, Dec 17, 2025
author: system
date: "2025-10-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eipip-meeting-122-dec-17-2025/25913
views: 77
likes: 1
posts_count: 2
---

# EIPIP Meeting #122, Dec 17, 2025

### Agenda

## Call for Input

- Discussion on new EIP editor – Jochem
- Call for Input: Updating Links to ethereum.org
- Allow Links to Unicode Technical Standards

## Editors’ Discussion

- Do we want to move Call for Input Issues to ethereum/pm for increased visibility?
- How should we best handle open PRs in the EIPs & ERCs repo?

Should we grant more Editors the permissions needed to force-merge when appropriate?

[Topics suggested](https://github.com/ethereum/pm/issues/1777#issuecomment-3575593807) and [here](https://github.com/ethereum/pm/issues/1777#issuecomment-3665986257) by [@jochem-brouwer](/u/jochem-brouwer)
Restructure & rename EIPIP meeting

- Extend invitation to the Ethereum Governance team from EF, client devs, along with EIP Editors.
- Rename ot to ACD-G with a once-a-month cadence
- Agenda to share & discuss present process & potential concerns. Support and guidance can help streamline the new upgrade process.

PRs for Editors review and/or consensus

- Misc

Update EIP-1186: fix broken links by sashass1315 · Pull Request #10319 · ethereum/EIPs · GitHub
- Update EIP-8: Replace incorrect HMAC-256 reference with Keccak-256 MAC in EIP-8 by MozirDmitriy · Pull Request #10338 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/10693

From EIP Office Hour [76](https://github.com/ethereum/pm/issues/1775)

- How best to handle reference implementation? Ref
- A collection of EIP documentation formats for test cases and reference implementation at a canonical place for new authors to refer to.

EIP-1 Updates & Editorial Policies: Follow up (any PRs from the last discussion?)

- EIP-1 isn’t updated on the website with changes pushed with PR

## PR analytics & Editors’ Updates

- Observations from incoming PRs over the past month

Increased volume of PRs for “Typo” fixes. Ref here

Availability for hosting EIP Editing Office Hours → add to the [schedule](https://docs.google.com/spreadsheets/d/1L1_HMqXyYndQZzG3494wcqFcUv9RpzzX67Rdo0UnKqU/edit?gid=0#gid=0)

## EIP Insight

- December 2025

## Community feedback/update

- Suggestion:

Adding “Upgarde” name on Final EIPs Ref: here
- Including the metrics of EIP number allocation in the “EIPsInsight” leaderboard

Will there be a canonical place outside the sheet to provide this data?

Project Showcase or feedback

## Next meeting - Jan 21 at 1600 UTC

**Meeting Time:** Wednesday, December 17, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1777)

## Replies

**poojaranjan** (2026-01-04):

# AI Summary

Meeting summary

## Quick recap

The meeting focused on coordinating logistics for upcoming EIP-related meetings and addressing technical issues with GitHub URLs. The team discussed various aspects of the EIP improvement process, including the review process, handling of PRs, and potential updates to the EIP system. They also explored solutions for managing the increasing number of PRs in EIP repositories and considered restructuring the EIP meeting to be more inclusive.

## Next steps

- jochem-brouwer: Leave a comment on the relevant issue (EIP 1186) regarding the use of archive.org links instead of direct Ethereum.org links, and clarify the reasoning for future reference.
- Sam: Talk to the DevOps team about adding more editors (e.g., Kshir) to the force merge group for EIP/ERC PRs.
- Pooja: Draft a document proposing the addition of an optional “upgrade” field to the EIP preamble, specifying when it can be activated and the associated responsibilities, for further discussion and input.
- jochem-brouwer: Make a pull request with updated GitHub account information for editorial and technical review separation, and propose changes for bot handling of multiple accounts.
- Pooja: Open a call for input to collect ideas from editors and the community about the best place to host/make visible “call for input” issues (e.g., EIPs repo, PM repo, or via banner on EIPs website).
- Pooja: Revisit the proposal to restructure/expand/rename the EIPPIP meeting (e.g., to ACD governance) and extend invitations to Ethereum governance team and client devs, bringing it for further discussion in the next meeting.

## Summary

### EIP Meeting Logistics Coordination

Pooja and Akash discussed the logistics for an upcoming meeting, ensuring the correct Zoom link was being used and that there was sufficient space in the meeting room. They agreed to use their own Zoom link for all EIP-related meetings to avoid any future issues. Pooja mentioned that she had updated the calendar with the correct meeting details, and they briefly discussed a confusion with another link that had been shared.

### GitHub URL Access Issues Resolved

The meeting discussed issues with the GitHub URL for EIP meetings, which was inaccessible to participants outside the Ethereum Foundation. Pooja explained that they would now use a cat herders meeting link instead, and had updated the protocol calendar and agenda with the new Zoom link. The group was waiting for Sam to join, and Pooja mentioned that Victor might be on vacation. Shariq joined the meeting to learn about the EIP process, as he had recently started attending Ethereum calls.

### EIPPIP Process Overview Meeting

The EIPPIP meeting began with Pooja explaining the purpose of the meeting to Shariq, who was new to the process. They discussed the Ethereum Improvement Proposals (EIPs) and the improvement process (IP). Pooja shared the meeting agenda and explained that the meeting is held once a month to discuss the current process and any community suggestions for improving it. The meeting would continue once more editors joined, and they planned to record and stream the session for those interested in learning more about the EIPPIP process.

### Link Update Discussion

The team discussed a call for input regarding updating links to [Ethereum.org](http://Ethereum.org), where Sam expressed concerns about changing links to external resources that could become outdated, and Jochem agreed, suggesting they should first update EIP1 to allow such changes. They decided to allow links to [archive.org](http://archive.org) as an alternative solution, with Jochem agreeing to leave a comment on the issue. The team also reviewed Unicode Technical Standard links, which received two yes votes.

### EIP Repository Management Discussion

The editors discussed moving the “Call for Input” issues to the Ethereum PM GitHub repositories for increased visibility, with Sam suggesting moving them to the EIP’s repository instead. Jochem raised concerns about potential confusion with the acronym “CFI” and proposed collecting input from other editors on the best location for these issues. The team also addressed the increasing number of PRs in EIP and ERC repositories, with Pooja suggesting a call for input to explore solutions for managing this volume, including potentially granting more editors the ability to close or force merge PRs.

### EIP Editor Review Process

Sam and Pooja discussed the rules for editor review in the EIP review bot. They agreed that most EIPs only need one editor, but certain conditions still require two editors, such as important proposals or website edits. Pooja explained the process for handling PRs for finalized EIPs, where editors can make the decision to merge if the change is trivial and no author response is received after 2-4 weeks.

### EIP Management and Review Process

The team discussed several topics related to EIPs and their management. They agreed to add more people to the force merge group, with Sam planning to talk to DevOps about this. The group also discussed adding an upgrade field to EIPs, with Pooja suggesting it could be an optional field in the preamble used when proposals are moved to final status. Jochem raised concerns about the distinction between technical and editorial reviews, leading to a discussion about potentially using separate GitHub accounts for different types of reviews. The team also considered restructuring and renaming the EIP meeting to be more inclusive and open to client developers and the Ethereum governance team. They agreed to revisit this discussion next month.

