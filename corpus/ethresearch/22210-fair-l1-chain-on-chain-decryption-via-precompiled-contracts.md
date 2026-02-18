---
source: ethresearch
topic_id: 22210
title: "FAIR L1 Chain: On-Chain Decryption via Precompiled Contracts"
author: kladkogex
date: "2025-04-24"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/fair-l1-chain-on-chain-decryption-via-precompiled-contracts/22210
views: 382
likes: 1
posts_count: 9
---

# FAIR L1 Chain: On-Chain Decryption via Precompiled Contracts

Hey folks

At SKALE we are developing BITE( Blockchain Integrated Threshold Encryption) where the current PoS validator committee is also a Threshold Encryption committee

The BITE protocol is used in the new L1 chain we just annouced - FAIR.

FAIR is an ETH fork that will support private data on chain


      ![](https://ethresear.ch/uploads/default/original/3X/c/8/c8cc64e7747c0d699ff934c18f029e5ebdc7cf9f.png)

      [fairchain.ai](https://www.fairchain.ai/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/d/4/d4eda73bff81630dab29d6c4960e9bf27a1ec221_2_690x361.png)

###



FAIR Blockchain is the first MEV-resistant Layer 1 built for the future of AI and finance. It has SKALE ecosystem integration, where MEV ends and fairness begins using AI Blockchain and AI Agents.










In addition to provably eliminating MEV, one compelling direction for **BITE** is enabling smart contracts to perform **on-chain decryption** via a **precompiled contract**.

This would allow **Threshold Encryption (TE)** to become a native primitive in the EVM, making advanced coordination, privacy, and game-theoretic mechanisms not just possible—but practical.

---

###  Use Case 1: Multiplayer Rock-Paper-Scissors (RPS)

In a 3-player RPS game, each player submits an **encrypted move** (Rock, Paper, or Scissors). Once all encrypted moves are collected:

- The contract calls a decryption precompile to simultaneously decrypt all inputs.
- This guarantees a fair reveal—no player can adjust their move after seeing others.

Today, this would require an off-chain commit-reveal protocol, which is more complex and less trustless.

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

## Replies

**jonhubby** (2025-07-18):

This is a really interesting direction. On-chain decryption via precompile could simplify a lot of otherwise clunky commit-reveal setups. Curious, are you considering any specific TE schemes (like BLS-based DKG) for the validator committees? Also wondering how gas costs might scale with number of decryptions.

---

**71104** (2025-07-18):

Eliminating MEV is a huge value proposition! How would this protocol work with e.g. a token swap transaction on a decentralized exchange? Imagine that both tokens as well as the exchange itself are based on this protocol, would then sandwiching the transaction with a buy and a sell become impossible?

---

**CPerezz** (2025-07-22):

Hey! This is a really cool idea!

I wonder:

- When is the key share distribution happening? At the beginning of each slot? Each block?
- What’s the expected bandwidth consumption you expect for distributing keys + encrypted messages vs no encryption whatsoever?
- How do you anticipate being able to maintain mempool health? ie. If I’m operating a pub mempool, I need to be sure I only include and forward VALID transactions. If those are encrypted, I assume there’s no way to check this??

Thanks!

---

**kladkogex** (2025-07-22):

Thank you Jon!!

We are doing BLS-based threshold encryption with DKG

The test net is already running !!!

---

**kladkogex** (2025-07-22):

Hey – thank you for the question.

For now, we perform DKG at each committee change. For temporary processes like auctions, this is acceptable since decryption happens within a reasonable timeframe.

If a transaction is submitted at an epoch boundary, it is encrypted using both the old and new committees’ public keys to ensure coverage.

For longer-term processes, we would need to explore something like re-keying, which requires using a Trusted Execution Environment.

If anyone is interested, here is a link to join the test net


      ![](https://ethresear.ch/uploads/default/original/3X/c/8/c8cc64e7747c0d699ff934c18f029e5ebdc7cf9f.png)

      [fairchain.ai](https://www.fairchain.ai/)



    ![](https://ethresear.ch/uploads/default/optimized/3X/d/4/d4eda73bff81630dab29d6c4960e9bf27a1ec221_2_690x361.png)

###



FAIR Blockchain is the first MEV-resistant Layer 1 built for the future of AI and finance. It has SKALE ecosystem integration, where MEV ends and fairness begins using AI Blockchain and AI Agents.

---

**kladkogex** (2025-07-22):

Thank you

Actually the smartcontracts do not change at all, so you could just run a Uniswap fork. The MEV-resistance is applied at the consensus layer, so smartcontracts get it for free. For AMM the transaction is encrypted by the user before submission and is decrypted after being included in the chain.

---

**qizhou** (2025-07-22):

Interesting idea.  I am curious about the security assumption of the TE, especially in terms of economic attacks such as bribery.

---

**kladkogex** (2025-07-22):

In TE things are decrypted and executed inside the Intel CPU enclave.

So break TE you in general need to break Intel corporate security

