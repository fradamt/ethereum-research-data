---
source: magicians
topic_id: 24956
title: All Core Devs - Testing (ACDT) #47 | August 4 2025
author: system
date: "2025-07-30"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-47-august-4-2025/24956
views: 764
likes: 2
posts_count: 10
---

# All Core Devs - Testing (ACDT) #47 | August 4 2025

# All Core Devs - Testing (ACDT) #47 | August 4 2025

- August 4, 2025, 14:00 UTC

# Agenda

- Fusaka updates
- Discussion regarding raising the limit of EIP-7825 to 30 million
- Gas limit testing updates

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : acdt
- Occurrence rate : weekly
- Already a Zoom meeting ID : false # Set to true if you bring your own link – WARNING the bot will not create a zoom ID and a summary or a Youtube video – (make sure your zoom link meeting is auto recording you’ll have to handle this yourself)
- Already on Ethereum Calendar : false # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- Need YouTube stream links : true # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1648)

## Replies

**abcoathup** (2025-07-31):

### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png)

      [All Core Devs - Testing (ACDT) #47 | August 4 2025](https://ethereum-magicians.org/t/all-core-devs-testing-acdt-47-august-4-2025/24956/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACD Testing Call #47 - (Quick Notes)
> Facilitator: Mario Vega
> TL;DR
>
> Fusaka Devnet 3
>
> Nimbus and Lodestar are still being debugged; fixes are underway.
> Decision: Wait until both are stable before advancing.
>
>
> EIP-7825 Gas Limit
>
> Proposal to raise to 30M discussed; concern over app impact.
> Decision: Maintain current 16M gas limit on Devnet 3.
>
>
> Gas Limit Testing
>
> Stateful and large contract tests in progress; repo flag awaited.
> ModExp pricing PoC tool being developed; Geth change not expected soo…

### Recordings/Stream

- YouTube
- X- Livestream [x.com/echinstitute]

### Writeups

- Tweet thread by @poojaranjan
- Tweet by @Christine_dkim

### Additional info

- Fusaka upgrade:

Ideally targeting mainnet before Devconnect
- Current devnet: fusaka-devnet-3 [specs]
- selected as mascot

---

**system** (2025-08-04):

### Meeting Summary:

The team reviewed the status of Fusaka Devnet-3 and discussed various technical issues including transaction propagation problems and sync bugs that are being addressed by different team members. They evaluated the integration of Nevermind with builders and discussed potential gas limit increases, while also considering proposals for slot component times and custody group balances. The team explored syncing capabilities in perfect peerless mode and discussed the implementation of blob syncing and backfill features, with plans to revisit these topics at the next meeting.

**Click to expand detailed summary**

The team discussed the status of Fusaka Devnet-3, where Barnabas reported 90% participation with two clients experiencing issues. Matthew mentioned ongoing work on a sync bug and implementing updates for the genesis validator set. Bharath explained that transaction propagation issues were occurring due to a flag disabling local transaction propagation in the reth builder, and proposed two potential solutions: using a direct RPC server or removing the flag entirely. The team agreed to continue exploring these solutions, with Bharath planning to provide an update once a final approach is determined.

Agnish reported on several issues, including a custody column mismatch in the DA’s guardian system and MEV-related problems, both of which have been fixed. He is investigating a peering issue affecting Erigon nodes and a Segfault crash, which he suspects may be related to incorrect slot indication. Agnish expects to resolve these issues in the next few days and mentioned that the fixes will be deployed to Devnet 3.

The team discussed the integration of Nevermind with builders, noting that while it replaces state providers, it still uses EVM for execution and requires more testing. They decided to keep the transaction gas limit at 16 million, addressing concerns about backward compatibility and defi transactions. Kamil reported progress on stateful testing and gas benchmarks, mentioning the need for further verification and improvements in worst-case scenarios. Marcin introduced a new tool to check modex repricing issues, while the team considered a potential increase in gas limits to 60 million in the future.

The team discussed two main topics: a PR for explicit slot component times and a proposal to increase the balance for additional custody groups. They decided not to merge the slot component times PR at this time, as it would deprecate intervals per slot but make no substantial changes. The team also rejected the proposal to increase the balance for additional custody groups, citing concerns about last-minute changes and potential issues with dynamic DA conditions. Finally, Jae presented a new report from Sunnyside Labs on high block loads and perfect PDAOs, highlighting the need for more bandwidth for sync nodes and discussing plans to retest with unrestricted bandwidth limits.

The team discussed issues with syncing in perfect peerless mode, where Manu explained that Prism currently fails because it doesn’t reconstruct peers from 64 columns. They tested several clients including Lighthouse and Grandine, finding that while full syncing is possible without blobs, the connection issues prevent proper operation. The team agreed that while supporting 72 blobs might be necessary before Glamsterdam, it’s not currently a blocker for Fusaka releases, with Parithosh suggesting they could scale up to 30+ blobs for Fusaka without immediately requiring 72 blob support.

The team discussed the need for a “perfect peer mode” feature, with Manu advocating for its inclusion to ensure nodes can sync correctly even without supernodes. Francesco raised concerns about the practicality of operating without peers sharing the desired columns, questioning how a node could function in such a scenario. Jae noted that while tested nodes correctly received their columns for the first 1,000 slots, having the feature would provide added security. Raúl suggested that reconstruction during idle time could address scheduling issues, but Francesco remained unconvinced about the long-term viability of operating without compatible peers.

The team discussed two main topics: blob syncing and backfill features. For blob syncing, there was consensus that while the feature isn’t immediately necessary for 30+ blobs in Fusica, clients should prepare for potential implementation, with Prysm expected to complete their implementation by end of week. Regarding backfill, while some clients like Prysm and Lighthouse are working on it, there was discussion about whether it’s a critical feature for the 4.0 launch, with Agnish noting it would require significant CPU resources and Matthew indicating it’s a substantial body of work for Lodestar. The team agreed to revisit both topics at Thursday’s meeting, with Mario requesting CL teams to provide implementation timelines for the blob syncing feature.

### Next Steps:

- All CL teams to investigate how long it would take to implement perfect peerless syncing and provide updates at ACDC on Thursday.
- Nimbus team to work on optimizations to support higher blob counts.
- Lodestar team to continue working on implementing backfill functionality.
- Prism team to continue work in progress on implementing backfill.
- Sunnyside Labs to launch new devnets for testing as needed by client teams.
- All teams to review the PR on explicit slot component times and provide feedback before ACDC.
- Besu team to follow up async on the EIP 7951 benchmarking results.
- All teams to focus on fixing bugs in Nimbus and Lodestar this week before proceeding further.
- All teams to review the Sunnyside Labs report on high block loads and perfect peerless testing.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: ^&wiS^8e)
- Download Chat (Passcode: ^&wiS^8e)

