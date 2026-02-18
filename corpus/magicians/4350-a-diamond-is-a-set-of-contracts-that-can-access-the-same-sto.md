---
source: magicians
topic_id: 4350
title: A diamond is a set of contracts that can access the same storage variables and share the same Ethereum address
author: mudgen
date: "2020-06-09"
category: Magicians > Primordial Soup
tags: [smart-contracts, proxy-contract, upgradeable-contract]
url: https://ethereum-magicians.org/t/a-diamond-is-a-set-of-contracts-that-can-access-the-same-storage-variables-and-share-the-same-ethereum-address/4350
views: 842
likes: 0
posts_count: 3
---

# A diamond is a set of contracts that can access the same storage variables and share the same Ethereum address

> Why use a diamond on Ethereum? Multiple small contracts calling each other increases complexity. A diamond handling its storage and functionality is simpler.

> It provides a cohesive way to organize and structure complex contract interaction.
>
>
> By cohesive I mean that code that is associated with each other should be easy to use together. At the same time the Diamond Standard provides a degree of modularity. It provides this balance that is very useful.

> The Diamond Standard also solves a huge technical problem which is the 24KB maximum contract size limit. This limit becomes a problem when you need contract code to access the same storage variables but can’t anymore because the contract size has gotten too big. The Diamond Standard enables multiple contracts to access the same storage variables in the same/similar way one large contract could.

> A contract architecture that makes upgradeable contracts flexible, unlimited in size, and transparent.

Diamond Standard: [EIP-2535: Diamonds · Issue #2535 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/2535)

The Diamond Standard is hot on Reddit right now: https://www.reddit.com/r/ethereum/comments/gze6k3/a_diamond_is_a_set_of_contracts_that_can_access/

Looking for someone to champion the Diamond Standard for OpenZeppelin: [Looking for Someone to Champion the Diamond Standard for OpenZeppelin - General - OpenZeppelin Forum](https://forum.openzeppelin.com/t/looking-for-someone-to-champion-the-diamond-standard-for-openzeppelin/3058)

## Replies

**Amxx** (2020-06-11):

shameless self promotion:

If you are looking for an implementation, maybe consider [my implementation of ERC1538](https://github.com/iExecBlockchainComputing/iexec-solidity/tree/master/contracts/ERC1538) (which is covered by [this audit report](https://github.com/iExecBlockchainComputing/PoCo/blob/v5/audit/v5/iexec-poco-audit-2020-03.pdf))

---

**mudgen** (2020-06-11):

[@Amxx](/u/amxx) Your implementation is welcome.  Glad to see it.

