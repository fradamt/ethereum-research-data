---
source: magicians
topic_id: 27612
title: EIP Editing Office Hour (EIP + ERC) Meeting #87
author: system
date: "2026-01-28"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-editing-office-hour-eip-erc-meeting-87/27612
views: 8
likes: 1
posts_count: 2
---

# EIP Editing Office Hour (EIP + ERC) Meeting #87

### Agenda

Editor - [@samwilsn](/u/samwilsn)

Meeting Link: [Zoom](https://us02web.zoom.us/j/84392811311?pwd=aStRRC9UZnZQbmFqbFh6T2NraFNYQT09)

## To Final

- Update ERC-7656: Move to Final by sullof · Pull Request #1413 · ethereum/ERCs · GitHub (Force Merge)

## To Last Call

- Update ERC-8034: Move to Last Call by richard-620 · Pull Request #1492 · ethereum/ERCs · GitHub

## To Review

- Update ERC-8019: Move to Review by Ivshti · Pull Request #1484 · ethereum/ERCs · GitHub

## Misc.

Force Merge

- Update EIP-1965: fix grammar and verb agreement by thuricela · Pull Request #11142 · ethereum/EIPs · GitHub
- Update EIP-2539: Fix grammar and spelling errors in EIP-2539 by andreypryjmak · Pull Request #11177 · ethereum/EIPs · GitHub

Others

- https://github.com/ethereum/EIPs/pull/11124
- Update EIP-1: Update EIP-1 by poojaranjan · Pull Request #11125 · ethereum/EIPs · GitHub
- Add contribute.md to EIP-1 document by poojaranjan · Pull Request #1487 · ethereum/ERCs · GitHub
- Website: Add 'Final' and 'Living' to draft stage conditions by poojaranjan · Pull Request #11198 · ethereum/EIPs · GitHub
- PR & here - Title Renaming by Bot — Bug or Expected Behavior?
- Update EIP-7805: Change author's email by jihoonsong · Pull Request #11224 · ethereum/EIPs · GitHub (Only one author was pinged - Is this a bug or feature?)
- Update EIP-7691: clarify that all 3 EL constants change in Prague by pdobacz · Pull Request #9243 · ethereum/EIPs · GitHub (Requires two authors’ approval - Is this a bug or feature?)
- Update EIP-7723: Update eip-7723.md by poojaranjan · Pull Request #11006 · ethereum/EIPs · GitHub (Thoughts on this process EIP, especially wrt usage of “status” & “stage”)
- Update EIP-8052: Add EIP-7932 to requires header by BitcoinPro9246 · Pull Request #11220 · ethereum/EIPs · GitHub
- Suspicious user?

GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built
- GitHub · Where software is built

### To be closed

- Update EIP-7935: fix discussion URL by skinnypete65 · Pull Request #10973 · ethereum/EIPs · GitHub
- Update EIP-7935: fix typo by jasmylon · Pull Request #10103 · ethereum/EIPs · GitHub
- Update EIP-7910: Add RFC 2119 and 8174 hyperlinks to spec by gap-editor · Pull Request #9679 · ethereum/EIPs · GitHub
- Update EIP-7910: fix wording issues in `activationTime` and `forkId` sections by mdqst · Pull Request #10309 · ethereum/EIPs · GitHub
- Update EIP-7892: Give Blob Parameter Only Hardforks more human names by SamWilsn · Pull Request #10490 · ethereum/EIPs · GitHub (Check with Sam)
- Update README: Update README.md by gitme1-ym · Pull Request #11217 · ethereum/EIPs · GitHub
- Update EIP-7607: Move to Final by MrEeeeet111 · Pull Request #11153 · ethereum/EIPs · GitHub (Superseded by Update EIP-7607: Move to Final by nixorokish · Pull Request #11237 · ethereum/EIPs · GitHub)

## To Draft

EIPs

- Add EIP: Upgrade Nomenclature by poojaranjan · Pull Request #11161 · ethereum/EIPs · GitHub
- Add EIP: Hardfork Meta - BPO1 by poojaranjan · Pull Request #11164 · ethereum/EIPs · GitHub
- Add EIP: Hardfork Meta - BPO2 by poojaranjan · Pull Request #11165 · ethereum/EIPs · GitHub
- Add EIP: Hardfork Meta - BPO3 by poojaranjan · Pull Request #11182 · ethereum/EIPs · GitHub

ERCs

- Add ERC: Onchain Metadata for Token Registries by nxt3d · Pull Request #1259 · ethereum/ERCs · GitHub
- Add ERC: Contract-Level Onchain Metadata by nxt3d · Pull Request #1260 · ethereum/ERCs · GitHub
- Add ERC: Minimal Agent Registry by nxt3d · Pull Request #1463 · ethereum/ERCs · GitHub
- Add ERC: ERC-8127 Human Readable Token Identifiers by nxt3d · Pull Request #1476 · ethereum/ERCs · GitHub
- Add ERC: Forensic Token (Forest) by MASDXI · Pull Request #1256 · ethereum/ERCs · GitHub
- Add ERC: Oracle-Permissioned ERC-20 with ZK Proofs by chadxeth · Pull Request #1062 · ethereum/ERCs · GitHub
- Add ERC: Smart Credential Resolution Interface by nxt3d · Pull Request #1504 · ethereum/ERCs · GitHub

### Other

PRs from [EIP Boards](https://eipsinsight.com/boards)

**Meeting Time:** Tuesday, February 03, 2026 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1906)

## Replies

**poojaranjan** (2026-02-05):

Meeting summary AI

## Quick recap

The Ethereum Improvement Proposal (EIP) Editing Office Hour meeting focused on reviewing pull requests and discussing various EIP-related updates. Editor Sam Wilson and Pooja reviewed several proposals, including EIP 4361 for wallet auto-login, EIP 1965, and contribution guidelines for EIPs. They addressed issues with link references, author approvals, and the distinction between EIP statuses and network upgrade stages. The team also discussed updates to the contribution guidelines and style guide, with plans to add context for AI models. They identified and banned a suspicious user who had submitted numerous inappropriate pull requests. The conversation ended with a review of several other EIPs, including discussions about malicious web content and on-chain metadata for token registries.

## Next steps

- Pooja: Update the contribution guide file name to “CONTRIBUTING.md” in both EIP and ERC repositories, and ensure the style guide improvements are included.
- Pooja: Update the EIP/ERC rendering logic so that “living” and “final” status EIPs do not display a “draft” tag, and implement the appropriate logic (e.g., “or else if” condition) as discussed.
- Pooja: Update the informational EIP about nomenclature by removing/fixing outdated links as highlighted by Sam, and wait for other editors’ review.
- Pooja: Mention to the relevant EIP author that their PR requires an explicit approval (not just a comment) from an author before it can proceed.
- Pooja: Fix links in the Fellowship of Ethereum Magicians documentation and consider adding rationale text to the first BPO for clarity.
- Sam: Take a closer look at the EIP regarding network upgrade stages vs. EIP statuses and provide feedback, particularly ensuring correct usage of “status” and “stage” terminology.
- Pooja: Close/delete all PRs/issues created by the banned user across relevant repositories.
- Premm.eth: Wait for Sam to merge the minimal agent registry PR (after confirming the requested changes are complete). [Note: If merging is Sam’s responsibility, reassign to Sam; context suggests Sam will handle.]
- Sam: Merge the minimal agent registry PR after confirming Premm.eth’s changes (copyright and confusing statement addressed).

## Summary

### EIP Pull Request Review Meeting

The meeting focused on reviewing pull requests for EIP and ERC repositories, with editor Sam Wilson participating. Pooja explained that the call would not be streamed due to technical issues, and they would upload the recording later. The team discussed a force merge that was already approved but couldn’t be merged, with Sam agreeing to investigate the issue. They reviewed a proposal about royalty distribution for referral NFTs and a configurator role, noting some changes that had been made.

### Ethereum Wallet Auto-login Pull Request

Sam and Pooja discussed a pull request related to wallet auto-login functionality for Ethereum sign-ins. They reviewed changes including a local allowlist for automatic signing of ERC-4361 messages, with policies managed by the wallet or user. The discussion concluded with agreement on a merge date of February 17th, noting that another related pull request had already been merged successfully.

### Wallet Auto-login Standards Discussion

The discussion focused on wallet user interface standards, particularly around auto-login authorization flows and domain policy implementation. Sam discussed a technical specification for wallet auto-signing when specific domain conditions are met, and mentioned a bug related to backtick syntax in code fencing. The conversation also touched on cookie handling rules between parent and subdomains, though the exact terminology for this concept remained unclear.

### AI Implementation and Wallet Features

Sam and Pooja discussed the implementation of AI responses and wallet UI features, focusing on user control and default policies for popular applications. They reviewed the rationale for signing with Ethereum and noted that HTTPS should be used for communication. Sam mentioned that they would follow up on certain points later.

### EIP Website and Guidelines Update

Sam and Pooja discussed the status of EIP and ERC website links, confirming that only [eips.etherthereum.org](http://eips.etherthereum.org) is functional, and agreed to maintain the EIP prefix for references despite the ERC website being non-functional. Pooja reported incorporating feedback from Sam and Johan into the contribution guidelines and style guide, which will be revisited after community review.

### Documentation Updates for AI Models

Sam and Pooja discussed improvements to documentation files, including adding context for AI models in claude.md and agent.md files to help with EIPs. They identified a need to update the file name from contribute.md to contributing.md, following the same capitalization as README. Pooja mentioned that they would share the updated file with the community and continue making improvements, while Sam agreed to the changes and noted that similar updates would be needed for the ERC repo.

### Draft Status Update for Ethereum

Sam and Pooja discussed changes to the draft stage conditions for final and living statuses in [eips.ethereum.org](http://eips.ethereum.org). They agreed to remove the draft status for these categories and update the code to reflect this change. Pooja will implement the suggested updates, and Sam will review the output. They also briefly touched on the topic of tailoring renaming and Creed nomenclature, but no decisions were made on these topics.

### EIP Document and Review Process

Pooja discussed an informational EIP and mentioned removing links to upcoming proposals to prevent the document from becoming too extensive. She clarified that the EIP does not recommend future actions but rather summarizes past efforts. Sam confirmed that Tim had created a meta-EIP containing several links, which Pooja used for her document. They also discussed a PR issue where the bot only pinged one author due to GitHub username limitations, and Sam explained that a comment does not count as an approval, clarifying the review process for Pooja.

### Network Upgrade and EIP Stages

Sam and Pooja discussed the importance of distinguishing between network upgrade stages and EIP statuses in a proposal, with Pooja suggesting replacing the term “status” with “stages” where appropriate. They reviewed several pull requests and issues, identifying and addressing concerns related to a problematic user who had been banned from Ethereum repositories. Sam agreed to open and close relevant issues to manage the situation effectively.

### Code Review and Documentation Updates

The team discussed several pull requests and code changes, with Pooja explaining that some items were already addressed in Nixon’s new PR. Sam and Pooja reviewed documentation updates, including the need to fix links and add rationale for parameter changes. Premm.eth made changes to the minimal token registry and minimal agent registry, fixing copyright issues and removing confusing statements. The team agreed to merge several pull requests after addressing outstanding comments, particularly from Johan.

