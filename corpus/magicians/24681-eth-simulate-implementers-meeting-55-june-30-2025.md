---
source: magicians
topic_id: 24681
title: Eth_simulate Implementers' | Meeting # 55 | June 30, 2025
author: system
date: "2025-06-27"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eth-simulate-implementers-meeting-55-june-30-2025/24681
views: 116
likes: 0
posts_count: 2
---

# Eth_simulate Implementers' | Meeting # 55 | June 30, 2025

# eth_simulate Implementers’ Meeting # 55 |  June 30, 2025

- Date and time in UTC in format June 30, 2025, 12:00 UTC

# Agenda

- Notes from Meeting 54
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
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : false
- display zoom link in invite : true

[GitHub Issue](https://github.com/ethereum/pm/issues/1595)

## Replies

**system** (2025-06-30):

### Meeting Summary:

Vaelyn and Micah waited for potential additional participants before discussing technical matters, including an error code link shared by Mercy. They explored challenges around including non-Ethereum data in execution API specifications and the difficulties in distinguishing between genuine L2s and other projects claiming the same status. The conversation ended with a discussion about troubleshooting issues with the spec check in the CI pipeline, where Micah suggested local testing and potential fixes while awaiting further input from Sarah.

**Click to expand detailed summary**

Vaelyn and Micah discussed the possibility of other participants joining the meeting, noting that Kalari would be absent. They agreed to wait for a few minutes before deciding whether to proceed. Mercy joined the call and shared a link about error codes, which Micah viewed. They briefly discussed the status of an issue, with Mercy mentioning that the client had not had time to review it yet.

Micah discussed the challenges of including non-Ethereum data in execution API specifications, noting it’s more of a political decision than a technical one. He highlighted the difficulty of distinguishing between genuine L2s and other projects calling themselves L2s, suggesting that someone would need to be in charge of decisions but this could lead to dissatisfaction among those not included. Mercy inquired about Tina’s involvement with the Ethereum Foundation, but Micah did not have any specific information on this matter.

Mercy and Micah discussed an issue with the spec check not running as expected in the CI pipeline. They determined that the check should run immediately after generating .io files, but it was not doing so. Micah suggested troubleshooting locally by cloning the repository and running the spec check manually, then applying a fix from PR #670. They also considered waiting for Sarah to provide more insight into the issue, as she might have a better understanding of the test setup.

### Next Steps:

- Mercy to run spec check locally on the cloned repository, apply the fix from PR #670, and test if it fails initially and then passes after the fix.
- Mercy to wait for Light Client to provide further explanation on the spec check issue.
- Micah to investigate why the spec check is running against the wrong code (checking the last committed code instead of the code being committed).
- Mercy to consult with Sarah for a better understanding of the test setup.
- Mercy to follow up with Gloria, Sina, or Felix for more information about the test setup and the spec check issue.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: Ev%00mVK)
- Download Chat (Passcode: Ev%00mVK)

