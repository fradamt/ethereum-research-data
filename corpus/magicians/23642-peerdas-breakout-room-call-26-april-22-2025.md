---
source: magicians
topic_id: 23642
title: PeerDAS Breakout Room - Call #26 | April 22, 2025
author: system
date: "2025-04-20"
category: Protocol Calls & happenings
tags: [peerdas]
url: https://ethereum-magicians.org/t/peerdas-breakout-room-call-26-april-22-2025/23642
views: 130
likes: 0
posts_count: 3
---

# PeerDAS Breakout Room - Call #26 | April 22, 2025

# PeerDAS Breakout Room - Call #26 | April 22, 2025

- Apr 22, 2025, 14:00 UTC
- Zoom link: Launch Meeting - Zoom

### Resources

- Ethereum Protocol Call calendar
- PeerDAS-PM.md
- Google Doc Meeting Notes
- Previous call
- Facilitator email: will@ethreum.org

# Agenda Overview

A.  Client Updates

B.  Devnet / Testing Updates

C.  Spec / EIP Discussion

D.  Open Discussion

# Agenda Details

## Client Updates

### CL Client Teams

| Team | Active ICs | Call 25 Update |
| --- | --- | --- |
| Lighthouse | Jimmy + Sunnyside Labs IC | No update provided. |
| Prysm | Manu & Terence + Francis & Niram from Base | Working on data column verification pipeline and implementing blobs bundle v2 structure to replace current v1 hack with extended size limit. |
| Teku | Dmitrii + Jerone Ost from Soneium | Completed distributed cell proofs implementation; merging PR - aim to join devnet-6 and starting 2-month transition of PeerDAS code to production. |
| Nimbus | Agnish & Dustin | NEW: OOO, current focus:  Investigating issues in the current devnet-6, improving column syncing for nimbus-eth2 |
| Lodestar | Matt K, Katya + Derek & Hugh from Base | Merged validator custody and getBlobsV2; implementing second column pull with metrics and making progress on multi-month refactor. |
| Grandine | Hangleang & Saulius Grigaitis | Investigating Grandine-Reth pairing issues, suspecting slow payload processing on Reth side. |

### EL Client Teams

| Team | Active ICs | Call 24 Update |
| --- | --- | --- |
| Geth | Felix, Marius, Lightclient | - No updated provided.- Sunnyside testing showed it used less resources while handling ~45 blobs per block. |
| Nethermind | FLCL, Marcin | Added metrics for getBlobs success/failure rates and working on PoC for SS endpoint for getBlobsV2. |
| Reth | Roman | Investigating high block processing times causing pairing failures with Lighthouse and Grandine. |
| Besu | tbd | - No updated provided.- Sunnyside testing showed it achieved highest performance (50 blobs per block). |
| Erigon | tbd | - No updated provided.- Sunnyside testing showed it achieved lowest performance (18 blobs per block). |
| ethereumjs | Gajinder | Working on PR; extending micro-eth-signer with cell functions and bundling CKG for devnets while waiting for library updates. |

## Devnet / Testing Updates

| Topic | Subtopic | Details |
| --- | --- | --- |
| peerdas-devnet-6 | current status | Pari to voice over |
|  | next steps | Pari to voice over |

**Sunnyside Labs** (recent activity):

- Shared 04/15 Update
- Testing different EL-CL client combinations on devnet-6; developing unified EL metrics proposal and continuing comparative performance analysis of execution clients.

## Spec / EIP Discussions

| Topic | Subtopic | Details |
| --- | --- | --- |
| BlobsBundleV2 | Formatting (flat vs. nested) | - Flat vs. nested structure for commitments/blobs/proofs arrays (FLCL) |
| BPO Schedule | CL BPO blob schedule | - confirm agreement on config- open PR: Introduce blob only parameter forks (note comment asking whether this should go into deneb) |
|  | EL BPO blob schedule | confirm agreement on config (any missing BPO-related PRs?) |

### Open Specs & Discussions

- Consensus: Remove placeholder MAX_BLOBS_PER_BLOCK_FULU (link)
- Consensus: Implement BPO fork blob limit logic (link)
- Engine API: Add EIP-7594 (PeerDAS) related change (link)
- Builder: Add EIP-7594 (PeerDAS) related change (link)
- Update EIP-7594: Add blob count per tx limit via blobSchedule (link)

### Draft Specs & Discussions

- Update EIP-7594: Polish EIP, expand rationale (link)

## Open Discussion

| Topic | Subtopic | Details |
| --- | --- | --- |
| Topic 1 | subtopic 1 | - details |
|  | subtopic 2 | - details |

# Schedule

| Date(s) | Item |
| --- | --- |
| April 9th | peerdas-devenet-6 live! |
| May ~5th | Pectra Mainnet |
| ~June 1st | fusaka-devnet-0 (w/ BPO) |
| June 8-14 | EL / CL Interop |
| Post June 14 | Audits: KZG libraries (c-kzg-4844, rust-eth-kzg, go-eth-kzg) |

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : PeerDAS Breakout Room
- Occurrence rate : weekly
- Already a Zoom meeting ID : false
- Already on Ethereum Calendar : true
- Need YouTube stream links : false
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1491)

## Replies

**system** (2025-05-06):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

