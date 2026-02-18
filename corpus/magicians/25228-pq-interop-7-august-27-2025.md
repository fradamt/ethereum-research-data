---
source: magicians
topic_id: 25228
title: PQ Interop #7, August 27, 2025
author: system
date: "2025-08-24"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/pq-interop-7-august-27-2025/25228
views: 50
likes: 0
posts_count: 4
---

# PQ Interop #7, August 27, 2025

### Agenda

• Spec Finalization - Review `pq-devnet-0` spec progress and 3SF mini integration status + confirm dates for M1 and M2

• Python Implementation - Update on SSZ types and remarkalized library setup

• Project Board Review - Assign owners and priorities to GitHub project tasks

• Signature Container - Confirm variable list approach and finalize parameters

• Blockers & Dependencies - Address any new technical roadblocks for September targets

**Meeting Time:** Wednesday, August 27, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1698)

## Replies

**system** (2025-08-27):

YouTube recording available: https://youtu.be/coCfDEnAzSo

---

**system** (2025-08-27):

### Meeting Summary:

The team reviewed project specifications and discussed updates to the state transition function, including implementation details and timeline for completion by September. They addressed various technical aspects including signature verification, justification maps, and simplified validation processes, with specific focus on Devnet 0 and Devnet 1 specifications. The team also discussed infrastructure needs, task ownership, and agreed to refine the devnet spec format while confirming timelines for testing and implementation phases.

**Click to expand detailed summary**

The team discussed updates on the project board, with Gajinder reporting that 90% of the specification was complete and aiming for completion by the end of August. They reviewed the straight transition function PR, which Gajinder and June had discussed, and agreed to refine some functions and definitions. The team decided to go over the specification details during the call, with Will expressing interest in reviewing it. Gajinder mentioned he would continue working on the folk to SPR and planned to have further discussions to finalize it.

Gajinder outlined a plan for the Genesis tooling, explaining that a simple config-based approach is sufficient and eliminating the need for an E.12 generator. The team aims to have the tooling ready by September 5th, with spec tests by September 12th, and interop for devnet 0 by September 26th. Thomas agreed to check the implementation timeline for the Python code and will report back on what can be achieved. The team also discussed a deadline of September 3rd for implementing all necessary specs for net 1, with Gajinder emphasizing the importance of meeting these strict deadlines for successful interop testing.

Gajinder presented a simplified version of the state transition function, explaining key features such as chaining, round-robin proposals, and simplified validators. He noted that signature verification is done outside the main state transition function to keep it light for the prover. Gajinder also described the process of slot processing and block validation, highlighting the absence of epoch transitions and the special treatment for genesis blocks in 3SF Mini. The discussion touched on the need to determine the optimal placement of signature verification within the ZKVM for future improvements.

Gajinder explained the structure and functionality of the justification map in 3SF Mini, which tracks routes validated by validators. He described the process of processing votes, including a new condition added based on zoom experimentation to avoid processing already justified targets. Gajinder also detailed the steps involved in populating and updating the justifications map, as well as the finalization of sources, which follow similar processes to 3SF Mini. Helper functions getJustification and setJustifications were identified as still needing definition.

Gajinder confirmed that the transition function implementation is complete and ready for review, with only helper functions for get and set justification needed to be added. The team discussed that while the code was initially written in Python, Jun from the Ream team had already verified its correctness and would help with syntax testing. Gajinder also mentioned that container structure was implemented to add block header functionality, and the team agreed to complete the definite 0 spec by the end of the month, with definite 1 spec due on September 5th.

The team discussed key types for attestation and block signatures, and the exact byte sizes for signatures and public keys. Gajinder proposed using a flat byte array for signatures instead of a complex container structure, allowing for variable-sized aggregated signatures up to 4KB. Unnawut presented a PR that simplifies the signature representation to 3 keys (path, randomness, and hashes), though the actual XMSS structure is more complex. The team agreed to use a vector of bytes for signatures to simplify implementation and client handling.

The team discussed the status of Devnet 0 and Devnet 1 specifications, with Gajinder confirming that SHA-256 will be used for SSZ hashing in Devnet 0 while Poseidon implementation will be considered for later Devnets to improve proving cycles. Jun reported limited progress on Dora implementation and suggested using Forkman as a simpler alternative for Devnet 0, which Guillaume agreed was sufficient. The team confirmed that infrastructure for running Devnets is being handled by Panda Ops with the Rim team on standby, and Kamil noted that their client team plans to participate in Devnet series after completing current LIP-2 work.

The team discussed the need for a genesis generator, confirming that it’s not necessary to generate a genesis file as the required parameters can be picked from the config and generated on-the-fly by clients. Guillaume is tasked with creating a Grafana dashboard for devnet 0, pending agreement from other teams on the dashboard format. The team also reviewed ownership of tasks related to Ethereum genesis generation, state issues, and key pair generation, with Guillaume and Gajinder taking ownership of specific items. Thomas mentioned discussing the CLI tool for key generation with Benedict upon his return from holidays.

The team discussed the timeline for completing the spec and launching Devnet 0. Gajinder suggested that if the spec is finished by the end of the month, they can build test cases and check clients against it within a week. Will proposed creating a more organized devnet spec format to capture all specs, tests, and success criteria in a single index. Unnawut suggested trimming unnecessary sections from the current spec and moving relevant parts to their proper places. The team agreed to review and refine the spec format in future meetings.

### Next Steps:

