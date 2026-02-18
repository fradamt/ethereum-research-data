---
source: magicians
topic_id: 10784
title: "{shanghai,cancun}-candidate: EIP-1153 Transient Storage"
author: moodysalem
date: "2022-09-09"
category: EIPs
tags: [evm, opcodes, shanghai-candidate, cancun-candidate]
url: https://ethereum-magicians.org/t/shanghai-cancun-candidate-eip-1153-transient-storage/10784
views: 3704
likes: 11
posts_count: 2
---

# {shanghai,cancun}-candidate: EIP-1153 Transient Storage

The current state of the EIP is as follows:

1. The EIP has been implemented in Geth, Nethermind, Besu, EthereumJS, Erigon.
2. Comprehensive EVM tests have been implemented in ethereum/tests. The tests are passing on Geth, Nethermind, Besu, and EthereumJS implementations.
3. A draft PR for assembly opcodes in Solidity has been implemented and tested with Uniswap prototypes
4. Application developers from Uniswap, OpenSea, Optimism, Arbitrum, Paradigm, Celo, OpenZeppelin, Nomad, Primitive have expressed support for the EIP. @holiman’s perspective here.

Related links:

- EIP
- Shanghai Planning · Issue #450 · ethereum/pm · GitHub
- Proposal to include EIP-1153 in Shanghai · Issue #438 · ethereum/pm · GitHub
- EthMagicians discussion

[Here](https://www.youtube.com/watch?v=xFp8RlRq0qU) is a talk I gave at EthCC[5] regarding the primary use case: the “till” pattern. This pattern can be used to reduce token transfers and external calls in future protocols, but requires transient storage in order to be gas-competitive with current patterns due to expensive storage access costs and capped gas refunds. There are many other use cases including (of course) reentrancy locks and rollup L2->L1 transactions. Using transient storage *just for reentrancy locks in Uniswap V2* would have freed up estimated `O(10-100billions)` of gas in block space.

The primary reasons for inclusion are:

- Enables better smart contract design patterns which are more developer friendly (the “till” pattern)
- Saves a lot of gas for existing storage-used-transiently use cases (e.g. reentrancy locks)
- Simplifies the EVM design (storage refunds are complicated)
- Unblocks parallel transaction execution (along with removing self destruct)

And for inclusion in Shanghai/Cancun:

- Already implemented and well tested
- Developers want this yesterday
- “Transient” usage of SSTORE/SLOAD needs to be deprecated for a long time before verkle trees can potentially deprecate storage refunds

## Replies

**pote** (2022-10-14):

Couple updates:

- PR for support in Vyper is out
- Pretty cool use case of non-custodial flash loans

Really cool to see the developer momentum behind this one

