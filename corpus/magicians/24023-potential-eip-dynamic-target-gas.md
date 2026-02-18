---
source: magicians
topic_id: 24023
title: "Potential EIP: Dynamic target gas"
author: SirSpudlington
date: "2025-05-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/potential-eip-dynamic-target-gas/24023
views: 62
likes: 0
posts_count: 1
---

# Potential EIP: Dynamic target gas

~~Instead of having a blocks target gas fixed to be exactly 1/2 of the gas limit of a block. What would happen if every 8192 epochs we take the average gas price for the last 8192 epochs and if it’s below (with some margin) a certain constant `g` we decrease the gas target by 1/1024 if it’s above, we increase it. This will prevent gas prices being too high/low for extended periods but keep them able to react short term. Maybe also adding a hard max limit of 3/4 of the gas limit.~~

Edit: After doing some math, it appears that this has the opposite effect, making it 10x more unstable.
