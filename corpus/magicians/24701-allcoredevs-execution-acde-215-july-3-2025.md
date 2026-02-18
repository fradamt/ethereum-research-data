---
source: magicians
topic_id: 24701
title: AllCoreDevs - Execution (ACDE) #215 (July 3, 2025)
author: system
date: "2025-06-30"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/allcoredevs-execution-acde-215-july-3-2025/24701
views: 230
likes: 2
posts_count: 5
---

# AllCoreDevs - Execution (ACDE) #215 (July 3, 2025)

- July 3, 2025, 14:00-15:30 UTC
- Ethereum Protocol Calls Calendar subscription

# Agenda

- Fusaka scope finalization

devnet-2 updates
- EIP-7907 next steps

Proposed changes
- Update EIP-7907: Account for large contracts as tx entry point by marioevz · Pull Request #9955 · ethereum/EIPs · GitHub

Finalize `maxBlobsPerTx` value for [EIP-7892](https://eips.ethereum.org/EIPS/eip-7892)
[Update EIP-7883: Triple price by marcindsobczak · Pull Request #9969 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9969)

Glamsterdam

- Headliner timeline changes?

Original: June 20 proposal deadline, July 17 final decision

All other EIPs to open PFI PRs?

- Update EIP-7773: Move previously CFI'd Glamsterdam EIPs to PFI by timbeiko · Pull Request #9970 · ethereum/EIPs · GitHub
- https://github.com/ethereum/EIPs/pull/9927

History expiry

- EraE file format to handle both pre and post-merge history data.
- Pre-merge history expiry as a default

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDE
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- Facilitator email: tim@ethereum.org
Note: The zoom link will be sent to the facilitator via email



[GitHub Issue](https://github.com/ethereum/pm/issues/1601)

## Replies

**system** (2025-07-03):

### Meeting Summary:

The meeting covered discussions on various technical aspects of upcoming network upgrades, including implementation details, performance issues, and timeline planning. The team debated and made decisions on several key topics, such as transaction limits, base fee updates, and code size limits, while also addressing concerns about client performance and potential pricing adjustments. Additionally, the group reviewed proposals for future forks and discussed the implementation of new features like partial history expiry and error file formats.

**Click to expand detailed summary**

Tim and Akash discussed the timing and posting of Twitter Stream links on the Github agenda, with Tim suggesting posting them 24 hours in advance for better visibility. Tim also mentioned that they could start the stream in a minute, and Akash confirmed they were live. Tim welcomed everyone to the meeting and mentioned having a few items on the agenda for discussion.

The team discussed issues with the Fussaka scope and Glamsterdam headliners, noting that finalizing headliners in two weeks was unrealistic due to pending Fussaka finalization. Barnabas reported that Defnet 2 was not progressing well, with only 56% completion and various peering and fork ID issues affecting multiple clients. The team agreed to investigate implementing EIP-7910 for EL clients, with teams given a few days to assess the implementation effort before making a decision on Monday. Regarding EIP-7907, Dragutin explained that three PRs need to be merged, including one for code size limit reduction, another to remove warm read cost for CODESIZE, and a third for handling large contracts, with all clients appearing to be in agreement.

The team discussed merging three PRs and agreed to include the code size index as an optional implementation detail, leaving it up to clients to decide how to handle it. They debated the merits of increasing the contract size limit from 24KB to 48KB, with Allan representing Arbitrum expressing a preference for the full 256KB limit but acknowledging the need to start slow. The group agreed to include the index in the spec for Fuzaka, with plans to monitor performance and remove it if issues arise, while Łukasz emphasized the need for benchmarks before making final decisions.

The team discussed the implementation of Devnet 3, agreeing to set the code size limit to 48KB and conduct stress testing after its successful deployment. They also addressed the max blobs per transaction limit, with FLCL noting that clients currently use the max value by default, which ranges from 6 to 12 in the first VPO. The team expressed a preference for keeping the limit at 6, but FLCL suggested creating a PR to formalize this decision.

The team discussed the definition and implementation of a video limit for transactions, focusing on whether it should be a text pool limit or part of the consensus mechanism. Francesco and others argued for including the limit in consensus to prevent large transactions, while FLCL suggested keeping it flexible for future adjustments. The group agreed to hardcode the limit at 6 or 9 blobs per transaction, with plans to review and potentially adjust it in future forks. They also considered the impact on rollups and concluded that the current limit of 9 blobs is sufficient for most use cases.

The team discussed two main topics: transaction limits and base fee update fractions. They decided to remove the max blobs per transaction from the BPO specification and add a cap of 6 in the peer-to-peer CIP. Regarding base fee update fractions, they chose to keep the existing feature in the BPO config, despite the potential for future complexity, as it provides a useful lever for adjusting throughput. The team agreed to revisit the removal of this feature if it becomes a significant pain point.

The team discussed performance issues with MoD exp at higher gas limits, considering two paths: client optimizations or increasing the price. Marcin presented data showing current client performance and the need to either improve performance or reprice, with a proposal to triple the price. The team debated the impact of this change on users and agreed to investigate further before making a final decision. They also discussed changes to Blob base cost and curve repricing in other EIPs, deciding to proceed with doubling the price for EIP-7951 without more data.

The team discussed the timeline for reviewing headliner proposals for the Glamsterdam fork, agreeing to focus on the EL side in two calls on July 31st and August 14th after finalizing Devnet 3 on July 17th. They decided to move non-headliner EIPs to the PFI list and agreed to wait for the headliner decision before reviewing smaller EIPs. Matt presented a new error file format (eraE) for the execution layer, which aims to improve syncing and allow for history expiry, and requested feedback on the specification. The team also discussed the implementation of partial history expiry, noting that some clients like Besu and Nethermind plan to enable it by default in their next releases.

### Next Steps:

- Tim: Reach out to MatterLabs, Coinbase Smart Wallet, and EigenDA regarding the impact of 3x price increase for MOD_EXP.
- Client teams: Review and provide feedback on the era-e file format proposal by the end of July.
- Client teams: Confirm in the History Expiry channel their plans for dropping pre-merge history by default.
- Client teams: Start reviewing Amsterdam headliner proposals before the July 31st and August 14th calls.
- Francesco: Open a PR to change the Blob base cost in EIP-7918.
- Marius: Open a PR to 2x the price of the r1 curve precompile.
- Guillaume: Leave a comment on the PR regarding the removal of previously CFI’d EIPs.
- Tim: Share a summary of the call and action items in the chat later today.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: f0Jr0i7!)
- Download Chat (Passcode: f0Jr0i7!)

---

**system** (2025-07-03):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=6DT6V4AdAaI

---

**timbeiko** (2025-07-03):

## Action  Items & Next Steps

## Fusaka

- Move forward with EIP-7907 with the following PRs:

https://github.com/ethereum/EIPs/pull/9910

feat: remove codesize warm read by rakita · Pull Request #11 · lightclient/EIPs · GitHub

[Update EIP-7907: Account for large contracts as tx entry point by marioevz · Pull Request #9955 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9955)

Include 7907 in devnet-3 and stress test implementations
Decide on requiring `eth_config` ([EIP-7910: eth_config JSON-RPC Method](https://eips.ethereum.org/EIPS/eip-7910)) before devnet-3 on Monday’s ACDT call
Remove `maxBlobsPerTx`from EIP-7892 and hard a constant limit of 6 blobs/txn in EIP-7594

- @FLCL to open a PR

Increase the modExp gas cost with this PR: [Update EIP-7883: Triple price by marcindsobczak · Pull Request #9969 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9969)

- Tim to reach out to Matter Labs, Coinbase and Eigen to gauge impact

Set the EIP-7918 `BLOB_BASE_COST` to `2**13` (https://github.com/ethereum/EIPs/pull/9979)
Double the gas cost of the EIP-7951 precompile ([Update EIP-7951: update gas costs for R1 verification by MariusVanDerWijden · Pull Request #9978 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9978))

## Glamsterdam

- EL Headliner EIP reviews will happen on the July 31st and August 14 ACDEs
- Previously CFI’d EIPs for Glamsterdam will be moved to PFI (Update EIP-7773: Move previously CFI'd Glamsterdam EIPs to PFI by timbeiko · Pull Request #9970 · ethereum/EIPs · GitHub)
- Non headliner EIP proposals for Glamsterdam should open a PR to be PFI’d. PFI deadline will be confirmed in the next 1-2 ACDEs.

# History Expiry

- All EL clients to enable pre-merge history pruning by default in their next stable release
- Teams should review the EraE draft and comment in #history-expiry

## Summary

#### 1. devnet‑2

- Finalization stalled (~56 % participation): fork‑ID mis‑calculation in Besu, 4‑byte IDs mishandled by Nethermind; EL/CL Nimbus unable to sync.
- Agreed on a standardised Genesis‑config RPC so devnets catch divergent parameters before launch; no client objects, all to estimate effort by Monday’s testing call.
- Devnet‑2 will remain up only as a bug‑hunt sandbox; Devnet‑3 becomes the “happy‑path” network.

#### 2. EIP‑7907 (Meter contract size & raise limit)

- New limit 48 kB (2× current), down from the early “10×” proposal; code‑size index optional, NOT in consensus.
- Inclusion gate: three PRs (clarification, patch removing code‑size warming, large‑contract fix).
- Stress‑test methodology: spammer tx + large‑block replay in Devnet‑3; pull the EIP if DOS issues surface.

#### 3. Blobs‑per‑Transaction Debate

- Status‑quo complexity (6 → 12 jump inside BPO schedule) deemed pointless.
- Decision: hard cap = 6 in PeerDAS; no BPO knob. Simple, less brittle, matches current L2 behaviour (Base averages <1.5 blobs/tx).
- Base‑fee update fraction remains in BPOs – valuable future lever; removal would create awkward special‑cases when tuning throughput.

#### 4. Precompile Re‑Pricing

- ModExp (EIP‑7883): triple cost; beats worst‑case at 100 M gas limit. Consensus that performance‑first outlook outweighs small fee hike for a handful of power users (Matter Labs, EigenDA, Coinbase wallets).
- secp256r1 / r1 curve (EIP‑7951): 2× bump to keep parity with EC ADD/MUL. No opposition.
- Clients still free to pursue GMP / gnark acceleration, but gas schedule will assume “slow” path.

#### 5. History Expiry Roadmap

- EraE → single EL‑centric archival format (headers, bodies, receipts in columnar chunks + optional Merkle proofs). Supersedes Era‑1, avoids consensus‑layer cruft.
- Once Era‑E spec is frozen and files generated, clients may prune history up to Cancun; rolling expiry research continues in parallel.

#### 6. Glamsterdam Scheduling

- Headliner proposal window closed (20 Jun). EL headliner reviews on July 31 & August 14 ACDEs.
- forkcast.org launched – comparative matrix of every headliner & stakeholder impact; authors invited to update their rows.

---

Notes were generated using o3, and edited by me.

---

**yashkamalchaturvedi** (2025-07-04):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 3 Jul 25](https://etherworld.co/2025/07/03/highlights-from-the-all-core-developers-exceution-acde-call-215/)



    ![image](https://etherworld.co/content/images/2025/07/EW-Thumbnails--4-.jpg)

###



Fusaka Scope & Devnet Planning, Glamsterdam Process & Scheduling & History Expiry Roadmap

