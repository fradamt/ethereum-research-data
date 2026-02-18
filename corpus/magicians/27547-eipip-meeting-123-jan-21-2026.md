---
source: magicians
topic_id: 27547
title: EIPIP Meeting #123, Jan 21, 2026
author: system
date: "2026-01-20"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eipip-meeting-123-jan-21-2026/27547
views: 29
likes: 0
posts_count: 2
---

# EIPIP Meeting #123, Jan 21, 2026

### Agenda

## Call for Input

- Call for Input: Force Merge Fusaka Status Changes
- Call for Input: Add Associate EIP Editors
- Call for Input: Best place to host “Call for Input”
- Call for Input: Allow Links to Unicode Technical Standards

## Editors’ Discussion

- Suggestions & Issues from EIP Office Hour 85

Bot’s ToDo marker should also include TBD
- Create a GitHub label for “Force Merge” and/or “Typo”
- Bot shouldn’t ping Editor, but automerge such PR
- Linting errors should be avoided PR

“Citation” section: Remove “[DRAFT]”?

#### PRs for Editors review and/or consensus

- Misc

chore: Remove redundant minima theme dependency from Gemfile by 0xlupin · Pull Request #10966 · ethereum/EIPs · GitHub
- chore: Remove redundant minima gem dependency from Gemfile by 0xxFloki · Pull Request #11042 · ethereum/EIPs · GitHub
- chore: remove non-existent LICENSE entry from Jekyll config by Aleksandr1732 · Pull Request #11096 · ethereum/EIPs · GitHub
- chore(config): remove obsolete `include` directive by marukai67 · Pull Request #11098 · ethereum/EIPs · GitHub
- chore(config): remove non-existent template exclusions from Jekyll config by 0xxFloki · Pull Request #11100 · ethereum/EIPs · GitHub
- Update EIP-1682: two typos by oooLowNeoNooo · Pull Request #10792 · ethereum/EIPs · GitHub
- Update EIP-1186: fix broken links by sashass1315 · Pull Request #10319 · ethereum/EIPs · GitHub
- Update EIP-8: Replace incorrect HMAC-256 reference with Keccak-256 MAC in EIP-8 by MozirDmitriy · Pull Request #10338 · ethereum/EIPs · GitHub (Force merge)
- Update EIP-1682: two typos by oooLowNeoNooo · Pull Request #10792 · ethereum/EIPs · GitHub
- Update EIP-6963: fix typo by ANtutov · Pull Request #10809 · ethereum/EIPs · GitHub
- Website: Fix typo by letreturn · Pull Request #10533 · ethereum/EIPs · GitHub
- Update EIP-5: fix grammatical issues by Bashmunta · Pull Request #10845 · ethereum/EIPs · GitHub
- Update EIP-3014: Fix duplicate word repetitions by jschnelder · Pull Request #11021 · ethereum/EIPs · GitHub
- Update EIP-1682: two typos by oooLowNeoNooo · Pull Request #10792 · ethereum/EIPs · GitHub

### Updates on topics from earlier meetings

- Grant more Editors force-merge permissions.
- Best place to host “Call for Input”
- Network upgrade name and stages on eips.etherum.org
- Restructure & rename EIPIP meeting
- From EIP Office Hour 76

A collection of EIP documentation formats for test cases and reference implementation at a canonical place for new authors to refer to.

EIP-1 Updates & Editorial Policies

- Contributor.md PR
- Update to EIP-1 PR

## PR analytics & Editors’ Updates

- Observations from incoming PRs over the past month

Increased volume of PRs for “Typo” fixes. Ref here

Availability for hosting EIP Editing Office Hours → add to the [schedule](https://docs.google.com/spreadsheets/d/1L1_HMqXyYndQZzG3494wcqFcUv9RpzzX67Rdo0UnKqU/edit?gid=0#gid=0)

## EIP Insight

- January 2026

## Community feedback/update

- Project Showcase or feedback

## Next meeting - Feb 17, 2026 at 1600 UTC

**Meeting Time:** Wednesday, January 21, 2026 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1886)

## Replies

**poojaranjan** (2026-01-21):

## Quick recap (AI)

The Ethereum Improvement Proposal (EIP) editors met to discuss various updates and proposals, including the addition of associate editors and the need to clarify their roles. They reviewed the status of several EIPs, discussed the increasing number of typo and formatting fixes, and considered ways to streamline the review process. The team also addressed the need for a contributor guideline document and discussed potential improvements to the EIP review workflow. Updates were provided on the number of new EIPs and ERCs created in January, as well as the progress made in moving proposals to final status. The conversation ended with a reminder of the upcoming office hours and the next EIP meeting scheduled for February 17th.

