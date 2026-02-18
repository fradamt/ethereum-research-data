---
source: magicians
topic_id: 24715
title: "EIP-7983: Granular Transaction Types"
author: marchhill
date: "2025-07-02"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7983-granular-transaction-types/24715
views: 77
likes: 1
posts_count: 1
---

# EIP-7983: Granular Transaction Types

Discussion thread for [Add EIP: Granular Transaction Types by Marchhill · Pull Request #9962 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9962)

> This proposal extends the capacity for new transaction types with a new transaction envelope beginning with 0xFF. The new type allows for more granular control; multiple transaction types can be combined together by being enabled in a bit field.
>
>
> The existing transaction type envelope introduced in EIP-2718 supports up to 128 different transaction types. Although this may seem like enough for the forseeable future, these could be rapidly used up due to the introduction of compound types, that combine existing transaction types.
>
>
> As an example, consider what would happen if a new transaction type is introduced for account abstraction (eg. EIP-7701). If smart accounts become widely adopted, there is a need to introduce many more types, combining the account abstraction transaction type with blob transactions, setcode transactions, etc. Account abstraction is one example, but the same argument could apply to any new transaction type added in future. This could lead to a combinatorial explosion in the number of transaction types.
>
>
> The new transaction format both extends the space for new transaction types, and allows for existing transaction types to easily combined.
