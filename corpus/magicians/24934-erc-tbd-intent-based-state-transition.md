---
source: magicians
topic_id: 24934
title: "ERC-TBD: Intent-Based State Transition"
author: zergity
date: "2025-07-28"
category: ERCs
tags: [security, ux, intents]
url: https://ethereum-magicians.org/t/erc-tbd-intent-based-state-transition/24934
views: 194
likes: 0
posts_count: 3
---

# ERC-TBD: Intent-Based State Transition

I’m proposing a new ERC for an **Intent-Based State Transition Framework**. This framework directly addresses critical security vulnerabilities observed in existing smart contract interaction models, particularly those exploited via front-end manipulation.

## Motivation: The Bybit Phishing Attack (February 2025)

The Bybit hack ($1.5B+ ETH stolen) illustrates the vulnerability this ERC aims to resolve. Attackers compromised a Safe{Wallet} developer’s machine, injecting malicious JavaScript into the Safe{Wallet} UI. This facilitated:

- Displayed Data Manipulation: The UI presented a seemingly legitimate cold-to-warm wallet transfer.
- Malicious Logic Execution: However, the transaction data submitted for signing was altered to perform a delegatecall to a malicious contract. This contract subsequently drained the wallet, circumventing multisig safeguards.
- Blind Signing Exploitation: Signers, despite using hardware wallets, effectively “blind-signed” complex EIP-712 message, trusting the compromised UI to accurately represent the transaction’s true intent.

This incident exposed a critical weakness: robust smart contract logic and multisig configurations are insufficient if the interface layer is compromised and users cannot independently verify the true intent of what they are signing.

## Paradigm Shift: From Operations to Intents

**Current operation-based models** require users to sign transactions specifying precise, low-level operations (e.g., `call`, `delegatecall`, function selectors, raw `calldata`, or complex EIP-712 struct). This imperative approach demands that users understand and trust every byte of underlying transaction data, which is impractical for complex interactions. The Bybit attack demonstrates how reliance on this model leads to security failures when the user’s perception of operations is corrupted.

This ERC introduces an **intent-based** model. Instead of signing technical operations, users define and cryptographically sign their **desired high-level outcome or intent** in a human-readable format. The framework then ensures the necessary on-chain operations are executed to achieve this authorized intent.

## Core Framework Principle

This ERC establishes a more resilient security model by **decoupling critical application state from the application’s smart contract logic, storing it in a separate, dedicated storage contract**.

### Key Components:

- Storage Isolation: Critical state resides in an isolated contract. This protects the state even if the application logic contract (or its front-end) is unintentionally upgraded with malicious code or exploited.
- Owner-Controlled State: Control over this segregated storage is explicitly held by the state owner’s signature, independent of the application’s logic. This shifts asset sovereignty directly to the user.
- Explicit Intent Signatures: Any modification to this protected state requires an explicit signature from the state owner on a human-readable intent message. This ensures users transparently understand and authorize the intent of the state change, not opaque transaction calldata or complex EIP-712 struct.

## Example UX Flow

Consider a user initiating a proxy upgrade (or any state change within an application):

1. User Signs Human-Readable Intent: The user signs a human-readable message, example:

```auto
# Agreement 13 (42161) // Nonce and Chain ID
0x1234...5678         // account address (for nonce uniqueness)

## 0x2222...2222         // proxy address
--- Implementation = 0x3333..3333 // storage intent: upgrade proxy
--- Admin = 0x2345...6789 // set the new admin to new account
```

*This signed message represents the user’s explicit, cryptographically verifiable agreement to a set of desired state transitions.*

1. Transaction Execution: A transaction containing this signed agreement can then be sent on-chain. This transaction can be initiated by the user directly or by any relaying service.
2. On-Chain Verification & Enforcement: Any state modification targeting the intent-based storage contract must adhere to the signed agreement as a whole. If the actual state changes proposed by the transaction do not precisely match the signed intent, or if only a partial set of the agreed-upon state changes are attempted, the transaction will revert. This ensures atomic enforcement of the user’s explicit intent.

## Rationale

This framework addresses a fundamental trust layer by establishing a **direct, cryptographically verifiable communication channel from the user to their state and associated resources**. Technical operation details are abstracted into a “black box,” eliminating the need for users to trust the intricacies of application logic or front-end integrity. User state is protected even when interacting with compromised front-ends or malicious smart contracts, as the final authorization always derives from the user’s clearly signed intent. This directly mitigates UI manipulation attacks like the Bybit incident.

## Benefits

1. Enhanced Security: Reduces attack surface by isolating critical state from mutable application logic.
2. User Sovereignty: State changes are explicitly authorized by the owner’s signed human-readable intent, not by arbitrary code execution from potentially compromised interfaces.
3. Resilience to Compromise: Protects user state against application contract or front-end compromises, directly addressing vulnerabilities exploited in attacks like the Bybit incident.
4. Intent-Centric Model Alignment: Shifts authorization from low-level operations to high-level, human-understandable intents, aligning with more secure and intuitive Web3 interaction paradigms.

### Message Signing Choice: Plain Text vs. EIP-712

We advocate for **plain text message signing** for the underlying intent, rather than strict EIP-712 typed data signing. This decision prioritizes:

- Hardware Wallet Compatibility: Plain text message signing minimizes computational and display overhead for low-power hardware wallets. This enables broader device support and more reliable signing of complex intents on constrained environments.
- Display Flexibility: Plain text allows for unconstrained presentation of intent messages to the user. This bypasses EIP-712’s rigid schema requirements, enabling dApps to render contextually rich and highly human-readable summaries of state changes, directly on the signing device, without pre-defined type limitations.

We invite your technical review and feedback on this proposal before creating a new ERC PR.

Let’s discuss.

## Replies

**ryley-o** (2025-08-02):

I like this concept.

I think there is a lot of thinking on how to best communicate this to the user, but in general, it’s a good concept.

---

**zergity** (2025-08-04):

Front-ends do all the communication work. All the user sees is a fully comprehensible text signing request. They don’t need any training or explaining.

[![Intent-based State Transition](https://ethereum-magicians.org/uploads/default/optimized/2X/6/66e267fd3f70a2cfa5ba228f5598a9fb2a933906_2_689x436.png)Intent-based State Transition1209×764 62.4 KB](https://ethereum-magicians.org/uploads/default/66e267fd3f70a2cfa5ba228f5598a9fb2a933906)

