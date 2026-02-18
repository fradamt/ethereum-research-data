---
source: magicians
topic_id: 15904
title: "Add EIP: Expire state of the inactive accounts"
author: danpark
date: "2023-09-25"
category: EIPs > EIPs core
tags: [state-expiry]
url: https://ethereum-magicians.org/t/add-eip-expire-state-of-the-inactive-accounts/15904
views: 573
likes: 2
posts_count: 1
---

# Add EIP: Expire state of the inactive accounts

This EIP tries to enhance node efficiency by keeping data only for active accounts needed for data verification. This approach optimizes node operations and reduces the burden of managing inactive accounts by expiring them periodically. This approach is a form of account-level expiry, two-tree based solution according to [this](https://hackmd.io/@vbuterin/state_size_management)

https://github.com/ethereum/EIPs/pull/7776
