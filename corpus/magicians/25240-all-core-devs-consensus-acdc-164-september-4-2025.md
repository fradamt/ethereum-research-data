---
source: magicians
topic_id: 25240
title: All Core Devs - Consensus (ACDC) #164, September 4, 2025
author: system
date: "2025-08-25"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-164-september-4-2025/25240
views: 209
likes: 3
posts_count: 5
---

# All Core Devs - Consensus (ACDC) #164, September 4, 2025

### Agenda

- Fusaka

devnet-3: syncing issues, anything to discuss?
- next steps on devnet-5
- Protocol Upgrade Process and testnets

**Meeting Time:** Thursday, September 04, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1700)

## Replies

**abcoathup** (2025-08-26):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #164, September 4, 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-164-september-4-2025/25240/5) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #164 Summary
> fusaka-devnet-3
>
> Multiple client issues identified across devnet
> Barnabas compiled comprehensive feedback document from all client teams
>
> https://notes.ethereum.org/@ethpandaops/fusaka-syncing-bugs
>
>
> Recent fixes reported:
>
> Lighthouse bug(s) fixed on unstable branch
> Prysm ready to use trunk
> Teku still working on RPC issues
>
>
> Next steps for fusaka-devnet-3
>
> Target Monday for all code on trunk branches
> Target near 100% participation recovery once fixes are deployed
> Run another …

### Recordings/Stream

- YouTube
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDC Call #164 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]: syncing issues
- Consensus layer client team merge to trunk branches status
- Proposed changes to upgrade process by @timbeiko - (14 days between client releases & upgrading first testnet, 10 days between testnet upgrades and 30 days between upgrading last testnet & mainnet)

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists

---

**system** (2025-09-04):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: OZ=d32*w)
- Download Chat (Passcode: OZ=d32*w)

---

**system** (2025-09-04):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=wF0gWBHZdu8

---

**ralexstokes** (2025-09-04):

**ACDC #164 Summary**

`fusaka-devnet-3`

- Multiple client issues identified across devnet
- Barnabas compiled comprehensive feedback document from all client teams

https://notes.ethereum.org/@ethpandaops/fusaka-syncing-bugs

Recent fixes reported:

- Lighthouse bug(s) fixed on unstable branch
- Prysm ready to use trunk
- Teku still working on RPC issues

Next steps for `fusaka-devnet-3`

- Target Monday for all code on trunk branches
- Target near 100% participation recovery once fixes are deployed
- Run another non-finality test for 1-2 days to confirm fixes

`fusaka-devnet-5` planning

- Will launch with larger scale like devnet-4
- Launch contingent on successful devnet-3
- Broader Fusaka timeline depends on completing current bug fixes and successful devnet-5 testing

Protocol Upgrade Process Timeline Changes

- Tim proposed modifications to original process document

Update the Protocol Upgrade Process document by timbeiko · Pull Request #1715 · ethereum/pm · GitHub

Key proposed changes:

- Minimum 14 days (down from 30) between client releases and first testnet
- Minimum 10 days between each testnet (ideally closer to 2 weeks)
- Maintain 30-day buffer between client releases and mainnet

Community feedback collected from L2s, LSTs, infrastructure providers who were mostly in favor; check issue for more color
Outstanding concerns:

- Mixed-use nature of testnets (testing vs staging environments)
- Need clearer public feedback from community stakeholders
- Teams need more time to review proposal

Participants had not had time to review in-depth yet, so taking conversation async to issue and will revisit next ACDE

Fusaka Timeline Considerations to note

- Holesky being deprecated allows compressed timeline there
- Sepolia considered primary “real” testnet with full 30-day buffer
- EF PandaOps indicates more extensive shadow fork testing
- Current Fusaka mainnet timeline premature until devnet-3/5 milestones completed

Open discussion

- ModExp gas cost increase breaking a contract from AlignedLayer

Discussion ongoing in Telegram channel

Mario highlighted teams should check Hive test results to ensure they all pass
Reminder: Glamsterdam EIP discussions deferred until Fusaka mainnet release

