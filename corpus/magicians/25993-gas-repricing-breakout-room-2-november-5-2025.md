---
source: magicians
topic_id: 25993
title: Gas repricing Breakout Room #2, November 5, 2025
author: system
date: "2025-10-27"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/gas-repricing-breakout-room-2-november-5-2025/25993
views: 42
likes: 0
posts_count: 4
---

# Gas repricing Breakout Room #2, November 5, 2025

### Agenda

- EIP deep dives [5 min each]:

EIP-7904: General Repricing by @misilva73
- EIP-7778: Block Gas Accounting without Refunds by @nerolation
- EIP-7686: Linear EVM memory limits  by @CarlBeek
- EIP-7923: Linear, Page-Based Memory Costing by @charles-cooper
- EIP-7971: Hard Limits for Transient Storage by @misilva73
- EIP-7976: Increase Calldata Floor Cost by @nerolation
- EIP-7981: Increase access list cost by @nerolation

[15min] Wrap-up and final comments

**Meeting Time:** Wednesday, November 05, 2025 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1785)

## Replies

**system** (2025-11-05):

YouTube recording available: https://youtu.be/ZYcHlh9-X48

---

**system** (2025-11-05):

### Meeting Summary:

The meeting focused on discussing various Ethereum Improvement Proposals (EIPs) related to compute repricing, memory management, and gas pricing changes. Participants evaluated different approaches to improve efficiency and scalability, including linear and page-based memory models, as well as adjustments to gas refunds and access list pricing. The group agreed to include certain EIPs in the fork while emphasizing the need for reliable benchmarking and further discussions in the EVM Pricing Discord channel.

**Click to expand detailed summary**

The meeting focused on discussing repricing EIPs, with Maria presenting on general compute repricing. She explained the motivation behind the proposal, which aims to harmonize the costs of compute operations to improve efficiency and scalability. The discussion highlighted concerns about using outdated benchmarks and the need for more accurate worst-case scenarios. Ameziane suggested an incremental approach, starting with specific opcodes and ensuring worst-case scenarios are addressed before moving to others. The group agreed to preliminarily include the EIP in the fork while pushing for reliable data for specific values in the next few months.

The team discussed EIP-7778, which proposes a simple change to gas refund pricing to improve scalability. Maria explained that this repricing would provide a one-time boost in gas limits, while future increases would require client optimizations and hardware improvements. The group agreed that this EIP was widely supported and likely to be included in the fork. Sophia clarified that ZK EVMs would be introduced after Glamsterdam, and her team favored eliminating precompiles rather than repricing them. The conversation ended with a reminder that the next presentation would cover EIP-7686 on linear EVM memory limits.

The meeting focused on comparing two EIPs for memory management in Ethereum: EIP 7686 (linear memory model) and EIP 7923 (page-based memory model). Carl presented EIP 7686, which simplifies memory costs to a linear model instead of the current quadratic system, allowing more efficient memory allocation. Łukasz and others preferred EIP 7923 due to its flexibility and ability to separate stack and heap memory, though they acknowledged the need to adjust the page size. The discussion highlighted the trade-offs between simplicity and flexibility in memory management, with participants considering how these models would impact compiler efficiency and address space usage.

The meeting focused on discussions around EIPs related to gas pricing and memory management in the Ethereum Virtual Machine (EVM). Charles presented a proposal for page-based memory allocation to address issues with linear memory and stack versus heap separation, emphasizing the need for benchmarks to determine the feasibility of the approach. Maria introduced EIPs to adjust transient storage pricing, aiming to reduce costs and limit slot allocations to prevent potential attacks. Toni presented two EIPs: one to increase call data floor costs and another to repricing access lists, both intended to reduce worst-case block sizes. Ansgar highlighted the importance of benchmarking repricing EIPs and suggested an 80-20 approach to focus on core repricings. The group discussed the need to address state growth, with suggestions including state expiry and scaling prices with gas limits. Concerns were raised about the impact of ZK EVMs and the need to validate pricing changes across different implementations. The conversation ended with a call for further discussions in the EVM Pricing Discord channel.

### Next Steps:

- Maria and team: Finalize benchmark numbers for EIP-7904  including precompiles before setting final repricing numbers
- Maria and team: Reconsider and determine the anchor  for EIP-7904
- Sophia and team: Consider not making any precompiles cheaper in Glamsterdam
- Maria and Charles: Benchmark the parameters for EIP transient storage hard limits, specifically the max number of slots per transaction to prevent DOS attacks
- Maria and Charles: Ensure transient storage costs are consistent with other compute repricings through benchmarking
- Toni: Share analysis on EIP-7976  in the chat
- EF and Othermine team: Continue gas benchmarks collaboration to test repricing numbers against worst-case blocks
- Marcin: Complete initial benchmarking work in coming days to identify which opcodes are too slow
- All participants: Provide thoughts on how to structure tomorrow’s AllCoreDevs conversation on 40 EIPs, either in Discord or before the meeting
- All participants: Continue discussion on repricing EIPs in the Discord channel "EVM Pricing
- Research teams: Develop a clear strategy around state growth by H-star fork, including consideration of state expiry solutions
- All teams: Validate that repricing changes do not conflict with ZK-EVM requirements before finalizing

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: ch0Ld&Z$)
- Download Chat (Passcode: ch0Ld&Z$)

