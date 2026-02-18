---
source: magicians
topic_id: 24817
title: All Core Devs - Testing (ACDT) #45 | July 21 2025
author: system
date: "2025-07-16"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-45-july-21-2025/24817
views: 155
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #45 | July 21 2025

# All Core Devs - Testing (ACDT) #45 | July 21 2025

- July 21, 2025, 14:00 UTC

# Agenda

- Fusaka updates
- Gas limit testing updates
- PeerDAS Specific Updates
- BloatNet data collection
- EngineAPI safe block discussion
- Builder response discussion

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

[GitHub Issue](https://github.com/ethereum/pm/issues/1624)

## Replies

**poojaranjan** (2025-07-21):

# ACD Testing Call #45 - Quick notes

Moderator: Mario Vega

## Fusaka Devnet Updates

**Mario:**

- Devnet 3 not gone live as of now

**Spenser:**

- EEST feature release for Devnet 3 includes:

Modexp gas repricing updates
- CLZ opcode changes (will be discussed today)
- Blob base fee and gas reduction
- New test added for PeerDAS and EIP-7907 testing

**Pari:**

- Two items pending before launch (Builder spec & Engine API v2 PR #123)
- Kurtosis testing in progress
- If unblocked, Devnet 3 release expected this week

**Client Status:**

- Besu, Geth (except config endpoint), Nethermind, Reth are ready
- Lighthouse, Grandine, Lodestar (pending builder API) are ready

#### Conclusion:

- No major blockers from clients side is anticipated for next 2 days.

## Gas Limit Testing Updates

**Pari:**

- 45M gas limit enabled across all clients on mainnet - Congratulations!
- Perf Devnet 2 was worked on the last weekend.
- New sync testing tool is available
- New RPC testing tool in development, team will reach out to RPC providers.

**Kamil:**

- Opcode benchmarking is WIP.
- Connecting with EEST team on full integration of opcode becnhmarking.
- Computation benchmarks mostly complete.

**Marcin Sobczak:**

- EIP-7883 Comprehensive ModExp Analysis
- Entity Impact Report
- Ask is for client teams to take a look.

## BloatNet Data Collection

**CPrezz:**

- BloatNet is approaching 2x the size of mainnet.
- Ongoing compaction testing aims to help evaluate safety for a potential 100M gas limit.
- Several metrics have been implemented, though some are still missing.
- Sync data is missing from Besu and Erigon.
- Grafana integration is challenging, especially due to difficulties extracting metrics from logs for Nethermind and others.
- Shared reference: BloatNet Metrics & Progress – HackMD
- Request to client teams: reach out if assistance is needed.

**Kamil Chodoła:**

- Will report additional metrics and is working to include more.
- Reminder: All changes to the performance branch are automatically used by:

Opcode benchmarking tools
- Perfnet
- BloatNet

Ensure `performance` branches are updated regularly with experimental changes and rebased on `master`.

**Amezaine (Besu):**

- Besu does have some metrics for sync and compaction.
- Needs to review implementation to confirm correctness and ensure coverage.

**Milen (Erigon):**

- Has been helpful in providing data and coordination.

**Additional Notes (CPrezz):**

- For compaction metrics, timing must cover insertion and removal operations in detail.

**Pari:**

- Emphasized the importance of keeping performance branches up to date across all clients.

## Engine API: Fast Confirmed Safe Block Discussion

- Discussion Link

**Mikhail Kalinin** initiated a conversation about incorporating a **fast confirmed block** reference in the Engine API. The goal is to enhance safety signals shared between clients and external consumers (like exchanges and L2s).

### Key Questions Raised:

- How is the safe block currently used by EL (Execution Layer) clients?
- How do consumers like exchanges and rollups use it via the JSON-RPC API?
- Should the safe block field be overloaded to include the fast confirmed block (currently mapped to justified)?
- Or should a new field such as fast_confirmed be introduced?
- How difficult would it be to add this from an engineering perspective?

**Mikhail Kalinin**

- There’s an open PR and ongoing experimentation with a slightly modified implementation.
- Historically, safeBlock was meant to serve as the confirmed block, but no robust algorithm exists today to guarantee this.
- Asks whether introducing a new tag in the Engine API is a better long-term solution.

**Marius van der Wijden**

- Suggests that safeHead should be the default for most applications currently relying on finalized.
- Notes underutilization of safeHead by clients.

**Terence (Prysm)**

- Points to consecutive slot disparity as a source of discrepancy.
- Prysm includes a flag that can expose this state to users.

**Further Considerations**

- Marius emphasized that no major EL changes are needed if CL (Consensus Layer) already marks blocks as safe.
- Shared if RPC providers and infrastructure operators running multiple clients: discrepancies in safe block may already be there.
- Noted that the current definition of safeBlockHash is vague enough to permit flexibility:

> "safeBlockHash": DATA, 32 Bytes – the "safe" block hash of the canonical chain under certain synchrony and honesty assumptions. This value MUST be either equal to or an ancestor of headBlockHash.

#### Conclusion

- Continue discussion in Ethereum R&D Discord.
- Bring the topic back to the next All Core Devs (ACD) call for wider input.

## Builder Response Discussion

**Bharath-123** proposed to [discuss](https://github.com/ethereum/pm/issues/1624#issuecomment-3095192635):

###

- Suggests deprecating JSON-formatted requests and responses in favor of SSZ encoding.
- This update was raised to gather any final feedback or objections from client teams.

**Parithosh Jayanthi**

- Asked for final input from the group on PR #123:

> “Can we merge it? Or any open discussion topics?”

**Bharath**

- Confirmed client developer consensus exists.
- If no objections are raised, this update can be targeted for Devnet 3.

### Decision

**Alex Stokes**

- Supports the proposal:

> “We should merge it.”
- Notes that work is already underway on MEV-Boost to support the changes.

The update is cleared to proceed and will be part of Devnet 3 scope unless new concerns are raised.

## getBlobsV3 Discussion

The proposal to introduce `getBlobsV3` was evaluated during ACD Testing Call #45. The discussion centered on whether it should be implemented now for future use or deferred due to testing and coordination concerns.

**Dustin**

- Suggests that if EL clients ship getBlobsV3 now, it could be retroactively validated through testing later.
- Notes it wouldn’t be trusted immediately but might become trusted if supporting tests are run in the future.

**Raúl Kripalani**

- Clarified that from an optimization perspective, the change would be purely on the Consensus Layer (CL).
- getBlobsV3 is an extension of the gossip subprotocol, already included in the master spec.
- No spec changes on CL are necessary at this point.
- Noted that CL clients are still using getBlobsV2 and have not yet implemented v3.

Some of the other client devs on call were not in favor.

**Mario**

- Raised concerns about the contentious nature of the proposal.
- Suggested deferring the discussion to an ACDE meeting.

**Parithosh**

- Flagged that there’s a BPO (Blobstream Precompile Opportunity) upgrade between Fusaka and Glamsterdam.
- This sequencing should be considered when deciding the scope of Devnet testing.

**Mario**

- Expressed uncertainty about having enough time to properly test getBlobsV3 in Devnet 3.

#### Decisions

- Do not include getBlobsV3 for now.
- Francesco: Recommended going forward with getBlobsV2 only, as current CL implementations support that version.
- Raúl Kripalani:

Closed PR #671 which proposed getBlobsV3.
- Opened a new PR to make getBlobsV2 all-or-nothing, so it’s uniformly adopted by all clients.

## CLZ Opcode Gas Cost Discussion

The gas cost of the `CLZ` (Count Leading Zeros) opcode was increased from 3 to 5. This change prompted discussion regarding whether it was justified or should be reverted based on updated benchmarking data.

**Dragan Rakita**

- Raised concerns over bumping CLZ from 3 to 5 gas.
- Cited comparative analysis of similar opcodes like ISZERO and MUL, which suggests a cost of 3 would be more accurate.
- Shared benchmarking data in Discord.
- Referenced Rust benchmark comparison in bluealloy/revm#2744 showing comparable performance among opcodes.
- Expressed willingness to reprice the opcode if consensus emerges.

**Mario**

- A rollback is complicated since the fork is close to finalization.
- Warned against hasty changes without broader client benchmarking data.
- Noted EEST is currently working on a more comprehensive benchmark, but it’s not yet available.

**Marius van der Wijden**

- Also hesitant to change the gas price without robust benchmarks.
- Shared benchmarking results for Geth:

opAdd: 8ns
- opCLZ: 48ns
Indicating that CLZ may be costlier than initially assumed.

**Dragan Rakita**

- Emphasized that benchmarking can vary by implementation.
- His team’s data shows CLZ might not even justify a gas cost of 3.

**Mario (on benchmarking status)**

- Not all clients have published reliable benchmarks yet.
- Encouraged finishing benchmarking work before making changes.

#### Decision

- No rollback of the CLZ gas cost at this time.
- Gas cost remains 5 for Devnet 3.
- Reconsider for Glamsterdam based on comprehensive benchmarking.
- General leaning is to adjust gas upward rather than downward if uncertainty exists.

> “Let’s keep it at 5 for now. Benchmark more thoroughly, revisit for Glamsterdam if needed.” — Mario

## 60M Gas Limit Discussion

Raised by: **Kamil Chodoła**

- Current blocks are already reaching 45M gas, so 60M is a foreseeable next step.
- Proposal to start thinking about re-pricing and scaling efforts to support 60M blocks, potentially even before Fusaka.
- Prompted a temperature check among client teams:

Should we proactively work toward 60M gas blocks?
- Known areas for improvement include ModExp performance.

**Marius van der Wijden**

- Noted that with refund mechanisms, actual gas pressure can be reduced by ~20%.
- Requested more data to understand the impact on state growth from scaling up to 60M gas.

Hopes the BloatNet initiative can provide valuable insights.

> “I would also like more data on state growth for 60M, hope that BloatNet can help us there.” — Marius

**CPerezz**

- Urged for a step-by-step approach:

First goal is achieving 2x mainnet state on BloatNet.
- Working on collecting EL client performance data to model a wide range of test cases.

> “One step at a time!  Getting to 2x mainnet for now and gathering EL client’s info to come up with as many cases as possible.” — CPerezz

**Ben**

- Highlighted that receipt data remains a bottleneck in scaling up to 100M gas.

**Kamil**

- Framed the discussion as exploratory:

Aimed to spark reflection and gather feedback.
- Will revisit the topic in the following week.
- Believes 60M is feasible before Fusaka if work continues as planned.

**Mario Havel**

- Welcomed the discussion.
- Emphasized no immediate decision is needed but encouraged teams to keep the topic in mind.

> “Nice to be brought up. No need for a decision now.” — Mario

### Follow-Up Items

- Merge builder-specs PR #123
- Continue safe block discussion on Discord
- Revisit CLZ gas in next testnet
- Monitor BloatNet metrics and performance benchmarks
- Prepare Devnet 3 as blockers resolve

---

**system** (2025-07-21):

### Meeting Summary:

The team discussed updates on the Fusaka devnet, including feature releases and client compatibility, with most Ethereum clients reported as ready pending implementation of getBlobsV3. The group reviewed progress on sync testing tools and metrics collection for various clients, addressing questions about testing tools and metrics collection while agreeing to push metric updates to the performance branch. The team made decisions about API changes for getBlobsV3, discussed gas pricing for the CLZ opcode, and addressed concerns about reaching higher gas limits, with plans to continue monitoring state growth and gather more data on the 60 million gas limit.

**Click to expand detailed summary**

The meeting began with morning greetings and small talk among participants, including Mario, Pooja, and Carson. Mario mentioned that the meeting would start shortly once everyone was present. The transcript ends with Mario welcoming everyone to the meeting and noting the date as July 21st.

The team discussed updates on the Fusaka devnet, with Spencer reporting a feature release that included updates to gas prices, modex, and curve CLZ, as well as new tests for the Max Blob for Tx limit. Parithosh mentioned that client images are still pending, but once received, they should allow for hive tests to run. Most Ethereum clients, including Besu, Geth, Erigon, Lighthouse, and Nethermind, are reported to be ready, pending the implementation of getBlobsV3. Parithosh also shared that the first 45 million gas limit blocks have been produced on Mainnet, and a minor issue with Besu on Buff devnet 2 is being addressed.

The team discussed progress on sync testing tools and metrics collection for various clients. Parithosh reported on the new syncor tool and Rpc testing tool, while Kamil shared updates on extended gas benchmarks and stateful testing efforts. The group addressed questions about testing tools and metrics collection, with milen confirming updates for Erigon and Ameziane discussing Besu metrics. CPerezz requested additional metrics from clients to support compaction testing and reaching 100 million gas limit safely. The team agreed to push metric updates to the performance branch and follow up on outstanding issues.

The team discussed merging API changes for getBlobsV3, with Raúl proposing to merge implementations now to avoid future coordination overhead. Dustin expressed concerns about testing and process, arguing that the changes should not be tied to the Fusaka fork without proper testing. The group debated whether to include the changes in the Fusaka spec, with Matthew highlighting process concerns about sneaking in last-minute changes. After prolonged discussion, the team agreed to make a final decision that day, with Francesco suggesting they default to not including the changes if consensus couldn’t be reached.

The team decided to revert the getBlobsv3 changes on master and stick with getBlobsv2 with all-or-nothing behavior for devnet. Mikhail presented a proposal for a new confirmation rule algorithm, which would be faster and easier to implement, but the team agreed to continue discussing this in Discord and potentially bring it up at ACD. Bharath introduced a new V2 API for relays that would return execution payload and blobs, which the team agreed to implement for devnet-3. The conversation ended with a brief discussion about CLC setup code being bumped to 5, with Dragomir Rakita suggesting further analysis might be needed.

The team discussed gas pricing for the CLZ opcode, which was increased from 3 to 5 gas. While Dragan suggested reverting to 3 gas based on benchmarks from the Reth client, Mario and others agreed to maintain the 5 gas price due to lack of comprehensive benchmarks across all clients. The team acknowledged the need for more thorough benchmarking, which they plan to address this week, before considering any changes to the gas price.

The team discussed reaching a gas limit of 60 million, with Kamil noting that while 45 million has been achieved, there are no immediate blockers to reaching 60 million, though some optimizations in modex libraries are needed. Marius raised concerns about receipt processing breaking at 72 million gas, but Parithosh clarified that receipts are not a problem after reaching 85 million gas. The team agreed to continue monitoring state growth and gather more data on the 60 million gas limit, with Ben highlighting that receipts are the main blocker for reaching 100 million gas.

### Next Steps:

- Parithosh to ensure all client metric changes are pushed to the performance branch for running on Blobnet.
- Client teams to implement and provide metrics for syncing and compaction on Blobnet, especially Besu and Erigon.
- Raúl to revert the get_blobs_v3 changes in the master branch, keeping get_blobs_v2 with all-or-nothing behavior for Devnet 3.
- Mikhail to follow up on Discord regarding the usage of safe block in the engine API response and bring the topic to ACD for wider discussion.
- Client teams to work on benchmarking CLZ opcode across all clients this week.
- Testing teams to add testing bandwidth for the builder API changes for Devnet 3.
- Client teams to consider and discuss the possibility of increasing the gas limit to 60 million before Cancun, to be revisited in the next meeting.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: @VXi*3dj)
- Download Chat (Passcode: @VXi*3dj)

---

**system** (2025-07-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=_h2UpVfPnG4

