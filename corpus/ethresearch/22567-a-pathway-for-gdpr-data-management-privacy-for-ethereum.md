---
source: ethresearch
topic_id: 22567
title: A pathway for GDPR Data Management & Privacy for Ethereum
author: EugeRe
date: "2025-06-09"
category: Privacy
tags: [zk-roll-up, data-availability, transaction-privacy, pet]
url: https://ethresear.ch/t/a-pathway-for-gdpr-data-management-privacy-for-ethereum/22567
views: 938
likes: 5
posts_count: 7
---

# A pathway for GDPR Data Management & Privacy for Ethereum

**Abstract**

Public permissionless chains like Ethereum face a pressing challenge: reconciling immutability and decentralization with the GDPR’s data-protection rules. Ethereum’s move to a modular architecture enhanced by privacy-preserving technologies offers a way to bake GDPR principles into the protocol itself. By pushing personal data to the edges (wallets and dApps), using off-chain storage with metadata-erasure, and splitting roles cryptographically, we can focus GDPR controller duties on a small set of entities, while the wider network becomes mere processors or falls out of scope.

To achieve GDPR compliance in permissionless blockchain environments, we propose a harmonized set of data management and processing practices. These practices extend the previously developed GDPR compliance roadmap, incorporating the technical innovations discussed and focusing on clear role allocation and data anonymization. The overarching goal is to allocate data controllership to the appropriate application layer actors (those who decide to process personal data), while ensuring that lower-level infrastructure (execution and consensus clients) only handle data that has been rendered anonymous or at least pseudonymous. In essence, personal data should be transformed or abstracted before it reaches the blockchain execution layer, and certainly before it propagates through the consensus layer.

At the same time, we must preserve the decentralized nature and security of the blockchain.

As European Blockchain Association we drafted a document to inform the topic and here you may find the full document for reading: [European Blockchain Association GDPR Consultation Reply (EDPB).pdf](/uploads/short-url/3WVHXZz5GVX8077K8Y1cAvuSX8C.pdf) (3.1 MB) that I summarized a small post here for those who may be interested:

**1 GDPR Principles become friction points Permissionless Context**

- Controller vs. Processor: Any actor who determines the purposes and means of on-chain personal data (dApp developers, node operators, validators) is a controller.
- Pseudonymization vs. Anonymization: Hashing or encryption alone does not anonymize if re-identification remains possible. Only irreversibly unlinkable data falls outside the GDPR.
- Right to Erasure: Immutable ledgers cannot delete data; controllers must keep personal data off-chain and store only pointers on-chain. Deleting the off-chain record “unlinks” the on-chain pointer.
- Joint Controllership: In permissionless settings, every node risks controller status. Practical mitigation includes protocol-level role splits or voluntary codes of conduct to limit who truly controls personal data.

**2 Privacy-Enhancing Technical Innovations can help to reduce the burden for data management in permissionless space**

- Proto-Danksharding (EIP-4844): Blobs of transaction data live off-chain for about 18 days, then prune to KZG commitments—enforcing storage limitation and data minimization.
- zk-SNARK Execution: Validators verify succinct proofs instead of raw transactions—“verify, don’t see”—dramatically reducing on-chain personal data exposure.
- Fully Homomorphic Encryption & TEEs: Execute on encrypted data or inside hardware enclaves so no node ever sees plaintext—meeting GDPR’s “appropriate technical measures.”
- Multi-Party Computation (MPC): Split decryption or signing keys among multiple parties so no single actor can reassemble personally identifiable data.
- Proposer-Builder Separation (PBS) & Attester-Proposer Separation (APS): Protocol-enforced splits concentrate data-viewing power in block builders, while proposers and attesters handle only commitments or proofs.
- Peer Data Availability Sampling (PeerDAS): Erasure-coded shards stored briefly and randomly by nodes; each node holds only unintelligible fragments that automatically expire.

**3.Modular Networks  Determine a Layered Role Attribution in Ethereum’s Modular Architecture**

Ethereum now splits transaction processing across three layers, each with distinct GDPR implications:

**Execution Layer:** Receives signed transactions, simulates contract execution, and feeds the mempool or block builders.

- Actors:

Wallets/dApp front-ends choose what data to submit (controllers).
- RPC nodes/mempool relays propagate transactions; under privacy enhancements they relay only encrypted or hashed data (processors).
- Block builders/sequencers assemble and order transactions; with PBS they handle blinded bundles (processors).
- What PET help to achieve in that context?

