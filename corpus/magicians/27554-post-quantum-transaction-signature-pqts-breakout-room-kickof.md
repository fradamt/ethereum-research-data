---
source: magicians
topic_id: 27554
title: Post Quantum transaction signature (PQTS) Breakout Room - Kickoff Call
author: system
date: "2026-01-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/post-quantum-transaction-signature-pqts-breakout-room-kickoff-call/27554
views: 90
likes: 0
posts_count: 7
---

# Post Quantum transaction signature (PQTS) Breakout Room - Kickoff Call

### Agenda

**Date**: Feb 04, 2026

**Time**: 15:00 UTC

First session of the Post Quantum transaction signature (PQTS) Breakout Room

# Agenda overview

This inaugural call focuses on high-level overviews, expectation setting, and community alignment for the Post Quantum transaction signature (PQTS).

Key topics:

- Introduction to PQTS and its goals
- Walkthrough of the current EIPs
- Scheduling cadence & contribution expectations
- Team introductions & open Q&A

**Meeting Time:** Wednesday, February 04, 2026 at 15:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1889)

## Replies

**Cybercentry** (2026-01-22):

Excellent, we will be there! Many thanks!

---

**mindlapse** (2026-01-24):

For awareness: EIP-8052 has some traction already for EVM precompile support for post-quantum Falcon 512 signatures, to help with L2 use cases and smart contracts, with significant progress towards an implementation in Rust in a fork of `revm-compile` used by Reth.  It already includes and passes official KAT (Known Answer Test) acceptance tests.

`https://ethereum-magicians.org/t/eip-8052-precompile-for-falcon-support/25860/3?u=mindlapse`

---

**system** (2026-02-04):

YouTube recording available: https://youtu.be/kD2XZcwYUgQ

---

**system** (2026-02-04):

### Meeting Summary:

The meeting served as a kickoff call for post-quantum transaction signatures, with presentations covering various aspects of cryptographic implementation and integration into Ethereum’s framework. The team discussed different post-quantum cryptographic approaches, including ZKNox’s work on EIPs, comparisons between Falcon and Dilithium, and a proposal for quantum mitigation through a “proof of seed” mechanism. The discussion concluded with conversations about cryptographic agility, user migration challenges, and the need for flexible signature formats to accommodate future cryptographic advancements.

**Click to expand detailed summary**

Antonio and Gaudenzio checked the presentation setup, confirming that the slides were visible in full-screen mode. Antonio mentioned that the call was being recorded and might be uploaded to YouTube later. The meeting was set to start in a few minutes, with Antonio planning to give a quick presentation to set the stage for the technical discussions that would follow.

The meeting served as a kickoff call for post-quantum transaction signatures, with Antonio setting the stage by introducing the four components of the execution layer: consensus, data-availability, and stateless Ethereum. He highlighted the need for new mathematics resistant to quantum computing, mentioning five to six macro areas of cryptography, and emphasized that selecting and implementing post-quantum algorithms is a time-consuming process. The discussion focused on the progress made in post-quantum cryptography, with Antonio noting that Ethereum has been preparing for potential quantum threats since 2016, and the meeting included presentations from Renaud, Simon, Nixo, Stefano, and Dano on various aspects of post-quantum transaction signatures and cryptographic agility.

Renaud-ZKNOX presented ZKNox’s work on post-quantum cryptography for blockchain, focusing on the implementation of EIPs 8051 (MLDSA) and 8052 (Falcon precompile). Simon detailed the comparison between Falcon and Dilithium in terms of key sizes, gas costs, and implementation challenges. The team discussed the advantages and limitations of each scheme, including security levels, standardization status, and zero-knowledge proof compatibility. They also addressed questions about precompile gas costs, hashing algorithms, and the integration of post-quantum signatures into Ethereum accounts.

