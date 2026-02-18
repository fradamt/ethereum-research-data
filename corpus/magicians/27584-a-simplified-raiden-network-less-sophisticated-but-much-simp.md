---
source: magicians
topic_id: 27584
title: A simplified Raiden Network (less sophisticated but much simpler)
author: bipedaljoe
date: "2026-01-25"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/a-simplified-raiden-network-less-sophisticated-but-much-simpler/27584
views: 14
likes: 0
posts_count: 1
---

# A simplified Raiden Network (less sophisticated but much simpler)

I like multihop payments a lot and I recently solved the coordination problem there (see [here](https://resilience.me/3phase.pdf)) but I also like simplicity and compromise when a simpler system can reach the goal better at the moment.

There is a mostly unknown payment network principle of “three-party novation”, where you invert a central network and it will behave as if it was a central network accounting-wise but it is computationally decentralized. I.e., it is ***very*** fast. This seems like it could work well for payment channels (over “state channels”…) A network of routers that are tightly connected (it does not have to be a perfect inverted central network but the closer it gets to one the better it clears debt) could reach infinite speed, and let users be members of a router (with a payment channel) and pay anyone else. A user reaches any other user in three hops.

[![Network_Topology_1_](https://ethereum-magicians.org/uploads/default/optimized/3X/6/8/68d6a4d3c8f1021d78cff8a5b6ae8ed91127d66c_2_690x206.jpeg)Network_Topology_1_1000×300 32.7 KB](https://ethereum-magicians.org/uploads/default/68d6a4d3c8f1021d78cff8a5b6ae8ed91127d66c)

The three-party novation itself is that in A to B to C where B is an intermediary in terms of debt, B simply asks A and C to move the debt directly between themselves. This is then accounting-wise the same as A to bank to B to bank to C, but it is computationally decentralized.

Infinitely fast Raiden Network. Can eventually scale up to the true multihop vision but something like this could take off more easily, faster. Users could use a relay network like Nostr to manage their interaction with their router, and thereby store the coins (their private key) locally without having to trust any third party with it.

I implemented 3-party novation a week ago, I used these coordination rules. It is overall extremely simple.

[![novation](https://ethereum-magicians.org/uploads/default/optimized/3X/1/5/15449d83754647f5ec834707387e21befecd1fd1_2_552x500.jpeg)novation600×543 52.7 KB](https://ethereum-magicians.org/uploads/default/15449d83754647f5ec834707387e21befecd1fd1)
