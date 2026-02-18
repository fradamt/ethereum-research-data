---
source: magicians
topic_id: 15662
title: "ERC-7511: Minimal Proxy Contract with PUSH0"
author: 0xAA
date: "2023-09-05"
category: EIPs
tags: [evm, opcodes, gas]
url: https://ethereum-magicians.org/t/erc-7511-minimal-proxy-contract-with-push0/15662
views: 2026
likes: 8
posts_count: 3
---

# ERC-7511: Minimal Proxy Contract with PUSH0

## Simple Summary

With the newly introduced `PUSH0` opcode ([eip-3855](https://eips.ethereum.org/EIPS/eip-3855)) at Shanghai Upgrade, we minimized the previous Minimal Proxy Contract ([eip-1167](https://eips.ethereum.org/EIPS/eip-1167)) by 200 gas at deployment and 5 gas at runtime, while remain the same functionalities.

## Specification

### Standard Proxy Contract

The exact runtime code for the minimal proxy contract with `PUSH0` is:

```auto
365f5f375f5f365f73bebebebebebebebebebebebebebebebebebebebe5af43d5f5f3e5f3d91602a57fd5bf3
```

wherein the bytes at indices 9 - 28 (inclusive) are replaced with the 20 byte address of the master implementation contract. The length of the runtime code is `44` bytes.

The disassembly of the new minimal proxy contract code:

```shell
| pc   | op     | opcode         | stack              |
|------|--------|----------------|--------------------|
| [00] | 36     | CALLDATASIZE   | cds                |
| [01] | 5f     | PUSH0          | 0 cds              |
| [02] | 5f     | PUSH0          | 0 0 cds            |
| [03] | 37     | CALLDATACOPY   |                    |
| [04] | 5f     | PUSH0          | 0                  |
| [05] | 5f     | PUSH0          | 0 0                |
| [06] | 36     | CALLDATASIZE   | cds 0 0            |
| [07] | 5f     | PUSH0          | 0 cds 0 0          |
| [08] | 73bebe.| PUSH20 0xbebe. | 0xbebe. 0 cds 0 0  |
| [1d] | 5a     | GAS            | gas 0xbebe. 0 cds 0 0|
| [1e] | f4     | DELEGATECALL   | suc                |
| [1f] | 3d     | RETURNDATASIZE | rds suc            |
| [20] | 5f     | PUSH0          | 0 rds suc          |
| [21] | 5f     | PUSH0          | 0 0 rds suc        |
| [22] | 3e     | RETURNDATACOPY | suc                |
| [23] | 5f     | PUSH0          | 0 suc              |
| [24] | 3d     | RETURNDATASIZE | rds 0 suc          |
| [25] | 91     | SWAP2          | suc 0 rds          |
| [26] | 602a   | PUSH1 0x2a     | 0x2a suc 0 rds     |
| [27] | 57     | JUMPI          | 0 rds              |
| [29] | fd     | REVERT         |                    |
| [2a] | 5b     | JUMPDEST       | 0 rds              |
| [2b] | f3     | RETURN         |                    |
```

### Minimal Creation Code

The minimal creation code of the minimal proxy contract is:

```auto
602c8060095f395ff3365f5f375f5f365f73bebebebebebebebebebebebebebebebebebebebe5af43d5f5f3e5f3d91602a57fd5bf3
```

where the first 9 bytes are the initcode:

```auto
602c8060095f395ff3
```

And the rest are runtime/contract code of the proxy. The length of the creation code is `53` bytes.

## Implementation

GitHub repo Clone0: [GitHub - AmazingAng/Clone0: Clone0 optimize the previous Minimal Proxy Contract (eip-3855) with `PUSH0` opcodes, saving 200 gas at deployment and 5 gas at runtime.](https://github.com/AmazingAng/Minimal-Proxy-PUSH0)

## Backwards Compatibility

Because the new minimal proxy contract uses `PUSH0` opcode, it can only be deployed after Shanghai Upgrade. It behaves the same as previous Minimal Proxy Contract.

## Test Cases

Test cases are performed using Foundry, which include:

- invocation with no arguments.
- invocation with arguments.
- invocation with fixed length return values
- invocation with variable length return values
- invocation with revert
- deploy with minimal creation code (tested on Goerli testnet, link)

Tests for these cases are included in the GitHub repo [Minimal Proxy PUSH0](https://github.com/AmazingAng/Minimal-Proxy-PUSH0).

## Reference

1. Peter Murray (@yarrumretep), Nate Welch (@flygoing), Joe Messerman (@JAMesserman), “ERC-1167: Minimal Proxy Contract,” Ethereum Improvement Proposals, no. 1167, June 2018. [Online serial]. Available: ERC-1167: Minimal Proxy Contract.
2. Alex Beregszaszi (@axic), Hugo De la cruz (@hugo-dc), Paweł Bylica (@chfast), “EIP-3855: PUSH0 instruction,” Ethereum Improvement Proposals, no. 3855, February 2021. [Online serial]. Available: EIP-3855: PUSH0 instruction.
3. Martin Abbatemarco, Deep dive into the Minimal Proxy contract, Deep dive into the Minimal Proxy contract - OpenZeppelin blog
4. 0age, The More-Minimal Proxy, https://medium.com/@0age/the-more-minimal-proxy-5756ae08ee48

## Replies

**0xAA** (2023-09-09):

The draft for ERC-7511 can be found at: [ERC-7511: Minimal Proxy Contract with PUSH0](https://eips.ethereum.org/EIPS/eip-7511)

Next step: we will add Solady’s implementation of Minimal Proxy Contract with PUSH0 to the draft.

---

**0xAA** (2024-10-16):

evmrobot ([evmrobot.com](http://evmrobot.com)) now support erc7511, showing there is 2,400 erc7511 minimal proxy deployed on Ethereum mainnet.

Dune dashboard: https://dune.com/patronumlabs/erc-7511-minimal-proxy

[![ZakMbF-V](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7455d6ca21902fd4d4478c0f62f74f3bac69a52b_2_690x362.jpeg)ZakMbF-V1200×630 73.8 KB](https://ethereum-magicians.org/uploads/default/7455d6ca21902fd4d4478c0f62f74f3bac69a52b)

