---
source: magicians
topic_id: 4435
title: "EIP-2746: Rules Engine Interface"
author: jaerith
date: "2020-07-19"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2746-rules-engine-interface/4435
views: 2250
likes: 1
posts_count: 3
---

# EIP-2746: Rules Engine Interface

https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2746.md

**Simple Summary**

An interface for using a smart contract as a rules engine. A deployed instance of the contract can register a data domain, create sets of rules that perform actions on that domain, and then invoke a set as an atomic transaction.

The original thread for this proposal can be found here:

[[EIP-?: Rules Engine Interface](https://ethereum-magicians.org/t/eip-rules-engine-interface/4374)]

([EIP-?: Rules Engine Interface](https://ethereum-magicians.org/t/eip-rules-engine-interface/4374))

## Replies

**mudgen** (2020-07-28):

Thanks for including a reference to the Diamond Standard in EIP 2746.

The Diamond Standard now has its own EIP here: https://eips.ethereum.org/EIPS/eip-2535

Consider updating the reference to use that URL.

---

**jaerith** (2020-07-28):

No problem, sir.  It’s been updated.

