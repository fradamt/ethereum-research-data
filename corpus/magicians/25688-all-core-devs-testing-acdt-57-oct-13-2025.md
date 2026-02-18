---
source: magicians
topic_id: 25688
title: All Core Devs - Testing (ACDT) #57, Oct 13, 2025
author: system
date: "2025-10-06"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-57-oct-13-2025/25688
views: 61
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #57, Oct 13, 2025

### Agenda

### UTC Date & Time

[October 13, 2025, 14:00 UTC](https://savvytime.com/converter/utc/oct-13-2025/2pm)

### Agenda

#### Fusaka:

- Fusaka Holesky BPO fork updates
- Fusaka devnet status updates
- Remove named forks from blob_schedule fields

#### Gas limit testing update:

- 60M gas limit on mainnet updates
- State test updates

#### Glamsterdam Testing Updates:

- BALer updates
- ePBS updates

#### Other Topics

- RPC Test Failures (See rpc-compat), Ethereum needs Standards-Punk - Meta-innovation - Ethereum Research

**Meeting Time:** Monday, October 13, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1756)

## Replies

**poojaranjan** (2025-10-13):

# ACD Testing Call #57 - October 13, 2025 (quick notes)

Mario Vega moderated the call.

## Fusaka Holesky BPO Fork Updates

Barnabas

- BPO fork update shared. Next fork scheduled for tonight
- Sepolia fork planned for tomorrow
- Noted a minor drop in participation
- Last week’s Sepolia shadow fork went well

Client Team Updates

- Prysm: New release out — v6.1.2
- Ameziane (Besu): Release supporting 60M gas coming this week
- Other clients to follow asynchronously

Bharth

- Announced a new MEV-Boost release
- This includes, added fallback support
- Flashbots should be ready for Sepolia
- Relay + client coordination appears fine
- Validators on Sepolia are encouraged to upgrade - details shared on Validators Telegram
- Client teams may call the v2 API from Fulu or the fallback support
- MEV-Boost will manage the fallbacks automatically

Barnabas shared

