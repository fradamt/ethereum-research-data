---
source: ethresearch
topic_id: 21772
title: An Enshrined Long-Term Storage (eLTS) L2
author: keyneom
date: "2025-02-18"
category: Uncategorized
tags: [stateless]
url: https://ethresear.ch/t/an-enshrined-long-term-storage-elts-l2/21772
views: 166
likes: 2
posts_count: 1
---

# An Enshrined Long-Term Storage (eLTS) L2

# Enshrined Long-Term Storage (eLTS) L2

---

## 1. Introduction

Ethereum’s promise as the world computer comes with a need for a variety of components. Computers have CPUs, GPUs, RAM, caches, hard drives, etc.  As Ethereum evolves, plans to eliminate state and history from validator duties and instead rely on 3rd parties to fulfill the needs of the network introduce potential weaknesses of centralization and improper influence when the network has nothing to fall back on. In some cases it even provides less than ideal solutions (e.g. trusting external entities to verify contract source code).  The proposed enshrined Long-Term Storage (eLTS) L2 addresses these issues by creating a dedicated storage layer where validators earn ETH by storing Ethereum’s history—ranging from blocks and transactions to state diffs and/or even contract source code or other data. This is intended to be the hard drive of the world computer. This builds on ideas similar to FileCoin’s proof-of-unique-storage and IPFS while incorporating novel mechanisms to ensure data redundancy and persistence, ultimately enhancing the network’s resilience and permissionless participation.

---

## 2. Protocol Overview and Core Goals

The eLTS L2 protocol is designed with the following objectives:

- Permanent Historical Record: Ensure all Ethereum history (blocks, transactions, state diffs) is stored forever.
- Permissionless Onboarding: Allow storage validators to join the network without requiring pre-owned ETH, thereby promoting anonymity and decentralization.
- Redundancy Incentives: Encourage multiple copies of data to improve security while implementing diminishing rewards to avoid waste.
- Robust Data Accessibility: Guarantee reliable data retrieval even if response times are slower, ensuring long-term persistence over speed.

This protocol enshrines long-term, decentralized, and permissionless storage into Ethereum and provides an economic pathway from zero-ETH to full participation on the network without external dependencies, much like Bitcoin’s mining model where energy is traded for BTC.

---

## 3. Storage Validator Lifecycle

### A. Joining as a Storage Validator

- Permissionless Entry:
Validators submit an on-chain transaction taking custody over a chunk of data and providing a proof of unique storage to join the eLTS validator set.

No Upfront Gas Fees: Transaction fees are deducted from what would have been rewards, streamlining entry.
- FOCIL Committee Oversight: Things like FOCIL could help to ensure censorship resistance.

**Data Chunk Selection & Proof:**

- Choosing a Data Chunk: Any validator can select any chunk of data at any time.
- Proof-of-Unique-Storage: Validators submit a proof (akin to FileCoin’s approach) that they uniquely store a chosen chunk.
- Reward Mechanism: Rewards are determined by the scarcity of the data; rarer data yields higher rewards, while common data earns less. If the chunk has not had a proof provided in a long time then it might increase the reward as well.

### B. Ongoing Participation

- Periodic Proofs: Validators can periodically submit proofs of continued storage or be challenged to provide a proof.
- Dynamic Rewards: As the number of copies increases, rewards adjust to maintain an optimal level of redundancy without incurring excessive duplication. We could possibly have storage validators earn small incremental rewards for each chunk they custody for each block that they hold it. Duration they hold it (and therefore their reward) is determined by when they took custody and when they relinquish custody. We don’t actually have to update balances for this since it can just be calculated at the end and they can’t withdraw without providing a valid storage proof anyways. As they earn more rewards they are able to accrue an eth balance that can be used for stake weighted attestations or maybe just FOCIL participation/proposing duties within the network. They can obviously also receive payments for responding to data requests by providing the relevant chunk(s), etc.

### C. Exiting as a Storage Validator

- Graceful Exit Procedure:

Signal Intent: Validators signal their intent to exit via an on-chain request.
- Grace Period & Transition: A grace period allows other validators to assume custody of the data.
- Final Proof Requirement: A final proof of storage must be submitted before withdrawal of rewards. Failure to comply results in slashing.

---

## 4. Fee Mechanisms

The protocol employs a multi-tier fee system to regulate participation and safeguard the network:

