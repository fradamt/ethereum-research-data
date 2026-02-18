---
source: magicians
topic_id: 8951
title: Calculating Type2 (EIP1559) gasFees
author: arjn
date: "2022-04-18"
category: EIPs
tags: [gas, eip-1559, transactions]
url: https://ethereum-magicians.org/t/calculating-type2-eip1559-gasfees/8951
views: 688
likes: 0
posts_count: 1
---

# Calculating Type2 (EIP1559) gasFees

Currently, I am using the [metaswap codefi network API](https://gas-api.metaswap.codefi.network/networks/3/suggestedGasFees).

I find it highly unreliable and uncomfortable to be dependent on an external API for fetching the gas parameters.

Is there any other way, function or formula to calculate the `maxFeePerGas` and `maxPriorityFeePerGas` ?

If not, then it is high time to develop a standardized function for the same.

I require the gas parameters between a range : slow, medium and fast.
