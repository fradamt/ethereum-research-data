---
source: magicians
topic_id: 20337
title: "ERC-7737: Custom data access model"
author: "1999321"
date: "2024-06-19"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7737-custom-data-access-model/20337
views: 409
likes: 0
posts_count: 1
---

# ERC-7737: Custom data access model

The custom data access model uses solidity’s delegate mode to obtain the contract’s data read permissions. Corresponding reading logic can be developed through any third-party contract to obtain the desired data form. This model can save gas costs when it requires multiple accesses to the memory of a contract to obtain the final data form. It can even embed the required data processing logic directly into the agent contract, which is equivalent to native execution of data. Access and compute without making external calls.