Renaud-ZKNOX demonstrated a user app implementation using non-native account abstractions, highlighting the need for native account abstraction to eliminate reliance on bundlers and EOA. Nico presented the Frame Transaction Proposal (EIP-8141), which introduces a new transaction type with flexible frames for verification and execution, replacing the current ECDsa signature model. The discussion addressed the compatibility and migration paths between existing account systems and the new native AA, with Nico confirming that the ERC-4337 ecosystem would continue to exist alongside the new native solution.

Stefano presented a proposal for a quantum mitigation strategy, focusing on a user-space, on-chain solution that can be deployed quickly in case of an unexpected quantum breakthrough. The proposal involves implementing a “proof of seed” mechanism, which lifts current quantum schemes to quantum resistance schemes using zero-knowledge proofs. The solution aims to protect the majority of hardware and software wallets without requiring user action, and is designed to be a temporary measure until more permanent post-quantum solutions are ready. Stefano highlighted the challenges of implementing this solution, including memory constraints in secure elements and the need for secure OS access in some cases. The team plans to have a concrete implementation with a demonstrator ready by ECC in the coming weeks.

The meeting focused on cryptographic agility in Ethereum transactions, presented by Danno. He explained the need for flexible signature formats to accommodate future cryptographic advancements, contrasting current ECDSA transactions with a proposed modular approach that would allow easy swapping of signature algorithms without major changes to the transaction format. The discussion highlighted potential challenges with integrating cryptographic agility into frame transactions and the importance of supporting multiple signature algorithms simultaneously to adapt to evolving cryptographic needs. Participants also discussed the implications for smart contracts and apps, with Parthasarathy raising concerns about apps relying on specific signature schemes.

The meeting focused on the integration of frame transaction efforts and the need to update dApps to address security concerns. Danno acknowledged learning about the issue recently and expressed the need to get involved, while Antonio emphasized the importance of viewing it as a unified effort. The discussion highlighted the challenges of convincing users to migrate, with Fab noting that the main concern is with average users who may not follow developments closely, and not with developers or infrastructure institutions. The team plans to address these challenges with a ZK-based patch and aims to continue the discussion in the next meeting.

Antonio discussed cryptographic agility, emphasizing the importance of allowing users to choose their own cryptographic methods, including post-quantum signatures. Danno highlighted the trade-offs associated with different signature methods and the varying needs of users. Nico presented an EIP that would allow users to deactivate their elliptic curve private keys, with a 7-day delay for cancellation. The group agreed to have a more focused meeting in the future to delve deeper into specific topics.

### Next Steps:

- Renaud and Simon : Continue integration of Falcon  into 4337 account to allow users to choose between Delithium or Falcon for hybrid accounts
- Stefano and Fabrizio: Complete concrete implementation with demonstrator for proof of seed solution within the next couple of weeks
- Stefano and Fabrizio: Have full demonstrator ready by ECC for the ZK-based proof of seed approach
- Renaud  and NeverLocal team: Collaborate on BIP39 derivation work as Antonio identified synergy between their similar efforts
- Danno: Connect and integrate with the frame transaction team  to discuss cryptographic agility design principles
- Nico: Complete opening PR to update EIP 7851 for EOA deactivation with time lock feature
- Nico: Create additional EIP to modify ECRECOVER precompile to address post-quantum security concerns with permit and option protocols
- Nico: Present EIP 7851  and related ECRECOVER changes in an upcoming breakout call
- Antonio: Collect and facilitate synergies identified during the call by connecting relevant parties privately
- Antonio: Organize call number two in two weeks with presentations on multi-signatures/threshold schemes and aggregatable signatures
- Jay: Prepare presentation on multi-signatures and threshold schemes for next call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: M^Y0n=Yt)
- Download Chat (Passcode: M^Y0n=Yt)
- Download Audio (Passcode: M^Y0n=Yt)

---

**system** (2026-02-04):

### Meeting Summary:

