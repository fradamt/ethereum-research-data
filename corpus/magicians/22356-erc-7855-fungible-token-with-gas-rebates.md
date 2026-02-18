---
source: magicians
topic_id: 22356
title: ERC-7855 Fungible Token with gas rebates
author: theBigRevolution
date: "2024-12-28"
category: ERCs
tags: [erc, token, erc-721, erc-20]
url: https://ethereum-magicians.org/t/erc-7855-fungible-token-with-gas-rebates/22356
views: 119
likes: 0
posts_count: 5
---

# ERC-7855 Fungible Token with gas rebates

Discussion topic for ERC-7855 <[link to ERC](https://github.com/blockchainDevAmitesh/ERC7849/blob/erc7849/ERCS/erc-7855.md)>

#### Update Log

- 2024-01-01: initial draft

#### External Reviews

Sam Wilson [@SamWilsn](/u/samwilsn) updated erc-7849 to erc-7855

#### Outstanding Issues

None as of 2025-01-06.

## Replies

**wjmelements** (2025-01-06):

Since you’re extending ERC20 you don’t have to re-specify ERC20 in your ERC.

---

**theBigRevolution** (2025-01-12):

For informational purposes, I thought it was important to note it.

---

**wjmelements** (2025-01-14):

It clutters your proposal with redundant information. It’s not informationally beneficial because it’s redundant. It’s redundant because the dependency is linked at the top. Your proposal doesn’t need to explain ERC20. ERC20 can explain ERC20.

---

**wjmelements** (2025-01-14):

I built gas refunds into TrueUSD when I was at TrustToken. The scheme used the SSTORE refund, setting 1’s to 0’s. This mostly doesn’t work anymore because the refund cap was reduced from half to 20%.

Some disadvantages to your proposal:

- emits an event; this costs gas
- one rebate per user; tracking this costs gas and makes every transfer worse, adding 20000+ gas
- rebate amount ambiguously defined as 25%
- requires ether transfer; this adds 9000 gas

Normally a token transfer uses 15k to 30k gas, so adding 29k+ will make it around 50% worse.

In summary your token will add more than 25% to the transfer gas to rebate less than 25% of the transfer gas. This is a bad mechanism, though it could still have marketing advantages.

Since your rebate percentage is so close to the theoretical limit imposed by eip-3529, you could consider using the SSTORE refund, but I suspect that this will also rarely be cost-effective due to relatively stable gas prices.

