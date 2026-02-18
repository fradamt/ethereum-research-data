---
source: magicians
topic_id: 8464
title: "[IDEA] On-chain UI"
author: Pandapip1
date: "2022-03-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/idea-on-chain-ui/8464
views: 667
likes: 1
posts_count: 2
---

# [IDEA] On-chain UI

Currently, DApps are standard websites that happen to have some of their logic in ethereum or other chains. It would be nice if DApps instead contained *all* their functionality (including user interface) on-chain.

This ERC would provide a framework to create a set of components (like navbars, modals, forms, and links, which would be standardized in a subsequent ERC) that would allow for a wide variety of user-interfaces. This ERC would also provide a mechanism for DApps to request to create their own components.

With [ERC-4834 - Hierarchical Domains Standard by Pandapip1 · Pull Request #4835 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4835), the DApp’s contract address could be resolved with a human-readable name. This would mean that interacting with fully on-chain DApps wouldn’t be significantly different than using a web browser, except that the applications are now fully on-chain, and accessibility is improved due to the fact that all websites now use a common set of components (which could potentially be customized by the user).

## Replies

**mfornet** (2022-03-16):

There is an implementation of this idea on NEAR:

https://web4.near.page/

