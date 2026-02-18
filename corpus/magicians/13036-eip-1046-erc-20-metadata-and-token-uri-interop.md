---
source: magicians
topic_id: 13036
title: "EIP-1046: ERC-20 Metadata and Token URI Interop"
author: Pandapip1
date: "2023-02-23"
category: EIPs
tags: [metadata]
url: https://ethereum-magicians.org/t/eip-1046-erc-20-metadata-and-token-uri-interop/13036
views: 2523
likes: 3
posts_count: 5
---

# EIP-1046: ERC-20 Metadata and Token URI Interop

This is the new discussion link if [Update EIP-1046: Move back to Review and add myself as author by Pandapip1 · Pull Request #6563 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6563) is merged.

Old discussion link:

https://www.reddit.com/r/raredigitalart/comments/8hfh1g/erc20_metadata_extension_eip_1046/

## Replies

**abcoathup** (2023-02-24):

With the proposed expansion to include ERC721.the title should change.

I regularly wish I had got token level metadata included in ERC721: [EIP 821: Distinguishable Assets Registry (Contract for NFTs) · Issue #821 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/821#issuecomment-358167639)

---

**Pandapip1** (2023-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> I regularly wish I had got token level metadata included in ERC721: EIP 821: Distinguishable Assets Registry (Contract for NFTs) · Issue #821 · ethereum/EIPs · GitHub

That would be a great EIP. Go ahead and write it!

---

**radek** (2023-10-21):

Is there any statistics on how many ERC20 token are using this ERC1046?

Considering the major ones, I am not sure it got any adoption traction.

Also advising not using name() goes against the autowrapping multichain protocols like xERC20.

---

**ivica** (2024-06-22):

I would also like to know how widely erc-1046 is adopted. Is it a problem that meta data behind the url could be changed silently? Moreover recommending not to implement erc-20 data fields (name, symbol, …) is actually breaking the erc-20 interface.

