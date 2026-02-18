---
source: magicians
topic_id: 24819
title: AllWalletDevs | call #35 | August 20th, 2025
author: system
date: "2025-07-16"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/allwalletdevs-call-35-august-20th-2025/24819
views: 59
likes: 0
posts_count: 3
---

# AllWalletDevs | call #35 | August 20th, 2025

# AllWalletDevs, call #35, August 20, 2025

- August 20, 2025, 17:00 UTC
- https://allwallet.dev

# Agenda

- Wallet API Documentation (MDN-like dev resource)
- metamask-improvement-proposals/MIPs/mip-6.md at main · MetaMask/metamask-improvement-proposals · GitHub
- ERC-7920

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : All Wallet Devs
- Occurrence rate : monthly
- Already a Zoom meeting ID : false # Set to true if you bring your own link – WARNING the bot will not create a zoom ID and a summary or a Youtube video – (make sure your zoom link meeting is auto recording you’ll have to handle this yourself)
- Already on Ethereum Calendar : false # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- Need YouTube stream links : true # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : true # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1625)

## Replies

**system** (2025-08-21):

### Meeting Summary:

The meeting covered discussions about wallet development standards and documentation, with presentations on new proposals for chain-agnostic standards and batch off-chain signatures. The team explored various technical implementations including gas limit hints for EIP-4792 and a server API for wallet signing, while also discussing the benefits of structured data for “Sign in with Ethereum.” The conversation ended with plans to further develop these proposals and explore their potential interactions with existing standards.

**Click to expand detailed summary**

The meeting focused on several topics related to wallet development and standards. Sam Wilson introduced a new project to create an MDN-like resource documenting wallet APIs, and Alex from MetaMask presented on MIP-6, a proposal for chain-agnostic standards that MetaMask has been implementing. Sola discussed EIP-7920, a proposal she had drafted several months ago, and requested feedback to move it into formal review. The conversation ended with Alex providing links to relevant resources and inviting further engagement on the discussed proposals.

Sola presented ERC-7920, a standard for batch off-chain signatures that builds on top of EIP-712, allowing users to sign multiple messages in one signature. The standard provides benefits like single signature verification, human-readable format, and compatibility with EIP-712 signatures, while also being backwards compatible. Sola discussed various use cases including gas-free DeFi decks, wallet sign-ins, and pre-configurations for trading. The community discussed potential interactions with other standards like EIP-1271 and super transactions, with Adam suggesting to explore Byconomy’s work in this area.

Adam Hodges presented a proposal to add a gas limit hint capability to EIP-4792, allowing apps to specify gas limits for individual calls made by wallets. The proposal aims to address issues with gas estimation and usage in complex transactions, particularly for decentralized exchanges and smart contracts. While the idea received support from the group, there was discussion about terminology, with Ivo suggesting “gas limit hint” over “gas limit override” to better reflect the optional nature of the feature. The team agreed to further explore the use cases and implementation details, with Adam planning to work on a prototype for the Server Wall API.

The meeting focused on discussions about Ethereum Request for Comments (ERCs) and their implementations. Adam Hodges introduced a draft specification for a server API for wallet signing, which would allow apps to use session keys without handling transaction preparation. The group also discussed the potential benefits of using structured data (ERC-7836) instead of plain text for “Sign in with Ethereum,” with Ivo highlighting advantages like better localization and accessibility. Orest inquired about the value of splitting terms and conditions signatures, which Ivo explained was due to limitations in the Ethereum proposal’s message structure. The conversation ended with Ivo planning to open a thread about the structured data proposal on the Magicians forum.

### Next Steps:

- Wallet developers to review and provide feedback on MIP-6 and CAPE-25 standards.
- Wallet developers to engage in the CASA Discord for discussions on chain-agnostic standards.
- Sola to seek formal reviewers for ERC-7920 .
- Wallet developers to review and provide feedback on Adam Hodges’ proposal for gas limit override capability in ERC-5792.
- Adam Hodges to consider renaming “gas limit override” to “gas limit hint” in the proposal.
- Adam Hodges to reconsider the restriction of requiring gas hints on all calls in a batch for ERC-5792.
- Wallet developers to review and provide feedback on ERC-7836 .
- Ivo to further explore the possibility of updating Sign-In with Ethereum to use EIP-712 instead of plain text.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: Ace9!YQB)
- Download Chat (Passcode: Ace9!YQB)

---

**system** (2025-08-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=pX8ATiNNAsU

