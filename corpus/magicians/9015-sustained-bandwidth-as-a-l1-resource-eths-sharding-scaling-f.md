---
source: magicians
topic_id: 9015
title: Sustained bandwidth as a L1 resource + ETH's sharding/scaling future
author: realty
date: "2022-04-22"
category: Magicians > Primordial Soup
tags: [gas, governance, networking]
url: https://ethereum-magicians.org/t/sustained-bandwidth-as-a-l1-resource-eths-sharding-scaling-future/9015
views: 778
likes: 0
posts_count: 1
---

# Sustained bandwidth as a L1 resource + ETH's sharding/scaling future

Several EIPs (e.g. 4488, 4844) have been proposed which advocate for increasing avg block size by up to an order of magnitude while mitigating state growth through new data retention requirements.

Additionally this slide is making the rounds which considers burst, but not sustained, bandwidth as a limiting resource.

[![media_FQ4CJpPVsAA7iVa.jpg?name=small](https://ethereum-magicians.org/uploads/default/original/2X/d/d5f83466a74773c6c935cc66da74ade1209fe2e3.jpeg)media_FQ4CJpPVsAA7iVa.jpg?name=small680×364 30.2 KB](https://ethereum-magicians.org/uploads/default/d5f83466a74773c6c935cc66da74ade1209fe2e3)

Setting aside burst bandwidth limits, the community and the proposers of the above and similar EIPs need to have a discussion on what the acceptable limits are for the data usage of the network.

Current monthly data usage for a user running a CL/EL client pair is in the low single terabyte range.

If something like EIP-4844 is introduced (which proposes economics incentivizing 1mb avg blocks vs ~100kb now) , we could easily see data usage reach 20+ TB per month.

Is this a number that the community is comfortable with?  How many personally run nodes/validators will be forced/incentivized to transfer to AWS or a staking pool?  How do we balance those costs vs. the gains (L2 fee reduction)?
