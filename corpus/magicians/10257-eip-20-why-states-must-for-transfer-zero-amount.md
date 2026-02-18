---
source: magicians
topic_id: 10257
title: "EIP-20: why states MUST for transfer zero amount?"
author: vsmelov
date: "2022-08-05"
category: EIPs
tags: [token, erc-20]
url: https://ethereum-magicians.org/t/eip-20-why-states-must-for-transfer-zero-amount/10257
views: 799
likes: 0
posts_count: 2
---

# EIP-20: why states MUST for transfer zero amount?

in [ERC-20: Token Standard](https://eips.ethereum.org/EIPS/eip-20)

you have

> Note Transfers of 0 values MUST be treated as normal transfers and fire the Transfer event.

I am security auditor and I often face with clients who have

```auto
require(amount > 0, "prohibited");
```

in their erc-20 token implementation.

It looks intuitive, that indeed, transfer for zero amount makes not sense.

1. Why EIP-20 states “MUST” for allowing such transfers? What is the rationale behind?
2. What is the risk if you prohibit transfer for zero amount?

My proposal is to add sich rationale inside EIP-20 standard to avoid confusion and incompliency

## Replies

**Dexaran** (2023-10-25):

It is not the worst thing of ERC-20 standard, for example there are [known problems of ERC-20](https://dexaran820.medium.com/known-problems-of-erc20-token-standard-e98887b9532c) such as lack of error handling and placing a burden of determining the behavior related to the internal logic of the contract on the end user.

It is unlikely that you will get ERC-20 standard modified however, it is immutable since it reached its final state.

