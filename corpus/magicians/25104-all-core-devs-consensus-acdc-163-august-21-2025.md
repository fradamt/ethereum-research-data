---
source: magicians
topic_id: 25104
title: All Core Devs - Consensus (ACDC) #163, August 21, 2025
author: system
date: "2025-08-14"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-163-august-21-2025/25104
views: 196
likes: 3
posts_count: 6
---

# All Core Devs - Consensus (ACDC) #163, August 21, 2025

### Agenda

- Fusaka

devnet-3 (?), devnet-4 reflections
- devnet-5 plans
- FYI: Set MAX_BLOB_COMMITMENTS_PER_BLOCK minimal preset to 4096 by barnabasbusa · Pull Request #4508 · ethereum/consensus-specs · GitHub
- ForkVersion in BPO design

Glamsterdam

- EIP-7928 breakout announcement
- https://github.com/ethereum/pm/issues/1673#issuecomment-3210713863
- Reminder: other EIP proposals for Glamsterdam should be made by Fusaka mainnet releases (est. Oct '25)

**Meeting Time:** Thursday, August 21, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1673)

## Replies

**abcoathup** (2025-08-14):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #163, August 21, 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-163-august-21-2025/25104/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #163 Action Items
>
> Continue work to produce trunk branches for Fusaka with target by end of next week
> fusaka-devnet-5 will launch once those are ready (est. 1 Sep)
> Non-headliner Glamsterdam EIPs should be proposed by the time Fusaka mainnet releases are out
>
> ACDC #163 Summary
> Fusaka
>
> fusaka-devnet-3 undergoing a non-finality test, restoring back to default state
>
> currently ~80% participation achieved
>
>
> Some client updates
>
> Lighthouse working through syncing issues
> Memory leak in Reth, re…

### Recordings/Stream

- YouTube
- Live stream on X: [x.com/ECHInstitute]
- Podcast (audio)

### Writeups

- Quick summary by @poojaranjan
- ACDC #163: Call Minutes by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDC #163 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- EIP-7732 Breakout Room Call #22, August 29, 2025
- EIP-7928 Breakout #1, August 27, 2025
- Meta EIP-8007: Glamsterdam gas repricings

---

**poojaranjan** (2025-08-21):

ACDC 163 - [Tweet Thread](https://x.com/poojaranjan19/status/1958529528927515092)

---

**ralexstokes** (2025-08-21):

**ACDC #163 Action Items**

- Continue work to produce trunk branches for Fusaka with target by end of next week
- fusaka-devnet-5 will launch once those are ready (est. 1 Sep)
- Non-headliner Glamsterdam EIPs should be proposed by the time Fusaka mainnet releases are out

**ACDC #163 Summary**

Fusaka

- fusaka-devnet-3 undergoing a non-finality test, restoring back to default state

currently ~80% participation achieved

Some client updates

- Lighthouse working through syncing issues
- Memory leak in Reth, reported to team

`fusaka-devnet-4` was launched, but taken down due to:

- BPO spec ambiguity resulting in chain split
- Syncing issues mentioned above

`fusaka-devnet-5` launch planned for week after next

- Same scope as devnet-4, no spec changes from devnet-3
- Large devnet like devnet-4
- Waiting on teams to have trunk branches ready, which pipelines things for testnets and mainnet

Team Readiness Updates

- All teams either working on issues noted above, or preparing trunk branches towards a release
- General agreement on target end of next week to be prepared for a devnet-5 the week after that
- Relevant link to see when clients update to trunk: fusaka-devnets/ansible/inventories/devnet-3/group_vars/all/images.yaml at master · ethpandaops/fusaka-devnets · GitHub

Spec & Testing Updates

- Minimal preset parameter adjustment merged for testing

Enables larger validator counts on minimal preset
- Helps with lighter devnet operations

Justin Traglia releasing `alpha.5` spec version today

- Includes parameter changes and additional updates

Security Analysis - BPO Fork Version

- Theoretical attack vector analysis completed across three areas:

Wasteful work through minority fork block fetching
- Potential mesh advantage for attackers serving unavailable data
- Cross-feeding attestations between forks

Conclusion: Extremely theoretical with 1 in 129 million probability

- Requires sophisticated attacker, not a realistic concern for mainnet

Plan to update EIP with trade-off documentation between fork digest vs fork version solutions

Glamsterdam

- Mostly announcements today, to keep focus on Fusaka
- Block-level access list breakout

EIP-7928 Breakout #1, August 27, 2025 · Issue #1691 · ethereum/pm · GitHub

EIP 7732 breakout

- EIP-7732 Breakout Room Call #22, August 29, 2025 · Issue #1696 · ethereum/pm · GitHub

Glamsterdam gas repricings: [Add EIP: Glamstardam Gas Repricings by misilva73 · Pull Request #10206 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/10206)
Targeting Fusaka mainnet releases as the deadline for non-headliner Glamsterdam proposals (~Oct)

---

**system** (2025-08-22):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: rWQ5Tt^V)
- Download Chat (Passcode: rWQ5Tt^V)

---

**system** (2025-08-22):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=gQly_DxdCHI

