---
source: magicians
topic_id: 25290
title: All Core Devs - Execution (ACDE) #220, September 11, 2025
author: system
date: "2025-08-29"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-220-september-11-2025/25290
views: 202
likes: 2
posts_count: 5
---

# All Core Devs - Execution (ACDE) #220, September 11, 2025

### Agenda

- Fusaka

devnet updates
- https://github.com/ethereum/pm/pull/1715

Glamsterdam

- Headliner updates

[The Weld](https://ethsteel.github.io/blog/blog_posts/2025-09-11_weld-announcement/)
EIP discussions

- EIP-7932: Secondary Signature Algorithms
- EIP-7980: Ed25519 transaction support
- EIP-7976: Increase Calldata Floor Cost
- EIP-7981: Increase access list cost
- EIP-2780: Reduce intrinsic transaction gas

[@adietrichs](/u/adietrichs) to chair ACDE from call 222 until EOY

**Meeting Time:** Thursday, September 11, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1707)

## Replies

**abcoathup** (2025-09-04):

### Summary

**
Summary by Tim Beiko**

PSA: Ansgar will be taking over ACDE during my leave, starting from Oct. 9 until EOY

**Fusaka**

- devnet-3 expected to finalize in the next day or so
- devnet-5 live, all BPOs expected by next week’s ACDC
- We agreed on the deployment process timelines, I’ve updated my PR to reflect this: https://github.com/ethereum/pm/pull/1715, will merge tomorrow if no objections on PR

**Glamsterdam**

- Progress on BAL spec discussions, first devnet expected by the end of this month
- EPBS breakout tomorrow

**The Weld**

- EL specs & testing repos are merging!
- All info here: The Weld - EELS + EEST - HackMD

**EIP discussions**

- Many EIPs discussed on the call (see agenda), mostly Q&A, no discussions about further Glamsterdam inclusions until Fusaka mainnet releases are out

### Recordings/Stream

- All Core Devs Execution #220 - Forkcast
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- ACDE #220: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDE Call #220 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnets: fusaka-devnet-3 [specs] & fusaka-devnet-5 [specs]
- Upgrade schedule (assuming testing goes well): Client releases (earliest September 22), Holešky upgrade + 1 week, Sepolia upgrade + 2 weeks, Hoodi upgrade + 2 weeks.  mainnet upgrade date to be selected after Hoodi safely upgrades.
- Holešky Testnet Shutdown Announcement | Ethereum Foundation Blog
- Consensus layer client team merge to trunk branches status

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners are being proposed for inclusion:

Discussions on The case for EIP-7932 & EIP-8030 inclusion in Glamsterdam,  EIP-7976: Increase Calldata Floor Cost,  EIP-7981 Increase access list cost & EIP-2780: Reduce intrinsic transaction gas

