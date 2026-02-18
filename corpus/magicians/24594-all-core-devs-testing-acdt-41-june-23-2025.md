---
source: magicians
topic_id: 24594
title: All Core Devs - Testing (ACDT) #41 | June 23 2025
author: system
date: "2025-06-19"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-41-june-23-2025/24594
views: 84
likes: 2
posts_count: 3
---

# All Core Devs - Testing (ACDT) #41 | June 23 2025

# All Core Devs - Testing (ACDT) #41, June 23 2025

- June 23, 2025, 14:00 UTC

# Agenda

- Fusaka Devnet 2
- PeerDAS testing
- EIP-7907 and tests
- engine_getBlobsV2: `engine_getBlobsV2`: add `partialResponse` flag to enable partial hits by raulk · Pull Request #669 · ethereum/execution-apis · GitHub

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : ACDT
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1583)

## Replies

**system** (2025-06-23):

### Meeting Summary:

The meeting focused on the status of Devnet 2 and implementation progress of EIP-7907 across various client implementations, with most clients reporting readiness for testing except for Nethermind which was still working on implementation. The team discussed network performance issues during testing, identifying that full nodes consumed significantly more bandwidth than expected and agreed to analyze the report in detail to understand the root causes. They also addressed changes to the getBlobs API, timeline for testnet rollout, and conducted benchmarks on the Shadow fork of Mainnet, while discussing performance issues related to code size and state tests.

**Click to expand detailed summary**

The meeting focused on the status of Devnet 2 and the implementation of EIP-7907 across various client implementations. Barnabas reported that client implementations were still pending, with only Yaga completed, and launch was delayed to the following day. Several clients, including Besu, Erigon, and others, provided updates on their progress, with most reporting readiness for testing except for Nethermind which was still working on implementation. Jochem presented benchmarks for EIP-7907, and Barnabas noted that Berlin had already updated their CGC values, though the network was still under testing for stability.

The team discussed network performance issues during testing, where full nodes consumed significantly more bandwidth than expected, with some clients using up to 80-100 megabits per second compared to 20 megabits for others. They identified that network traffic scaled linearly with the number of blocks, though Raúl noted this might be due to recent optimizations and suggested further investigation of the networking stack implementations. The team agreed to analyze the report in detail and coordinate with the Sunnyside labs team to understand the root causes of the high network usage.

The team discussed changes to the getBlobs API, ultimately deciding to remove the partial response flag and make partial responses the default behavior, as proposed by Marius. They also addressed the timeline for testnet rollout, with Barnabas indicating that they need a stable spec before conducting performance tests. The group agreed to continue working on identifying networking bottlenecks and implementing optimizations, with Raúl emphasizing the importance of benchmarking in realistic scenarios. They plan to review the results of Devnet 2 before making further decisions about the BPO numbers and testnet rollout.

Jochem and Marius conducted benchmarks on the Shadow fork of Mainnet using a gas limit of 30 million for transactions targeting six contract sizes, including small and large contracts. They observed slower execution times for larger contracts, with the worst case taking almost a second for statical big contracts. Łukasz explained that performance could vary based on hardware and optimization strategies, while Ansgar emphasized the need for standardized behavior across clients regarding the use of an index for contract size, expressing concerns about its interaction with future features like ZK proofs.

The team discussed performance issues related to code size and state tests, with Ameziane inquiring about triggering tests after pushing changes to the performance branch. Jochem explained that state tests should be run against the fixtures, and Mario suggested summarizing the list of tests run in perfnets. The group agreed to continue using the current state of the EIP for Devnet 2, with plans to reassess and potentially make final changes to the EIP either during ACDE or asynchronously. Łukasz expressed concerns about including 256 kB code size information in the EIP, but the team decided to proceed with the current specification for Devnet 2.

### Next Steps:

- Jochem to add 7907 benchmarking tests to the state test fixtures.
- Jochem to summarize and share the list of tests run in the perfnet for 7907 benchmarking.
- Client teams to implement and test Devnet 2 with current EIP-7907 specification (256 KB max contract size).
- All teams to reassess EIP-7907 after Devnet 2 launch and provide feedback on any necessary changes.
- Raul to update the PR for get_blobs_v2 to remove the partial response flag and change the default behavior to return partial responses.
- Peer-to-peer networking team to analyze the Sunnyside Labs report on network usage and investigate potential bottlenecks.
- Client teams to continue working on implementing and optimizing EIP-7907, considering the benchmarking results presented.
- All teams to discuss and decide on standardized behavior for the code size index across all clients before Cancun rollout.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: xCyP%s24)
- Download Chat (Passcode: xCyP%s24)

---

**system** (2025-06-23):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=3mnaILTNk6w

