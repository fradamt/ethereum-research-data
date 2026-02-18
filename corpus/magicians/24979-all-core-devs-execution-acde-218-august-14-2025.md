---
source: magicians
topic_id: 24979
title: All Core Devs - Execution (ACDE) #218, August 14, 2025
author: system
date: "2025-08-01"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-218-august-14-2025/24979
views: 272
likes: 3
posts_count: 5
---

# All Core Devs - Execution (ACDE) #218, August 14, 2025

- Fusaka
- Glamsterdam
-

**Meeting Time:** Thursday, August 14, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1652)

## Replies

**abcoathup** (2025-08-05):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #218, August 14, 2025](https://ethereum-magicians.org/t/all-core-devs-execution-acde-218-august-14-2025/24979/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE TL;DW
> Fusaka
>
> The issues that came up indevnet-4 warrant a new devnet. We’ll have devnet-5 to test the fixes (no other spec changes).
> On Monday’s ACDT, we’ll determine when to launch devnet-5 , ideally before ACDC next week
> We didn’t set dates yet, will wait until devnets & testing stabilizes before doing that
>
> Glamsterdam
>
> EPBS & BALs are confirmed as headliners
> FOCIL still CFI’d, will decide on inclusion once EPBS & BALs are live on devnets
> Deadline for other EIP PFI proposals is…

### Recordings/Stream

- https://www.youtube.com/live/iPYHJnEeY9g?t=137s
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- Quick notes & ACDE #218: Call Minutes by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDE Call #218 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-4 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists

---

**timbeiko** (2025-08-14):

# ACDE TL;DW

**Fusaka**

- The issues that came up indevnet-4 warrant a new devnet. We’ll have devnet-5 to test the fixes (no other spec changes).
- On Monday’s ACDT, we’ll determine when to launch devnet-5 , ideally before ACDC next week
- We didn’t set dates yet, will wait until devnets & testing stabilizes before doing that

**Glamsterdam**

- EPBS & BALs are confirmed as headliners
- FOCIL still CFI’d, will decide on inclusion once EPBS & BALs are live on devnets
- Deadline for other EIP PFI proposals is when we put out Fusaka mainnet releases (moved from Aug 21st)
- We discussed many spec changes for BALs, @toniwahrstatter update the EIP based on the conversation and set up a BAL breakout room to discuss further once we have an updated spec

We didn’t have much time to discuss the other topics, but two EIPs were shared on the agenda, and we briefly continued the `safe` head discussion by [@mkalinin](/u/mkalinin)

# Full Summary (AI-gen )

## ACDE #218 Summary – August 14 2025

### Action Items

1. Devnet‑4 Stabilisation & Devnet‑5 Launch

 Fix outstanding bugs: Devnet‑4 launched cleanly through BPO 1–2, but BPO 3 exposed several problems.
 – Erigon computed the blob‑fee incorrectly, causing it to fork away from other execution clients; a fix has been merged in Geth and other ELs but Erigon is still investigating.
 – Lighthouse and Nimbus struggled with peer discovery and sync due to poor boot‑node diversity; half the boot nodes have been switched from Lighthouse–Geth to Prism–Geth pairs, but both clients still need fixes to reliably find peers.
 – No mass validator slashing is expected because the super‑node topology mirrors mainnet and should allow finality once the client fixes land.
 – Update fork‑ID logic in all clients and improve boot‑node diversity prior to Devnet‑5.  Owners: all EL/CL teams  • Due: before Devnet‑5.
2. Update‑fraction specification: when the base‑fee update fraction changes at a fork, use the fork parameters of the current block, not the parent.  This applies to constants such as BLOB_BASE_FEE_UPDATE_FRACTION and resolves the inconsistency that triggered the DevNet‑4 fork.  Anders Elowsson will update the relevant EIPs, and Mario Vega will publish static tests to ensure all clients implement the same logic.
 Context: some EL clients used the parent block’s update fraction when computing the next block’s parameters; others used the current block’s constants.  The call agreed that the current‑block approach is simpler and more consistent, but future EIPs must explicitly specify which set of parameters to use.
