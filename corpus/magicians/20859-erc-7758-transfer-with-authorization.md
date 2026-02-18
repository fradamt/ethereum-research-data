---
source: magicians
topic_id: 20859
title: "ERC-7758: Transfer With Authorization"
author: dongri
date: "2024-08-22"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7758-transfer-with-authorization/20859
views: 258
likes: 6
posts_count: 8
---

# ERC-7758: Transfer With Authorization

https://github.com/ethereum/ERCs/pull/598

## Replies

**radek** (2024-08-25):

Hi, ERC-2612 is mentioned and compared.

Could you please elaborate the improvement over ERC-3009?

---

**dongri** (2024-08-25):

https://github.com/ethereum/ERCs/pull/504

I think you can understand the background by looking at the differences and comments in this PR.

---

**radek** (2024-09-03):

ah, so is is the correction of the example code of 3009, i.e. no change in the standard as such.

[@abcoathup](/u/abcoathup) why this has a new ERC number?

---

**abcoathup** (2024-09-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> @abcoathup why this has a new ERC number?

The change needed the authors approval, otherwise a new EIP (with a new number) needed to be created (which is what happened).  As per [@SamWilsn](/u/samwilsn):

https://github.com/ethereum/ERCs/pull/504#pullrequestreview-2248218868

---

**radek** (2024-09-04):

Thanks for clarification. IMHO the outcome is the duplicity of the standard, where 3009 is already used (at least USDC).

---

**SamWilsn** (2024-09-10):

Duplicating it isn’t really a huge problem. If a 3009-like interface is already used in production, the relevant standard should be finalized. Doesn’t really matter if the number is 3009 or 7758.

When you feel it is ready, please open pull requests to move 7758 through Review, Last Call, and Final.

---

**dongri** (2024-09-10):

https://github.com/ethereum/ERCs/pull/632

open pull request

