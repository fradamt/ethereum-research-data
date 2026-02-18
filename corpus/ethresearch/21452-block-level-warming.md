---
source: ethresearch
topic_id: 21452
title: Block-Level Warming
author: Nero_eth
date: "2025-01-16"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/block-level-warming/21452
views: 1009
likes: 18
posts_count: 11
---

# Block-Level Warming

# Block-Level Warming

The proposal is to introduce block-level address and storage key warming, allowing accessed addresses and storage keys to maintain their “warm” status throughout an entire block’s execution. Accessed slots can be effectively cached at the block level, allowing for this optimization.

Furthermore, a future transition to multi-block warming could unlock additional potential.

## Motivation

Currently, the EVM’s storage slot warming mechanism operates at the transaction level, requiring each transaction to “warm up” slots independently, even when accessing the same storage locations within the same block. This design doesn’t take advantage of the fact that modern node implementations can effectively cache storage access patterns at the block level. By extending the slot warming duration to the block level, we can:

1. Reduce redundant warming costs for frequently accessed slots
2. Better align gas costs with actual computational overhead
3. Improve overall network throughput without compromising security

## Impact Analysis

For the following, I analyze 22,272 blocks between 12 and 15 January 2025. The opcodes relevant for this analysis are those that distinguish between “warm” and “cold” access: These are SSTORE, SLOAD, BALANCE, EXTCODESIZE, EXTCODECOPY, EXTCODEHASH, CALL, CALLCODE, DELEGATECALL and STATICCALL.

