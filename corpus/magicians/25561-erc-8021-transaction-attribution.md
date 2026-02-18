---
source: magicians
topic_id: 25561
title: "ERC-8021: Transaction Attribution"
author: conner
date: "2025-09-22"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8021-transaction-attribution/25561
views: 608
likes: 1
posts_count: 3
---

# ERC-8021: Transaction Attribution

Original PR: [Add ERC: Transaction Attribution by ilikesymmetry · Pull Request #1209 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1209/files)

Discussion happening in this telegram chat: [Telegram: Join Group Chat](https://t.me/+3bdizCng-2MxNmUx)

## Replies

**wjmelements** (2025-11-07):

Can it be backward compatible with existing schemes such as `CoinbaseSmartWallet`?

---

**conner** (2025-11-10):

Because the schema enforces a suffix to identify the ERC (`0x8021...8021`), it is not backwards compatible unfortunately.

