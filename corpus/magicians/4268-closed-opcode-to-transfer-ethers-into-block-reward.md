---
source: magicians
topic_id: 4268
title: "[CLOSED] Opcode to transfer ethers into block reward"
author: rumkin
date: "2020-05-11"
category: Magicians > Primordial Soup
tags: [evm, opcodes, eth1x]
url: https://ethereum-magicians.org/t/closed-opcode-to-transfer-ethers-into-block-reward/4268
views: 795
likes: 0
posts_count: 3
---

# [CLOSED] Opcode to transfer ethers into block reward

## Abstract

Some contracts uses fees as a spam protection. This money mostly are using as a reward to contract owners, but for simple contracts like registries the fee size could be illogically big as a reward for zero activity from the contract owners. It’s especially relevant when we talk about socially meaningful contracts. And it seems fair enough to transfer this fee into a block reward. Seems like it requires a new opcode for this.

> I feel like I saw this idea before, but I couldn’t find the EIP for it. If it’s so provide a link please.

## Replies

**wjmelements** (2020-05-13):

There is the COINBASE opcode and so you can CALL with COINBASE as the recipient arg. We don’t need a special opcode therefore.

---

**rumkin** (2020-05-13):

Thanks. It was lame ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=9)

