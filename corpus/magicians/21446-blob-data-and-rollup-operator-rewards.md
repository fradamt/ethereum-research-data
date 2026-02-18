---
source: magicians
topic_id: 21446
title: BLOB Data and Rollup Operator Rewards
author: sopia19910
date: "2024-10-23"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/blob-data-and-rollup-operator-rewards/21446
views: 105
likes: 5
posts_count: 3
---

# BLOB Data and Rollup Operator Rewards

---

## title:
description: ), Khajiev Nizomjon()>
discussions-to:
status: Draft
type:
category:  # Only required for Standards Track. Otherwise, remove this field.
created: <2024-10-23>
requires: <EIP number(s)> # Only required when you reference an EIP in the Specification section. Otherwise, remove this field.

## Abstract

This proposal introduces a way to reward L2 Rollup operators for

uploading block data to L1 (the Ethereum mainnet). It reduces the gas

cost burden for operators. It strengthens the sustainability of rollup

operations. It promotes network decentralization.

## Motivation

1. There is a cost burden for L2 operators.

 An operator uploads L2 block data to L1. It pays gas fees but has no direct way to recoup them.
2. The higher the cost, the more likely a few large operators dominate, causing censorship risk and centralization.
3. There is data availability and blob usage.

 An operator must regularly upload block data to ensure that L2 data remains available.
4. A reward mechanism incentivizes the operator to use blob space effectively. It increases overall scalability.
5. There is potential for greater network scalability and
decentralization.

 A reward scheme encourages more rollup operators to enter, which fosters competition and reduces rollup fees.
6. Multiple operators submitting blocks in parallel can reduce L1 transaction load and maximize overall network capacity.

## Specification

### 1) Block Submission and Reward Flow

**L2 Block Creation and Data Aggregation**

- The operator aggregates L2 transactions and creates a block. It converts the block into blob data (blobTx).
- It may include a compressed state root, a ZK proof, or a fraud-proof payload.
- It uses high compression to get higher rewards.

**Submission to L1**

- The block submitter sends the blobTx to a specialized Rollup contract on L1 (for example, RollupBlockSubmitter).
- The data is committed on L1 through a transaction.
- The msg.sender of that L1 transaction identifies the submitter.

**Challenge Period and Verification**

- An Optimistic Rollup finalizes the block after its fraud-proof challenge period ends.
- A ZK Rollup finalizes the block immediately when the ZK proof is verified.
- A detected fraud triggers penalties against the submitter.

**Reward Distribution**

- The rollup contract pays ETH to the block submitter if the block is verified without issues.
- It considers metrics such as data size, network congestion, and compression efficiency.
- It can grant extra incentives if data remains available on-chain for a required duration (e.g. with EIP-4844 blobs).

### 2) How L1 Identifies the L2 Block Submitter

- L1 does not store the operator’s identity explicitly, but it checks the transaction’s msg.sender.
- A rollup contract logs events so that off-chain analyzers can track who submitted each block.
- A mapping can store the block hash and operator address, like in this

```auto
mapping(bytes32 => address) public rollupProposers;

function submitRollup(bytes32 _blobHash) external {
    rollupProposers[_blobHash] = msg.sender;
    emit RollupSubmitted(msg.sender, _blobHash, block.timestamp);
}
```

### 3) Ways to Use L2 Block Submitter Information

1. Reward Distribution

It grants rewards to the valid block submitter after the block passes all checks.
2. Verification and Fraud Proofs

A malicious operator faces blacklisting or slashing if fraud is proven.
3. Extra Incentives for Honest Submitters

It tracks submission history. It provides higher rewards to trustworthy operators who consistently submit correct blocks.

###

###

### 4) Reward Calculation Criteria

1. Blob Size

 Submitting more data (thus more L2 transactions) increases potential reward.
2. The system imposes a minimum of valid transactions to block trivial spam.
3. Network Congestion

Higher L1 congestion raises gas costs, so the reward can scale up to offset the operator’s expenses.
4. Compression Efficiency

 Fewer bytes for the same number of transactions leads to bonus payments.
5. For instance:

