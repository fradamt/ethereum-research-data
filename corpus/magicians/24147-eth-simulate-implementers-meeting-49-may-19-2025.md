---
source: magicians
topic_id: 24147
title: Eth_simulate Implementers' | Meeting # 49 | May 19, 2025
author: system
date: "2025-05-12"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eth-simulate-implementers-meeting-49-may-19-2025/24147
views: 171
likes: 1
posts_count: 4
---

# Eth_simulate Implementers' | Meeting # 49 | May 19, 2025

# eth_simulate Implementers’ Meeting # 49, May 19, 2025

- Date and time in UTC in format May 19, 2025, 12:00 UTC

# Agenda

- Notes from the last meeting
- Client Implementation update
- Test
- Discuss spec for eth_simulateV2

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: [Killari@gmail.com](mailto:Killari@gmail.com), [pooja@ethcatherders.com](mailto:pooja@ethcatherders.com)

 **🤖 config**

- Duration in minutes : 60 mins
- Recurring meeting : true
- Call series : eth simulate
- Occurrence rate : weekly # Options: weekly
- Already a Zoom meeting ID : false
- Already on Ethereum Calendar : false
- Need YouTube stream links : false
- display zoom link in invite : true

[GitHub Issue](https://github.com/ethereum/pm/issues/1537)

## Replies

**system** (2025-05-19):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

The team discussed keeping the Eth Simulate and JSON RPC calls separate, with Micah expressing concern that merging the calls could lead to decreased attendance and focus. Sina shared that their priority is maintaining attendance from current participants, and they are open to either keeping the calls separate or merging them, depending on scheduling. The group also discussed the need to achieve test parity with Spacewoo and other miners before pushing for the spec and tests to be merged in the repos. Mercy mentioned that the JSON RPC call currently meets bi-weekly at 3 PM UTC.

Mercy discussed project maintenance issues, particularly regarding the RPC API report and the need for someone to handle project maintenance due to numerous PRs pending review. Micah explained that for Ethereum simulate, the main challenge is getting clients like Geth, Nethermind, and Baysu to implement it, noting that it’s like “herding cats” and requires technical expertise in Ethereum JSON RPC. Micah suggested that future versions of eth simulate could accommodate design changes, but for v1, they need to focus on fixing issues and updating tests when clients like Geth or Nethermind encounter problems. S1na mentioned that Reth has a functioning implementation but doesn’t participate in calls, and suggested incorporating all clients into their CI flow for better observability and follow-up.

The team discussed adding Bay Sue to their fork of Hive, noting that if the code is on a branch, they need to know which branch. Micah suggested simply adding Bay Sue and letting failing tests alert them to issues, which could be as simple as checking the wrong branch. They agreed to post in Telegram and have Mercy reach out to non-failing client dev teams. The conversation ended with plans to meet again next week with Nethermind and Basu.

### Next Steps:

- Sina to add Besu, Reth, and Aragon to the Hive fork for eth_simulate testing.
- Mercy or other volunteers to reach out to client dev teams not currently participating in eth_simulate testing and encourage their involvement.
- Sina to update the Telegram channel with the status of adding additional clients to the Hive fork.
- Micah to continue poking Nethermind and Besu teams to participate in future eth_simulate calls.

### Recording Access:

- Join Recording Session (Passcode: yfff#y0T)
- Download Transcript
- Chat file not found in recording data.

---

**system** (2025-05-19):

YouTube recording available: https://youtu.be/oKV0cvi20Mc

---

**poojaranjan** (2025-05-20):

Updated Recording: https://youtu.be/t_FNyYNNQV8

