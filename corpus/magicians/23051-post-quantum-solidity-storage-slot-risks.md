---
source: magicians
topic_id: 23051
title: Post-Quantum Solidity Storage Slot Risks
author: ryley-o
date: "2025-03-03"
category: Magicians > Primordial Soup
tags: [security, postquantum]
url: https://ethereum-magicians.org/t/post-quantum-solidity-storage-slot-risks/23051
views: 79
likes: 1
posts_count: 1
---

# Post-Quantum Solidity Storage Slot Risks

Consider the following:

- existing immutable smart contract (e.g. erc-20) has mapping(address account => mapping(address spender => uint256)) private _allowances;

In a post-quantum world, Grover’s algorithm weakens preimage resistance, reducing the difficulty of someone being able to brute-force overwrite a specific approval storage slot from 2^256 to 2^128. While still decent, this may be breakable in 20-30+ years.

This problem is generalizable to many, many situations in solidity, because fundamentally, solidity maps all contract storage to deterministic slots based on keccak256 hash of something controlled by often untrusted third parties.

If I’m designing a smart contract that I want to remain secure in a post-quantum world, but I don’t want to make it upgradeable (which has its own uncertainties and issues), what tools are we providing developers to get ahead of this problem? Are there discussions of alternate hashing function precompiles to make available to developers in the near term, without them paying significant gas penalties? It seems that we should be incentivizing post-quantum smart contracts for our protocol’s long-term outlook.

An entirely separate concern of mine is how legacy, non-upgradeable smart contracts will remain secure in a post-quantum world, so any discussion in that area would also be great in this thread!
