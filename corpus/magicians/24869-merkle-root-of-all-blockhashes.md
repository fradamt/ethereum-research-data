---
source: magicians
topic_id: 24869
title: Merkle Root of All Blockhashes
author: adraffy
date: "2025-07-21"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/merkle-root-of-all-blockhashes/24869
views: 70
likes: 1
posts_count: 1
---

# Merkle Root of All Blockhashes

Would it be possible to maintain a merkle root in a system contract like [EIP-2935](https://eips.ethereum.org/EIPS/eip-2935) or [EIP-4788](https://eips.ethereum.org/EIPS/eip-4788) that represents all blockhashes so we can verify deep historical data?

It could be some kind of 2-stage tree where the first level is a tree of block ranges `[0, N), [N, 2N), ..` and then each range is just a binary merkle of blockhashes so updaters only need to know the last `N` blocks and `height / N` range roots.   Probably there’s a more efficient structure.

Maybe something like this already exists and I don’t know about it.
