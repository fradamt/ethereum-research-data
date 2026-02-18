---
source: magicians
topic_id: 13404
title: Contract double create
author: RenanSouza2
date: "2023-03-18"
category: Uncategorized
tags: [create2, create]
url: https://ethereum-magicians.org/t/contract-double-create/13404
views: 459
likes: 1
posts_count: 3
---

# Contract double create

What happens, in a contract creation, if the address already has a code?

There is a solution for sending EOA transactions from addresses with code, should there also be a solution for this?

## Replies

**bawtman** (2023-03-18):

Hi [@RenanSouza2](/u/renansouza2), My guess is that it would revert, Beyond that if it happened to me I would go buy a bunch of lottery tickets. ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12)

---

**RenanSouza2** (2023-03-18):

I’m using the same thinking as in this article here, [EIP-3607: Reject transactions from senders with deployed code](https://eips.ethereum.org/EIPS/eip-3607),

this can be manipulated and I’m not understimating the increasing power of computers,

if this happens to you by accident I would like some of your lottery tickets haha

