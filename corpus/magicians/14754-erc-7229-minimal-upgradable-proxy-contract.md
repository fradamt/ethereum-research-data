---
source: magicians
topic_id: 14754
title: "ERC-7229: Minimal upgradable proxy contract"
author: xiaobaiskill
date: "2023-06-20"
category: EIPs
tags: [erc, evm, opcodes, gas]
url: https://ethereum-magicians.org/t/erc-7229-minimal-upgradable-proxy-contract/14754
views: 1890
likes: 7
posts_count: 17
---

# ERC-7229: Minimal upgradable proxy contract

Discussion thread for https://github.com/ethereum/EIPs/pull/7229

The Minimal Upgradable Proxy contract is a lightweight contract upgrade pattern designed to save gas costs while providing the ability to upgrade contracts.

## 1 Standard Proxy

### 1.1 evm opcode

In the following EVM code, the `PUSH0` instruction (EIP-3855) is used. As of 2023-06-23, the BSC chain does not support EIP-3855 yet.

```auto
# store logic address to slot of proxy contract
PUSH32           [slot]
PUSH20   [logicAddress slot]
DUP2                   [slot logicAddress slot]
SSTORE                 [slot]          => storage(slot => logicAddress)

# return deployedCode
PUSH1 0x9              [0x9 slot]
PUSH1 0x4c             [0x4c 0x9 slot]
PUSH0                  [00 0x4c 0x9 slot]
CODECOPY               [slot]          ==> memory(0x00~0x8: 0x4c~0x54(deployedCode1stPart))
PUSH1 0x9              [0x9 slot]
MSTORE                 []              ==> memory(0x9~0x28: slot(deployedCode2ndPart))
PUSH1 0x10             [0x10]
PUSH1 0x55             [0x55 0x10]
PUSH1 0x29             [0x29 0x55 0x10]
CODECOPY               []              ==> memory(0x29~0x38: 0x55~0x64(deployedCode3rdPart))
PUSH1 0x39             [0x39]
PUSH0                  [00 0x39]
RETURN

# proxy contract (deployedcode)
CALLDATASIZE        [calldatasize]
PUSH0               [00 calldatasize]
PUSH0               [00 00 calldatasize]
CALLDATACOPY        []     ==> memory(00~(calldatasize-1) => codedata)
PUSH0               [00]
PUSH0               [00 00]
CALLDATASIZE        [calldatasize 00 00]
PUSH0               [00 calldatasize 00 00]
PUSH32              [slot 00 calldatasize 00 00]
SLOAD               [logicAddress 00 calldatasize 00 00]
GAS                 [gas logicAddress 00 calldatasize 00 00]
DELEGATECALL        [result]
RETURNDATASIZE      [returnDataSize result]
PUSH0               [00 returnDataSize result]
PUSH0               [00 00 returnDataSize result]
RETURNDATACOPY      [result] => memory(00~(RETURNDATASIZE - 1) => RETURNDATA)
RETURNDATASIZE      [returnDataSize result]
PUSH0               [00 returnDataSize result]
DUP3                [result 00 returnDataSize result]
PUSH1 0x37          [0x37 result 00 returnDataSize result]
JUMPI				[00 returnDataSize result]
REVERT              [result]
JUMPDEST            [00 returnDataSize result]
RETURN              [result]
```

### 1.2 evm opcode to code

- bytecode

replace `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` to a slot of 32bytes and replace `yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy` to a address of 20bytes before deploying contract

```auto
7fxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx73yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy81556009604c3d396009526010605560293960395ff3365f5f375f5f365f7f545af43d5f5f3e3d5f82603757fd5bf3
```

- deployedcode

wherein the bytes at indices 9 - 40 (inclusive) are replaced with the 32 byte slot of the master after created

```auto
365f5f375f5f365f7fxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx545af43d5f5f3e3d5f82603757fd5bf3
```

## 2 Storage slot of logic address optimization

To further optimize the minimal upgradeable proxy by controlling the slot value for the logic address within the range of 255(inclusive), you can use the following opcode to reduce gas consumption:

### 2.1 evm opcode

```auto
# store logic address to slot of proxy contract
PUSH1            [slot]
PUSH20   [logicAddress slot]
DUP2                   [slot logicAddress slot]
SSTORE                 [slot]          => storage(slot => logicAddress)

# return deployedCode
PUSH1 0x9              [0x9 slot]
PUSH1 0x30             [0x30 0x9 slot]
PUSH0                  [00 0x30 0x9 slot]
CODECOPY               [slot]          ==> memory(0x00~0x8: 0x30~0x54(deployedCode1stPart))
PUSH1 0xf8             [0xf8 slot]
SHL                    [slotAfterShl]
PUSH1 0x9              [0x9 slotAfterShl]
MSTORE                 []              ==> memory(0x9: slotAfterShl(deployedCode2ndPart))
PUSH1 0x10             [0x10]
PUSH1 0x39             [0x39 0x10]
PUSH1 0xa              [0xa 0x39 0x10]
CODECOPY               []              ==> memory(0xa~0x38: 0x39~0x64(deployedCode3rdPart))
PUSH1 0x1a             [0x1a]
PUSH0                  [00 0x1a]
RETURN

# proxy contract (deployedcode)
CALLDATASIZE        [calldatasize]
PUSH0               [00 calldatasize]
PUSH0               [00 00 calldatasize]
CALLDATACOPY        []     ==> memory(00~(calldatasize-1) => codedata)
PUSH0               [00]
PUSH0               [00 00]
CALLDATASIZE        [calldatasize 00 00]
PUSH0               [00 calldatasize 00 00]
PUSH1               [slot 00 calldatasize 00 00]
SLOAD               [logicAddress 00 calldatasize 00 00]
GAS                 [gas logicAddress 00 calldatasize 00 00]
DELEGATECALL        [result]
RETURNDATASIZE      [returnDataSize result]
PUSH0               [00 returnDataSize result]
PUSH0               [00 00 returnDataSize result]
RETURNDATACOPY      [result] => memory(00~(RETURNDATASIZE - 1) => RETURNDATA)
RETURNDATASIZE      [returnDataSize result]
PUSH0               [00 returnDataSize result]
DUP3                [result 00 returnDataSize result]
PUSH1 0x18          [0x18 result 00 returnDataSize result]
JUMPI				[00 returnDataSize result]
REVERT              [result]
JUMPDEST            [00 returnDataSize result]
RETURN              [result]
```

