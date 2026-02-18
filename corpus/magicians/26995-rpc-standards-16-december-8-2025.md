---
source: magicians
topic_id: 26995
title: RPC Standards # 16 | December 8, 2025
author: system
date: "2025-12-07"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rpc-standards-16-december-8-2025/26995
views: 30
likes: 0
posts_count: 4
---

# RPC Standards # 16 | December 8, 2025

### Agenda

- https://github.com/ethereum/execution-apis/pull/650
- Execution API Versioning - Update README with versioning information by kclowes · Pull Request #704 · ethereum/execution-apis · GitHub

**Other Topics**

**Meeting Time:** Monday, December 08, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1836)

## Replies

**system** (2025-12-08):

YouTube recording available: https://youtu.be/YbMm1PkS5Uw

---

**system** (2025-12-08):

### Meeting Summary:

The team discussed versioning proposals for Execution APIs and JSON RPC error code standardization, with Keri providing updates on pending pull requests and Mercy sharing progress on various PRs. Mercy noted the absence of some team members for documentation and website updates, while Chase introduced himself as the new EF member for node infrastructure and RPC. The team addressed an ongoing issue between Geth and Nethermind regarding transaction types and agreed to continue the discussion in the Discord channel, with plans to reconvene in two weeks.

**Click to expand detailed summary**

Keri presented an update on the Execution APIs versioning proposal, which aims to provide version information to help client developers avoid compatibility issues with Hive specs. She mentioned addressing feedback and waiting for Felix’s input before merging the pull request. Keri also plans to set up a system where clients can test against both tagged and unstable versions of the APIs.

Mercy noted the absence of SIMS and another team member who were expected to discuss documentation and website updates for OpenRLPC, deciding to postpone these topics to the next call. Keri informed Mercy about upcoming enhancements to the website by Zane and OpenRPC, expected around the 24th due to a grant deadline. Mercy also mentioned the need to review stale open PLs, which she left for Keri to address.

The team discussed ongoing work on JSON RPC error code standardization, with Mercy sharing updates on PRs #673, #650, and #701. Keri suggested adding the JSON RPC error code discussion to the ACD call next Monday, even though Sims had already addressed some comments, to gather more feedback and potentially move towards merging. The team also briefly discussed a specific error code issue raised in a Discord thread, which Keri agreed to review. Chase introduced himself as the new EF member responsible for node infrastructure and RPC, noting this was his first meeting.

The team discussed an issue with transaction types between Geth and Nethermind, where Geth ignores transaction types while Nethermind uses them for execution. Kira noted that Geth currently serves as the de facto spec, though the official specs were written after Geth’s implementation. The team agreed to continue the discussion in the Discord channel, and Mercy mentioned she would share a Notion page about test cases. The group decided to reconvene in two weeks, avoiding the holiday season.

### Next Steps:

- Keri: Give it a couple more days for feedback on the Execution API versioning PR, then merge it and get something up in Hive
- Mercy: Get in contact with Sims before this week to discuss adding JSON RPC error code standardization to ACD call agenda
- Mercy and Keri: Add JSON RPC error code standardization to ACD call agenda for next Monday
- Keri: Take a look at the get log error thread and double check if a response is needed or if it needs to be put on one of the agendas
- Mercy: Share Notion page on Discord about cases where Geth is missing something or not complying with spec
- Nikita and team: Continue discussion about transaction type issues on Discord JSON RPC channel

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: v&fC7x66)
- Download Chat (Passcode: v&fC7x66)
- Download Audio (Passcode: v&fC7x66)

---

**system** (2025-12-08):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=30hy9fwIZ1Y

