---
source: magicians
topic_id: 20052
title: "EIP-7709: Read BLOCKHASH opcode from storage and adjust gas cost"
author: gabrocheleau
date: "2024-05-20"
category: EIPs > EIPs core
tags: [opcodes, gas]
url: https://ethereum-magicians.org/t/eip-7709-read-blockhash-opcode-from-storage-and-adjust-gas-cost/20052
views: 922
likes: 2
posts_count: 1
---

# EIP-7709: Read BLOCKHASH opcode from storage and adjust gas cost

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/8578)














####


      `master` ← `gabrocheleau:eip/verkle-blockhash-ring-buffer`




          opened 04:08PM - 18 May 24 UTC



          [![](https://avatars.githubusercontent.com/u/18757482?v=4)
            gabrocheleau](https://github.com/gabrocheleau)



          [+101
            -0](https://github.com/ethereum/EIPs/pull/8578/files)







This EIP extracts the following verkle-specific behavior into a separate EIP to […](https://github.com/ethereum/EIPs/pull/8578)be included in a subsequent hard-fork (the verkle hard fork).

### Changes

- Updates the behavior of the BLOCKHASH opcode, which should now be served from the system contract storage
- Updates the gas cost of the BLOCKHASH opcode to reflect the cost of an SLOAD operation
- Specifies that BLOCKHASH storage accesses should be contained in the verkle execution witness

### Links
- [Ethereum Magicians thread](https://ethereum-magicians.org/t/eip-7709-read-blockhash-opcode-from-storage-and-adjust-gas-cost/20052)












## Abstract

Adjust the BLOCKHASH opcode to read from storage, and increase its gas cost.

## Motivation

The `BLOCKHASH (0x40)` opcode currently assumes that the client has stateful knowledge of the previous blocks, which is a blocker for stateless execution (e.g. in the context of Verkle). This EIP assumes that EIP-2935 has been implemented, and that blockhashes can be retrieved from the systems contract storage. By updating the behavior of `BLOCKHASH (0x40)` to directly read and serve from state through the system contract storage, we allow Verkle blocks to include a storage access witness, which will allow stateless execution.

The motivation behind the updated gas cost is to match the real cost of the operation, which is equivalent to an `SLOAD`.

## Open Questions

- When providing access witnesses. Should only the storage witness be provided, or also the account witness?
- Related to the above, it has been mentioned that the storage slot that has been updated at the beginning of the block processing (i.e. the blockhash of the parent block) should be considered warm. Should it actually be considered warm? And should the corresponding account also be considered warm, or only the storage slot?
