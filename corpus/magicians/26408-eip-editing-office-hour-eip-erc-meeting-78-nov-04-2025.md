---
source: magicians
topic_id: 26408
title: EIP Editing Office Hour (EIP + ERC) Meeting #78, Nov 04, 2025
author: system
date: "2025-11-03"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-erc-meeting-78-nov-04-2025/26408
views: 28
likes: 0
posts_count: 3
---

# EIP Editing Office Hour (EIP + ERC) Meeting #78, Nov 04, 2025

### Agenda

Agenda

Editor: [@samwilsn](/u/samwilsn)

### To Final

- Update ERC-7857: Move to Final by Wilbert957 · Pull Request #1284 · ethereum/ERCs · GitHub

### To Last Call

- Update ERC-7930: Move to Last Call by euler0x · Pull Request #1240 · ethereum/ERCs · GitHub
- Update ERC-7634: Move to Last Call by OniReimu · Pull Request #1224 · ethereum/ERCs · GitHub
- Update ERC-7908: Move to Last Call by elizabethxiaoyu · Pull Request #1333 · ethereum/ERCs · GitHub

### To Review

- Update ERC-7893: Move to Review by SeanLuis · Pull Request #1223 · ethereum/ERCs · GitHub
- Update EIP-7495: Move to Review by etan-status · Pull Request #10587 · ethereum/EIPs · GitHub

#### Other

- Update EIP-1186: fix broken links by sashass1315 · Pull Request #10319 · ethereum/EIPs · GitHub
- Update EIP-1485: Removed Broken Ethereum Wiki Link from Documentation by santamasa · Pull Request #10509 · ethereum/EIPs · GitHub

### Force merge & Spam

Spam

- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built

### To Draft

- https://github.com/ethereum/ERCs/pull/1212
- https://github.com/ethereum/EIPs/pull/9374
- https://github.com/ethereum/EIPs/pull/10646
- Add EIP: Prevent consolidation overflow withdrawals by anderselowsson · Pull Request #10654 · ethereum/EIPs · GitHub
- Add EIP: Prevent using consolidations as withdrawals by mkalinin · Pull Request #10656 · ethereum/EIPs · GitHub
- Add EIP: Transaction Inclusion Subscription by LukaszRozmej · Pull Request #10666 · ethereum/EIPs · GitHub
- Add EIP: Precompile for ML-DSA signature verification by simonmasson · Pull Request #10557 · ethereum/EIPs · GitHub
- Add EIP: Precompile for Falcon support by simonmasson · Pull Request #10560 · ethereum/EIPs · GitHub
- Website: Delegatable Utility Tokens for NFTs by shinthom · Pull Request #1196 · ethereum/ERCs · GitHub
- Add ERC: Fixed-Supply Agent NFT Collections by nxt3d · Pull Request #1237 · ethereum/ERCs · GitHub
- Add ERC: Onchain Metadata for Token Registries by nxt3d · Pull Request #1259 · ethereum/ERCs · GitHub
- https://github.com/ethereum/ERCs/pull/1271

## Announcement

Meet editors and authors in [EIP Summit ARG](https://luma.com/5lwboseu)

**Meeting Time:** Tuesday, November 04, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1791)

## Replies

**system** (2025-11-04):

### Meeting Summary:

The meeting began with a discussion of technical Zoom access issues and agenda setting for the EIP Editing Office Hour meeting. The team then reviewed several proposals including NFT interface standards, contract ownership interfaces, and on-chain treasury management, with detailed discussions around code validation, privacy considerations, and documentation improvements. The conversation ended with discussions about proposal categorization and management, including decisions about ERC classification and upcoming EIP events scheduled for November 21st.

**Click to expand detailed summary**

The meeting focused on addressing technical issues with Zoom host permissions and discussing the agenda for the EIP Editing Office Hour meeting. Pooja and Nixo agreed to meet asynchronously to resolve the Zoom access problem, with Nixo explaining that the EFZ Zoom Bot was preventing alternative hosts from being assigned. The meeting then began with Sam Wilson as editor, and Pooja confirmed that authors had joined to discuss EIPs and ERC pull requests, with the agenda including finalizing proposals and reviewing PRs for authors.

The team reviewed a pull request for an NFT interface standard designed for AR agents, which David shared in the chat. Sam confirmed that the Solidity code looked valid and discussed the need for privacy protection in the metadata. Pooja left the meeting briefly, and Sam concluded by asking David if he had any specific questions about his proposal.

The team reviewed a multi-step contract ownership interface proposal, which defines three distinct stages for ownership transfer: initiation by the original owner, confirmation, and acceptance by the new owner. They discussed the importance of an optional time window between initiation and confirmation stages to allow for industry review and key compromise. Sam pointed out a minor grammar issue in the documentation regarding the listing of security assumptions, and the team agreed to update the buffer period specifications and ensure the owner keys interface is properly defined.

Sam and David discussed the rationale section of a proposal, with Sam suggesting improvements to make it more aligned with ERC173 standards. They agreed to fix up the rationale and for Sam to review it later. Pooja mentioned an author approval for proposal 7828, which Sam was also an author of. Sam read through the proposal and noted some grammatical inconsistencies, particularly with the use of plural and singular terms.

Sam and Pooja discussed merging a PR into the last call stage, as the changes were not significant and needed to be completed before the panel. They agreed to change the status of the PR and allow the author time for further iterations. Sam mentioned that as an author, they couldn’t edit the document, so they would add comments instead. They also noted that there were unaddressed comments on another document, which needed attention.

Sam and Pooja discussed the review of a proposal related to on-chain treasury management and secure private key generation. They agreed to move it to last call, noting the presence of various images and core interfaces in the proposal.

Pooja and Sam discussed categorizing a DeFi protocol proposal as an ERC, agreeing it should remain under this broad category to avoid confusion following the EIP-ERC repo split. They noted the proposal’s use of tables and emoji, which Sam attributed to possible ChatGPT assistance for formatting and content generation, though he expressed no objection to using AI tools for proposal development as long as they add value.

The team discussed a proposal related to ownership and key management, with David addressing previous comments and explaining the mechanics of how a compromised owner key would be handled. Sam clarified that if an attacker doesn’t have the owner key, they cannot initiate ownership changes, leading to a potential gas fee battle if the attacker tries to acquire the key. Pooja announced an upcoming EIP Editing Office Hour and EIP Summit on November 21st, where Sam will be available for questions.

### Next Steps:

- Nixo and Pooja: Meet and figure out how to assign Pooja as an alternative host for Zoom so she has access to transcripts and logs
- Pooja and Nixo: Connect async to solve the host issue permanently, hopefully by next week
- David: Address the rationale section by moving some content and doing nitpicking as discussed with Sam
- Sam: Review David’s proposal  after fixes are made
- Sam: Merge the proposal that is moving from draft to last call  and add comments since he is an author and cannot edit it directly

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: iaHDaR7%)
- Download Chat (Passcode: iaHDaR7%)

---

**system** (2025-11-04):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=bmBzItd6Tgw

