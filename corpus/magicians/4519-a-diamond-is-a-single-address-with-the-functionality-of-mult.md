---
source: magicians
topic_id: 4519
title: A diamond is a single address with the functionality of multiple contracts that are independent from each other but can share internal functions, libraries and state variables
author: mudgen
date: "2020-08-20"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/a-diamond-is-a-single-address-with-the-functionality-of-multiple-contracts-that-are-independent-from-each-other-but-can-share-internal-functions-libraries-and-state-variables/4519
views: 561
likes: 0
posts_count: 3
---

# A diamond is a single address with the functionality of multiple contracts that are independent from each other but can share internal functions, libraries and state variables

I tried to make it very clear what an Ethereum diamond is and how it works in the [latest revision of the Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535).  Did I succeed?


      [github.com](https://github.com/mudgen/EIPs/blob/patch-21/EIPS/eip-2535.md)




####

```md
---
eip: 2535
title: Diamond Standard
author: Nick Mudge
discussions-to: https://github.com/ethereum/EIPs/issues/2535
status: Draft
type: Standards Track
category: ERC
created: 2020-02-22
---

![image](../assets/eip-2535/diamond.svg)

## Simple Summary

A new smart contract paradigm that works today.

A diamond is a contract that implements the Specification in this standard.

Diamonds are powerful, organized, modular, optionally upgradeable, flexible, unlimited in size, and transparent.
```

  This file has been truncated. [show original](https://github.com/mudgen/EIPs/blob/patch-21/EIPS/eip-2535.md)

## Replies

**dysbulic** (2020-08-28):

I’m very much a beginner, but I was able to follow what you wrote for the most part. I get what the diamond pattern is and, had I the Solidity knowledge, I could start writing one.

Personally, I’d like to see more examples of facets and how they’re written. The code examples really helped solidify the concepts.

---

**mudgen** (2020-08-28):

That’s great. Have you seen the Diamond reference implementation?  It is good to look at how its contracts are written: https://github.com/mudgen/Diamond   And the reference implementation is useful to get started writing a diamond.

More examples are coming.  Also, I hope bloggers/writers will write some diamond tutorials.

