---
source: magicians
topic_id: 24771
title: All Core Devs - Consensus (ACDC) #160, July 10 2025
author: system
date: "2025-07-09"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-160-july-10-2025/24771
views: 170
likes: 1
posts_count: 5
---

# All Core Devs - Consensus (ACDC) #160, July 10 2025

All Core Devs - Consensus (ACDC) #160, July 10, 2025

- Jul 10, 2025, 14:00 UTC

# Agenda

- CL releases with updated gas limit values
- Fusaka

fusaka-devnet-2 status
- fusaka-devnet-3 spec

All Core Devs - Consensus (ACDC) #160, July 10 2025 · Issue #1598 · ethereum/pm · GitHub
- https://github.com/ethereum/execution-apis/pull/674
- https://github.com/ethereum/builder-specs/pull/123
- open issues with BPO or validator custody?
- devnet launch date?

Road to mainnet

- cf. Road to Shipping PeerDAS to Mainnet in 2025
- get stable devnet-3 then shift to hardening implementations
- BPO schedule proposals

Glamsterdam

- Select 1 CL headliner on 24 July

n.b. only 1 headliner per layer

headliner discussion

Facilitator emails:

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : acdc
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1598)

## Replies

**system** (2025-07-10):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 5nn8T$K&)
- Download Chat (Passcode: 5nn8T$K&)

---

**system** (2025-07-10):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=WPT-PTuBb0U

---

**yashkamalchaturvedi** (2025-07-10):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 10 Jul 25](https://etherworld.co/2025/07/10/highlights-from-the-all-core-developers-consensus-acdc-call-160/)



    ![image](https://etherworld.co/content/images/2025/07/EW-Thumbnails-3.jpg)

###



Gas Limit Updates, Fusaka Devnet 2 Status & Devnet 3, engine_getBlobsV3 Proposal, GetPayload Change, Roadmap to Fusaka, PeerDAS & BPO Glamsterdam Discussion

---

**ralexstokes** (2025-07-11):

**ACDC #160 Action Items**

- Prepare/publish releases with updated default gas limit
- Debug fusaka-devnet-2 and prepare for fusaka-devnet-3 genesis the week of 21st July

https://notes.ethereum.org/@ethpandaops/fusaka-devnet-3

Start preparing client opinions for headliner selection to occur after `fusaka-devnet-3` is live and stable

- https://forkcast.org/upgrade/glamsterdam for a nice digestible EIP explorer

**ACDC #160 Summary**

Releases for higher (default) gas limit

- CL releases require updated gas limit values to 45M
- Clients plan releases soon with updated gas limits

Fusaka

- devnet-2

Participation rate and proposals are healthy but could be better
- Some nodes experiencing memory issues with high column participation; some other peering issues
- Current focus on fixing existing bugs to ready for devnet-3

devnet-3

- Launch targeted for week of 21st July
- Will reflect the mainnet Fusaka spec
- [clarification for EL EIPs] Will include CLZ and transaction gas cap changes

Refer to https://notes.ethereum.org/@ethpandaops/fusaka-devnet-3 for the latest

With a stable devnet-3, then turn to hardening implementations

- Focus on testing non-finality scenarios and syncing

GetBlobs API Changes

- Proposal to revert GetBlobs v2 semantics and move partial response functionality to v3

engine/blobs: move partial return support to mandatory `engine_getBlobsV3` by raulk · Pull Request #674 · ethereum/execution-apis · GitHub

Current v2 spec uses “may” language for partial responses which creates ambiguity
Agreement to:

- Restore v2 to all-or-nothing responses
- Implement mandatory partial responses in v3

meaning merge in #674

Aim to have v3 in Fusaka so that we can leverage the feature with further networking optimizations even ahead of Glamsterdam

Builder API changes

- One open spec item for devnet-3 is changing the response of the builder API’s getPayload call to reflect the high planned blob count
- A PR proposing one solution is here:

Add `eth/v2/builder/blinded_blocks` which does not return the execution payload and blobs by bharath-123 · Pull Request #123 · ethereum/builder-specs · GitHub
- Core devs present generally favored this solution

Mainnet Planning

- Rough target timelines from Sigma Prime blog post:

Road to Shipping PeerDAS to Mainnet in 2025
- Mid-October mainnet launch
- September testnets
- August preparation

General consensus on something like this to target Q4 Fusaka launch

- although consider the above post a strawman for now

Wide agreement that we need the following before going to mainnet:

- Need extensive testing of:

Non-finality scenarios and other failure cases
- Syncing behavior
- Network with 1000+ nodes and more realistic P2P conditions

Attendees also favored a conservative BPO rollout strategy

- Initial modest increase at launch, with an observation period to gather mainnet data
- Then, a second increase early next year aiming for the full theoretical gain PeerDAS can unlock

⠀Glamsterdam EIP Discussion

- Focus on selecting single headliner EIP per layer
- Key CL headliner candidates:

EIP-7732 (ePBS)
- EIP-7782 (6-second slots)
- EIP-7805 (FOCIL)
- EIP-7919 (Pureth)
- EIP-7942 (Available attestation)

Plenty of discussion on the best way to select a single headliner to start to form the Glamsterdam scope
Participants felt it was too early to begin headliner selection today, and after checking with EL representation we decided to coordinate more closely with ACDE which needs more time
Reflecting all of the discussion, we decided to wait for Glamsterdam headliner selection until `fusaka-devnet-3` is live and healthy
Client teams still have time to assemble their opinions on headliner, but there seems to be early interest in a headliner that generally follows the “theme” of scaling
We also highlighted the need for better community input as a way to surface to core developers what is best for Ethereum at this time
`fusaka-devnet-3` is still some time out, but we did agree that allocating two ACD calls, 1 for headliner discussion and 1 for headliner decision, made sense

