---
source: ethresearch
topic_id: 17748
title: MAPP(Multi Asset Privacy Pool)
author: adust09
date: "2023-12-10"
category: Privacy
tags: []
url: https://ethresear.ch/t/mapp-multi-asset-privacy-pool/17748
views: 1800
likes: 0
posts_count: 3
---

# MAPP(Multi Asset Privacy Pool)

# 1. Introduction

The Multi Asset Privacy Pool proposed here is an integration of the Multi Asset Shielded Pool mechanism into Privacy Pools.

It enables the maximization of the Privacy Pool size and allows users with all assets to have a common level of privacy.

# 2. Motivation

Both Privacy Pool and MASP share the motivation of maximizing the pool size, so combining the two mechanisms can result in synergistic effects.

It also allows for addressing the respective shortcomings of each.

# 3. Privacy Pool

## 3.1 Overview

Privacy Pool can provide compliance functionality to protocols that offer Confidential Tx capabilities, such as Tornado Cash.

Intuitively, the idea is to restrict user participation in the pool based on a whitelist or blacklist.

This allows for transactions only with KYC-verified addresses or prevents access to the pool for users identified as malicious based on past transactions.

## 3.2 Statement

The following statement is required:

```auto
note commitment = hash(amount, pubKey, blinding, assetType)
association commitment = hash(amount, pubKey, blinding, assetType, valueBase)
nullifier = hash(commitment, merklePath, sign(privKey, commitment, merklePath))

```

The importance of maximizing the Association Set is discussed in the Privacy Pool derived from Tornado Cash.

## 3.3 Weakness

Shielded spaces created within transparent spaces like Ethereum, similar to Tornado Cash, can be susceptible to inference based on transactions accessing both internal and external spaces. In other words, increasing the number of participating addresses or transactions in the protocol enhances obfuscation, making the continuous maximization of pool size important from a privacy perspective.

However, there remains the challenge of relatively easier inference for low-liquidity assets due to their smaller pool size.

Additionally, there may be pressures to reduce the pool size, such as through blacklisting.

(The management method for the Association set by the Association set provider is determined for each protocol and is not discussed here.)

# 4. MASP

## 4.1 Overview

MASP is a concept proposed by the Zcash community, which involves managing multiple assets in a single Shielded Pool, thereby simplifying the process.

This not only allows for providing Confidential Transaction functionality to multiple assets but also enables consolidating assets in one Shielded Pool, leading to improved obfuscation.

In other words, any asset can share the same level of obfuscation.

[![スクリーンショット 2023-12-10 14.44.08](https://ethresear.ch/uploads/default/optimized/2X/7/70239af0c294437a416c817f45bc57835739d5a0_2_690x334.jpeg)スクリーンショット 2023-12-10 14.44.081920×930 61.8 KB](https://ethresear.ch/uploads/default/70239af0c294437a416c817f45bc57835739d5a0)

Projects like Namada and Penumbla have adopted MASP and provide cross-chain private swaps through their own bridges.

## 4.2 Statement

The following statement is required:

```auto
valueBase = hash(assetType)
note commitment = hash(amount, pubKey, blinding, assetType, valueBase)
nullifier = hash(commitment, merklePath, sign(privKey, commitment, merklePath))

```

## 4.3 Weakness

While MASP itself helps maximize privacy strength, it does not inherently have compliance functionality within the protocol. From the perspective of user protection, additional features such as Zcash’s Viewing Key or zkBob’s Optional KYC become necessary.

# 5. MAPP

The mechanism is simple - add valuebase to the note commitment of the Privacy Pool.

The following statement is required:

```auto
valueBase = hash(assetType)
note commitment = hash(amount, pubKey, blinding, assetType, valueBase)
association commitment = hash(amount, pubKey, blinding, assetType, valueBase)
nullifier = hash(commitment, merklePath, sign(privKey, commitment, merklePath))

```

Asset type can be obtained from the token’s contract address or hardcoded.

For example, Namada explicitly defines supported token types and has rules and mechanisms in place to handle them appropriately.

This allows for maintaining compliance functionality in the Privacy Pool while maximizing the pool size and providing a common level of obfuscation for all assets.

# 6. Conclusion

Here, we have introduced the integration of MASP as a way to complement the functionality of Privacy Pools.

Conversely, it can be seen as adding compliance functionality to MASP.

The specific methods of obtaining asset types and listing Association sets will vary between projects, but integrating these two systems with a shared motivation can be understood in terms of maximizing privacy.

# 7. References

- GitHub - namada-net/masp: The multi-asset shielded pool (MASP) provides a unified privacy set for all assets on Namada.
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4563364

## Replies

**paulneet** (2023-12-22):

Shielding transactions requires more computation (validation on the client or on the blockchain). So how can the transaction costs of blocking transactions be reduced? Isn’t this also a hard problem that MASP needs to solve?

---

**crandll** (2024-01-05):

Tools like MASP are completely decentralized, which is promising from this point of view. but their decentralization also brings drawbacks, such as difficulty in obtaining investments. There is also the increasingly strict regulation, if all users need kyc, then it will greatly limit the number of his users, thus not conducive to the development.

