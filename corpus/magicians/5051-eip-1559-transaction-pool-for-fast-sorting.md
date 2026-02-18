---
source: magicians
topic_id: 5051
title: EIP-1559 Transaction Pool for Fast Sorting
author: minaminao
date: "2020-12-20"
category: Uncategorized
tags: [eip-1559]
url: https://ethereum-magicians.org/t/eip-1559-transaction-pool-for-fast-sorting/5051
views: 769
likes: 0
posts_count: 1
---

# EIP-1559 Transaction Pool for Fast Sorting

![](https://ethereum-magicians.org/uploads/default/original/1X/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://hackmd.io/@minaminao/Hy0ZyFn3w)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



# ******# EIP-1559 Transaction Pool for Fast Sorting  ## TL;DL - The idea of an EIP-1559 transaction










Discussions in Eth R&D Discord: [Discord](https://discord.com/channels/595666850260713488/749160974506000444/790156754347753472)

## TL;DL

- The idea of an EIP-1559 transaction pool for fast sorting.
- Computational complexity

Add a transaction in $O(\log n)$
- Sort transactions when basefee changes in $O(k \log n)$
- Pop the most profitable transaction in $O(\log n)$
- Produce a block in $O(m \log n)$
- $n$: The number of transactions in a txpool
- $k$: The number of transactions where the miner bribe varies with basefee
- $m$: The number of transactions in a block

Implementation: [GitHub - minaminao/eip1559txpool](https://github.com/minaminao/eip1559txpool)
