---
source: magicians
topic_id: 21145
title: "ERC-7772: Partial Gas Sponsorship Interface"
author: lucaslim
date: "2024-09-20"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7772-partial-gas-sponsorship-interface/21145
views: 132
likes: 5
posts_count: 3
---

# ERC-7772: Partial Gas Sponsorship Interface

Discussion topic for EIP-7772 https://github.com/ethereum/ERCs/pull/649

This proposal defines the necessary interface that decentralized applications (dApps) must implement to sponsor a portion of the required gas for user operations utilizing a Paymaster that supports this standard. The proposal also provides a suggested code implementation that Paymasters can include in their current implementation to support dApp sponsorship. Partial sponsorship between more than one dApps may also be achieved through this proposal.

## Replies

**VGabriel45** (2024-09-30):

This could indeed open up exciting possibilities for tokenomics, such as offering gas discounts based on token holdings or other criteria.

Given that this ERC works alongside ERC-4337, how does the gas efficiency of transactions using this partial sponsorship method compare to standard ERC-4337 implementations? Are there any estimates on the potential gas savings for users or additional costs for dApps when implementing this sponsorship model?

---

**dror** (2024-10-01):

Commented on the ERC.

The problems I see is that there is full trust between the paymaster and those sponsors: that is, a sponsor is tied to a specific paymaster, and the paymaster must have a “whitelist” of audited sponsors, otherwise, each of them is vulnerable to attacks - either denial of service attacks or actual funds steal.

In general, a paymaster must be very careful on external code it executes. The validation rules (ERC-7562) are there to prevent an attack by paymaster on the system (on bundlers). By calling external contracts, the paymaster exposes itself to other contracts that might breach those rules - and thus get the paymaster itself blamed for the failures.

