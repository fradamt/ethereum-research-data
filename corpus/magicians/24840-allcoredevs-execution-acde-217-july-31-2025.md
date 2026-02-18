---
source: magicians
topic_id: 24840
title: AllCoreDevs - Execution (ACDE) #217 | July 31, 2025
author: system
date: "2025-07-18"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/allcoredevs-execution-acde-217-july-31-2025/24840
views: 266
likes: 4
posts_count: 6
---

# AllCoreDevs - Execution (ACDE) #217 | July 31, 2025

# All Core Devs - Execution (ACDE) #217 | July 31, 2025

- Jul 31, 2025, 14:00 UTC

# Agenda

- Fusaka

Devnet updates
- EIP-7825 concerns
- Increase BALANCE_PER_ADDITIONAL_CUSTODY_GROUP from 32 to 128 ETH by dgusakov · Pull Request #4477 · ethereum/consensus-specs · GitHub
- Upgrade rollout

@ralexstokes proposal:

1 Sep - RC client releases
- 15 or 22 Sep - Sepolia
- 16 Oct - Hoodi
- 15 Nov - Mainnet

Ephemery? Holesky?
Audits / security reviews

[Glamsterdam](https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195)

- Community Feedback Thread

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : acde
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- Facilitator email: tim@ethereum.org
Note: The zoom link will be sent to the facilitator via email

