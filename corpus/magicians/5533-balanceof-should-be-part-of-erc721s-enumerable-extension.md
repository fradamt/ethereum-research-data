---
source: magicians
topic_id: 5533
title: "`balanceOf` should be part of ERC721's enumerable extension"
author: Arachnid
date: "2021-03-10"
category: EIPs
tags: [erc-721]
url: https://ethereum-magicians.org/t/balanceof-should-be-part-of-erc721s-enumerable-extension/5533
views: 603
likes: 0
posts_count: 1
---

# `balanceOf` should be part of ERC721's enumerable extension

As far as I can tell, `balanceOf` on ERC721 serves almost no purpose unless the token implements the optional enumerability extensions. Without them, knowing how many tokens an account owns - but with no way to fetch what they are onchain - seems entirely pointless.

It’s too late to officially move it over, since 721 is final, but I wonder if it would be practical to issue an errata that it should not be relied on, and encourage implementations to make it optional? It wastes over 20k gas when issuing a token to a new account, and 5k on each token issued to an existing account.

If anyone reading relies on `balanceOf` for something other than enumerating tokens, I’d be keen to hear what it is, too.