In the meeting, Will led the discussion, and Manu provided updates on the new data current by route request, noting issues with the validator study and the need for improvements in sync speed. Dimitrii reported on the progress of the Vpr. Fox feature, while Agnish from the Nimbus team discussed their work on the new data columns by root Identifier, issues with the Sunnyside Network, and the implementation of validator custody. Agnish also mentioned improvements in column sync performance and the development of a column cache for block validation.

Will led a meeting discussing the readiness of Devnet 7. Matthew reported that the last piece was the updated recresp format, which was ready to merge but needed to be debugged first. Saulius mentioned that Hengling was working on issues and Devnet 7 readiness. Marcin discussed the network spam with drop transactions and updated metrics. Roman reported that they were yet to disable something on their branch. Csaba mentioned that Marius was working on removing affiliated things and looking into performance-related things. Gajinder reported on testing with definite 6 bills and found a couple of issues. Parithosh mentioned that Barnabas might have an update this week. Minhyuk reported on issues with nodes going over the data TV size disk size and some nodes not sinking further. Mikel mentioned that they had been analyzing the cat blobs.

Mikel presented a research course on the theoretical side of block transactions on the Polygon network. He shared his findings from running a small fork of the prison, which included extra information about the data. Mikel noted that 44% of the blocks had no blobs, and the distribution of blobs fell more into the range of one to three rather than four to six. He also observed that 68% of the RPC API calls were responded to successfully with all the blocks, indicating potential bandwidth savings for the consensus client. Mikel found that most partial responses were missing only one block out of the total requested, and he is still debugging the reasons for this.

Mikel discussed the time it took for the real to reply to requests, noting that 99% of the time stayed within 100 seconds. He suggested that pushing forward block transactions could speed up the time it takes to process a block on the consensus client. Mikel also mentioned the value of partial requests and the potential for distributed block building. Marcin added that they have partner responses in mind for v.1 and will have them for v.2. Will noted that 60-70% is still a good hit rate.

Will led a meeting where updates were shared about Nimbus, Teku, and Peerdas. Barnabas mentioned issues with Nimbus and the progress on Teku. The team discussed the possibility of targeting a Thursday launch for Peerdas. Parithosh shared about the sync tests and the need for refining them. The team also discussed the blob schedule, with Justin requesting a review and planning to merge it after the upcoming stable release. Justin also mentioned plans to merge a PR from JS Sunnyside regarding blob side cars defecation support. Lastly, Francis discussed the Beacon API.

Francis proposed two options for the Pr: either to change the current get block sidecars Pr to return only the data or to deprecate the current function and implement a new one called get blobs that only returns the blob data. The team agreed to merge the current Pr and update it later. The decision was made to align on a direction and not to block anyone’s progress. The team also discussed the possibility of implementing the changes after finalizing the solution.

Will discussed merging a project and flagged open discussions from the ACD call and Discord chat. Agnesh raised questions about validator custody, including the need for updates at least every two epochs, whether to pause or continue proposing while refilling, and the impact of changes in a non-finalized network. Justin clarified that validator custody should not change in a non-finalized network and that an honest validator should automatically update.

Justin and Agnish discussed the potential for penalization in their network, with Justin expressing uncertainty about how it would work. Agnish also raised the question of how often the validated custody can change in a practical network, suggesting it could be every bulk. They also discussed the possibility of checking advertised subnets to update their system, but Justin noted that this might break privacy. Agnish proposed the idea of a reward for having a validated custody above a certain number, but Justin said it was unlikely. Stokes and Will discussed the implementation of validator custody in Peerdas Devnet 7, with Stokes suggesting it should be included in the spec. The plan for the network was to ship Figured out, step net 7, followed by a devnet 8 including the Bpo feature, and then move on to Fusaka. Devnet 0 based on the devnet 8 spec.

Will led the discussion on moving the call to the testing call on Monday, which Justin agreed with. Mario and Parithosh discussed the moderation of the discussion topics for Peerdas, with Will agreeing to help. Parithosh suggested moving most of the discussion to the core devs testing call. Francis raised a question about the timeline for the launch of Devnet, which Parithosh responded to. Francis also suggested better tools for visualization to speed up the debugging process. Yannis mentioned that work on this had started but not much progress had been made yet. Marcin asked about the blob schedule changes in the scope of definite 7, to which Justin responded that it was not included in the scope.

### Next Steps:

- Francis to merge the PR regarding blob sidecars defecation support.
- Stokes to merge the builder spec change PR.
- Justin to include validator custody implementation in the Peerdas Devnet 7 spec.
- Will to remove the Peerdas breakout room meeting from the calendar and move discussions to the Monday ACD testing call.
- Will to help bring up Peerdas discussion topics for the Monday ACD testing call.
- Mario to open a PM issue for the Monday ACD testing call and send the link to Will.
- Parithosh to mention the meeting change in ACD this week.
- Yiannisbot and Francis to schedule a call to discuss collaboration on visualization tools for Peerdas debugging.
- Justin to finalize and merge the blob schedule changes by Friday for inclusion in the next Devnet.

### Recording Access:

- Join Recording Session (Passcode: J^jRW!^4)
- Download Transcript
- Download Chat

---

**system** (2025-05-06):

YouTube recording available: https://youtu.be/OLv7WV1LKCw