- Base Fee for L1 Submissions:
Reflects standard L1 transaction fees, ensuring validator commitments are recorded on-chain.
- Multiple EIP-1559 Type Fee Markets:
Multiple fee markets could exist for separate operations. e.g. taking or relinquishing data custody, which would help prevent sudden data drop-offs since we get a target gas limits for actions. To some extent these fees introduce an auction-like mechanism for claiming custody of a given chunk of dataand can help ensure that new data is stored at the desired replication rate. They also allow for us to constrain the number of validator exits or how much data can have custody relinquished at once (similar to the consensus layer’s limits) ensuring continuity of all data.
Another market could be for submitting storage proofs giving us a mechanism to incentivize ongoing proof submissions but constraining their submission to match the value of their production (i.e. rewards = fees for submitting the tx). This would of course be in addition to the ability to challenge a storage validator where it must also provide a proof (maybe at no reward?). Proofs for chunks that have not been proven in a while could be worth more but ideally not more than what submitting two proofs in half that time would have been worth.
It might be worth it to separate newly entering validators from the other fee markets but it might be better to let them be part of the regular proof submission market.
- Priority Fee/Tip:
Prioritizes transactions during high contention, new validator entries earn no reward. Their reward is instead used for the L1 base fee + the L2 eip 1559 fee (we could call maybe call it the L2 base fee), the remainder of which always goes to the priority fee. I.e. they max bid in order to join the validator set at no reward. This should help to prevent sybil attacks and discourage creating separate validators for no reason.

---

## 5. Economic Open Access

A distinguishing feature of the eLTS L2 is its permissionless economic model:

- No Upfront ETH Requirement:
Unlike traditional staking (which demands 32 ETH), new validators can earn ETH directly through storage activities.
- On-Ramping Mechanism:
Validators accumulate ETH rewards from providing data custody. Over time, they could of course transition to full L1 staking or participate in Ethereum in any other desired manner, fostering a more inclusive and decentralized ecosystem.

This open-access model mirrors the energy-for-BTC exchange in Bitcoin mining that I admittedly have what some have called holy envy for.

---

## 6. Data Types, Queryability, and Resilience Enhancements

### Data to Be Stored

We aim to permanently store key components of Ethereum’s history. Structuring this in a verkle tree(s) (or something with similar properties) would allow for submissions to the L1 with actionable guarantees and potentially partitioning within the L2 itself in a parallelizable way for all operations:

- Blocks & Transactions: The entire ledger history.
- State Diffs: Incremental changes that allow reconstruction of historical states.
- Contract Source Code: Potentially enabling on-chain source code validation for enhanced transparency.
- Additional Metadata: Data used by archive nodes and block explorers to support queryability and analysis or even just any kind of data in general (though we would of course want a separate mechanism for this than supporting it through issuance so people would need to be willing to pay for it like FileCoin)!

### Queryability

Ensuring that stored data is not only preserved but also accessible is crucial:

- Indexing for Portals and Explorers:
The protocol can integrate with existing query systems such as the Portal Network and Ethereum block explorers.
- Supporting Smart Contract Verification:
Validators could store original contract source code, facilitating on-chain source code validation, which strengthens trust in deployed contracts and could even support permissionless addition of ERC20’s to markets that are guaranteed to match certain attributes (like no fee on transfer or having 18 decimals of precision).

### Resilience via Reed Solomon Encoding

- Enhanced Data Redundancy:
Implementing Reed Solomon encoding might be worth it to improve data recovery in the event of partial data loss or when certain validators become unavailable without excessive raw copies of chunks and maybe reduce overall storage overhead.

---

## 7. Challenges and Outstanding Problems

Tons of stuff but I figured I’d at least put the idea out there.

This is intended to not only secure Ethereum’s past but also provide a robust foundation for its future, ensuring that critical data remains accessible, verifiable, and resilient against both technical and economic adversities. I plan on publishing another post on how I believe this system could be paired with statelessness to enable desirable outcomes for Ethereum but all things in due time.

Now that I’ve written this and I’m about to submit, I see that "[my] topic is similar to . . . " [EthStorage: Scaling Ethereum Storage via L2 and DA](https://ethresear.ch/t/ethstorage-scaling-ethereum-storage-via-l2-and-da/14223) so props to them for all they wrote there. I believe there are some similarities there and a decent number of differences (I’m proposing something more akin to the beacon chain where a full node is run but instead of having a validator client node participating on the beacon chain we have a storage client node that can participate on the eLTS L2). Anyways, I know there are plenty of things that I haven’t specified about how this could work but hopefully it is enough to give an idea of how it could work and/or spur some questions. I know there are also plenty of people who are unlikely to like this proposal. Meh, what can you do? If it isn’t able to work for some reason I’ve missed that’d be good to know as well so feel free to let me know! ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12)
