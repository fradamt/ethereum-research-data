---
source: magicians
topic_id: 25323
title: PQ Interop #8, September 3, 2025
author: system
date: "2025-09-02"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/pq-interop-8-september-3-2025/25323
views: 71
likes: 5
posts_count: 7
---

# PQ Interop #8, September 3, 2025

### Agenda

- Devnet-0 spec update
- Devnet-1 spec update
- Walk through of multiSign spec by Thomas

**Meeting Time:** Wednesday, September 03, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1712)

## Replies

**system** (2025-09-03):

### Meeting Summary:

The team reviewed progress on Devnet 0 development, including code review needs and metrics integration requirements. Thomas presented detailed explanations of various technical implementations including Python specifications, finite field operations, and XMSS code interface, while the team discussed signature verification and key management approaches. The conversation ended with a review of network performance simulation results and discussions about handling proposals and attestation processes.

**Click to expand detailed summary**

The team discussed progress on the development of Devnet 0. They discussed the need for the remaining code to be reviewed and reviewed by the team. Guillaume provided updates on the metrics integration and the need for the Korthosis configuration to be ready for the testnet. The team agreed on the importance of aligning the metrics across clients after the fork choice specs are merged. Thomas and Gajinder confirmed that the multi-sig spec is ready for translation into the clients, and Mercy raised concerns about the use of a specific tool for the testnet, which Thomas will discuss with Benedict upon his return.

Thomas presented an overview of the Python specification file migration, explaining the structure of the spec repo and its organization into folders for different components like types, chains, containers, and networking. He described how the code is designed with typed structures and basic devnet config constants, with each file containing specific classes like blocks and other elements. Thomas emphasized that the code is simple and can be modified as needed, with documentation provided in Markdown files.

Thomas explained the implementation of finite field operations using the Collaber prime field, including basic operations like addition, subtraction, and multiplication. He demonstrated how the finite field is defined and tested, highlighting the simplicity of the current implementation compared to optimized versions like Poseidon. Thomas also described the structure of the Poseidon function, emphasizing the decoupling of the permutation step and the permutation of the function’s layers.

Thomas explained the XMSS code interface, emphasizing that clients should use the provided code rather than developing their own implementation for security reasons. He outlined the key functions: key generation, signing, and verification, detailing the parameters and procedures involved. Thomas clarified the concepts of activation epoch and active epochs, explaining how they relate to the key. Giacomo asked about the question about domain separation, which Thomas did not directly answer.

Thomas presented an overview of his work on signature verification, including the verification function and signature verification, and discussed the parameters and next steps for signature schemes. He agreed with the team to use a test configuration with smaller parameters for testing, as the current production configuration was too slow. Thomas mentioned he would implement the state transition function and present more details during the lean consensus call on Friday. The team discussed signature and public key sizes, with Gajinder requesting these values be included in the constants file for clarity. Thomas agreed to add these calculations. Ladislaus inquired about the relationship between activation time and key lifetime, and Thomas explained that for devnets, they would use a shorter activation time to reduce key generation time. Justin suggested using a maximum lifetime of 2^32 for consistency across all networks, avoiding key rotation complications.

Justin discussed solutions for handling proposals and attestation processes, suggesting two approaches: including attestation implicitly in proposals or splitting keys into proposer and attester groups. He clarified that proposals can include votes implicitly in blocks, but this vote won’t be aggregated with others due to a different message signature. Gajinder raised concerns about the applicability of these solutions to other key types, such as signing and slashing messages, and questioned the role of whistleblowers in rewards. Justin explained that whistleblowing rewards do not require signatures and clarified that proposals and attestations are the only two areas requiring signatures in the current system.

Kamil presented findings on the simulation of network performance. The results of the simulation were consistent with the network’s performance. The simulation results were discussed in the meeting. The simulation results were discussed in the meeting.

### Next Steps:

- Gajinder and Jun to finalize and clean up the specs for the transition functions for Devnet 0.
- unnawut and Reem team to integrate the finalized specs into their codebase within 3-5 days after the specs are merged.
- Guillaume to work with PQ on the kurtosis configuration for Devnet 0 testing.
- Guillaume to implement the Grafana setup for metrics visualization.
- unnawut and Guillaume to define specific metrics for consensus and fork choice measurements after the remaining specs are merged.
- Thomas to discuss with Benedict about merging Mercy’s PR related to hash sync.
- Thomas to add signature size and public key size constants to the XMSS implementation for clarity.
- Thomas to implement the state transition function and other 3SF components in the spec.
- Thomas to provide a more extensive presentation of the XMSS implementation during the Lean Consensus call on Friday.
- Kamil to share PQ aggregation simulation results with networking team members  for the Cambridge workshop.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: $0wq*zse)
- Download Chat (Passcode: $0wq*zse)

