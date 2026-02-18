---
source: magicians
topic_id: 4595
title: Problem while submitting a pull requiest
author: AlePart
date: "2020-09-10"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/problem-while-submitting-a-pull-requiest/4595
views: 535
likes: 1
posts_count: 2
---

# Problem while submitting a pull requiest

i had this error with htmlproofer  while submitting my [pull request](https://github.com/ethereum/EIPs/pull/2966). someone can help me?

Error:

Liquid error (/home/travis/build/ethereum/EIPs/_includes/eiptable.html line 11): comparison of Array with Array failed included in all.htmle[0m

## Replies

**matt** (2020-09-11):

Hi [@AlePart](/u/alepart), it looks like the problem is that you didn’t have an EIP number assigned to the EIP. Since your PR is #2966, I would assign it that. This means you need to update the `eip` field in the header and the filename to be `eip-2966.md`. That should resolve your issues. If you’d like to pursue your EIP, please reopen PR and make these changes, then ping me (@lightclient).

