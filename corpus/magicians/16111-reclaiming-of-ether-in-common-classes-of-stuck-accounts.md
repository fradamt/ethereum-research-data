---
source: magicians
topic_id: 16111
title: Reclaiming of ether in common classes of stuck accounts
author: Pandapip1
date: "2023-10-16"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/reclaiming-of-ether-in-common-classes-of-stuck-accounts/16111
views: 660
likes: 2
posts_count: 4
---

# Reclaiming of ether in common classes of stuck accounts

Migrating conversation from

https://github.com/ethereum/EIPs/issues/156

## Replies

**akcryptoguy** (2023-10-16):

Thank you for keeping this alive.  I still support the return of ether stuck in the null address.  How can we make this happen?

---

**Pandapip1** (2023-10-16):

The best way to do this, IMO, is to review EIP-1 and try to resuscitate and modernize EIP-867 to work with the new EIP process. The first step is to submit a PR that changes the status to Draft and adds yourself as an author. If/when that’s merged, you can make changes as you see fit by submitting PRs that modify the EIP (they will be automerged), and once you’re happy you can request that it be moved to Review by submitting a PR that updates the status.

---

**ReyRod** (2025-04-03):

Came here after watching the Vice documentary about QuadrigaCX and learning more about this particular issue. It seems like this should be pretty easy to fix.

So far, it appears that we can identify which transactions led to the funds being stuck. Therefore, the new smart contract should be able to revert each transaction and maintain a hash so that these transactions cannot be reverted multiple times. Am I getting it right?

I’ve made a PR to revive the EIP

