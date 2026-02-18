---
source: ethresearch
topic_id: 21763
title: Post quantum TXs in The Verge
author: adria0
date: "2025-02-17"
category: Execution Layer Research
tags: [post-quantum]
url: https://ethresear.ch/t/post-quantum-txs-in-the-verge/21763
views: 278
likes: 1
posts_count: 1
---

# Post quantum TXs in The Verge

*This note is a collection of ideas about how to use detached signature transaction format that separates signature data from payloads, enabling Ethereum’s shift from ECDSA to post-quantum schemes like Falcon (what is used as an example here). It allows per-address activation of signature methods, emergency fallback, backward compatibility, and initial verification without state queries while aligns with future zk-proof scalability improvements.*

**Motivation**

Ethereum’s transition from ECDSA to post-quantum secure signatures like Falcon requires a flexible and backward-compatible approach. Users should be able to activate signature schemes as needed, having the possibility of a smooth migration path. Also, since it is unknown when Q-day will arrive, an emergency fallback mechanism should be available in case any signature method is compromised (therefore, no paymasters can be active).

There is an ongoing AA native abstraction proposal (EIP-7701) that is well-designed to mitigate DoS attacks, but it’s also a good candidate for handing PQ Tx signatures through its crypto-agility. However, it requires access to the state for the transaction signature to be initially validated. A first-pass transaction verification without requiring state queries or EVM execution is an interesting topic, especially when the underlying signature scheme requires more computation than ECDSA.

Additionally, it is unclear at this moment whether there will be a single signature scheme or multiple options to choose from as a replacement for ECDSA. Instead of modifying all transaction types individually (Legacy, 1559, SETCODE, BLOB, etc.) to support different signature schemes, a detached signature transaction format would allow existing types to be wrapped seamlessly, minimizing disruption to Ethereum’s architecture.

The size of PQ signatures is currently a significant issue (it seems that is hard to go lower that 666 bytes), as it will increase the block size to impractical levels. There are ongoing efforts to build aggregated signatures (hash-based and others like Falcon/LaBRADOR), but with zk-proof-based block validation expected to become a reality in a few years, it is worth considering whether it makes sense to store signatures in blocks or transactions, given that they will be verified within the zk proof. A detached signature scheme would allow these signatures to be removed when clients request block transactions (via RPC or P2P). Of course, this also impacts offline-generated signatures, so it should be generalized to support their transport as well.

Of course, PQ-day will impact so many aspects of the Ethereum protocol (DAS, Groth16-wrapped zk(E)VM L2 and zkDapps, BLS aggregated sigs, P2P Key Exchange) as well as the whole internet, which makes this proposal just an approximation for a partial solution; however, it could be an interesting approach to start finding solutions for the ownership of Ethereum assets.

**ENABLESIG_TX_TYPE**

`ENABLESIG_TX_TYPE,rlp[sig_type,param,nonce,r,s,v]`

Options for `sig_type`,`param`:

- [ECDSA,1] / [ECDSA,0] : enables/disables ECDSA for the address.
- [FALCON,keccak(pk)] / [FALCON,0] : enables/disables FALCON for this address with the specified falcon public key. Falcon public key is large and is sent in the transaction to avoid storing it in the state. Falcon-signed txs must be sent via DETACHEDSIG_TX_TYPE.
- [TAPROOT,root] / [TAPROOT,0] : enables/disables the verification of a signature by using pre-built merkelized transactions. Is expeced the user to introduce some random data to the tree to avoid an attacked guessing transactions.

**DETACHEDSIG_TX_TYPE**

This transaction type is an envelope for detached transactions wrapping existing tx types (`ENABLESIG_TX_TYPE`, `LEGACY_TX_TYPE`, `SETCODE_TX_TYPE`, `BLOB_TX_TYPE`, etc…).

Note that these existing types must be ideally rewritten to do not transport the current ECDSA signature, but we still keep it in this document for two reasons:

- It allows to build composite signatures (see section composite over hybrid)
- It allows to unique identify the transactionId, because the detacched signature itself is not going to be part of the TransactionId. Note that in the case that only Falcon is activates, e.g. enveloped ECDSA signature must contain the hash of the dettached signature in order to somehow link it. Anyway, this is an area that needs more work.

`DETACHEDSIG_TX_TYPE,rlp[sig_type, rlp_encoded_tx, signature]`

where

- if sig_type is FALCON, signature contains Falcon signature in key recovery mode (see Section 3.12 of Falcon paper).
- if sig_type is TAPROOT then signature contains a merkle path from the root to the hash of rlp_encoded_tx.
- if sig_type is pqSNARK then signature contains a stark proof of merkle tree transaction of taproot.

