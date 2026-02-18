---
source: magicians
topic_id: 20186
title: All Core Devs - Execution (ACDE) #189, June 6 2024
author: abcoathup
date: "2024-06-02"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-189-june-6-2024/20186
views: 1158
likes: 0
posts_count: 2
---

# All Core Devs - Execution (ACDE) #189, June 6 2024

### Agenda

[Execution Layer Meeting 189 · Issue #1052 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1052)

Moderator: [@timbeiko](/u/timbeiko)

### Summary

Recap by [@timbeiko](/u/timbeiko)

- After a lot of back and forth, we finalized the Pectra scope ! EOF and EIP-7702 are both included (PR: Update EIP-7600: Add Included EIPs by timbeiko · Pull Request #8627 · ethereum/EIPs · GitHub). To give teams time to work on their EOF implementations and do cross-client testing on everything else in the fork, devnet-1 will not include EOF, but will include all other Pectra EIPs. Notably, we’ll include 7702 even though the spec may still be changed.
- We’re tentatively planning to include the following changes in devnet-1, but will leave a few more days for people to review them prior to merging the PRs:

Update EIP-7251: Add EL triggered consolidations by mkalinin · Pull Request #8625 · ethereum/EIPs · GitHub

engine: Add EL triggered consolidations by mkalinin · Pull Request #554 · ethereum/execution-apis · GitHub
- engine: align WithdrawalRequestV1 with EIP-7002 and consensus spec by nflaig · Pull Request #549 · ethereum/execution-apis · GitHub
- engine: Extend payload bodies with deposit and withdrawal requests by mkalinin · Pull Request #545 · ethereum/execution-apis · GitHub (already merged)

We discussed deactivating EIP-158, as it would cause issues similar to SELFDESTRUCT in a post-Verkle world and EIP-7702 as currently specified could create accounts with 0 nonce/balance/codehash but storage. [@gballet](/u/gballet) will draft a proposal to formally consider the change. If 7702 is tweaked in a way that does not cause this issue, we’d consider it for the Verkle fork.
[@pipermerriam](/u/pipermerriam) came on to get a status update on EIP-4444 & portal support by client teams. A few client teams have begun working on this, but flagged that they currently have many competing priorities. The Portal team will keep monitoring ⁠history-expiry to offer help to any client team needing it!
We briefly discussed my proposed ACD/Network Upgrade Process/EthMag change doc ([AllCoreDevs, Network Upgrade & EthMagicians Process Improvements](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157)) and agreed to try the “EIP Review Request” proposal. There weren’t any objections to PFI/CFI/SFI, but given the scope I’ll open a PR for us to discuss before agreeing to the change.
Testing teams proposed a new channel layout for discord (see above)

And, lastly, we flagged the upcoming EPBS (tomorrow) and PeerDAS (June 11) breakouts:

- ePBS breakout room #2 · Issue #1060 · ethereum/pm · GitHub
- PeerDAS Breakout Room #1 · Issue #1059 · ethereum/pm · GitHub

*From Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1248304663904784466)*

### Recording

  [![image](https://img.youtube.com/vi/A5EaPLLRsoQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=A5EaPLLRsoQ&t=180s)

### Additional info

Notes by [@timbeiko](/u/timbeiko): [Tweet thread](https://twitter.com/TimBeiko/status/1798821575162302751)

Notes by [@Christine_dkim](/u/christine_dkim):  [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-execution-call-189-writeup/)

## Replies