3. Chain‑config RPC: estimate and implement a new eth_getChainConfig JSON‑RPC method (mirroring the consensus layer’s engine_getPayloadBodiesByHash) to expose the static fork‑ID configuration used by each client.  Devnet‑5 will not launch until all EL clients implement this RPC.  Owners: all EL teams  • Due: before Devnet‑5.
4. Devnet‑5 planning: once Devnet‑4 finalises cleanly, schedule Devnet‑5 with fixes and increased minority‑client representation (Grandine/Erigon/Lodestar ~3–5 %), keeping Lighthouse/Prism at realistic levels.  Owners: PandaOps, client teams  • Due: next ACDE if ready.
5. Fusaka Timelines

Postpone schedule decisions: Alex Stokes proposed Sepolia/Holesky client releases on 8 September, a Holesky fork on 15 September and a Sepolia fork on 29 September, but multiple teams objected because Devnet‑4 is still unstable, static tests for fork‑parameter calculations aren’t ready and several clients are running off feature branches.  Consensus was to defer timeline discussions until Devnet‑5 is clean and stable.  Once Devnet‑5 finalises, dates will be selected for public test‑net forks and client releases.  Owners: coordinators  • Due: TBD.
6. Glamsterdam Headliners Finalised

 ePBS & BAL: Core devs confirmed that EIP‑7732 (ePBS)—enshrined proposer‑builder separation—is the consensus‑layer headliner and EIP‑7928 (Block‑Level Access Lists) is the execution‑layer headliner.  Both must be implemented and tested before any additional features are added.
7. Fossil & 6‑second slots: EIP‑7778 (6‑second slots) was removed because its multi‑dimensional fee‑market changes conflicted with block access lists; EIP‑7702 (Fossil)—a proposed in‑protocol Ethereum Virtual Machine (EVM) to support account abstraction—remains CFI.  Fossil’s inclusion will be evaluated only after ePBS and BAL are far along.
8. Accept new CFI proposals for Glamsterdam until the Fusaka mainnet releases are prepared (post‑launch proposals close once Fusaka is live).  Owners: EIP authors.
9. Block‑Level Access Lists (BAL) Specification

 State‑read locations: keep entries for reads (e.g., SLOAD, balance checks, static calls) in the BAL, even though they add ~50 kB per block.  Auditors indicated that knowing which contracts were touched is valuable, and these entries may enable future parallel batch I/O and transaction parallelisation.
10. Serialisation: use RLP for now—SSZ provides compact proofs but lacks mature Go libraries; the EL can revisit SSZ once the tooling improves.  Tim suggested that migrating peer‑to‑peer messages to SSZ could be a first step, but for Glamsterdam the EL will stick to RLP.
11. System‑contract handling: split pre‑execution system‑contract state changes (e.g., ring buffer writes, EL‑triggered withdrawals) and post‑execution changes.  One proposal is to map all pre‑execution changes to index 0 and all post‑execution changes after the final transaction; another is to order indices to mirror the actual execution sequence.  Toni Wahrstätter will update the EIP with a concrete proposal and convene a breakout call.
12. Naming: avoid calling these indices “transaction indices”; instead, use “block‑level access list indices.”
13. Testing & Process Improvements

 Early collaboration: Mario Vega reminded EIP authors to consult the testing team before ACD presentations.  Every Amsterdam candidate should outline its testing requirements and complexity up front to avoid last‑minute surprises.  The block‑access‑lists team’s proactive engagement was cited as a model.
14. Static tests: the testing team will publish static test suites for fork‑boundary parameter calculations and the MODEXP gas‑repricing changes.  Clients must integrate these tests before launching Devnet‑5 and beyond.
15. “Safe‑Head” Proposal