The meeting served as a kickoff call for post-quantum transaction signatures, with presentations covering various aspects of cryptographic implementation and integration into Ethereum’s framework. The team discussed different post-quantum cryptographic approaches, including ZKNox’s work on EIPs, comparisons between Falcon and Dilithium, and a proposal for quantum mitigation through a “proof of seed” mechanism. The discussion concluded with conversations about cryptographic agility, user migration challenges, and the need for flexible signature formats to accommodate future cryptographic advancements.

**Click to expand detailed summary**

Antonio and Gaudenzio checked the presentation setup, confirming that the slides were visible in full-screen mode. Antonio mentioned that the call was being recorded and might be uploaded to YouTube later. The meeting was set to start in a few minutes, with Antonio planning to give a quick presentation to set the stage for the technical discussions that would follow.

The meeting served as a kickoff call for post-quantum transaction signatures, with Antonio setting the stage by introducing the four components of the execution layer: consensus, data-availability, and stateless Ethereum. He highlighted the need for new mathematics resistant to quantum computing, mentioning five to six macro areas of cryptography, and emphasized that selecting and implementing post-quantum algorithms is a time-consuming process. The discussion focused on the progress made in post-quantum cryptography, with Antonio noting that Ethereum has been preparing for potential quantum threats since 2016, and the meeting included presentations from Renaud, Simon, Nixo, Stefano, and Dano on various aspects of post-quantum transaction signatures and cryptographic agility.

Renaud-ZKNOX presented ZKNox’s work on post-quantum cryptography for blockchain, focusing on the implementation of EIPs 8051 (MLDSA) and 8052 (Falcon precompile). Simon detailed the comparison between Falcon and Dilithium in terms of key sizes, gas costs, and implementation challenges. The team discussed the advantages and limitations of each scheme, including security levels, standardization status, and zero-knowledge proof compatibility. They also addressed questions about precompile gas costs, hashing algorithms, and the integration of post-quantum signatures into Ethereum accounts.

Renaud-ZKNOX demonstrated a user app implementation using non-native account abstractions, highlighting the need for native account abstraction to eliminate reliance on bundlers and EOA. Nico presented the Frame Transaction Proposal (EIP-8141), which introduces a new transaction type with flexible frames for verification and execution, replacing the current ECDsa signature model. The discussion addressed the compatibility and migration paths between existing account systems and the new native AA, with Nico confirming that the ERC-4337 ecosystem would continue to exist alongside the new native solution.

Stefano presented a proposal for a quantum mitigation strategy, focusing on a user-space, on-chain solution that can be deployed quickly in case of an unexpected quantum breakthrough. The proposal involves implementing a “proof of seed” mechanism, which lifts current quantum schemes to quantum resistance schemes using zero-knowledge proofs. The solution aims to protect the majority of hardware and software wallets without requiring user action, and is designed to be a temporary measure until more permanent post-quantum solutions are ready. Stefano highlighted the challenges of implementing this solution, including memory constraints in secure elements and the need for secure OS access in some cases. The team plans to have a concrete implementation with a demonstrator ready by ECC in the coming weeks.

The meeting focused on cryptographic agility in Ethereum transactions, presented by Danno. He explained the need for flexible signature formats to accommodate future cryptographic advancements, contrasting current ECDSA transactions with a proposed modular approach that would allow easy swapping of signature algorithms without major changes to the transaction format. The discussion highlighted potential challenges with integrating cryptographic agility into frame transactions and the importance of supporting multiple signature algorithms simultaneously to adapt to evolving cryptographic needs. Participants also discussed the implications for smart contracts and apps, with Parthasarathy raising concerns about apps relying on specific signature schemes.

The meeting focused on the integration of frame transaction efforts and the need to update dApps to address security concerns. Danno acknowledged learning about the issue recently and expressed the need to get involved, while Antonio emphasized the importance of viewing it as a unified effort. The discussion highlighted the challenges of convincing users to migrate, with Fab noting that the main concern is with average users who may not follow developments closely, and not with developers or infrastructure institutions. The team plans to address these challenges with a ZK-based patch and aims to continue the discussion in the next meeting.

