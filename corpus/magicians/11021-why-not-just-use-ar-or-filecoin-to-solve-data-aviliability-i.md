---
source: magicians
topic_id: 11021
title: Why not just use AR or filecoin to solve data aviliability issue？
author: xiaolese1
date: "2022-09-25"
category: Magicians > Primordial Soup
tags: [data, sharding]
url: https://ethereum-magicians.org/t/why-not-just-use-ar-or-filecoin-to-solve-data-aviliability-issue/11021
views: 702
likes: 0
posts_count: 3
---

# Why not just use AR or filecoin to solve data aviliability issue？

Since ethereum wants to be the data layer for Rollup, why not just build rollup in AR or Filecoin？

These two programs are focus on data aviliability. Every one can cheaply store data on AR or Filecoin.

## Replies

**fewwwww** (2022-09-26):

Data availbility is not the same as data storage.

In my understanding, data storage solutions like them cannot make sure the data are available, and the checking of whether the data is available is not efficient, cause you need to download all data to see if they are stored.

---

**xiaolese1** (2022-09-26):

As I know, storage program will check that for you,  see if nodes stores your data as you wish, that’s the key point of Filecoin or AR or Crust. Filecoin use zk to prove and crust use TEE to sample check. I mean this looks like data aviliability check to me

