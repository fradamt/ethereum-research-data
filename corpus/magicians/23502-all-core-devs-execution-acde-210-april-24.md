---
source: magicians
topic_id: 23502
title: All Core Devs - Execution (ACDE) #210, April 24
author: system
date: "2025-04-12"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-210-april-24/23502
views: 733
likes: 10
posts_count: 6
---

# All Core Devs - Execution (ACDE) #210, April 24

# All Core Devs - Execution (ACDE)

- April 24, 2025, 14:00-15:30 UTC
- Stream
- Ethereum Protocol Calls Calendar subscription

# Agenda

- Pectra

Mainnet announcement

[Fusaka](https://eips.ethereum.org/EIPS/eip-7607)

- BPO EIP-7892 config format
- EOF

Status updates
- Moving to Option D
- RISC-V concerns

SFI’ing [gas limit defaults change](https://github.com/ethereum/EIPs/pull/9678)
[RLP Execution Block Limit](https://github.com/ethereum/EIPs/pull/9658)

History Expiry updates

- Meta EIP

Sepolia activation

[Data endpoints](https://eth-clients.github.io/history-endpoints/#sepolia)

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDE
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : false #
- Already on Ethereum Calendar : false #
- Need YouTube stream links : true #
- Facilitator email: tim@ethereum.org
Note: The zoom link will be sent to the facilitator via email



[GitHub Issue](https://github.com/ethereum/pm/issues/1462)

**YouTube Stream Links:**

- Stream 1 (Apr 24, 2025): https://youtube.com/watch?v=uXgmz4oqz5w

## Replies

**abcoathup** (2025-04-19):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #210, April 24](https://ethereum-magicians.org/t/all-core-devs-execution-acde-210-april-24/23502/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> Next Steps
>
> EOF Next Steps Decision on Monday’s interop call
>
> EL teams, please share your views about the next steps for EOF based on today’s conversation on the interop call agenda: Interop Testing #34 | April 28 2025 · Issue #1499 · ethereum/pm · GitHub. We’ll make a decision on Monday about any potential scope adjustments for EOF then. If you’re not sure what I’m referring to, please make sure to watch the recording of today’s ACD.
>
> SFI’ing the Gas Limit Defaults Informational EIP
>
> On the la…

### Recordings

  [![image](https://img.youtube.com/vi/7BKH9C2afNc/maxresdefault.jpg)](https://www.youtube.com/watch?v=7BKH9C2afNc&t=133s)



      [x.com](https://x.com/EthCatHerders/status/1915405085175349328)





####

[@](https://x.com/EthCatHerders/status/1915405085175349328)



  https://x.com/EthCatHerders/status/1915405085175349328










### Writeups

- by @Christine_dkim [christinedkim.substack.com]

### Additional info

- Mainnet upgrades to Pectra May 7, Epoch 364032: Pectra Mainnet Announcement | Ethereum Foundation Blog

---

**timbeiko** (2025-04-24):

# Next Steps

1. EOF Next Steps Decision on Monday’s interop call

EL teams, please share your views about the next steps for EOF based on today’s conversation on the interop call agenda: [Interop Testing #34 | April 28 2025 · Issue #1499 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1499). We’ll make a decision on Monday about any potential scope adjustments for EOF then. If you’re not sure what I’m referring to, please make sure to watch the recording of today’s ACD.

1. SFI’ing the Gas Limit Defaults Informational EIP

On the last ACDE, we agreed to make increasing the gas limit one of the key “features” of Fusaka. To align on client defaults and keep this as a priority, we’ve drafted an EIP. It’s a bit unconventional, but not unprecedented (see EIP-7840). We plan to get it merged early next week and formally SFI it on the next ACD.

PR: https://github.com/ethereum/EIPs/pull/9678

As we find bottlenecks that prevent raising the gas limit, we should expect minor EIPs to patch them, such as: https://github.com/ethereum/EIPs/pull/9658

1. History Expiry Next Steps

It’s still unclear exactly where different teams stand with respect to dropping history in May. Let’s use `#history-expiry` to coordinate next steps.

# Call Summary

## Pectra

- Mainnet announcement is out
- PandaOps has been testing the block builder workflow, as well as using the latest client releases for feature tests. A mainnet shadow fork using the latest releases is planned for next week.

## Fusaka

### BPO Config Format

- EL teams agreed to use the format as specified in the EIP, with a minor change to the naming scheme: each BPO fork should use the name BPO1, BPO2, etc. instead of a timestamp.

### EOF

*A lot was discussed about EOF. These notes are a brief summary. Please watch the full recording for complete context.*

#### EOF updates

- devnet-1 supports all container changes as well as TXCREATE. An EEST release is out for this.

Besu and Geth are passing all tests, as well as EVMone. EELS support is expected soon.

Planning to fuzz the implementations. ETA for devnet launch is the week of May 5.

#### Contract compilation issues

- The current EOF version bans code introspection, which means existing contracts cannot trivially recompile to EOF, especially if they use assembly along with Solidity.
- This implies that many popular libraries (e.g., OpenZeppelin contracts) cannot be imported as-is in EOF contracts, requiring a rewrite (and audits) to provide the same developer experience post-EOF.
- This led some client teams to reconsider whether we should ban code introspection, or instead pursue a different variant of EOF (“Option D”) or potentially drop EOF in favor of simpler EVM changes (e.g., EIP-7907 and/or this proposal).
- Concerns were raised both about the impact on the decision-making process of removing EOF so late and about the risks of shipping EOF with code introspection and then being unable to remove that functionality later (versus reintroducing it if EOF goes live with the ban).
- Teams agreed to review the different options and make a final decision about scope on Monday’s interop call.

#### RISC-V

- Another set of EOF-related concerns came from the recent proposal to replace the EVM with RISC-V. If the ecosystem adopts EOF over the next few years, and Ethereum later moves away from it, is that work wasted?
- There was a lot of back and forth (again, see the livestream for full context). Ultimately, the uncertainty around RISC-V felt too high for this to directly affect the Fusaka EOF decision.
- Still, there was some recognition that EOF may not be the long-term execution environment. Whether that future is RISC-V or another VM, this should be part of our reasoning about whether to move forward with EOF.

### Gas Limit Default Configs

- On ACDE #209, we agreed to prioritize raising the L1 gas limit in parallel with Fusaka work. While the gas limit is ultimately set by validators, we agreed that having an EIP to coordinate client defaults would help keep this a priority and ensure all clients update their defaults by the time Fusaka goes live.
- An EIP was drafted for this purpose. We expect to merge it next week and formally SFI it on the next ACDE.
- As we continue this work, we expect to identify changes that need to be made in-protocol to support a higher gas limit. This implies adding more EIPs to Fusaka, even though the fork scope is “final.” Example: EIP-9658

## History Expiry

- Clients are expected to drop history on Sepolia in the coming weeks. Team statuses were unclear on the call, so please update the Ethereum Magicians thread accordingly.

---

**system** (2025-04-30):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=uXgmz4oqz5w

---

**system** (2025-04-30):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

Tim announces that the Petra client releases were published on the Ethereum Foundation blog, with the Mainnet fork scheduled for May 7th at 10:05 UTC. He urges those who haven’t updated their clients to do so. Barnabas reports successful testing of the MEV workflow for Petra, with recent bug fixes and improvements. Parithosh mentions ongoing client release testing, with plans for a shadow fork early the following week.

The group discusses the configuration format for the BPO (Blob Post-Cancun Upgrades) forks on the execution layer (EL). Marius suggests treating these as normal hard forks on the EL side to avoid potential bugs and complications. Alex proposes a configuration structure, which is generally well-received. The group agrees to remove timestamps from the blob schedule, as they are already present in the normal fork schedule. Tim suggests verifying client parameterization for different forks to ensure consistency across EL clients. Ahmad raises concerns about client-specific activation methods. The group decides to specify the configuration in the EIP (7892) directly, using generic names like “BPO1” and “BPO2” instead of timestamps to avoid potential issues. They plan to update the EIP with these changes.

Tim explains the concept of bundling multiple Beacon-chain Protocol Upgrades (BPOs) into a single client release, with the ability to activate them at different times. This approach reduces the operational overhead of frequent hard forks while maintaining flexibility. The consensus layer would have less frequent but more complex hard forks, while the execution layer could have more frequent but simpler upgrades. Tim also mentions the possibility of delaying or removing future BPOs if issues arise, though the term “emergency hard fork” is deemed inaccurate. The group discusses renaming the BPOs and the potential for intervention if needed.

The group discusses challenges with compiling legacy contracts to the new EOF format. Ben Adams explains that many popular libraries like OpenZeppelin would not compile due to use of deprecated opcodes. This creates a poor developer experience, as most existing contracts would break. Danno proposes revisiting “Option D”, which would re-enable certain introspection opcodes within EOF contracts while still preventing introspection of EOF contracts themselves. This could allow existing libraries to compile without major rewrites. There is debate about whether to reconsider the previously decided EOF scope, with some arguing it’s too late to change course while others feel the implications weren’t fully understood before.

The discussion focuses on the proposed changes to the Ethereum Object Format (EOF) for the upcoming Fusaka upgrade. Ahmad expresses a different perspective, suggesting that disabling certain features only for EOF contracts is not problematic as legacy contracts can still be used. Dan and Tim emphasize the importance of sticking to the frozen set of features and only making subtractive changes at this point to avoid extending timelines. Ansgar argues for a high bar to changes, noting the asymmetric risk of adding features that can’t be removed later versus the ability to add missing features in future upgrades. Gakonst stresses that the top priority for Fusaka should be scaling with PeerDAS, and any compromises to that goal would be a significant failure.

The discussion focuses on the implications of shipping EOF (EVM Object Format) without code introspection. Tim questions the value of this approach, while gakonst emphasizes that the main issue is contract compatibility and the widespread use of assembly in existing code. Alex from Epsilon reports that they have successfully rewritten parts of their codebase to work with EOF, but notes that assembly code cannot be automatically translated. Charles raises concerns about the need to maintain two different codebases for L2s without EOF and EOF-enabled mainnet. The group also discusses the potential impact on developer experience and the timeline for full ecosystem support.

The group discusses the implications of implementing EOF (EVM Object Format) and its impact on developer experience. They consider two main options: implementing EOF without introspection bans or adopting EIP-7907. Concerns are raised about potential delays in ecosystem adoption and the need to maintain separate codebases for legacy and EOF contracts. The team agrees to review the proposed changes and make a final decision by Monday, aiming to minimize delays in the testing cycle. They also briefly touch on the differences between EOF and raw EVM changes, noting that EOF contracts would fail to deploy on L2s that haven’t adopted it, while raw EVM changes might deploy but fail at runtime.

The discussion focuses on the potential adoption of RISC-V as a future execution environment for Ethereum and its implications for the current EOF (EVM Object Format) implementation. Lightclient expresses concerns about investing in EOF when RISC-V might be adopted in the future, potentially making EOF obsolete. Others argue that RISC-V is a long-term consideration (2-5 years away) and shouldn’t prevent the implementation of EOF. The group discusses the trade-offs between improving the current EVM with EOF and waiting for a potential RISC-V implementation, considering factors such as proving costs, tooling development, and maintenance burdens. They also touch on the need to support multiple versions of the EVM indefinitely, regardless of which path is chosen.

The discussion focuses on the potential switch from EVM to RISC-V or another traditional architecture. Vitalik argues that this change could bring benefits such as improved efficiency, better alignment with ZK-proofs, and attracting developers who want to use the same language on-chain and off-chain. The group debates how this potential switch affects the decision on EOF (Ethereum Object Format) and whether to proceed with EOF or wait for further research on RISC-V. They also consider the implications for future-proofing Ethereum and the need to reevaluate short-term benefits of EOF in light of a possible different end-game for Ethereum.

The group discusses the potential impact of RISC-V on the decision to implement EOF (EVM Object Format) in the upcoming Fusaka upgrade. They consider two main options: making a decision about EOF on Monday based on current information, or delaying the decision for 4 weeks to conduct a “research sprint” on RISC-V. The consensus is that 4 weeks is likely not enough time to gain significant insights, and that EOF should be evaluated on its own merits. Tim suggests making a final decision about EOF’s scope in Fusaka during Monday’s testing call, considering the uncertainty of future execution environment changes but not over-indexing on RISC-V specifically. The group acknowledges that if EOF is not included in Fusaka, it may not be implemented for several years.

The meeting discusses prioritizing an increase in the gas limit for the upcoming Fusaka upgrade. Tim proposes merging an EIP that would set a new default gas limit, serving as a reminder to focus on this work. The group generally supports this approach, seeing value in coordinating efforts to safely scale the gas limit. Ben Adams notes that many nodes have not updated to higher limits, so having clients commit to new defaults is important. A related proposal to add a cap on block size at the RLP level is also discussed, which could allow for higher gas limits. The meeting concludes with updates on history expiry, with Piper noting that Sepolia activation is set for May 1st and urging client teams to document any changes in their behavior.

### Next Steps:

- Client teams to review and make a decision on EOF options by Monday’s testing call.
- Dan or Ben to write up a quick summary of the different EOF options and provide links to specs for people to review before Monday’s call.
- Tim to merge the gas limit EIP in the next week or so.
- Client teams to review the proposal for adding a cap to the block size at the RLP level.
- EL client teams to publish documentation on any changes to their client behavior due to history expiry and send links to Piper.
- Client teams to follow up on history expiry implementation in the Discord history expiry channel.
- All participants to review the gas limit EIPs in the next few days.

### Recording Access:

- Join Recording Session (Passcode: YU@d1^F6)
- Download Transcript
- Download Chat

---

**system** (2025-05-10):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=uXgmz4oqz5w

