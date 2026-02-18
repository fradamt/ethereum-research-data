---
source: magicians
topic_id: 2270
title: Account-bound EVM memory
author: androlo
date: "2018-12-20"
category: EIPs
tags: [evm, memory]
url: https://ethereum-magicians.org/t/account-bound-evm-memory/2270
views: 1633
likes: 0
posts_count: 3
---

# Account-bound EVM memory

Withdrew PR to flesh it out a bit more. (https: //github .com/ethereum/EIPs/pull/1666)

Transient storage repo, related: https://github.com/androlo/tstorage

Much of this comes from experimenting with transient storage ([EIP-1153: Transient storage opcodes](https://ethereum-magicians.org/t/eip-transient-storage-opcodes/553)).

There are three types of memory involved here:

1. EVM-bound memory - protected memory used by the EVM to store things like call-, and returndata. Can be read from contract code.
2. Account-bound memory - Lasts throughout an entire transaction and can be written to and read from by contract code. Needs special consideration when a revert happens.
3. VM-bound memory. Can only be accessed from a specific VM. Can be written to and read from by contract code.

### Suggestions

- Add a address->Memory map that lasts throughout an entire transaction.
- Keep MLOAD/MSTORE/MSTORE8 as is.
- Add a map, Map to the EVM which binds memories to contract addresses.
- Add instructions TSTORE, TLOAD, TCOPY to work with account-bound memory.
- Change CALLDATALOAD/CALLDATASIZE/CALLDATACOPY to read from accountMemory[0].
- Change RETURNDATASIZE/RETURNDATACOPY to read from accountMemory[0].
- Change call related instructions (CALL, DELEGATECALL, etc.) to write to accountMemory[0].
- Change RETURN/REVERT instructions to write to accountMemory[0].

Note: Address `0x00` of `accountMemory[0]` can be used for data size, and `0x20` and beyond for the data itself. Lifetime of calldata and returndata is now related, and works like returndata does now.

### New instructions

```auto
TLOAD cAddr sAddr
```

`TLOAD`  reads the data stored at address  `sAddr`  in the transient storage of the account with address  `cAddr` .

Example: if the account with address  `0x00...01`  wants to read from its own transient storage at address  `0x20` , in LLL that would be  `(TSTORE 0x00...01 0x20)`

```auto
TSTORE sAddr val
```

Stores the 32 byte value  `val`  at address  `sAddr`  in the account’s own transient storage.

```auto
TCOPY cAddr sAddr mAddr len
```

Copies  `len`  bytes of data from the address  `sAddr`  in the transient storage of account  `cAddr`  to memory address  `mAddr` .

### Notes

The big change is to add a new memory with a different scope, and making other instructions use memory rather then their own special storage locations, instructions, and gas rules. Harmonization + simplification. Also enables reentrancy locks + other things that has to last over an entire transaction.

## Replies

**androlo** (2018-12-22):

With the `0x00` address for length convention, the call-, and returndata instructions would be changed to:

`CALLDATALOAD addr -> TLOAD 0 (addr + 32)`

`CALLDATACOPY addr mAddr len -> TCOPY 0 (addr + 32) mAddr len`

`CALLDATASIZE -> TLOAD 0 0`

`RETURNDATACOPY addr mAddr len -> TCOPY 0 (addr + 32) mAddr len`

`RETURNDATASIZE -> TLOAD 0 0`

---

**androlo** (2018-12-22):

An alternative would be to just move VM-bound memory out of the VM and make it account bound. It would have its own pros and cons.

