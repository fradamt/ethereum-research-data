---
source: magicians
topic_id: 25633
title: All Core Devs - Testing (ACDT) #56, Oct 6, 2025
author: system
date: "2025-09-30"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-56-oct-6-2025/25633
views: 52
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #56, Oct 6, 2025

### Agenda

**Fusaka:**

- Fusaka Holesky fork updates
- Fusaka devnet status updates

**Gas limit testing update:**

- 60M gas limit on mainnet updates
- State test updates

**Glamsterdam Testing Updates:**

- BALer updates
- ePBS updates

**Meeting Time:** Monday, October 06, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1750)

## Replies

**poojaranjan** (2025-10-06):

# ACD Testing Call #56 - Oct 06, 2025 (Quick Notes)

Parithosh Jayanthi facilitated the call.

## Fusaka

## Fusaka Holesky fork updates

- Fork upgrade happened last Wednesday.
- BPO 1 scheduled to go live tomorrow (11h45m from call time).

### Lighthouse Reorg Issue

- High reorg rates observed on Lighthouse.
- Pawan: Issue acknowledged.
- A fix is planned for the next release (this week or next).

### Unrelated Testnet Incident (Nethermind)

- No direct update shared.
- More information available in the testnet channel
- New client release is out.

### Client Readiness for BPO 1

- Teams generally feel prepared for the rollout.

### KZG Proof Verification Issue

Pawan: Raised a question regarding KZG proof verification.

- OP Stack team reported a proof failing to verify.
- Discussion ongoing here

Next steps:

- Pari to sync with attestations team.
- A public statement will be issued explaining the upcoming change.

### MEV-Boost (Get Payload API)

- Teams were using version 2 prior to Fusaka activation.

Question raised:

➝ Is there consistent behavior across all clients using v2?

- Prysm believes they’re aligned post-fork but will confirm.

- nflaig: Switching occurs at fork boundary.

