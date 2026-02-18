---
source: ethresearch
topic_id: 23545
title: How CREATE2 Prevents Initial Deposit Leakage in Privacy Systems
author: pememoni
date: "2025-11-26"
category: Privacy
tags: []
url: https://ethresear.ch/t/how-create2-prevents-initial-deposit-leakage-in-privacy-systems/23545
views: 170
likes: 5
posts_count: 5
---

# How CREATE2 Prevents Initial Deposit Leakage in Privacy Systems

### How CREATE2 Prevents Initial Deposit Leakage in Privacy Systems

*by Peyman Momeni, Fairblock*

No One Needs to See You Buy Chips Before You Hit the Poker Table. Confidential transfers, encrypted balances, and private payment rails often focus on hiding amounts and identities with cryptography. Yet one of the biggest privacy leaks happens before any encryption or zero-knowledge proof even begins. The leak happens at the moment a new onchain wallet or vault is created.

If a system deploys a new contract for every user, every merchant, or every private vault, observers can track the exact time of creation and the first deposit that enters the contract. This is enough to undermine privacy for many use cases. A merchant’s payment volume, a user’s starting balance, or the very fact that someone is using a private system can be deduced by watching contract deployments and the following deposits.

CREATE2 provides a powerful way to close this metadata leak.

### The Privacy Problem With Normal Deployments

[![Screenshot 2025-11-26 at 2.03.36 PM](https://ethresear.ch/uploads/default/optimized/3X/f/7/f7575182b88260d36271acfde4635d83a2c7fa3c_2_503x499.jpeg)Screenshot 2025-11-26 at 2.03.36 PM980×974 87 KB](https://ethresear.ch/uploads/default/f7575182b88260d36271acfde4635d83a2c7fa3c)

Under standard contract deployment, the blockchain reveals:

- who deployed the contract
- when the contract was deployed
- what the first deposit was
- who funded the initial balance

Even if amounts are encrypted once inside the system, the first deposit is visible because it must be sent after the contract exists. This is unavoidable under CREATE because the address does not exist until the deployment transaction is executed.

For any confidential stablecoin system, private merchant settlement layer, or shielded user vault, this creates an immediate privacy problem. The moment you deploy a wallet, the world sees the wallet’s birth and its initial balance.

### What CREATE2 Changes

CREATE2 lets developers compute the final address of a contract long before it is deployed. The address is derived from four inputs: the deployer address, a salt, a constant prefix, and the contract’s init code. This address can be calculated offchain and shared privately.

This feature has a major privacy benefit: assets can be sent to the future address before the contract exists.

In other words, you can deposit funds into a contract that has not yet been deployed.

### Why This Hides Initial Deposits

Depositing into an address that does not yet contain a contract looks no different from sending tokens to a random unused address. There is no visible signal that this address will later become a vault, a merchant settlement contract, or a private stablecoin container.

This breaks the link between:

- the time of deposit
- the time of wallet creation
- the identity of the deployer

When the contract is eventually deployed, it already contains a balance. No observer can tell when the deposit happened or what the initial amount was.

This solves one of the biggest practical privacy leaks in confidential payment systems.

### Removing Linkability Between User and Vault

With CREATE2, the contract can be deployed by a neutral relayer. The user does not need to touch the blockchain with their wallet at all. The address is known privately, funds are deposited privately, and deployment happens through an anonymous executor.

This removes the trace that normally links a user’s EOA to the private vault they intend to use.

For merchant privacy, this prevents competitors or analytics firms from guessing revenue by watching contract births and matching them with early deposits.

For user privacy, this prevents the chain from revealing that a person has started using a private wallet.

### Integrating CREATE2 With Confidential Stablecoins

In systems that use homomorphic encryption or ZK proofs, exposure of the first deposit can still reveal sensitive metadata. CREATE2 fills the last gap by hiding wallet creation.

A typical flow looks like this:

1. The private vault address is computed offchain with CREATE2.
2. The user or merchant receives the future address privately.
3. The user deposits confidential stablecoins or encrypted amounts into the address.
4. A relayer deploys the vault contract when needed.
5. The vault is born with funds inside and no visible creation signal.

Every step remains unlinkable from the outside.

This aligns with the idea of dynamic confidentiality. Cryptography hides amounts and identities. CREATE2 hides the very moment that the private environment is created.

### Ideal for Encrypted Payment Infrastructure

Confidential stablecoins and merchant payment systems often need to operate in a way that does not reveal:

- who receives how much
- when they receive it
- how often they receive payments
- how large a merchant’s daily volume is

CREATE2 allows the vault or settlement contract to exist privately even before deployment. Combined with encrypted transfers, this prevents the largest metadata leak in the system.

The result is a more complete form of financial privacy that covers both cryptographic confidentiality and operational privacy.

## Replies

**MicahZoltu** (2025-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/pememoni/48/9476_2.png) pememoni:

> When the contract is eventually deployed, it already contains a balance. No observer can tell when the deposit happened or what the initial amount was.

I don’t believe this is true, at least as you have described it here.  When the contract is deployed you can look at chain history and see who deposited into that address, how much they deposited, and who paid the fee to deploy the contract.

---

**Judaixxspexy** (2025-11-27):

Mind checking the typical flow points which was stated in the content

---

**pememoni** (2025-11-27):

it’s combined with other private/confidential transfers

---

**MicahZoltu** (2025-11-27):

Then it is unclear what value CREATE2 adds.  Once the contract is deployed, you are in the same place as you would have been using otherwise the same techniques but CREATEd contracts.

