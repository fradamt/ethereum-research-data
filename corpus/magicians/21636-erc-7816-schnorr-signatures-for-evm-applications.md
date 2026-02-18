---
source: magicians
topic_id: 21636
title: "ERC-7816: Schnorr Signatures for EVM Applications"
author: merkleplant
date: "2024-11-09"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7816-schnorr-signatures-for-evm-applications/21636
views: 313
likes: 5
posts_count: 3
---

# ERC-7816: Schnorr Signatures for EVM Applications

Discussion topic for ERC-7816: [Add ERC: Schnorr Signatures for EVM Applications by pmerkleplant · Pull Request #713 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/713)

#### Update Log

- 2024-11-09: Initial draft
- 2024-12-12: Updated title and sections order to conform to ERC guidelines

#### External Reviews

None as of 2024-11-09.

#### Outstanding Issues

- 2024-11-09: Provide test cases

## Replies

**merkleplant** (2024-11-09):

For some more background information, see [GitHub - verklegarden/schnorr-on-evm: A Schnorr Signature Scheme for EVM Applications](https://github.com/verklegarden/schnorr-on-evm).

---

**StackOverflowExcept1** (2024-11-10):

I experimented a bit with applications of this ERC, [FROST from Zcash Foundation](https://github.com/ZcashFoundation/frost) and [ROAST](https://eprint.iacr.org/2022/550). I managed to write very cheap threshold signature. It only costs ~4200 gas to verify threshold signature `t` of `n` onchain, plus ~2100 gas for calldata. See repository for more information: [GitHub - StackOverflowExcept1on/frost-secp256k1-evm: Cheap threshold signature scheme for EVM](https://github.com/StackOverflowExcept1on/frost-secp256k1-evm). I also made PR at Zcash Foundation that adds an efficient cipher suite for EVM: [feat: add `frost-secp256k1-evm` crate by StackOverflowExcept1on · Pull Request #749 · ZcashFoundation/frost · GitHub](https://github.com/ZcashFoundation/frost/pull/749). Based on audited cryptography from Zcash Foundation, I was also able to build an implementation of ROAST protocol (FROST protocol that is suitable for signing messages in asynchronous networks): [GitHub - StackOverflowExcept1on/roast: Rust implementation of ROAST (Robust Asynchronous Schnorr Threshold Signatures) with cryptography by Zcash Foundation](https://github.com/StackOverflowExcept1on/roast). The only downside of these Schnorr-based threshold signatures is that FROST is an interactive protocol. But these signatures are very cheap to use them in decentralized applications that are governed by an honest majority.