- Gajinder to iterate on the state transition function PR with O and Jun.
- Toma to review the state transition function PR.
- Gajinder to work on the fork choice PR with O.
- Gajinder to verify the correctness of the state transition function code in Zoom.
- Gajinder to define the helper functions get_justification and set_justifications in the state transition function.
- Gajinder to prepare the Devnet 1 spec by September 5th.
- Thomas to implement the Python code for spec tests by September 12th.
- Guillaume to work with PK on Ethereum genesis generator for config files.
- Guillaume to coordinate with client teams on Grafana dashboard requirements.
- Kamil to connect with Guillaume regarding Docker image for Quadrivium.
- Thomas to discuss with Benedict about adding CLI for key generation to the signature repo.
- Client teams to prepare for interop by September 19th.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: zVt8W%p.)
- Download Chat (Passcode: zVt8W%p.)

---

**system** (2025-08-28):

### Meeting Summary:

The team reviewed project specifications and discussed updates to the state transition function, including implementation details and timeline for completion by September. They addressed various technical aspects including signature verification, justification maps, and simplified validation processes, with specific focus on Devnet 0 and Devnet 1 specifications. The team also discussed infrastructure needs, task ownership, and agreed to refine the devnet spec format while confirming timelines for testing and implementation phases.

**Click to expand detailed summary**

The team discussed updates on the project board, with Gajinder reporting that 90% of the specification was complete and aiming for completion by the end of August. They reviewed the straight transition function PR, which Gajinder and June had discussed, and agreed to refine some functions and definitions. The team decided to go over the specification details during the call, with Will expressing interest in reviewing it. Gajinder mentioned he would continue working on the folk to SPR and planned to have further discussions to finalize it.

Gajinder outlined a plan for the Genesis tooling, explaining that a simple config-based approach is sufficient and eliminating the need for an E.12 generator. The team aims to have the tooling ready by September 5th, with spec tests by September 12th, and interop for devnet 0 by September 26th. Thomas agreed to check the implementation timeline for the Python code and will report back on what can be achieved. The team also discussed a deadline of September 3rd for implementing all necessary specs for net 1, with Gajinder emphasizing the importance of meeting these strict deadlines for successful interop testing.

Gajinder presented a simplified version of the state transition function, explaining key features such as chaining, round-robin proposals, and simplified validators. He noted that signature verification is done outside the main state transition function to keep it light for the prover. Gajinder also described the process of slot processing and block validation, highlighting the absence of epoch transitions and the special treatment for genesis blocks in 3SF Mini. The discussion touched on the need to determine the optimal placement of signature verification within the ZKVM for future improvements.

Gajinder explained the structure and functionality of the justification map in 3SF Mini, which tracks routes validated by validators. He described the process of processing votes, including a new condition added based on zoom experimentation to avoid processing already justified targets. Gajinder also detailed the steps involved in populating and updating the justifications map, as well as the finalization of sources, which follow similar processes to 3SF Mini. Helper functions getJustification and setJustifications were identified as still needing definition.

Gajinder confirmed that the transition function implementation is complete and ready for review, with only helper functions for get and set justification needed to be added. The team discussed that while the code was initially written in Python, Jun from the Ream team had already verified its correctness and would help with syntax testing. Gajinder also mentioned that container structure was implemented to add block header functionality, and the team agreed to complete the definite 0 spec by the end of the month, with definite 1 spec due on September 5th.

The team discussed key types for attestation and block signatures, and the exact byte sizes for signatures and public keys. Gajinder proposed using a flat byte array for signatures instead of a complex container structure, allowing for variable-sized aggregated signatures up to 4KB. Unnawut presented a PR that simplifies the signature representation to 3 keys (path, randomness, and hashes), though the actual XMSS structure is more complex. The team agreed to use a vector of bytes for signatures to simplify implementation and client handling.

The team discussed the status of Devnet 0 and Devnet 1 specifications, with Gajinder confirming that SHA-256 will be used for SSZ hashing in Devnet 0 while Poseidon implementation will be considered for later Devnets to improve proving cycles. Jun reported limited progress on Dora implementation and suggested using Forkman as a simpler alternative for Devnet 0, which Guillaume agreed was sufficient. The team confirmed that infrastructure for running Devnets is being handled by Panda Ops with the Rim team on standby, and Kamil noted that their client team plans to participate in Devnet series after completing current LIP-2 work.

The team discussed the need for a genesis generator, confirming that it’s not necessary to generate a genesis file as the required parameters can be picked from the config and generated on-the-fly by clients. Guillaume is tasked with creating a Grafana dashboard for devnet 0, pending agreement from other teams on the dashboard format. The team also reviewed ownership of tasks related to Ethereum genesis generation, state issues, and key pair generation, with Guillaume and Gajinder taking ownership of specific items. Thomas mentioned discussing the CLI tool for key generation with Benedict upon his return from holidays.

The team discussed the timeline for completing the spec and launching Devnet 0. Gajinder suggested that if the spec is finished by the end of the month, they can build test cases and check clients against it within a week. Will proposed creating a more organized devnet spec format to capture all specs, tests, and success criteria in a single index. Unnawut suggested trimming unnecessary sections from the current spec and moving relevant parts to their proper places. The team agreed to review and refine the spec format in future meetings.

### Next Steps:

- Gajinder to iterate on the state transition function PR with O and Jun.
- Toma to review the state transition function PR.
- Gajinder to work on the fork choice PR with O.
- Gajinder to verify the correctness of the state transition function code in Zoom.
- Gajinder to define the helper functions get_justification and set_justifications in the state transition function.
- Gajinder to prepare the Devnet 1 spec by September 5th.
- Thomas to implement the Python code for spec tests by September 12th.
- Guillaume to work with PK on Ethereum genesis generator for config files.
- Guillaume to coordinate with client teams on Grafana dashboard requirements.
- Kamil to connect with Guillaume regarding Docker image for Quadrivium.
- Thomas to discuss with Benedict about adding CLI for key generation to the signature repo.
- Client teams to prepare for interop by September 19th.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: zVt8W%p.)
- Download Chat (Passcode: zVt8W%p.)

