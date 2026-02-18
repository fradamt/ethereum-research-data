---
source: ethresearch
topic_id: 20590
title: "Parallelizing Ethereum: A Novel Approach Using Historical Data and Transactional Data"
author: malik672
date: "2024-10-08"
category: EVM
tags: [layer-2]
url: https://ethresear.ch/t/parallelizing-ethereum-a-novel-approach-using-historical-data-and-transactional-data/20590
views: 421
likes: 9
posts_count: 3
---

# Parallelizing Ethereum: A Novel Approach Using Historical Data and Transactional Data

Currently at max, Ethereum TPS is maxed out 12-15 TPS  compared to VISA(Visa does 25k up to 65k per seconds btw) that’s like way too low, now of course one of the main reasons this is happening is due to lack of parallelization on Ethereum but what if there was a way we could parallize Ethereum, in my current research which is still in work, I propose two ways to parallelize Ethereum transactions using two methods:

**1. Historical data**

**2. Transactional data**

**Historical data**: when you think about historical data, think about branch prediction your compiler uses. This would involve analysing past transactions from popular contracts that are not proxies or dynamic in nature. For example, think about Uniswap v3 contracts, non-upgradeable and highly predictable due to the number of times it has been executed there’s no reason we can’t predict possible states a popular or highly executed non-upgradeable smart contract can interact with, this is how it works: based on how highly executed contracts have behaved previously (which states they accessed), the system could predict which states future transactions will likely interact with.

**Transactional data**: 3 methods and 3 ways, ever heard of static analysis, using a transaction method, the calldata and the contract bytecode there is way we can predict the expected states a transaction will cause effect

### How the parallelization will work:

- Block Builders can perform this analysis before proposing blocks. Once the transactional or historical data is analysed, the block builder can organize the transactions into groups or clusters that can be parallelized. Each cluster represents transactions that do not conflict with each other.
- Block Proposal: After grouping transactions into parallelizable clusters, the block builder can propose a block in a way that minimizes execution time, potentially allowing multiple processors or threads to handle different clusters in parallel.

### Challenges

1. Dependent Transactions:  let’s assume we have two transactions (y1, y2) that depend on each other, parallelization of this will be extremely difficult, a popular example of this would be a transaction to approve a number of tokens for spending(y1) and another one to actually transfer the token by a smart contract, trying to parallelize this will throw an error. A common way to solve this is not to parallelize transactions or use a single processor to process these transactions, how do we identify these transactions? quite simple, we can use Tx.origin and msg.sender to identify these types of transactions
2. Internal transactions that are inter and intra dependent: The only way to solve these types is to implement a type of algorithm I call TGA (Transactional Graph Analysis). What’s TGA,

### How TGA works:

1. Understanding Transaction Dependencies

- Each Ethereum transaction can modify or read certain parts of the state (e.g., account balances, contract storage).
- Some transactions depend on the results of previous transactions. For example, a transaction to transfer tokens depends on a prior approval transaction. If the approval hasn’t happened yet, the transfer will fail.
- TGA helps map out these dependencies by constructing a graph where each node is a transaction, and edges between nodes represent dependencies.

1. Building the Transaction Graph

- Nodes: Each transaction in a block is represented as a node in the graph.
- Edges: An edge between two nodes (transactions) indicates that one transaction depends on the other. For example, if Tx1 modifies a state that Tx2 will read, an edge would be drawn from Tx1 to Tx2, showing that Tx2 depends on Tx1.

1. Analyzing the Graph

- Once the graph is constructed, TGA analyzes the dependencies to identify independent transactions (i.e., nodes without incoming or outgoing edges).
- Parallelizable clusters: Transactions that are not connected by edges can be grouped into clusters that can be processed in parallel. These clusters are independent and won’t conflict with each other.
- Sequential clusters: If transactions are connected by edges, TGA ensures that they are processed sequentially to preserve the correct execution order.

1. Handling Cycles (Mutual Dependencies)