The code used for conducting this analysis can be found [here](https://github.com/nerolation/blk-lvl-warming-analysis).

### Unlocking Potential

Block-level warming presents an immediate opportunity to achieve 5-6% efficiency gains in gas consumption.

An initial analysis shows significant improvements in efficiency when comparing block-level warming to the current situation. In typical blocks consuming 15m gas, block-level warming could save approximately 0.5-1m gas per block - gas which would otherwise be spent on warming addresses and storage keys that were already accessed earlier in the block.

Even more promising results emerge when we extend the warming window. When accessed addresses and storage keys remain warm for 5 blocks, we can observe savings of up to 1.5m gas (~10%), as illustrated in the green line of the following chart:

[![save_over_time (4)](https://ethresear.ch/uploads/default/optimized/3X/4/c/4c0671f78c5f7e995b51d39adfeade9f41966de8_2_690x383.png)save_over_time (4)900×500 66.8 KB](https://ethresear.ch/uploads/default/4c0671f78c5f7e995b51d39adfeade9f41966de8)

The length of the warming window significantly impacts potential efficiency gains. This analysis shows that:

- A 5-block warming window yields approximately 10% gas savings
- Extending to 15 blocks increases savings to 15%

This relationship between window size and efficiency gains is demonstrated here:

[![slot_warming_potential (1)](https://ethresear.ch/uploads/default/optimized/3X/7/2/72a383c5f1f174b5ead715f4893d97858a7d3f9a_2_690x492.png)slot_warming_potential (1)700×500 23.3 KB](https://ethresear.ch/uploads/default/72a383c5f1f174b5ead715f4893d97858a7d3f9a)

To understand the maximum potential of this approach, we compared these results against a theoretical scenario where all addresses and storage keys remain permanently warm (eliminating all cold access costs):

[![slot_warming_potential_2 (2)](https://ethresear.ch/uploads/default/optimized/3X/a/8/a867d5000806260a13800aefd458438c09a5e1cb_2_690x492.png)slot_warming_potential_2 (2)700×500 22.2 KB](https://ethresear.ch/uploads/default/a867d5000806260a13800aefd458438c09a5e1cb)

This comparison highlights that over 35% of current gas consumption is attributed to the costs of warming addresses and storage keys. The efficiency curve shows a steep initial improvement before quickly plateauing, suggesting that even relatively short warming windows can capture a significant portion of the potential benefits.

Among the most popular addresses and storage slots we find candidates such as WETH, USDC and Uniswap. However, there are also less obvious contracts (e.g., `0x399121f5b1bab4432ff8dd2ac23e5f6641e6f309`) that primarily serve to burn gas (via warm SSTOREs). This tactic is used to circumvent on-chain priority gas limits, thereby increasing the total priority fees paid to the transaction’s fee recipient. For an example, see this [transaction](https://dashboard.tenderly.co/tx/mainnet/0x9eac0ada21d56e2e2adf8a36661baa5668b29e79424044b05447096b67d4c94d).

## Specification

### Mechanics

When a storage slot is accessed within a block:

1. The first access to a slot in a block incurs the cold access cost as of EIP-2929.
2. All subsequent accesses to the same slot within the same block incur only the warm access cost as of EIP-2929.
3. The warm/cold status resets at block boundaries

### Block Processing

1. At the start of each block:

Initialize two empty sets block_level_accessed_addresses and block_level_accessed_storage_keys
2. For each transaction in the block:

Before processing storage access:

Check if touched address is in block_level_accessed_addresses
3. If yes: charge GAS_WARM_ACCESS
4. If no:

Charge GAS_COLD_ACCOUNT_ACCESS
5. Add address to block_level_accessed_addresses
6. Check if storage key is in block_level_accessed_storage_keys
7. If yes: charge GAS_WARM_ACCESS
8. If no:

Charge GAS_COLD_SLOAD
9. Add storage key to block_level_accessed_storage_keys

### Implementation Details

> The following uses the ethereum/execution-specs. Find a first draft implementation here.

The proposal modifies the block execution process to maintain block-level sets of accessed addresses and storage slots.

#### Block-Level Storage Management

```python
def apply_body(...):
    # Initialize block-level tracking sets
    block_level_accessed_addresses = set()
    block_level_accessed_storage_keys = set()

    for i, tx in enumerate(map(decode_transaction, transactions)):
        # Create environment with block-level context
        env = vm.Environment(
            # ... other parameters ...
            block_level_accessed_addresses=block_level_accessed_addresses,
            block_level_accessed_storage_keys=block_level_accessed_storage_keys
        )

        # Process transaction and update block-level sets
        gas_used, accessed_addresses, accessed_storage_keys, logs, error = process_transaction(env, tx)
        block_level_accessed_addresses += accessed_addresses
        block_level_accessed_storage_keys += accessed_storage_keys
```

This code illustrates the implementation of block-level slot warming at the execution layer. The `block_level_accessed_addresses` and `block_level_accessed_storage_keys` sets are maintained throughout the block’s execution and passed to each transaction’s environment.

#### Transaction Processing

```python
def process_transaction(env: vm.Environment, tx: Transaction) -> Tuple[Uint, Tuple[Log, ...], Optional[Exception]]:
    preaccessed_addresses = set()
    preaccessed_storage_keys = set()

    # Add block-level pre-accessed slots
    preaccessed_addresses.add(env.block_level_accessed_addresses)
    preaccessed_storage_keys.add(env.block_level_accessed_storage_keys)

    # Handle access lists from transaction
    ...
```

This adds the block-level accessed addresses and storage keys to the preaccessed addresses and storage keys.

As a result, from the perspective of a transaction, block-level accessed addresses and storage keys are treated the same as precompiles or the coinbase address.

```python
def process_message_call(message: Message, env: Environment) -> MessageCallOutput:
    return MessageCallOutput(
        # ... other fields ...
        accessed_addresses=evm.accessed_addresses,
        accessed_storage_keys=evm.accessed_storage_keys
    )
```

The message call processing tracks accessed addresses and storage keys during execution, which are then propagated back up to the transaction level and ultimately to the block level.

## Rationale

The proposal builds on several key observations:

1. Caching Efficiency: Today’s Ethereum clients already implement sophisticated caching mechanisms at the block level. Extending address and storage key warming to match this caching behavior better aligns gas costs with actual computational costs.
2. Backward Compatibility: The worst-case scenario for any transaction remains unchanged - it will never pay more than the current cold access cost for its first access to a slot.
3. First Access Warming System
The proposed mechanism operates on a “first warms for all” principle: when a transaction first accesses and warms multiple addresses or storage slots in a block, it bears the entire warming cost. Subsequent transactions can then access these warmed slots without additional costs.
This approach aligns well with current dynamics, as early block positions are typically occupied by professional builders who specifically target top-of-block execution. Since the cost difference is relatively minor, this straightforward approach is preferred over more complex alternatives aimed at better fairness.
An alternative approach would distribute warming costs across all transactions within a block that access the same slots. Under this system:

Each transaction would initially pay the full cold access cost
4. After block execution completes, these costs would be evenly distributed among all transactions that accessed the slots
5. The excess payments would then be refunded to transaction originators
6. Alternative Block Warming Windows: Instead of applying warming at the block level, more advanced multi-block warming approaches can be considered. Potential options include:

Warming addresses and storage keys over the duration of an epoch
7. Using a ring buffer spanning x blocks

## Reference Implementation

Find a first draft implementation of block-level warming here:


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/nerolation/execution-specs/tree/block-level-warming)





###



[block-level-warming](https://github.com/nerolation/execution-specs/tree/block-level-warming)



Specification for the Execution Layer. Tracking network upgrades.










## Related work:

- https://www.usenix.org/conference/fast25/presentation/he
- Add EIP: Block-level Warming by forshtat · Pull Request #7968 · ethereum/EIPs · GitHub
- Block access list
- Proper disk i/o gas pricing via LRU cache

## Replies

**pipermerriam** (2025-01-16):

In the multi-block form, I think this would mean that stateless would then need to not only provide the state for the current block, but that either:

- Proofs would need to span multiple blocks.
- Clients would need to aggregate proofs for multiple blocks or maintain state across multiple blocks.

The single block case shouldn’t effect stateless.  I think the multi-block version is a no-go for stateless.

---

**terence** (2025-01-16):

Awesome!

In your current proposal, I think it’s assuming the cache is unbounded in size, but realistically the cache will have to be bounded, or it could lead to a DOS attack on the memory. What do you think the cache size should be to achieve the same gain? and how does the protocol update the cache size?

---

**Nero_eth** (2025-01-16):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> In your current proposal, I think it’s assuming the cache is unbounded in size, but realistically the cache will have to be bounded, or it could lead to a DOS attack on the memory. What do you think the cache size should be to achieve the same gain? and how does the protocol update the cache size?

It’s already implicitly bounded by the block gas limit.

We can do \frac{30{,}000{,}000}{22{,}100}\approx 1357 cold SSTORE writes in a single block.

Each storage key (32 bytes) holding 32 bytes, so the maximum cache size is \approx 1357 \times 64 \approx 86.8\,\text{KB} (per block).

By leveraging refunds from zero’ing storage slots, I’m certain on could build a block that uses even more but in the end there is already a limit the cache can grow every block.

If clients do want to have size limits, they must coordinate on it or make sure it’s higher than the “natural” limit imposed through the block gas limit.

---

**terence** (2025-01-17):

Thanks! What I meant is that different client implementations should have a consensus on the max size, but using the block gas limit as the worst case makes sense.

Another question: In a multiple-block setting, are we writing any of the cache data into the state as part of the consensus? Meaning, does anything carry over between blocks and get represented as part of the state root?

---

**Nero_eth** (2025-01-17):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Thanks! What I meant is that different client implementations should have a consensus on the max size, but using the block gas limit as the worst case makes sense.

Yeah, agree!

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> In a multiple-block setting, are we writing any of the cache data into the state as part of the consensus?

Multi-block is still in the early stages of the thought process, but I believe we should avoid putting any references to the cache into the state, as this would enforce finding consensus on it. That said, I’m not entirely sure if avoiding it is feasible.

One idea that comes to mind is maintaining a ring buffer in the state to store the last `x` access lists of blocks (=list which addresses and storage keys were accessed), which can be derived during block execution. For example:

```python
buffer = list()
buffer_length = 10

for each block_number:
    buffer[block_number % buffer_length] = set(access_list[block_number])
```

When you need the access lists for execution, you can combine them like this:

```python
multi_block_cache = set.union(*state.buffer)
```

I initially thought of this approach as a way to ensure that cached accounts and storage keys are replaced with new ones in the event of reorgs.

Curious to hear your thoughts on the pros and cons of putting it into state.

---

**terence** (2025-01-17):

When I first considered this problem, my initial reaction was to add the access list to the block header. It would then be the proposer’s additional duty to provide the block’s access list, and the state transition function would check its correctness. I liked this approach because it allows for somewhat optimistic parallel execution, enabling client implementations to have multiple transaction pipelines. However, I understand that this approach is more involved and complex.

Alternatively, you could use a ring buffer, as you mentioned, or implement some kind of caching metadata system contract. If user-space contracts need this information, a precompile could also be provided. I do agree with you that I think we need to persist caching information across blocks and it probably needs to be part of consensus

---

**jochem-brouwer** (2025-01-18):

Just a small point regarding the cache size:

I’d argue that if a DoS vector regarding the cache currently fails, then it also fails if we implement the current idea of this EIP (1-block warming). The reason is that EIP-2929 considers accounts/slots “cold” if these are taken from disk and will then mark them as warm. The cheaper gas cost reflects that the data does not have to be read from disk anymore (the details are a bit more complex regarding reverting the warm accounts/slots in case a subcall fails, but the details of this are in EIP-2929).

A point here could be: if we expand the scope of warm accounts/slots from tx to block, then this will increase the max cache size. This is not true: one could also craft a tx with a gas limit set to the block gas limit where the cache would still govern at the tx-level. So, the max cache size would not increase if we add block-level warming. The max cache size is obviously still dependent on the gas limit of the block.

---

**benaadams** (2025-03-14):

Not sure what this solves?

As a user it gives you a random gas reduction you aren’t expecting and cannot predict? So it won’t effect behaviour (you need to already agreed to full price); and with a lot of tx being private order flow even the most advanced user can’t try and get these discounts by looking at the mempool.

For multi transactions of your own hitting the same address; 7702 now provides a mechanism to combine these into one tx, meaning it doesn’t help there either as they will get the intra-tx warming benefits already.

---

**Nero_eth** (2025-03-15):

In practice, average users would benefit from many commonly used storage keys and addresses being pre-warmed by transactions at the top of the block.

Since transactions are packed cumulatively, a reduction in gas usage for one transaction creates room for additional transactions, without necessarily impacting user behavior. Builders can still construct blocks with more transactions.

I’ve removed the EIP from the “Proposed for Pectra” status. Realistically, it still requires further research, and its efficiency gains may be smaller compared to other proposals, such as block-level access lists or delayed execution.

---

**benaadams** (2025-03-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> In practice, average users would benefit from many commonly used storage keys and addresses being pre-warmed by transactions at the top of the block.

I acknowledge this; but it would be a post-inclusion effect.

So the user would have estimated gas at the higher amount and accepted that price and they couldn’t expect the refund (as depends on other txs). Mostly am wonder if the approach could be altered in some way to be more impactful and behaviour modifying (but then it would also need to be predictable)