---

**poojaranjan** (2025-08-04):

# ACD Testing Call #47 - (Quick Notes)

Facilitator: Mario Vega

## TL;DR

- Fusaka Devnet 3

Nimbus and Lodestar are still being debugged; fixes are underway.
- Decision: Wait until both are stable before advancing.

EIP-7825 Gas Limit

- Proposal to raise to 30M discussed; concern over app impact.
- Decision: Maintain current 16M gas limit on Devnet 3.

Gas Limit Testing

- Stateful and large contract tests in progress; repo flag awaited.
- ModExp pricing PoC tool being developed; Geth change not expected soon.

EIP-7951 (secp256r1) Benchmarking

- Besu results show high cost.
- Action: Mario to follow up with Besu team asynchronously.

INTERVALS_PER_SLOT Replacement (EIP-4476)

- Adds slot timing config without protocol changes.
- Decision: No breaking changes; clients should begin prepping for implementation.

PR-4477 Proposal

- Dev’s consensus that it’s too late for Fusaka.
- Decision: Do not proceed; no Devnet 4 for this. Plan shadow fork next.

Sunnyside Devnet / PeerDAS Syncing

- Sync failures in perfect PeerDAS; investigation ongoing.
- Decision: Feature required, clients to report progress.

Backfill Implementation

- Prysm, Lighthouse, and Lodestar in progress.
- Decision: Next ACD to revisit Devnet 4 for backfill.

## Fusaka Devnet 3

Barnabas:

