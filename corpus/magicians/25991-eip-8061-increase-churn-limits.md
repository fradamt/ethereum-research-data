---
source: magicians
topic_id: 25991
title: "EIP-8061: Increase churn limits"
author: fradamt
date: "2025-10-27"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8061-increase-churn-limits/25991
views: 105
likes: 0
posts_count: 3
---

# EIP-8061: Increase churn limits

Discussion topic for [EIP-8061](https://eips.ethereum.org/EIPS/eip-8061)

## Replies

**rolfyone** (2025-11-07):

The validator arrays aren’t great to iterate now, which kind of remains un-addressed, so going to an increased churn may exacerbate that problem again - its less about active validators and more about the size of the array because we iterate it so often (several times at epoch transition).

If we addressed that array structure it’d potentially become academic, either through reuse or allowing us to have a sparse array or something, haven’t thought through exactly but the max index at time of writing on mainnet is `2122156` (over double the number active now)

I do think we should have an open discussion about whether we really need to maintain the separate consolidation path long term, it seems like we’re better off not fragmenting the exit queue and creating an uneven playing field. That is probably better as a separate eip, but arguably may make this eip very different if theres one exit path and no consolidation to consider.

---

**rolfyone** (2025-11-10):

Just to capture side chat

- talked about retaining the deposit cap
- talked about why we want separate consolidation, and makes sense
- eip got updated reflecting those things.

Probably to remove the deposit cap we’d want to address how heavily we iterate the validators during epoch transition which is definitely out of scope (and now not a problem because deposit cap is remaining).

