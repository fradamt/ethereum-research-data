---
source: ethresearch
topic_id: 8494
title: A question about the liveness proof of casper
author: yj1190590
date: "2021-01-11"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/a-question-about-the-liveness-proof-of-casper/8494
views: 1796
likes: 2
posts_count: 5
---

# A question about the liveness proof of casper

I have a doubt when I read this section in the Casper-FFG paper :

[![屏幕截图 2021-01-11 145057](https://ethresear.ch/uploads/default/optimized/2X/1/1575c7aaadb002545d446b819894461f05377f07_2_690x168.png)屏幕截图 2021-01-11 1450571038×254 51.1 KB](https://ethresear.ch/uploads/default/1575c7aaadb002545d446b819894461f05377f07)

How can a’ be justfied if b is in an other branch?

like this:

[![屏幕截图 2021-01-11 155737](https://ethresear.ch/uploads/default/optimized/2X/b/b5a7dbe57d58910a2ae1021d6bfc6485b42455e2_2_345x199.png)屏幕截图 2021-01-11 155737777×449 19 KB](https://ethresear.ch/uploads/default/b5a7dbe57d58910a2ae1021d6bfc6485b42455e2)

Doesn’t it mean “stucked” for ever in this situation?

## Replies

**kladkogex** (2021-01-11):

I think the idea is that at some point you can build a supemajority link from “finalized” to a child of  a’.

This is assuming that a’ is on a winning branch. So you implicitly finalize a’ by  finalizing it child. Presumably at some point a’ will be well behind in history, and a supermajority of nodes will converge on a’ being on a winning branch.

---

**yj1190590** (2021-01-13):

Thanks. I confused block with epoch.

---

**BoltonBailey** (2021-01-16):

Thanks for posting this question, since it’s something that’s bugged me for a while and I’ve never gotten around to asking about it.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I think the idea is that at some point you can build a supermajority link from “finalized” to a child of a’.

This doesn’t make sense to me. The condition II in the “Casper commandments” states that a validator can’t make two votes (s_1, t_1) and (s_2, t_2) where h(s_1) < h(s_2) < h(t_1) < h(t_2). If we have a supermajority link from “finalized” in the above diagram to a child of a', then it seems to me the the 1/3 of validators that vote on the link from the top child of a to the top grandchild of a, and the 1/3 of validators that vote on the link from the bottom child of a to block b will be in violation of this commandment. But these validators make up 2/3 of all stake, so some of them will have to participate in any supermajority.

---

**kladkogex** (2021-01-18):

I think what may be a little confusing is that validators do not have to keep the same opinion.

The “Casper commandment”, as you call, it lets a validator change her mind.  What you seem to presume is that validators can not change here mind …

If I voted one way in the past I can vote in a different way in the future. In general a validator is supposed to vote with according to the majority  (as she perceives it according to her local picture).

So if she sees that a majority is converging in a particular way, she needs to change the vote.

What may cause confusion, is that the actual algorithm for the validator behavior is not described in the spec.

It would be an interesting thing to research how each of implemented clients behaves / which algorithm is used …