---

**system** (2025-11-06):

### Meeting Summary:

The meeting focused on discussing various Ethereum Improvement Proposals (EIPs) related to compute repricing, memory management, and gas pricing changes. Participants evaluated different approaches to improve efficiency and scalability, including linear and page-based memory models, as well as adjustments to gas refunds and access list pricing. The group agreed to include certain EIPs in the fork while emphasizing the need for reliable benchmarking and further discussions in the EVM Pricing Discord channel.

**Click to expand detailed summary**

The meeting focused on discussing repricing EIPs, with Maria presenting on general compute repricing. She explained the motivation behind the proposal, which aims to harmonize the costs of compute operations to improve efficiency and scalability. The discussion highlighted concerns about using outdated benchmarks and the need for more accurate worst-case scenarios. Ameziane suggested an incremental approach, starting with specific opcodes and ensuring worst-case scenarios are addressed before moving to others. The group agreed to preliminarily include the EIP in the fork while pushing for reliable data for specific values in the next few months.

The team discussed EIP-7778, which proposes a simple change to gas refund pricing to improve scalability. Maria explained that this repricing would provide a one-time boost in gas limits, while future increases would require client optimizations and hardware improvements. The group agreed that this EIP was widely supported and likely to be included in the fork. Sophia clarified that ZK EVMs would be introduced after Glamsterdam, and her team favored eliminating precompiles rather than repricing them. The conversation ended with a reminder that the next presentation would cover EIP-7686 on linear EVM memory limits.

The meeting focused on comparing two EIPs for memory management in Ethereum: EIP 7686 (linear memory model) and EIP 7923 (page-based memory model). Carl presented EIP 7686, which simplifies memory costs to a linear model instead of the current quadratic system, allowing more efficient memory allocation. Łukasz and others preferred EIP 7923 due to its flexibility and ability to separate stack and heap memory, though they acknowledged the need to adjust the page size. The discussion highlighted the trade-offs between simplicity and flexibility in memory management, with participants considering how these models would impact compiler efficiency and address space usage.

The meeting focused on discussions around EIPs related to gas pricing and memory management in the Ethereum Virtual Machine (EVM). Charles presented a proposal for page-based memory allocation to address issues with linear memory and stack versus heap separation, emphasizing the need for benchmarks to determine the feasibility of the approach. Maria introduced EIPs to adjust transient storage pricing, aiming to reduce costs and limit slot allocations to prevent potential attacks. Toni presented two EIPs: one to increase call data floor costs and another to repricing access lists, both intended to reduce worst-case block sizes. Ansgar highlighted the importance of benchmarking repricing EIPs and suggested an 80-20 approach to focus on core repricings. The group discussed the need to address state growth, with suggestions including state expiry and scaling prices with gas limits. Concerns were raised about the impact of ZK EVMs and the need to validate pricing changes across different implementations. The conversation ended with a call for further discussions in the EVM Pricing Discord channel.

### Next Steps:

- Maria and team: Finalize benchmark numbers for EIP-7904  including precompiles before setting final repricing numbers
- Maria and team: Reconsider and determine the anchor  for EIP-7904
- Sophia and team: Consider not making any precompiles cheaper in Glamsterdam
- Maria and Charles: Benchmark the parameters for EIP transient storage hard limits, specifically the max number of slots per transaction to prevent DOS attacks
- Maria and Charles: Ensure transient storage costs are consistent with other compute repricings through benchmarking
- Toni: Share analysis on EIP-7976  in the chat
- EF and Othermine team: Continue gas benchmarks collaboration to test repricing numbers against worst-case blocks
- Marcin: Complete initial benchmarking work in coming days to identify which opcodes are too slow
- All participants: Provide thoughts on how to structure tomorrow’s AllCoreDevs conversation on 40 EIPs, either in Discord or before the meeting
- All participants: Continue discussion on repricing EIPs in the Discord channel "EVM Pricing
- Research teams: Develop a clear strategy around state growth by H-star fork, including consideration of state expiry solutions
- All teams: Validate that repricing changes do not conflict with ZK-EVM requirements before finalizing

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: ch0Ld&Z$)
- Download Chat (Passcode: ch0Ld&Z$)

