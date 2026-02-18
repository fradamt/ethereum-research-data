---
source: magicians
topic_id: 24768
title: All Core Devs - Testing (ACDT) #44 | July 14 2025
author: system
date: "2025-07-09"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-44-july-14-2025/24768
views: 161
likes: 4
posts_count: 6
---

# All Core Devs - Testing (ACDT) #44 | July 14 2025

# All Core Devs - Testing (ACDT) #44 | July 14 2025

- July 14 2025, 14:00 UTC

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

[GitHub Issue](https://github.com/ethereum/pm/issues/1609)

**YouTube Stream Links:**

- Stream 1 (Jul 14, 2025): https://youtube.com/watch?v=8tz5ZkMygEE

## Replies

**poojaranjan** (2025-07-14):

# ACD Testing Call #44 - July 14, 2025 (Recap)

**Facilitator:** Parithosh Jayanthi

**Links:**

- Fusaka Devnet 3 EIP PR #9981
- Sunnyside Labs Testing Update
- engine_getBlobsV3 PR #674
- GetPayload builder-specs PR #123

## Fusaka Devnet 2 Updates

**Barnabas** provided an update:

- Reaching out to client teams
- No major bugs reported
- eth-das-guardian tool is now in active use

## Gas Limit: 45 Million

- Nimbus and Lighthouse have released specs with the 45M gas limit
- Prysm, Lodestar, and Grandine to release later this week
- Clients are aligning around 45M → up from 36M

## Fusaka Devnet 3

- PR open: EIP #9981
- Awaiting broader approval — Raul has approved
- BPO EIP is no longer part of Devnet-3 but for the main fork
- Next: Merge remaining 2 PRs and set timeline post EIP-7907 decision

## EIP-7907: Raise Code Size Limit (Jochem’s presentation)

Proposal to increase code size limit from **24 KiB to 48 KiB**

**Highlights:**

- Increases the contract code size limit introduced in EIP-170 and adds a gas metering to code loading
- Warm vs. cold code state
- Benchmarks at 100M to be collected and presented by ACDE. Client teams are to have an opinion about implementation difficulty for indexes as well as a timeline estimation by ACDE.

**Concerns raised:**

- Bigger witness sizes
- Gas cost implications
- Implicit codeHash behavior
- Risk of increased technical debt
- Likely to break some existing contracts

**Comments:**

- Mario: Underspecified
- Marius: Has concerns
- Charles: Large contracts may be more expensive
- Pari: Further discussion planned for ACDE
- Pari: If Fusaka is planned before Devconnect, the focus should be on hardening specs.

## Other Gas Limit Discussions

- Two targets in EIPs: 45M and 16M
- Milen (Erigon): Asked how large contracts deploy with 16M
- Pari: Will evaluate in the future
- 45M Gas target is part of Devnet 3

## Related PRs for Review

**Flagged by Barnabas:**

- engine_getBlobsV3 (partial return)
- GetPayload update (remove execution payload/blob bundle)

## Sunnyside Labs – Devnet Testing Update

- Ran across all CL and EL clients
- CL tested with up to 60 blobs/block
- All clients supported 72 blobs
- Testing state is strong; recommend spec hardening next

Recap from earlier meetings -  [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2).

---

**jochem-brouwer** (2025-07-14):

Slides of my presentation can be found here: [All Core Devs - Testing (ACDT) #44 | July 14 2025 · Issue #1609 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1609#issuecomment-3069923114)

---

**system** (2025-07-14):

### Meeting Summary:

The team discussed updates on various projects, including Fussaka participation, bug fixes, and ongoing development work. They addressed challenges related to code size limits, contract deployment, and gas costs, with a focus on balancing flexibility and efficiency. The meeting also covered Devnet 3 planning, execution API updates, and recent testing results, emphasizing the importance of continued stress testing and performance benchmarking.

**Click to expand detailed summary**

The team discussed updates on Fussaka, where Barnabas reported 95% participation and addressed client-specific issues with editors and document proposals. They reviewed recent bug fixes, including a Nimbus issue with verifyCellKzgProofBatch and a new consensus spec PR from Leo that adds test types, which Justin and the CL teams will review. Barnabas mentioned ongoing work with a new tool called Eth-DAS-Guardian to help debug metadata fields and status messages, and Parithosh noted that sync tests were proceeding well, with plans for more stable testing by the end of the week.

The team discussed several updates and issues related to GitHub actions, MEV workflows, and Devnet coordination. Bharath provided an update on the MEV workflows, mentioning that the code for the first map boost and relay is ready for review and local testing, but there are some dependency issues with IP7.9.0.7 that need to be resolved. Parithosh suggested deploying a fork of the unmerged code to catch bugs earlier if the dependency issues are not fixed. The team also discussed the progress of releases for different CLs, with Lighthouse and Members having released updates, and other clients like Prism, Lodestar, and Grindine planning to release soon. Barnabas explained the changes to the blob transaction limit, removing it from the blob schedule configuration and hard-coding it instead. Jochem presented on the challenges of raising the code size limit for EIP-7907, scheduled for inclusion in Fussaka, highlighting the complexity of the issue.

The meeting discussed the challenges and considerations around pricing and structuring contracts for code deployment, particularly focusing on gas costs and contract splitting. Jochem Brouwer highlighted the complexity of pricing based on worst-case scenarios and the implications for existing contracts, emphasizing the need for a balance between flexibility and cost efficiency. The group also addressed the overhead of calling contracts and the trade-offs involved in optimizing code deployment. There was a consensus on the importance of considering shared code between contract paths and the potential impact on gas usage. The discussion concluded with a focus on addressing concerns about pricing structures and ensuring that contracts are designed to handle various scenarios effectively.

The team discussed concerns about code size data structures and implementation details for clients. Guillaume and Charles explained that while code chunking could be implemented in the future, it would require significant changes and might not provide the expected benefits. The group agreed that every client would need to build a code size index, even if it remains an implementation detail. Ansgar pointed out that existing contracts don’t need to be updated with the new code size information, as it would only be relevant for contracts created after the fork boundary.

The team discussed contract size limits and performance concerns. Ansgar explained that contracts need to be below 24kB and suggested making it a hard requirement to have high-quality benchmarks showing all clients can handle worst-case load patterns before finalizing the 7,907 info decision. Parithosh mentioned this topic would be presented at ACDE for further discussion. Draganrakita and Marius raised concerns about DDoS attack handling and the reliability of current performance tests, with Marius noting that tests for large contract loads could pull up significant amounts of data, making it difficult to predict real-world performance.

The team discussed concerns about contract size limits and gas costs, particularly focusing on a proposed increase to 24kB and its implications. Marius raised concerns about gas costs per word being too high, while Charles noted that loading large contracts would be more expensive with the new EIP. The team confirmed that no contracts above 24kB were created before the limits were implemented. They agreed to collect benchmarks for performance at 100M gas, with Jochem assigned to gather these benchmarks. The discussion also touched on the impact of a potential future transaction gas limit reduction to 16M, with Milen questioning the feasibility of deploying large contracts under such constraints.

The team discussed updates on Devnet 3 planning, with Barnabas noting that three PRs need to be merged before launch. They reviewed the status of the execution API EIP regarding partial responses, which Raúl reported is awaiting final approvals from EL and CL developers before merging. The Sunnyside Labs team presented their latest testing results, showing improvements in block throughput and network performance across various node configurations. The team agreed to continue stress testing and interrupt testing, with Raúl providing feedback on additional test scenarios to make the benchmarks more realistic.

### Next Steps:

- Client teams to come to ACDE with an opinion on how difficult it would be to implement the index for EIP-7907.
- Client teams to come to ACDE with an assessment of whether large contract sizes would be problematic for their implementation.
- Client teams to provide benchmarks at 100 million gas limit to ensure no new bottlenecks are introduced.
- Client teams to implement and test the 16 million transaction gas limit for Devnet 3.
- EL and CL developers to review and approve the execution API EIP for partial responses before Thursday.
- Sunnyside Labs team to add default spammer transactions to their next round of benchmarks.
- Raúl to send feedback to Sunnyside Labs team on additional testing scenarios (including bandwidth constraints, node profiles, backfill tests, latency distributions, and gossip sub parameter adjustments).
- Client teams to focus on hardening their implementations for Cancun by testing edge cases and continuing stress testing and interop testing.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 0#dupCDn)
- Download Chat (Passcode: 0#dupCDn)

---

**system** (2025-07-14):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=8tz5ZkMygEE

---

**meetrick** (2025-07-17):

# 1. Fusaka Update

The Fusaka update is progressing smoothly with roughly **95% participation** so far.

- Progress and Issues: Consensus Layer (CL) teams have deposited additional funds to test coupled validators and CL clients. Some issues were found and shared with all client teams. They were asked to verify and inspect if validators fail to reach the head or miss proposals.
- Bugs and Debugging Tools: A metadata-related bug discovered in Teku is under investigation, supported by a new debugging tool called ‘eth-das-guardian’. This tool helps identify minor issues by analyzing metadata fields and state messages from specific CL clients. Long-term, it’s expected to be a third-party data source for analyzing dependencies between two clients and will be integrated into Dora to help client developers track network issues more easily.
- Other Updates: A minor issue with the Nimbus client has been fixed, and a new consensus spec issue (where the verify_kzg_proof patch wasn’t being properly verified) has also been resolved. Liao’s Pull Request (PR) added some new test types, and Justin and the CL team have been asked to review them.

# 2. Sync Test Progress

Sync tests generally look good, but current limitations in test conditions mean it’s too early to draw major conclusions.

- Stability Goal: The expectation is to have very stable Sync tests by the end of this week.
- Test Repository: The Sync test repository is public and is automatically triggered daily via GitHub Actions to confirm if each client passes or fails the tests.
- IOPS Limitations: Currently, GitHub runner’s Input/Output Operations Per Second (IOPS) limitations are causing timeouts after two hours. Test failures due to this are not related to actual performance, so results should only be considered for reference. Once the infrastructure improves, comparisons of test speeds will be possible.

# 3. MEV (Maximal Extractable Value) Test Update

Barat shared updates on the MEV workflow.

- Code Status: The MEV-boost and MEV-boost relay code has been reviewed by Justin and found to be fine. The Builder has been temporarily implemented to work in local and Kurtosis environments, and blob generation has been confirmed in local environments.
- Compatibility Issues: There are currently breaking changes between Reth and Alloy, making widespread deployment on DevNet challenging. Specifically, Reth, which is used in the Fusaka DevNet-2 branch, conflicts with EIP-7907 and is not working. This is being addressed based on Roman’s proposal.
- DevNet Deployment Plan: If these dependency issues are resolved while DevNet-2 is active, deploying unmerged fork versions for testing purposes to catch bugs early is being considered. However, if the issues persist, these changes will be prepared for the DevNet-3 release.

# 4. State Bloat Network and Gas Limit

The State Bloat Network operated stably over the weekend. This testnet simulates mainnet conditions by increasing the state size.

- State Size Goal: A minor issue found in Nethermind is under investigation, and the goal is to reach a state size twice that of the mainnet soon.
- Metric Coordination: A Telegram group is active to coordinate the different metrics and data types each client needs to collect, and client teams’ cooperation has been requested.
- Gas Limit Settings Status: Lighthouse completed its release last week, and Nimbus has also released. Relay API analysis shows approximately 41% of nodes are set to 45 million gas, about 50% to 36 million gas, and some to 30 million gas. These values are expected to be refined within a few days. Prism, Lodestar, and Grandine are scheduled for release this week or early next week.
- Blob Transaction Limit PR: The PR to remove the maximum number of blobs per transaction limit for Fusaka DevNet-3 has not yet been merged and is awaiting approval. This PR aims to remove this limit from the blob schedule configuration and move it to a fork-level setting rather than a BPO (Blob Parameter Only) setting. Approval from at least EIP authors Mark or Raul is needed, and feedback from other Execution Layer teams is welcome.

# 5. EIP-7907: Code Size Limit Increase Discussion

Yokum presented on **EIP-7907**. This proposal aims to increase the current 24KB contract code size limit to 48KB and introduce a dynamic metering formula that charges additional fees for code exceeding a certain size.

## 5-1. Proposal Details

- New State Introduction: Previously, only warm/cold states existed for accounts. EIP-7907 introduces cold/warm states for code as well. When code is read for the first time, it transitions from cold to warm, costing 2,100 gas.
- Dynamic Fee Imposition: This fee formula only applies when reading contracts larger than 24KB. Specifically, an additional 4 gas is charged for every 32 bytes (word) exceeding 24KB.
- DoS Risk: Since code size cannot be read directly from the Merkle Patricia Tree (MPT), verifying it requires first opening the account in the MPT, reading the code hash, and then looking up the actual code. This complex and resource-intensive process creates a potential attack surface for DoS (Denial of Service).
- Proposed Solutions: Suggestions include introducing an implicit or mandatory lookup cache for code hash to code size lookups, or even including code size directly in the account structure.

## 5-2. Yokum’s Main Concerns

- Introduction of Implicit Cache Structure: Incorporating new data structures like a lookup cache into a network upgrade without explicit consensus is unprecedented and could cause confusion.
- Economic Impact: If every contract call requires loading the entire code, incurring additional costs, it might incentivize developers to needlessly split contracts. For instance, even simple, frequently called methods like transfer() in ERC20 would incur the cost of the entire contract, leading to a poor user experience and increased burden for developers. This is essentially a form of coding memorization, potentially conflicting with the “pay-as-you-go” principle.
- Potential for Future Strategy Changes: Concerns were raised that if the strategy changes in future upgrades like Glammsterdam, the currently introduced fee formula could become ‘code debt’ and a long-term burden.
- Gas Pricing Uncertainty: It’s difficult to determine if the rate of 4 gas per 32 bytes is appropriate; it could be excessive or insufficient.
- EOA Issues: Sending Ether to an Externally Owned Account (EOA) without code could still incur an unnecessary 2,100 gas for the cold → warm transition.
- Increased Test Complexity: The introduction of warm/cold states for both accounts and code could make the testing structure highly complex and increase costs.

Yokum emphasized that while the 24KB limit is indeed too small and needs to be raised, sufficient consideration of side effects and a cautious approach are necessary.

## 5-3. In-depth Discussion and Feedback within the Developer Community

- Opposition to Fee Structure: With EIP-7907’s dynamic metering, loading a 256KB contract could incur an additional 30,000 gas. Some participants highlighted that if fees are based on such large contracts, it would create an excessive cost burden rooted in a worst-case scenario, potentially hindering the execution of existing contracts.
- Lookup Cache Design: Some client teams proposed storing code size in an account field, bytecode, or a separate table. This approach is much faster than tree traversal, and Ben even suggested removing the current static gas cost.
- Effectiveness of Contract Splitting: Charles and Ben pointed out that splitting contracts is not easy for developers, and in practice, it might be more beneficial to expand contracts despite the gas costs. Especially for shared code like ERC20, splitting can lead to code duplication and reduced efficiency.
- Need for Code Chunking: Code Chunking is essential for Zero-Knowledge Virtual Machines (ZKVMs); without it, significant bottlenecks can occur on the prover side. Accordingly, EIP-2926 has been reactivated, and it was suggested that chunking could be implemented with minor tree changes. Some participants argued, “If the code structure will change to accommodate ZKVMs anyway in the future, let’s design it properly from now.”
- Client Opinions: Mario felt that EIP-7907 hasn’t been analyzed enough and deploying it in an unclear state is risky. Ansgar explained that since most contracts are currently under 24KB, there’s no need to initialize the entire index.
- Importance of Benchmarking: Ansgar strongly insisted that before introducing EIP-7907 to Fusaka Devnet-3, all clients must secure benchmark results demonstrating their ability to handle worst-case patterns under those conditions. If the results are negative or not ready in time, EIP-7907 should be withdrawn.

## 5-4. Future Tasks

The next ACDE meeting will involve further discussion based on the following data points:

- Benchmark results at a 100 million gas limit.
- Opinions from each client team regarding the difficulty of index implementation.
- Feedback on the potential for issues with large contract sizes.

**Specific benchmark scenarios**

(1) Calling 36,000 contracts per block under a 100 million gas limit, with each contract triggering **jumpdest analysis**.

(2) Loading and calling a contract chain with a depth of 1,024 into memory. (3) Comparative testing with and without a code size index.

(4) Cases where contract calls roll back due to insufficient gas (demonstrating the need for an index).

# 6. DevNet-3 Plan and Key Tasks

Regarding the DevNet-3 release schedule, one of the most critical issues is the adoption of EIP-7907. This decision is a major variable determining whether it will be included in DevNet-3.

- Repricing EIP Implementation Status: How much each client team has implemented various repricing-related EIPs is also a crucial factor for DevNet-3 preparation.
- Spec Sheet Status: The DevNet-3 spec sheet is mostly updated, with only three more PRs needing to be merged before it’s ready for release.
- Already Merged PRs: The block limit-related PR, which limits the maximum number of blobs per transaction, has already been merged.
- Remaining Key PRs: One unmerged PR involves changes related to the Execution API, adding partial responses functionality. This PR was discussed at last week’s ACDC meeting and is currently awaiting approval from more EL and CL developers. Once approved, the Execution API spec can be frozen.
- Estimated Release Time: A final decision on EIP-7907 at this week’s ACDE meeting will clarify the specific release timing and progress schedule for DevNet-3.

# 7. Sunnyside Labs Latest Test Results

The Sunnyside Labs team presented the latest test results conducted on DevNet.

## 7-1. Test Summary

- Test Environment: Tests were performed with 8 validators and full nodes across all CL/EL combinations except for Nimbus CL.
- Block Processing Performance: All CL networks stably processed over 60 blobs per block. Nimbus improved its block processing rate from 9 in previous Berlin tests to over 40. All EL clients were able to process over 72 blobs per block.
- Maintaining Stable Blob Throughput: Even in tests with 128 nodes configured in various combinations, an average throughput of about 60 blobs per block was stably maintained for 48 hours.
- Network Bandwidth Limitation Test (30Mbps): A single CL network recorded about 60 blobs per block, while the 128-node configuration recorded about 45. The main factor limiting throughput in this test was short bursts of network traffic.
- Genesis Sync Test: All CL and EL clients, except Geth, passed the test. Geth is currently reviewing its fixes.
- Future Test Focus: The next steps aim to enhance the robustness (hardening) of CL and EL for Fusaka through edge case, stress, and interrupt tests.
- Benchmark Item Enhancement: It was emphasized that future benchmarks should also include basic spammer transactions.

## 7-2. Future Test Improvements

Raul suggested the following improvements to enhance test realism:

- Asymmetric Bandwidth Limitation: Separately limit upload and download bandwidth for more realistic network conditions.
- Apply Diverse Node Profile Types: Categorize node profiles according to CIP-7870 specification and reflect different bandwidth requirements for each.
- Perform Backfill Tests: Verify that new or syncing nodes can efficiently download and process historical block data.
- Block Generation Competing with Blobs: Simulate propagation conflicts by creating competing blocks simultaneously with blob propagation.
- Gas Saturation and Pathologically Large Block Tests: Create pathologically large blocks by filling them with gas, then compress and propagate them.
- Latency Distribution Experiments: Apply various latency distributions and record this data.
- GossipSub Parameter Limitation Experiments: In smaller testnets, the number of hops is low. The goal is to recreate mainnet-level hop counts and message delivery times to obtain better test signals.

