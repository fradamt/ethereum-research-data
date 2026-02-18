---
source: magicians
topic_id: 21399
title: "EIP-7788: Dynamic target blob count"
author: marchhill
date: "2024-10-17"
category: EIPs > EIPs interfaces
tags: []
url: https://ethereum-magicians.org/t/eip-7788-dynamic-target-blob-count/21399
views: 160
likes: 1
posts_count: 5
---

# EIP-7788: Dynamic target blob count

Discussion thread for [Add EIP: Dynamic target blob count by Marchhill · Pull Request #8972 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8972)

> This EIP proposes to make the target blob count adjust dynamically up to a safe maximum target. This adjustment will target a constant price in ETH for blobs, aiming for consistent costs of L2 transactions.

## Replies

**ismeth** (2024-10-31):

This is definitely needed, especially after blob count increases above some level. I was also thinking something similar:

https ://x.com/ufukaltinok/status/1800565902133600431

I think it would be better if new target is dynamically adjusted based on how many times target hit in n epochs. For example if in the last n slots if blob count was above the target for k times, target should increase and vice versa.

I think n should be a lot more than 32 slots, could be even 10 epoch (320 slots).

---

**marchhill** (2024-11-01):

Interesting, why do you think this approach is better? My concern would be that such a mechanism would be too slow to react to changes in demand. There’s a tradeoff between reacting quickly to changes in demand, and changing the target too often - for me once per epoch seems reasonable.

Also, since the design aims to target consistent blob costs it adjusts when the average cost falls outside of the range of desired blob costs. It’s not clear to me why adjusting based on the number of times the target is hit would be better; how would we set this parameter, and under what conditions would the target be decreased?

---

**ismeth** (2024-11-01):

In my opinion, dynamic targets should be adjusted based on overall L2 demand observed over extended periods, rather than focusing solely on demand surges. The aim is to accommodate the organic growth of L2s while ensuring that blob costs are not free. In fact, I might suggest setting targets daily, informed by the previous day’s data.

With this EIP, we’ll introduce two mechanisms: one for adjusting blob gas prices during surge demand (eip1559 like) and another for catering to long-term L2 blockspace demand. I also believe that having two mechanisms addressing similar short-term goals might complicate effective strategizing for blob posting due to frequent oscillations in adjustments for L2s.

The adjustment could work like this: If, on average, blob usage in the last window is 20% below the target, the target should decrease; and if it’s above 5%, the target should increase for the next window.

---

**marchhill** (2024-11-01):

Ok that makes sense, maybe one epoch is too regular to change the target. I think this is something that would have to discussed with the community and L2 teams to decide on a value.

In terms of the adjustment, I think aiming for a specific blob cost accomplishes the same thing. Eventually (assuming reasonably constant demand) the target would settle on some equilibrium, the difference is the adjustment you describe would reach equilibrium at a random blob cost rather than one which has been explicitly targeted.

