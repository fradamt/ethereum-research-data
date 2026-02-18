---
source: ethresearch
topic_id: 2578
title: Exit Queue Stuck Issue
author: maxweng
date: "2018-07-16"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/exit-queue-stuck-issue/2578
views: 1259
likes: 0
posts_count: 4
---

# Exit Queue Stuck Issue

For Plasma, if for whatever reason a withdraw request to the RootChain smart contract fails and gets reverted, it’ll just keep stucking in the exit queue and blocking all the remaining withdrawals. I found out this issue while I’m working on trying to withdrawal ERC20 or ERC721 tokens, which forked from the Plasma MVP (https://github.com/fastxprotocol/plasma-mvp).

I guess the operator can just simply delete the stuck withdrawal tx. But in a real world, the operator won’t have that much power, right? I also tried to leave a mark with event logs so anyone can send the delete request and the smart contract can do the verification, but it seems that event logs are reverted when the withdraw requests fails and get reverted.

Wondering if anyone sees this issue or has any insights.

## Replies

**josojo** (2018-07-16):

Yes, this was and maybe still is an issue.

I know that there were 2 PRs open that fixed it. But the omisego team decided to not include them. It was mentioned in the closure of the PR that this will be dealt with later, once it goes into production.

Maybe they have found a better solution in the meantime.

If they have no solution yet, and you are interested, one PR was from my side with this commit:



      [github.com/josojo/plasma-mvp](https://github.com/josojo/plasma-mvp/commit/6aa6c9c29d689388ced6999bb4520775030cebbd)












####



        committed 04:28PM - 11 Apr 18 UTC



        [![](https://ethresear.ch/uploads/default/original/3X/b/1/b1b7bcf0079a8e21de8a9f3cd1ceafc7937b2afc.jpeg)
          josojo](https://github.com/josojo)



        [+20
          -2](https://github.com/josojo/plasma-mvp/commit/6aa6c9c29d689388ced6999bb4520775030cebbd)

---

**maxweng** (2018-07-17):

That’s a good idea you coming up with, about separating the finalize_exit and withdraw_fund into 2 transactions. I think it’s good enough for me. I’m adapting it to fit ERC20/721 tokens.

---

**kfichter** (2018-08-07):

omisego’s temporary solution to this problem was to ignore any errors and skip the payout. This isn’t ideal in the long term, it’d be better to have an isolated pool of funds from which these contracts can manually withdraw. You still need to enforce an ordering but you don’t want to allow a user to block the queue by not withdrawing, so you need to give each user a small window of time in which they can withdraw.

