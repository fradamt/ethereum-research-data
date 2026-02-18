---
source: magicians
topic_id: 25770
title: RPC Standards # 14 | October 13, 2025
author: system
date: "2025-10-13"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rpc-standards-14-october-13-2025/25770
views: 27
likes: 0
posts_count: 3
---

# RPC Standards # 14 | October 13, 2025

### Agenda

- Status: Open Agenda

> This meeting has an open agenda — topics will be proposed and discussed during the session.

**Meeting Time:** Monday, October 13, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1758)

## Replies

**system** (2025-10-13):

### Meeting Summary:

The meeting focused on standardizing JSON RPC error codes across EVM chains, with discussions centered on grouping and categorizing errors, particularly for transaction submissions and ETH calls. The team explored various technical aspects including error code numbering systems, the use of error messages and data fields, and the need to align error codes between different types of operations. The conversation ended with updates on API improvements and documentation, along with encouragement for continued participation in future discussions.

**Click to expand detailed summary**

The meeting focused on standardizing JSON RPC error codes across EVM chains. Sims presented a proposal to group and categorize errors, with initial work on transaction submission errors. Felix raised concerns about the large number of error codes and suggested starting with a minimal set focused on transaction submission and index queries. The group discussed using negative or positive error codes, with Sims agreeing to reduce the number of error codes and consider using positive numbers. They also explored the use of error messages and data fields in the specification, with Sims explaining that while messages are not currently required, they may be in the future to allow for more detailed error information.

The meeting focused on standardizing error codes for Ethereum clients, particularly for ETH call and transaction submission. Felix presented a proposal to use error code 3 for execution reverts in ETH calls, which was discussed by Łukasz and Simsonraj. The group agreed to align error codes between ETH calls and transaction submissions. Keri raised questions about the process for making changes to execution APIs, and Felix explained the challenges with using EIPs for this purpose. The team also discussed potential improvements to the JSON RPC API, including a new minimal REST API proposal by Geth. Zane provided an update on OpenRPC’s extension specification and documentation improvements. The conversation ended with Mercy urging participants to join future discussions to accelerate progress on these initiatives.

### Next Steps:

- Simsonraj to reduce the number of error codes in the proposal to focus on top hitters and remove those not relevant to clients.
- Simsonraj to consider changing error codes from negative to positive numbers in the next iteration of the proposal.
- Simsonraj to reuse existing error codes where applicable .
- Besu and Nethermind teams to implement error code 3 for execution reverted in ETH call.
- Felix to provide Simsonraj with more error codes that could be added to the proposal.
- Keri to review and merge PRs related to typos in the documentation.
- Felix to present the REST API proposal at the ETH Client Summit at DevConnect.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: =zNC9qkB)
- Download Chat (Passcode: =zNC9qkB)

---

**system** (2025-10-13):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=7cqkjADopvM

