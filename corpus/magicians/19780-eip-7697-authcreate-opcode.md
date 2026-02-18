---
source: magicians
topic_id: 19780
title: EIP-7697：AUTHCREATE opcode
author: txgyy
date: "2024-04-24"
category: EIPs > EIPs core
tags: [evm, opcodes, account-abstraction]
url: https://ethereum-magicians.org/t/eip-7697-authcreate-opcode/19780
views: 1185
likes: 6
posts_count: 9
---

# EIP-7697：AUTHCREATE opcode

**EIP**: [Add EIP: AUTHCREATE opcode by txgyy · Pull Request #8493 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8493/files)

**Go-Ethereum**: [Comparing ethereum:master...txgyy:EIP-7697 · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/compare/master...txgyy:go-ethereum:EIP-7697)

**AA Factory**: [Comparing eth-infinitism:develop...txgyy:AA-EIP-7697 · eth-infinitism/account-abstraction · GitHub](https://github.com/eth-infinitism/account-abstraction/compare/develop...txgyy:account-abstraction:AA-EIP-7697)

## Abstract

The EIP introduces an EVM instruction `AUTHCREATE`. It allows a deterministic addresses to migrate to a smart contract.

Inspiration comes from [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074) and [EIP-5003](https://eips.ethereum.org/EIPS/eip-5003):

- (EIP-3074) + EIP-5003 = (AUTH + AUTHCALL) + AUTHUSURP
- EIP-7697 = AUTHCREATE = AUTH + AUTHUSURP

## Motivation

For a long time, the EVM ecosystem has been plagued by two issues:

1. Difficulty ensuring consistency across addresses on multiple chains, even when using the same bytecode.
2. EOAs lack contract capabilities, preventing the realization of account abstraction.

Authentication - any form of proving one’s identity.
3. Authorization - any access policy.
4. Replay protection - transaction ordering decoupled from replay protection.
5. Gas payment - gas payment decoupled from the account itself.
6. Execution - any execution logic.

| Feature | EIP-7697 | EIP-3074 | EIP-5003 | EIP-7377 |
| --- | --- | --- | --- | --- |
| Deploy the same address ERC-2470 |  |  | need 3 opcodes | only EOA |
| Help EOA to upgrade to CA |  |  | need 3 opcodes |  |
| Support secp256r1 or more |  |  |  |  |
| Reuse existing wallet infrastructure | adapt the contract |  | adapt the contract | adapt the node rpc |
| Integrate easily with ERC-4337 and RIP-7560 | support factory contract |  |  |  |
| Grant temporary CA capabilities to EOA |  |  |  |  |

## Replies

**matt** (2024-04-24):

This seems nearly identical to EIP-5003 AUTHUSURP. Can you please define the difference of your proposal?

---

**txgyy** (2024-04-24):

Yes, AUTH_CREATE = AUTH + AUTHUSURP. If Ethereum’s goal is “Full AA,” it should not introduce new OpCodes that merely enhance EOAs.

---

**txgyy** (2024-04-24):

Moreover, AUTH_CREATE integrates very easily with ERC-4337 and RIP-7560.

---

**txgyy** (2024-04-24):

Yes, AUTH_CREATE = AUTH + AUTHUSURP. If Ethereum’s goal is “Full AA,” it should not introduce new OpCodes that merely enhance EOAs.

---

**yaonam** (2024-04-25):

Building on a bit of what [@txgyy](/u/txgyy) was saying…

(3074) + 5003 == (AUTH + AUTHCALL) + AUTHUSURP

AUTHCREATE == AUTH + AUTHUSURP

AUTHCALL is undesirable for AA endgame as it is only used for fully featured invokers where the account remains an EOA. These invokers will not be reused when the eoa migrates via 5003/AUTHUSURP, leading to wasted effort and distraction. I think this is the strongest reasoning for combining 3074/5003 into something like AUTHCREATE.

---

**wjmelements** (2024-04-29):

Based on the name I was expecting AUTHCREATE to be like AUTHCALL but performing sudo `CREATE` instead of sudo `CALL`.

---

**txgyy** (2024-04-30):

Yes, AUTHCREATE is ‘auth + create’. But after you CREATE, it becomes like a contract.

---

**wjmelements** (2024-04-30):

It seems to differ from create in an important way, by usurping.