[GitHub Issue](https://github.com/ethereum/pm/issues/1629)

## Replies

**abcoathup** (2025-07-21):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [AllCoreDevs - Execution (ACDE) #217 | July 31, 2025](https://ethereum-magicians.org/t/allcoredevs-execution-acde-217-july-31-2025/24840/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items
>
>
> Fusaka Devnet-3 Stability Testing
>
> Finalize debugging MEV-related issues and other client-specific bugs.
> Run “perfect progress” and non-finality tests; aim for stable participation above 94%.
>
>
>
> Finalize Decision on Transaction Gas Limit Cap (EIP-7825) on August 4 (ACDT)
>
> Currently capped at 16.8M gas per transaction; community concerns raised on Ethereum Magicians regarding breaking existing dApps.
> 0x highlighted DEX aggregator limitations; additional analysis forthcoming.
>
>
>
> C…

### Recordings/Stream

- https://www.youtube.com/live/IUS5Z-BD79M?t=169s
- ECH Institute:

Podcast (audio): [Ethereum Cat Herders podcast]
- Live stream on X: live stream [https://x.com/echinstitute]

### Writeups

- Tweet thread by @poojaranjan
- Tweet thread by @Christine_dkim [christinedkim.substack.com]
- Highlights from the All Core Developers Execution (ACDE) Call #217 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Ideally targeting mainnet before Devconnect
- Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Stakeholder feedback wanted
- Consensus layer headliner short list, decide headliner at ACDC August 8: EIP7732 ePBS, EIP7782 Six second slots & EIP7805 FOCIL
- Non-headliner EIPs can be proposed for inclusion now

---

**poojaranjan** (2025-07-31):

Tweet thread - https://x.com/poojaranjan19/status/1950920527968719228

---

**timbeiko** (2025-07-31):

### Action Items

1. Fusaka Devnet-3 Stability Testing

Finalize debugging MEV-related issues and other client-specific bugs.
2. Run “perfect progress” and non-finality tests; aim for stable participation above 94%.
3. Finalize Decision on Transaction Gas Limit Cap (EIP-7825) on August 4 (ACDT)

Currently capped at 16.8M gas per transaction; community concerns raised on Ethereum Magicians regarding breaking existing dApps.
4. 0x highlighted DEX aggregator limitations; additional analysis forthcoming.
5. Confirm Fusaka Upgrade Schedule by August 7 (ACDC)

Client teams to confirm preferred testnet order (Holesky, Sepolia, Hoodi) by next call; consider non-finality testing on Holesky.
6. Evaluate Custody Balance Parameter Adjustment (Consensus-spec Issue #4477) by August 7 (ACDC)

Proposal to increase BALANCE_PER_ADDITIONAL_CUSTODY_GROUP from 32 ETH to 128 ETH.
7. Impact on home stakers and fractional staking products (Lido CSM, Rocketpool).
8. Default decision is to defer from Fusaka; potential inclusion via future Block Parameter Override (BPO).
9. Block-Level Access Lists (BAL) Considered for Inclusion (EIP-7928, PR #10083)

Community consensus favors BAL as EL headliner for Glamsterdam fork (Ethereum Magicians feedback summary).
10. Benchmark “read+write” vs. “write-only” variants; report findings to determine final specification.
11. Finalize CL Headliner Decision (ePBS vs. Delayed Execution EIP-7862) by August 7 (ACDC)

CL community to choose between enshrined proposer-builder separation (ePBS) and delayed execution (EIP-7862).
12. Conditional support indicated for BAL as EL headliner if ePBS is chosen.

---

### Detailed Summary

#### Fusaka Devnet-3 Status

Devnet-3 stability improved, reaching ~94% participation. Ongoing debugging of client-specific and MEV-related issues. “Perfect progress” and non-finality tests planned shortly. Lighthouse and Nimbus to flag unresolved bugs before RC release.

#### Transaction Gas Limit Cap (EIP-7825)

Extensive debate over the proposed 16.8M gas cap. Community members, particularly [0x](https://0x.org), raised concerns about breaking existing DeFi aggregation use cases. Proponents highlighted benefits such as DoS mitigation and improved parallelization. Vitalik Buterin and others emphasized long-term advantages for client design simplification and potential future enhancements (e.g., multidimensional gas pricing, stateless clients). Additional analysis from affected dApps (notably DEX aggregators) requested; decision to be finalized during the August 4 ACDT call.

#### Fusaka Rollout and Testnet Schedule

General consensus on target schedule: client binaries by **September 1, 2025**; Sepolia, Hoodi, and Holesky forks sequentially through September and October; Mainnet by mid-November. Holesky identified for potential non-finality testing; client teams requested an additional week buffer for adversarial testing. Teams to confirm the preferred sequence by the August 7 ACDC call.

#### Custody Balance Parameter Adjustment

Discussion around increasing custody group balance threshold to 128 ETH ([consensus-spec issue #4477](https://github.com/ethereum/consensus-specs/pull/4477)). Concerns raised about impacts on home stakers, particularly regarding fractional staking and validator consolidation. Given complexity and timing, the decision deferred to future upgrade considerations, with further discussion at the August 7 ACDC call.

#### Glamsterdam Headliner: Block-Level Access Lists (EIP-7928)

Strong community and developer consensus resulted in BAL being Considered for Inclusion ([PR #10083](https://github.com/ethereum/EIPs/pull/10083)) as the EL headliner for Glamsterdam. Benchmarking needed between variants including/excluding read-locations. Conditional commitment pending final CL headliner decision.

#### CL Headliner Debate: ePBS vs. Delayed Execution (EIP-7862)

Deep debate between enshrined proposer-builder separation (ePBS) versus delayed execution (EIP-7862), which defers state root computation. Considerations around complexity, L1/L2 interoperability, and the “free option” problem discussed extensively. Consensus-layer teams to finalize choice at the August 7 ACDC call, with conditional commitment to BAL if ePBS is chosen.

---

**system** (2025-07-31):

### Meeting Summary:

The meeting celebrated Ethereum’s 10th anniversary before addressing technical issues related to transaction sizes and gas limits, with extensive discussion about whether to increase the limit from 16.8M to 20M or maintain the current level. The team also discussed a proposal to increase the requirements for node operators to become super nodes, with various perspectives on the impact of economies of scale. The conversation ended with plans for testnet releases and fork schedules leading to the mainnet launch, as well as discussions about potential headliners for the Glamsterdam fork.

**Click to expand detailed summary**

The meeting celebrated Ethereum’s 10th birthday before discussing two main issues. Barnabas reported that physical devastry had been stable with 94% participation, though Load Star and Nimbus were experiencing bugs related to library P.2.B and MEV respectively. The team addressed a transaction size capping issue where capping at 16.8 million gas could cause problems for some applications, with Toni noting that rbuilder restarts could temporarily fix the issue.

The team discussed concerns about reducing the transaction gas limit from 30 million to 16.8 million, with Duncan highlighting that this change would be a breaking one for application developers and expressing frustration about its late introduction. Vitalik argued for the importance of allowing breaking changes to enable future improvements, while Luis suggested that 30 million gas per transaction would be sufficient for current scaling needs. The discussion touched on various technical considerations, including the impact on distributed proving and parallel execution, with the team agreeing on the need for careful consideration of timing for such changes.

The group discussed the gas limit for transactions, with Duncan arguing for an increase from 16.8 million to 30 million to support larger decentralized exchange (DEX) aggregators. Toni presented data showing that only 0.3-0.4% of transactions were affected by the current limit, primarily affecting users of specific contracts like Uniswap. The team debated whether to set a higher limit now and potentially lower it later, or to start with a lower limit and adjust in future forks. They also considered the impact on scalability and the potential for deprecating high-gas transactions in future upgrades.

The team discussed adjusting the transaction gas limit, with a proposal to increase it from 16 million to 20 million. They considered the trade-offs between gas consumption and parallel execution capabilities. Vitalik suggested making this change sooner rather than later to allow for easier adjustments in the future. Duncan mentioned that he would provide more data on gas consumption for decentralized exchanges and the impact of the proposed changes later in the day.

The team discussed transaction gas limits, with a focus on whether to keep the current 16.8M limit or increase it to 20M. They decided to wait 2 weeks to make a final decision, with Duncan agreeing to provide numbers by the next day. The group also touched on the need for further analysis of worst-case scenarios for per-chunk code access pricing and multidim. Finally, they briefly mentioned a CL issue regarding increased requirements for CL nodes, which they agreed to resolve on the next CL call.

The meeting discussed a proposal to increase the limit for node operators to become super nodes, from 100 validators (4,000 ETH) to 512 validators (16,000 ETH). Dmitry argued this change would benefit home stakers by reducing hardware and bandwidth requirements, while Ansgar expressed concerns about encouraging economies of scale that could disadvantage solo stakers. The group debated whether the change would truly promote economies of scale, with Vitalik noting it could increase economies of scale between 32 ETH and 4096 ETH but decrease them between 4096 ETH and 16384 ETH. Potuz raised technical considerations about node distribution and block propagation, suggesting that increasing the number of validators while maintaining minimal column custody could be beneficial.

The team discussed a proposed change to staking parameters, with Tim suggesting to table the change for now and make a final decision on the CL call next week rather than at ACDT. The group agreed this was a philosophical rather than technical change, with Ansgar emphasizing it was too late in the process to make such a significant change. Barnabas confirmed the change was purely a config adjustment with no technical implications, and the team decided to maintain the current spec for the Fushaka launch while keeping the discussion open for potential future VPO changes.

The team discussed the timeline for testnet releases and the fork schedule leading to the mainnet launch. They agreed to aim for a September 1st release with a possible delay to September 15th if major bugs are found. The proposed schedule includes releasing Holeski and Sepolia in the week of September 8th, followed by a fork of Holeski on the week of September 15th, and then forking Hudi on the week of October 29th, assuming all goes well. The team plans to finalize these dates in the next week’s call, with the goal of forking the mainnet around November 3rd, just before Dev Connect.

The meeting focused on discussing headliners for the Glamsterdam fork, with strong support from CL teams for ePBS (Execution Payload Separation) and Block Access Lists (BALs). The team decided to CFI BALs as a candidate headliner while deferring the final decision on ePBS vs. delayed execution to next week’s CL call. There was discussion about the benefits of delayed execution for L2s and concerns about the free option problem, but the group agreed to move forward with CFIing BALs and making a final headliner decision next week.

### Next Steps:

- Duncan: Provide hard numbers on gas consumption by notional trade size on low-gas L2s for DEX aggregation by tomorrow morning.
- Duncan: Find and share transaction hashes of massively multi-atomic transactions for Vitalik.
- All participants: Review and analyze the impact of the 16.8 million gas limit over the next two weeks.
- All participants: Prepare for a final decision on the transaction gas limit at the next call in two weeks.
- Testing team: Maintain the current 16.8 million gas limit for tests until a final decision is made.
- All participants: Review and discuss the transaction gas limit change on Monday’s testing call.
- CL teams: Share opinions on the proposed change to increase the validator limit for custodying blob samples, either before or during the next CL call.
- All participants: Continue discussing and reviewing the proposed change to increase the validator limit for custodying blob samples on the GitHub PR.
- All client teams: Review and form opinions on the proposed change to increase the validator limit for custodying blob samples before the next ACDC call.
- Client teams: Prepare for potential testnet releases around September 1st, aiming for the Dev Connect timeline.
- All teams: Provide preferences for testnet forking order and timeline by the next call.
- All teams: Be prepared to finalize the “happy path” dates for testnet and mainnet forks on next week’s call.
- Client teams: Consider and be ready to discuss Block Access Lists as a potential EL headliner for the Amsterdam upgrade.
- Client teams: Prepare for further discussion on EPBs, shorter slot times, and fossil as potential CL headliners for Amsterdam.
- All teams: Provide preferences for the Cancun/Deneb rollout timeline by next week’s call.
- Core devs: Finalize the “happy path” dates for Cancun/Deneb rollout on next week’s call.
- Core devs: Make a final decision on EIP-4844 vs delayed execution as the CL headliner for Prague/Electra on next week’s call.
- Core devs: Discuss next steps on the transaction size limit on the testing call next week.
- Client teams: Continue implementation and testing of block access lists.
- Charit: Collect and share initial performance numbers for block access lists implementation.
- Core devs: Review the free option problem write-up before next week’s call to inform the EIP-4844 vs delayed execution decision.
- CL team: Finalize the decision on Epbs vs. delayed execution for Cancun headliners during the CL call next Thursday.
- CL team: Discuss and finalize the Cancun timeline during the CL call next Thursday.
- Core Devs: Make a final decision on including block access lists as a Cancun headliner, contingent on the Epbs decision.
- Client teams: Continue implementation and benchmarking of block access lists, including exploring variants with and without read locations.
- Jared: Gather benchmarks related to read locations in block access lists.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: !5WTY53T)
- Download Chat (Passcode: !5WTY53T)

---

**system** (2025-07-31):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=IUS5Z-BD79M

