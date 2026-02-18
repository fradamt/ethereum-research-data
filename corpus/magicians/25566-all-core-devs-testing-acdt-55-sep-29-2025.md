---
source: magicians
topic_id: 25566
title: All Core Devs - Testing (ACDT) #55, Sep 29, 2025
author: system
date: "2025-09-23"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-55-sep-29-2025/25566
views: 67
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #55, Sep 29, 2025

### Agenda

#### Fusaka

- Devnet 3 update (will continue running throughout the testnet upgrades), dora.fusaka-devnet-3.ethpandaops.io.
- Fusaka Testnet Announcement on blog.ethereum.org.
- Fusaka & BPOs testnet schedule:

.ics calendar to import via URL in your calendar.
- activation schedule in meta EIP (now also included in the Protocol Calendar).
- First activations:

Holešky Fusaka: This Wednesday, 2025-10-01 08:48:00.
- Holešky BPO1: Following Tuesday, 2025-10-07 01:20:00.
- Holešky BPO2: Monday, 2025-10-13 21:10:24.
- Sepolia Fusaka: Tuesday, 2025-10-14 07:36:00.

Status of client testnet releases.
EEST v5.2.0 release predominantly only updates the exception messages in client exception mappers.
EEST v5.3.0 is pending, which will update the `blobSchedule` params used in the fixtures to match the [params used in the testnets](https://github.com/eth-clients/holesky/blob/8aec65f11f0c986d6b76b2eb902420635eb9b815/metadata/genesis.json#L39-L47).
STEEL testnet verification efforts:

- Will verify client testnet configuration via execute config pre-launch.
- Live Fusaka Testnet EEST Test Execution via execute as performed for Prague Mainnet.

Currently WIP: Defining a representative subset of tests to execute.

Shadowfork discussion(?)
[Sherlock Fusaka Audit contest](https://blog.ethereum.org/2025/09/15/fusaka-audit-content) still ongoing: Started Sept 15th for 4 weeks.

#### Gas limit testing update

- Mainnet 60M gas limit target in Fusaka releases
- Latest proposal for ./tests/benchmarks/ dir structure in EEST.

**Compute-intensive benchmarks**

- There is a new EEST test format benchmark_test that abstracts the tx gas limit cap for easier test implementation. There is still some ongoing work here.

**State-intense benchmarks**

- @jochem-brouwer would like to bring up benchmark tests using mainnet state snapshots:

Questions for client teams:

What triggers worst-case behavior in state-intensive updates?
- E.g., in the XEN contracts: Updating existing storage slots, writing new slots, or deleting storage keys?

Questions about other known pathalogical cases on mainnet:

- Does anyone have an overview of the biggest storage tries on mainnet?
- Are there other exotic contracts on mainnet that mark multiple state trie nodes as dirty, which means they have to be updated before the state root calculation?

#### Glamsterdam Testing Updates

- New consenus-specs release last Thurs: v1.6.0-beta.0.

BALers be BALing:

- @raxhvl update on the state of BAL testing.
- bal-devnet-0 timeline: bal-devnet-0 spec - HackMD

eBPS:

- epbs-devnet-0 (targeting end of Oct 2025): epbs-devnet-0 spec - HackMD

**Meeting Time:** Monday, September 29, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1736)

## Replies

**poojaranjan** (2025-09-29):

# ACD Testing Call #55 - Sep 29, 2025 (Quick Notes)

Facilitated by Mario Vega

## Devnet 3 Update

- Devnet 3 will continue running throughout the testnet upgrades.

Mario:

- No finalization on Devnet 3?

PK:

- Just tested one non-finality scenario; non-finality on Devnet 3 is expected.
- This test was requested by a few client teams.
- The test will run for a couple of days; afterward, more clients will be added.

Mario: Any other clients want to chime in?

•	No additional updates.

### Additional Updates (Pari)

- Holešky shadowfork is up.
- Network appears to have stabilized; checking with Erigon.
- Besu is building blocks but experiencing some issues; client team has been informed.
- Able to submit queue; transition to Fusaka on that network should occur within the next half hour.

##

- Scheduled activation times are now available.
- For Holešky, activation is this Wednesday.

### Mainnet Shadowfork

- Barnabas: At least a month away.

### Testnet Updates

- Pari: Another testnet line (Devnet 3) is activated with a non-finality test and parallel sync test.
- Mario: It makes sense to delay the mainnet shadowfork.

### Lighthouse:

- The blog can be updated as we have a client release today.

### Prysm

- James He (Chat):

Released a version to support Fusaka.
- There are ongoing issues; from the team’s perspective it should be fine for the testnet.
- Some users are still experiencing problems.

## Fusaka & BPOs Testnet Schedule

- BPO activation will happen next week.

### Holešky To-Do List (Pari)

- Ensure all client releases are available.
- Perform shadowfork.
- Roll out Holešky nodes.
- Validate Holešky snapshots.
- Spin up one instance of every client on our stack.
- Enable Tracoor for Holešky, Forky, and Dora.
- Make sure Dugtrio is updated and running.
- Update Checkpointz.

## EEST Releases

- EEST v5.2.0: Predominantly updates exception messages in client exception mappers.
- EEST v5.3.0: Released with updated blobSchedule parameters in the fixtures to match the parameters used in the testnets.
- The blog post will be updated accordingly.
- If any issues are found, client teams will be notified (pinged).

##

- Contest is still ongoing; started on Sept 15th for 4 weeks.
- Justin: 2 more weeks remain for the competition; going well so far.

### Repository Organization

- Fredrik: Suggested creating a Fusaka directory on the pm repo to add relevant files.
- Pooja: Mentioned there is already a Fusaka folder.
- Alex Stokes: Will update the folder with related files.

## Gas Limit Testing Update

- Mainnet 60M gas limit target in Fusaka releases
- Latest proposal for ./tests/benchmarks/ directory structure in EEST.

### Current Status

- Testnet is already at 60M.
- Mainnet will reach 60M upon release in Nethermind.

### Clients’ Notes

- Kamil (Testing Perspective):

There is a PR that will include the mainnet release.

**Ameziane Hamlat (Chat):**

- In Besu, it is not yet included in the testnet release; will be part of the mainnet release.

**Jen:**

- Reth is ready; 60M is included in its release.

## Compute-Intensive Benchmarks

- A new EEST test format, benchmark_test, abstracts the transaction gas limit cap for easier test implementation.
- There is still some ongoing work in this area.
- Related discussion: Issue #1926 – Comment

### Notes

- Mario: PR #2160 will update the EEST benchmarking test.
- No action needed from client teams.

## State-Intense Benchmarks

### Overview

**jochem-brouwer** raised the idea of benchmark tests using mainnet state snapshots:

- Create state events to benchmark.
- Target clients with large mainnet states.
- Working with Kamil from Nethermind.
- Would like to write more tests — please share any specific worst-case situations.
- Announcement: State benchmarks are coming soon.

### Questions from the EEST Side

- How are we approaching this?
- How will the big state be included in tests?

### Approach (Jochem)

- Need extra tooling (current one is CL mock).
- Spin up a node.
- On top of the snapshot, run tests generated by the tool.
- This tooling will be developed in collaboration with n/m.

**Pari:** Having a fully independent test would be nice to have.

XEN tests on mainnet: [PR #2101](https://github.com/ethereum/execution-spec-tests/pull/2101) (currently hardcoded addresses, not using stubs yet).

**Kamil:** There will be a separate tool but it will integrate.

**Andrewn & Pari :** “Snapshot” means [EthPanda Snapshots](https://ethpandaops.io/data/snapshots/); we will use that.

**Amezian:** How close are these to mainnet transactions?

**Jochem:** Mainnet for some situations.

- Wants to write more XEN test cases.
- Less SSTOREs and more SLOADs can be found related to mainnet.
- Please reach out with suggestions.
- Mario: We’d need an EIP for SSTORE.
- CPerezz: FYI, all of the cases in this HackMD doc will eventually land in EEST. Make sure whatever you propose is already there.
- Mario: Please add a PR to include your test cases into this list.

## Glamsterdam Testing Updates

- New consensus-specs release last Thursday: `v1.6.0-beta.0.

Justin: epbs-devnet-0 will be based on this release.

### BALers Be BALing

- Raxhvl provided an update on the state of BAL testing.
- BAL Devnet 0 Timeline: Notes
- Working on complex test cases.
- EIP-7702 is quite nuanced; system admin updates have been applied in the EIP.
- Bugs fixed and EIP updated.
- Close to 30 test cases under review.
- Would like to proactively run test cases.
- For questions, client teams should reach out to Raxhvl or Felippe.

**Toni:**

- BAL hash vs. root discussion — please check Discord or the breakout call.
- The change will be small but needs a decision; reach out to share your opinion.

**Mario Vega (chat):**

- BAL Devnet info: Notes

### eBPS

- epbs-devnet-0 (targeting end of Oct 2025): Notes
- Devnet slated for the end of October.
- Client branches will be added.

**Justin T:** Short recap of our breakout call this week: [Tweet](https://x.com/JustinTraglia/status/1971589863280402721)

- Clients are working on the devnet.
- Need devnet-0 branch for EthPandaOps.
- Working on implementing everything.
- Unsure about any metrics needed for eBPS.

(PS: This is a quick summary. For any edits, please leave a comment [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-55---Sep-29-2025).)

---

**system** (2025-09-29):

### Meeting Summary:

The team discussed updates on the Ethereum development network (DevNet) and its unfinality test, as well as the upcoming transition to Fusaka on the Holesky testnet. They reviewed progress on various projects including the Ethereum Execution Specification Tests (EEST) repository, state benchmarks, and the structure of their testing framework. The conversation ended with discussions on Block-level Access List (BAL) and Ethereum Proof of Stake (ePBS) specifications, including updates on testing and implementation plans.

**Click to expand detailed summary**

Mario led the meeting and discussed updates on the Ethereum development network (DevNet). pk910 explained that a new unfinality test was being conducted on DevNet 3, which was expected to last for 1-2 days. The test was requested by some clients to assess chain split scenarios. Mario asked if there were any action items for client teams, but pk910 did not provide specific details. Mario encouraged client representatives to share any findings or updates regarding DevNet 3 during the meeting.

The team discussed the upcoming transition to Fusaka on the Holesky testnet, scheduled for Wednesday. Parithosh reported that Holesky Shadow Fork was up and running, with some issues related to node peering. The team agreed to delay the mainnet Shadow Fork until mainnet releases are available. They also discussed client releases, with Pawan mentioning a new Lighthouse release. The team planned to verify the EEST client testnet configuration and update the blog post with the latest information. Parithosh provided a todo list for Holesky, including client releases, shadow fork, and node validation.

The team discussed updates on the Fusaka project, including the ongoing audit contest with two weeks remaining. They agreed to create a Fusaka directory in the PM repository, similar to what was done for Pectra, with Stokes volunteering to handle this task. The group also reviewed the status of 60 million gas limit activation across different clients, with Geth, Nethermind, Besu, and Riff confirming readiness for mainnet release, while testnets were already at this limit.

The team discussed updates to the Ethereum Execution Specification Tests (EEST) repository, focusing on restructuring benchmark tests into compute-intensive and state-intensive categories. Jochem presented progress on state benchmarks, explaining that new tooling is being developed with Kamil from Nethermind to test clients against large states, including mainnet state. The team is seeking input from clients about worst-case state management scenarios to create relevant tests, with the goal of updating gas limits and identifying optimization opportunities. Jochem clarified that these state benchmarks will be written in EEST and will use the ADDSTIP to target specific networks, with tests running on a mock chain that generates payloads for client performance testing.

The team discussed the structure of their testing framework, where EEST will handle test definitions while separate tooling (initially GAS Benchmarks) will manage test execution using custom VMs. Parithosh suggested making the tooling fully independent to allow integration with other tools, particularly for mock CL capabilities. The team clarified that test execution will use snapshots of the blockchain state, with the ability to revert to initial states after testing. Andrew inquired about the nature of snapshots, which jochem-brouwer explained involves specific block numbers and testnets. Ameziane raised a question about the similarity between SLOAD operations in mainnet transactions and the testing environment, noting that many SLOAD operations in the mainnet were zero reads, which the team acknowledged as something to consider in their testing framework.

The team discussed SLOAD performance issues, particularly on the Mainnet, with Jochem explaining that the problem is related to accessing non-existing slot keys and not dependent on contract size. Ameziane shared that Besu has optimizations for root hash calculation by preloading storage slots during transaction execution, and mentioned a pending PR to address a LuxDB bug related to zero reads. The team also explored the possibility of changing SSTORE to not check the current value for pricing, which Ben suggested could improve performance by reducing the most expensive part of SSTORE operations, though this would require an EIP and might affect state growth tracking.

The meeting focused on updates and discussions around Block-level Access List (BAL) and Ethereum Proof of Stake (ePBS) specifications. Rahul provided an update on BAL, highlighting the addition of complex test cases and the need for clients to share DevB branches for testing. Toni raised a discussion about potentially switching from a hash to a root-based BAL, which clients were encouraged to provide input on. Justin Traglia mentioned that ePBS DevNet Zero is scheduled for the end of October, pending client implementations and testing. The team also discussed the need for metrics in ePBS, with Katya raising the question. The conversation ended with a reminder about the upcoming activation in Holesky and a call for any additional topics.

### Next Steps:

- All client teams to ensure their Fusaka releases include 60 million gas limit support for mainnet.
- Client teams to provide ePBS devnet-0 branches to EthPandaOps for testing.
- Client teams to share Block-level access list dev branches with Rahul/Felipe for proactive testing.
- Alex to start the PR for moving Fusaka-related files to the appropriate folder in the Ethereum/PM repository.
- Client teams to review the list of test cases for state benchmarking and provide feedback if any scenarios are missing.
- Client teams to reach out to Jochem with ideas for additional state benchmarking tests, especially for worst-case scenarios.
- Besu team to address the missing test related to Block-level access list mentioned in Discord.
- Client teams to consider what metrics might be needed for ePBS testing.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: t$55RrLA)
- Download Chat (Passcode: t$55RrLA)

---

**system** (2025-09-29):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=zYcxqTAyWvc

