---
source: magicians
topic_id: 2973
title: UseCases for account abstraction
author: Ethernian
date: "2019-03-23"
category: EIPs
tags: [account-abstraction]
url: https://ethereum-magicians.org/t/usecases-for-account-abstraction/2973
views: 1055
likes: 1
posts_count: 3
---

# UseCases for account abstraction

Please correct me, but I hear again and again, that [EIP859 - Account Abstraction](https://github.com/ethereum/EIPs/issues/859) is hard stuff and the implementation is postponed because of that.

Let us remember what we need it for.

Maybe the UseCases are so important, that we will consider a specific MVP implementation?

Here we go…

**The Account Abstraction Use Case List:**

1. Fail-fast Tx calls for CREATE2 contracts
Optionally submit and check of target contract’s codebase hash and fail-fast on mismatch. It should atomically prevent unexpected behavior if codebase silently changes.
2. Tx call by ENS name: native ENS Support in EVM.
Support ENS name as the transaction Target and resolve it on the fly (using the global cache for performance) to the Target address before execution.
It makes the Upgradable Contract Pattern more clear and straightforward.
3. Anything else?

## Replies

**lrettig** (2019-03-26):

There’s a bunch on this topic over at ethresear.ch, including https://ethresear.ch/t/a-recap-of-where-we-are-at-on-account-abstraction/1721.

---

**Ethernian** (2019-03-26):

oh, great! thank you!

