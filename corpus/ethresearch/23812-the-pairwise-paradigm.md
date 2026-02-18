---
source: ethresearch
topic_id: 23812
title: The Pairwise Paradigm
author: kronosapiens
date: "2026-01-08"
category: Economics
tags: [public-good]
url: https://ethresear.ch/t/the-pairwise-paradigm/23812
views: 142
likes: 4
posts_count: 3
---

# The Pairwise Paradigm

Pairwise methods have been part of Ethereum’s public goods funding toolkit for years, and are well-adapted to social choice in environments of scarce attention, but their full potential has been limited by fragmented and partial applications.

This essay treats pairwise as a *design paradigm* for distributed capital allocation, connecting algorithm and pair selection with interface and audience development to form a coherent, end-to-end system.

The goal is to equip practitioners with a complete context for deploying pairwise methods effectively.


      ![](https://ethresear.ch/uploads/default/original/3X/8/7/87add881aafc5297781abe7f384737530d46073d.png)

      [kronosapiens.github.io](http://kronosapiens.github.io/blog/2025/12/14/pairwise-paradigm)





###



      The Pairwise Paradigm










I have been working with pairwise methods for distributed governance since 2016; this essay reflects lessons learned across research and practice.

Feedback and discussion welcome.

## Replies

**vbuterin** (2026-01-09):

Good post, thank you for writing it!

Regarding the continuous paradigm, how much of the benefit do you expect will come from it being fully continuous, as opposed to simply having automated very frequent rounds (eg. 30 or 7 day cycle)?

I know it’s a goal of the deep funding effort to get to having automated frequent rounds, and historically Gitcoin etc has failed to do it realistically because it was not automated enough, and with humans deadlines easily slip etc.

Regarding IIA, I personally find that axiom to be overrated, and I think it’s possible to come up with principled reasons why “a good voting rule” would not necessarily satisfy it: [Reddit - The heart of the internet](https://www.reddit.com/r/math/comments/1noy4if/comment/nfxo2u9/)

In general, I think human preferences *are* cardinal much more than ordinal, we just don’t have very good explicit access to our preferences, and ordinal happens to be one of several good ways to easily get some of our information out. So if we treat ordinal queries as an approximation, rather than as a fundamental input, then this becomes easier to reason about.

---

**kronosapiens** (2026-01-09):

Thanks for engaging!

Some thoughts:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Regarding the continuous paradigm, how much of the benefit do you expect will come from it being fully continuous, as opposed to simply having automated very frequent rounds (eg. 30 or 7 day cycle)?
>
>
> I know it’s a goal of the deep funding effort to get to having automated frequent rounds, and historically Gitcoin etc has failed to do it realistically because it was not automated enough, and with humans deadlines easily slip etc.

I’d draw a distinction between the *underlying mechanism* and the *productization* of that mechanism. A fully continuous mechanism could be presented to users (grantees, voters) as fully continuous, or discretized into epochs, etc, all without changing the underlying machinery. This would allow exploration of different user-facing configurations while preserving the administrative efficiency of a fully-continuous substrate.

At [the coliving house](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4856267) (which you once visited!) the system is fully continuous. It works well for that setting (daily chores), but other settings might benefit from having more clearly-defined epochs, which would be more amenable to things like social media campaigns, get-out-the-vote drives, etc.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In general, I think human preferences are cardinal much more than ordinal, we just don’t have very good explicit access to our preferences, and ordinal happens to be one of several good ways to easily get some of our information out. So if we treat ordinal queries as an approximation, rather than as a fundamental input, then this becomes easier to reason about.

I agree that differences in intensity of preference is a real and meaningful thing, and that the relative preference is only the “most significant bit.” My caution comes more from a skepticism of our ability to measure these differences accurately. If cardinal preferences are capturing more noise than signal (i.e. are measurements of mood or personality) then all we’ve done is given ourselves a de-noising task which hands power back to round administrators – which I would argue is what we’re seeing with Deep Funding now. Combined with cardinal measurements taking longer to make, and we’re net down on signal overall.

As an aside, one of the best things about QV/QF in my opinion was the way it constrained cardinal measurements to avoid these issues.

