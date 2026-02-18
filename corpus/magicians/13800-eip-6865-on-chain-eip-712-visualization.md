---
source: magicians
topic_id: 13800
title: "EIP-6865: on-chain EIP-712 Visualization"
author: a6-dou
date: "2023-04-12"
category: EIPs
tags: [eip-712]
url: https://ethereum-magicians.org/t/eip-6865-on-chain-eip-712-visualization/13800
views: 1801
likes: 0
posts_count: 3
---

# EIP-6865: on-chain EIP-712 Visualization

PR link: [Add EIP: on-chain EIP-712 Visualization by a6-dou · Pull Request #6865 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6865)

Numerous protocols employ distinct EIP-712 schemas, leading to unavoidable inconsistencies across the ecosystem. To address this issue, we propose a standardized approach for dApps to implement an on-chain view function called `visualizeEIP712Message`. This function takes an abi encoded EIP-712 payload message as input and returns a universally agreed-upon structured data format that emphasizes the potential impact on users’ assets. Wallets can then display this structured data in a user-friendly manner, ensuring a consistent experience for end-users when interacting with various dApps and protocols.

The adoption of a universal solution will not only streamline the efforts and reduce the maintenance burden for wallet providers, but it will also allow for faster and more extensive coverage across the ecosystem. This will ultimately result in users gaining a clearer understanding of the transactions they’re signing, leading to increased security and an improved overall user experience within the crypto space.

We are seeking reviews and comments from Ethereum community, EIP maintainers, Wallets and Dapps developers that uses EIP-712

## Replies

**SamWilsn** (2023-05-17):

You’ve looked at [ERC-6384](https://eips.ethereum.org/EIPS/eip-6384) I assume?

Some optional bike shedding on the names:

- to and from are a bit ambiguous. I’d prefer validAfter and validBefore, where isValid() = validAfter < now() < validBefore.

---

**a6-dou** (2023-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> You’ve looked at ERC-6384  I assume?

Yes, we found out about Zengo proposal from their [red pill attack article](https://www.techtarget.com/searchsecurity/news/365533432/ZenGo-finds-transaction-simulation-flaw-in-Coinbase-others) at late stage of implementing this proposal, the key difference is that this proposal treat visualization result as structured data which is in my opinion more easier to implement and to use by off-chain client compared to string based buffers (enumerable structs to take advantage of various EVM types)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Some optional bike shedding on the names:
>
>
> to and from are a bit ambiguous. I’d prefer validAfter and validBefore, where isValid() = validAfter < now() < validBefore.

`validAfter` and `validBefore` are more Date Domain-specific than `from` and `to` which is a good point.

My only concern is that using `validAfter` and `validBefore` can lead to misinterpretation of the intended meaning. For example, “validBefore” may be mistakenly perceived as the starting point of validity, while “validAfter” may be perceived as the ending point where in `from` - `to` is more straightforward and less error prone

