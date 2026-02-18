---
source: magicians
topic_id: 649
title: Paying rent with deposits - Cross-post from ethresear.ch
author: jpitts
date: "2018-07-05"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/paying-rent-with-deposits-cross-post-from-ethresear-ch/649
views: 513
likes: 0
posts_count: 2
---

# Paying rent with deposits - Cross-post from ethresear.ch

Posted by [@Arachnid](/u/arachnid) on http://ethresearh.ch:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 12 Jun 18](https://ethresear.ch/t/paying-rent-with-deposits/2221)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          Sharding






            storage-fee-rent







Thinking about storage rent - what about requiring a deposit for all storage used, instead of a rental fee? The deposit can be refunded in its entirety when storage is freed up, and provides a direct financial incentive to free up unused storage,...



    Reading time: 4 mins 🕑
      Likes: 14 ❤

## Replies

**fubuloubu** (2018-07-05):

Isn’t this pretty much what happens now? We could increase the gas cost of `SSTORE` and have a more direct withdrawal when it’s reset.