- Sometimes, transactions may form a cycle where Tx1 depends on Tx2, and Tx2 depends on Tx1. This situation is called a cyclic dependency.
- TGA would detect these cycles and flag the transactions involved as requiring sequential processing, meaning they cannot be parallelized.

1. Practical Implementation

- In a block, the Block Builder could run TGA to analyse all transactions before proposing the block. This analysis would result in two sets:

 Independent transactions: These can be executed in parallel across different processors.
- Dependent transactions: These must be executed sequentially, based on their dependencies.

**Example:**

Let’s say a block has 5 transactions:

- Tx1: Transfers ETH from Alice to Bob.
- Tx2: Approves a DAI transfer for a DeFi contract.
- Tx3: Transfers DAI from Alice to the contract (depends on Tx2).
- Tx4: Changes a parameter in a governance contract.
- Tx5: Reads a balance from the governance contract (depends on Tx4).

Using TGA:

- Tx1, Tx2, and Tx4 are independent (no edges between them), so they can be parallelized.
- Tx3 depends on Tx2 and must be executed after it.
- Tx5 depends on Tx4, so it must be executed after Tx4.

**Of course, a better method will be to implement timestamps for each transaction ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)**

**I also think this is more suitable to a L2 ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)**

## Replies

**MASDXI** (2024-12-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/malik672/48/17557_2.png) malik672:

> Tx1: Transfers ETH from Alice to Bob.
> Tx2: Approves a DAI transfer for a DeFi contract.
> Tx3: Transfers DAI from Alice to the contract (depends on Tx2).
> Tx4: Changes a parameter in a governance contract.
> Tx5: Reads a balance from the governance contract (depends on Tx4).

From your example, I grouped it into scenarios and additional case contract creation

### EOA Transfer to EOA Transaction

```json
"tx": {
  "form": "EOA_ADDRESS",
  "to": "EOA_ADDRESS",
  "value": "HEX_VALUE",
  "data": null
}
```

| TX | Scenario | Conflict |
| --- | --- | --- |
| 1 | alice transfer to bob | TRUE |
| 2 | bob transfer to charlie | TRUE |
| 3 | charlie transfer to dave | TRUE |

### EOA Transfer to Contract Transaction

```json
"tx": {
  "form": "EOA_ADDRESS",
  "to":"CONTRACT_ADDRESS",
  "value": "HEX_VALUE",
  "data": null
}
```

> receive operations can trigger transaction conflicts.

| TX | Scenario | Conflict |
| --- | --- | --- |
| 1 | alice transfer to CONTRACT_A | FALSE |
| 2 | bob transfer to CONTRACT_B | TRUE |
| 3 | charlie transfer to CONTRACT_B | TRUE |

### EOA Call to Contract Transaction

```json
"tx": {
  "form": "EOA_ADDRESS",
  "to": "CONTRACT_ADDRESS",
  "value": "0x00", // or with hex value
  "data": "0x..."
}
```

| TX | Scenario | Conflict |
| --- | --- | --- |
| 1 | alice call to CONTRACT_C | TRUE |
| 2 | bob call to CONTRACT_B | FALSE |
| 3 | charlie call to CONTRACT_C | TRUE |

> if CONTRACT_B have internal call to CONTRACT_C will lead tx3 to conflict with tx1 and tx2
> internal calls and receive operations can trigger transaction conflicts.

### Contract Creation Transaction

```json
"tx": {
  "form": "EOA_ADDRESS",
  "to": null,
  "value": "0x00", // or with hex value
  "data": "0x..."
}
```

| TX | Scenario | Conflict |
| --- | --- | --- |
| 1 | alice create CONTRACT_A | FALSE |
| 2 | bob create CONTRACT_B | FALSE |
| 3 | charlie create CONTRACT_C | FALSE |

> if constructor of CONTRACT_A have internal call to CONTRACT_C will lead tx3 to conflict with tx1 and tx2
> internal calls and receive operations can trigger transaction conflicts.

---

**p_m** (2024-12-20):

Tps is not 12-15, it’s 300+: https://rollup.wtf/

And it could be made 5000 tomorrow, but state / bandwidth growth is the main issue.

