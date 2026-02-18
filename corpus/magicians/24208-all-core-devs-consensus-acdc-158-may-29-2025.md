---
source: magicians
topic_id: 24208
title: All Core Devs - Consensus (ACDC) #158, May 29 2025
author: system
date: "2025-05-16"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-158-may-29-2025/24208
views: 523
likes: 7
posts_count: 8
---

# All Core Devs - Consensus (ACDC) #158, May 29 2025

All Core Devs - Consensus (ACDC) #159, June 26, 2025

- June 26, 2025, 14:00 UTC

# Agenda

- Fusaka
- Glamsterdam
- TBA

Facilitator emails:

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDC
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1579)

**YouTube Stream Links:**

- Stream 1 (Jun 26, 2025): https://youtube.com/watch?v=nV-myyBPbWk

## Replies

**abcoathup** (2025-05-20):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #158, May 29 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-158-may-29-2025/24208/7) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #158 Summary
> Action items
>
> Continue debugging of fusaka-devnet-0
> EIP-7917 has been SFI’d for Fusaka with target of fusaka-devnet-1
> Prepare readiness for fusaka-devnet-1, recognizing PeerDAS bugfixes from fusaka-devnet-0 and EIP-7917
>
> Summary
> Fusaka
>
>
> fusaka-devnet-0 is live!
>
> Some minor issues client teams are working through, but things are progressing well
> Includes the BPO feature to scale blob count, which is working as intended so far
>
>
>
> Fusaka CL EIPs to SFI
>
> only EIP to consider…

### Recordings

  [![image](https://img.youtube.com/vi/cIHtUaIev4M/maxresdefault.jpg)](https://www.youtube.com/watch?v=cIHtUaIev4M&t=278s)

https://x.com/i/broadcasts/1eaKbWpkYQnGX

### Writeups

- X thread by @poojaranjan
- Highlights from the All Core Developers Consensus (ACDC) Call #158 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

EIP-7917: Deterministic proposer lookahead SFI’d.  Adding to fusaka-devnet-1 June 9.
- fusaka-devnet-2 targeting two weeks after devnet-1

Glamsterdam upgrade:

- Initial headliner proposals:

ePBS: presentation & headliner proposal
- FOCIL: presentation & headliner proposal

Bogotá + H-star upgrade:

- H-star name needed for consensus layer upgrade after Glamsterdam

---

**system** (2025-05-29):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=cIHtUaIev4M

---

**ralexstokes** (2025-05-30):

**ACDC #158 Summary**

**Action items**

- Continue debugging of fusaka-devnet-0
- EIP-7917 has been SFI’d for Fusaka with target of fusaka-devnet-1
- Prepare readiness for fusaka-devnet-1, recognizing PeerDAS bugfixes from fusaka-devnet-0 and EIP-7917

**Summary**

Fusaka

- fusaka-devnet-0 is live!

Some minor issues client teams are working through, but things are progressing well
- Includes the BPO feature to scale blob count, which is working as intended so far

Fusaka CL EIPs to SFI

- only EIP to consider was EIP-7917 for proposer lookahead
- began with input from EIP champions and community members (preconf builders/users) who are impacted by this EIP
- consensus amongst client teams was that implementation complexity was low, and the EIP is supported by spec testing that builds confidence in correctness
- taken together, we decided to SFI 7917 and target fusaka-devnet-1 inclusion, with the understanding that it could be pulled in the event there are further complications from testing/integration

PeerDAS

- Resolved some open questions around the BPO EIP

Decided to move forward with BPO-change aware fork digests that would be reflected in a node’s ENR, update to EIP forthcoming.

Touched on open questions around validatory custody, but the relevant contributors were not present so we decided to handle on Monday’s ACDT.

Glamsterdam

- Opened the Glamsterdam conversation with a general discussion on high-level fork framing and some headliner previews
- We had rough consensus that the fork focus should be around scalability and a potential subfocus of UX
- With that in mind, we had two headliner presentations

EIP-7732 (ePBS)

check the call for a short presentation from @potuz
- EIP-7732 the case for inclusion in Glamsterdam
- the pipelining benefits of 7732 fall into the scalability focus, although there were a number of questions around other parts of the proposal

EIP-7805 (FOCIL)

- check the call for a short presentation from @soispoke
- EIP-7805 Fork-Choice Inclusion Lists (FOCIL) as a candidate for Glamsterdam
- the discussion around this EIP was interesting, as many participants underscored the importance of FOCIL for CR properties but pointed out it didn’t directly contribute to the scalability focus; some discussion around presenting this EIP as enhancing UX
- regardless, there was general support for this EIP and participants decided to keep reviewing in the context of other headliners as we progress in the fork scoping conversation

We wrapped the call by exploring which parts of the community ACD should seek to provide perspectives on Glamsterdam EIPs

- for 7732, we identified the MEV ecosystem as desireable to weigh in on the builder mechanics of this EIP, and the solo staker community as desireable to speak to the improvements to node load from the EIP’s proposed pipelining structure
- FOCIL was a bit trickier as it applies to the entire Ethereum community although that is signal in itself

We did not make any explicit decisions around Glamsterdam scope today, and instead opened the conversation to begin headliner selection alongside forthcoming EL EIPs.

---

**system** (2025-05-31):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: kmIa6ub^)
- Download Chat (Passcode: kmIa6ub^)

---

**system** (2025-06-26):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: JGdU5#tg)
- Download Chat (Passcode: JGdU5#tg)

---

**system** (2025-06-26):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=nV-myyBPbWk

---

**nixo** (2025-07-12):

who can correct the info on this post? an admin or a mod? [@nicocsgy](/u/nicocsgy) [@abcoathup](/u/abcoathup) - the info in the original post is for ACDC #159 (e.g. YT stream link / date / github issue)

