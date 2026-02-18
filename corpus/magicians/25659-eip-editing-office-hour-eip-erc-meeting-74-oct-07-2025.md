---
source: magicians
topic_id: 25659
title: EIP Editing Office Hour (EIP + ERC) Meeting #74, Oct 07, 2025
author: system
date: "2025-10-03"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-erc-meeting-74-oct-07-2025/25659
views: 39
likes: 0
posts_count: 4
---

# EIP Editing Office Hour (EIP + ERC) Meeting #74, Oct 07, 2025

### Agenda

Editor: [@SamWilsn](/u/samwilsn)

### To Final

- Update ERC-7950: Move to Final by microbecode · Pull Request #1228 · ethereum/ERCs · GitHub
- Update ERC-7291: Move to Final by veenkumarr · Pull Request #1230 · ethereum/ERCs · GitHub
- Update ERC-3009: Move to Draft by petejkim · Pull Request #1241 · ethereum/ERCs · GitHub

### To Last Call

- Update EIP-7607: Move to Last Call by timbeiko · Pull Request #10423 · ethereum/EIPs · GitHub
- Update ERC-7656: Move to Last Call by sullof · Pull Request #1189 · ethereum/ERCs · GitHub

### To Review

- https://github.com/ethereum/ERCs/pull/1243
- Update ERC-7518: Move to Review by rajatwasan · Pull Request #1204 · ethereum/ERCs · GitHub
- Update ERC-7893: Move to Review by SeanLuis · Pull Request #1223 · ethereum/ERCs · GitHub
- Update ERC-2333: Move to Review by CarlBeek · Pull Request #1225 · ethereum/ERCs · GitHub
- https://github.com/ethereum/ERCs/pull/1014

### Misc

- Layout Bugs: 100+ pages on mobile have broken page margins · Issue #10357 · ethereum/EIPs · GitHub & Website: fix broken mobile page margins by ritorhymes · Pull Request #10358 · ethereum/EIPs · GitHub
- Add JSON-LD navigation & breadcrumbs for accessibility · Issue #10098 · ethereum/EIPs · GitHub & Website: add JSON-LD for site nav and breadcrumbs by ritorhymes · Pull Request #10099 · ethereum/EIPs · GitHub
- Distinguish between `h2` and `h3` more obviously · Issue #8546 · ethereum/EIPs · GitHub
- Will I be able to find bugs using AI? · Issue #1199 · ethereum/ERCs · GitHub
- Auto Review Bot Failing on PR #930 — "no artifacts found" Error · Issue #1008 · ethereum/ERCs · GitHub
- https://github.com/ethereum/EIPs/pull/10365

GitHub-Action (Marked `w-stale` but not auto closed)

- Update ERC-7726: Move to Review by ruvaag · Pull Request #688 · ethereum/ERCs · GitHub

Force merge

- Update EIP-1108: correct typo in EIP-1108 rationale section by radik878 · Pull Request #10094 · ethereum/EIPs · GitHub
- Update EIP-5792: Fix two typos in EIP by sashass1315 · Pull Request #10132 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/10136
- Update EIP-684: typo by avorylli · Pull Request #10091 · ethereum/EIPs · GitHub
- Update EIP-1108: correct typo in EIP-1108 rationale section by radik878 · Pull Request #10094 · ethereum/EIPs · GitHub
- Update EIP-684: fix grammar in eip 684 by RenanSouza2 · Pull Request #10115 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/10146
- Update EIP-1283: fix grammatical issues by Fibonacci747 · Pull Request #10162 · ethereum/EIPs · GitHub
- Update EIP-695: fix typo in specification text by Snezhkko · Pull Request #10167 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/10049
- Update EIP-7636: fix typo by hawkadrian · Pull Request #10271 · ethereum/EIPs · GitHub
- Update EIP-908: Fix typo by keeghcet · Pull Request #10312 · ethereum/EIPs · GitHub
- Update EIP-2025: fix typo in EIPS/eip-2025.md by CreeptoGengar · Pull Request #10326 · ethereum/EIPs · GitHub
-

(Spam?)

- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- Pending tasks for ERC migration · Issue #1 · ethereum/ERCs · GitHub (When can we close this Issue?)
- https://github.com/ethereum/EIPs/pull/10316

### To Draft

