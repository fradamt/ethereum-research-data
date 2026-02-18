---
source: magicians
topic_id: 24554
title: ERC Stateless Encrypted Communication Standard
author: sewing848
date: "2025-06-14"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/erc-stateless-encrypted-communication-standard/24554
views: 107
likes: 1
posts_count: 1
---

# ERC Stateless Encrypted Communication Standard

ERC-7970 proposes a minimal, non-financial standard for encrypted peer-to-peer communication using smart contracts on EVM chains.

The draft ERC defines a stateless protocol that transmits encrypted messages through a single emitted event. It specifies structured message types to support ECDH key exchange and AES-GCM encryption, but does not enforce these cryptographic operations in the contract itself. Instead, all key derivation, encryption, decryption, and semantic enforcement occur off-chain in compliant clients. The contract emits one event with four parameters: `from`, `to`, `messageType`, and `data`.

The goal is to define a foundational primitive, not a full messaging protocol. This allows applications to build on top with their own onboarding, spam controls, identity layers, or encryption preferences, while maintaining interoperability through the shared event format.

You can find the draft here:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1085)














####


      `master` ← `sewing848:master`




          opened 01:47PM - 12 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/85144593?v=4)
            sewing848](https://github.com/sewing848)



          [+215
            -0](https://github.com/ethereum/ERCs/pull/1085/files)







This PR proposes a new ERC: Stateless Encrypted Communication Standard.

It de[…](https://github.com/ethereum/ERCs/pull/1085)fines a minimal, event-based interface for encrypted peer-to-peer messaging between two EVM addresses. The standard is:

- Stateless (no in-contract storage)
- Non-financial (no value transfer or payment required)
- Gas-efficient (single event emission)
- Designed for encrypted communication using off-chain interpretation

Message types 0, 1, and 2 are reserved for connection setup and encrypted text messaging, following a RECOMMENDED cryptographic model: key exchange via ECDH and authenticated encryption via AES-GCM. All cryptographic operations are performed off-chain, enabling interoperability while preserving implementation flexibility.

Discussion thread: [Ethereum Magicians topic](https://ethereum-magicians.org/t/erc-stateless-encrypted-communication-standard)












A working prototype of a decentralized messaging application has informed the development of this standard. The app uses a similar model, with encrypted messaging over EVM blockchains transmitted through emitted events. It currently separates the user-connection process and encrypted messaging into different contracts, but a major refactor is underway to incorporate the proposed standard as the unified messaging layer. This real-world usage has helped identify the core requirements for the standard. The app is functional on macOS but not yet production-ready.

The contracts currently used for connection setup and encrypted messaging in the prototype are available here:



      [github.com](https://github.com/sewing848/ataraxia)




  ![image](https://opengraph.githubassets.com/d383cf1f8a230d4bcc02e4f06dd5953f/sewing848/ataraxia)



###



Ataraxia protocol for data transfer












      [github.com](https://github.com/sewing848/pyoconnectionmanager)




  ![image](https://opengraph.githubassets.com/ffd74336415b5970478537891b794bed/sewing848/pyoconnectionmanager)



###



Contribute to sewing848/pyoconnectionmanager development by creating an account on GitHub.










## Related EIPs

This proposal is intentionally minimal and stateless, in the spirit of [ERC-3722: Poster](https://eips.ethereum.org/EIPS/eip-3722), which emits plaintext posts for decentralized social media. While Poster focuses on public broadcast-style messaging, this proposed standard defines a private, encrypted peer-to-peer communication model.

The two differ not just in use case but in security assumptions: posting plaintext messages to an immutable, public blockchain poses long-term risks, especially if illegal or harmful content becomes permanently associated with a project or platform. This standard is specifically intended for encrypted communication between two addresses - not plaintext public posts.

This proposal also contrasts with [ERC-7627: Secure Messaging Protocol](https://eips.ethereum.org/EIPS/eip-7627), which defines a comprehensive messaging interface, including on-chain key management, encryption algorithm enumeration, and session identifiers.

By contrast, this standard is intended to facilitate basic encrypted communication between two addresses within a wide range of app environments, while offering the flexibility to incorporate other features through app-specific use of the messageType parameter. It also aims to minimize gas costs.

This ERC is intended as a foundation for further work. I’m currently preparing a follow-up ERC that defines a Non-Economic Token standard for per-connection blockchain channel blocking (replacing the prototype’s current ERC-20 token approach).

Thanks in advance for your input.

Scott
