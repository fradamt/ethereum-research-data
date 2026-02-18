---
source: magicians
topic_id: 19676
title: Union Lock based on TSTORE/TLOAD can avoid flash loan attacks
author: "1999321"
date: "2024-04-16"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/union-lock-based-on-tstore-tload-can-avoid-flash-loan-attacks/19676
views: 918
likes: 4
posts_count: 7
---

# Union Lock based on TSTORE/TLOAD can avoid flash loan attacks

The feature of Union Lock can query the number of calls of other contracts and the number of calls of other contract functions in the same Ethereum transaction, thereby realizing the cross-contract locking function.

related link:

eip link: [Add EIP: Union Lock by 1999321 · Pull Request #8442 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8442)

test cases: [GitHub - 1999321/Union-Lock](https://github.com/1999321/Union-Lock)

## Replies

**zhous** (2024-06-18):

*Flash Loan attack* can grab millions of dollars from decentralized vaults in one single transaction, so this EIP would be meaningful.

Great!

---

**Aranna-0572** (2024-06-18):

glad to see a new update from this! we need more ideas

---

**Hanna** (2024-06-19):

a meaningful update EIP-1153！

---

**0x_WeakSheep** (2024-06-19):

Is there any relevant practice code available? I would like to study it. Thank you.

---

**ZWJKFLC** (2024-06-24):

This is a meaningless ERC submission

Before this, using the hash value of “tx. origin+blocknumber” could also achieve the same function, which is to charge more gas.

---

**JCXsivan** (2024-06-24):

I think its really a good idea

