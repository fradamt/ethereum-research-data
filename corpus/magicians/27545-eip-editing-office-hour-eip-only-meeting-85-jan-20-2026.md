---
source: magicians
topic_id: 27545
title: EIP Editing Office Hour (EIP Only) Meeting #85, Jan 20, 2026
author: system
date: "2026-01-20"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-only-meeting-85-jan-20-2026/27545
views: 22
likes: 0
posts_count: 2
---

# EIP Editing Office Hour (EIP Only) Meeting #85, Jan 20, 2026

### Agenda

Meeting Link: [Zoom](https://us02web.zoom.us/j/84392811311?pwd=aStRRC9UZnZQbmFqbFh6T2NraFNYQT09)

Editor - @g11tech

## To Final

- Update EIP-7934: Move to Final by poojaranjan · Pull Request #11112 · ethereum/EIPs · GitHub
- Update Fusaka EIP: Move to Final by poojaranjan · Pull Request #11113 · ethereum/EIPs · GitHub

## To Last Call

## To Review

## Misc.

- Fix minor typos in EIP documentation by katikatidimon · Pull Request #11115 · ethereum/EIPs · GitHub
- chore: Remove redundant minima theme dependency from Gemfile #10966
- chore: Remove redundant minima gem dependency from Gemfile #11042
- chore: remove non-existent LICENSE entry from Jekyll config #11096
- chore(config): remove obsolete include directive #11098
- chore(config): remove non-existent template exclusions from Jekyll config #11100
- Update EIP-1682: two typos #10792

## To Draft

- Update EIP-7843: Move to Draft by Marchhill · Pull Request #11083 · ethereum/EIPs · GitHub
- Update EIP-7954: Move to Draft by benaadams · Pull Request #11116 · ethereum/EIPs · GitHub
- Add EIP: MEVless Protocol #10855
- Add EIP: Temporary Contract Storage #11081
- Add EIP: MLOAD8 and CALLDATALOAD8 Opcodes #11038

### Other

PRs from [EIP Boards](https://eipsinsight.com/boards)

**Meeting Time:** Tuesday, January 20, 2026 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1884)

## Replies

**poojaranjan** (2026-01-20):

AI Notes

Meeting summary

## Quick recap

The meeting focused on reviewing EIP-related items, including submissions, approvals, and merging issues, with discussions on CI errors and authoring system changes. The team addressed concerns about typo PRs and the need for increased editor permissions to reduce the number of open PRs, while also discussing changes to author handles and the approval process for second authors. The conversation ended with updates on PR reviews and a plan to add a “Force Merge” label for better categorization in future meetings.

## Next steps

- Pooja: Follow up with the authors of the two remaining EIPs (related to PR 111113) for their approval; if approval is received and the PR is still blocked, resurface the PR for further discussion.
- Pooja: Bring EIP 7951 CI error to Sam’s attention in tomorrow’s meeting.
- Pooja: Add agenda item for tomorrow’s meeting to discuss CI flagging issues for asset changes, so that CI flags the author (not the editor) for changes in draft or other appropriate stages.
- Pooja: Add agenda item for tomorrow’s EIP meeting to discuss granting force merge access to editors (Gajinder and/or new editor) and reducing open typo PRs.
- Pooja: Add agenda item for tomorrow’s EIP meeting to discuss tracking both “to-do” markers and plain “TBD” text in EIPs for better automation and less back-and-forth with authors.
- Pooja: Add agenda item for tomorrow’s EIP meeting to discuss implementing a “Force Merge” label for PRs that require force merge, to help editors categorize and process such PRs more efficiently.
- Pooja: Leave a comment on the PR where Ben is changing the author handle, asking the second author (Julio) to approve the change.

## Summary

### EIP Editing Office Hour Preparation

The meeting began with Pooja and Gajinder discussing the setup for screen sharing and reviewing the agenda for the EIP Editing Office Hour. They confirmed that the meeting would focus on EIP-related items and that Gajinder had already reviewed most of the agenda. Pooja mentioned that a few additional items had been added, and the meeting was set to start in a minute.

### EIP Submission and Approval Status

Pooja reported that 4-5 EIPs had been submitted, with 3 receiving approval, though one (EIP 7951) was failing to merge. Gajinder inquired about the status of EIP 7951, and Pooja suggested checking the editor approval status, noting that Gajinder had editor privileges.

### CI Error Resolution Discussion

Pooja and Gajinder discussed a CI error that prevented merging an EIP, despite author approval. They agreed to re-trigger the CI and bring the issue to Sam’s attention the next day. Pooja also planned to follow up with the authors of two other EIPs that were blocked, and they decided to move forward with miscellaneous PRs while waiting for the CI issue to be resolved.

### Authoring System CI Flag Issues

Gajinder and Pooja discussed changes to the authoring system, focusing on CI flags that incorrectly notify editors instead of authors for draft-stage changes. They agreed to move these CI-related issues to the next day’s meeting, as they are causing unnecessary delays for authors and adding to the large number of open PRs. They also decided to have Sam review the website rendering issues that were raised.

### Resolving Typo PR Accumulation

Gajinder and Pooja discussed the issue of typo PRs piling up in the system, with Gajinder suggesting that either he or Pooja should be granted force merge capabilities to quickly dispose of these unnecessary PRs. Pooja confirmed that she had previously raised this issue in an EIP meeting, where it was suggested that Sam would check with the Ethereum Foundation team about granting additional access to editors. Both agreed that increasing permissions for existing editors could help reduce the number of open PRs.

### Author Handle Change Review

The team discussed a change in author handle for a draft, with Gajinder and Pooja examining whether the new handle belongs to the same author. They determined that while Ben had approved the change, another review would be needed from Gileo, and Ben might not be able to approve the change himself since he created it. Pooja suggested leaving a comment for Ben to clarify the situation.

### MEVS Protocol EIP Approval

Gajinder and Pooja discussed the approval process for a second author and confirmed that Julio could handle it. They also mentioned that a new EIP for the MEVS protocol had been merged. Arthur completed a task requested by Gajinder, and Pooja noted that the PR was now cleared after Gajinder’s review. Gajinder added a small nit to the PR, requesting a to-do marker be added.

### PR Merging and TBD Tracking

Gajinder and Pooja discussed merging a PR and the importance of using HTML to-do markers for TBD items in proposals to help track progress. They agreed to add a discussion about tracking TBD items without markers to the next EIP IP meeting. Pooja noted that many PRs are waiting for author approval and expressed hope for getting approval on Fusaka proposals to move them to final status.

### PR Review Process Updates

The team discussed the status of PR reviews, with Gajinder explaining that most PRs were already reviewed before the meeting and only 10 were listed for discussion. Gajinder suggested adding a “Force Merge” label to help categorize PRs that require special handling, which Pooja agreed to add as an agenda item for the next meeting. The conversation ended with an open invitation for questions, but none were raised.

