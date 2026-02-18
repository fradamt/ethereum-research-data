---
source: magicians
topic_id: 8893
title: "EIP-4938: Removal of GetNodeData"
author: fjl
date: "2022-04-11"
category: EIPs > EIPs networking
tags: []
url: https://ethereum-magicians.org/t/eip-4938-removal-of-getnodedata/8893
views: 2145
likes: 0
posts_count: 3
---

# EIP-4938: Removal of GetNodeData

This is the discussion thread for EIP-4938.

## Replies

**jochem-brouwer** (2022-04-12):

If I want to implement Beam Sync (each time DB does not have a trie node, use `GetNodeData` to retrieve said node) if this EIP is activated, then I should use `GetTrieNodes` of `snap/1`, right? However, I am slightly confused how I should upgrade here. As I understand correctly, I should query by path, but since I don’t have the full trie then I cannot query said path, only partial paths? Am I correct that the `path` here is the path in the trie? (So starting from root we move down the trie in order to reach an account leaf)

EDIT: Maybe I’m wrong here, and `path` is actually the path in the trie? So it would work the same as `GetNodeData`?

---

**rjl493456442** (2022-06-15):

According to the snap protocol spec, the path here refers to the partial path from root to node.

More detail [devp2p/snap.md at master · ethereum/devp2p · GitHub](https://github.com/ethereum/devp2p/blob/master/caps/snap.md#gettrienodes-0x06)

