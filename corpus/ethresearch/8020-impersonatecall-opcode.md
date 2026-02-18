---
source: ethresearch
topic_id: 8020
title: IMPERSONATECALL Opcode
author: SergioDemianLerner
date: "2020-09-24"
category: EVM
tags: []
url: https://ethresear.ch/t/impersonatecall-opcode/8020
views: 2309
likes: 7
posts_count: 5
---

# IMPERSONATECALL Opcode

I would like to open the discussion about a proposal for a new opcode named IMPERSONATECALL that calls other contracts and replaces the msg.sender at the same time. It saves gas and simplifies several use cases regarding meta-transactions and sponsored wallets.

You can read the proposal here:


      [github.com](https://github.com/ethereum/EIPs/blob/716fadffb103dd9e491d7ca6cb98b3f98036ea71/EIPS/eip-IMPERSONATECALL.md)




####

```md
---
eip:
title: IMPERSONATECALL Opcode
author: Sergio Demian Lerner (sergio.d.lerner@gmail.com)
category: Core
type: Standards Track
status: Draft
created: 2020-09-24
---

### Overview

Add a new opcode, `IMPERSONATECALL` at `0xf6`, which is similar in idea to `CALL`, except that it impersonates a sender, i.e. the callee sees a sender different from the real caller. To prevent collisions with other deployed contract or externally owned accounts, the impersonated sender address is derived from the real caller address and a salt.

### Specification

`IMPERSONATECALL`: `0xf6`, takes 7 operands:

- `gas`: the amount of gas the code may use in order to execute;
- `to`: the destination address whose code is to be executed;
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/716fadffb103dd9e491d7ca6cb98b3f98036ea71/EIPS/eip-IMPERSONATECALL.md)








The idea is that a contract can impersonate child contracts (created with a derivation similar, but not equal, to CREATE2). Therefore there is no practical risk that the caller impersonates a third party contract.

This opcode enables the creation of multi-user wallets, where each user is given a separate non-custodial smart-wallet having its own address for storing ethers and tokens, yet no contract code is deployed, and a main-wallet contract retains the common functionality (i.e. social private key recovery).  Wallets are accessed by a meta-transaction system (i.e using EIP-712) embedded in the multi-user wallet contract.

Even if the same functionality can be achieved by using counterfactual contract creation, this solution is attractive because:

- It’s much simpler to design and less error prone.
- It provides the sponsor huge gas savings, removing the need for the deployment of thousands of wallets.

I’m sure there are plenty more use cases that can benefit from this opcode.

## Replies

**SergioDemianLerner** (2020-09-24):

As IMPERSONATECALL sounds like a risky thing (it’s not), somebody suggested I rename it CALLFROM.

---

**SergioDemianLerner** (2020-10-09):

The EIP has been assigned a final number and, after reviews, it was accepted to the EIP repository. You can read the latest version here:


      [github.com](https://github.com/ethereum/EIPs/blob/930e456484589a403cee7bbb94539a096182ed6e/EIPS/eip-2997.md)




####

```md
---
eip: 2997
title: IMPERSONATECALL Opcode
author: Sergio Demian Lerner (@SergioDemianLerner)
discussions-to: https://ethresear.ch/t/impersonatecall-opcode/8020
category: Core
type: Standards Track
status: Draft
created: 2020-09-24
---

## Abstract

Add a new opcode, `IMPERSONATECALL` at `0xf6`, which is similar in idea to `CALL (0xF1)`, except that it impersonates a sender, i.e. the callee sees a sender different from the real caller. The impersonated sender address is derived from the real caller address and a salt.

## Motivation

This proposal enables native multi-user wallets (wallets that serve multiple users) that can be commanded by EIP-712 based messages and therefore enable meta-transactions. Multi-user wallets also enable the aggregation of transfer operations in batches similar to rollups, but maintaining the same address space as normal onchain transactions, so the sender's wallet does not need to be upgraded to support sinding ether or tokens to a user of a multi-user wallet.
Additionally, many times a sponsor company wants to deploy non-custodial smart wallets for all its users. The sponsor does not want to pay the deployment cost of each user contract in advance. Counterfactual contract creation enables this, yet it forces the sponsor to create the smart wallet (or a proxy contract to it) when the user wants to transfer ether or tokens out of his/her account for the first time. This proposal avoids this extra cost, which is at least 42000 gas per user.

```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/930e456484589a403cee7bbb94539a096182ed6e/EIPS/eip-2997.md)

---

**matt** (2020-10-10):

https://ethereum-magicians.org is usually the preferred place for EIP discussions ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**SergioDemianLerner** (2020-10-10):

thanks for the tip!

The discussion has been moved to :

https://ethereum-magicians.org/t/eip-2997-impersonatecall-opcode/4816

Please follow that link while I correct the EIP link.

