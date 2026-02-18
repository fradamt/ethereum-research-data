---
source: magicians
topic_id: 4982
title: "EIP: Add memo to Transaction (Requires hard fork)"
author: junderw
date: "2020-12-01"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-add-memo-to-transaction-requires-hard-fork/4982
views: 826
likes: 0
posts_count: 1
---

# EIP: Add memo to Transaction (Requires hard fork)

This is related to [EIP-2876](https://eips.ethereum.org/EIPS/eip-2876)

The following idea is an alternative to the above EIP for deposit systems (centralized exchanges and merchants being major use cases) to differentiate funds moving toward a single account.

By adding a memo space (it can be small and very limited, 8 bytes etc.) all deposits can be sent to one single cold wallet account, and the deposit watching system could just check the memo for an identifier.

This would allow for apps like BTCPay to easily support ETH deposits, ERC20 deposits, and much more by just checking the memo in all received transactions and matching it with the invoice in the local database.

Any thoughts?