- Add EIP: P256 transaction support by SirSpudlington · Pull Request #10373 · ethereum/EIPs · GitHub
- Add ERC: Universal Compliance Router for RWA's by deepanshu179 · Pull Request #1087 · ethereum/ERCs · GitHub
- Add EIP: P256 transaction support by SirSpudlington · Pull Request #10373 · ethereum/EIPs · GitHub
- Add EIP: State Creation Gas Cost Increase by misilva73 · Pull Request #10486 · ethereum/EIPs · GitHub

**Meeting Time:** Tuesday, October 07, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1752)

## Replies

**system** (2025-10-07):

### Meeting Summary:

The meeting focused on reviewing multiple pull requests related to Ethereum Improvement Proposals (EIPs) and ERCs, with participants discussing technical details and making decisions on proposal statuses. The group reviewed various proposals including replacements for withdrawn EIPs, discussed implementation details for ERCs and multi-party agreements, and addressed issues related to cryptography and licensing. The conversation ended with discussions about merging pull requests, handling authorship cases, and streamlining work within the GitHub UI, with participants making decisions on proposal approvals and technical implementations.

**Click to expand detailed summary**

The meeting focused on reviewing several pull requests related to Ethereum Improvement Proposals (EIPs) and ERCs. Pooja requested participants to share specific PR links, and Kwame provided a link for PR 1243, which Pooja agreed to add to the agenda. An unknown speaker discussed PR 1230, explaining it was a replacement for the withdrawn EIP 7980 with a different backing algorithm. Sam joined the meeting later, and the group began reviewing the pull requests.

The EIP Editing Office Hour meeting reviewed proposals and PRs from GitHub repositories, with one proposal moving to final standard status. Kumar’s proposal (PR 1230) was approved, while another proposal (PR 1243) was moved to review status. The meeting also discussed handling miscellaneous items, spam, and adding new drafts.

The meeting focused on reviewing a technical proposal related to ERCs and multi-party agreements, with Sam providing detailed feedback on various aspects including intent specifications, acceptance mechanisms, and error handling. Sam suggested purging nonces and proposed using deterministic hashtags, while also discussing the implementation of typed data hashes and agent IDs. Pooja then mentioned that a new PR had been submitted to the EIP GitHub repository (10373) as a potential replacement for a previously withdrawn proposal, noting that one participant was unable to speak due to microphone issues.

Sam and Pooja discussed a withdrawn EIP (number 7980) and its replacement, with Pooja noting that the author might have developed better ideas. Sam mentioned he would open a bug report due to an issue with the rendered document. They reviewed a list of scams and discussed an EIP related to P256 support, including its algorithm type and signature verification steps. Sam acknowledged that he couldn’t read the cryptography code but confirmed the details were correct.

Sam and Pooja discussed finalizing proposals, focusing on updating an old EIP (3009). They reviewed its history and considered moving it from the draft stage to final, but decided to return it to its original status for further updates. They also touched on encoding chain IDs and transaction hashes, as well as the MIT license for SWCs.

Sam and Pooja discussed the status of SWCs and their acceptance as links. They clarified that SWCs that are not actively maintained cannot be part of the accepted links, even if a proposal is made. Sam approved a design for a project, mentioning the need for subheadings and a discussions section. They also briefly touched on the progress of another project, with Sam planning to leave a comment.

Pooja and Sam discussed a unique case involving authorship and whether to use an older or newer work, with Sam suggesting that the authors could withdraw the newer one if they preferred the older. They also explored the possibility of creating a browser extension to streamline their work within the GitHub UI.

Sam and Pooja discussed merging pull requests, with Sam identifying and fixing an issue related to CloudCo’s inability to handle EP Validator. They reviewed several pull requests, including one that needed to go to last call, which Sam updated and approved. Sam also reviewed another pull request related to a generalized contract for services, finding it acceptable with some minor adjustments. The conversation ended with Sam thanking everyone for their participation.

### Next Steps:

- Sir to continue work on the new PR #10373 as a replacement for withdrawn EIP-7980.
- Kwame to continue working on updates for PR #1243 while it’s in review status.
- Authors of ERC-3009 to decide whether to proceed with the original proposal or the newer ERC-7758 version, and withdraw one if necessary.
- Sam to follow up on the bug report regarding withdrawn proposals not showing properly in rendered view.
- Sam to check if the browser extension for running EAPW inside GitHub UI can be developed.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: GUn?7eiP)
- Download Chat (Passcode: GUn?7eiP)

---

**system** (2025-10-07):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=THKxFCBPQ04

---

**poojaranjan** (2025-10-11):

Summary [Tweet thread](https://x.com/poojaranjan19/status/1975561757771882579).

