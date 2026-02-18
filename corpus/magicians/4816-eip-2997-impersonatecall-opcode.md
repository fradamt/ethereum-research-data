---
source: magicians
topic_id: 4816
title: "EIP-2997: IMPERSONATECALL Opcode"
author: sergio_lerner
date: "2020-10-10"
category: EIPs
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/eip-2997-impersonatecall-opcode/4816
views: 1738
likes: 5
posts_count: 12
---

# EIP-2997: IMPERSONATECALL Opcode

I would like to open the discussion about a proposal for a new opcode named IMPERSONATECALL that calls other contracts and replaces the msg.sender at the same time. It saves gas and simplifies several use cases regarding muti-user wallets, sponsored wallets, meta-transactions, cheap batch operations (similar to rollups), and more.

The idea is that a contract can impersonate child contracts (created with a derivation similar, but not equal, to CREATE2). Therefore there is no practical risk that the caller impersonates a third party contract.

This opcode enables the creation of multi-user wallets, where each user is given a separate non-custodial smart-wallet having its own address for storing ethers and tokens, yet no contract code is deployed, and a main-wallet contract retains the common functionality (i.e. social private key recovery). Wallets are accessed by a meta-transaction system (i.e using EIP-712) embedded in the multi-user wallet contract.

Even if the same functionality can be achieved by using counterfactual contract creation, this solution is attractive because:

- It’s much simpler to design and less error prone.
- It provides the sponsor huge gas savings, removing the need for the deployment of thousands of wallets.

I’m sure there are plenty more use cases that can benefit from this opcode.

You can read the proposal here:


      [github.com](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2997.md)




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

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2997.md)

## Replies

**sergio_lerner** (2021-02-15):

Does anyone have any opinion on this super useful feature?

---

**bradleat** (2021-02-16):

What is the definition of a child contract for the purposed of your EIP?

---

**sergio_lerner** (2021-02-17):

A contract whose address is derived from the parent’s contract address only for the purpose of IMPERSONATECALL.

In other words, the child contract address cannot be derived by CREATE2/CREATE from that parent’s contract, or from any other account without breaking the keccak hash function.

---

**matt** (2021-02-24):

I think omitting the word of zeros in the address pre-image is best, since it can’t collide with CREATE or CREATE2.

Otherwise, I like this EIP.

---

**bradleat** (2021-03-01):

I think there are many situations in which a child contract should not be able to be impersonated by a parent contract. Does this EIP propose a CREATE_IMPRESSIONABLE_CHILD opcode or another mechanism of marking a child contract as able to be impersonated. In a similar vein, should there be a method for removing this ability?

---

**matt** (2021-03-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bradleat/48/216_2.png) bradleat:

> I think there are many situations in which a child contract should not be able to be impersonated by a parent contract.

Can you elaborate? I believe these sort of things should be handled by the contract itself, for example, the `IMPERSONATECALL` could be protected by a ECDSA recovery + nonce check. Therefore the owner of the corresponding private key is the only one with access to the address.

---

**sergio_lerner** (2021-03-01):

Not all child contracts can be impersonated. Only the ones that `IMPERSONATECALL` can access by address derivation. The set of derived addresses from `IMPERSONATECALL`  does not overlap with the set of addresses derived by CREATE2 or by CREATE (unless the keccak hash function is broken).

---

**sergio_lerner** (2021-03-01):

In other words, child contracts used by `IMPERSONATECALL` **cannot** be deployed, ever. They are will always be “virtual” contracts.

---

**sergio_lerner** (2021-03-01):

If in the future someone finds a use case for instantiating an impersonated contract, then a new opcode CREATE3 would need to be created. Note that a CREATE3 opcode won’t be able to link the address of the created contract with a specific initialization code, as CREATE2 does.

However, counterfactual contracts could be created anyway with CREATE3 because the nonce is user-selectable.

---

**bradleat** (2021-03-02):

Ah okay. I see what’s going on here. I think it’s good idea.

Have you thought about the implications of the possible collisions with an existing deployed contract or with other contracts that interact with the counterfactual child contract?

In the rare possibility of a collision, we might have a situation in which funds are transferred to/from an account that already exists. Moreover, by adjusting the salt an attacker might be able to find/mine a collision on purpose by abusing the SALT.

The other concern I would have is that contracts that interact with the counterfactual child contract. There are many contracts which check to see if a contract or account exists at an address before interacting with it further. Do you have any thoughts about this or other potential issues?

This “This EIP makes address collisions possible, yet practically impossible” is concerning to me. Could you expound on this point?

---

**sergio_lerner** (2021-03-08):

Regarding collisions: Ethereum already is affected by potential address collisions by the CREATE2 opcode. It affects EOAs, and counterfactually deployed contracts (before deployment). The IMPERSONATECALL opcode only makes collisions slightly worse, because they could also affect deployed contracts.

But believe me that stealing from EOAs with an address collision is so bad already that I wouldn’t worry about the slight increase in attack surface.

You can read Vitalik’s proposal on increasing the address space [here](https://ethereum-magicians.org/t/increasing-address-size-from-20-to-32-bytes/5485/30).

Regarding the contracts checking other contracts existence: I’m not aware that contracts check non-zero balance existence using the BALANCE opcode. Some contracts check if an address is a contract using EXTCODESIZE. If we don’t change anything in the EIP, those contracts will not detect correctly impersonated contracts.

We could change the EIP in several ways to solve this minor issue:

1. the first time the parent contract impersonates a child contract and the child contract is calling another contract then we actually create the child contract with 1 byte of code (zero). I don’t like this because it would make IMPERSONATECALL more expensive in two ways. First the actual I/O of creating the contract and second the need to check if the code already exists on every IMPERSONATECALL.
2. We can add an in-memory map address->callDepth, where callDepth is an integer that counts the number of recursive IMPERSONATECALLs performed for that address. When IMPERSONATECALL is called for a child contract X then the depth of X is incremented in the map. Whenever a contract executes EXTCODESIZE, the address is looked up in the map, and if the depth counter is greater than zero then the value 1 is returned as code size, simulating a 1-byte code. A similar emulation is performed for EXTCODECOPY. When IMPERSONATECALL returns, the counter is decremented and the item is removed if counter reaches zero. While this solves the problem, I don’t like it either, because adding more state to VM execution complicates fraud proofs for L2 EVM rollups that attempt to emulate the EVM.
3. Still another possibility is to let IMPERSONATECALL dynamically apply codes to addresses on-the-fly on each call. A similar map like in (2) would be used, but containing the counter plus the code itself (for simplicity, no nested code changes would be allowed within a single transaction).
4. Another possibility is to allow a single IMPERSONATECALL per contract per transaction. This limitation would make calls from impersonated addresses limited very much like EOAs (the main difference would be that EOA have ORIGIN == SENDER while calls from impersonated addresses won’t).

To summarize, I think the best is to do nothing. I don’t like options (1) to (3) because of the added complexity. Option (4) is ok.

In the future, if a larger address space is implemented in Ethereum, then we can use an address space ID to identify impersonated addresses, so contracts can treat them as contracts if desired.

