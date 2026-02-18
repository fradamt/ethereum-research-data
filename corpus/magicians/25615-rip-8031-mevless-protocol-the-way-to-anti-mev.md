---
source: magicians
topic_id: 25615
title: "RIP-8031: MEVless protocol, the way to anti-MEV"
author: Lawliet-Chan
date: "2025-09-29"
category: RIPs
tags: [mev]
url: https://ethereum-magicians.org/t/rip-8031-mevless-protocol-the-way-to-anti-mev/25615
views: 244
likes: 3
posts_count: 7
---

# RIP-8031: MEVless protocol, the way to anti-MEV

# MEVless Protocol

extends: [A trustless on-chain anti-MEV solution for Layer2/3](https://ethresear.ch/t/a-trustless-on-chain-anti-mev-solution-for-layer2-3/20260)

PR：[Add RIP-8031: MEVless Protocol - A Solution to MEV Attacks For L2 by Lawliet-Chan · Pull Request #75 · ethereum/RIPs · GitHub](https://github.com/ethereum/RIPs/pull/75)

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

[![MEVless](https://ethereum-magicians.org/uploads/default/optimized/3X/d/5/d5b6171a2bcc6c9aa475cced27bcc85e0863f5b6_2_283x500.png)MEVless466×822 64.6 KB](https://ethereum-magicians.org/uploads/default/d5b6171a2bcc6c9aa475cced27bcc85e0863f5b6)

1. Block N (ordering block) begins block production
2. Users send transaction hashes to the chain and pay a certain prepayment. The prepayment consists of two parts:
(1) Gas fee for transaction hash: Used for storage of transaction hash and computation fees during ordering. This fee is generally fixed and mandatory.
(2) Additional tip: Extra fee paid by users to ensure their transaction can be ordered as early as possible. This amount is not fixed and can be zero
3. After the chain nodes receive transaction hashes, they will complete the following steps:

- Check if the transaction account has sufficient funds to pay the prepayment
- Sort transaction hashes from high to low based on prepayment amount
- Deduct the prepayment amount from the transaction account
- Store the sorted transaction order as a commitment in the block and publish it to the P2P network
4. After users subscribe and query to see the ordering sequence number of their transaction hash committed on-chain, they send specific transaction content (including the remaining gasfee) to the chain and DA (DA is optional)
5. Block N+1 (execution block) begins block production
6. After chain nodes receive transaction content, they will complete the following steps:
- Pull transaction content from DA (if all txHashes committed to ordering in the previous block have corresponding transaction content, skip this step)
- Check if the transaction content matches the previously committed ordering txHash, discard if not matching
- Execute transactions according to the previously committed order, deduct the remaining fee and  50% of the actual difference  between gasUsed and gaslimit for tax  ( prevent the gasLimit much more than gasUsed so that validators can entire the whole block to get MEV)

This process continues cyclically.

### Role of DA (Optional)

In this scheme, it may happen that after transaction content is sent to the chain, miners see that the transaction is profitable and may maliciously withhold the transaction to prevent it from being included on-chain, then wait for users to resend the same transaction for attack. At this time, not only will users’ transaction profits still be eroded, but they will also waste a prepayment for the previously sent transaction hash.

Therefore, we need DA (such as ETH Blob) to ensure that transactions sent by users will definitely be included on-chain. This way, even if block-producing nodes maliciously withhold the transaction, other verification nodes and full nodes can still receive the transaction content and execute the transaction in subsequent block production processes. This forces block-producing nodes to include the transaction in their blocks to prevent state inconsistency with other nodes.

In this process, DA provides an additional layer of protection for users and is not mandatory. If users feel that the transaction has been sufficiently propagated to enough full nodes in the P2P network, they can choose not to use DA. Introducing DA can also prevent miners on the chain from jointly monopolizing and withholding user transactions.

### Consensus Requirements

The MEVless protocol requires a consensus mechanism with **unpredictable block production** to prevent speculative MEV attacks. Without unpredictable block production, block producers can perform cost-free speculative MEV attacks by submitting transaction hashes and then deciding whether to submit their transaction content based on other users’ transaction content, thus performing cost-free speculative MEV attacks. Since the prepayment ultimately goes to the block producer themselves, predictable block production allows them to recover their prepayment costs through block fees, making MEV attacks economically viable. Random block production forces attackers to pay prepayments for speculative transactions without knowing if they will be selected to produce the next block, making the prepayment cost real rather than recoverable through block fees, thus making such attacks economically unviable. The anti-MEV effectiveness increases exponentially with network decentralization - more validators mean lower individual selection probability, making attacks economically unviable. This protocol is applicable to Proof of Work, VDF-based consensus, and random beacon mechanisms, but not applicable to consortium chains, round-robin consensus, or any predictable block production schedules where validators can anticipate their turn to produce blocks. Additionally, the optional Data Availability layer prevents transaction withholding attacks by ensuring transaction content reaches the network even if block producers attempt to censor profitable transactions.

### Advantages

1. Compared to encrypted mempools, the MEVless solution has lower overhead, requiring no decryption operations that are energy-intensive for CPU and memory. MEVless only orders transaction hashes first, with a hash being only 32 bytes long (or even shorter). After ordering is complete, propagation places minimal burden on network bandwidth.
2. Compared to PBS, MEVless constrains from the source of MEV attacks - transaction ordering rights - by blocking attackers’ access to transaction information before ordering, eliminating the prerequisite for attackers to perform MEV attacks.
3. Conducive to decentralized execution and verifiable results. All MEV resistance methods and steps are hardcoded at the code level. As long as full nodes execute according to this code, the results are deterministic, making it difficult to perform MEV attacks in black box operations.
4. The difference between the privacy memory pool node and the privacy memory pool node is that the privacy memory pool will not publish the promised transaction order to the entire network nodes for consensus before knowing the specific transaction content, while MEVless will publish the promised transaction order to the entire network and let each full node write it into the block after consensus to ensure that the transaction will be executed in the promised order.

​​

​​

## Replies

**wjmelements** (2025-10-08):

If they can’t see the transaction contents, how do they keep the block gas below the limit?

---

**Lawliet-Chan** (2025-10-09):

Users have to include the gas-limit of their tx when they submit the txHash ( the txHash submision include these metadata but not calldata),  so that validators can keep the block gas below the limit

---

**wjmelements** (2025-10-09):

Currently the block gas limit is the gasUsed by all of their transactions and not their gas limits. Some other chains like Filecoin do this the other way. Filecoin also taxes the difference between your gas limit and your gasUsed to prevent transactions from wasting blockspace for free. So for this approach you would probably want a similar mechanism, perhaps charging transactions according to gas limit instead of gasUsed; otherwise, users only pay for gasUsed but can deny the whole block fairly cheaply.

---

**Lawliet-Chan** (2025-10-10):

1. What does ’ users can deny the whole block ’ mean? Users have no permission to deny block, only validators can do it.
2. blockspace won’t be wasted, if the gasUsed is out of the limit, validators will discard those transactions.   AND the prepayment is not all of the transaction’s GasFee, it just represents gasfee of txHash and tip that users want to offer for the priority of their txs,   when users submit their tx-content and they will offer the remaining fee

---

**wjmelements** (2025-10-10):

> Users have to include the gas-limit of their tx when they submit the txHash ( the txHash submision include these metadata but not calldata), so that validators can keep the block gas below the limit

I submit transaction with tx gas = block gas, priority fee = 5 gwei, outbidding every other transaction. Validator picks me because I pay the most. So I am the entire block. But my gasUsed is only 21000, so I only pay 105 szabo priority to deny the whole block. I can keep doing this until it is my turn to propose a block, and then I can get all of the MEV.

---

**Lawliet-Chan** (2025-10-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> I submit transaction with tx gas = block gas, priority fee = 5 gwei, outbidding every other transaction. Validator picks me because I pay the most. So I am the entire block. But my gasUsed is only 21000, so I only pay 105 szabo priority to deny the whole block. I can keep doing this until it is my turn to propose a block, and then I can get all of the MEV.

Oh! I get u!  I will improve MEVless protocol with your suggestion!   Thank u, bro ~

