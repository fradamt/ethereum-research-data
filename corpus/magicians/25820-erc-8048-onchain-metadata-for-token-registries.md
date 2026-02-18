---
source: magicians
topic_id: 25820
title: "ERC-8048: Onchain Metadata for Token Registries"
author: nxt3d
date: "2025-10-15"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8048-onchain-metadata-for-token-registries/25820
views: 79
likes: 0
posts_count: 1
---

# ERC-8048: Onchain Metadata for Token Registries

Introduces a new standard for storing arbitrary metadata directly onchain for ERC-721, ERC-1155, ERC-6909, and ERC-8004 registries.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1259)














####


      `master` ← `nxt3d:onchain-metadata-branch`




          opened 10:46AM - 15 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/3857985?v=4)
            nxt3d](https://github.com/nxt3d)



          [+127
            -0](https://github.com/ethereum/ERCs/pull/1259/files)







Introduces a new standard for storing arbitrary metadata directly onchain for ER[…](https://github.com/ethereum/ERCs/pull/1259)C-721, ERC-1155, ERC-6909, and ERC-8004 registries.

**Key features:**
- Key-value pair interface: string keys mapped to bytes values for each token
- Required `getMetadata()` function and `MetadataSet` event
- Backwards compatible with existing token standards
- Enables trustless AI agents, proof of personhood, and custom metadata

This addresses the long-felt need for uniform onchain metadata storage while avoiding gas inefficiencies.

**Note on Standard History:**

This onchain metadata standard was originally introduced as part of ERC-8041 on **September 30, 2025** (commit `13f11f2`). ERC-8041 later pivoted to focus on fixed-supply agent collections, so this core metadata functionality is being reintroduced as a standalone standard.












**Key features:**

- Key-value pair interface: string keys mapped to bytes values for each token
- Required getMetadata() function and MetadataSet event
- Backwards compatible with existing token standards
- Enables trustless AI agents, proof of personhood, and custom metadata

This addresses the long-felt need for uniform onchain metadata storage while avoiding gas inefficiencies.

**Note on Standard History:**

This onchain metadata standard was originally introduced as part of ERC-8041 on **September 30, 2025** (commit `13f11f2`). ERC-8041 later pivoted to focus on fixed-supply agent collections, so this core metadata functionality is being reintroduced as a standalone standard.
