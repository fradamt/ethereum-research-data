---
source: magicians
topic_id: 23496
title: RollCall #12 May 21
author: system
date: "2025-04-11"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/rollcall-12-may-21/23496
views: 314
likes: 1
posts_count: 3
---

# RollCall #12 May 21

# RollCall #12 May 21, 2025

- May 21, 2025, 14:00 UTC

# Agenda

- Future of shared execution for L2s
- Geth refactoring for L2s

Facilitator email: [nicolas@ethereum.org](mailto:nicolas@ethereum.org)

edit test

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : RollCall
- Occurrence rate : monthly
- Already a Zoom meeting ID : false # Set to true if this meeting is already on the auto recording Ethereum zoom (will not create a zoom ID if true)
- Already on Ethereum Calendar : True #
- Need YouTube stream links : true # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false #

[GitHub Issue](https://github.com/ethereum/pm/issues/1461)

## Replies

**system** (2025-05-21):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

The meeting began with a discussion about streaming capabilities and the need to reorient the L1’s approach to EVM and execution. Ansgar explained that plans are consolidating throughout June, with implications for the rollcall effort to be discussed in August. The group agreed to start streaming, and Carl welcomed everyone to roll call number 12, introducing the first topic of the day, which was previously discussed in previous meetings and raised on multiple occasions.

The team discussed implementing a limit on the number of blobs per transaction, with Carl noting that while 7 was under consideration, 3 blobs per transaction should not be an issue for now. Ansgar presented updates on Ethereum L1 developments, including the shipping of the pack chart and support for EIP-7702, which allows UAs to act as smart accounts. He emphasized that L2s should have a strategy in place for supporting this feature, and mentioned that the scope of Fusaka has changed, with the UF being removed and PRs remaining as the main feature. The team also discussed upcoming research calls and potential changes to the Ethereum roadmap, with Ansgar highlighting the importance of considering these developments for L2s.

Ansgar presented a framework for addressing scaling bottlenecks in L2 networks, outlining three approaches: improving engineering, containing bottlenecks without blocking scaling, and protocol changes. He explained that L2s primarily rely on engineering improvements, while containing involves techniques like capping activities or implementing dynamic pricing, which L1s cannot easily do due to their permissionless nature. Ansgar emphasized the need for better tooling to address L2-specific bottlenecks and mentioned ongoing efforts to make pricing more flexible and customizable across L1 and L2 networks.

The meeting focused on scaling considerations for Ethereum nodes, particularly the distinction between prover nodes and executor nodes. Ansgar explained that while the L1 is becoming more dynamic in its execution layer, the hardware requirements for full nodes have been formalized in Meta EIP-7870, which sets minimum specifications for RAM, CPU, disk, and network bandwidth. Tsahi raised concerns about the L1’s focus on prover nodes, noting that executor nodes that handle RPC calls and Eth calls are equally important for scaling, and suggested a need for better collaboration between L1 and L2 teams on these issues. The group agreed that while formal collaboration might be premature, there would be value in future discussions between L1 and L2 teams regarding scaling strategies.

### Next Steps:

- Ethereum L1 team to finalize the exact limit on the number of blobs per transaction for the upcoming upgrade.
- L2 teams to develop strategies for supporting EIP-7202 (account abstraction) on their networks.
- L2 teams to review and adjust their strategies regarding EUF (Ethereum User Fee) in light of its removal from the Ethereum L1 Cancun upgrade scope.
- Ethereum L1 team to continue work on improving scaling loops, including identify, improve, contain, and change strategies.
- Off-chain Labs and Ethereum L1 team to collaborate on developing more dynamic pricing mechanisms for L2s and L1.
- Ethereum research team to organize a dedicated forum or breakout session to discuss scaling strategies between L1 and L2 teams.
- Ethereum L1 team to further develop strategies for addressing the needs of RPC nodes and execution-only nodes in future scaling efforts.

### Recording Access:

- Join Recording Session (Passcode: Z$4ZBi!?)
- Download Transcript
- Download Chat

---

**system** (2025-05-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=rLpvd0c0y1E

