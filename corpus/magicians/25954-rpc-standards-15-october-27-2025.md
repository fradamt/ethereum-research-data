---
source: magicians
topic_id: 25954
title: RPC Standards # 15 | October 27, 2025
author: system
date: "2025-10-25"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rpc-standards-15-october-27-2025/25954
views: 31
likes: 0
posts_count: 3
---

# RPC Standards # 15 | October 27, 2025

### Agenda

1. Error Handling for “Block Not Found”

Address the gap in rpc-compat hive tests to standardize error handling for “block not found” across all relevant RPCs (e.g., eth_getBalance, eth_getCode).

Reference: Besu PR #9303
2. Execution API Versioning
3. Execution-APIs PR Review

eth: add blockHash in Filter schema by MqllR · Pull Request #693 · ethereum/execution-apis · GitHub
4. eth: add eth_config API definitions for EIP-7910 by shemnon · Pull Request #678 · ethereum/execution-apis · GitHub
5. https://github.com/ethereum/execution-apis/pull/650

> Other Topics
> -

**Meeting Time:** Monday, October 27, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1782)

## Replies

**system** (2025-10-27):

### Meeting Summary:

The team discussed error handling improvements for block retrieval scenarios and agreed to align Besu’s behavior with the specification by returning null for non-existent blocks instead of errors. They explored versioning Execution APIs using semantic versioning and discussed updates to various pull requests, including one for GoEthereum that adds a block hash option to GetLogs. The conversation ended with updates on error reporting and testing improvements, including modifications to ranges, categories, and gas errors, along with discussions about integrating new test suites and error handling implementations.

**Click to expand detailed summary**

Mercy and Simsonraj discussed waiting for a few minutes before starting the stream, as Mercy was trying to tag people in the chat. Akash was helping with the stream and offered to let them know when to begin.

The team discussed an issue raised by Mark regarding error handling for block not found scenarios in GetBlock receipts. Felix explained that the pull request aims to fix tests by changing Besu to return null instead of an error, aligning with the specification that non-existent blocks should return null, not throw errors. The team noted that while this change affects multiple RPCs due to an abstract class, it is consistent with the defined behavior in the specification. Zane clarified that the expectation is for blocks to be found and not found scenarios to return null, not throw errors.

The team discussed inconsistencies in how Besu handles errors when accessing non-existent blocks, with Felix explaining that the API currently returns null for missing blocks while Besu returns errors. They identified that while the spec is clear, Besu’s behavior is inconsistent with other clients, and agreed that this needs to be addressed. The team also discussed the need to create a test for ETH calls with future blocks to clarify the behavior for such cases, and considered adding a dedicated “not found” error code, though this would require changes across all servers, specs, and tests.

The team discussed versioning Execution APIs to prevent clients from targeting a moving target, with Keri proposing semantic versioning and a changelog. Zane supported the idea and suggested creating a versioning.md file to outline rules for version bumps. Keri agreed to implement this before the next meeting, including steps for tagging, addressing issues, and having Hive pick up the changes. The team also briefly touched on three PRs related to the merchant rights API, which Keri was asked to review.

The team discussed a pull request for GoEthereum that adds a block hash option to the GetLogs function, which was confirmed to be an official EIP from 2017. While the functionality is useful for some clients, Nethermind does not currently support it. The team debated whether to return null or an error when the specified block is not found, with Felix suggesting that since the operation is impossible, an error might be more appropriate. The group agreed to proceed with merging the pull request, though the exact implementation of error handling was left open for further discussion.

The team discussed merging a pull request for error codes and agreed to proceed with it. Felix noted that the ETH config implementation was final, with a last call ending the next day. They also discussed the need to update test cases for ETH config, as the current tests would need to be backported into the test generator to ensure they remain up-to-date with changes to the test chain. Mercy inquired about the generation of .I/O files without corresponding tests, which Felix explained was due to the separate nature of the test generator and actual tests.

The team discussed challenges with testing ETH config, particularly regarding its dependency on the current block state and upcoming forks. Felix explained that their current test setup cannot simulate future forks, making it difficult to validate certain responses. Zane suggested adding a parameter to specify chain state for RPC requests, but Felix noted they already have a single test chain that is loaded before tests run. The team agreed to discuss the issue in Discord and potentially modify ETHConfig to remove the next fork feature, as it’s not yet finalized. They also decided to merge a PR that implements an EIP, with Mercy tasked to add a generated test. Finally, they briefly touched on JSON RPC error code standardization, noting that some changes were made after their last discussion on the topic.

Simsonraj presented updates on his work related to error reporting and testing for Ethereum clients. He explained that he had modified ranges, added new categories, and reduced the number of gas errors to reflect only those actually encountered. Simsonraj also created a new test suite and shared it on GitHub, which Felix found interesting. They discussed the potential to integrate this work with existing tools like Hive and RPC testgen, with Felix suggesting that running RPC testgen inside Hive could be beneficial. The conversation concluded with a brief mention of adding support for Nethermind, though Simsonraj noted it would take about a day to implement.

The team discussed improvements to the PR and error handling implementation. Simsonraj agreed to move the data field into the message field to align with OpenRPC standards, as suggested by Zane and Felix, who explained that the data field should specify a schema. Felix noted that the current implementation has some improvements over the previous version, including the addition of ZK errors. The team also agreed to review all defined error codes for accuracy. Mercy suggested moving the discussion to the ACDT call for further input from other clients.

### Next Steps:

- Felix: Create a test that tries ETH call with a future block after the call
- Felix: Implement error code handling for GetBlockReceipts after the call
- keri: Implement versioning for Execution APIs before next meeting, including creating a versioning.md file, tagging the current state, and updating Hive to pick up the tag
- Mercy: Add ETH config call to the RPC test generator
- Felix: Ping Dano to figure out what to do about the next Fork thing in ETH config
- Simsonraj: Move test suite to Hive or RPC testing
- Simsonraj: Add Nethermind to the error code testing
- Simsonraj: Move data field content into message field and remove data from the error code standardization proposal before tomorrow
- Simsonraj: Complete final commit with cleanup and README description updates before tomorrow
- Simsonraj: Send updated error code proposal to the channel before next week so it can be taken to ACD call
- Mercy: Create a PR for documentation changes on the website and send the PR link for further discussion

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: %2bH!#BK)
- Download Chat (Passcode: %2bH!#BK)

---

**system** (2025-10-27):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=ZEDNGE67qYU