## Next steps

- jochem-brouwer: leave a comment on Matt’s call for input for adding an associate editor role by today
- Editors: review and approve PRs 7910 and 7935 to move them to final status (after author approval already received)
- Pooja: communicate with authors to get responses on 3 pending EIPs to move them to final status
- Sam: open an issue about the bot incorrectly pinging editors when only assets are edited
- Sam: open a bug about the tooling issue with the citation section incorrectly showing “draft” status
- Editors: review PR 1124 (contributor.md) and associated PR to reference contribution guidelines in EIP 1
- Editors: review and handle PRs requiring Jekyll knowledge that are currently blocked
- Editors: allocate themselves new date/time slots for office hours in the shared sheet
- Sam: review PRs that were requested by Garjendar
- Editors: review the text and suggest fixes for the contributor.md guidelines

## Summary

### EIP Meeting #1886 Review

The meeting began with Pooja welcoming participants and introducing the agenda for Ethereum Improvement Proposal (EIP) Meeting #1886. She mentioned that the meeting aimed to review call for inputs, editor discussions, PRs, and updates from previous meetings. Sam was invited to discuss the call for inputs, with the goal of addressing and closing them during the meeting.

### Associate Editor Role Proposal Discussion

The team discussed two main topics: the closure of PR #400 regarding Fusaka status changes, and a proposal to add associate editor roles. Pooja reported that all editors had been contacted and the PR was now closed. Jochem agreed to review and comment on the associate editor proposal, which aims to allow more people to merge PRs while maintaining governance process eligibility restrictions. Pooja raised concerns about the terminology, suggesting that “EIP reviewer” might be more appropriate than “associate editor” to avoid confusion with existing roles, and proposed moving existing reviewers into the new associate editor role. The team agreed to further discuss the proposal at the next meeting, with a deadline of February 10th for input.

### EIP Pull Request Status Review

The team discussed the status of various EIP pull requests, with Sam confirming that one PR was closed while others needed attention. Pooja presented a list of pending PRs for EIP 7723, including one that required author review for stage/status terminology corrections. The team noted that two PRs for EIP 7910 had received author approval but were awaiting editor approval to move to final status, while EIP 7935 was ready for editor approval after receiving author approval. Gajandar’s suggestion from the EIP editing office hour was discussed regarding the use of “TBD” instead of “to-do” in the review process to prevent bot-related delays.

### PR Bot and Merge Issues

Sam and Pooja discussed several issues with the review bot and PR handling. They agreed to create an issue for fixing the bot’s inability to handle asset-only edits, which Mark might help with. Sam confirmed that linter issues in PRs would not block merges. Pooja raised a bug where the citation section remains in draft mode, which Sam agreed to open a bug report for. They also noted that many PRs require force merges or editor attention, and Sam has a CI for one specific PR. The discussion concluded with a reminder about granting more editors force merge permissions, though no updates were provided on this topic.

### EIP Documentation and Meeting Updates

The team discussed several topics including network upgrade naming, where Sam confirmed the new tooling will be implemented in the next EIP. They also addressed the rebranding of EIPIP meetings to ACDG, noting there wasn’t strong support for the change, and decided to continue with EIPIP meetings while sharing relevant information with the ACD meeting. Pooja presented a new contributor.md file containing guidelines for EIP documentation, which she created based on Sam’s previous author guidelines, and requested editor review of PRs 11124 and 11125.

### Typo Fix Rules and Scheduling

Pooja and Jochem discussed the need to address an increasing number of typo fixes in their project, with over 93 out of 400 issues being typographical errors. They agreed to establish stricter rules for handling such fixes to improve efficiency. Additionally, they touched on the scheduling of office hours and the need to update contributor documentation while reducing frequent updates to EIP1.

### Contributor Recognition and PR Handling

The meeting focused on addressing issues related to contributor recognition and PR handling in EIPs and ERCs. Zainan suggested implementing a contributor metadata line in headers to allow authors to credit non-authors, while Carson emphasized the need to balance incentivizing participation with avoiding overcrediting trivial fixes. Sam and Pooja discussed the challenges of reviewing typo and formatting fixes, with Sam explaining the trade-offs of combining multiple PRs. The group agreed to review pending PRs and consider enhancing contributor guidelines. Pooja also highlighted January’s progress, including 9 new EIPs and 3 new ERCs, and announced the next meeting on February 17th.