### 2.2 evm opcode to code

- bytecode
replace xx to a slot of 1byte and replace yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy to a address of 20bytes before deploying contract

```auto
60xx73yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy8155600960305f3960f81b60095260106039600a39601a5ff3365f5f375f5f365f60545af43d5f5f3e3d5f82601857fd5bf3
```

- deployedcode
wherein the bytes at indices 9 are replaced with the 1 byte slot of the master after created

```auto
365f5f375f5f365f60xx545af43d5f5f3e3d5f82601857fd5bf3
```

I am eager to hear feedback and suggestions from the Ethereum community regarding this proposal. I am also open to discussing any potential limitations or risks related to its design. Thank you for your time and consideration.

## Replies

**xinbenlv** (2023-06-20):

This is extremely interesting. Whether this is considered “Minimum” and worthy of standardization would be up for peer review, but I really like the idea that you are sharing this upgradable proxy with everyone.

---

**xiaobaiskill** (2023-06-21):

After I removed some zero bytes, it became smaller and now it looks more streamlined

---

**xinbenlv** (2023-06-21):

Is it transparent pattern or UUPS pattern?

---

**xiaobaiskill** (2023-06-21):

UUPS, It requires placing the logic for contract upgrades in the logic contract.

---

**xiaobaiskill** (2023-06-21):

Here, I have provided a simple example.

- example.sol
- test example.sol

You can take a look and hope to receive your feedback.

Thank you

---

**joeblogg801** (2023-06-22):

Great job on your code! I noticed that you’re using the `returndatasize` opcode to push a zero value onto the stack. While this workaround achieves the desired result, I’d like to suggest a different approach.

Instead of abusing the `returndatasize` opcode, you can leverage the `push0` opcode, which is specifically designed for pushing a zero value onto the stack.

`push0` was implemented in EIP-3855 and should be available now.

---

**xiaobaiskill** (2023-06-22):

Cool, thank you for the reminder. It’s a great suggestion. I will optimize it based on your advice. Additionally, I noticed that other chains don’t seem to have started supporting EIP-3855 yet, and the Foundry tool is also not supported.

---

**xiaobaiskill** (2023-06-23):

Thank you for your suggestion. I have made the modification to replace `RETURNDATASIZE` with `PUSH0` , and during the process, further optimization of the EVM code was performed

---

**joohhnnn** (2023-06-23):

May I ask that if the minimal upgradable proxy is used for gas saving? if so this proposal may help. [EIP-XX: add gasRefund for CREATE/CREATE2 if the codeHash already exist](https://ethereum-magicians.org/t/eip-xx-add-gasrefund-for-create-create2-if-the-codehash-already-exist/14813)

---

**xiaobaiskill** (2023-06-24):

Indeed, the minimal upgradable proxy is designed with the intention of saving gas, and it does not conflict with your proposal. The minimal upgradable proxy also incurs minimal gas consumption during contract invocation.

---

**Bschuster3434** (2023-07-01):

Can you describe some use case in which this pattern would not be something to consider? And I mean more than just the instance where gas optimization would not be a concern.

---

**xiaobaiskill** (2023-07-02):

The two most important features of the minimal upgradeable contract are:

1. Minimum gas consumption during the execution of interactions in the proxy contract.
2. Retention of upgradability capability.

When we use OpenZeppelin’s ERC1967 or UUPS contracts, we can consider using the minimal upgradeable contract to save gas consumption.

However, it’s worth noting that the majority of ERC20 and ERC721 standard contracts in the market do not utilize proxy patterns.

---

**frangio** (2023-07-24):

The main thing that I see missing from this proxy contract is the ability to initialize the contract atomically with deployment, without the use of the factory. Is this something you’ve considered?

---

**xiaobaiskill** (2023-07-25):

Regarding the initialization of the contract, I don’t want you to include it in the bytecode of the proxy contract as it would complicate the bytecode of the minimal upgradeable contract. If you insist on doing so, I suggest using a factory contract or sending a transaction to execute the initialization.

Additionally, here is an interesting way to use the minimal upgradeable proxy contract.

[depoy minimal upgradeable proxy by Create the logical contract](https://github.com/xiaobaiskill/minimal-upgradable-proxy/blob/main/contracts/utils/Proxy0.sol)

---

**conner** (2023-08-01):

Really interesting optimization! I was perusing your example implementations as was wondering if you could make one with the `implementationSlot = bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1)`? If a goal is to help people use this instead of something like OpenZeppelin’s standard EIP1967 proxy, I think aligning the slots is important for easy adoption and interoperability

---

**xiaobaiskill** (2023-08-08):

I think you may achieve a similar effect by using the following Solidity file. You can replace the `implementationSlot = bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1)` in `proxy32.sol`

[proxy32.sol](https://github.com/xiaobaiskill/minimal-upgradable-proxy/blob/main/contracts/utils/Proxy32.sol)

Here is a usage scenario:

[example used proxy32.sol](https://github.com/xiaobaiskill/minimal-upgradable-proxy/blob/main/contracts/mock/mock32/Example.sol)