**Notes**

*Composite vs hybrid signatures*

Should txs be double-signed and then double-verified (like PGP draft-wusseler-openpgp-pqc-00 or X509 draft-ounsworth-pq-composite-sigs) or should be the PQ signature be alternative option (like ITU-T X509 Hybrid Catalist extensions)?

Having hybrid schemas is a controversial topic from regulatory bodies: Requiered for France and Germany, allowed in EU and ETSI, forbbiden in US, UK and Canada) also and it seems some kind of open problem from the community.

In this document, we do not condider composite signatures, since it’s a pre-conditon that tx signatures will be something temporal for miner block validaton and thrown away due Zk block validation.

Anyway if any user wants to be able to verify both signatures, it seems that this should factible by adding a AA ECDSA signature verification (e.g. via EIP7702 designed delegator, via EIP4337 in a very natural way or maybe with the forthcomming EIP7701)

*Massive PoP for Q-day procrastinators*

The vitaik proposal of proof-of-possesion of wallet seed ([How to hard-fork to save most users' funds in a quantum emergency](https://ethresear.ch/t/how-to-hard-fork-to-save-most-users-funds-in-a-quantum-emergency/18901)), is an ideal proposal for quantum procrastinators and can be added to this proposal in order to be activated via `sig_type` is `pqSNARK`, but unfortunately does not cover vanity addresses or HD wallets.

Additionally user can generate an special TAPROOT leaf (like `0xc0de fade 0ff`) to easely prove the possesion of a key.

In case of such scenarios, providing an already existing pqSNARK rollup (like StarkWare that does not uses EC for final ethereum verification) or specially-crafted proofs could be a nice way to minimize the amount of gas spent per block in a massive migration.

*Offline signatures*

Probably, it is going to be the same problem with offline signatures, where signatures will be transported via Tx calldata and will increase their size, thereby incrementing the block size.

Creating a proposal for calldata detached signatures that are not going to be transported in transactions is an interesting direction.

For instance, DETACHEDSIG_TX_TYPE could be expanded to temporarily transport an additional list of signatures that will not be transported after the zk block proof is generated. A special EVM opcode, similar to ECRECOVER, called FALCONRECOVER(<hash|data>, signature_no) will be able to recover the public key of the specified signature sent as dettached data in the tx.

**Examples of operative scenarios**

*Happy path, soft-migration scenario, link ecdsa and falcon while we can*

- User activates FALCON signature.
- User tests FALCON signature.
- User deactivates ECDSA signature.
- Everybody migrated to Falcon? maybe not procrastinators.
- Q-day, fork ECDSA is disabled

*Quantum procrastinators. Users that do not want to activate FALCON until Q-day happens.*

- User builds a TAPROOT with a transaction that disables ECDSA and another that activates FALCON.
- Q-day, fork, ECDSA is disabled.
- User submits TAPROOT transactions to enable ECDSA and to activate FALCON.

*Unexpected Q-day scenario with ECDSA and FALCON compromised*

- User builds a special leaf called 0xc0de fade 0ff in the TAPROOT.
- Q-day, fork, ECDSA and FALCON are disabled.
- EF selects a new signature algorithm (like SPHINCS+) and forks.
- User sends a new ENABLESIG_TX_TYPE, [SPHINCS, pqSTARK_taproot_proof_mt_0xcafe...caffe, keccak(SPHINCS_pk)] where pqSTARK has keccak(SPHINCS_pk) as a public input.

The pqSTARK could contain multiple proofs for a quicker migration.

*Urgent actions on Q-day*

- User builds a set of transactions to be executed in case of Q-day (paying salaries, pausing some contracts, etc.) and builds a TAPROOT, setting it via transaction.
- Q-day, fork, ECDSA and FALCON are disabled.
- User sends pre-authorized transactions

**Notable links**

- Tasklist for post-quantum ETH - #8 by vbuterin
- So you wanna Post-Quantum Ethereum transaction signature
and Falcon as an Ethereum Transaction Signature: The Good, the Bad, and the Gnarly
- https://www.nics.uma.es/wp-content/papers/agudo2024cbt.pdf
- Shai Wyborski_Procrastinators-PQCSM.pdf - Google Drive
- https://eprint.iacr.org/2025/055.pdf
- Aggregating Falcon Signatures with LaBRADOR
- https://www.youtube.com/watch?v=yeTNeiVl0BM
