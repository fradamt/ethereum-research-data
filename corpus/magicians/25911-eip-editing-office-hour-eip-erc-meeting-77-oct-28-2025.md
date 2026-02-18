---
source: magicians
topic_id: 25911
title: EIP Editing Office Hour (EIP + ERC) Meeting #77, Oct 28, 2025
author: system
date: "2025-10-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-erc-meeting-77-oct-28-2025/25911
views: 27
likes: 0
posts_count: 3
---

# EIP Editing Office Hour (EIP + ERC) Meeting #77, Oct 28, 2025

### Agenda

Editor: [@xinbenlv](/u/xinbenlv)

#### To Final

- Update ERC-7857: Move to Final by Wilbert957 · Pull Request #1284 · ethereum/ERCs · GitHub

#### To Last Call

- Update ERC-7930: Move to Last Call by euler0x · Pull Request #1240 · ethereum/ERCs · GitHub
- Update ERC-7634: Move to Last Call by OniReimu · Pull Request #1224 · ethereum/ERCs · GitHub

#### To Review

- Update ERC-7518: Move to Review by rajatwasan · Pull Request #1204 · ethereum/ERCs · GitHub
- Update ERC-7893: Move to Review by SeanLuis · Pull Request #1223 · ethereum/ERCs · GitHub
- https://github.com/ethereum/ERCs/pull/1014  (close? as the EIP is already in Review)

### Force merge

*TBA*

#### To Draft

- https://github.com/ethereum/ERCs/pull/1212
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

## Announcement

- Meet editors and authors in EIP Summit ARG

**Meeting Time:** Tuesday, October 28, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1776)

## Replies

**system** (2025-10-29):

### Meeting Summary:

The meeting focused on reviewing multiple Ethereum Improvement Proposals and ERC pull requests, with discussions centered around technical implementations and functionality details. The team examined specific proposals including an ERC20 pre-initialization extension with Sentinel storage and a bond system implementation, with detailed technical reviews and feedback provided by participants. The conversation ended with updates about an upcoming EIP Summit and the scheduling of the next review meeting.

**Click to expand detailed summary**

The meeting focused on reviewing and discussing Ethereum Improvement Proposals (EIPs) and ERC pull requests. Victor, the editor, joined to review proposals, starting with PR 1158 by German, who was present in the meeting. German’s proposal had been in the draft stage for some time and was ready for merging. Pooja mentioned that the proposal would be discussed once the editor was available. The meeting also addressed Rajat’s ongoing work on ERC-7518, which was still in progress and awaiting further review. The agenda for the meeting was shared, and participants were encouraged to share their PR links in the chat for review.

Zainan and German discussed a proposal for an ERC20 pre-initialization extension with Sentinel storage. German explained the implementation, which involves pre-loading storage with a magic value represented as a byte32 string to save gas. They explored how the system would handle token transfers and balances, with German clarifying that the magic value effectively disappears when performing arithmetic operations. Zainan requested to see a demonstration of the proposed system’s functionality, including a failure scenario, which German agreed to provide.

The team discussed a proposal review, with Zainan and Jon examining the technical aspects of an ERC implementation. Jon explained that the bond system works as a negative consequence for incorrect answers, with stakes being removed if agents provide wrong responses. The discussion focused on whether certain features could be optional, with Jon confirming that none of the core components could be omitted. Pooja mentioned that the author, John, was present for the review of PR number 1226, and the team agreed to prioritize the review once German completes certain transactions.

The meeting focused on reviewing and refining an ERC (Ethereum Request for Comment) proposal, with Zainan providing detailed feedback on various aspects of the document. Key points included clarifying the bond amount and implementation specifics, discussing judge selection methods, and addressing the need for more detailed specifications around the aggregation and resolution process. The group also touched on the use of different tokens for bonds and rewards, and the importance of providing clear guidance for implementers. German shared test results for a related proposal, which Zainan reviewed and approved. The conversation ended with Pooja announcing an upcoming EIP Summit at DevConnect and reminding participants of the next review meeting on November 4th.

### Next Steps:

- German: Execute four test transactions  and post results in the Ethereum Magicians forum to demonstrate math works correctly
- German: Address bot failures in the PR
- Victor : Review German’s test transaction results once posted and complete the merge review for ERC-8003
- John: Rephrase the bond definition sentence to separate the definition from implementation-specific details
- John: Clarify whether deadline timestamp uses Unix epoch or block number, and declare if it’s implementation-specific
- John: Include dispute process in the core flow overview section
- John: Clarify what token the bond accepts  and update the payable function documentation accordingly
- John: Add bond token address to the request struct if allowing different tokens for bond and reward
- John: Clarify what “must auto count” means using Solidity code demo
- John: Clarify how to handle the case when Judge Agent believes Info agents need to be overwritten
- John: Answer whether Judge Agent can override the majority of votes and clarify the aggregate function logic
- Victor : Complete the remaining review of ERC-8033  in a future session
- Rajat: Complete work on feedback for ERC-7518 and notify when ready for editor review

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 1E?ttp%F)
- Download Chat (Passcode: 1E?ttp%F)

---

**system** (2025-10-29):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=GiOfi_hFSVc

