---
source: magicians
topic_id: 23529
title: EVMMAX Implementers Call 5 | April 24, 2025
author: system
date: "2025-04-14"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/evmmax-implementers-call-5-april-24-2025/23529
views: 76
likes: 2
posts_count: 2
---

# EVMMAX Implementers Call 5 | April 24, 2025

# EVMMAX Implementers Call 5 | April 24, 2025

- Date and time in UTC in format April 24, 2025, 12:00 UTC
- Duration in minutes : 90 mins
- Occurrence rate : monthly
- Other optional resources

EVMMAX Implementers Call Playlist
- EVMMAX Breakout - Devcon SEA L1 R&D Workshop
- Poqeth: Efficient, post-quantum signature verification on Ethereum

# Agenda

- Client Updates
- Open Questions

Other comments and resources

## Next call is on May 22, 2025

[GitHub Issue](https://github.com/ethereum/pm/issues/1469)

## Replies

**nicocsgy** (2025-04-24):

## Meeting summary for EVMMAX Implementers Call 5 April 24, 2025 (04/24/2025)

### Quick recap

The meeting focused on discussing the potential impact and implementation of EVM Max, including its inclusion in upcoming forks and its role in scaling solutions. Participants shared updates on benchmarks, cryptographic primitives, and progress on implementations, while also emphasizing the need for more research, feedback from L2s and other projects, and concrete use cases to justify EVM Max’s inclusion. The team agreed on the importance of finalizing the EIP, reviewing gas numbers, and presenting the project to potential users for valuable feedback before moving forward.

### Next steps

• Radek to create a PR to the EIP to add inversion and remove Montgomery modulus for small bit sizes.

• Epsilon team to determine how to declare EVM Max context on top of the EOF container for validating immediate argument values at deploy time.

• Team to review gas numbers for EVM Max operations.

• Team to prepare presentation of EIP for L2s and other projects to get feedback.

• Team to identify which L2s are already using Poseidon and prepare to present EVM Max to them.

• Kevaundray to lead discussion in next call about which L2s to present EVM Max to and who specifically to approach.

**Summary**

**Evm Max Roadmap and Risk 5 Proposal**

Danno and Kevaundray discussed the potential impact of the risk 5 proposal on Evm Max. Danno expressed concerns about the lack of groundwork and the need for more research before making any changes. They also discussed the possibility of Evmx not being included in Glamsterdam and the need for a clear roadmap for future developments. Kevaundray suggested reaching out to the L twos to understand their needs and potential use of the new proposals. Danno agreed, emphasizing the importance of having a clear story for the roadmap.

**Gas Scaling and Blob Scaling Discussion**

In the meeting, Danno and Kevaundray discussed the focus on gas scaling and blob scaling, with Radek suggesting that the EVM Max could still be made in Lamsterdam if the spec is closed as soon as possible and all tools are reached for opinions. Kevaundray agreed with Radek’s points. The meeting then transitioned to updates from client devs, with Radek sharing benchmarks for different cryptographic primitives, including Falcon signature primitive. Radek also mentioned that the numbers looked very good compared to what was implemented in the legacy VM.

**EVM1 Speedup and Gas Reduction**

Rodiazet discussed the implementation of a primitive for small fields, utilizing SIMD instructions and a library. He also mentioned changes to the spec regarding gas models for smaller fields and values, and the addition of assumptions about the Montgomery representation. Kevaundray asked about the implementation of the inversion function in EVM1 and the speedup achieved for the FFT function. Rodiazet confirmed the implementation and a 200x speedup. Marc questioned the gas reduction for the Poseidon hash, to which Rodiazet clarified that it was a comparison of different versions of EVM Max.

**Ethereum JS Progress and Gas Functions**

Kevaundray led the meeting, discussing updates and potential improvements. Rodiazet shared insights on the cost of Poseidon in solidity, noting a significant reduction. Scorbajio reported progress on Ethereum JS’s implementation, including the completion of opcode tests. He also raised questions about gas functions, which Kevaundray confirmed were still tentative. The team discussed the need for further testing and validation. No new items were introduced, and no open questions were raised.

**EVMX’s Role in Fork Scaling**

Danno discussed the challenges of scaling l1 and the need for specific use cases to justify the inclusion of EVMX in the next fork. He emphasized the importance of having a concrete use case, such as efficient Poseidon hashing, to justify the need for EVMX. Danno also suggested that EVMX could be positioned as a solution before any precompiles, as it could help avoid issues with the choice of library. The team agreed that meaningful feedback from L2s would be crucial in determining the next steps for EVMX.

**Evmx Scaling and Precompiles Discussion**

Danno discussed the need for Evmx to fit into the scaling story and the importance of having a spec and sample contracts written down. Kevaundray raised questions about the precompiles and the need for more valuable feedback from tools. Rodiazet agreed that while some use cases are known, more feedback is needed. The team also discussed the need for more players to support the project and the importance of having established parties like L twos and Zk rollups to say that Evmx helps them scale. Danno emphasized that a compelling argument, such as a decrease in cost for contracts by 5x, would be needed to get Evmx into Glanster.

**Project Progress and EIP Discussion**

Kevaundray led a discussion on the progress of a project, focusing on the addition of a special case for small bit sizes and the creation of a proof of concept (PoC) to the EIP. Rodiazet mentioned the need to declare EVM Max context for validation and deployment. The team discussed the potential use of the project in other areas, with Rodiazet suggesting it could be beneficial for various projects. Kevaundray proposed presenting the project to L Twos and other projects for feedback. The next steps include finalizing the EIP and reviewing gas numbers for operations.

AI-generated content may be inaccurate or misleading. Always check for accuracy.