Presentation on [the Weld](https://steel.ethereum.foundation/blog/blog_posts/2025-09-11_weld-announcement/) (execution spec tests moving to execution specs)

---

**system** (2025-09-11):

### Meeting Summary:

The meeting focused on updates and discussions around the Fusaka Devnets, testing, and deployment timelines, including participation rates, plans for data collection, and issues with legacy blobs. The team agreed on various timelines for testnet releases and client deployments, with a consensus to maintain a 2-week gap between production testnets and between testnets and mainnet. They also discussed plans to consolidate Python test source code repositories by Q4 2025 and addressed post-quantum cryptography concerns, while reviewing two EIPs related to reducing worst-case block sizes and optimizing transaction costs.

**Click to expand detailed summary**

The meeting focused on updates and discussions around the Fusaka Devnets, testing, and deployment timelines. Parithosh reported on Devnet 3’s nonfinality testing and the launch of Devnet 5, noting participation rates and plans for data collection and analysis. The team discussed issues with legacy blobs at the fork boundary, with a consensus forming to drop them rather than convert, as other clients are not performing conversions. Tim mentioned a PR regarding the process for Fusaka deployment and a potential timeline for client releases and testnet deployments, with further discussion needed on specific dates.

The team discussed deployment processes and testnet timelines following the Pectra issues. They agreed to reduce the 30-day default waiting period, with a proposal to have 2-3 weeks between the first supported testnet and client releases, and potentially longer delays before moving to Sepolia. For Holesky, there was consensus to move faster, with a week between client releases and Holesky deployment, as infrastructure providers are less concerned with this testnet. The team also discussed aiming for client releases by the end of day on September 22, assuming successful completion of Devnet 5 and testnets.

The team discussed the timeline for testnet releases, agreeing to have a one-week gap between Holesky and Sepolia testnets. They decided to release both testnets in the same package, with Holesky forking on the week of the 29th and Sepolia on the week of the 6th, allowing for a three-week gap between releases. Tim proposed this schedule, which was supported by the team, with Stokes and James agreeing to a one-week gap and Justin confirming it was feasible for client teams to handle non-finalization testing.

The team discussed the timing between Ethereum testnets and releases, agreeing that 2 weeks should be the standard interval between production testnets and between testnets and mainnet. While there was general support for a 2-week gap, Tim noted that some teams might prefer more time, but the consensus was to maintain 2 weeks for consistency. The group also considered the timing between releases and testnets, with Tim suggesting a 1-week gap between Hoodi and Sepolia, though this was not finalized.

The team discussed and aligned on a testnet timeline, agreeing to 1 week between EOL testnet and client releases, 2 weeks between client releases and Holeski fork, 2 weeks between Holeski and Sepolia, and 2 weeks between Sepolia and Hoodi fork. They also reviewed updates on block access lists and EIPS, with Toni explaining current mapping of transaction indices and the proposal to include transaction indices for touched storage slots. The team confirmed that the Steel team’s work on merging testing and specs repos, named “weld,” was complete.

The team discussed plans to merge two repositories into one by Q4 2025, consolidating Python test source code, test frameworks, vector generation, and hive simulators under a single repository named “execution-spec-tests.” The main goal is to improve the developer experience by eliminating the need for the resolver tool and simplifying test coverage, while maintaining minimal disruption for clients. During a brief transition period, external contributions to the test repository will be paused to allow for cleanup, after which developers will direct their PRs to the consolidated repository.

The team discussed post-quantum cryptography and signature schemes, with Danno raising concerns about the proposed Ed. 25519 signature not being quantum-resistant. Felix suggested focusing on account abstraction rather than adding multiple elliptic curves, while Carl and Antonio mentioned ongoing work on Falcon post-quantum signatures. The group agreed that while there’s no immediate deadline, they should start working on a solution, with Justin emphasizing the need to abstract signatures early to accommodate future changes.

The meeting focused on discussing two EIPs related to reducing worst-case block sizes and optimizing transaction costs. Toni presented proposals to increase the floor cost and add data costs to access lists, which would help deprecate their use. Ben introduced EIP-2780, which reduces the base transaction cost to 6k gas and charges 25k for creating new accounts, addressing state growth concerns. The group also discussed the potential impact of these changes on transaction processing and access list usage. Ansgar announced he would be filling in for Tim during his absence, emphasizing his commitment to maintaining neutrality in discussions.

### Next Steps:

- Tim to merge the PR that reflects the agreed Fusaka deployment process  later today.
- Parithosh to apply the Geth fix to Devnet 3 and continue monitoring its recovery to finality.
- Geth team to investigate whether to continue with their plan to convert legacy blobs at transition or switch to dropping them like other clients.
- Client teams to look at their instances on Devnet 3 and investigate remaining issues based on the recovery summary thread.
- Client teams to prepare for releases by approximately the 22nd .
- Teams implementing block access lists to join the next breakout call in 2 weeks .
- Teams implementing EPBs to join the breakout call on Friday to discuss spec, tests, and finalizing scope for Devnet 0 .
- Steel team to proceed with the “weld”  in Q4 2023.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: *N!a$=?2)
- Download Chat (Passcode: *N!a$=?2)

---

**system** (2025-09-11):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=wc40rKbl2LY

---

**yashkamalchaturvedi** (2025-09-11):

![image](https://etherworld.co/favicon.png)

      [EtherWorld.co – 11 Sep 25](https://etherworld.co/2025/09/11/highlights-from-the-all-core-developers-execution-acde-call-220/)



    ![image](https://etherworld.co/content/images/2025/09/EW-Thumbnails--6-.jpg)

###



Ethereum core devs in ACDE #220 reviewed Fusaka devnets, testnet timelines, Glamsterdam features, the Weld repo merger & key EIPs on gas & cryptography.

