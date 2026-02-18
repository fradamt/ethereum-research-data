---
source: magicians
topic_id: 27425
title: All Core Devs - Consensus (ACDC) #173, Jan 22, 2026
author: system
date: "2026-01-12"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-173-jan-22-2026/27425
views: 84
likes: 1
posts_count: 4
---

# All Core Devs - Consensus (ACDC) #173, Jan 22, 2026

### Agenda

- Fusaka EIPs housekeeping
- Glamsterdam

ePBS devnet-0
- Engine API for BALs

Hegota

- Must have made EthMag post with hegota tag by 4 Feb inclusive

**Meeting Time:** Thursday, January 22, 2026 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1874)

## Replies

**system** (2026-01-22):

### Meeting Summary:

The meeting covered updates and discussions on multiple Ethereum Improvement Proposals and the ePBS project, including status adjustments and review requests for various EIPs. The team discussed ePBS implementation progress across clients, setting a February deadline for the devnet zero and considering an EL-only fork if ePBS is not ready. They also reviewed recent technical issues with Teku nodes and discussed partial cell proofs implementation, with clients working on different stages of the SSZ library updates.

**Click to expand detailed summary**

The meeting focused on updates and discussions around several Ethereum Improvement Proposals (EIPs) and the ePBS project. Pooja requested status adjustments for EIPs 76077723, 7594, and 7918, which were to be reviewed by relevant participants. The team discussed progress on ePBS, including spec changes and the need for ePBS DevNet Zero, with Barnabas sharing notes on scoping and Ben Adams highlighting a required CL change for SlotNum EL. Participants were encouraged to review the shared links and provide feedback on the ePBS devnet planning.

The team discussed the status and timeline of Ethereum Protocol Buffers (ePBS) implementation across clients, with Barnabas proposing a February 20th deadline for ePBS devnet zero. While some clients expressed concerns about shipping without ePBS, the group agreed to aim for the end of February deadline, with the option to proceed with an EL-only fork if ePBS is not ready. The team also reviewed recent issues with Teku nodes, which experienced performance problems during mainnet stress testing, and discussed a new Engine API PR related to Block Lab access lists. Finally, they noted that proposals for the Hecata fork are due February 4th, with champions requested to present their proposals by that date.

The team discussed the implementation status of partial cell proofs and the EIP-7688 SSZ library updates. Barnabas reported that Lighthouse and Prysm have partial implementations, while Teku and Lodestar are still working on it. The team agreed to roll out partial cell proofs through devnet, testnet, and then allow clients to implement it in their next stable release. Etan confirmed that SSZ container implementation can be done parallel to ePBS and is a library change that doesn’t affect consensus. Potuz expressed concern about potential issues with in-memory structures due to rehashing, and the team agreed to de-risk this point with a prototype.

### Next Steps:

- EIP authors : Review and adjust EIP statuses as requested by Pooja
- All CL clients: Target ePBS devnet zero by end of February
- Prysm and Lighthouse: Continue ePBS implementation progress and provide timeline updates in future calls
- Teku: Complete mitigations for LevelDB issues and move to RoxDB as default database in next release
- All CL clients: Review and implement Engine API PR for block-level access lists
- Prysm, Teku, Grandine, Nimbus: Implement BALs devnet 2 spec
- Teku, Lodestar, Nimbus: Implement partial cell proofs for devnet
- stokes: Follow up with Raul or Marco to champion partial cell proofs and bring them to future call
- Prysm, Grandine, Teku: Complete SSZ stable containers  library implementation
- Someone : Prototype and de-risk the rehashing/tree structure concerns for stable containers EIP
- Headliner proposal champions: Present proposals at ACD by February 4th

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: *Lp*#2mN)
- Download Chat (Passcode: *Lp*#2mN)
- Download Audio (Passcode: *Lp*#2mN)

---

**system** (2026-01-22):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=APiyToa6UmI

---

**abcoathup** (2026-01-28):

## Call details

### Video, transcript & chatlog

- All Core Devs Consensus #173 - Forkcast - [Forkcast] by EF Protocol Support

### News coverage

- Ethereal news weekly #8 | Ethereal news - [Ethereal news] edited by @abcoathup
- ACD After Hours: ACDC #173 - [ACD After Hours] by @Christine_dkim
- Highlights from ACDC #173 - [Etherworld] by @yashkamalchaturvedi

### Resources

- Glamsterdam Upgrade - Forkcast
- Hegotá Upgrade - Forkcast

