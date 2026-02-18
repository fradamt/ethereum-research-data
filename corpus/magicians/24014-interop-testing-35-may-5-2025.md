---
source: magicians
topic_id: 24014
title: Interop Testing #35 | May 5 2025
author: system
date: "2025-05-02"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/interop-testing-35-may-5-2025/24014
views: 188
likes: 0
posts_count: 3
---

# Interop Testing #35 | May 5 2025

# Interop Testing #35 | May 5 2025

- May 5th, 2025, 14:00 UTC

# Agenda

- Updates on Pectra testing and last minute readiness check
- Discussions of communication channels for Pectra
- PeerDAS testing

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : interop testing
- Occurrence rate : weekly
- Already a Zoom meeting ID : false # Set to true if this meeting is already on the auto recording Ethereum zoom (will not create a zoom ID if true)
- Already on Ethereum Calendar : true # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- Need YouTube stream links : true # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1520)

## Replies

**system** (2025-05-05):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=YvlLhvICtbc

---

**system** (2025-05-06):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

Parithosh led a meeting to discuss the final preparations for the upcoming Petra release. The client teams have completed their bug fix releases, and the blog posts have been updated to reflect this. The Panda Ops team has run the bug fix releases through asserta and updated all nodes, including boot nodes, testnet nodes, and validators. Parithosh mentioned a potential issue with flashbots, which they have communicated to the relevant team. The team will continue to monitor the situation and ensure everything is functioning correctly.

Parithosh and Mario discussed the status of the Pectra testing. Mario reported that there were a few Hive tests not passing, but these were deemed as nice to have passing as they were based on scenarios that were not technically possible. They planned to share a document with the teams to double check with them. Mario also mentioned that he did a manual review of all the client teams and everything seemed fine. Parithosh mentioned that the Gnosis chain guys went through Pectra last week and it was successful. They also discussed the latest East release, which contains all the Ethereum tests. Mario mentioned that they plan to migrate everything from Ethereum tests into execution spec tests. They also discussed the Gnosis drop in participation and the update to 7, 7, 0, 2.

Parithosh discussed the communication channels for Petra, including a primary channel to be created before the fork and archived afterward. He emphasized the importance of keeping discussions in the Ether and D Discord and moving them from other platforms. Parithosh also mentioned a checklist on the Panda Ops blog for those interested in monitoring the fork. He asked primary and backup team members to be available and monitor the Ether R&D Discord channel during the upgrade. Łukasz suggested setting up a live monitoring session and sharing the details beforehand. Parithosh then moved on to discuss Pidas, inviting Barnabas to provide an update.

Barnabas discussed the launch of the net 7, which will require changes in the step by route and sales. The Devnet 6 spec will be shut down and replaced by Devnet 7. Parithosh suggested that client teams should prepare their images as soon as possible. The team also discussed the implementation of BPI and the possibility of canceling the previous testing calls. Parithosh mentioned that the only active workstream is gas limit testing, and they plan to increase the gas limits on testnets after the Petra shipment on Mainnet. The team also discussed the history expiry, but lacked documentation on what needs to happen.

In the meeting, the team discussed the status of history expiry, a feature that allows nodes to drop their history and preserve it via era files. They noted that while the feature is supported, it has not been shipped yet and there is a lack of documentation on how to use it. The team also discussed the need for a new deadline for history expiry, as the previous one had been postponed. They agreed to discuss this further in the history expiry channel. The team also mentioned the upcoming release of Petra and the need for more testing before merging changes. They ended the conversation by agreeing to invite Piper to future calls to discuss the coordination of his work.

### Next Steps:

- Mario to share the link of the manual review of client repositories with the team.
- Mario and East team to add an East test for the 7702 wording update.
- Parithosh to create a Petra upgrade channel in the Eth R&D Discord before the fork.
- Primary and backup persons for each client team to be available and monitor the Eth R&D Discord channel during the Petra upgrade.
- Parithosh to set up and share a voice channel for the Petra upgrade.
- Client teams to prepare their images for Devnet 7 as soon as possible.
- Parithosh to discuss merging the Prdos testing call with this call in next week’s Prdos testing call.
- Kamil to update Nethermind release notes and documentation with clearer information on history expiry and how to drop history.
- Client teams to continue work on history expiry implementation and provide documentation on how to use it.
- Parithosh to initiate a discussion in the history expiry channel about a new plan and timeline for history expiry implementation across clients.
- Parithosh to consider inviting Piper to future calls for coordinating history expiry efforts.

### Recording Access:

- Join Recording Session (Passcode: @!sHDcR0)
- Download Transcript
- Download Chat

