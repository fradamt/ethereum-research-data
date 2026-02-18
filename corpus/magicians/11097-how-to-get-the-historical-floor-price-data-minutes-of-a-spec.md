---
source: magicians
topic_id: 11097
title: How to get the historical floor price data (minutes) of a specified NFT?
author: BabyBluez
date: "2022-09-29"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/how-to-get-the-historical-floor-price-data-minutes-of-a-specified-nft/11097
views: 444
likes: 0
posts_count: 1
---

# How to get the historical floor price data (minutes) of a specified NFT?

Through an NFT contract address and a timestamp in minutes, the historical floor price at that moment can be returned.

This floor price is the floor price listed in the market (like the floor price displayed by gem.xyz), not the sale floor price.

For example, the function of [nftscoring.com](http://nftscoring.com) is very good, and you can also capture its api address for querying historical floor prices, but it can only display historical floor price data within 30 days, and it does not have 1-minute precision.

[![nftscoring_fp](https://ethereum-magicians.org/uploads/default/optimized/2X/f/ff8e46f612a437b7adcc50f6e69ef2d001e2ed41_2_690x482.png)nftscoring_fp893×624 65.5 KB](https://ethereum-magicians.org/uploads/default/ff8e46f612a437b7adcc50f6e69ef2d001e2ed41)

Many platforms have this function, but unfortunately, when querying historical floor prices for all time periods, the time interval for returning data is often hours or even days.

I have been trying for a few days to solve this problem. Happy to be able to ask questions here. I hope you can give me some pointers on what I should do, thank you very much.
