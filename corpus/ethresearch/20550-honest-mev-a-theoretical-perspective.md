---
source: ethresearch
topic_id: 20550
title: "Honest MEV: a Theoretical Perspective"
author: destrat18
date: "2024-10-03"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/honest-mev-a-theoretical-perspective/20550
views: 371
likes: 3
posts_count: 1
---

# Honest MEV: a Theoretical Perspective

# Honest MEV: a Theoretical Perspective

# Greetings

Hi there! We are a research team [Togzhan](https://sites.google.com/view/btogzhan/about), [Soroush](http://soroush.farokhnia.me/), [Amir](https://amir.goharshady.com/), [Sergei](https://polka125.github.io/) who cares about blockchain research, algorithms, and optimization.

# TL;DR; (aka abstract)

We propose a new research direction: using graph parameters to solve the honest MEV problem (the problem of forming a block with maximum gas fees by an honest miner). The method was successfully tested on real-world data from other blockchains, increasing miners’ revenue by **13.4%** on Bitcoin **(~100 million USD/year)** and by **55.7%** on Cardano **(~0.5 million USD/year)**. However, Ethereum presents unique challenges that are yet to be overcome: non-trivial transaction dependencies, a unique reward model, and a non-UTXO model which causes undecidability. We look forward to the community’s opinions and suggestions regarding the challenges we face.

# Related Works

Our previous for other blockchains:

- Bitcoin: https://hal.science/hal-03232783v2/file/OptimalMining.pdf
- Cardano: https://hal.science/hal-04616639/file/main.pdf

Similar work on ethresear.ch:

- Block Building is not just knapsack!

# The Project

**What is Honest MEV?** Let’s consider the perspective of an honest validator – one who refrains from frontrunning, sandwiching, and other dishonest behaviors. The reward we receive for validating a block includes the base reward, and the gas fees paid by transactions. The gas fees are the only variable we can influence, so naturally, we’re interested in maximizing them.

**What do we want to do?** We have only one degree of freedom: how to take an ordered subset of the transactions from the pool to a new block to maximize the gas fees. Our main ambition is to make this decision procedure **optimal**, **fast**, and **accessible** for everyone.

**I’m not a block proposer, why care?** Besides the obvious benefits to an honest block proposer, the indirect impact of our project is far greater:

- It helps validators achieve maximum block utilization
- It helps with throughput, allowing more transactions to be added to the consensus chain faster
- The increase in revenues also incentivizes more people to become validators, helping more decentralized consensus.
- In addition to protocol constraints (e.g. dynamic pricing policy for gas), external constraints also commonly influence miners’ decisions. For example, miners may choose to produce smaller blocks to speed up block propagation or adjust the algorithm to manage different sets of transactions within the pool. The primary goal of the divine algorithm is to allow miners to maximize their profitability, within the constraints. This means that even if a miner has to create a small block, she can still maximize her revenue by picking a better set of transactions.

**What has been done already?** If the problem is so fundamental, someone must have done something about it already, right? Right. Our team has a line of research devoted to developing optimal mining algorithms, i.e. algorithms that produce blocks with maximum rewards, for different blockchains, we successfully tested, implemented and published optimal approaches for the [Bitcoin](https://hal.science/hal-03232783v2/file/OptimalMining.pdf) and [Cardano](https://hal.science/hal-04616639/file/main.pdf) blockchains. We tested our approach on the real world data and achieved a **13.4%** increase in transaction fees on Bitcoin **(~100 million USD/year)** and a **55.7%** growth on Cardano **(~0.5 million USD/year)**. Moreover, the problem has independently attracted the attention of [other Ethereum researchers](https://ethresear.ch/t/block-building-is-not-just-knapsack/19871)

**Why not just reuse the previous algorithms?** The Ethereum execution model is inherently complex as it does not follow the UTXO model; the final gas fees as well as gas consumption of one transaction might depend on others, it makes a huge tractability gap compared to other networks.

While for two transactions it is simple to say if they are not conflicting (by checking a set of predefined rules, like nonce, balance, etc), it is really hard to say if one transaction interferes with others gas consumptions; if not a block gas limits, the gas dependency problem is **theoretically undecidable**, and if having a gas bound it is [EXPTIME-complete](https://en.wikipedia.org/wiki/EXPTIME#EXPTIME-complete).

**So what is your plan?** Our plan has several subgoals:

- Find a way to detect all dependencies between the transactions in a pool
- Formulate the problem as an optimization instance with a graph input
- Implement the algorithm and test it on real pools and blocks

**Where can I see more technical details?** Sure, in the next few paragraphs we want to give a deeper introduction for our framework, and what challenges we are facing.

# Transaction Interference

There are three ways how transactions might affect each other: they might

- depend on each other, i.e. one transaction cannot be included to a block unless another is included
- conflict, i.e. cannot both appear in the same block
- gas dependent, i.e. depending on co-occurrence of two transactions, their gas fees might be different

We will illustrate all interference types with a simple example.

### Dependency Interference

In a correct block, transactions originating from the same account must have sequential nonce, lower nonce must appear before transactions with higher nonce to preserve the ordering. When a miner observes the transaction pool, she should choose transactions in a way that preserves an increasing nonce order for a particular account.

[![](https://ethresear.ch/uploads/default/optimized/3X/f/a/faf35736906a2c9a3948871cc08e092dc0c6ed50_2_450x219.png)1148×562 15.8 KB](https://ethresear.ch/uploads/default/faf35736906a2c9a3948871cc08e092dc0c6ed50)

This requirement creates the dependency relations, captured as oriented **dependency edges** in the interference graph.

### Conflict Interference

Transactions originating from the same account must have sequential nonce, it is not allowed to have two transactions with the same nonce. When the miner encounters two transactions with the same nonce, he has to choose only one of them to be included in the block.

**[![](https://ethresear.ch/uploads/default/optimized/3X/5/9/59c90103b23f5e9379b0a6ec8bb378bbd63ee680_2_478x234.png)1148×562 11.1 KB](https://ethresear.ch/uploads/default/59c90103b23f5e9379b0a6ec8bb378bbd63ee680)**

We introduce undirected **conflict edges** to the graph to represent this restriction.

### Gas Dependency Interference

The last one is the most complicated relation, we will demonstrate it using a simple example. Consider a smart contract with the following two functions `f` and `g`:

```auto
function f(): x = 1000
function g(): for i=1 to x { do something }
```

Assume that `x` is originally `0` and there are two transactions `Tx1` calling `f` and `Tx2` calling `g`. If  the validator puts `Tx2` before `Tx1`, the for loop in `g` terminates immediately, using very little gas. However, if `Tx1` is put before `Tx2`, then much more gas is used in `g`, leading to higher revenues for the validator.

### DCG Graph

We call a DCG graph a graph with each vertex representing a transaction in the mempool and edges of three sorts, with one for each type of interference.

A graph abstraction is an important step in our framework as it splits the problem into two subtasks: constructing the graph from the mempool and solving the optimization problem over the graph.

# Graphs and Optimizations

Many graph problems are known for being very difficult. Our case is no exception: having only conflict-type edges makes the problem of choosing an optimal subset of vertices for the answer set **strongly NP-hard**. This essentially means we cannot hope for an algorithm that is **fast**, **optimal**, and **works on all inputs**. When we cannot have all three, we can still choose two, and that is what happens in practice:

- {works on all inputs, fast, optimal}: if we discard optimality, we find ourselves in the realm of approximate and heuristic algorithms.
- {works on all inputs, fast, optimal}: discarding the requirement to be fast leads to exponential time algorithms. While they might work on tiny inputs, it is unfeasible to run them on real data.
- {works on all inputs, fast, optimal}: generally hard problems become very easy in the special cases. For instance, a three coloring problem is trivial for tree graphs. We claim that real-world graphs are well-structured, and this structure can be exploited to build fast and optimal algorithms.

However, we don’t provide an exact definition of a **well-structured** graph, there is a [zoo of graph classes](https://www.graphclasses.org/). For some graph classes, there often exists a specially tailored algorithm which works well within the given class (see our previous publications). One step of our research program is to **identify the most suitable class** the real graphs belong to and design an algorithm which works within that class.

# An Example

We will demonstrate our ideas with an example. The oversimplifications here are intentional, allowing us to showcase the main techniques without getting bogged down in technical details.

The classical knapsack problem is [weakly NP-hard]([https://en.wikipedia.org/wiki/Weak\_NP-completeness](https://en.wikipedia.org/wiki/Weak%5C_NP-completeness)), and there are polynomial algorithms when all item volumes are discrete and each volume belongs to the set [1,…,N]. In this case, there is a dynamic programming algorithm that is polynomial in:

- The size of the knapsack S
- The maximum possible volume N

Consider an extremely simple version of the knapsack problem: all item volumes are equal to 1. How can we find an optimal value packing when the capacity of the knapsack is S? The algorithm is trivial: sort the items in decreasing order of price and select the top S most valuable items.

Translating this to the optimal block mining language, all transactions pay an equal gas fee of 1, and have no conflicts or dependencies, the optimal block would consist of the transactions offering the highest tips. This holds when there are no conflicts or dependencies.

What happens when we add interference edges? Again, let’s keep it simple and assume that we have only conflicts. Going back to the knapsack formulation, for some pairs of items, we cannot pack them together.

The problem suddenly became **very hard.** It’s not just NP-hard, it’s **strongly NP-hard**. The reason for that, that the problem of finding a [maximal independent set]([https://en.wikipedia.org/wiki/Maximal\_independent\_set](https://en.wikipedia.org/wiki/Maximal%5C_independent%5C_set)) is a special case of our problem: by setting the knapsack capacity to infinity and all weights to 1, finding the optimal knapsack becomes equivalent to finding a maximal independent set.

Although it is clear that not all graphs can be achieved as a conflict graph of a set of transactions (and in fact, the dependency graph is always a union of cliques), this aligns with our final goal: exploit specific graph patterns to design a faster algorithm.

Do demonstrate how, assume that the conflict edges form a binary tree. The full list assumptions we are making till this point are:

- Each transaction uses 1 unit of gas
- We don’t make a restriction on the tips the transactions can pay
- The only type of interference edges we have are conflict edges, and they form a binary tree (the least realistic assumption)

This problem from strongly NP hard becomes again polynomial time solvable! The main algorithmic technique for this is dynamic programming, we will demonstrate it on a concrete example.

Consider a pool of 6 transactions {a, b, c, d, e, f} with unit gas usage and with the miner tips given in the table

| Tx: | a | b | c | d | e | f |
| --- | --- | --- | --- | --- | --- | --- |
| Total tip: | 6 | 7 | 1 | 3 | 7 | 5 |
| Gas usage: | 1 | 1 | 1 | 1 | 1 | 1 |

Let us fix the size of the block to be 3. Further suppose that the miner observed a set of conflicts which form a binary tree with the edges {(a, b), (a, c), (b,d), (c,e), (c,f)}:​​

**[![](https://ethresear.ch/uploads/default/optimized/3X/4/7/47e875969aa2f1f1f722a8d61000f2d28b96b284_2_149x190.png)1259×1600 136 KB](https://ethresear.ch/uploads/default/47e875969aa2f1f1f722a8d61000f2d28b96b284)**

Introduce a tensor table opt[tx, IsIncl, Cap] with tx ∊ {a, b, c, d, e, f}; IsIncl ∊ {“no”, “yes”} and Cap ∊ {0, 1, 2, 3, 4}.

The value of the tensor is defined as:

`opt[tx, “no”, c] := “the best revenue a miner can get, only using transactions from the subtree of tx, when tx is not included, if the block capacity is c”`

And the similar rule for “yes”:

`opt[tx, “yes”, c] := “the best revenue a miner can get, using only transactions from the subtree of tx, when tx is included, if the block capacity is c”.`

Now our goal is to fill this table with values, then we can find the maximum possible benefit as

`max(opt[a, “no”, 3], opt[a, “yes”, 3]),`

I.e. as maximum profit which can be achieved using the subtree of a (which is the whole set {a, b, c, d, e, f}) and a block of capacity 3.

The filling out strategy is called bottom-up dynamic approach, we are going to fill the tables starting from the leaves of the tree, advancing to the root.

The values in the leaves are determined as:

`opt[tx, “no”, *] := 0`

As if we don’t take the leaf transaction, the bag is forced to be empty

`opt[tx, “yes”, 0] := - inf`

It is merely a convention to put the negative infinity profit, as such a configuration is not feasible: the “yes” field forces us to take the item tx to the set, but the value 0 constrains the block capacity to be 0. And the last case for the leaf table:

`opt[tx, “yes”, ≥ 1] := tip(tx),`

As we are forced to include transaction tx to the block, and including it does not exceed the block capacity.

For the running example after the initialization step we will have:

[![](https://ethresear.ch/uploads/default/optimized/3X/a/d/ad77eeec2e5f3a6fb6776d40b52d38161adf6759_2_624x312.png)1600×801 37.3 KB](https://ethresear.ch/uploads/default/ad77eeec2e5f3a6fb6776d40b52d38161adf6759)

To fill out the tables for the internal nodes, we again will consider two cases, if the node is forced to be included or not “yes”/”no”. Let’s start from the “yes” case, when a note tx is forced to be included to the block. The node tx has up to two children, suppose that it has exactly two children tx_l and tx_r (the case of one child can be handled by introducing a fake node with unit gas usage and zero tips).

Then to find the value of opt[tx, “yes”, c] first we need to allocate one unit of our capacity to the transaction tx, and the remaining capacity is split between two subtrees. Observe that if we took tx, then we cannot take neither tx_l or tx_r to the block because of the conflict edges from tx. Therefore

`opt[tx, “yes”, c] := tip(tx) +`

`max (opt[tx_l, “no”, i] + opt[tx_r, “no”, c - i - 1])`

`for i in [0, c)`

The i indicates the capacity allocated to the left child, and all remaining capacity is allocated to the right child.

Similar reasoning leads us to the formula for the “no” case:

`opt[tx, “no”, c] := max(`

`max{opt[tx_l, “no”, i], opt[tx_l, “yes”, i}`

`+ max{opt[tx_r, “no”, c - i - 1], opt[tx_r, “no”, c - i - 1]})`

where having to have max{opt[tx_l, “no”/”yes”, *]} is caused by necessity to consider two cases whether to include or exclude the child from the set. Filling the tables using these formulas, we end up with:

**[![](https://ethresear.ch/uploads/default/optimized/3X/2/4/2461dd155e6cb079d8ae3afe3642efd3840b0742_2_624x312.png)1600×801 41.1 KB](https://ethresear.ch/uploads/default/2461dd155e6cb079d8ae3afe3642efd3840b0742)**

We can see that the optimal block of size 3 will produce revenue 19 from the table at the root, which is the case for the block {b, e, f}. Finding not only the answer but also the block itself is achieved by a standard technique of keeping the optimal capacity split between the children when evaluating the formula for the internal nodes, as well as keeping the optimal decision whether to take a child to the set or not.

Despite the oversimplifications we made, our general algorithms for other blockchains have the same flavor: we find a way to build the graph starting from elementary parts (leafs for this case) using simple combining operations (combining two children subtrees into the node’s tree in this case) and providing the way to recompute the objective function during the combination operation.

# Challenges

We identified the challenges we need to address during the project. The challenges vary in nature: some are related to engineering and computation, while other are purely theoretical.

We anticipate to face the following challenges:

- to have a well-connected node to access the transaction pool.
- to be able to execute transaction bundles and obtain their gas usage.
- to be able to Identify if two transactions are exactly gas dependent is possible if we execute every possible subset of transactions and in every possible order. One way is to use various tools which include symbolic execution tools and static analysis tools.
- to examine the structure of the transactions interference graph, choose the closest class from the zoo of graph classes and create an efficient algorithm solving the optimization problem

# Opinion Request

We truly believe it is possible to obtain an increase in the transaction revenue for Ethereum and beat real-world miner results. If we do this, it would greatly benefit both miners and the Ethereum ecosystem. What do you think about this project? Please feel free to share your opinion and potential concerns. Let’s have a discussion below! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)
