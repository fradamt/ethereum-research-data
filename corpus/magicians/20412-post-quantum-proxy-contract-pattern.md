---
source: magicians
topic_id: 20412
title: Post-Quantum Proxy Contract Pattern
author: srarcharles
date: "2024-06-29"
category: Magicians > Primordial Soup
tags: [erc, proxy-contract, postquantum]
url: https://ethereum-magicians.org/t/post-quantum-proxy-contract-pattern/20412
views: 485
likes: 0
posts_count: 1
---

# Post-Quantum Proxy Contract Pattern

I want you all to check out my idea.

New “Proxy Pattern Smart Contract with Quantum-Resistance Ability”

I’m concerning about quantum-computer’s attacks on Proxy contract. It may become single point of failure(SPOF) for many smart contract(DApps like LIDO, DEFIs, etc…) because malicious quantum attacker can upgrade proxy’s embedded address to any address they want without users knowing it have happened.

- About commonly used “Proxy Pattern”
https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies

But, I find out new smart contract to protect it to be attacked when secret keys of smart contract owner of proxy contract is stollen.

[![ProxyWallet-eng](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7ad2f3bd746cd2391e8c7c498769cd0b2f7a3496_2_536x499.jpeg)ProxyWallet-eng2071×1930 275 KB](https://ethereum-magicians.org/uploads/default/7ad2f3bd746cd2391e8c7c498769cd0b2f7a3496)

Above is new scheme of smart contract with ability to prevent the attack to Proxy contract.

Main Point is…

- Proxy contract’s implementation addresses can only be upgraded through the authentication by post-quantum signature scheme(like Lamport Signature).

So, malicious attacker can not upgrade Proxy contracts’ implementation addresses with Alice(Owner)'s secret key.

I also have written minimum implementation with tests of this idea although authentication part is not implemented(because any Post-quantum signature scheme can be embedded there like [Pauli Group’s Lamport Signature Authentication](https://github.com/Pauli-Group/walletV2/blob/0eeb317870e543eb8b6fbb1af9a7268f9ac5a66c/contracts/AccountAbstraction/Lamport/VerifyLamport.sol#L4-L26))

- This repository includes minimum implementation of quantum-resistant proxy contract. (I called it ProxyWallet)



      [github.com/starcharles/quantum-resistant-proxy-contract](https://github.com/starcharles/quantum-resistant-proxy-contract/blob/main/test/ProxyWallet.spec.ts)





####

  [main](https://github.com/starcharles/quantum-resistant-proxy-contract/blob/main/test/ProxyWallet.spec.ts)



```ts
import {
  time,
  loadFixture,
} from "@nomicfoundation/hardhat-toolbox-viem/network-helpers";
import { expect } from "chai";
import hre from "hardhat";
import "@nomicfoundation/hardhat-ethers";
import {
  getAddress,
  keccak256,
  Abi,
  parseGwei,
  getContract,
  TransactionExecutionError,
} from "viem";
import { AbiCoder } from "ethers";

describe("ProxyWallet contract", function () {
  async function deployFixture() {
    const [owner, addr1, addr2] = await hre.viem.getWalletClients();
```

  This file has been truncated. [show original](https://github.com/starcharles/quantum-resistant-proxy-contract/blob/main/test/ProxyWallet.spec.ts)










This includes

- Contract code to realize my concept.
- Tests to confirm desirable behavior of the contract.

Please feel free to give me any comments and further implovement idea.

And If this idea make sense or valuable for Ethereum Community, I want to propose this as new ERC.

Thanks for reading.

Naoto Sato (Blocq, Inc)
