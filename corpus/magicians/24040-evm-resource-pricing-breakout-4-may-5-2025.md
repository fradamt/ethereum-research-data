---
source: magicians
topic_id: 24040
title: EVM Resource Pricing Breakout #4, May 5, 2025
author: system
date: "2025-05-04"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/evm-resource-pricing-breakout-4-may-5-2025/24040
views: 106
likes: 0
posts_count: 4
---

# EVM Resource Pricing Breakout #4, May 5, 2025

# EVM Resource Pricing Breakout #4, May 5, 2025

- May 5, 2025, 16:00 UTC

# Agenda

- Memory costs @shemnon
- EL Roadmap @adietrichs
- TBD
- Discussion

Other comments and resources

The zoom link will be sent to the facilitator (please fill in the email and telegram)

Facilitator email: [davide.crapis@ethereum.org](mailto:davide.crapis@ethereum.org)

 **🤖 config**

- Duration in minutes : 60
- Already a Zoom meeting ID : false # Set to true if this meeting is already on the auto recording Ethereum zoom (will not create a zoom ID if true)
- Already on Ethereum Calendar : false # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- display zoom link in invite : true # Set to true to add the Zoom link to the Google Calendar invite description



[GitHub Issue](https://github.com/ethereum/pm/issues/1504)

## Replies

**poojaranjan** (2025-05-06):

[![image](https://img.youtube.com/vi/aaDFcQKcpAY/maxresdefault.jpg)](https://www.youtube.com/watch?v=aaDFcQKcpAY)

---

**system** (2025-05-06):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

Davide initiated the meeting, proposing to start with Ansgar’s thoughts on the El Roadmap, particularly focusing on Amsterdam. Ansgar briefly discussed the upcoming research call, which he suggested would be interesting for the attendees. Davide also mentioned that Yasuck might have a small update on repricing and there would be a discussion on Dunkrat’s exponential gas limit increase proposal. The meeting was more focused on discussion rather than presentation.

Ansgar discussed the upcoming GLUMS fork and its impact on execution throughput scaling. He highlighted the need for performance engineering and the importance of understanding current bottlenecks to make necessary changes. Ansgar emphasized the role of repricing in short-term containment of bottlenecks and its potential to unblock scaling efforts. He also mentioned the mismatch between the lead time for pricing changes and performance devnets, and the need to understand bottlenecks early in the process.

Ansgar and Davide discussed the potential for more dynamic repricing to help with performance bottlenecks. Storm suggested that the REST team is working on RPC methods that could provide data on the impact of different price schedules. Ansgar proposed the idea of a standard config for gas costs that could be changed more frequently. Storm mentioned that tracing every individual opcode could be expensive, but a non-obvious distribution of opcodes could be revealing. Davide suggested pushing the conversation forward on this topic and discussed the possibility of prioritizing specific opcodes for repricing.

Jacek presented a proposal to simplify and reduce the cost of gas for most simple opcodes, while increasing the cost for more complex ones. The proposal also aims to make memory cost formulas simpler and cheaper for warm addresses. The proposal’s implementation might be challenging for client teams. Jacek also discussed the impact of the proposal on network security and the need to consider the worst-case scenario for clients like Geth and Etagon. The team is conducting further analysis on the proposal’s effects and is considering different approaches to gas cost calculation.

Jacek discussed the potential impact of underpricing due to varying gas costs across different clients. He mentioned that the slowest and worst-case scenarios for easy padding could be around 40 million gas per second, while fast clients could reach up to 100 million gas per second. Ansgar suggested rounding up gas prices to avoid underpricing, and Jacek agreed to prepare a comparison to discuss further. Carl also suggested a rounding threshold of 1.3 or 1.2. The team agreed to create a table showing MGas/s for each opcode per client under the current pricing regime.

Ansgar and Jacek discussed the challenges of dealing with different client behaviors, particularly in relation to network security and efficiency. Jacek suggested three options: pricing based on the worst-case scenario, the best-case scenario, or an average approach. He emphasized the need to balance network stability with the potential for improvement in implementations. Ansgar agreed with Jacek’s worst-case scenario approach for easy padding, but also highlighted the need for a general strategy to handle similar issues in other areas of client performance. Jacek proposed using a medium approach overall, but noted that easy padding required closer examination. The team agreed to continue discussing this topic in future meetings.

Jacek and Ansgar discussed the need for proactive measures to address performance issues in clients. They agreed that publishing data on client performance could create a feedback loop for improvement. However, they also expressed concerns about direct client comparison, preferring to avoid unnecessary conflicts. Ansgar suggested that transparency is valuable in this context. The team also discussed the potential for generalizing this approach to other areas, such as sync performance.

Ansgar proposed discussing the details of upcoming events in future meetings. Jacek agreed to finish the pricing analysis, including a ‘what if’ scenario, M. Gas analysis, and client comparisons. Sophia suggested separating the opcode pricing into one EP for the OP codes and one for the precompiles, as it may be non-controversial and unlikely to change in the future. Davide and Jacek discussed the possibility of splitting the changes into smaller categories for easier consumption, but Jacek pointed out that this could lead to inconsistencies if not all changes are implemented.

Davide, Jacek, Ansgar, and Sophia discussed the potential for splitting and remerging changes in their methodology. Ansgar suggested normalizing pricing changes and building infrastructure to make frequent changes trivial. Sophia disagreed, stating that most changes are unlikely to be made in the future and that monotonic changes are preferable. The team also discussed the potential for changes in precompiles and hash functions, with Sophia suggesting that these might be cheaper to traditionally compute and more expensive to prove. The conversation ended with Ansgar expressing disagreement with Sophia’s stance on monotonic changes.

In the meeting, Ansgar and Sophia discussed the need for more explicit guidance on changes to the system, particularly regarding precompiles and gas costs. They agreed that while innovation is important, it should not come at the cost of predictability. Ansgar suggested that developers should be aware of potential changes in costs and not overly rely on specific prices. The team also discussed the importance of making compute more efficient to allow for gas increases without being held back by specific categories. They concluded that they should prepare for a world where they would want to reprice certain categories every hard fork, and build infrastructure to support this seamlessly. The conversation ended with a few topics to follow up on in the next call.

### Next Steps:

- Jacek to finish the “what if” scenario showing how the repricing changes would affect typical transactions.
- Jacek to add M Gas analysis to the repricing proposal.
- Jacek to consider adding client comparisons for each opcode and precompile to the repricing proposal.
- Storm to prepare a table of M Gas per second for each opcode across different clients.
- EL client teams to consider creating a standard config for gas costs to make future pricing changes easier.
- Ansgar to follow up on the discussion about normalizing frequent pricing changes and building infrastructure to support it.
- Jacek to consider the suggestion of splitting the repricing proposal into separate EIPs for opcodes and precompiles.
- All participants to prepare for further discussion on the repricing approach and its implications for Amsterdam hard fork at the next call.

### Recording Access:

- Join Recording Session (Passcode: U%=HtH=5)
- Download Transcript
- Download Chat

---

**system** (2025-05-06):

YouTube recording available: https://youtu.be/-3Nkrd4olgk

