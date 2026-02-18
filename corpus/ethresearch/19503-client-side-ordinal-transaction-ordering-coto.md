---
source: ethresearch
topic_id: 19503
title: Client-Side Ordinal Transaction Ordering (COTO)
author: cryptskii
date: "2024-05-08"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/client-side-ordinal-transaction-ordering-coto/19503
views: 2961
likes: 5
posts_count: 6
---

# Client-Side Ordinal Transaction Ordering (COTO)

**TL;DR** ProofChain introduces a novel transaction ordering mechanism called Client-Side Ordinal Transaction Ordering (COTO) that achieves deterministic and uniform ordering of transactions across shards without requiring shard synchronization, enhancing the scalability of the system.

**Background** Existing blockchain systems face scalability challenges due to limitations in their transaction ordering approaches. Global consensus ordering suffers from limited throughput, while shard-level consensus ordering requires cross-shard synchronization. DAG-based approaches face challenges in transaction finality and handling conflicting transactions.

**Proposal** COTO assigns a unique ordinal rank to each transaction based on the sender’s shard ID, logical clock value, timestamp, and hash of the serialized transaction. The ordinal rank determines the order in which transactions are processed. Each shard validates and processes transactions independently using the assigned ordinal ranks. Processed transactions are propagated to other shards through either Client View (signed transactions) or Global View (Global State Proofs) propagation modes.

Let \mathcal{T} denote the set of all transactions in the ProofChain network. Each transaction tx \in \mathcal{T} is represented as a tuple:

tx = (s, r, a, n, t)

where:

s is the sender’s address

r is the recipient’s address

a is the transaction amount

n is the transaction nonce

t is the transaction timestamp

The ordinal rank of a transaction tx is calculated as follows:

OrdinalRank(tx) = (Shard(tx), LogicalClock(tx), Timestamp(tx), Hash(Serialize(tx)))

where:

Shard(tx) = hash(tx.s) \bmod m, with hash being a cryptographic hash function and m the total number of shards

LogicalClock(tx) is the current logical clock value of the client

Timestamp(tx) is the current timestamp at the time of transaction submission

Hash(Serialize(tx)) is the cryptographic hash of the serialized transaction

**Illustration** Consider two transactions, tx_1 and tx_2, submitted to the ProofChain network. The ordinal ranks of these transactions are calculated as follows:

OrdinalRank(tx_1) = (Shard(tx_1), LogicalClock(tx_1), Timestamp(tx_1), Hash(Serialize(tx_1)))

OrdinalRank(tx_2) = (Shard(tx_2), LogicalClock(tx_2), Timestamp(tx_2), Hash(Serialize(tx_2)))

Assuming tx_1 and tx_2 belong to different shards and have unique ordinal ranks, they can be processed independently by their respective shards without requiring cross-shard synchronization.

**Advantages** COTO offers several advantages over alternative transaction ordering approaches:

1. Scalability: COTO allows parallel transaction processing across shards, eliminating the need for global consensus or cross-shard synchronization.
2. Deterministic Ordering: COTO ensures a deterministic ordering of transactions based on their unique ordinal ranks, providing consistency across shards.
3. Efficient Propagation: COTO supports efficient propagation of shard states through succinct Global State Proofs (GSPs) or signed transactions.

**Applications** COTO can be applied in various scenarios where scalability and deterministic ordering of transactions are crucial:

1. High-Throughput Payment Systems: COTO enables fast and parallel processing of transactions, making it suitable for large-scale payment networks.
2. Decentralized Exchanges: COTO ensures a consistent ordering of trades across shards, facilitating efficient and fair execution of orders.
3. Supply Chain Management: COTO can be used to track and order events in supply chain networks, ensuring data integrity and consistency across participants.

**Conclusion** Client-Side Ordinal Transaction Ordering (COTO) introduces a scalable and deterministic approach to transaction ordering in sharded blockchain networks. By assigning unique ordinal ranks to transactions and enabling parallel processing across shards, COTO addresses the scalability challenges faced by existing transaction ordering approaches. The mathematical formalisms, algorithms, and proofs presented demonstrate the correctness and scalability properties of COTO, making it a promising solution for various applications requiring high throughput and consistent transaction ordering.

## Replies

**cryptskii** (2024-05-08):

Simply put. We remove ordering from consensus. Consensus should focus on validity and inclusion. For a more efficient and scalable approach. Based on the advancements of ZKPs use directly in consensus mechanism, this is entirely plausible. There no longer exists a need to continue with this as a bottleneck.

