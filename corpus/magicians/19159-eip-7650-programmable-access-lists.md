---
source: magicians
topic_id: 19159
title: "EIP-7650: Programmable access lists"
author: qizhou
date: "2024-03-11"
category: EIPs
tags: [evm, gas]
url: https://ethereum-magicians.org/t/eip-7650-programmable-access-lists/19159
views: 1674
likes: 2
posts_count: 9
---

# EIP-7650: Programmable access lists

We introduce a new precompile named `prefetch`, which accepts an `accessList`.

The `accessList` specifies a list of addresses and local storage keys; these addresses and local storage keys are added into the `accessed_addresses` and `accessed_storage_keys` global sets (introduced in EIP-2929. Similar to EIP-2930, prefetching data through this precompile incurs a gas charge, albeit at a reduced rate compared to accesses made outside of this list.

https://github.com/ethereum/EIPs/pull/8300

## Replies

**drllau** (2024-03-12):

What problem is this supposed to address? If it is purely gas charges then Arbitrum’s orbit allows you to redefine gas for any operation.If it is supposed to be a caching function (local vs non-local) then presumably there is a different temporal access pattern … are you suggesting the accessed_{address/storage) be “fixed/static” during the optimistic execution phase but might be different if reverted?

---

**qizhou** (2024-03-12):

Gas price change in EVM has to reflect actual storage read cost (especially in terms of IO latency).   Without increasing IO latency, a simple optimization is to read multiple storage data in parallel.  For example, a modern NVME disk can easily support 10 or even more concurrent IOs without sacrificing the latency.  As a result, we can reduce the gas cost of reading N storage data from 2100 * N to 2100 if we assume the node can support > N parallel reads without increasing the IO latency.

To employ IO parallelization, the access list is a simple existing solution in the EVM (as introduced in EIP-2929/2930).  Unfortunately, the access list is not widely adopted, according to the paper here [[2312.06574] Dissecting the EIP-2930 Optional Access Lists](https://arxiv.org/abs/2312.06574), only 1.46% of transactions use access lists.  This EIP’s main motivation is to push access list adoption further.  Allowing a smart contract to program an access list (and thus cache the data of the access list in EVM) will have a sustained adoption of access lists and then harvest the gas cost reduction constantly.

For example, suppose that most nodes can perform N = 5 parallel SLOADs without increasing IO latency, then we can safely use the same gas cost (2100 for SLOAD) for 5 SLOADs in parallel.

As a concrete example, for the following uniswap swap code

```auto
    // this low-level function should be called from a contract which performs important safety checks
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external lock {
        prefetch {
             token0.slot,
             token1.slot,
             reserve0.slot,
             price0CumulativeLast.slot,
             price1CumulativeLast.slot,
        } // add the storage keys `accessed_storage_keys`
        prefetch {
             token0,
             token1,
        } // add the contracts of token0 and token1 to `accessed_addresses`
        ...
    }
```

the gas cost can be reduced from  `2100 * 5 + 2600 * 2 = 15700` to  `2100 + 2600 = 4700` saving about 10,000 per swap with the proposed parallel read optimization in EVM.

---

**matt** (2024-03-12):

Fwiw, I don’t think this makes sense as a precompile. Precompiles generally do pure computation. This would make more sense as an opcode.

---

**qizhou** (2024-03-14):

I agree that opcode may be a preferred choice.

The main benefit of a precompile is that a contract can be compiled once and deployed to any chain no matter whether the EVM has adopted this EIP or not.

---

**dror** (2024-03-15):

I want to understand what is the motivation behind this one: simply save gas?

The idea behind `access_list` is that it is beneficial to the nodes to know in advance (prior execution) what storage cells a transaction accesses.

For this advanced knowledge, a incentive is given as a gas reduction.

What is the incentive to give the same gas reduction during execution ?

---

**qizhou** (2024-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> For this advanced knowledge, a incentive is given as a gas reduction.

The issue with the current access list in EIP-2930 is that it is optional, and only 1.45% of transactions use this feature ([[2312.06574] Dissecting the EIP-2930 Optional Access Lists](https://arxiv.org/abs/2312.06574)).  The motivation of this EIP is to allow the contract to harvest a sustained gas reduction by providing a programmable access list.  In this uniswapv2 swap case, given some mild concurrency of a node, we can predict a constant 10,000 gas reduction.

Of course, if a tx includes the access list in the tx itself, then the benefit will fade away.

---

**wminshew** (2024-03-26):

why not just propose bumping the gas savings for 2930?

---

**qizhou** (2024-03-27):

Good point!  Assuming the parallel preloading results in lower read latency, I believe the gas saving for 2930 should be adjusted accordingly.

One noticeable thing is the access list’s data cost since it is part of tx.  Given [EIP-7623: Increase calldata cost](https://eips.ethereum.org/EIPS/eip-7623) where per non-zero byte gas is 68, then we have

- the address data cost is about 68 * 20 = 1360 (vs 2930’s address cost is 2400); and
- the storage data cost is about 68 * 32 = 2176 (vs 2930’s storage cost is 1900).
This implies that the room to reduce the gas cost for the storage access list is limited to 2930 if EIP 7620 is taking account.  What do you think @vbuterin?

