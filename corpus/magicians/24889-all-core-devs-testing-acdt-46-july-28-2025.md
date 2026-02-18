---
source: magicians
topic_id: 24889
title: All Core Devs - Testing (ACDT) #46 | July 28 2025
author: system
date: "2025-07-22"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-46-july-28-2025/24889
views: 174
likes: 2
posts_count: 7
---

# All Core Devs - Testing (ACDT) #46 | July 28 2025

# All Core Devs - Testing (ACDT) #46 | July 28 2025

- July 28 2025, 14:00 UTC

# Agenda

- Fusaka updates
- Gas limit testing updates

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : All Core Devs - Testing
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1634)

**YouTube Stream Links:**

- Stream 1 (Jul 28, 2025): https://youtube.com/watch?v=Xc0eg8s71c4

## Replies

**abcoathup** (2025-07-25):

### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png)

      [All Core Devs - Testing (ACDT) #46 | July 28 2025](https://ethereum-magicians.org/t/all-core-devs-testing-acdt-46-july-28-2025/24889/5) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACD Testing Call #46 - Quick notes.
> Moderator: Parithosh Jayanthi
> Next Steps
>
> Devnet 3
>
> Network is live.
> Launch BPO-4 tomorrow to reduce blob count.
> Continue investigation into Nimbus peering and orphan block issues (Pari, Bharath).
> Barnabas to share async notes.
>
>
> Eth Config
>
> Danno to update PR removing JSON hash from eth_config.
>
>
> Gas Limit Testing
>
> Alexey to analyze secp256r1 gas pricing.
> Teams to report peer-related anomalies; Marius to review Geth behavior with PR logs.
> Investigate Netherm…

### Recordings/Stream

- YouTube
- X- Livestream  [ x.com/echinstitute]

### Writeups

- Tweet thread by @poojaranjan

### Additional info

- Fusaka upgrade:

Ideally targeting mainnet before Devconnect
- Current devnet: fusaka-devnet-3 [specs]
- CLZ benchmark results

EEST benchmark [v0.0.3](https://github.com/ethereum/execution-spec-tests/releases/tag/benchmark%40v0.0.3)

---

**system** (2025-07-28):

### Meeting Summary:

The team reviewed the status of the Fusaka Devnet 3 and discussed various technical issues including peering problems, orphaned blocks, and registration workflow challenges. They addressed concerns about JSON-RPC response hashing and agreed on standardizing precompiled contract addresses, while also discussing peer connectivity issues on Mainnet and blueprint project updates. The team reviewed benchmarking results for client execution times and discussed state growth testing, with several team members reporting progress on devnets and ongoing investigations into various technical implementations.

**Click to expand detailed summary**

The team discussed the status of the Fusaka Devnet 3, which went live last week with 18 BPOs and 30% gigabit nodes. They identified issues with Nimbus and Nimbus EL clients experiencing peering problems, and discussed an unusual pattern of orphaned blocks due to delayed column propagation. Bharath provided updates on the MAP workflow, noting that 672 validators were registered out of 818, and highlighted two ongoing issues: timestamp problems with Lodestar registrations and state root mismatches for Nimbus block publishing. The team also discussed the implementation of private block mempools and the need to test the new configuration checks in EIP-2384.

The team discussed concerns about hashing JSON-RPC responses, with Marius expressing that the current method using RLP is brittle and suggesting alternatives like RRP. Danno agreed to remove the hash from the specification, and Parithosh confirmed that an updated PR would be submitted incorporating the EIP and execution API changes. The team also aligned on normalizing keys and values in addresses for precompiled contracts, with Danno proposing to standardize the format to “precompile:name:address” and Mario agreeing to this change.

The team discussed ongoing issues with peer connectivity on Mainnet, where Alexey and Marius reported seeing decreased visibility of peers, which Csaba attributed to recent changes in node connection logic. The team agreed to investigate further, with Csaba requesting more details about the timing and specific issues. Carlos presented updates on the blueprint project, requesting reviews of two documents containing test cases and questions for finalization, which the team agreed to review. The team also discussed the timeline for testing, with Stokes indicating they should move forward as soon as possible, pending resolution of Nimbus and map workflow issues.

Marius explained that a memory issue on Bloatnet was caused by Geth ignoring tracing flags, resulting in excessive memory usage and node crashes. The problem was resolved by updating to the current master branch, which fixed an outdated image issue. They are also reworking the tracing to use less memory. CPerezz asked about the database’s maximum payload capacity, but Marius clarified that this was a separate issue related to the log indexer. Parithosh mentioned he had started re-syncing the node with the fried database.

The team discussed state growth and state root computation testing, with Mario expressing interest in working on computationally intensive benchmarking tests. They agreed to test with a blocknet state size of 2x mainnet, with plans to expand to larger state sizes in the future. Parithosh mentioned the Netherland team’s use of a specific file system for quick snapshot copying and reverting, which could be useful for gas benchmarking and Yields integration. Mario reported a new release of benchmark tests in East, which includes a consolidated genesis file for Nevermind tool integration, though some updates to benchmark tests are still needed.

Louis presented benchmark results for calculating leading zeros in code, comparing different gas costs and transaction limits. He explained the test setup, which includes filling test cases and running benchmarks with various client configurations. The results showed that with a gas cost of 5, both 72 and 100 million gas transactions were successfully completed. The team noted that the current gas cost of 5 might be slightly conservative, but the results were still acceptable.

The team reviewed benchmarking results showing client execution times below 4 seconds without warming up, with an open issue raised for adding warming up functionality later. They discussed maintaining the current status quo of 5 clients while considering repricing in the next fork, and Mario suggested implementing EELS methodology for future hard forks. Minhyuk reported progress on two devnets, including tests with regular transactions and a 16-node network with data column propagation, while noting some issues with Teku’s backfill implementation that required further investigation with the Teku team.

### Next Steps:

- Client teams to focus on investigating the orphaned block issue and any client-specific bugs found in Fusata Devnet 3.
- Parithosh to make a post on the interop channel regarding the plan for the next phase of testing.
- Client teams to reach out if they notice any peering issues with their nodes on mainnet.
- Csaba to investigate potential peering issues related to recent Geth changes.
- Nethermind, Besu, and Aragon teams to review the document shared by CPerezz regarding test cases for Bloatnet.
- CPerezz to follow up asynchronously with Kamil regarding the integration of Yul’s with the gas benchmarking tool.
- Client teams to engage with the two open metrics PRs.
- Client teams to review the hack.md document shared by Carlos.
- Danno to update the PR for the EIP and execution API regarding the eth_config changes.
- Client teams to check if they are ready for backfill implementation and reach out to Sunnyside Labs for testing if needed.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: .r4Fl55U)
- Download Chat (Passcode: .r4Fl55U)

---

**system** (2025-07-28):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=Xc0eg8s71c4

---

**poojaranjan** (2025-07-28):

# ACD Testing Call #46 - Quick notes.

Moderator: Parithosh Jayanthi

### Next Steps

- Devnet 3

Network is live.
- Launch BPO-4 tomorrow to reduce blob count.
- Continue investigation into Nimbus peering and orphan block issues (Pari, Bharath).
- Barnabas to share async notes.

Eth Config

- Danno to update PR removing JSON hash from eth_config.

Gas Limit Testing

- Alexey to analyze secp256r1 gas pricing.
- Teams to report peer-related anomalies; Marius to review Geth behavior with PR logs.
- Investigate Nethermind peer discovery issue (Csaba, Raul).

BloatNet

- Geth team to finish tracing/memory fix.
- Client teams to review Cperezz’s test plans and align with EELS integration.

Benchmarking

- Mario to finalize EEST benchmark tests and resolve blockers.

Sunnyside Labs

- Continue large block size propagation tests.

## Fusaka Devnet 3 Updates

Parithosh shared:

- Devnet 3 launched late last week.
- Network is finalizing with 3 BPOs already completed.
- Live tracking: Dora Explorer
- Blob Configuration**

Currently running at 18 blobs per block.
- BPO-4 will reduce blob count (currently at 18 blobs/block).
- BPO-4 expected to go live tomorrow.

Added rate limiters:

- 30% nodes are gigabit “super nodes”
- Rest are 100 Mbps down / 50 Mbps up
- Based on EIP-7870

Validator Key distribution is uneven; staking top-ups added for addditional test coverage.

- Network includes every client pair.
- Top-ups used to normalize validator stake across the board.

Clients experiencing:

- Nimbus EL/CL unable to connect to bootnodes
- Higher-than-expected orphan blocks (no pattern, possibly MEV-related)

MEV updates (Bharath):

- 672 validators have successfully registered for MEV.
- Block delivery confirmed from the latest slot.
- Investigation ongoing into node connectivity issues:
- Initial findings point to a problem with Lodestar.

Block publishing for Nimbus is currently failing
- other than these two issues, regular blocks are being delivered consistently.
- MEV Relay Dashboard

**Other discussions**

- Manu: Do all nodes have the same rate limiting, or does it depend on the node type?
- Pari: It depends. Full nodes are capped at 100 Mbps, while super nodes have more. All specs are per EIP-7870. If those limits prove insufficient, we’ll flag and evaluate adjustments.
- Pari: Nimbus EL + CL clients are facing peering issues, unable to connect to bootnodes. Bharath will investigate this asynchronously.
- Pari: There’s a higher-than-expected rate of orphan blocks. No consistent client is at fault — random distribution, no clear pattern. The only major change from previous devnets is the presence of MEV.
There was an issue where aclient block tried to build on an old parent. Root cause is still unclear. Block link

### Next steps:

- Bhartah will continue to investigate Nimbus and other issues.
- Barnabus will share his notes async.

## Eth Config Discussion

- Mario

Noted that eth_config is now available.
- Testnet and mainnet configurations need to be reviewed.
- EEST (Execution Engine Spec Tests) should understand the config; queries can be placed during the testing phase.

Pari: Asked if **RLP serialization is in progress**.
Marius

- Raised concerns about hashing JSON-RPC responses.

If all clients return the same JSON-RPC result, it can become brittle.
- Suggested we find a better way to hash the data.

Prefers **RLP**, but open to **SSZ** if other clients prefer it.

Danno

- Questioned use of RLP: “If we shouldn’t use RLP, why go that route?”
- Later suggested dropping the hash entirely.

Tim Asked: “Why are we not supposed to use RLP?”
Roman: Clarified that the **Execution Layer (EL)** currently **only supports RLP**, not SSZ.

- Said dropping the hash might complicate things for testing teams.

Mario Vega: Suggested testing teams can **perform the hashing themselves** if needed.

- Referenced EIP-specified JSON standardization: RFC 8785.
- Personally liked the idea of including the hash.

Danno: Mentioned another change
Pari: Confirmed it seems like a similar change; **no objections** from the group.
**Danno will include the change** in the updated PR.

### Decision:

- Drop the hash from the config.
- Danno will update the PR accordingly.

## Next Phase Testing  - Timeline Discussion

Pari mentioned

- Shadow fork and large testnet are in planning.
- Reference doc: Fusaka Devnet 3 Notes
- Alex stokes: Urged to begin the next phase of testing as soon as possible.
- Pari: Emphasized that client teams should focus on orphan block issues and other topics discussed earlier in the call.

## Gas Limit Testing Updates

- Pari updated

Mainnet is currently running at 45 million gas with no major issues noted.
- Investigation into Consensus Layer (CL) validator behavior is underway, and analysis will be shared soon.

Alexey

- Plan to check the real gas cost of secp256r1 this week.
- Expressed doubt about time availability to update the pricing if anything significant is found.
- Asked if other clients observe similar behavior; requested that findings be reported.

**Peering Issues**

- Marius van der Wijden

Geth team is also looking into the issue.
- Shared a theory: a Geth-specific peering optimization might be causing issues for other clients.
- Shared a PR for adding debug logging:

go-ethereum PR #32287 – Add more debug logs

Csaba

- Highlighted a peer discovery issue involving the Nethermind client.
- Problem appeared about 5 days ago.
- This testing has only been live on mainnet for less than a month, so needs further understanding.

Raul

- Suggested sharing peer IDs to investigate potential common patterns.

Pari

- Both Nethermind and Geth issues appear to be unrelated to the 45M gas limit setting itself.

## BloatNet Testing Discussion

- Cperezz

Shared context and resources:

BloatNet HackMD 1
- BloatNet HackMD 2
- Go-Ethereum Issue #32290

Plans to expand testing with support from additional teams.
Requested **review from client teams** to grow BloatNet testing coverage.
Raised the question: **Can we align with the EELS team** on state-growth-related tests?

- Related EEST GitHub Issue #1923

Noted: EELS will be integrated with spammer for better testing.

Marius van der Wijden

- Reported a serious issue on BloatNet with Geth:

When Geth detects a state change, it tries to dump all states.
- This behavior consumes a lot of memory, causing nodes to crash.
- Geth had 55 node crashes, and the database got corrupted.

**Root cause**: nodes **ran out of memory** during tracing.
Fixes implemented:

- Working on tracing with less memory usage.

Shared infrastructure resource usage:

> “We allocated ~10TB because of tracing and

Pari

- Confirmed resyncing the node from the corrupted database has been started.
- Will investigate tracing issues further.

Mario

- Commented on the limitations of state growth testing:

Tests produced cannot contain very large state due to technical constraints.
- Most current tests are computationally intensive rather than focused on state growth.

Highlighted the need for **state-specific benchmarking**.

Cperezz (follow-up)

- Emphasized that the new tests are more state-related.
- Ideally, such tests should be executed using BloatNet state.

Marius van der Wijden

> “It would be ideal to write the tests in a way so they can be replayed on arbitrary networks.”

- Pari

Shared that the Nethermind team has started EELS integration.
- Suggests continued asynchronous coordination on integration efforts.

## EEST Integration, Benchmarking, and Testing Reports

- Mario

Announced a new release: EEST Benchmark v0.0.3, which includes all benchmark tests.
- Noted that Nethermind tools can now use genesis files.
- Stated that genesis will be the starting point for future benchmarks.
- Shared that this is still a work in progress.
- Blocker: All benchmarks still need to be functional and verified.

## CLZ Benchmark Results

- Louis

Presented findings via this slide deck.
- Shared methodology and test notes.
- Tests based on EIP-7825 and focus on worst-case block sizes.
- Two gas limit scenarios tested: 72M and 100M.
- Call participants were generally supportive of the CLZ benchmark methodology.

Pari

- On reducing gas pricing, he recommended sticking to 5.
- Mentioned the intent to reduce pricing in the upcoming Glamsterdam fork.

Mario

- Noted the benchmarking methodology:

> “Use EELS first, then test across client implementations in future forks.”

## Sunnyside Labs Testing Update

- Minhyuk (Sunnyside Labs)

Provided a progress update:

Running two testnets with regular transactions to monitor how larger block sizes affect network data propagation.
- Began test execution.
- Teku is currently the only client supporting backfill, though some issues remain.
- Team is working on resolving backfill issues and aiding with broader test coverage.

Report will be **shared on Discord** once ready.
Confirmed that the **Perfect Column Devnet** appears to be **functioning correctly at first glance**.

Any corrections tothe notes, please [add here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-46---July-28-2025)

---

**cskiraly** (2025-07-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Csaba
>
>
> Highlighted a peer discovery issue involving the Nethermind client.
> Problem appeared about 5 days ago.
> This testing has only been live on mainnet for less than a month, so needs further understanding.

Quick correction: I did not highlight the issue, just heard about it in the call.

Regarding the specific dial improvement mentioned:

PR: [p2p: Filter Discv4 dial candidates based on forkID by cskiraly · Pull Request #31592 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/pull/31592)

Background to change

- Geth collects dial candidates from 3 sources: discv4, discv5, DNS
- Specific to discv4, when we learn about nodes, we don’t know anything about the network or fork ID they are on (in discv5 we have this info).

What changed in Geth

- Before the change, specific to discv4, we were dialing many nodes, just to then figure our they are not compatible. This is less of an issue on Mainnet, more a problem on smaller networks where a large part of dials would be useless.
- After the change, for the peers discovered over discv4, we do an EnrRequest first, and only dial if it would make sense (an ENR with compatible network and fork ID received).
- This saves quite some outbound TCP dial traffic for us, and quite some inbound traffic for nodes on other networks (while it is adding a UDP exchange).

This should not create issues, except if there is a problem with the ENR exchange. I think (not yet sure) this was the problem, the EnrRequest - EnrResponse exchange failing between the two client implementations for some reason.

Note that this only influences our outgoing connections. Peers can still dial us as before.

---

**poojaranjan** (2025-07-29):

[@cskiraly](/u/cskiraly) Appreciate adding details ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

