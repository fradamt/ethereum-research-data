---
source: magicians
topic_id: 15822
title: "ERC-7518: Dynamic Compliant Interop Security Token - DyCIST"
author: 0xabhinav
date: "2023-09-18"
category: ERCs
tags: [erc, token, security, rwa]
url: https://ethereum-magicians.org/t/erc-7518-dynamic-compliant-interop-security-token-dycist/15822
views: 1973
likes: 5
posts_count: 7
---

# ERC-7518: Dynamic Compliant Interop Security Token - DyCIST

Discussion for ERC-7518

DyCIST is a proposed token standard that extends ERC-1155 and combines its functionality with other existing token standards, introducing unique features for interoperability, cross-chain operation, and token wrapping.

[PR](https://github.com/ethereum/ERCs/pull/67)

ERC-7518 defines a partitioned, semi-fungible token interface designed for regulated Real-World Assets (RWA). Existing token standards like ERC-20, ERC-721, and ERC-1155 cover fungibility and transfers, but they don’t natively handle the requirements of regulated assets such as compliance checks, partitioned balances, forced actions, or custody.

### Why it matters

RWA tokenization needs a standard that can satisfy issuers, custodians, and regulators without reinventing the wheel for every jurisdiction. ERC-7518 provides the base layer for this.

### Core Features

- Dynamic compliance hooks - onchain canTransfer, pluggable policy modules for US, EU, and global jurisdictions.
- Semi-fungibility and partitions - ERC-1155 native, with partition-scoped balances, rules, and lifecycle ops.
- Forced actions - standardized interfaces for force transfer, redeem, freeze/unfreeze, with audit events.
- Escrow and custody aware - vault-compatible holds/releases, authority-gated withdrawals, freezes without breaking accounting.
- Identity-agnostic - issuer-controlled eligibility checks, works with onchain or off-chain KYC, or custom registries, no hard dependencies.
- Cross-chain interoperability - clean split between token logic and bridging, proof-friendly events, adapters for message buses and wrappers.
- Upgrade and governance ready - parameters stored on-chain, upgradable via governed registry or parameter NFT.
- Minimal, safe admin surface - role separation, explicit scopes, no overlap between user and admin paths.
- Indexer-friendly events - partition-aware mint/burn/freeze/force ops with operator and reason codes.

Reference Implementation: [GitHub - zoniqx/erc7518_reference: Reference ERC7518 security token](https://github.com/zoniqx/erc7518_reference)

## Replies

**scotthconner** (2023-09-19):

This is really interesting, and very close to what I have for account keys for Locksmith Wallet, which is an ERC1155 token that has soulbinding mechanics as well, although they hare self minted.


      ![image](https://locksmith-wallet.gitbook.io/whitepaper/~gitbook/icon?size=small&theme=light)

      [locksmith-wallet.gitbook.io](https://locksmith-wallet.gitbook.io/whitepaper/architecture/permissions/key-vault)



    ![image](https://locksmith-wallet.gitbook.io/whitepaper/~gitbook/ogimage/jbppCceOh3e6EeWM2A2g)

###



ERC1155 Contract with some flare

---

**rajatwasan** (2025-08-18):

How do you see the self-minted soulbound tokens interacting with compliance or revocation?

---

**rajatwasan** (2025-09-09):

The reference implementation is now publicly available as ERC-7518, with EIP-712 compliance verification. Feedback is welcome. PRs and issues are open

---

**Serrus** (2025-10-16):

In practice, how should EIP-7518 handle token transfer rejections due to expired KYC or jurisdictional limits? Should these be logged on-chain (for audit) or handled via off-chain attestations?

---

**0xabhinav** (2025-10-18):

Such transfers would fail at the voucher generation stage itself. If the sender’s KYC has expired or the receiver is in a restricted jurisdiction, the generateVoucher() call will revert with a compliance error, preventing voucher creation. No on-chain event should log personal or sensitive data; instead, the off-chain attestation layer records the failure reason for audit.

Note: The standard is flexible; if you’re using on-chain attestations instead, you can emit opaque reason codes (e.g., 0x01 for compliance failure) in rejection events for on-chain audit trails, while keeping sensitive details off-chain.

---

**Divyansh2910** (2025-12-05):

How does ERC-7518 enforce transfer restrictions on a blockchain other than the primary issuance chain?

