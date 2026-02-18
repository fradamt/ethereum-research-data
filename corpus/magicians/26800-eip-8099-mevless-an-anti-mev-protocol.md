---
source: magicians
topic_id: 26800
title: "EIP-8099: MEVless, an anti-MEV protocol"
author: Lawliet-Chan
date: "2025-12-01"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8099-mevless-an-anti-mev-protocol/26800
views: 94
likes: 1
posts_count: 1
---

# EIP-8099: MEVless, an anti-MEV protocol

### Prerequisites

**MEVless applicable attack scenarios**:

- Sandwich attacks
- Front-running attacks

### Principle

The principle of MEVless lies in constraining miners’ behavior in transaction ordering. Our approach is to prevent miners from seeing specific transaction content during ordering. Transactions are ordered without miners seeing the transaction content, so even miners cannot perform MEV attacks since they don’t know the specific transaction content. After ordering, the sequence needs to be published to the public network so other nodes and users are informed. At this point, the transaction order is finalized and included in the block, so when specific transaction content is submitted later, it will be executed according to this consensus order, with no room for MEV operations.

We divide on-chain blocks into two types:

- Ordering blocks, which only complete three things: receiving transaction hashes, deducting user prepayments, and providing transaction ordering commitments. The interval between sequenced blocks can be shorter than that between execution blocks.
- Execution blocks, which are no different from ordinary blocks, only need to execute transactions according to the order committed in the previous ordering block

These two types of blocks are produced alternately. For example, after the genesis block, blocks with odd block heights are ordering blocks, and blocks with even block heights are execution blocks.

### Process

[![MEVless](https://ethereum-magicians.org/uploads/default/optimized/3X/d/f/df2a6db7088cb4ddcf7fbcfb5e5fc4ae4bd9a56d_2_256x500.png)MEVless421×822 56.4 KB](https://ethereum-magicians.org/uploads/default/df2a6db7088cb4ddcf7fbcfb5e5fc4ae4bd9a56d)

1. Block N (ordering block) begins block production
2. Users send transaction hashes to the chain and pay a certain prepayment. The prepayment consists of two parts:
(1) Gas fee for transaction hash: Used for storage of transaction hash and computation fees during ordering. This fee is generally fixed and mandatory.
(2) Additional tip: Extra fee paid by users to ensure their transaction can be ordered as early as possible. This amount is not fixed and can be zero
3. After the chain nodes receive transaction hashes, they will complete the following steps:

- Check if the transaction account has sufficient funds to pay the prepayment
- Sort transaction hashes from high to low based on prepayment amount
- Deduct the prepayment amount from the transaction account
- Store the sorted transaction order as a commitment in the block and publish it to the P2P network

1. After users subscribe and query to see the ordering sequence number of their transaction hash committed on-chain, they send specific transaction content (including the remaining gasfee) to the chain
2. After chain nodes receive transaction content, they will complete the following steps:

- Check if the transaction content matches the previously committed ordering txHash, discard if not matching
- Execute transactions according to the previously committed order
This process continues cyclically.

### Consensus Requirements

The MEVless protocol requires a consensus mechanism with **unpredictable block production** to prevent speculative MEV attacks. Without unpredictable block production, block producers can perform cost-free speculative MEV attacks by submitting transaction hashes and then deciding whether to submit their transaction content based on other users’ transaction content, thus performing cost-free speculative MEV attacks. Since the prepayment ultimately goes to the block producer themselves, predictable block production allows them to recover their prepayment costs through block fees, making MEV attacks economically viable. Random block production forces attackers to pay prepayments for speculative transactions without knowing if they will be selected to produce the next block, making the prepayment cost real rather than recoverable through block fees, thus making such attacks economically unviable. The anti-MEV effectiveness increases exponentially with network decentralization - more validators mean lower individual selection probability, making attacks economically unviable. This protocol is applicable to Proof of Work, VDF-based consensus, and random beacon mechanisms, but not applicable to consortium chains, round-robin consensus, or any predictable block production schedules where validators can anticipate their turn to produce blocks. Additionally, the optional Data Availability layer prevents transaction withholding attacks by ensuring transaction content reaches the network even if block producers attempt to censor profitable transactions.

### Advantages

1. Compared to encrypted mempools, the MEVless solution has lower overhead, requiring no decryption operations that are energy-intensive for CPU and memory. MEVless only orders transaction hashes first, with a hash being only 32 bytes long (or even shorter). After ordering is complete, propagation places minimal burden on network bandwidth.
2. Compared to PBS, MEVless constrains from the source of MEV attacks - transaction ordering rights - by blocking attackers’ access to transaction information before ordering, eliminating the prerequisite for attackers to perform MEV attacks.
3. Conducive to decentralized execution and verifiable results. All MEV resistance methods and steps are hardcoded at the code level. As long as full nodes execute according to this code, the results are deterministic, making it difficult to perform MEV attacks in black box operations.
4. The difference between the privacy memory pool node and the privacy memory pool node is that the privacy memory pool will not publish the promised transaction order to the entire network nodes for consensus before knowing the specific transaction content, while MEVless will publish the promised transaction order to the entire network and let each full node write it into the block after consensus to ensure that the transaction will be executed in the promised order.