- Devnet 3 is mostly stable with ~90% participation.
- All 5 Blob Parameter Only (BPO) forks are activated and running smoothly.
- Most prior issues have been resolved.
- However, 2 consensus clients — Nimbus and Lodestar — are still facing issues.
- Caplin also involved in ongoing testing.

Lodestar:

- Matthew K is investigating genesis value sync and working on resolving the bug.

Nimbus:

- Update relayed by Agnish:
- Issue with the custody column related to hash functions in indices.
- EF test vectors are passing.
- EAS (Earliest Available Slot) was not moving — now fixed.
- General updates: MEV issues were reported and have been addressed.
- Issue raised on Eth R&D Discord - Nimbus and Geth having difficulty syncing (likely a peering issue).
- DAS Guardian fix expected within the next few days.

Bharath:

- Local transaction propagation was disabled on the RETH node, which caused transactions not to be streamed.
- Fixes of issues shared on the call.
- Also, under discussion with the RETH team to consider removing local transaction propagation entirely.
- Some complications related to spam filtering reported, and the root cause of transaction exclusion has now been identified.

Roman (RETH): Inquired about the RETH flag and its specific issue.

Bharath: Shared technical context also shared on Eth R&D Discord.

Nethermind (Marek):

- Nethermind worked with rbuilder as state provider on integration with state
- The state sync component is ready, but the EVM integration is still in progress.
- Additional testing is requested before full readiness.
- More details: Flashbots Multi-client Support Announcement

### Conclusion & Next Steps

Mario:

- Overall, Devnet 3 is progressing well.

Barnabas:

- Aiming to ensure Nimbus and Lodestar are bug-free before moving forward.

## Raising the Limit of EIP-7825 to 30 Million

Mario:

- Provided an update from last Thursday’s ACD discussion.
- Discussion link on Ethereum Magicians.
- Raised concerns that raising the gas limit may negatively impact certain applications.

Toni:

- Stated that tradeoffs favor keeping the current spec as implemented in Devnet 3.

### Decision:

- Maintain the gas limit at 16 million for now.

## Gas Limit Testing Updates

Barnabas:

- No major updates.

Kamil:

- Still working toward full state testing.
- Marcin is running additional tests and benchmarking.
- EEST is running on existing infrastructure for stateful testing.
- A test is live on a contract with a very large state size; waiting on repo to receive the necessary flag.
- Some tweaks are needed on Devnet.
- BloatNet is being prepared; results expected this week.
- Will continue iterating and updating.

Marcin:

- Developing a new tool to evaluate ModExp pricing.
- Differences in gas usage are expected; further investigation underway.
- Currently working on a PoC — actual testing still pending.

Parithosh (in chat):

- Geth team noted that upstreaming changes would take time, if at all. Not a short-term solution.

Mario:

- No Geth representative was present to elaborate further.

Louis:

- Related issue: execution-spec-tests#1976
- Related PR for configuring gas limits: PR #1983

Kamil:

- 60M gas limit update still requires more testing.
- Genesis file handling and stateful test considerations are ongoing.

## Besu’s EIP-7951 Benchmarking Results

