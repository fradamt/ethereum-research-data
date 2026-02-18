---
source: magicians
topic_id: 24076
title: All Core Devs - Testing (ACDT) #36 | May 12 2025
author: system
date: "2025-05-06"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-36-may-12-2025/24076
views: 200
likes: 4
posts_count: 4
---

# All Core Devs - Testing (ACDT) #36 | May 12 2025

# All Core Devs - Testing (ACDT) #36, May 12 2025

- May 12, 2025, 14:00 UTC
- 60 Minutes
- Recurring meeting : true
- Call series : All Core Devs - Testing
- Occurrence rate : weekly
- Already on Ethereum Calendar : true
- Need YouTube stream links : true

# Agenda

- Pectra fork (if necessary)
- Decide which CFI’d EIPs move to SFI status for include in Fusaka Devnet-0
- PeerDAS testing
- Introduce blob schedule CL discussion (https://github.com/ethereum/consensus-specs/pull/4277)
- Discussion about history expiry and what our plan is for rollout, releases, docs, testing

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: [mario.vega@ethereum.org](mailto:mario.vega@ethereum.org)

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : All Core Devs - Testing
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1528)

## Replies

**poojaranjan** (2025-05-12):

### Summary

- Fusaka Devnet 0

Launch Target: ~2 weeks
- Devnet will include proposals:

BPO
- PeerDAS
- ModExp proposals - EIP-7823, EIP-7883

**History Expiry**

- History Expiry drop and Documentation (on Sepolia) target: June 1, 2025

- Quick Notes

---

**system** (2025-05-12):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

In the meeting, Mario led the discussion on the Ethereum fork, highlighting the successful completion of the deposit mechanism transition. He also mentioned the removal of the eth1_data poll. Kyle shared that they are still investigating performance issues for Prysm. Mario then presented a tracker for the Fuzaka devnet 0, which included a list of CF5 VIPS for Fuzaka. The team discussed the inclusion of these VIPS, with Erigon’s list being the main point of discussion. The team agreed to include all other EIPs that other teams consider important.

In the meeting, the team discussed the timeline for the next devnet. They agreed to include the BPO (Bloom Proof of Work) in the first devnet, which is scheduled for two weeks. The team also discussed the possibility of including two of the CF5 (Consensus Forks) VIPs (Very Important Pieces) in the devnet. However, Justin Florentine suggested that these should go into a devnet one, not the first one. The team also discussed the need for more rigid timelines to ensure issues are found before the in-person meeting in June.

In the meeting, the team discussed the inclusion of Modex in their project. Roman expressed a preference for including Modex, but Justin Florentine mentioned a timing issue and the need for isolation of pure DOS testing. The team also discussed the implementation of Pr desk on the Cl side and the potential changes required on the Yale side. Andrew raised a question about the changes needed on the Yale side, to which Parithosh responded that it shouldn’t be a massive change set. The team also discussed the issue with the native crypto integration and the need to nail it down for cell proofs. The team agreed to include Modex in the project and to start preparing the tests. The team also discussed the inclusion of the pay opcode in the project, with Jochem-brouwer suggesting that it should be included in the next version. The team agreed to include the pay opcode in the next version.

In the meeting, FLCL proposed a suggestion to limit the book count per transaction. Marcin agreed, suggesting a cap on the maximum number of blobs per transaction. Terence discussed the potential cost savings of batching posts and suggested bringing the topic to the raw venue. Francis suggested tentatively including the limit and starting work on it. Kevaundray asked about the intersection with the cap on transaction size in the network. Mario clarified that the limit was on the block size, not the transaction size. The team agreed to defer the topic to at least version 11. The PR raised by Alex was discussed, with Justin confirming it had been merged. Barnabas was set to discuss the history expiry.

In the meeting, Barnabas proposed pushing the deadline for dropping history on support to the 1st of June, from the original deadline of the 1st of May. Parithosh suggested including documentation for public testing by the same deadline. The team agreed to coordinate the implementation of history expiry across clients, with the understanding that each client can enable it whenever they’re ready. The conversation ended with the decision to set the new deadline as the 1st of June, with the expectation of having some clients ready by then.

### Next Steps:

- All client teams to prepare for Devnet 0 in 2 weeks, including Peerdas, BPO, and ModExp EIPs (78,23 and 78,83).
- Justin Traglia to merge the BPO block/blob schedule PR and make an APR to backport it to Dene.
- Client teams to consider and provide feedback on limiting blob count per transaction for potential inclusion in Devnet 1.
- Client teams to prepare documentation and user guides for history expiry by June 1st.
- Client teams to work towards enabling history expiry before Cancun, with progress updates to be provided in weekly meetings.
- Barnabas and team to continue work on adding support for arbitrary history drop at specific heights for testing history expiry.

### Recording Access:

- Join Recording Session (Passcode: KxhNf.T6)
- Download Transcript
- Download Chat

---

**system** (2025-05-12):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=Lzpb1czKWR8