---

**system** (2025-09-03):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=RJB3IHo1H84

---

**system** (2025-09-04):

### Meeting Summary:

The team reviewed progress on Devnet 0 development, including code review needs and metrics integration requirements. Thomas presented detailed explanations of various technical implementations including Python specifications, finite field operations, and XMSS code interface, while the team discussed signature verification and key management approaches. The conversation ended with a review of network performance simulation results and discussions about handling proposals and attestation processes.

**Click to expand detailed summary**

The team discussed progress on the development of Devnet 0. They discussed the need for the remaining code to be reviewed and reviewed by the team. Guillaume provided updates on the metrics integration and the need for the Korthosis configuration to be ready for the testnet. The team agreed on the importance of aligning the metrics across clients after the fork choice specs are merged. Thomas and Gajinder confirmed that the multi-sig spec is ready for translation into the clients, and Mercy raised concerns about the use of a specific tool for the testnet, which Thomas will discuss with Benedict upon his return.

Thomas presented an overview of the Python specification file migration, explaining the structure of the spec repo and its organization into folders for different components like types, chains, containers, and networking. He described how the code is designed with typed structures and basic devnet config constants, with each file containing specific classes like blocks and other elements. Thomas emphasized that the code is simple and can be modified as needed, with documentation provided in Markdown files.

Thomas explained the implementation of finite field operations using the Collaber prime field, including basic operations like addition, subtraction, and multiplication. He demonstrated how the finite field is defined and tested, highlighting the simplicity of the current implementation compared to optimized versions like Poseidon. Thomas also described the structure of the Poseidon function, emphasizing the decoupling of the permutation step and the permutation of the function’s layers.

Thomas explained the XMSS code interface, emphasizing that clients should use the provided code rather than developing their own implementation for security reasons. He outlined the key functions: key generation, signing, and verification, detailing the parameters and procedures involved. Thomas clarified the concepts of activation epoch and active epochs, explaining how they relate to the key. Giacomo asked about the question about domain separation, which Thomas did not directly answer.

Thomas presented an overview of his work on signature verification, including the verification function and signature verification, and discussed the parameters and next steps for signature schemes. He agreed with the team to use a test configuration with smaller parameters for testing, as the current production configuration was too slow. Thomas mentioned he would implement the state transition function and present more details during the lean consensus call on Friday. The team discussed signature and public key sizes, with Gajinder requesting these values be included in the constants file for clarity. Thomas agreed to add these calculations. Ladislaus inquired about the relationship between activation time and key lifetime, and Thomas explained that for devnets, they would use a shorter activation time to reduce key generation time. Justin suggested using a maximum lifetime of 2^32 for consistency across all networks, avoiding key rotation complications.

Justin discussed solutions for handling proposals and attestation processes, suggesting two approaches: including attestation implicitly in proposals or splitting keys into proposer and attester groups. He clarified that proposals can include votes implicitly in blocks, but this vote won’t be aggregated with others due to a different message signature. Gajinder raised concerns about the applicability of these solutions to other key types, such as signing and slashing messages, and questioned the role of whistleblowers in rewards. Justin explained that whistleblowing rewards do not require signatures and clarified that proposals and attestations are the only two areas requiring signatures in the current system.

Kamil presented findings on the simulation of network performance. The results of the simulation were consistent with the network’s performance. The simulation results were discussed in the meeting. The simulation results were discussed in the meeting.

### Next Steps:

- Gajinder and Jun to finalize and clean up the specs for the transition functions for Devnet 0.
- unnawut and Reem team to integrate the finalized specs into their codebase within 3-5 days after the specs are merged.
- Guillaume to work with PQ on the kurtosis configuration for Devnet 0 testing.
- Guillaume to implement the Grafana setup for metrics visualization.
- unnawut and Guillaume to define specific metrics for consensus and fork choice measurements after the remaining specs are merged.
- Thomas to discuss with Benedict about merging Mercy’s PR related to hash sync.
- Thomas to add signature size and public key size constants to the XMSS implementation for clarity.
- Thomas to implement the state transition function and other 3SF components in the spec.
- Thomas to provide a more extensive presentation of the XMSS implementation during the Lean Consensus call on Friday.
- Kamil to share PQ aggregation simulation results with networking team members  for the Cambridge workshop.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: $0wq*zse)
- Download Chat (Passcode: $0wq*zse)

