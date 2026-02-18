---
source: ethresearch
topic_id: 12658
title: An other attempt at simplifying finality in Gasper
author: ulrych8
date: "2022-05-18"
category: Consensus
tags: []
url: https://ethresear.ch/t/an-other-attempt-at-simplifying-finality-in-gasper/12658
views: 1120
likes: 1
posts_count: 1
---

# An other attempt at simplifying finality in Gasper

I’ve seen the previous attempts of [@jacob-eliosoff](/u/jacob-eliosoff) [here](https://ethresear.ch/t/should-we-simplify-casper-votes-to-remove-the-source-param/3549) and [here](https://ethresear.ch/t/simplifying-casper-votes-to-remove-the-source-param-take-two/6398) suggesting to remove the source of the FFG vote in Gasper.

I think that in his quest to simplify Gasper, Jacob tried the wrong way. A quick simplification can be made by noticing that an *FFG vote* is redundant once a *GHOST vote* is made. Once you made a GHOST vote, you commit to one particular chain. If you are honest, the target and the source of your FFG vote will be on this same chain. And since the chain you support with the GHOST vote contains attestations, we can determine the target and source vote you would have voted (the target is the last checkpoint on this chain, and the source is the last justified checkpoint according to the attestations on that chain).

Thus, a new checkpoint will be justified at the end of an epoch if during this epoch at least 2/3 of the attesters made a GHOST vote on the same chain.
