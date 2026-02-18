---
source: ethresearch
topic_id: 23084
title: MEVless protocol, the way to anti-MEV
author: Lawliet-Chan
date: "2025-09-21"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/mevless-protocol-the-way-to-anti-mev/23084
views: 374
likes: 2
posts_count: 3
---

# MEVless protocol, the way to anti-MEV

# MEVless Protocol

extends: [A trustless on-chain anti-MEV solution for Layer2/3](https://ethresear.ch/t/a-trustless-on-chain-anti-mev-solution-for-layer2-3/20260)

### Prerequisites

**MEVless applicable attack scenarios**:

- Sandwich attacks
- Front-running attacks

**MEVless applicable chains**:

Here, **I do not recommend using the MEVless protocol directly at the L1 public chain level** (especially general-purpose blockchains like ETH and Solana), because MEVless requires targeted modifications to the blocks themselves, which are specifically designed to resist MEV and may not be suitable for other business types (especially those that don’t need MEV resistance). The author recommends placing MEVless on dedicated DeFi application chains or L2s, and then returning to ETH L1 for settlement.

### Principle

The principle of MEVless lies in constraining miners’ behavior in transaction ordering. Our approach is to prevent miners from seeing specific transaction content during ordering. Transactions are ordered without miners seeing the transaction content, so even miners cannot perform MEV attacks since they don’t know the specific transaction content. After ordering, the sequence needs to be published to the public network so other nodes and users are informed. At this point, the transaction order is finalized and included in the block, so when specific transaction content is submitted later, it will be executed according to this consensus order, with no room for MEV operations.

We divide on-chain blocks into two types:

- Ordering blocks, which only complete three things: receiving transaction hashes, deducting user prepayments, and providing transaction ordering commitments. The interval between sequenced blocks can be shorter than that between execution blocks.
- Execution blocks, which are no different from ordinary blocks, only need to execute transactions according to the order committed in the previous ordering block

These two types of blocks are produced alternately. For example, after the genesis block, blocks with odd block heights are ordering blocks, and blocks with even block heights are execution blocks.

### Process

[![MEVless](https://ethresear.ch/uploads/default/optimized/3X/c/4/c4f1fd7b53ad83da39323f1eb918b2c91effaf76_2_283x500.png)MEVless466×822 14.2 KB](https://ethresear.ch/uploads/default/c4f1fd7b53ad83da39323f1eb918b2c91effaf76)

1. Block N (ordering block) begins block production
2. Users send transaction hashes to the chain and pay a certain prepayment. The prepayment consists of two parts:
(1) Gas fee for transaction hash: Used for storage of transaction hash and computation fees during ordering.  This fee is generally fixed and mandatory.
(2) Additional tip: Extra fee paid by users to ensure their transaction can be ordered as early as possible. This amount is not fixed and can be zero
3. After the chain nodes receive transaction hashes, they will complete the following steps:

- Check if the transaction account has sufficient funds to pay the prepayment
- Sort transaction hashes from high to low based on prepayment amount
- Deduct the prepayment amount from the transaction account
- Store the sorted transaction order as a commitment in the block and publish it to the P2P network

 After users subscribe and query to see the ordering sequence number of their transaction hash committed on-chain, they send specific transaction content to the chain and DA (DA is optional)
- Block N+1 (execution block) begins block production
- After chain nodes receive transaction content, they will complete the following steps:
- Pull transaction content from DA (if all txHashes committed to ordering in the previous block have corresponding transaction content, skip this step)
- Check if the transaction content matches the previously committed ordering txHash, discard if not matching
- Execute transactions according to the previously committed order

This process continues cyclically.

### Role of DA (Optional)

In this scheme, it may happen that after transaction content is sent to the chain, miners see that the transaction is profitable and may maliciously withhold the transaction to prevent it from being included on-chain, then wait for users to resend the same transaction for attack. At this time, not only will users’ transaction profits still be eroded, but they will also waste a prepayment for the previously sent transaction hash.

Therefore, we need DA (such as ETH Blob) to ensure that transactions sent by users will definitely be included on-chain. This way, even if block-producing nodes maliciously withhold the transaction, other verification nodes and full nodes can still receive the transaction content and execute the transaction in subsequent block production processes. This forces block-producing nodes to include the transaction in their blocks to prevent state inconsistency with other nodes.

In this process, DA provides an additional layer of protection for users and is not mandatory. If users feel that the transaction has been sufficiently propagated to enough full nodes in the P2P network, they can choose not to use DA. Introducing DA can also prevent miners on the chain from jointly monopolizing and withholding user transactions.

### Advantages

1. Compared to encrypted mempools, the MEVless solution has lower overhead, requiring no decryption operations that are energy-intensive for CPU and memory. MEVless only orders transaction hashes first, with a hash being only 32 bytes long (or even shorter). After ordering is complete, propagation places minimal burden on network bandwidth.

2. Compared to PBS, MEVless constrains from the source of MEV attacks - transaction ordering rights - by blocking attackers’ access to transaction information before ordering, eliminating the prerequisite for attackers to perform MEV attacks.

3. Conducive to decentralized execution and verifiable results. All MEV resistance methods and steps are hardcoded at the code level. As long as full nodes execute according to this code, the results are deterministic, making it difficult to perform MEV attacks in black box operations.

4. The difference between the privacy memory pool node and the privacy memory pool node is that the privacy memory pool will not publish the promised transaction order to the entire network nodes for consensus before knowing the specific transaction content, while MEVless will publish the promised transaction order to the entire network and let each full node write it into the block after consensus to ensure that the transaction will be executed in the promised order.

## Replies

**Lawliet-Chan** (2025-09-22):

### Speculative MEV

In the previous discussion, we covered ordinary MEV attacks, but when attackers cannot see specific transaction content and cannot target specific transactions, they may adopt another attack method: speculative MEV attacks.

This attack method is specifically manifested as: in MEVless, attackers can pre-position a transaction and submit the transaction hash to the chain. When the execution block begins and everyone submits transaction content, attackers can judge and calculate whether they have attack profits based on the transaction content submitted by other users. If there are profits, they submit their transaction content; if not, they choose to refuse to submit their transaction content, achieving sandwich attacks.

This approach is difficult to succeed in the MEVless protocol because speculation requires costs. When attackers find it unprofitable and choose to abandon submitting their transaction content, the prepayment they paid when submitting the txHash earlier becomes wasted. The more attackers want their transactions to be ranked higher in the ordering, the greater the prepayment cost they need.

**Then, some readers might wonder: if block-producing nodes themselves perform MEV attacks, then this prepayment is essentially paying themselves, completely offsetting the attack cost. In this case, how should it be solved?**

### Consensus Layer Optimization

Indeed, when block-producing nodes themselves perform MEV attacks, this prepayment will be covered by their own block rewards, so there will be no waste of attack costs. Our approach to weakening this speculative method is: making it impossible for miners to predict whether the next block will be produced by them, thus dramatically increasing their speculative costs. For this purpose, We need to make the following design at the consensus layer:

- Access consensus: Proof of Burn L1-token, people must burn some L1 tokens (ETH/USDT/USDC) on L1 to gain the right to join the miner group.
- Block production consensus: VDF based on L1 hash, we use the hash of the latest block on ETH L1 as input, generate random output values with VDF, and compare all miners’ output values. The node with the maximum value of (output value * burned L1 token amount) will become the block-producing node for this round.
- Final consensus: Upload the blocks produced in the above steps to ETH L1 every 3 ETH slots as a cycle, and select the fork with the maximum value of (output value * burned L1 token amount) as the finalized branch. Once finalized on ETH, it cannot be rolled back.

Moreover, this consensus design has better MEV resistance as decentralization increases, because the more miners there are, the harder it is for each miner node to predict whether they will be the next block-producing node, and the higher their risk of speculative MEV.

---

**Lawliet-Chan** (2025-09-29):

[MEVless protocol, the way to anti-MEV - #2 by Lawliet-Chan](https://ethresear.ch/t/mevless-protocol-the-way-to-anti-mev/23084/2)  is an  addtional post  just for clarification and is not considered as part of the official content of MEVless.

