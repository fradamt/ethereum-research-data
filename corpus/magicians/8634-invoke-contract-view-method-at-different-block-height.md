---
source: magicians
topic_id: 8634
title: Invoke contract view method at different block height
author: numtel
date: "2022-03-17"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/invoke-contract-view-method-at-different-block-height/8634
views: 566
likes: 3
posts_count: 4
---

# Invoke contract view method at different block height

From my searches, it does not seem possible to invoke contract view methods at a different block height. Although this would probably incur significant gas, it seems like it would allow a contract to use a liquidity pool (or multiple or an average over multiple blocks) as a source of price data since it would mitigate flash loan manipulations.

Is my understanding correct? Would this be possible?

## Replies

**Pandapip1** (2022-03-18):

IIUC, view functions are not actually included in blocks and are instead evaluated by the node (that’s why they cost no gas).

---

**numtel** (2022-03-18):

Yes, of course this is the case but I’m specifically asking about invoking the method from another contract. I’m well aware that I can call the function at any height if I’ve got a node.

---

**Pandapip1** (2022-03-18):

Okay, that makes more sense. That’s out of my realm of expertise now. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

