---
source: magicians
topic_id: 25797
title: EIP Editing Office Hour (EIP + ERC) Meeting #75, Oct 14, 2025
author: system
date: "2025-10-14"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-erc-meeting-75-oct-14-2025/25797
views: 35
likes: 0
posts_count: 3
---

# EIP Editing Office Hour (EIP + ERC) Meeting #75, Oct 14, 2025

### Agenda

Editor: [@xinbenlv](/u/xinbenlv)

#### To Final

#### To Last Call

- Update ERC-7930: Move to Last Call by euler0x · Pull Request #1240 · ethereum/ERCs · GitHub
- Update ERC-7634: Move to Last Call by OniReimu · Pull Request #1224 · ethereum/ERCs · GitHub

#### To Review

- Update ERC-7518: Move to Review by rajatwasan · Pull Request #1204 · ethereum/ERCs · GitHub
- Update ERC-7893: Move to Review by SeanLuis · Pull Request #1223 · ethereum/ERCs · GitHub
- Update ERC-2333: Move to Review by CarlBeek · Pull Request #1225 · ethereum/ERCs · GitHub
- Update ERC-7936: Move to Review by monperrus · Pull Request #1242 · ethereum/ERCs · GitHub
- https://github.com/ethereum/ERCs/pull/1014  (close? as the EIP is already in Review)

GitHub-Action (Marked `w-stale` but not auto closed)

- Update ERC-7726: Move to Review by ruvaag · Pull Request #688 · ethereum/ERCs · GitHub

Force merge

- Update EIP-2025: fix typo in EIPS/eip-2025.md by CreeptoGengar · Pull Request #10326 · ethereum/EIPs · GitHub

#### To Draft

- Add ERC: Diamond Storage by mudgen · Pull Request #1250 · ethereum/ERCs · GitHub
- Add ERC: Universal Compliance Router for RWA's by deepanshu179 · Pull Request #1087 · ethereum/ERCs · GitHub
- https://github.com/ethereum/ERCs/pull/1226
- Add ERC: Non‑Fungible Account Tokens by mikelxc · Pull Request #1101 · ethereum/ERCs · GitHub
- https://github.com/ethereum/ERCs/pull/1129
- Add ERC: Universal Compliance Router for RWA's by deepanshu179 · Pull Request #1087 · ethereum/ERCs · GitHub
- https://github.com/ethereum/ERCs/pull/1129
- Add ERC: Verifiable ML Model Inference (ZKML) by aryaethn · Pull Request #1133 · ethereum/ERCs · GitHub
- Add ERC: Oracle-Permissioned ERC-20 with ZK Proofs by chadxeth · Pull Request #1062 · ethereum/ERCs · GitHub
- Add ERC: Operator contract for non delegated EOAs by marcelomorgado · Pull Request #1148 · ethereum/ERCs · GitHub
- Add ERC: Pre-delegated Signature Verification by jxom · Pull Request #1186 · ethereum/ERCs · GitHub
- Add ERC: ERC-20 Pre-initialization (Sentinel Storage) by ariutokintumi · Pull Request #1158 · ethereum/ERCs · GitHub
- Add ERC: Minimal Avatar Smart Wallet (MASW) by MostafaS · Pull Request #1118 · ethereum/ERCs · GitHub

**Meeting Time:** Tuesday, October 14, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1761)

## Replies

**system** (2025-10-15):

### Meeting Summary:

Pooja and Zainan coordinated the technical setup and agenda for an Ethereum PM EIP Editing Office Hour meeting, where they reviewed and discussed various proposals in different stages of review. The team evaluated several pull requests, including proposals for new standards, storage patterns, and fractionalized stations, while addressing issues with draft proposals and the review process. They concluded by discussing the status of pending drafts, review comments, and merging processes, with plans to continue reviewing proposals in the next session.

**Click to expand detailed summary**

