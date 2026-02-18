---
source: magicians
topic_id: 25859
title: All Core Devs - Testing (ACDT) #58, Oct 20, 2025
author: system
date: "2025-10-17"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-58-oct-20-2025/25859
views: 55
likes: 1
posts_count: 5
---

# All Core Devs - Testing (ACDT) #58, Oct 20, 2025

### Agenda

#### Fusaka:

- Fusaka Holesky BPO fork updates
- Fusaka devnet status updates

#### Gas limit testing update:

- 60M gas limit on mainnet updates
- State test updates

#### Glamsterdam Testing Updates:

- BALer updates
- ePBS updates

#### Other Topics

- RPC updates

**Meeting Time:** Monday, October 20, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1769)

## Replies

**poojaranjan** (2025-10-20):

# All Core Devs - Testing (ACDT) #58 October 20, 2025 (Quick Notes)

Parithosh Jayanthi facilitated the call.

## Fusaka Holesky BPO fork updates

Barnabas

- Sepolia hard fork completed last week.
- BPO 1 scheduled for tomorrow.

Target blobs: increase to 10
- Max blobs: 15

Next BPO: Oct 20
Hoodi hard fork is planned between BPOs.
Reported issue: a few operators failed to update nodes, but no major bugs detected.

Pari

- EF Blobs blog post is published.
- Another post to include on tx cap limits is expected.
- If clients face RPC or related issues, teams should reach out.

### Client Updates

Prysm

- New release coming to fix blob endpoint on mainnet.

Pawan

- A new RC (release candidate) expected tomorrow.
- Includes bug fixes.
- Semi-supernode support might be included (not guaranteed).

Andrew (Erigon)

- v3.2.1 released — recommended for Hoodi.
- Was producing invalid blocks only on Hoodi.
- Pari suggested continuing the discussion on Discord.

Lucas (Nethermind)

- New release today — optional for Hoodi.

Marius (Geth)

- Optional release is live.
- RPC providers may see extra strain and should auto-reject problematic txs.
- Issue expected to persist until 1–2 releases after the fork.

Besu (Amazein)

- Optional release:
Release 25.10.0 · hyperledger/besu · GitHub

Mehdi Aouadi

- Another release is expected soon.

Pari: A full round of client releases seems likely.

### Holesky Sunset

- Barnabas reminded node providers about the Holesky sunset.
- Pari noted it may be a gradual wind-down.
- Barnabas suggested a blog post would help.
- Pari said he’ll look into it.

### Additional Notes

Lukasz

- Nethermind is reviewing Fusaka changes and repricing logic.
- Scanned 100k blocks.

Marek

- Exploring gas pricing more broadly.

Reference

•	Parithosh update:



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/1769#issuecomment-3421983277)












