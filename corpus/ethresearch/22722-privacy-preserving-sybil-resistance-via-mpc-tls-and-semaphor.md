---
source: ethresearch
topic_id: 22722
title: Privacy-Preserving Sybil Resistance via MPC-TLS and Semaphore Proofs
author: Dobrokhvalov
date: "2025-07-09"
category: Privacy
tags: [identity, sybil-attack]
url: https://ethresear.ch/t/privacy-preserving-sybil-resistance-via-mpc-tls-and-semaphore-proofs/22722
views: 262
likes: 2
posts_count: 3
---

# Privacy-Preserving Sybil Resistance via MPC-TLS and Semaphore Proofs

We propose a solution that allows Internet users to privately prove control over real web accounts (like Uber or GitHub) using MPC-TLS without revealing any personal data. By converting these credentials into unlinkable zero-knowledge group proofs, we can unlock Sybil-resistant airdrops, governance, and access control without compromising user privacy.

#### Protocol Overview:

```auto
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Browser  │    │   TLS Notary    │    │   Web Service   │
│   Extension     │    │                 │    │   (e.g. Uber)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │←──── MPC Protocol ───→│                       │
         │                       │                       │
         │←──────── MPC-TLS Session─────────────────────→│
         │         (joint client)                        │
         │                       │                       │
         │──── Encrypted TLS ───→│                       │
         │      transcript       │                       │
         │                       │                       │
         │←─── Attestation  ─────┤                       │
         │   (garbled circuit)   │                       │
         │                       │                       │
         ▼
┌─────────────────┐
│   Semaphore     │
│   Group         │
│   Commitment    │
└─────────────────┘
```

The protocol works as follows (simplified for clarity):

**Phase 1: Private Credential Verification**

1. User’s browser extension and TLS Notary cooperatively establish MPC-TLS session with web service
2. Notary validates ciphertext integrity using garbled circuits, signs attestation over committed fields
3. Notary sees only encrypted data—never plaintext account information
4. User receives cryptographic proof of credential without exposing account details

**Phase 2: Unlinkable Commitment Generation**

```auto
commitment = Hash(master_key || credential_group_id || account_id_hash)
```

1. User generates unlinkable identity commitment using private Master Key
2. Commitment is published to corresponding Semaphore group (GitHub credentials → GitHub group, etc.)
3. Each credential type maps to separate group, enabling granular proof targeting

**Phase 3: Providing Zero-Knowledge Group Proofs**

1. For verification, user generates ZK proofs of Semaphore group membership
2. Proofs confirm credential possession without revealing specific accounts
3. Verifying parties can combine multiple group proofs for composable trust scores

### Privacy Guarantees:

- Unlinkable: Cannot connect different web accounts to same user
- Group-anonymous: Individual verifications don’t reveal which specific member of a credential group is generating the proof
- Untraceable: Cannot track users across different applications
- Composable: Can prove membership in multiple groups simultaneously

## Implementation

We’re building BringID to validate these cryptographic techniques in practice. The implementation leverages existing infrastructure ([TLSN](https://tlsnotary.org/) for MPC-TLS, [Semaphore](https://semaphore.pse.dev/) for ZK group proofs) to minimize novel cryptographic assumptions.

The current design assumes a trusted TLS Notary for attestation verification. We’re exploring various decentralization approaches to minimize this trust requirement in the future, including TEE-backed infrastructure and distributed validator networks.

## Economic Security Model

Our approach doesn’t cryptographically prevent Sybils—it makes them **economically infeasible**. The security assumption is:

> Reward value per verified account < Cost of producing a Sybil identity

Web accounts require real-world activity (Uber rides, GitHub commits, Airbnb stays), time investment (account aging, reputation building), and often monetary cost (service usage fees). Applications can combine multiple credential groups and apply time-bounded verification to further increase forgery costs.

---

**Technical Specification**: [Draft whitepaper](https://github.com/BringID/whitepaper/blob/929ab34093a7b8a920673643a6b9f6a787a5d72f/whitepaper.md)

**Related Work**: [TLSN](https://tlsnotary.org/) | [Semaphore](https://semaphore.pse.dev/)

## Replies

**jonhubby** (2025-07-11):

That’s super interesting work, Dobrokhvalov! ![:rocket:](https://ethresear.ch/images/emoji/facebook_messenger/rocket.png?v=12) I love the idea of using MPC-TLS and Semaphore together for private credential proofs. Curious, have you thought about how to handle revocation if a user’s web account gets compromised?

---

**Dobrokhvalov** (2025-07-12):

Great question!

So if a user web account has been compromised, an attacker can tie the account to their Master Key by updating the corresponding identity commitment in the Credential Registry and use it generate proofs to bypass sybil checks.

To be honest, revocation scheme is something we still need to iron out, here’s our initial thoughts:

First, the registry should allow updates of a commitment for the same web account only on periodic basis (e.g. monthly), otherwise we will end up with two distinct nullifiers for the same web account or double use of the identity commitment in the same scope. (e.g. vote being counted twice in the same voting contract). As there’s no way to map nullifier to originating identity commitment, there’s also no way to prevent this double use if the identity commitment has been updated.

On the other hand, we think that web account verifications should have an expiration age similar to how identity docs (passports, driving licences) have an expiration date.

Now with that in mind, we have two scenarios:

1. Web account had NOT been added to the credential registry before it was compromised. In this case, the attacker can verify the web account and add it to the registry and use the credential to prove that they’re human in this period. The real user if he’s able to get access back to the account will have to wait until the verification expires to re-verify the account and add the identity commitment with the correct key.
2. Web account had been added to the credential registry before it was compromised. The attacker will not be able to update the identity commitment until it expires and user has the time to get the access to web account back until the verification expires.

By the way, the exact same logic applies if the user loses their Master Key and need to update it with a new one.

What do you think?