- Bharath to give additional clarification in the [Discord thread](https://discord.com/channels/595666850260713488/892088344438255616/1423587130323632268)

Pari: Expects steady MEV blocks to resume.

### Holesky End-of-Life

Announcement: Holesky will reach End Of Life at the end of this month.

## Fusaka devnet status updates

- Devnet 3 has been running non-finality tests for the past 2–3 days; it is successfully recovered.
- Some nodes experienced disk exhaustion again.
- Planning another network split test using the Sunnyside Labs tool.

Side note: This will run through BPO: [Experiments | The Lab by ethPandaOps](https://lab.ethpandaops.io/experiments)

## Gas limit testing update:

## 60M gas limit on mainnet updates

Besu:

- Bug report shared.
- Implementation is complete and will be frozen by tomorrow.
- Fuzzing and testing will follow.
- The testing team has already been contacted.
- Marius (Geth) has started efuzzing on his end.
- Full testing to begin by Wednesday.

## State test updates

Cprezz:

- Needs to adapt the Nethermind framework.
- Will experiment and report findings.
- Pari: A call is already scheduled and will happen soon.

## Glamsterdam Testing Updates:

## BALer updates

Toni:

- BALer specs progressing well.
- Execution API PR merged
- Working through complex edge cases like EIP-7702—spec side looks good.
- BAL breakout happening this week to discuss client updates, including:
- BAL hash vs BAL root

Felipe:

- Testing status is positive.
- One incorrect test reported and fixed.
- A few open PRs to add additional tests.
- RETH added to the tracker.
- Both RETH and Geth are currently passing tests.

Referenced Links:

- Add Amsterdam execution-api specs by nerolation · Pull Request #691 · ethereum/execution-apis · GitHub
- https://pokebal.raxhvl.com/
- bal-devnet-0 spec - HackMD

**Next Milestones**:

- Interop between Geth & Reth is the upcoming goal.
- Once three EL clients are running, the BAL testnet will launch.

Felipe: Nethermind is close but needs more context; Marc is investigating a Hive config issue.

Barnabas:

Requested that bal-devnet-0 branches live on the main repo to reduce confusion.

Łukasz:

Suggested syncing with Marc to make it happen.

Pari:

- Standardized naming schemes will simplify testing.
- Assertor will run to help uncover bugs.

## ePBS updates

Justin:

- Client teams are actively implementing.
- Breakout call planned for Friday.
- Trusted payment still undecided; needs more clarification.

Pari:

- There is a spec sheet for ePBS devnet-0, which will be updated.
- Standardized branch naming will apply here as well.

### RPC / Notifications

- If client teams want push notifications for RPC updates, they should reach out to Pari and team.
- Reference: Ethereum needs Standards-Punk - Meta-innovation - Ethereum Research

### MEV-Boost / Relay Behaviour

Pawan:

[Discord link](https://discord.com/channels/595666850260713488/1424763176008024095/)

- Asked about the correct way to switch behavior.

Bharath:

- Switch is not fork-dependent.
- ll relays just need proper implementation.
- Recommendation is to apply changes after Fusaka.
- Implementation must be in place by the Fusaka timeline.

Pawan (follow-up):

- Suggested confirming implementations across clients to ensure consistent behavior.

Pari:

- Requested Bharath to prepare a list for consistent behavior across teams.

*PS: This is a quick notes. In case of correction, please suggest [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-56---Oct-06-2025)*.

---

**system** (2025-10-06):

### Meeting Summary:

The team discussed updates on the Holsky fork and BP01 launch, addressing various technical issues including node reorganization rates and a Nethermind bug, while noting that most clients will switch to V2 at the fork boundary despite MEV relays’ support discontinuation. They reviewed progress on non-finality testing and upcoming maintenance for both Holsky and Fusaka testnets, including discussions on gas limits, scaling, and block-level access list specifications. The team concluded with plans for a breakout call to address trusted payments and agreed to improve application-focused testing and weekly Hive RPC reporting.

**Click to expand detailed summary**

The team discussed updates on the Holsky fork and the upcoming BP01 launch, noting a higher reorg rate on Lighthouse nodes that will be addressed in the next release. They also addressed a Nethermind bug and discussed changes to the blob sidecar endpoint, with Pawan raising questions about the KZG proof field. The team confirmed that most clients switch to the V2 version at the fork boundary, and Parithosh mentioned that MEV relays have stopped supporting Holsky, though this should not affect Sepolia and Goerli. Finally, they noted that Holsky is officially EOL at the end of the month, and there was a brief mention of nonfinality testing and disk space issues on some nodes.

The team discussed updates on Holsky and Fusaka testnets, including a successful non-finality testing period and upcoming maintenance. They addressed issues with gas limits, scaling, and MEV workflows, with Besu reporting progress on a 60 million gas implementation. The group reviewed block-level access list specifications and testing progress, noting that Reth and Geth are passing most current tests. They also discussed ePBS implementation and planned a breakout call for Friday to address trusted payments. Finally, they agreed to update the weekly Hive RPC pass/fail rate reporting and to coordinate on improving application-focused testing.

### Next Steps:

- Lighthouse team to release a fix for the higher reorg rate issue in the next release.
- Client teams to check with the attesting team to add support for the new GetBlobs endpoint.
- Client teams to put out a statement about the API change for GetBlobs endpoint.
- Pawan to find and share the thread about GetPayloadv2 endpoint usage.
- Besu team to freeze implementation of 60 million gas limit by tomorrow and start fuzzing and testing.
- Carlos and team to work with EAST on orchestrating the framework for stateful tests this week.
- Client teams to push block-level access list code to a branch called “BAL DevNet0” on their main repositories.
- Client teams to attend the ePBS breakout call on Friday to discuss trusted payments and other details.
- Client teams to create a branch called “ePBS devnet0” on their main repositories for automation.
- Bharath to create a list on Discord showing how each client is implementing GetPayloadv2 for consistency.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 1?FV!HF&)
- Download Chat (Passcode: 1?FV!HF&)

---

**system** (2025-10-06):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=dfngSRH8r4E