---

**system** (2025-09-04):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=RJB3IHo1H84

---

**system** (2025-09-04):

### Meeting Summary:

The team reviewed progress on Devnet 0 development, including code review needs and metrics integration requirements. Thomas presented detailed explanations of various technical implementations including Python specifications, finite field operations, and XMSS code interface, while the team discussed signature verification and key management approaches. The conversation ended with a review of network performance simulation results and discussions about handling proposals and attestation processes.

**Click to expand detailed summary**

The team discussed progress on the development of Devnet 0. They discussed the need for the remaining code to be reviewed and reviewed by the team. Guillaume provided updates on the metrics integration and the need for the Korthosis configuration to be ready for the testnet. The team agreed on the importance of aligning the metrics across clients after the fork choice specs are merged. Thomas and Gajinder confirmed that the multi-sig spec is ready for translation into the clients, and Mercy raised concerns about the use of a specific tool for the testnet, which Thomas will discuss with Benedict upon his return.

Thomas presented an overview of the Python specification file migration, explaining the structure of the spec repo and its organization into folders for different components like types, chains, containers, and networking. He described how the code is designed with typed structures and basic devnet config constants, with each file containing specific classes like blocks and other elements. Thomas emphasized that the code is simple and can be modified as needed, with documentation provided in Markdown files.

Thomas explained the implementation of finite field operations using the Collaber prime field, including basic operations like addition, subtraction, and multiplication. He demonstrated how the finite field is defined and tested, highlighting the simplicity of the current implementation compared to optimized versions like Poseidon. Thomas also described the structure of the Poseidon function, emphasizing the decoupling of the permutation step and the permutation of the function’s layers.

Thomas explained the XMSS code interface, emphasizing that clients should use the provided code rather than developing their own implementation for security reasons. He outlined the key functions: key generation, signing, and verification, detailing the parameters and procedures involved. Thomas clarified the concepts of activation epoch and active epochs, explaining how they relate to the key. Giacomo asked about the question about domain separation, which Thomas did not directly answer.

Thomas presented an overview of his work on signature verification, including the verification function and signature verification, and discussed the parameters and next steps for signature schemes. He agreed with the team to use a test configuration with smaller parameters for testing, as the current production configuration was too slow. Thomas mentioned he would implement the state transition function and present more details during the lean consensus call on Friday. The team discussed signature and public key sizes, with Gajinder requesting these values be included in the constants file for clarity. Thomas agreed to add these calculations. Ladislaus inquired about the relationship between activation time and key lifetime, and Thomas explained that for devnets, they would use a shorter activation time to reduce key generation time. Justin suggested using a maximum lifetime of 2^32 for consistency across all networks, avoiding key rotation complications.

Justin discussed solutions for handling proposals and attestation processes, suggesting two approaches: including attestation implicitly in proposals or splitting keys into proposer and attester groups. He clarified that proposals can include votes implicitly in blocks, but this vote won’t be aggregated with others due to a different message signature. Gajinder raised concerns about the applicability of these solutions to other key types, such as signing and slashing messages, and questioned the role of whistleblowers in rewards. Justin explained that whistleblowing rewards do not require signatures and clarified that proposals and attestations are the only two areas requiring signatures in the current system.

Kamil presented findings on the simulation of network performance. The results of the simulation were consistent with the network’s performance. The simulation results were discussed in the meeting. The simulation results were discussed in the meeting.

### Next Steps:

- Gajinder and Jun to finalize and clean up the specs for the transition functions for Devnet 0.
- unnawut and Reem team to integrate the finalized specs into their codebase within 3-5 days after the specs are merged.
- Guillaume to work with PQ on the kurtosis configuration for Devnet 0 testing.
- Guillaume to implement the Grafana setup for metrics visualization.
- unnawut and Guillaume to define specific metrics for consensus and fork choice measurements after the remaining specs are merged.
- Thomas to discuss with Benedict about merging Mercy’s PR related to hash sync.
- Thomas to add signature size and public key size constants to the XMSS implementation for clarity.
- Thomas to implement the state transition function and other 3SF components in the spec.
- Thomas to provide a more extensive presentation of the XMSS implementation during the Lean Consensus call on Friday.
- Kamil to share PQ aggregation simulation results with networking team members  for the Cambridge workshop.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: $0wq*zse)
- Download Chat (Passcode: $0wq*zse)

---

**system** (2025-09-04):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=RJB3IHo1H84

