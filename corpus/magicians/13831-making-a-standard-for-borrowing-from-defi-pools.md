---
source: magicians
topic_id: 13831
title: Making a standard for borrowing from DeFi pools
author: briankostar
date: "2023-04-15"
category: EIPs
tags: [defi]
url: https://ethereum-magicians.org/t/making-a-standard-for-borrowing-from-defi-pools/13831
views: 421
likes: 0
posts_count: 1
---

# Making a standard for borrowing from DeFi pools

This is a proposal to address the fragmented lending/borrowing pools that makes up a large chunk of the DeFi ecosystem on ethereum.

Draft: [Add EIP: Sharable interface for Borrowing by briankostar · Pull Request #6882 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6882)

The main motivation for this is that, to borrow from a defi pool, users often have to search through dozens of protocols to find the best rate among other conditions.

To improve this experience for borrowers, we are suggesting an interface that lending/borrowing pools can adapt to allow for easy query of the interest rates and other methods.

This will allow for development of dapp similar to 1inch where a user can connect, and borrow from various pools at once.

This is inspired by [EIP 4626](https://eips.ethereum.org/EIPS/eip-4626) which offered standard for tokenized defi vaults that many defi protocols followed afterwards. (4626 alliance)
