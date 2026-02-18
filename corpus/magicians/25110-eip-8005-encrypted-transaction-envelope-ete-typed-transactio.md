---
source: magicians
topic_id: 25110
title: "EIP-8005: Encrypted Transaction Envelope (ETE) Typed Transaction"
author: lengyeltyler
date: "2025-08-15"
category: EIPs > EIPs core
tags: [privacy, mempool, zero-knowledge]
url: https://ethereum-magicians.org/t/eip-8005-encrypted-transaction-envelope-ete-typed-transaction/25110
views: 193
likes: 6
posts_count: 6
---

# EIP-8005: Encrypted Transaction Envelope (ETE) Typed Transaction

This thread is for discussion of EIP-8005: Encrypted Transaction Envelope (ETE) Typed Transaction.

ETE defines a new EIP-2718 typed transaction carrying an AEAD-encrypted payload and a zero-knowledge proof, enabling mempool-private transactions with pre-inclusion confidentiality and policy enforcement.

Builders and proposers who opt in can decrypt and verify before inclusion, then convert the payload into a standard EIP-1559 transaction for execution.

Feedback is sought on serialization, proof constraints, mempool policy, and integration with existing client/mempool rules.

---

#### Update Log

- 2025-08-14: Discussion thread created for EIP-8005 (ETE).
- 2025-08-14: Initial draft prepared for PR, awaiting number assignment
- 2025-08-15: Initial EIP PR opened
- 2025-08-15: EIP# 8005 assigned
- 2025-08-20: Branch cleaned and pushed to GitHub for EIP editors to review

---

#### External Reviews

*No formal reviews received yet (as of 2025-08-20)*

---

#### Outstanding Issues

- 2025-08-14: Normative serialization — finalize exact RLP field ordering, lengths, and error cases for malformed header/ciphertext/proof.
- 2025-08-14: Size caps — propose concrete MAX_CIPHERTEXT_BYTES and MAX_PROOF_BYTES values and rationale (DoS considerations).
- 2025-08-14: Proof constraints — specify minimum required statements (well-formedness, policy binding, nonce uniqueness) and recommended optional statements (anti-spam PRF tag).
- 2025-08-14: Mempool policy — define replacement/conflict rules, TTL, and propagation guidance for opaque payloads (alignment with 1559 mempool rules).
- 2025-08-14: Replay protection — make domain separation over chainId and toCommitment fully normative, with test vectors.
- 2025-08-14: Viewing key discovery — tighten vkLocator format and minimal resolver requirements; consider carving out a companion “VKReg” standard or referencing an existing registry pattern.
- 2025-08-14: Builder/proposer workflow — specify MUST/SHOULD steps for decryption, proof verification, and transformation into a 1559 transaction; clarify failure modes.
- 2025-08-14: Compatibility — document interactions with EIP-2930 access lists (inside ciphertext vs outer envelope), EIP-7702, PBS/MEV-Boost flows, and L2 adoption notes.
- 2025-08-14: Security analysis — expand DoS/censorship/privacy sections and include concrete mitigations and parameter recommendations.

---

#### Feedback Requested

- Recommended field ordering and encoding for header and ciphertext
- Optimal size caps for ciphertext and proof to balance DoS resistance and flexibility
- Standardizing vkLocator format and registry patterns
- Alignment with EIP-1559 replacement rules and EIP-2930 access list handling

## Replies

**pepae** (2025-08-15):

Very cool and this would be highly complementary/compatible with our (Shutter) encrypted mempool efforts together with Gnosis and Nethermind: [The Road Towards a Distributed Encrypted Mempool on Ethereum - mev - Ethereum Research](https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717)

And live deployment on Gnosis Chain: [Shutterized Gnosis Chain is Live - Gnosis](https://www.gnosis.io/blog/shutterized-gnosis-chain-is-live)

Would love to touch base on this and whether there’s some way to collaborate!

---

**lengyeltyler** (2025-08-15):

I’d love to!

There is another EIP that I’m hoping to submit today that focuses on how the verification keys are being stored. The core difference between Shutter and 8005 is 8005 doesn’t rely on human trust where “Keyper” or a “Validator” do.

Also, in Shutter the finalized transactions are public, where EIP-8005 allows the transaction to remain private indefinitely or be revealed selectively, depending on user intent.

The goal is to make 8005 chain agnostic, so as long as the chain is EVM compatible, wallets can essentially “op-in” or “op-out” of this transaction type.

---

**pepae** (2025-08-18):

Sounds awesome! So which/whose key is used to encrypt?

I can’t dm you on twitter, want to dm me so we can set up a call? https://x.com/bezzenberger

---

**lengyeltyler** (2025-08-18):

it will have to be the users key used in order to encrypt.

and i will shoot you a DM!

---

**pepae** (2025-08-19):

Interesting, so the one issue with that is the free option problem present when users hold their own decryption keys because they can choose not to decrypt (e.g., if the transaction fails to yield profit), they effectively gain a “free option” to abort execution, undermining the reliability of encrypted-transaction systems. see point 5 here: blog.shutter.network/on-the-limits-of-encrypted-mempools-a-response-to-a16z-cryptos-analysts/

But we also think that there should be a general encrypted mempool interface, which is agnostic about how/who generates the keys, so user key could also be one option, alongside other options, e.g. threshold encryption, TEE, VDF.

Let’s have a chat in dm, looking forward to it!

