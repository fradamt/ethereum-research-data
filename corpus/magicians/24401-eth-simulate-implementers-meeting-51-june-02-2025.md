---
source: magicians
topic_id: 24401
title: Eth_simulate Implementers' | Meeting # 51 | June 02, 2025
author: system
date: "2025-06-02"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eth-simulate-implementers-meeting-51-june-02-2025/24401
views: 59
likes: 0
posts_count: 2
---

# Eth_simulate Implementers' | Meeting # 51 | June 02, 2025

# eth_simulate Implementers’ Meeting # 51, June 02, 2025

- Date and time in UTC in format June 02, 2025, 12:00 UTC

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
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : false
- display zoom link in invite : true

[GitHub Issue](https://github.com/ethereum/pm/issues/1563)

## Replies

**system** (2025-06-02):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

The team discussed merging changes and testing results. Sina mentioned having some eye infections but confirmed they could proceed with the meeting. They agreed to use Sina’s test suite for now and try to merge it with the main repository later. Killari expressed uncertainty about some differences between versions and asked for updates from Nether, but Sina said they hadn’t heard back recently.

The team discussed issues with test messages and transaction costs, noting that some messages were being incorrectly flagged as errors despite successful processing. They identified changes in block structure and state routes, which Sina attributed to differences in the Hive viewer version. Killari suggested that the team might be using an older version of the Geth client, which could explain some of the observed discrepancies.

Sina and Killari discussed the concept of difficulty in the context of blockchain technology, particularly in relation to proof of work and proof of stake. They noted that the difficulty should remain constant and agreed that total difficulty should be removed from the API spec. Sina mentioned that a PR had been merged to remove total difficulty from responses, and they identified that Geth was not returning withdrawals and parent beacon block route, which Sina agreed to investigate further. Killari suggested that the issue might be related to running a test against the wrong version or a recent fork.

Sina and Killari discussed discrepancies in test results, particularly focusing on state routes and hash differences. They identified that the issue might be related to chain configuration and historical block hashes, which could be due to the implementation of EIP-2935. Micah suggested reaching out to Lucas to check on the progress of related work. The team agreed to investigate the problem further, particularly focusing on empty requests and state route changes, and to potentially provide a list of issues to be fixed.

Sina and Killari discussed discrepancies in their analysis of a petrol block and transaction data. They identified several differences in gas usage, transaction hashes, and trace data between their results. Sina suggested that some of these discrepancies could be due to errors in their analysis or in the data provided. They agreed to continue refining their approach and running tests again to iron out these differences.

The team discussed issues with gasless transactions and empty contract creation calls, noting that some test cases were returning unexpected results. They identified that transaction hashes and error codes were different between implementations, and discussed a bizarre test case involving an empty call with no data. The conversation concluded with a discussion about debugging approaches, where Nethermind’s team would fix issues one by one and report back when encountering problems they believed were due to incorrect code.

Sina and Killari discussed the state override issue and the need to verify test cases before merging them into the test suite. Sina planned to run tests against Ruth and Bisu, and they agreed it was important to ensure the test cases were correct before merging. Micah was considering reaching out, but the transcript ended before his decision was shared.

Micah and Sina discussed exporting and sharing a page with findings, aiming to make it easier for Lucas to review. Sina agreed to move the page to a more accessible format and include notes taken during the review process. They also touched on the importance of providing clear documentation to encourage timely completion of tasks.

### Next Steps:

- Sina to investigate why Geth is not returning withdrawals and withdrawal route in some test cases.
- Sina to look into the discrepancy in gas usage between Nethermind and Geth in certain test cases.
- Sina to investigate the state override issue causing errors in transaction processing.
- Sina to run the test suite against Besu and Erigon and compare results.
- Sina to prepare a detailed list of findings and discrepancies between Nethermind and Geth for review.
- Micah to reach out to Lucas regarding the status of Nethermind’s progress on addressing the identified issues.
- Sina to export the test results page and share it with Micah for forwarding to Lucas.
- Sina to compile and share notes on the findings from the meeting with Micah to send to Lucas.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: M8=xP2K+)
- Download Chat (Passcode: M8=xP2K+)

