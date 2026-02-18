---
source: magicians
topic_id: 21497
title: "EIP-7799: System logs"
author: etan-status
date: "2024-10-29"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7799-system-logs/21497
views: 130
likes: 6
posts_count: 5
---

# EIP-7799: System logs

Discussion topic for EIP-7799 [EIP-7799: System logs](https://eips.ethereum.org/EIPS/eip-7799)

#### Update Log

- 2024-10-29: initial draft https://github.com/ethereum/EIPs/pull/9002

#### External Reviews

None as of 2024-10-29.

#### Outstanding Issues

- 2024-10-29: Whether or not to batch priority fee credits, https://github.com/ethereum/EIPs/pull/9002/files
- 2024-10-29: Details of log data, https://github.com/ethereum/EIPs/pull/9002/files

#### Update Log

- 2025-07-03: Adopt ProgressiveList

## Replies

**jochem-brouwer** (2025-05-11):

This is a very interesting EIP especially in combination with 7708.

Here is some general feedback:

- EIP lists 7708 as required but this is technically not required, so I suggest to remove it
- MAX_LOGS_PER_RECEIPT is necessary for the SSZ type but it is not defined anywhere. NVM this is part of EIP 6466
- Why is the priority fee not credited to coinbase as-is? I understand that this is a transfer which is not logged anywhere, but it can be deduced from every tx in combination with the logs. From cumulativeGasUsed (together with previous receipt) the gas used can be deduced, and the priority fee can be calculated from the tx. So the data is there to calculate this. Alternatively, these priority fee logs could also be inserted after each tx into the system_logs. This will not “change” the behavior of the EVM which I think is an undesired side effect of this EIP (block coinbase does not collect fee during block, but now only after the block has been executed will it receive fees). But this would require all that data as opposed to adding this to the logs. (Then only log data is necessary). EDIT: ok this is motivated a bit more in the Alternatives/Future section
- For clarity, I think the data fields of the eth-transfering events should just be encoded as uint? It should be a representation of bytes which does not have leading zeros in the log.
- Why must the log be added to a genesis block if the EIP is used from the beginning? This will be clear because there is a system_logs_root field, so there is no need to add this log there in the genesis block
- block_header.system_logs_root = system_logs.hash_tree_root() it is not mentioned how the hash tree root should be calculated
- “Batched crediting of priority fees improves parallel execution of transactions, as a transaction can no longer start with insufficient fees”. I don’t see how it was previously possible to start a transaction with insufficient fees (this is not possible)

---

**jochem-brouwer** (2025-05-12):

Disregard my previous post, should first read 6466 in-depth before raising these points

---

**etan-status** (2025-05-12):

1. The goal is to enable fully accurate ETH balance tracking. This EIP alone cannot achieve it without 7708
2. Yes, EIP-6466 contains the definition
3. Emitting a priority fee log after every individual transaction is quite wasteful. Combining them leads to a single log when producing a block. Up for discussion, though, it could be done per transaction to reduce changes if this is the only blocker. Note that the EVM is not changed here, priority fees are credited outside the EVM (after the transaction is executed).
4. The data encoding follows the smart contract ABI convention, it’s similar to ERC-20 encoding
5. If one wants a truly accurate history, genesis ETH has to be tracked as well. New testnets can start with the logs included in the genesis block’s system_logs_root. For other networks, a historical system_logs_root for entries preceding the activation of EIP-7799 can be computed and provided as part of network metadata, so that wallets can provide accurate accounting even for wallets that started with a genesis balance.
6. hash_tree_root is a standard SSZ operation: consensus-specs/ssz/simple-serialize.md at dev · ethereum/consensus-specs · GitHub
7. If priority fees are credited after each tx, the fee recipient can spend the priority fees within the same block. If they are only credited at the end of the block (with a single log), the fee recipient can only spend it from the next block onward. There is the tradeoff of storage space / repeated account access / parallelism, vs. reducing the amount of changes.

---

**etan-status** (2025-07-03):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9975)














####


      `master` ← `etan-status:7799-progressive`




          opened 10:00AM - 03 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/89844309?v=4)
            etan-status](https://github.com/etan-status)



          [+3
            -3](https://github.com/ethereum/EIPs/pull/9975/files)







Use `ProgressiveList` to avoid `MAX_LOGS_PER_RECEIPT` bound.












- Use ProgressiveList to avoid MAX_LOGS_PER_RECEIPT bound.

