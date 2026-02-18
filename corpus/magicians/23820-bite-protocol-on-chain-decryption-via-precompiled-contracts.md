---
source: magicians
topic_id: 23820
title: "BITE Protocol: On-Chain Decryption via Precompiled Contracts"
author: kladkogex
date: "2025-04-24"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/bite-protocol-on-chain-decryption-via-precompiled-contracts/23820
views: 59
likes: 0
posts_count: 1
---

# BITE Protocol: On-Chain Decryption via Precompiled Contracts

Hey folks

At SKALE we are developing BITE( Blockchain Integrated Threshold Encryption) where the current PoS validator committee is also a Threshold Encryption committee

In addition to provably eliminating MEV, one compelling direction for **BITE** is enabling smart contracts to perform **on-chain decryption** via a **precompiled contract**.

This would allow **Threshold Encryption (TE)** to become a native primitive in the EVM, making advanced coordination, privacy, and game-theoretic mechanisms not just possible—but practical.

---

###  Use Case 1: Multiplayer Rock-Paper-Scissors (RPS)

In a 3-player RPS game, each player submits an **encrypted move** (Rock, Paper, or Scissors). Once all encrypted moves are collected:

- The contract calls a decryption precompile to simultaneously decrypt all inputs.
- This guarantees a fair reveal—no player can adjust their move after seeing others.

---

###  Use Case 2: Sealed-Bid Auctions

Participants submit encrypted bids on-chain.

- After the smart contract collects all submissions, a precompiled decryption function is invoked.
- All bids are decrypted at once, enabling a trustless, fair reveal.

This eliminates the need for off-chain reveal phases and complex timeout logic.

---

###  Why a Precompiled Contract?

- Security: Deterministic, on-chain decryption avoids front-running and malicious reveals.
- Simplicity: Reduces reliance on off-chain coordination or multi-transaction workflows.

---

```auto
bytes plaintext = DecryptPrecompile.decrypt(bytes ciphertext);
```

The ciphertext would be encrypted using the current TE committee public key and decrypted using the current TE committee

###  Impact

If implemented, this would unlock a wide range of **privacy-preserving**, **game-theoretic**, and **multi-party coordination** applications on-chain—many of which are currently impractical due to the lack of synchronous, verifiable secret handling in Solidity.

---

Would love to hear thoughts on:

- Precompile feasibility and gas cost targets
- Threshold decryption protocols best suited for this use
- Real-world dApps this would enable

Looking forward to feedback from the community!
