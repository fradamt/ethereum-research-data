---
source: magicians
topic_id: 9044
title: "EIP-1238: Non-Transferable Tokens"
author: ra-phael
date: "2022-04-25"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-1238-non-transferable-tokens/9044
views: 1765
likes: 0
posts_count: 1
---

# EIP-1238: Non-Transferable Tokens

Discussion thread for https://github.com/ethereum/EIPs/issues/1238

We have been working on a proposal for it which is presented here: https://erc1238.notion.site

Some TL;DR considerations for this proposal in its current form:

- It’s based on ERC1155. This allows managing both fungible and non-fungible non-transferable tokens in one smart contract and for example minting a badge and reputation points in one transaction.
- It requires consent from the recipient for minting.
- Some extensions have been explored but might not need to be included in this standard.

Feedback here, or as comments on the notion pages, is welcome!
