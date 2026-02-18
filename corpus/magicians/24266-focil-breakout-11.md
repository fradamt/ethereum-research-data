---
source: magicians
topic_id: 24266
title: FOCIL Breakout #11
author: system
date: "2025-05-19"
category: Protocol Calls & happenings
tags: [breakout, focil]
url: https://ethereum-magicians.org/t/focil-breakout-11/24266
views: 147
likes: 0
posts_count: 3
---

# FOCIL Breakout #11

# FOCIL Breakout #11, May 20, 2025, 14:00 UTC

[Zoom Link](https://us02web.zoom.us/j/84332720478?pwd=xtSJe8qQACMD8m8UaPWNahzM8gmaKx.1)

# Agenda

- Berlin interop, research news and progress
- Implementation updates

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : (e.g Breakout room)
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true #
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1551)

## Replies

**system** (2025-05-21):

YouTube recording available: https://youtu.be/wwlsrljZr84

---

**system** (2025-05-21):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

Thomas provided updates on the upcoming Fossil session during the Berlin IETF in June, including confirmed speakers and topics. He mentioned progress on the interaction between fossil delayed execution and block access lists, which simplifies static validation of blocks. Thomas also highlighted the local node favoring delta to the scaling roadmap and encouraged participants to engage in discussions on the future of fossil and its interaction with EIPs. Kubi then presented on relay inclusion lists, thanking everyone for their feedback and encouraging further discussion on the EIP research page.

Kubi presented the goals and design of relay inclusion lists, emphasizing their immediate impact on censorship resistance without introducing new protocol complexities or trust assumptions. The design aims to prepare the block production pipeline for future in-protocol inclusion, ensuring sustainability by preserving relay competitiveness and block value. Kubi outlined the three-step process: setup, inclusion list creation, and validation, highlighting the importance of deterministic inclusion rules and API endpoints for builders.

Kubi presented two options for calculating inclusion scores: a multiplicative approach (option 1) and a normalized additive approach (option 2). Option 1 multiplies waiting time and priority fee, while option 2 adds them after normalization. Both methods compare transactions and adjust scores based on total gas paid or transaction byte size. Kubi noted that option 1 is leaner and more elegant, but both approaches are appropriate. The team aims to finalize the decision with stakeholders. Kubi also discussed the importance of sizing the inclusion list to avoid negatively impacting block value, which decreases with increased latency.

Kubi presented on relay inclusion lists, explaining how they provide an advantage over proposal-driven inclusion lists by not being constrained by proposal bandwidth, allowing for larger sizes as relay adoption increases. He outlined future directions including multi-relay inclusion lists for improved censorship resistance and reduced redundancy, as well as blob type transactions and larger relay inclusion lists. The discussion addressed concerns about potential centralization risks and interaction with proposal build item separation, with Kubi clarifying that the design is built to fit the current PBS supply chain. The group also discussed transaction size considerations and the potential deprecation of relay inclusion lists once included in the protocol.

The team discussed progress on implementation and testing of clients. Jacob reported on PRs for execution specs and test fixtures, emphasizing the need to merge the IP-related PR soon. Jihoon shared updates on consensus specs and tests, aiming for the next release in two weeks. The group also addressed a discrepancy between the overview picture and text in the EIP, which Jochem Brouwer pointed out. Mercy mentioned working on the frontend of a transaction visualizer. The team agreed to follow up with the Lighthouse client team separately.

### Next Steps:

- Marc to review and address comments on the fossil EIP PR in the next day or two.
- Jacob to rebase the execution specs PR on top of the latest Osaka fork.
- Jacob to open a PR for execution spec tests in the next few days.
- Jihoon to complete the consensus specs and add more test cases for fossil.
- Jihoon and Justin to aim to include fossil updates in the next consensus spec release in 2 weeks.
- Thomas to review and align the overview picture with the text in the fossil EIP.
- Mercy to continue working on populating the front-end of the transaction visualizer.
- Thomas to follow up with the Lighthouse team regarding their fossil implementation progress.

### Recording Access:

- Join Recording Session
- Download Transcript
- Download Chat

