---
source: magicians
topic_id: 19448
title: "EIP-7686: Linear EVM memory limits"
author: vbuterin
date: "2024-03-31"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7686-linear-evm-memory-limits/19448
views: 1742
likes: 8
posts_count: 7
---

# EIP-7686: Linear EVM memory limits

Add a hard memory limit equal to the gas limit of the current context. Make the maximum gas cost of a sub-call depend on the memory used in the current context. The two rules together ensure that a transaction with N gas can use at most N bytes of memory.

## Replies

**wjmelements** (2024-04-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> The two rules together ensure that a transaction with N gas can use at most N bytes of memory.

Consider the quine program:

```auto
CODECOPY(0,0,CODESIZE)
RETURN(0,CODESIZE)
```

This program would normally need 32 bytes of memory to return seven bytes of data because `MSIZE` increases by word, but it only needs 19 gas to execute. So your change will require 32 gas provided but only needs 19. It is cases like this that demonstrate that this limit harms small memory users not large ones.

~~Concerns about memory abuse are already addressed by the quadratic term. There does not need to be an additional limit.~~

Edit: This EIP actually removes the quadratic term which is nice.

---

**qizhou** (2024-04-07):

I am glad to see this EIP to improve the EVM memory limit.  This is very helpful in ERC-4804 which turns EVM into a decentralized HTTP server - the EVM can process much larger HTTP request/response with the increased memory limit.

One security concern is the potential out-of-memory (OOM) attack using `eth_call` JSON-RPC - e.g., Infura allows `eth_call` to accept 10x gas limit, i.e., `300e6` given the current block limit `30e6`.  That means an `eth_call` JSON-RPC can use up to ~300MB of memory.  Depending on the concurrency of a client allowed (e.g., Erigon supports 4k/s, and reth supports 10k/s, See [Releasing Reth!](https://www.paradigm.xyz/2023/06/reth-alpha)), 1k concurrent `eth_call` calls will consume 1k * 300MB = 300 GB in the worst case, which may exceed the memory size of most of the nodes.

I think it is worth noting in the `Security Considerations` that a client should implement a proper rate limit of `eth_call` (and `eth_estimateGas`) to prevent the OOM attack.

BTW: from

```auto
def max_call_gas(gas, memory_byte_size):
    return gas - max(gas // 64, memory_byte_size)
```

It is possible that max_call_gas become negative?

---

**vbuterin** (2024-04-11):

> It is possible that max_call_gas become negative?

If this is true, then the call should fail. But you’re right that it’s worth specifying explicitly.

> One security concern is the potential out-of-memory (OOM) attack using eth_call JSON-RPC - e.g., Infura allows eth_call to accept 10x gas limit, i.e., 300e6 given the current block limit 30e6

This is also true today, right? I suppose today technically the memory limit is some weird function approximately proportional to sqrt rather than linear, so the memory consumption increases more slowly?

Are there any actual use cases of `eth_call` with supersized gas limits? Could the gas limit cap be decreased?

---

**qizhou** (2024-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> I suppose today technically the memory limit is some weird function approximately proportional to sqrt rather than linear, so the memory consumption increases more slowly?

I make a lookup table below, and the current memory limit of 300e6 gas limit is about 12MB.

| Size (KB) | Linear Gas Term | Quadratic Gas Term | Sum |
| --- | --- | --- | --- |
| 1 | 96 | 2 | 98 |
| 4 | 384 | 32 | 416 |
| 16 | 1,536 | 512 | 2,048 |
| 32 | 3,072 | 2,048 | 5,120 |
| 64 | 6,144 | 8,192 | 14,336 |
| 128 | 12,288 | 32,768 | 45,056 |
| 256 | 24,576 | 131,072 | 155,648 |
| 512 | 49,152 | 524,288 | 573,440 |
| 1,024 | 98,304 | 2,097,152 | 2,195,456 |
| 3,849 | 369,504 | 29,629,602 | 29,999,106 |
| 12,223 | 1,173,408 | 298,803,458 | 299,976,866 |

Note that, one interesting attack to bypass the existing quadratic term is to spread the memory to multiple call stacks. E.g., I can allocate 1MB to two call stacks, each allocating 512KB instead of 1MB in one call stack.  As a result, the memory gas cost is reduced from `2,915,456` to `573,440 * 2 = 1,146,880`.

Taking gas limit = 300e6 as an example, recursively calling a contract that allocates 256KB in each call stack can allocate `54MB` of total memory, which is still much smaller than `300MB` of this EIP.

```python
gas_limit = 300 * 10 ** 6
mem_size = 0
while gas_limit >= 155648:
    mem_size = mem_size + 256 * 1024
    gas_limit = (gas_limit - 155648) * 63 // 64
mem_size # return 57409536 ~ 54MB
```

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Are there any actual use cases of eth_call with supersized gas limits? Could the gas limit cap be decreased?

The 10x cap of Infura can be found [here](https://docs.infura.io/api/networks/ethereum/json-rpc-methods/eth_call). Alchemy has an even higher gas limit of [550M](https://docs.alchemy.com/reference/eth-call).

One application as I mentioned is EVM as a decentralized HTTP server in ERC-4804/6860, where an `eth_call` may return a large composed HTML from EVM (potentially call an L2 to have lower storage cost).  There may be other applications that I am not aware of.

---

**charles-cooper** (2025-03-23):

I think one issue with this EIP is that it breaks an important invariant: subcalls now have a memory limit which is not predictable and depends on how much memory their callers used.

For instance if you wanted to build a traditional ‘stack’ and ‘heap’ structure, you would want to start the stack from “end of mem”. But end of mem is not predictable, so I’m not sure it enables this use case.

---

**charles-cooper** (2025-03-28):

I’ve drafted an EIP which has linear pricing, and but avoids the subcall upper bound invariant: [EIP: Linearize Memory Costing](https://ethereum-magicians.org/t/eip-linearize-memory-costing/23290)

Per [@qizhou](/u/qizhou)’s comments, it might make sense to add a (transaction-)global limit to the memory usage, on the order of 64-128MB.