####



        opened 02:39PM - 17 Oct 25 UTC



          closed 05:02PM - 21 Oct 25 UTC



        [![](https://avatars.githubusercontent.com/u/17509050?v=4)
          parithosh](https://github.com/parithosh)





          ACD


          protocol-call







### UTC Date & Time

Oct 20, 2025, 14:00 UTC

### Agenda

#### Fusaka:
- Fusaka […]()Holesky BPO fork updates
- Fusaka devnet status updates

#### Gas limit testing update:
- 60M gas limit on mainnet updates
- State test updates

#### Glamsterdam Testing Updates:
- BALer updates
- ePBS updates

#### Other Topics
- RPC updates

### Call Series

All Core Devs - Testing

<details>
<summary>🔧 Meeting Configuration</summary>

### Duration

60 minutes

### Occurrence Rate

weekly

### Use Custom Meeting Link (Optional)

- [ ] I will provide my own meeting link

### Facilitator Emails (Optional)

parithosh@ethereum.org

### Display Zoom Link in Calendar Invite (Optional)

- [x] Display Zoom link in invite

### YouTube Livestream Link (Optional)

- [x] Create YouTube livestream link
</details>












## Perfnet Devnet 2 Updates

Pari:

- Nethermind team is investigating unhealthy nodes.
- Erigon plans to run additional tests.
- State and gas limit testing: no significant updates yet.
- Teams should keep an eye on Perfnet Devnet 2 for upcoming changes.

## Glamsterdam Testing Updates

Stefan

- Solid progress across Besu, Geth, and Nethermind.
- Getting close to Devnet 0 readiness.

### BALs

Toni

- Coinbase handling will be discussed in the upcoming breakout room.
- Any breaking changes, if needed, will be deferred to Devnet 1 instead of Devnet 0.

Dragan Rakita

- All BAL blockchain tests have passed; updates will land in a branch soon.

### ePBS

Justin Traglia confirmed that the decision from the last ACD call is to keep the current spec.

- Next breakout Agenda
- Specs for devnet

Beta 0 remains the spec for Devnet 0.
- Beta 1 is planned for release this week.

## RPC Updates

- Active discussions are happening on Eth R&D Discord.
- Lukasz: Ongoing discussion around parsing — whether it should be strict or lenient.
- Nethermind has already implemented adjustments based on Felix’s suggestions.
- Marek shared progress (chat):
Nethermind RPC compatibility is at 165/190, only 25 tests left.
- Pari mentioned:

A weekly bot is posting RPC status.
- Currently, two client teams are participating in this tracking.

## Communications Approach

Pari shared

- A new STEEL Discord server has been set up.
- EthPandaOps will manage:

One channel per client team
- One channel for the STEEL team

This will be the primary hub for client and testing communications going forward.
All client developers should already have invites.
If someone is missing access, they should contact EthPandaOps.

*PS: This is quick notes. In case of any change, please add comments [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#All-Core-Devs---Testing-ACDT-58-October-20-2025).*

---

**system** (2025-10-20):

### Meeting Summary:

The team discussed updates on the Sepolia hard fork and upcoming changes related to the Fusaka blob update, including new release plans for various clients and potential system issues to watch for. They reviewed progress on client implementations and discussed improvements in RPC compatibility, with a new communication approach being implemented on the Steel Discord server. The team also addressed concerns about the upcoming shutdown of Bosky and discussed various technical issues including block-level access lists and gas limit problems in account abstraction.

**Click to expand detailed summary**

The team discussed updates on the Sepolia hard fork and upcoming changes related to the Fusaka blob update. Barnabas reported that the first BPO will increase the target to 10 and max to 15 blobs on Sapori, with the next BPO scheduled for October 28th. James mentioned a new release for prysm to fix the blob endpoint on mainnet, and Parithosh highlighted the introduction of a 16 million transaction cap limit with Osaka, advising users to review their systems for potential issues. The team encouraged users to report any UX or RPC-related issues observed after the Sepolia Fusaka update for further tracking and fixes before the mainnet launch.

The team discussed the release of Erigon 3.2.1, which includes bug fixes and is recommended for use on Hoodi due to fixing an issue with Aragon producing invalid blocks. Andrew explained that the invalid block issue occurred when transactions depended on the beacon route, and Parithosh suggested discussing more details in a shared chat and adding a test case to EEST. The team also mentioned an optional release of Geth and planned to update their blog with information about Lighthouse and Aragon issues.

The team discussed the upcoming release of Geth that will automatically convert blob transactions for L2s still sending the wrong transactions, which will be enabled by default without any flags. Parithosh clarified that this conversion feature will be available in the next one or two releases after the fork. Ameziane mentioned that Besu also has an optional release available. The team also briefly discussed enabling 60M gas on Hoodi, which Parithosh confirmed should already be at that level.

The team discussed the status of Hoodie, which is already at 60 million, and confirmed it’s in good shape. Barnabas warned about the upcoming shutdown of Bosky by the end of the month, urging operators to migrate their infrastructure away from it as non-finality is expected by the end of the week. The team agreed to create a blog post to remind everyone about the Bosky shutdown, which Parithosh and Barnabas will work on this week.

The team discussed issues with user operations in account abstraction and gas limit problems, with Marek explaining that increasing gas limits is challenging with bundled transactions. Parithosh provided updates on DevNet 2, noting that while most nodes are now healthy, there’s still an unhealthy Netherland node that needs to be fixed before switching the network ID. The team also mentioned that Aragon wants to conduct tests on PostDevnet, and Stefan was asked for an update on block-level access lists, which was not provided in the transcript.

The team discussed progress on client implementations, with Besu, Geth, and Nethermind being close to completion for DevNet0. Toni mentioned an upcoming block access list breakout call on Wednesday to discuss Coinbase handling and edge cases. The team also discussed visualization improvements for block-level access lists in DORA, with Toni noting that a tab already exists in the Explorer but metrics are still pending. Justin provided an update on the EPBS spec, confirming that the Beta Zero spec is finalized for DevNet0, with a new Beta 1 release planned for later in the week. The team encouraged client teams to reach out if they have implementations ready for early testing.

The team discussed improvements in RPC compatibility, with Łukasz reporting progress in parsing implementation and increased compatibility with Hive tests. Parithosh mentioned that a weekly bot now tracks RPC compatibility progress, noting positive improvements in two clients and a 13% increase in passing tests. The team also announced a new communication approach, consolidating channels on the Steel Discord server for better coordination between client developers and testing teams.

### Next Steps:

- Ethereum Foundation to publish a blog post about the transaction cap limit with Osaka and considerations for users with pre-signed transactions.
- Ethereum Foundation to publish a blog post reminding everyone about Holsky shutdown by the end of the month.
- Pawan to release a new RC for Hoodie with bug fixes.
- Parithosh to update the blog with Lighthouse, Aragon, and other client issues.
- Client teams to implement block-level access lists for DevNet 0 .
- EPBS team to release Beta 1 spec sometime this week.
- Toni’s team to discuss Coinbase handling for block-level access lists at the breakout call on Wednesday.
- Katya to introduce metrics for block-level access lists in DORA.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 4QBi*@4u)
- Download Chat (Passcode: 4QBi*@4u)

---

**system** (2025-10-20):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=5qqcQaAet2o

---

**zaraberg** (2025-10-26):

I found this site recently and it seems like a good place for those interested in exploring modern financial opportunities. It provides useful features and practical insights that can help improve money management. If you’re into smart financial tools, you might want to take a look [madcash.pro](http://madcash.pro).