Justin (Besu): Updates shared in [Comment #1648](https://github.com/ethereum/pm/issues/1648#issuecomment-3149294281).

Mario:

- Initial results suggest the cost is too high. Will follow up asynchronously with the Besu dev team.

## Replace INTERVALS_PER_SLOT with Explicit Slot Component Times

- consensus-specs#4476

Justin Traglia:

- Introduced the PR to replace INTERVALS_PER_SLOT with explicit slot component times.
- Goal: Raise awareness now and propose merging within the next 3 months to begin implementation.
- This proposal adds additional config values; no substantial changes to protocol behavior.
- Believes there’s no reason to delay merging sooner.

Mario:

- Asked whether this introduces any breaking changes for Fusaka.

Justin T.:

- No breaking changes expected.
- Clients will need to update configurations, but should not impact Fusaka.

Pawan:

- Initial review looks good.
- Will revisit the PR for a deeper look.

## PR-4477 Discussion & Decision

- Barnabas shared and requested decison on PR.

Feedback from devs on call & chat:

- Justin T.: Against including this change.
- Alex S.: Suggests leaving it for now.
- Pawan: Opposes the proposal.
- Barnabas: Notes that the proposal has received support from some CL devs (Potuz, Terence, nflaig).
- Toni W.: Feels it’s already too late to consider this change.
- Csaba K.: Also against; if needed, should be done with a future BPO.
- Barnabas: Opposes bundling this change with BPO.
- Mario: Including this would require an entirely new fork.
- Pari: Suggests deferring it to Glamsterdam.
- Raul: Reminds that BPOs were explicitly designed to avoid code changes.
- Agnish: Opposes inclusion; the proposal is too tricky and more data is needed from dynamic DA conditions with supernodes.
- nflaig (Nico): Agrees it’s too late for Fusaka.

### Decision & Next step

- This PR will not move forward.
- Devnet 4 will not be launched.
- Focus will remain on stabilizing Nimbus and Lodestar before further progression.
- A shadow fork is being planned for next week. Barnabas encourages client teams to have established branches ready ahead of the shadow fork.

## Sunnyside Update

Update on [New Report](https://testinprod.notion.site/Sunnyside-Devnet-Updates-08-04-2458fc57f546808ab2c9e34480e0b7a9?source=copy_link):

- Successfully reached 60 blobs per block; observed impact on usage.
- Hit limits as expected per hardware requirements in EIP.
- Encountered genesis sync failures in perfect PeerDAS network setup.

Devs comments (from call & chat):

Manu:

- Provided explanation for Prysm issues on perfect PeerDAS.
- Actively working on a fix; expects resolution by end of the week.

Agnish:

- Requested clarity on the importance of syncing in perfect PeerDAS mode.

Pari:

- Clarified that Fusaka will not support PeerDAS with this in its initial release.
- This feature can be evaluated later, and if necessary, included in a future BPO.

Agnish agreed with this direction.

Mario:

- Agreed Perfect PeerDAS support is not required for Fusaka.
- May be revisited for future upgrades.

Agnish:

- Shared that reconstruction-based syncing offers more guarantees and would prefer that over relying on dynamic peer discovery.
- May need this feature.

Mario:

- Acknowledged that this feature might become necessary.
- Requested CL teams to confirm timelines for implementation as it may be a potential blocker for Fusaka.

Pawan:

- Currently does not have it implemented but is aware of the mechanism and will assess how long it would take to develop.

### Decision:

Mario:

- This is important enough to be tracked closely.
- Requested the rest of the CL team to respond.
- Will raise the topic again on the next ACD call for broader CL input.

Note:

Sunnyside may spin up additional testnets to support further PeerDAS testing.

## Backfill

Barnabas:

- Asked if any client implementations for backfill are in progress.

Manu:

- Prysm implementation is in progress.

Other Clients:

- Lighthouse and Lodestar are actively working on it.

Devnet 4 for Backfill?

Barnabas:

- Proposed the idea of a Devnet 4 focused on backfill testing.
- Suggested waiting for confirmation on ACD once client implementations are ready.

Backfill Implementation Challenges

Agnish:

- CPU usage is significant, depending on how quickly backfilling is expected.

Question raised: Should nodes provide slot-level data granularity while backfill is in progress?

Pawan:

- Mentioned they had to change the database structure to make Earliest Available Slot (EAS) accessible.
- Average backfill size observed: ~1 epoch.
- For their implementation, this is not a blocker.

### Conclusion:

- Awaiting updates on perfect PeerDAS syncing before proceeding further.

Suggest any changes to notes [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-47---Aug-04-2025).

---

**system** (2025-08-06):

### Meeting Summary:

The team reviewed the status of Fusaka Devnet-3 and discussed various technical issues including transaction propagation problems and sync bugs that are being addressed by different team members. They evaluated the integration of Nevermind with builders and discussed potential gas limit increases, while also considering proposals for slot component times and custody group balances. The team explored syncing capabilities in perfect peerless mode and discussed the implementation of blob syncing and backfill features, with plans to revisit these topics at the next meeting.

**Click to expand detailed summary**

The team discussed the status of Fusaka Devnet-3, where Barnabas reported 90% participation with two clients experiencing issues. Matthew mentioned ongoing work on a sync bug and implementing updates for the genesis validator set. Bharath explained that transaction propagation issues were occurring due to a flag disabling local transaction propagation in the reth builder, and proposed two potential solutions: using a direct RPC server or removing the flag entirely. The team agreed to continue exploring these solutions, with Bharath planning to provide an update once a final approach is determined.

Agnish reported on several issues, including a custody column mismatch in the DA’s guardian system and MEV-related problems, both of which have been fixed. He is investigating a peering issue affecting Erigon nodes and a Segfault crash, which he suspects may be related to incorrect slot indication. Agnish expects to resolve these issues in the next few days and mentioned that the fixes will be deployed to Devnet 3.

The team discussed the integration of Nevermind with builders, noting that while it replaces state providers, it still uses EVM for execution and requires more testing. They decided to keep the transaction gas limit at 16 million, addressing concerns about backward compatibility and defi transactions. Kamil reported progress on stateful testing and gas benchmarks, mentioning the need for further verification and improvements in worst-case scenarios. Marcin introduced a new tool to check modex repricing issues, while the team considered a potential increase in gas limits to 60 million in the future.

The team discussed two main topics: a PR for explicit slot component times and a proposal to increase the balance for additional custody groups. They decided not to merge the slot component times PR at this time, as it would deprecate intervals per slot but make no substantial changes. The team also rejected the proposal to increase the balance for additional custody groups, citing concerns about last-minute changes and potential issues with dynamic DA conditions. Finally, Jae presented a new report from Sunnyside Labs on high block loads and perfect PDAOs, highlighting the need for more bandwidth for sync nodes and discussing plans to retest with unrestricted bandwidth limits.

The team discussed issues with syncing in perfect peerless mode, where Manu explained that Prism currently fails because it doesn’t reconstruct peers from 64 columns. They tested several clients including Lighthouse and Grandine, finding that while full syncing is possible without blobs, the connection issues prevent proper operation. The team agreed that while supporting 72 blobs might be necessary before Glamsterdam, it’s not currently a blocker for Fusaka releases, with Parithosh suggesting they could scale up to 30+ blobs for Fusaka without immediately requiring 72 blob support.

The team discussed the need for a “perfect peer mode” feature, with Manu advocating for its inclusion to ensure nodes can sync correctly even without supernodes. Francesco raised concerns about the practicality of operating without peers sharing the desired columns, questioning how a node could function in such a scenario. Jae noted that while tested nodes correctly received their columns for the first 1,000 slots, having the feature would provide added security. Raúl suggested that reconstruction during idle time could address scheduling issues, but Francesco remained unconvinced about the long-term viability of operating without compatible peers.

The team discussed two main topics: blob syncing and backfill features. For blob syncing, there was consensus that while the feature isn’t immediately necessary for 30+ blobs in Fusica, clients should prepare for potential implementation, with Prysm expected to complete their implementation by end of week. Regarding backfill, while some clients like Prysm and Lighthouse are working on it, there was discussion about whether it’s a critical feature for the 4.0 launch, with Agnish noting it would require significant CPU resources and Matthew indicating it’s a substantial body of work for Lodestar. The team agreed to revisit both topics at Thursday’s meeting, with Mario requesting CL teams to provide implementation timelines for the blob syncing feature.

### Next Steps:

- All CL teams to investigate how long it would take to implement perfect peerless syncing and provide updates at ACDC on Thursday.
- Nimbus team to work on optimizations to support higher blob counts.
- Lodestar team to continue working on implementing backfill functionality.
- Prism team to continue work in progress on implementing backfill.
- Sunnyside Labs to launch new devnets for testing as needed by client teams.
- All teams to review the PR on explicit slot component times and provide feedback before ACDC.
- Besu team to follow up async on the EIP 7951 benchmarking results.
- All teams to focus on fixing bugs in Nimbus and Lodestar this week before proceeding further.
- All teams to review the Sunnyside Labs report on high block loads and perfect peerless testing.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: ^&wiS^8e)
- Download Chat (Passcode: ^&wiS^8e)

---

**system** (2025-08-06):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=bGepA_I1vTg

---

**system** (2025-08-13):

YouTube recording available: https://youtu.be/-ayYLnWSjsE

---

**system** (2025-08-13):

YouTube recording available: https://youtu.be/1CMMjyg0Mtw

---

**system** (2025-08-21):

### Meeting Summary:

The team reviewed ongoing network experiments and testing progress, including work on the Fussaka network, private mempool development, and Devnet 3 deployment with a new Prism fork. They discussed host key releases for the Holski scheme and planned future testing arrangements, while also addressing sync tests and benchmark releases with a new consolidated genesis format. The conversation ended with discussions on block-level access control implementation, EIPs related to gas repricing and multi-dimensional metering, and the handling of Ethereum call gas limits.

**Click to expand detailed summary**

The team discussed ongoing experiments with the Fussaka network, including non-finality tests involving full nodes and super nodes, which demonstrated successful recovery times of about an hour and 20-30 minutes respectively. Bharath reported progress on the private mempool, mentioning an issue with the get payload API transition that needs fixing, and suggested using the existing spammer jobs for testing, which Parithosh agreed to set up. The team plans to monitor the spammer jobs and peer-to-peer data, with Bharath committing to spend more time on the private mempool once the fork transition issue is resolved.

Parithosh reported on the progress of Devnet 3, where a new Prism fork with runtime hooks has been deployed for testing. The network is performing well with 1,500-1,600 nodes, and a BPO test is scheduled to check the system’s ability to handle high loads. The team discussed the performance of the network, noting that the test was successful. Dustin is working on a problem, and the team is looking into the cause of the issue. The team also discussed the performance of the network, noting that the test was successful. Dustin is working on a problem, and the team is looking into the cause of the issue.

The team discussed host key releases for the Holski scheme, noting that while community validators can support ad hoc releases, there were concerns about disrupting the normal release flow. They agreed to continue testing with Definite 4 and planned a shadow fork after final releases, with Parithosh requesting any testing accommodations be communicated in advance due to the time required to set up networks. Pawan suggested exploring longer non-finality periods for certain attacks, and Parithosh offered to set up a smaller test network for this purpose after Definite 4 testing concludes.

Parithosh reported on sync tests, noting a fix was needed for Nethermind and that Raphael ordered additional machines for testing. He mentioned a new page for tracking historic sync times across clients. Mario shared updates on benchmark releases, mentioning a new consolidated genesis format that allows for faster and more efficient testing. They discussed plans to extend this format to consensus tests in the future.

The team discussed implementation details for block-level access control and related testing. Toni confirmed that the execution specs exist and Teretto has started implementation in Git, but noted that a test environment is still needed. The team decided to activate block-level access control at the time of Glamsterdam and Toni will provide the necessary configuration. Parithosh suggested rebasing on top of Fusaka, but the team agreed to focus on getting a working devnet first.

The team discussed several EIPs and their implementation status, with a focus on gas repricing and multi-dimensional metering. Ansgar highlighted that the upcoming Glamsterdam fork will significantly impact network throughput and throughput levels. The team agreed to prioritize testing at higher throughput levels and prepare for Glamsterdam fork, which will significantly impact Ethereum’s throughput and throughput. The team also discussed the need for a shared development environment to test and validate the Glamsterdam fork’s impact on Ethereum’s throughput and throughput.

The meeting focused on discussing the implementation of gas limits for Ethereum calls, particularly in relation to EIP-7 and its impact on clients. It was agreed that the current wording of the EIP should remain as is, and the team will investigate the issue where the bug is located. The team agreed to leave the wording of the EIP as is and the decision was made to patch the bug.

### Next Steps:

- Bharath to fix the fork transition issue and spend more time on private mempool testing.
- Parithosh to set up spamming on the private mempool and analyze peer-to-peer data to ensure get tools are properly disabled.
- Client teams to review and approve Tanno’s EIP for merging this week.
- Mario to make another benchmark release and share it with the CK team for testing.
- Toni and Parithosh to coordinate on creating a Kurtosis config for block level access list implementation.
- Justin to merge the intervals per slot PR soon.
- Ansgar to create a meta EIP for gas repricing topics related to Amsterdam.
- Mario to check with the team about the merged fix for the modexp base and mode 0 issue.
- Client teams to double-check coverage of gas cost calculation issues this week.
- EF Protocol Security team to continue reviewing clients for potential issues.
- Client teams to manually test Eth calls against all client RPCs to identify which client has mistakenly configured the tx gas limit for Eth calls.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 1y&KpbrD)
- Download Chat (Passcode: 1y&KpbrD)

---

**system** (2025-08-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=lsJhGRKrpes