Antonio discussed cryptographic agility, emphasizing the importance of allowing users to choose their own cryptographic methods, including post-quantum signatures. Danno highlighted the trade-offs associated with different signature methods and the varying needs of users. Nico presented an EIP that would allow users to deactivate their elliptic curve private keys, with a 7-day delay for cancellation. The group agreed to have a more focused meeting in the future to delve deeper into specific topics.

### Next Steps:

- Renaud and Simon : Continue integration of Falcon  into 4337 account to allow users to choose between Delithium or Falcon for hybrid accounts
- Stefano and Fabrizio: Complete concrete implementation with demonstrator for proof of seed solution within the next couple of weeks
- Stefano and Fabrizio: Have full demonstrator ready by ECC for the ZK-based proof of seed approach
- Renaud  and NeverLocal team: Collaborate on BIP39 derivation work as Antonio identified synergy between their similar efforts
- Danno: Connect and integrate with the frame transaction team  to discuss cryptographic agility design principles
- Nico: Complete opening PR to update EIP 7851 for EOA deactivation with time lock feature
- Nico: Create additional EIP to modify ECRECOVER precompile to address post-quantum security concerns with permit and option protocols
- Nico: Present EIP 7851  and related ECRECOVER changes in an upcoming breakout call
- Antonio: Collect and facilitate synergies identified during the call by connecting relevant parties privately
- Antonio: Organize call number two in two weeks with presentations on multi-signatures/threshold schemes and aggregatable signatures
- Jay: Prepare presentation on multi-signatures and threshold schemes for next call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: M^Y0n=Yt)
- Download Chat (Passcode: M^Y0n=Yt)
- Download Audio (Passcode: M^Y0n=Yt)

---

**system** (2026-02-04):

### Meeting Summary:

The meeting served as a kickoff call for post-quantum transaction signatures, with presentations covering various aspects of cryptographic implementation and integration into Ethereum’s framework. The team discussed different post-quantum cryptographic approaches, including ZKNox’s work on EIPs, comparisons between Falcon and Dilithium, and a proposal for quantum mitigation through a “proof of seed” mechanism. The discussion concluded with conversations about cryptographic agility, user migration challenges, and the need for flexible signature formats to accommodate future cryptographic advancements.

**Click to expand detailed summary**

Antonio and Gaudenzio checked the presentation setup, confirming that the slides were visible in full-screen mode. Antonio mentioned that the call was being recorded and might be uploaded to YouTube later. The meeting was set to start in a few minutes, with Antonio planning to give a quick presentation to set the stage for the technical discussions that would follow.

The meeting served as a kickoff call for post-quantum transaction signatures, with Antonio setting the stage by introducing the four components of the execution layer: consensus, data-availability, and stateless Ethereum. He highlighted the need for new mathematics resistant to quantum computing, mentioning five to six macro areas of cryptography, and emphasized that selecting and implementing post-quantum algorithms is a time-consuming process. The discussion focused on the progress made in post-quantum cryptography, with Antonio noting that Ethereum has been preparing for potential quantum threats since 2016, and the meeting included presentations from Renaud, Simon, Nixo, Stefano, and Dano on various aspects of post-quantum transaction signatures and cryptographic agility.

Renaud-ZKNOX presented ZKNox’s work on post-quantum cryptography for blockchain, focusing on the implementation of EIPs 8051 (MLDSA) and 8052 (Falcon precompile). Simon detailed the comparison between Falcon and Dilithium in terms of key sizes, gas costs, and implementation challenges. The team discussed the advantages and limitations of each scheme, including security levels, standardization status, and zero-knowledge proof compatibility. They also addressed questions about precompile gas costs, hashing algorithms, and the integration of post-quantum signatures into Ethereum accounts.