Before: Every execution node saw full transaction payloads and could be a controller.
- After: Transactions are encrypted or blinded on submission; relays and builders never see plaintext.

**Consensus Layer:** Orders and finalizes blocks via Proof-of-Stake voting.

- Actors:

Proposers select blocks; with PBS they choose only commitments without reading transactions (neutral verifiers).
- Attesters (validators) vote on block validity; with zk execution they verify proofs instead of raw data (out of GDPR scope).

What PET help to achieve in that context?

- Before: All validators processed every transaction and acted as joint controllers.
- After: Validators handle only proofs and commitments, no longer processing personal data.

**Data Availability Layer** : Stores large payloads (e.g., rollup blobs) for availability proofs.

- Actors:

Full archival nodes store everything indefinitely (controllers).
- PeerDAS sampling nodes each hold a small, erasure-coded fragment for a limited time (processors or out of scope).
- What PET help to achieve in that context:

Before: Archival nodes held full data and were controllers.
- After: Sampling nodes store only anonymous fragments that expire automatically, meeting data-minimization and storage-limitation.

[![image](https://ethresear.ch/uploads/default/optimized/3X/0/f/0f529d00924deebb641fe57bb62f0458daee1b5d_2_690x388.png)image1004×565 63.9 KB](https://ethresear.ch/uploads/default/0f529d00924deebb641fe57bb62f0458daee1b5d)

**4  An Harmonized GDPR Compliance Framework**

| Participant | Before | After |
| --- | --- | --- |
| Wallet / Client | Controller (publishes clear data, logs) | Local controller; publishes only encrypted/pseudonymous data |
| dApp Provider / Exchange | Controller (on-chain PII + off-chain DB) | Controller (off-chain PII only; on-chain: hashes or encrypted) |
| RPC Endpoint | Controller if logging; else undefined | Processor (non-logging relay of encrypted transactions) |
| Execution Client / Mempool | Controller (gossips full payloads) | Processor (relays only blinded or hashed payloads) |
| Block Builder / Sequencer | Controller (orders raw txs, extracts MEV) | Processor (packages blinded bundles; no access to PII) |
| Validator (Proposer/Attester) | Joint Controller (finalizes PII) | Neutral verifier (only proofs/commitments under PBS + zk) |
| Data Availability Node | Controller (stores full shards) | Processor (stores only anonymous fragments; ephemeral) |

**Personal Concluding thoughts**

Ethereum’s modular roadmap shows that decentralization and data protection can co-evolve. By concentrating controller duties at the edges and transforming most network participants into processors of pseudonymous or anonymous data, Ethereum can align with GDPR without sacrificing its permissionless vision. This path depends on widespread adoption of privacy-enhancing technologies and clear, collaborative governance but it is a realistic blueprint for public blockchains that protect individual rights.

## Replies

**ivanmmurciaua** (2025-06-09):

Hey, better than others proposals seen here. The main contradiction of Europe’s bureaucrats is that the EDPB proposes data anonymity but conflicts with other (silly) anti-money laundering laws. How does your proposal solve this?

My take is forget Europe’s overregulation path. Ethereum must follow the ethos that brought it here.

---

**EugeRe** (2025-06-09):

Thanks [@ivanmmurciaua](/u/ivanmmurciaua) for your interest and message! To my knowledge AML or any other public interest data required should be available for request. So in that context I can see a scenario where in the app layer, app providers they host off-chain environments where they collect such data from user with user consent. At protocol layer I can see a solution like alt DA that use privacy pools to determine KYT proof for batches of transactions.

---

**ivanmmurciaua** (2025-06-09):

And doesn’t this go against the fundamental principles recently underlined by the EF?

---

**EugeRe** (2025-06-09):

I do not see any principle violation; the decision to implement this feature at protocol level is anyway community driven. Any implementation at app level is client driven so it falls under different logics.

This example actually balances principles implementation (eg. AML). Actually, we preserve inclusion and permissionless access while leaving the bad guys out of the door. But this is my personal opinion.

---

**itsnighthawk338** (2025-06-10):

Palantir Technologies has a product “Palantir Foundry for Crypto” since september 2021. Integrating AI with crypto.

You think maybe this product can be used?

---

**EugeRe** (2025-06-10):

Hey [@itsnighthawk338](/u/itsnighthawk338) I did not know about the product you are describing. Happy to give it a look if you can share any repo or material about it.