Mikael Kalinin outlined options for fast‑confirmation exposure: repurpose the existing safe block tag to point to the fast‑confirmed block; add a separate fastConfirmedBlock hash to the Engine API and JSON‑RPC; or make the meaning of the safe block configurable per CL client.  The first option requires no API changes but redefines semantics that consumers might rely on.  Data providers are encouraged to provide feedback via the Eth R&D Discord (#execution-specs) before the next call.
16. ModExp and Contract‑Size Changes

 MODEXP repricing: the EIP‑7883 repricing will triple the cost of the MODEXP precompile in Fusaka.  Although geth and Erigon are investigating code‑level optimisations, the repricing remains the consensus fix to prevent MODEXP from becoming a throughput bottleneck.
17. Contract‑size limit: EIP‑7907 will raise the maximum contract size to 48 KB (doubling it from the current 24 KB) and remove the requirement to maintain a global “warm index” for contract code.  Implementations will be free to warm code as they see fit; additional cold‑load gas has been added to mitigate DoS vectors.  Stress‑testing this change will be a priority in Devnet‑5.

---

### Summary

#### Devnet‑4 Status & BPO Rule Issues

- Devnet‑4 launched with BPO 1 and 2 transitions, but BPO 3 exposed multiple issues.  Erigon forked off because it used different gas‑calculation logic for block fee; Lighthouse suffered from peer‑discovery problems and couldn’t sync to head; Nimbus also struggled to connect.  Boot nodes were all Lighthouse+Geth pairs, so half were switched to Prism+Geth to improve diversity.  The network is working toward finalising the chain by end‑of‑day and proceeding to BPO 5 tomorrow.
- To finalise Devnet‑4 and avoid mass validator slashing, teams must fix EL and CL bugs and ensure super‑node finalisation logic operates correctly.

#### BPO Update‑Fraction Calculation

- The update fraction calculation (used when moving from one BPO to the next) had inconsistent implementations.  After debate, core devs agreed to use the current block’s fork parameters rather than the parent’s, simplifying the implementation (see the discussion).  Anders will update the relevant EIP and Mario will produce static tests to ensure all clients handle future fork boundaries consistently.  The decision sets a precedent that future EIPs must explicitly specify whether current or parent parameters are used.

#### Fusaka Timelines & Devnet‑5 Planning

- Alex’s proposed timeline (Sep 8 release for Sepolia/Holesky, Sep 15 Holesky fork, Sep 29 Sepolia fork) faced strong pushback because Devnet‑4 still isn’t stable and static tests for fork‑parameter calculations are missing.  Several CL teams (Lodestar, Prysm and Nimbus) requested an extra 4 weeks; consensus was to delay timeline discussions until Devnet‑5 is clean and stable and CL branches are merged into main.
- Devnet‑5 will include fixes from Devnet‑4, static tests and improved minority‑client representation.  Launch will be discussed on Monday’s testing call once remaining issues are resolved.  Timeline decisions will only follow after a successful Devnet‑5.

#### Glamsterdam Headliner Finalisation & Scope

- Core devs confirmed that EIP‑7732 (ePBS) is the consensus‑layer headliner and EIP‑7928 (Block‑Level Access Lists) is the execution‑layer headliner.
- EIP‑7778 (6‑second slots) was removed due to conflicts with BAL; EIP‑7702 (Fossil) remains CFI and will be revisited only after ePBS and BAL implementations are stable.  New proposals for Glamsterdam will be accepted until Fusaka mainnet releases are ready.
- Initial Glamsterdam timelines were discussed on the ACDC call: CL teams estimate ePBS implementation work converging around March/April 2026; FOCIL adds 1–2 months.  Consensus is to follow a phased approach—stabilise SFI EIPs first, then consider CFI EIPs.

#### Block‑Level Access Lists (EIP‑7928) Decisions

- State‑read locations will remain in the BAL spec despite increasing size (~21 blobs → 50 kB per block) because they enable parallel batch I/O, transaction parallelisation and auditability.
- Serialization: RLP will be used for encoding; SSZ was rejected for now due to limited Go‑SSZ library support and to maintain EL serialization consistency.
- System contracts: pre‑execution changes will be recorded at index 0 and post‑execution changes at the end of the list; indices will be called “block‑level access list indices”.
 Toni (@nerolation) will update the EIP accordingly and schedule a breakout.

#### Other Discussion Points

- Max blobs per transaction: final spec sets a cap of 6 blobs per transaction in the PeerDAS API; the max‑per‑tx limit will be removed from the BPO schedule to simplify client logic.
- Base‑fee update fraction remains in the BPO schedule; removing it would limit future flexibility and require extra mapping between BPOs and fork constants.
- ModExp repricing: teams acknowledged that client implementations of MODEXP vary widely; consensus was to triple the gas price to avoid bottlenecks, while allowing optimisations to continue (see PR #9855).
- Safe‑head proposal: @mikaelsq presented a proposal to repurpose the safe block as the “fast confirmed” block or introduce a new RPC (see discussion).  Stakeholders are asked to provide feedback, particularly on whether redefining the safe block’s semantics would impact existing API consumers.
- Testing process: Mario stressed that EIP authors must collaborate with the testing team before presenting to ACD; the block‑access‑lists team’s collaboration was cited as a good example.  All pending Glamsterdam EIPs should review testing complexity to avoid delays.

### Next Steps

- Aug 18 Testing Call: assess progress on Devnet‑4 fixes (Lighthouse/Nimbus sync), chain‑config RPC effort, and readiness for Devnet‑5.  If fixes land, schedule Devnet‑5 launch.
- Next ACDE (Aug 28): revisit Fusaka timelines after Devnet‑5, review EIP‑7907 tests, and discuss Glamsterdam progress.
- BAL Breakout: Toni to circulate updated EIP‑7928 text and organise a breakout session to finalise system‑contract handling and SSZ vs RLP details.
- Headliner EIPs Implementation: EL/CL teams to begin coding ePBS and BAL; only after stability is proven will Fossil be reconsidered for Glamsterdam.
- Safe‑Head Feedback: block explorers and API providers to send feedback on the fast‑confirmation proposal before the next ACDE.

---

---

**system** (2025-08-21):

### Meeting Summary:

The meeting covered updates on Devnet 4 issues, discussions on Cancun timelines, and plans for the Grandsterdam fork. Participants debated technical aspects of blob-based fees, parameter calculations, and block access lists, making decisions on implementation approaches and encoding methods. The group also addressed timeline concerns for upcoming upgrades and agreed on headliners for the Grandsterdam fork, while planning further discussions on specific technical details.

**Click to expand detailed summary**

Tim opens the meeting and outlines the agenda, which includes discussing Devnet 4 issues, Cancun timelines, and Dencun headliners. Barnabas provides an update on Devnet 4, reporting successful transitions through BPO 1 and 2, but issues arising at BPO 3. These include gas calculation problems with Erigon and peering difficulties for Lighthouse. Lighthouse and Nimbus are still investigating their issues, with Lighthouse unable to sync to head. The team is working on fixes and hopes to achieve a finalized chain soon, potentially by the end of the day.

The group discusses how to handle the calculation of blob-based fees and related parameters at the Cancun fork boundary. They decide to use the current block’s parameters on the fork block, rather than the parent block’s parameters. This choice is made to prioritize implementation simplicity and consistency, despite some opposition. The group acknowledges that this decision may require updates to the EIP and test cases to clarify the approach. They agree to have someone update the EIP and ideally the specs or tests soon to reflect this decision.

The discussion focuses on how to calculate and set the BASE_FEE_UPDATE_FRACTION parameter for future devnets and testnets. Barnabas proposes using a specific formula that assumes a 3:2 ratio of max to target blobs. While there is general agreement that this formula is reasonable, there are concerns about enshrining it in the protocol or committing to a specific ratio long-term. The group decides not to enforce this in consensus, but agrees to use it as a default for now while retaining flexibility to change it in the future if needed. They plan to discuss further how to best support this approach in testing.

The meeting discusses the timeline for the Fusaka upgrade and plans for Devnet 5. Alex proposes dates for client releases and testnet forks, but some teams express concerns about the timeline due to ongoing sync issues and lack of static tests. There is debate about whether to set firm dates now or wait until issues are resolved. The group agrees to launch Devnet 5 next week to test fixes for CL syncing issues and EL spec changes. They plan to increase the share of minority clients on Devnet 5 for more thorough testing. The timeline for Fusaka will be reassessed after seeing how Devnet 5 performs.

The meeting discusses the headliners and scope for the upcoming Grandsterdam fork. Tim confirms that EPBS (Enshrined Proposer-Builder Separation) and Block Access Lists will be the two headliners. The group agrees to move forward with implementing these two features first and creating devnets to test them. FOCIL (Fully On-Chain Inclusion Lists) remains CFI (Considered for Inclusion) but will not be actively worked on until the headliners are further along. The team aims for a June mainnet fork, with releases ready for testnets in April. They decide to set the deadline for proposing non-headliner EIPs as the mainnet release date for the Fusaka fork.

The discussion focuses on two main points regarding block access lists (BALs): whether to include state locations and whether to use RLP or SSZ encoding. For state locations, there is debate about their usefulness for parallel execution and auditing versus the increased size. No firm decision is made, but they will likely be kept for now. On encoding, despite some arguments for SSZ, most participants lean towards using RLP due to concerns about Go SSZ library quality and implementation challenges. Toni decides to update the EIP to use RLP as the default for now, with the possibility to switch to SSZ later if a good library becomes available.

The group discusses how to handle system calls in the context of block-level access lists. They agree to keep pre-execution and post-execution changes separate, with pre-execution changes as index 0 and post-execution changes at the end. The group decides to move away from calling these “transaction indices” and instead use a term like “state transition index” or “block-level access list index”. Toni will update the EIP with these changes, and a breakout session will be scheduled to further discuss the modifications once they are ready for review.

### Next Steps:

- Anders: Update the EIP today to clarify the use of current block parameters at fork boundaries.
- Mario/Execution Specs team: Create static tests for the blob base fee calculation behavior by today or tomorrow.
- Testing team: Collaborate with EIP champions for the 11 proposed EIPs for Cancun/Deneb to discuss testing complexities.
- Lighthouse team: Continue investigating and testing fixes for their syncing issues on Devnet 4.
- Nimbus team: Investigate their peering issues on Devnet 4.
- Erigon team: Continue investigating their forking issue on Devnet 4.
- Client teams: Update their implementations to use current block parameters for blob base fee calculations at fork boundaries.
- Mario: Ensure static tests for side effects are released by today or tomorrow.
- EIP champions: Reach out to the testing team to discuss testing complexities for their EIPs before bringing them to All Core Devs calls.
- Testing team: Review the 11 proposed EIPs for Amsterdam with their authors to assess testing requirements.
- Barnabas and testing team: Discuss async how to best support the BPO fraction update formula in testing without enshrining it in consensus.
- Client teams: Work on resolving sync issues before committing to release dates.
- Client teams: Prepare for Devnet 5, focusing on applying fixes to the BPO schedule and addressing CL-side syncing issues.
- Pana Ops: Consider increasing the share of minority clients in Devnet 5 for more comprehensive testing while maintaining overall client distribution similar to mainnet.
- Testing team: Prepare for Devnet 5 launch, incorporating CL syncing fixes and EL changes based on new specs.
- Alex: Merge the PR setting EPBs and block access list as headliners for Cancun/Deneb.
- CL teams: Work on implementing a minimal version of EPBs for a “Devnet 0” within 1-2 months.
- EL teams: Implement block access list for the initial devnet alongside EPBs.
- All teams: Aim for June as a rough target for Cancun/Deneb mainnet fork, with releases ready for testnets by April.
- Tim: Remove the 6-second slot proposal from consideration for Cancun/Deneb.
- All teams: Continue accepting new EIP proposals for Cancun/Deneb until the Dencun mainnet releases.
- Pana Ops: Coordinate with clients on setting up Devnet 0 for EPBs and block access lists.
- Tony: Keep state locations in the block access list specification for now, pending further evaluation.
- All clients: Continue using RLP for block access list serialization instead of switching to SSZ.
- Toni: Update the EIP to use RLP as the default serialization format for block access lists.
- Toni: Update the EIP to change the indexing scheme for system contract state changes in block access lists, with pre-execution changes at index 0 and post-execution changes after transaction indices.
- Toni: Rename “transaction indices” to “block-level access list index” or similar in the EIP.
- Toni: Notify the group when EIP changes are ready for review.
- All participants: Review the updated EIP changes once notified.
- Tim: Schedule a breakout session to discuss the modified EIP once changes are ready.
- All participants: Review EIP-7514 and EIP-7516 asynchronously.
- Blockchain data consumers: Reach out in the Ethereum Discord’s JSON-RPC channel regarding potential changes to safe block semantics if using the “safe block”.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: cc#0!WS8)
- Download Chat (Passcode: cc#0!WS8)

---

**system** (2025-08-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=iPYHJnEeY9g