![20250303_153454](https://ethereum-magicians.org/uploads/default/original/2X/4/4c93350a6466468db3173c7b7b44f9c4881b1804.png)

```
  A higher ratio results in greater rewards.
```

1. Data Availability Period

EIP-4844 blobs stay on-chain for around 2–3 weeks. The operator can earn extra rewards if no challenge arises during that period.

### 5) Reward Delivery Methods

1. Smart Contract–Based Reward

 The rollup contract on L1 tracks submitters. It can directly send ETH to them once a block is finalized, or allow them to call claimReward().
2. The funds can come from a dedicated pool, funded by rollup fees or other means.
3. EVM Opcode–Based Reward

 A new opcode (e.g. OP_ROLLUP_REWARD) can trigger automatic ETH transfers when a blobTx is accepted.
4. It requires a protocol-level change (a hard fork), so it is more difficult to implement and less flexible than the contract-based model.

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

## Rationale

1. Ensures Operator Sustainability

An operator covers gas fees on L1. A reward allows the operator to recoup part of that cost and remain profitable, sustaining rollup operations.
2. Boosts Data Availability and Efficiency

Operators aim for better compression and effective blob usage to earn higher rewards. This approach improves the entire network’s data efficiency.
3. Lowers L2 Transaction Costs

A reimbursed operator can reduce L2 fees for users. It makes L2 adoption more attractive.

## Security Considerations

1. Reward Only after Proper Verification

 The system waits for fraud-proof or ZK-proof validation before issuing rewards.
2. Wrongful submissions get no rewards and can be penalized (e.g. slashing or blacklisting).
3. Spam Mitigation

 The system sets a minimum transaction threshold or a minimum state update to disincentivize empty blob submissions.
4. It keeps rewards below the raw cost for non-useful data, deterring spam attempts.
5. Operator Trust

 The system can require stake deposits from operators or vary rewards by past performance.
6. It can track multiple addresses tied to the same entity to prevent Sybil attacks.

## Backwards Compatibility

- This proposal targets EIP-4844 (Proto-Danksharding) for blob transactions.
- It can also work with pre-EIP-4844 calldata, though data storage costs are higher there.
- A smart contract–based reward system does not conflict with existing Ethereum protocol rules.
- EIP-1559, EIP-4337, or other improvements do not interfere with this scheme. Existing rollups (Optimism, Arbitrum, zkSync, etc.) can adopt it with minimal changes.

## Security Considerations

The reward mechanism must be based on accurate verification, with clear rules to prevent fraudulent activity. Rollup operators submitting incorrect data should not receive rewards, and the reliability and accuracy of the data must be ensured.

Needs discussion.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**abcoathup** (2024-10-24):

I don’t understand the need for a reward mechanism for rollups to use blobs.

Rollups moved to using blobs as they are generally cheaper than calldata.


      ![](https://www.growthepie.com/favicon-32x32.png)

      [growthepie.com](https://www.growthepie.com/economics)



    ![](https://api.growthepie.com/v1/og_images/economics.png)

###



Explore protocol revenue, fees, and profit across Ethereum and its scaling layers. Analyze network health through economic metrics and profit margins.











      ![](https://ethereum-magicians.org/uploads/default/original/2X/3/3661dc3b06665389aae183675b52e4aa22a43729.png)

      [Rollup.wtf](https://rollup.wtf/)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/6/646641172fdba3bd3b55776d0e25fc6db3061527_2_690x361.png)

###



real-time rollups performance - built by conduit.xyz










There also doesn’t appear to be a shortage of upcoming rollups


      ![](https://l2beat.com/static/icon.c58a8403.svg)

      [L2BEAT](https://l2beat.com/scaling/upcoming)



    ![](https://l2beat.com/static/meta-images/scaling/upcoming/opengraph-image.6f48972b.png)

###



Discover upcoming Ethereum scaling solutions before they launch.

---

**sopia19910** (2024-10-24):

Hello,

Ethereum has adopted layer technology, where L2 is connected to the Ethereum blockchain with finality at lower fees. This means that L2 blocks are also recognized as part of the Ethereum blockchain.

In other words, Layer 2 is part of the Ethereum blockchain, and I believe that this scalability should extend not only to blocks but also to validators and the reward system. However, the current focus is solely on block expansion, which has led to the perception that Ethereum is becoming centralized.

Therefore, I believe that if the validator and reward systems are also expanded, Ethereum would not be considered centralized.

To address this issue, our team has made a proposal, and we plan to continue suggesting specific code modifications to support this.

To clarify what we are proposing: ultimately, we are suggesting not just providing rewards to operators who perform rollups, but also creating a system where the consensus algorithm of L2 chains interacts with L1 and receives rewards based on that interaction. We will further elaborate on this in more detail.