Pooja and Zainan prepared for a screen-sharing session during an Ethereum PM EIP Editing Office Hour meeting. They discussed technical setup details, including recording and streaming arrangements, and confirmed the agenda was shared via a GitHub issue link. The meeting officially began with Pooja welcoming participants and noting that several proposals were in various stages of review, including some in last call status.

The meeting focused on discussing a peer review process for a draft proposal. Zainan and Pooja identified several issues with the request, including the author not being present on the call, the proposal skipping the review stage, and the need for authors’ approval before status changes. They decided to reject the request and send it back to the author, emphasizing that draft proposals should move from draft to review before going to last call, with exceptions only granted by the EIP editors.

Zainan suggested that the PR could be caught by the EIP review bot to automate the review process and save time. Pooja agreed and mentioned that they had to stop using checkboxes due to the ACD bot triggering multiple messages. They discussed the need for more explanation in the EIP regarding transfer limits and counts, with Zainan identifying several ambiguous terms and unanswered questions. They decided to leave the editorial feedback to the author for further action.

Pooja and Zainan discussed moving forward with a proposal (PR 1204) to be reviewed, focusing on fractionalized stations and existing ERCs. Zainan raised questions about partitioning RAP tokens and the need for best practice suggestions, while Pooja mentioned that Sam previously maintained similar lists. They agreed to research existing ERCs, consider adopting or disregarding them, and create a rationale for their decision.

The team reviewed two pull requests: PR 1250, which proposes a new proposal by Marjan (author of Diamond) and is awaiting review, and PR 1226, which introduces a change to Solidity Compiler enabling new storage patterns. Zainan approved PR 1226 with conditions to satisfy the validator, noting that the proposal could be merged while still in draft status. The team discussed the rapid increase in EIP numbers and considered starting to assign numbers only when proposals move to draft status, though they decided against it due to the quick pace of number allocation.

Pooja and Zainan reviewed two proposals (PR 1225 and PR 1242) and decided to move them into the review status. Zainan noted that PR 1225 needed some section changes and PR 1242 required a technical review by Nick March.

Pooja and Zainan discussed PRs related to EIP/ERC status updates. They identified that PR 1014 to move ERC4337 to review status was already merged, and agreed to either close this PR or update the branch if there were additional changes. Zainan emphasized the importance of keeping branches up to date to avoid review issues, and suggested providing comments to authors about next steps when PRs are out of date.

Pooja and Zainan discussed the status of several pending drafts, focusing on PR number 1087 for the Universal Compliance Router and PR number 1101 for Nonfungible Account Token. They noted that both drafts had received editor recommendations but had not been viewed by the author. Zainan checked the numbering and confirmed the correct assignments, mentioning that these issues should be easily caught by the bot. They also briefly discussed the potential for community interest in implementing the ERC-7210 standard and leaving security as a dropped topic.

The team discussed the status of review comments and merging drafts, with Zainan checking for updates. They explored the functionality of non-fungible tokens and ERCs, considering the need for new contracts and account addresses. Pooja thanked Victor for reviewing proposals and announced that the Editing Office Hour would return next week with more PRs for review.

### Next Steps:

- Teddy to correct the PR that attempted to move a proposal directly from draft to last call, as it should go through review first.
- Victor to provide feedback to Sam and C about automating the detection of blocking conditions in PRs through EIP review bot.
- Nick Mudge to fix the issues identified in PR #1250 for the Diamond proposal.
- Authors of PR #1014  to either sync their branch or close the PR if there are no other major updates since the proposal is already in review status.
- Victor to file feature requests for the EIP bot to catch common issues like branch being out of date.
- Authors of Universal Compliance Router  to demonstrate community interest in adopting their proposal.
- Authors of Non-fungible Account Token  to address Victor’s feedback about whether the functionality could be achieved by simply adopting ERC-721.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: .f8w5a@r)
- Download Chat (Passcode: .f8w5a@r)

---

**system** (2025-10-15):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=eZPjR4OYBSg