Renaud-ZKNOX demonstrated a user app implementation using non-native account abstractions, highlighting the need for native account abstraction to eliminate reliance on bundlers and EOA. Nico presented the Frame Transaction Proposal (EIP-8141), which introduces a new transaction type with flexible frames for verification and execution, replacing the current ECDsa signature model. The discussion addressed the compatibility and migration paths between existing account systems and the new native AA, with Nico confirming that the ERC-4337 ecosystem would continue to exist alongside the new native solution.

Stefano presented a proposal for a quantum mitigation strategy, focusing on a user-space, on-chain solution that can be deployed quickly in case of an unexpected quantum breakthrough. The proposal involves implementing a “proof of seed” mechanism, which lifts current quantum schemes to quantum resistance schemes using zero-knowledge proofs. The solution aims to protect the majority of hardware and software wallets without requiring user action, and is designed to be a temporary measure until more permanent post-quantum solutions are ready. Stefano highlighted the challenges of implementing this solution, including memory constraints in secure elements and the need for secure OS access in some cases. The team plans to have a concrete implementation with a demonstrator ready by ECC in the coming weeks.

The meeting focused on cryptographic agility in Ethereum transactions, presented by Danno. He explained the need for flexible signature formats to accommodate future cryptographic advancements, contrasting current ECDSA transactions with a proposed modular approach that would allow easy swapping of signature algorithms without major changes to the transaction format. The discussion highlighted potential challenges with integrating cryptographic agility into frame transactions and the importance of supporting multiple signature algorithms simultaneously to adapt to evolving cryptographic needs. Participants also discussed the implications for smart contracts and apps, with Parthasarathy raising concerns about apps relying on specific signature schemes.

The meeting focused on the integration of frame transaction efforts and the need to update dApps to address security concerns. Danno acknowledged learning about the issue recently and expressed the need to get involved, while Antonio emphasized the importance of viewing it as a unified effort. The discussion highlighted the challenges of convincing users to migrate, with Fab noting that the main concern is with average users who may not follow developments closely, and not with developers or infrastructure institutions. The team plans to address these challenges with a ZK-based patch and aims to continue the discussion in the next meeting.

Antonio discussed cryptographic agility, emphasizing the importance of allowing users to choose their own cryptographic methods, including post-quantum signatures. Danno highlighted the trade-offs associated with different signature methods and the varying needs of users. Nico presented an EIP that would allow users to deactivate their elliptic curve private keys, with a 7-day delay for cancellation. The group agreed to have a more focused meeting in the future to delve deeper into specific topics.

### Next Steps:

- Renaud and Simon : Continue integration of Falcon  into 4337 account to allow users to choose between Delithium or Falcon for hybrid accounts
- Stefano and Fabrizio: Complete concrete implementation with demonstrator for proof of seed solution within the next couple of weeks
- Stefano and Fabrizio: Have full demonstrator ready by ECC for the ZK-based proof of seed approach
- Renaud  and NeverLocal team: Collaborate on BIP39 derivation work as Antonio identified synergy between their similar efforts
- Danno: Connect and integrate with the frame transaction team  to discuss cryptographic agility design principles
- Nico: Complete opening PR to update EIP 7851 for EOA deactivation with time lock feature
- Nico: Create additional EIP to modify ECRECOVER precompile to address post-quantum security concerns with permit and option protocols
- Nico: Present EIP 7851  and related ECRECOVER changes in an upcoming breakout call
- Antonio: Collect and facilitate synergies identified during the call by connecting relevant parties privately
- Antonio: Organize call number two in two weeks with presentations on multi-signatures/threshold schemes and aggregatable signatures
- Jay: Prepare presentation on multi-signatures and threshold schemes for next call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: M^Y0n=Yt)
- Download Chat (Passcode: M^Y0n=Yt)
- Download Audio (Passcode: M^Y0n=Yt)

