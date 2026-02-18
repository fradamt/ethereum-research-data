---
source: magicians
topic_id: 4038
title: Diamond Standard for Upgradeable Contracts
author: mudgen
date: "2020-02-25"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/diamond-standard-for-upgradeable-contracts/4038
views: 1761
likes: 6
posts_count: 5
---

# Diamond Standard for Upgradeable Contracts

**Simple Summary**

A contract architecture that makes upgradeable contracts flexible, unlimited in size, and transparent.

New terminology from the diamond industry.

Improved design over [ERC1538](https://eips.ethereum.org/EIPS/eip-1538) using ABIEncoderV2 and function selectors.

**Abstract**

A diamond is a contract that implements this standard.

A diamond provides the following:

1. A way to add, replace and remove multiple functions atomically (in the same transaction).
2. An event that shows what functions are added, replaced, removed and one or messages describing changes.
3. A way to look at a diamond to show its functions.
4. Solves the 24KB maximum contract size limitation. Diamonds can be any size.
5. Enables zero, partial or full contract immutablity as desired, and when desired.
6. Designed for tooling and user-interface software.

A diamond is a proxy contract that supports using multiple logic/delegate contracts at the same time. In this standard the term for logic/delegate contract is facet. A diamond can have many facets. Which facet is used depends on which function is called. Each facet supplies one or more functions.

This standard supersedes [ERC1538: Transparent Contract Standard](https://eips.ethereum.org/EIPS/eip-1538).

See the full standard here: https://github.com/ethereum/EIPs/issues/2535

## Replies

**Amxx** (2020-02-26):

I was just about to write an article about our use of ERC1538 … and send our ERC1538 powered contracts for audit.

I guess I’ll have to reconsider ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9)

More seriously. Your proposed implementation is lacking ways to delegate the `receive` and the `fallback` functions. I think this is an essential feature to have! But has they don’t have dedicated function selector, you need to be a bit creative. See [my ERC1538 implementation](https://github.com/iExecBlockchainComputing/iexec-solidity/tree/master/contracts/ERC1538).

To me it feals like a nice sugar coating on top of ERC1538, with a wording that makes it more easily understandable. But in term of functionnality, I don’t really see what is the added benefit.

---

**mudgen** (2020-02-26):

[@Amxx](/u/amxx), wow that is really great about ERC1538!   You definitely could write your article about ERC1538 and send your ERC1538 contracts for audit.  Probably most of what you write about ERC1538 applies to the diamond standard.  I am sorry about coming out with the newer standard. I thought of just updating ERC1538 but it was a lot of fancy clothes to put on.

I will look into the what you are talking about for delegating to `receive` and `fallback`. I don’t want the standard to miss any essential things.

You are right, the diamond standard is the same contract architecture as ERC1538.  I like to think of the diamond standard as ERC1538 wearing fancy clothes.

I’ll be looking into your ERC1538 implementation soon. I really appreciate this valuable feedback.

---

**mudgen** (2020-02-26):

I would love to see your article on ERC1538,  or diamond standard if you want to switch it to that.  From an experienced contract programmer who knows and uses ERC1538 I think your article would be very valuable.

---

**mudgen** (2020-02-26):

By the way, yesterday two people asked me to write articles about the diamond standard,  so I know content about the diamond standard or ERC1538 is in demand.

