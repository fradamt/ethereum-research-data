---
source: magicians
topic_id: 13400
title: "[Core EIP] Cold/Hot Accesses within the context of a Block"
author: green
date: "2023-03-18"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/core-eip-cold-hot-accesses-within-the-context-of-a-block/13400
views: 526
likes: 3
posts_count: 5
---

# [Core EIP] Cold/Hot Accesses within the context of a Block

(This is messy, I just want to start an informal discussion)

Considering cold/hot accesses (for storage, or accounts) in the context of a block, instead of the context of a transaction.

Cons:

- probably hard to implement, since it breaks many assumptions and the clients would have to add a bunch of complexity
- whoever lands first in the block, pays the cold load for everyone else (but, that’s a “fairness” con, since they’re already paying for it)

Pros:

- cheaper gas for users. more reasonable gas pricing, more aligned with the costs

Uniswap has been using big routers to do things, and now there’s `permit2`. Permit2 is arguably healthy for the protocol (less bytecode on new deployed tokens). But it’s punished by the gas pricing, since users have to do more cold accesses.

(making up numbers now) let’s say that in most blocks there are 20 redundant permit2 cold accesses. The execution clients are benefiting from less cache misses, due to interacting with this contract, so there’s a pricing mismatch here.

Obviously, this occurs with way more things:

- delegating calls to highly used contracts (Safe, Blur)
- most relevant rollups are, even when they ossify, delegating calls

Is this worthwhile to implement, or is this too difficult and unpractical for execution clients?

## Replies

**bawtman** (2023-03-18):

Hi [@green](/u/green) , I am not sure this is possible because there would be no way to estimate the gas in advance. Maybe if it were the last block it would be feasible. It would also put an unfair burden on whom ever had to pay depending on what is in the other transactions entail. Would be interested in hearing more on how this could be implemented.

---

**green** (2023-03-19):

> there would be no way to estimate the gas in advance

Just like now, then. Wallets should estimate the worst case scenario, as regular, as if all the accesses that used to be cold, continue to be cold.

> Maybe if it were the last block it would be feasible

Accounts or storage (= *space*) that were last accessed last block, can still be cheaper to load compared to *space* that was last accessed 100 blocks ago.

However this would be even more cumbersome to implement. In this case, the problem at hand is that, since every node is validating the transactions in the same block, that *space* has been accessed <1 second ago, so it’s very likely to remain in cache. The cost to access them is, on average, way lower compared to the cost of accessing space last accessed in the previous block.

> It would also put an unfair burden on whom ever had to pay depending on what is in the other transactions entail

In this case, I don’t think *fairness* is a problem. Gas costs would either be the same, or less. It’s not unfair if the other transactions get a discount and you don’t, because if you’re the first transaction to open the block, you access them cold. You would have previously accessed them cold as well, so, from your perspective, you’re doing whatever you could do before.

You can’t tell if other transactions will want to also access those spaces in the same block.

There’s also MEV considerations. Users are paying *priority fees* in order to get their transactions to be executed first. In a way, being the transaction that opens up the way for the other transactions on the block to be cheaper, is a priority fee as well.

---

**bawtman** (2023-03-19):

Hey [@green](/u/green), OK I am warming up to this idea after reading your rebuttals. How would we go about implementing this, Can you give an example or some code that points to a solution?

---

**green** (2023-03-19):

I don’t work on the execution clients so I won’t resort to writing code to convey the idea of the proposal, without getting feedback about whether if it’s worthwhile or not.

The EVM is currently keeping track of [access sets (EIP-2929)](https://eips.ethereum.org/EIPS/eip-2929) within the context of a transaction. [Here’s some code in geth](https://github.com/ethereum/go-ethereum/blob/ee8e83fa5f6cb261dad2ed0a7bbcde4930c41e6c/core/vm/operations_acl.go#L103) linking to the implementation.

The idea of the proposal here is, simply, have those *access sets* work block wide, instead of transaction wide.

Implementation:

- From EIP_???_FORK_BLOCK onwards, eip-2929 access sets will work within the context of the block.
- they don’t reset when a transaction begins, only when a new block begins.

The implementation sounds easy but it might break a lot of assumptions the execution clients have been doing. For example (i can’t assert this, but…) blocks might not have been required to hold state until now, and this EIP would break the assumption and introduce unwanted complexity.

You can check this file to understand the complexity and technical debt that a Core EIP can inflict upon the clients. [go-ethereum/gas_table.go at ee8e83fa5f6cb261dad2ed0a7bbcde4930c41e6c · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/blob/ee8e83fa5f6cb261dad2ed0a7bbcde4930c41e6c/core/vm/gas_table.go)

