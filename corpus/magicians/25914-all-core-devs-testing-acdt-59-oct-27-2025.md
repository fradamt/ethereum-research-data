---
source: magicians
topic_id: 25914
title: All Core Devs - Testing (ACDT) #59, Oct 27, 2025
author: system
date: "2025-10-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-59-oct-27-2025/25914
views: 58
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #59, Oct 27, 2025

### Agenda

#### Fusaka:

- Sepolia BPO fork events/updates
- Devnet status updates
- Hoodi Activation updates

#### Gas limit testing update:

- 60M gas limit on mainnet updates
- State test updates

#### Glamsterdam Testing Updates:

- BALer updates
- ePBS updates

#### Other Topics

- RPC updates
- RIP Holesky
- EIP-7610
- Weld updates (EELS+EEST)

**Meeting Time:** Monday, October 27, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1778)

## Replies

**poojaranjan** (2025-10-27):

# All Core Devs - Testing (ACDT) #59 October 27, 2025 (Quick Summary)

Mario Vega facilitated the call

## Fusaka:

### Sepolia BPO fork events/updates

Barnabas

- BPO 1 fork happened last Monday.

- BPO 1 completed successfully
- BPO 2 expected in ~9 hours
- Everything running smoothly; no major client issues reported

Other updates

- Devnet 3 remains online — expected to continue for about a month
- Validators: please update your nodes and stay online as much as possible

### Holesky deprecation

- Holesky has been deprecated
- Migration recommended to Sepolia and Hoodi for continued testing
- Holesky stopped finalizing as of Oct 27 (10:32 AM UTC)

Minhyuk Kim

- Suggested Hoodi fork before Sepolia sunset to support L2 project testing

Barnabas

- Emphasized balancing between home staker and L2 operator needs

Marius van der Wijden

- Encouraged everyone to use Sepolia for L2 testing

Mario Vega

- Advised moving to Hoodi
- Confirmed fork sequence: Sepolia first, then Hoodi

## Gas Limit Testing Update

- 60M gas is now set as the default value across all clients.

### State Test Updates

Kamil

- All compute tests are running fine.
- Some scenarios are merging faster — currently under review.
- Major milestone: discovered a way to overcome a key stateful testing challenge.
- Implemented better result comparison methods.
- Shared the latest compute test updates.
- Found one issue in n/m, which has been fixed.
- Working on creating a custom buffer file for improved test handling.

## Glamsterdam Testing Updates:

### BALs

Raxhvl

- A new release is coming up with 20 additional test cases.
- Identified a bug during BAL testing.
- Shared a presentation detailing findings.
- Two bugs were missed earlier — one in Geth, another in Nethermind.
- Shared a small presnetation with suggestions.

Stefan

- Devnet is in progress.
- Invited CL client teams to reach out and join the devnet implementation efforts.

### ePBS

Justin T.

- Everything looks good so far; waiting for devnets to start.
- Next ePBS breakout is scheduled for Friday.
-Requested all client teams to join the upcoming meeting.

## Other Topics

### RPC Updates

Lukasz

- Two weeks ago, RPC enhancement discussions were initiated.
- Proposed changing the reverted error code to be free.
- Suggested a larger discussion may be needed around blob fields and related tests.

Keri

- Recommended opening an issue on the Execution API GitHub for further review by the team.

### EIP-7610 Discussion

Marius

- Provided overview that this EIP defines a specific scenario.
- Mentioned there are 28 such instances on mainnet that cannot be easily removed.
- Explained a theoretical example of deploying a contract to illustrate the challenge.

### Weld updates (EELS+EEST)

Dan provided a summary

- Weld focuses on migrating code from the execution-spec-tests repository to the execution-specs repository.
- This integration will improve alignment between the spec and testing processes.
- The team has been working intensively over the past few weeks, and an update has been posted — though it is still a work in progress (WIP).
- As a result, the old repositories are being phased out and execution-spec-tests will now contain the test fixtures, and test fixture releases, but no code.
- For Osaka, contributors can open pull requests directly in the new repository.
- Amsterdam contributors are advised to hold off temporarily until further notice.
- Regarding benchmarking, Louis has a large PR in progress to restructure workflows — expect significant upcoming changes.
- Client teams do not need to take any action at this stage.
- Updated testing documentation will be published on the official website once available (currently WIP).