thanks to Casey Rodarmor for bringing ordinal theory and its ability to impact how we tackle issues in hard to tackle instances to our attention. like interacting with BTC

---

**MicahZoltu** (2024-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptskii/48/14536_2.png) cryptskii:

> We remove ordering from consensus. Consensus should focus on validity and inclusion.

Validity is a function of order though.  Changing the order of inclusion may change validity, so you must come to consensus on at least partial ordering (where there is a validity conflict).

A simple example of this is two transactions with the same nonce and gas price.  How do you decide which is canonical and which is not?

---

**cryptskii** (2024-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> A simple example of this is two transactions with the same nonce and gas price. How do you decide which is canonical and which is not?

Great Point. If we extend the `OrdinalRank` to include additional transaction attributes and define a comprehensive comparison function. The extended `OrdinalRank` is defined as:

```auto
OrdinalRank = (ShardID, LogicalClock, GasPrice, TransactionFee, Nonce, Timestamp, Hash)
```

The comparison function \prec is defined as:

```auto
rank_1 \prec rank_2 \iff \begin{cases}
ShardID_1 < ShardID_2 \\
ShardID_1 = ShardID_2 \wedge LogicalClock_1 < LogicalClock_2 \\
ShardID_1 = ShardID_2 \wedge LogicalClock_1 = LogicalClock_2 \wedge GasPrice_1 < GasPrice_2 \\
ShardID_1 = ShardID_2 \wedge LogicalClock_1 = LogicalClock_2 \wedge GasPrice_1 = GasPrice_2 \wedge TransactionFee_1 < TransactionFee_2 \\
ShardID_1 = ShardID_2 \wedge LogicalClock_1 = LogicalClock_2 \wedge GasPrice_1 = GasPrice_2 \wedge TransactionFee_1 = TransactionFee_2 \wedge Nonce_1 < Nonce_2 \\
ShardID_1 = ShardID_2 \wedge LogicalClock_1 = LogicalClock_2 \wedge GasPrice_1 = GasPrice_2 \wedge TransactionFee_1 = TransactionFee_2 \wedge Nonce_1 = Nonce_2 \wedge Timestamp_1 < Timestamp_2 \\
ShardID_1 = ShardID_2 \wedge LogicalClock_1 = LogicalClock_2 \wedge GasPrice_1 = GasPrice_2 \wedge TransactionFee_1 = TransactionFee_2 \wedge Nonce_1 = Nonce_2 \wedge Timestamp_1 = Timestamp_2 \wedge Hash_1 < Hash_2
\end{cases}
```

The comparison function \prec compares the attributes in a specific order, ensuring a total ordering of transactions and eliminating the possibility of ties:

\forall rank_1, rank_2 \in OrdinalRank: rank_1 \neq rank_2 \implies rank_1 \prec rank_2 \vee rank_2 \prec rank_1

This way it resolves conflicts deterministically without relying on consensus.

---

**MicahZoltu** (2024-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptskii/48/14536_2.png) cryptskii:

> Simply put. We remove ordering from consensus. Consensus should focus on validity and inclusion. For a more efficient and scalable approach. Based on the advancements of ZKPs use directly in consensus mechanism, this is entirely plausible. There no longer exists a need to continue with this as a bottleneck.

This allows a user to send multiple copies of a transaction (one in each shard) but only have one of them actually execute and charge them gas, potentially opening the doors to a DoS attack.  I believe we would need to have the gas cost for base transactions be multiplied by the number of shards to protect against this.

---

**cryptskii** (2024-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I believe we would need to have the gas cost for base transactions be multiplied by the number of shards to protect against this.

What about?:

1. Transaction Footprint Analysis: Before processing, the system evaluates how many shards a transaction impacts. This can be determined based on the transaction’s data dependencies, such as which accounts or contracts are being interacted with and their respective locations within the shard architecture.
2. Base Rate Plus Incremental Fee: A base transaction fee is charged for all transactions. Additional fees are then added based on the number of shards the transaction touches. For instance:

- Base fee: Charged for computational costs and maintaining the transaction in the ledger.
- Incremental shard fee: Added for each shard beyond the first that is required to process or verify the transaction.

1. Calculation and Billing: The total cost is dynamically calculated at the time of transaction submission, ensuring that the fees are reflective of the actual network resources consumed.