![image](https://hackmd.io/_uploads/H1gHuq5Tge.png)

## Remove Named Forks from blob_schedule Fields

Context:

Discussion reference: [Discord](https://discord.com/channels/595666850260713488/688075293562503241/1425748011438575719)

Barnabas

- Proposed for clients team to remove named forks from “Blob_schedule” fields and only have explicit BPO values in there.
- Already implemented in Besu and Nethermind
- Requested confirmation from remaining EL teams

Related PRs:

•	[chore: remove osaka from blob schedule in genesis.json by barnabasbusa · Pull Request #23 · eth-clients/hoodi · GitHub](https://github.com/eth-clients/hoodi/pull/23)

•	[chore: remove osaka from blob schedule in genesis.json by barnabasbusa · Pull Request #119 · eth-clients/sepolia · GitHub](https://github.com/eth-clients/sepolia/pull/119)

•	[chore: remove osaka from blob schedule in genesis.json by barnabasbusa · Pull Request #136 · eth-clients/holesky · GitHub](https://github.com/eth-clients/holesky/pull/136)

Marius

- Confirmed it hasn’t been implemented in Geth yet
- No objections to the change

## 60M Gas Limit on Mainnet — Updates

Kamil

- EL clients are generally ready for the 60M gas limit.
- Good milestone: several nodes currently running at this configuration.
- Erigon and Reth have some issues; others performing well.
- Nethermind shows occasional instability but not consistently.
- No major bottlenecks identified so far.

Q: Why aren’t benchmarks matching mainnet behavior?

Kamil has a few possible theories:

- Differences in preparation block design
- Varying cache strategies across clients
- Hardware differences between test nodes
- Other implementation-specific factors

Ameziane

- Asked if the exempt blocks were part of the performance devnet.
- Kamil clarified:
•	The blocks were manually crafted by his team
•	They’re testing a variety of load and attack scenarios
•	More edge cases still need to be explored

### Next Steps

- Kamil and Ameziane to sync asynchronously on profiling tool integration
- Teams encouraged to suggest test scenarios
- Contributions welcome to add extra benchmark tests via this issue.

From Zoom chat:

- cperezz: XEN is larger on Bloatnet; depth is already 8–9, so it would take extreme bloat to shift impact.
- Mario: Confirms testing is headed in the right direction.
- Jochem Brouwer: Worst-case client scenarios should go into the benchmark suite.
- Teams noticing edge cases should reach out so they can be added

## State Test Updates

Marcin

- Currently analyzing ModExp test cases
- Artificially increased gas price to surface edge cases
- Identified a few hundred failing transactions post-Fusaka
- Failures follow the same pattern and error message
- Frequency: roughly 1 transaction per hour
- Error originates from Account Abstraction

Example:

Error: [AA40 over verificationGasLimit](https://etherscan.io/tx/0x1010c2cbd31e3c46e512670bfc41f995a4811fc1bbceb62363d4a712dabc1b10)

Hypothesis:

- General gas limit changes might be causing the issue
- Account Abstraction has a gas limit, which may not align with new conditions

Next Step:

- Confirm the root cause
- Determine whether the issue resolves under Fusaka rules or requires action

## Glamsterdam Testing Updates - BALer Updates

Felipe

- Some test vectors released last week
- Fixes were merged this morning
- A full release will follow after verifying if anything else is missing

Latest Test Results — Release v1.2.0

Shared by raxhvl (chat)

1.	Besu: 80/90 (89%)

2.	Reth: 67/90 (74%)

3.	Geth: 64/90 (71%)

4.	Nethermind: 63/90 (70%)

From Zoom chat

- Stefan: Encouraged improving the number of passing tests
- Mario: Asked which tests are failing
- Felipe:
•	Most failures are spec tests
•	Issues tied to gas handling
•	Both spec and test vectors were updated over the weekend
•	Previous vectors were incorrect

Jared Wasinger (chat)

- Asked Rahul if tests are being run with the bal-devnet-0 branch of Geth
- Locally, two tests fail on the master branch (as of 12 hours ago)
- One known incorrect test is documented here: https://pokebal.raxhvl.com/

#### Action: Coordinate with Rahul and Felipe on BALer test issues

## ePBS Updates

Justin T

- Client teams are still focused on Devnet 0
- Expect Devnet 0 to be ready by the end of the month
- Some decisions are expected during the ACDC call

## RPC Test Failures & Standardization Discussion

Reference: [Ethereum needs Standards-Punk - Meta-innovation - Ethereum Research](https://ethresear.ch/t/ethereum-needs-standards-punk/23151)

As shared in this post, failures in RPC test suites (via rpc-compat/Hive) triggered a broader conversation on RPC fragmentation and the lack of standardization across clients and providers.

Sebastian Bürgel (Gnosis) provided an overview of the situation.

- Highlighted that apps rely heavily on the Ethereum RPC layer
- EthPandaOps provided help with testing
- Two core gaps were identified:

Hive’s scale hasn’t grown with Ethereum’s complexity
- Lack of shared understanding and consensus on RPC behavior

Łukasz Rozmej (Chat): We have consensus on Ethereum as a protocol — we don’t have consensus on RPC calls.

Jochem: Noted that RPC standardization efforts exist (e.g., ongoing “RPC Standards” call), but they’re still very basic.

Marius shared EF & Client Perspective

- Acknowledged the long-standing nature of the issue
- RPC was originally designed for Mist
- Hard to evolve due to broad ecosystem dependencies
- Nodes today are vastly different vs. 10 years ago
- Resource constraints and prioritization slow progress
- EF plans to allocate help; client teams have requested support

Łukasz shared about Current RPC Standards Efforts

- Joined the RPC spec calls — still at early/“basic” stages
- Concern: RPC providers may resist standardization
- Some things should remain client-implementation-specific
- Hive tests are often Geth-derived — not always portable
- Some fields/behaviors are tested superficially or omitted entirely
- Nethermind is running its own set of Hive tests for specific testing

Mercy (shared in cha)

- Shared proposals on error code standardization:
- JSON RPC Error codes standardization using open-rpc extension specs by simsonraj · Pull Request #650 · ethereum/execution-apis · GitHub
- https://github.com/simsonraj/execution-apis/blob/527bb9af49ba12bbed37cc36d4cfe42048cd114e/src/extensions/README.md
- Feedback from client teams and the wider community is needed

Spencer (chat): Suggests making it an EIP if the community wants it implemented

Call resources shared:

•	Discord channel + recurring working group calls

•	[RPC Standards # 14 | October 13, 2025 · Issue #1758 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1758)

Keri (chat)

•	Emphasized the need for more client devs to attend RPC meetings

Felix provided an overview of Test Suite Challenges

He clarified:

- Geth is not the spec — only used to generate test vectors
- Specs are independent YAML files
- Results are compared across implementations
- Differences often come down to:
- Error code expectations vs. values
- Testing today:
•	Slow to expand
•	Mostly manual review
•	Coverage is good but not exhaustive
- Suggestions:
•	Improve methodology
•	Add more test cases gradually
•	Contributions welcome via repo
•	Nimbus is failing the most; should be addressed
•	Client teams should attend RPC standardization calls

Sebastian Bürgel rebuttal on Broader Process Debate

- Pointed out structural mismatch:
- Current approach tries to force RPC standards through the EIP process
•	Suggested reviewing alternative standards lifecycles:
•	Life Cycle of a Blockchain Standard - cd ~

Barnabas: To succeed:

- Needs to be an EIP
- Needs a champion
- Needs someone dedicated who won’t burn out
- Important but thankless work

Mario concluded the call

- Encouraged teams to join the next RPC call today
- Suggested supporting EELs with testing language-specific tooling

---

**system** (2025-10-13):

### Meeting Summary:

The team reviewed progress on BPO forks and MEVBoost release updates, including discussions about removing named forks from the schedule and ensuring clients can run with static tests. They examined gas limit testing across multiple Ethereum clients and discussed performance variations, with plans to investigate potential discrepancies further. The conversation ended with extensive discussions about RPC standardization challenges, testing coverage issues, and the need for improved test cases and specifications across Ethereum clients.

**Click to expand detailed summary**

The meeting discussed updates on the BPO fork for Holesky and Sepolia, with Barnabas reporting smooth progress and minor participation drops. Bharat shared updates on the new MEVBoost release (VE1.10 Alpha 6), which now supports fallback to the V1 Blinded Blocks API if the V2 API is not supported by relays. The team agreed to remove named forks from the BPO schedule in the genesys.json file, with Barnabas explaining that this is redundant since named forks cannot update values on the CL side after Cancun. The conversation ended with an agreement to make a new release to ensure clients can run with static tests and update the DevNet notes.

The team discussed gas limit testing, with Kamil reporting progress on stateful testing using five major Ethereum clients (Nethermine, Besu, Geth, Erigon, and Reth) on top of BlobTnet. Kamil noted that while performance varied, with Nethermine showing the biggest struggles, the current benchmarks did not fully align with mainnet observations. The team discussed potential reasons for the discrepancy, including caching differences between clients and hardware considerations, with Ameziane offering to help with profiling tools and Mario suggesting further investigation of block preparation and testing scenarios.

The team discussed several topics related to Ethereum client development and testing. Kamil requested feedback on stateful scenarios and performance bottlenecks from clients, while Marcin presented findings on transaction failures under different consensus rules. The group reviewed test results for block-level access lists, with Felipe reporting that some test vectors needed fixes but were already merged. They discussed the need for more clients to pass tests before starting a devnet, and Justin provided an update on the delayed DevNet Zero implementation. Finally, Sebastian introduced a discussion on RPC test failures, which he had raised in a recent Ethereum research post.

Sebastian highlighted critical issues with the Ethereum RPC layer, emphasizing the need for extensive test cases and standardization to ensure the reliability of Ethereum-based applications. He noted that current test coverage is insufficient, with only 190 tests for the entire RPC layer, and highlighted inconsistencies in client implementations, particularly regarding log retrieval. Marius and Łukasz discussed ongoing efforts to address these issues, including proposals for REST-based APIs and improved log indexing, while acknowledging the challenges of prioritizing RPC improvements due to finite developer resources and the need for broader consensus among client teams.

The team discussed challenges with RPC standardization and testing, with Łukasz highlighting that while Geth serves as a de facto specification, some differences exist between clients that need addressing. Felix clarified that while Geth is used for generating test vectors, the official specs are contained in YAML files, and the team is working on expanding test coverage while being mindful not to overwhelm clients with hundreds of failing tests. The group agreed that client developers need to attend RPC standardization meetings to reach consensus, and Justin Florentine suggested that the process needs to be formalized through an EIP with a dedicated champion.

The team discussed challenges with testing eth_getLogs for large ranges and the need for a testing pipeline to sync multiple clients and conduct fuzz testing. They acknowledged resource constraints due to hardfork season but agreed to prioritize this task. The group decided to continue the discussion in the next RPC call and bring it up in the ACDE meeting. Mario suggested exploring a better specification model, potentially incorporating ideas from EELS into the RPC testing framework to improve test generation.

### Next Steps:

- Client teams to update Sepolia validators to use the new release of MEVBoost  which supports fallback to V1 Blinded Blocks API.
- Lighthouse, Besu, and Grandine teams to provide information about stable releases before Hoodi.
- Besu team to release a new version for Hoodi and mainnet related to 60 million gas limit this week.
- EF team to make a new release to ensure they are not including named forks in the BPO schedule.
- Client teams to check the failing tests in the Block-level access list test results and fix any outstanding issues on their side.
- Client teams to reach out to Felipe and Raul if there are any unknowns on the Block-level access list tests.
- Client teams to continue working on DevNet Zero implementations for EPBS.
- Client teams to investigate the RPC test failures and attend the RPC standardization calls to address the issues.
- Sebastian and interested parties to join the next RPC call and ACD to continue the discussion on RPC standardization.
- Client teams to help Kamil with profiling blocks and suggesting interesting stateful scenarios for gas limit testing.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: XwtMY9C%)
- Download Chat (Passcode: XwtMY9C%)

---

**system** (2025-10-13):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=R7cs3ogM7f4

