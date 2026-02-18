---
source: magicians
topic_id: 25013
title: "ERC-7995: Encrypted Data"
author: immortal-tofu
date: "2025-08-04"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7995-encrypted-data/25013
views: 137
likes: 0
posts_count: 1
---

# ERC-7995: Encrypted Data

ERC-7995 defines a standard for handling encrypted data in Ethereum smart contracts. It introduces:

- Encrypted data types (euint256, ebool, etc.) as bytes32 handles.
- Off-chain encrypted inputs with validation proofs (externalEuint8, externalEuint16, externalEbool, …).
- Smart contract modules for access control, encrypted computation, and decryption via oracles.
- Support for homomorphic operations (e.g. addition, comparison) on encrypted values.
- JavaScript API for encrypted input generation and user-side or delegated decryption (via EIP-712).

It enables building **privacy-preserving DApps**, like private voting, sealed-bid auctions, or confidential transfers, while maintaining composability and auditability.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1143)














####


      `master` ← `immortal-tofu:add-encrypted-types`




          opened 08:08PM - 30 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/1384478?v=4)
            immortal-tofu](https://github.com/immortal-tofu)



          [+596
            -0](https://github.com/ethereum/ERCs/pull/1143/files)







This PR proposes a new ERC introducing a standard for representing, validating, […](https://github.com/ethereum/ERCs/pull/1143)and operating on encrypted data in Ethereum smart contracts. It defines a set of encrypted data types (euint*, ebool, etc.), validation interfaces for off-chain ciphertexts, and decryption oracle mechanisms for asynchronous decryption. The goal is to enable privacy-preserving dApps that remain composable, auditable, and interoperable across contracts and toolchains.
