---
source: magicians
topic_id: 27418
title: RPC Standards # 18 | Jan 12, 2026
author: system
date: "2026-01-11"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rpc-standards-18-jan-12-2026/27418
views: 30
likes: 2
posts_count: 3
---

# RPC Standards # 18 | Jan 12, 2026

### Agenda

- Housekeeping

Open PR’s -

Add debug trace tests by MysticRyuujin · Pull Request #728 · ethereum/execution-apis · GitHub
- Update README with versioning information by kclowes · Pull Request #704 · ethereum/execution-apis · GitHub
- Feat: Docusaurus build in execution-apis by zcstarr · Pull Request #725 · ethereum/execution-apis · GitHub e.t.c

Open Issues -

- Call to Standardize `debug` Methods · Issue #651 · ethereum/execution-apis · GitHub
- Add block timestamp to `eth_getTransactionByHash` · Issue #729 · ethereum/execution-apis · GitHub
- Fully apply EIP-1898 in specs · Issue #713 · ethereum/execution-apis · GitHub

Untested JSON-RPC Methods Review Plan - 14 Untested JSON-RPC Methods: eth_accounts, eth_coinbase, eth_sendTransaction, eth_sign, eth_signTransaction, eth_gasPrice, eth_maxPriorityFeePerGas, eth_newFilter, eth_newBlockFilter, eth_newPendingTransactionFilter, eth_getFilterChanges, eth_getFilterLogs, eth_uninstallFilter, and debug_getBadBlocks.

CI workflow fail on some PR’s [Workflow runs · ethereum/execution-apis · GitHub](https://github.com/ethereum/execution-apis/actions)

**Meeting Time:** Monday, January 12, 2026 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1871)

## Replies

**system** (2026-01-12):

### Meeting Summary:

The team reviewed error code implementations and test plans for client implementations, with discussions around standardizing debug trace calls across Ethereum clients and improving the Docusaurus website for API method specifications. They explored versioning systems and release workflows, while addressing various technical issues including block timestamps and canonical requirements for block queries. The conversation ended with discussions about testing requirements and parameter parsing, along with scheduling conflicts for the next meeting.

**Click to expand detailed summary**

The team discussed error codes and test plans for client implementations. Simsonraj presented on the status of error code implementation and shared that other clients will review and provide feedback on the PR. Felix offered to help with test chain configurations and explained how RPC test generation works. They agreed that not all error codes need to be covered in testing, but some key ones should be implemented consistently across clients. Chase mentioned he had PRs ready for adding debug trace test and execution APIs, though he noted it might be challenging to get client agreement on some proposals.

The team discussed standardizing debug trace calls across Ethereum clients, focusing on two separate PRs: one for debug trace call and another for debug trace block by number. Felix suggested starting with basic opcode tracing and removing the trace config parameter to avoid overwhelming complexity. Tullio proposed specifying the output schema for the call tracer in the debug trace call PR. The group agreed to add tests for multi-contract interactions and subcalls. Mercy offered to champion the related EIP (EIP-3155) for standardizing trace output formats, though Felix noted this would be a collective effort. Tullio raised concerns about using EIPs as the primary mechanism for RPC layer standardization, fearing it could slow down progress.

The team discussed merging a PR for the Docusaurus website, which improves the display of API method specifications. Felix presented the changes, noting that while the new version has some issues, it’s an overall improvement over the current system. The team agreed to merge the PR, with plans to make additional refinements in future updates. They also briefly touched on the need to address why the CI is failing, though this was not fully explored in the meeting.

Mercy, Felix, and Chase discussed the need for a more robust versioning system for the API, emphasizing the importance of creating release workflows and attaching tests as artifacts. Felix highlighted that while the current PR for versioning is good, it’s only a description of what’s needed, and further action is required to establish a release strategy. Chase mentioned that Patches will work on integrating the test generator into the repository and figure out the build process. The team also discussed open issues, including standardizing the debug method and adding block timestamps to ETH transactions, with Felix raising questions about the utility of the latter feature.

The team discussed two main issues: a proposal to add block timestamp support for the ETH_getTransactionByHash API, which would require two calls for some clients but is easily implementable in Geth, and EIP 1898, which allows block hash and require canonical fields for certain methods but was previously unknown to the team. Felix noted that Geth already supports this EIP from 2019, and the team agreed to gather more client input before proceeding with any changes. Mercy offered to share the discussion with the ACDE group for further feedback.

The team discussed the implementation of a “require canonical” feature for block queries, with Felix expressing doubts about its practical usage despite its technical merits. Chase explained the feature’s value in preventing fork blocks from being returned during chain reorganizations, though the team noted that client libraries may not fully support this parameter. The group agreed to add tests to check parameter parsing, which Felix identified as a backlog item, and confirmed the merge of pull request 707 which adds the netversion method to the specification. Mercy will investigate issue 651 regarding debug method error behaviors, and the team identified a calendar conflict for the next meeting, which was supposed to be held the following Monday.

### Next Steps:

- Simsonraj: Signal in the group when test plan is ready for error codes
- Simsonraj: Reach out to Felix to work on implementing error code tests in Hive
- Chase: Refactor debug trace PR into two separate PRs - one for debug trace call only and another for debug trace block by number
- Chase: Remove trace config parameter from debug trace call PR to focus on the default tracer
- Tullio: Add full specification of the schema for the result in the case of the call tracer for debug trace call
- Chase: Champion EIP 3155 for standardizing call tracer output format
- Mercy: Bug clients about EIP 3155 on ACDT calls
- Felix: Merge the Docusaurus website PR after the call
- Felix: Update and merge the versioning PR
- Mercy: Add follow-up discussion on versioning and release strategy to next call agenda
- Chase: Talk to Patches internally about merging test generator into specs repository
- Chase: Link Mercy up with Patches in Discord regarding test generator work
- Felix and others: Add comments to issue 729  expressing support or concerns
- Mercy: Drop link for issue 729 to ACDE call for broader client input
- Felix: Create tests for EIP 1898
- Mercy: Check if RPC compat tests cover issue 651  and report back
- Felix: Merge pull request 707
- Chase: Bug Nixo to fix calendar for next meeting date

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: A%*7gUl8)
- Download Chat (Passcode: A%*7gUl8)
- Download Audio (Passcode: A%*7gUl8)

---

**system** (2026-01-12):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=iClCUfORtII

