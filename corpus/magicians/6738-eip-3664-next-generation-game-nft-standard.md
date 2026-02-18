---
source: magicians
topic_id: 6738
title: "EIP-3664: Next Generation Game NFT Standard"
author: T.Y
date: "2021-07-28"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-3664-next-generation-game-nft-standard/6738
views: 4482
likes: 1
posts_count: 2
---

# EIP-3664: Next Generation Game NFT Standard

In this proposal, we created the gNFT standard, which makes up for the problem that ERC-1155 can only support packed transfer and unchangeable attributes of NFTs. gNFT can make the attributes in the game props have four characteristics: transferable, upgradeable, changeable and evolvable. By using ERC-3664 standard NFTs in game, players are able to complete almost all operations on props only through smart contracts!

For details, please check [EIPs/eip-3664.md at master · DRepublic-io/EIPs (github.com)](https://github.com/DRepublic-io/EIPs/blob/master/EIPS/eip-3664.md)

Also, suggestions are welcome! Let’s make game NFT standard stronger:)

## Replies

**SamWilsn** (2022-03-14):

Would you mind updating the first post to link directly to the PR in the `ethereum/EIPs` repository?

---

The `TransferSingle` and `TransferBatch` events shadow the names of the EIP-1155 interface. While they might not conflict on a technical level (maybe they do, I’m not sure), I would propose renaming them to `AttributeTransferSingle` and `AttributeTransferBatch` to make it clear what is being transferred.

---

Reusing `balanceOf` to read the value of an attribute seems a bit misleading. Maybe choosing a different name (ex. `attachedTo`) would make it more clear?

