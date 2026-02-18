---
source: magicians
topic_id: 13441
title: "EIP-6732: Redeemable Tokens"
author: LucazFFz
date: "2023-03-20"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-6732-redeemable-tokens/13441
views: 875
likes: 0
posts_count: 5
---

# EIP-6732: Redeemable Tokens

Hi everbody!

Created this ERC for redeemable tokens as a part of a school assignment. Would love any feedback / criticism.

https://github.com/ethereum/EIPs/pull/6732

## Replies

**vic** (2023-05-13):

Hi will this proposal be merged into the main repository under draft stage?

---

**SamWilsn** (2023-09-13):

Once the review process finishes, yes, probably.

---

**SamWilsn** (2023-09-13):

Token standards generally don’t define functions like `setMaxSupply`, `setBatchMaxSupplies`, `setPrice`, `setBatchPrice`, or even `mint` because these operations are generally only controlled by the same entity that deployed the token contract. Generally, EIPs only exist to coordinate between multiple parties.

I’d recommend either removing functions from the standard that are only ever called by the contract owner, or adding some justification to your Rationale section explaining why these functions need to be standardized.

---

**SamWilsn** (2023-09-13):

On another note, I believe that removing the transfer family of functions will lead to a much worse user experience than ERC-1155 with transfer functions that revert.

With standard transfer functions (that always revert) a user can *try* to transfer, and receive a useful error message when it fails. Most wallets won’t even try to put a reverting transaction on-chain.

On the other hand, without standard transfer functions, how does the wallet even know if it should display UI elements for a transfer? That’s a whole other ordeal.