PS: This is a quick note, please suggest any changes [here](https://hackmd.io/@poojaranjan/ACDT59Onwards#All-Core-Devs---Testing-ACDT-59-October-27-2025).

---

**system** (2025-10-27):

### Meeting Summary:

The meeting covered updates and discussions about various testnets, including the Sepolia and Hoodi forks, as well as the deprecation of the Holesky testnet, with Barnabas providing specific timing details for upcoming events. The team reviewed performance testing efforts, including improvements in stability and gas limit discussions, while also addressing concerns about test case documentation and devnet updates. The conversation ended with discussions about ePBS releases and consensus specifications, including updates on test cases and storage-related issues, along with an announcement about the “weld” project and contributor guidelines.

**Click to expand detailed summary**

The meeting focused on updates and discussions related to the Sepolia and Hoodi forks, as well as the deprecation of the Holesky testnet. Barnabas confirmed that BPO2 was scheduled to happen in 9 hours, followed by the Hoodi Fork, and noted that BPO1 on Hoodi would be reviewed a week later. The team discussed the status of the devnet, which was expected to remain online until midnight, and emphasized the need for participants to update their notes and stay online during the transition. Minhyuk raised concerns about the removal of Holesky, highlighting its utility for testing upcoming forks, and Barnabas explained the challenges of coordinating Hoodi’s larger user base. The conversation ended with a reminder for clients to confirm and update their gas limits to 60 million, as it was the default setting for most clients.

The team discussed performance testing and profiling efforts, with Kamil reporting on stateful and compute tests, including improvements in stability and the creation of a custom Docker file for detailed tracing. They also addressed gas limit increases, with Marius and others discussing EIPs related to gas pricing and precompiles, while Kamil noted that recent benchmarking showed improvements but required further evaluation. The conversation ended with a brief mention of Block Access List updates and a reminder about Rahul’s presentation on that topic.

Rahul presented updates on a new release with 20 test cases for Coinbase withdrawals and edge cases, and highlighted a bug that escaped detection by all three clients during early testing. He proposed maintaining a formal Markdown document for test cases to improve collaboration and suggested linking it to EIPs, which sparked a discussion on whether to keep test cases within EIPs or in an external document. The team also discussed updates on devnets, with Stefan confirming they would be ready by the end of the day, and Mario noted that Holesky has officially stopped finalizing.

The team discussed updates on ePBS, including a new Consensus-specs release with additional ePBS tests for COAS and a rejected proposed structure change to attestation. They noted that a missing Gossip condition check was identified for fixing. The next ePBS breakout call is scheduled for next Friday, and clients were encouraged to attend. Łukasz raised concerns about the need to update ETH simulation tests to reflect the reverted error code change and discussed potential issues with transaction type resolution logic. Keri suggested opening issues in the Execution APIs repo to address these concerns. Mario mentioned a discussion about EIP 7610 regarding storage dangling in contracts, which was deemed underspecified.

The team discussed an edge case involving contract deployments to accounts with no code but existing storage, which was previously addressed by EIP-684. They debated whether to leave the storage as-is or implement a self-destruct approach, with Gary expressing concerns about the semantic implications of leaving storage unchanged. The group agreed to continue the discussion offline and revisit it at the upcoming ACDE meeting. Additionally, danceratopz provided an update on the “weld” project, announcing that Osaka contributors can now start PRing to the default execution-specs branch, while Amsterdam contributors should hold off until the fork is rebased.

### Next Steps:

- All node operators: Update nodes and be online as much as possible for Hoodi fork activation
- All users on Holesky: Migrate away from Holesky to Sepolia or Hoodi as soon as possible
- Barnabas: Clean up devnet 3 nodes that have run out of disk space
- All client teams: Confirm that 60 million gas default is set in their clients, reach out if not the case
- Kamil: Share custom Docker file documentation for profiling once merged
- Kamil: Continue working with Luis to get latest version of compute tests aligned with EST
- Stefan: Complete devnet setup by end of today for Block Access List testing
- Client teams with finished implementations: Reach out to Stefan to join the Block Access List devnet
- Rahul: Release new version with about 20 test cases covering Coinbase withdrawals and edge cases for storage and account access
- Łukasz: Open two issues on Execution APIs repo regarding reverted error code and transaction type resolution logic
- All contributors: Direct all PRs and issues to Execution specs repository
- Amsterdam contributors: Hold off on PRs until fork is rebased on top of Fusaka
- All teams: Continue discussion on EIP 7610 async in STEEL Discord server and evaluate options
- All teams: Revisit EIP 7610 discussion on ACDE if needed

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 3cR@^ky!)
- Download Chat (Passcode: 3cR@^ky!)

---

**system** (2025-10-27):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=zfrPOtUxK90

