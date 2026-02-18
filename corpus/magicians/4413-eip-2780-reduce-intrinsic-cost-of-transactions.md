---
source: magicians
topic_id: 4413
title: "EIP-2780: Reduce intrinsic cost of transactions"
author: matt
date: "2020-07-11"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-2780-reduce-intrinsic-cost-of-transactions/4413
views: 3178
likes: 2
posts_count: 9
---

# EIP-2780: Reduce intrinsic cost of transactions

Discussion thread for [EIP-2780: Reduce intrinsic transaction gas](https://github.com/lightclient/EIPs/blob/reduce-intrinsic-cost/EIPS/eip-2780.md)

(Note: `16,340` is a back-of-the-napkin estimate until we can perform better load testing on a testnet and analyze its performance)

Inspired by this thread: https://twitter.com/uriklarman/status/1281972141055934464?s=20

## Replies

**zemse** (2020-07-11):

If the account is not initialized, then would it make a difference? For example if we consider `20000` for writing to an uninitialized storage, `(16 * 110) + 2 * 800 + 2 * 20,000  + 3000 = 46,360`.

---

**matt** (2020-07-11):

You’re correct. I need to update the EIP to better outline both scenarios, highlighting the discrepancy.

---

**uri** (2020-07-14):

I think there are two potential (and compatible) EIPs here:

1. Significantly adjusting down the 21K gas cost for sending Tx - keeping everything else as-is.
2. Differentiating between sending Tx to a new account vs an existing account.

I want to outline my arguments for the 1st approach, which I believe delivers 90% of the value to the Ethereum community, can be achieved much quicker, carry very little risk, complexity or debt, and is incremental in nature.

However, I don’t want to “hog” your EIP on this, which feels to me leaning towards the 2nd approach.

Should I fork this with my own take  or should I add another EIP?

---

**matt** (2020-07-14):

[@uri](/u/uri) don’t worry about hogging the EIP, please feel free to fork it and add in your outline. I welcome it and look forward to reading your arguments. Although I don’t think there is any need worrying about this until after you complete your outline, I feel strongly that 1 should not be done unless 2 is also done. Please add yourself as an author to the EIP so you can automerge changes in the future. Thanks.

---

**uri** (2020-07-20):

I hope I didn’t mess up the process, but I submitted my draft for this to your branch.

---

**matt** (2020-08-08):

This EIP was discussed by [@uri](/u/uri) in [ACD #93](https://youtu.be/Riu-PqrJVH4?t=2379).

The main points of feedback were:

- generally speaking, there are other more concerning problems with the network (state size growth) that should be addressed before more EIPs which negatively impact this are accepted
- some calculations should be double checked, especially the state size growth when new accounts are created
- approximately 3x as many transactions will be possible within a block, so how will the network handle the increased block size?

---

**benaadams** (2025-09-05):

This has been revived, but change is to

> Reduce intrinsic transaction gas from 21k to 6k and charge 25k when a value transfer creates a new account

---

**gurukamath** (2026-01-29):

Currently, the [specs](https://github.com/ethereum/execution-specs/blob/7c8ec4ff4ac84ce6cb61863a2311d7c80140db5c/src/ethereum/forks/amsterdam/fork.py#L559) do perform checks on the sender code to ensure that it is either empty or is a valid 7702 delegation. Was just wondering how that aligns with this line from the EIP

“`tx.sender` is charged as a cold non-code account (`COLD_ACCOUNT_COST_NOCODE = 500`), representing the first access and coalesced account-leaf update.“

