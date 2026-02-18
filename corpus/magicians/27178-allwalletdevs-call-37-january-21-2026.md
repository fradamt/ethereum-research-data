---
source: magicians
topic_id: 27178
title: AllWalletDevs, call #37, January 21, 2026
author: system
date: "2025-12-15"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/allwalletdevs-call-37-january-21-2026/27178
views: 43
likes: 0
posts_count: 3
---

# AllWalletDevs, call #37, January 21, 2026

### Agenda

- ERC-8092: Associated Accounts
- ERC-8117: Compress Address Format
- Pretty Safe - Vanity Address Mining

**Meeting Time:** Wednesday, January 21, 2026 at 18:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1846)

## Replies

**system** (2026-01-21):

### Meeting Summary:

The 37th AllWalletDevs meeting marked a shift to on-demand calls and included presentations on associated accounts, address compression formats, and display innovations. The group discussed specifications for blockchain account associations, including validation flows and potential improvements to the system. Various proposals were shared for improving wallet security and transaction optimization, including new EIPs for account abstraction and address verification.

**Click to expand detailed summary**

The 37th AllWalletDevs meeting was held, marking a shift to on-demand calls instead of monthly meetings. Sam introduced the first agenda item, associated accounts, and mentioned that a Zoom account would be provided to Sam Wilson after the call. Zainan planned to present EIP-8117 (Compressed Display Format for Addresses) and PrettySafe.xyz during the meeting.

Steve Katzman presented the associated accounts specification, explaining how two blockchain accounts can agree on a shared payload and sign to create an association object. He discussed the structure of association records, key types, and validation flows, noting that the specification is chain-agnostic and can be used for various applications like subaccounts, authorization delegation, and asset dashboarding. The group discussed potential improvements to the specification, including using contract addresses for validation logic instead of key IDs and encoding directionality in the data field. Victor presented a new ERC for compressing long strings of digits in contract addresses to improve user experience and prevent spoofing attempts.

Zainan presented a proposal for displaying wallet addresses using GPU mining to create addresses with leading zeros, making it harder for attackers to spoof addresses. The system would be optional and could be implemented by wallets, with the main benefit being improved user security through easier verification of addresses. Chris then shared a new EIP proposal for account abstraction that aims to optimize transactions by removing some of the complexity of native EIP-437 transactions, while maintaining security through a simplified configuration system. The proposal includes support for delegated keys and native token payments, though it sacrifices some flexibility compared to the original EIP-437 design.

### Next Steps:

- Katzman: Review EIP 7779 specification and provide comments on differences with ERC 8092 in the Ethereum Magicians Forum or Telegram chat
- Katzman: Consider replacing key ID schema with contract-based validation logic  as suggested by Sam
- Katzman: Revisit lexicographical sorting for initiator/approver ordering and document the rationale for the current approach in the spec
- Katzman: Add rationale section explaining why lexicographical sorting was removed from earlier drafts
- Katzman: Explore including validator/storage location in the association record as suggested in the ERC 8092 Telegram chat
- Victor : Seek feedback and collaboration from wallet teams on ERC for compressed address display format
- Chris: Continue conversation about the new account abstraction proposal  in Discord thread
- Chris: Share the GitHub link and detailed proposal in Discord for community review

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 4adhy&&Z)
- Download Chat (Passcode: 4adhy&&Z)
- Download Audio (Passcode: 4adhy&&Z)

---

**system** (2026-01-22):

YouTube recording available: https://youtu.be/nWSn_BJaFIc

