---
source: ethresearch
topic_id: 13642
title: View-merge algorithm
author: anand
date: "2022-09-12"
category: Consensus
tags: []
url: https://ethresear.ch/t/view-merge-algorithm/13642
views: 2253
likes: 0
posts_count: 4
---

# View-merge algorithm

In [Vitalik’s recent talk at the Stanford Blockchain Conference](https://www.youtube.com/watch?v=8DHGOlIlMvc&t=1938s) (51% attack recovery), he mentions the view-merge algorithm (47:08), by which online nodes can tell which other nodes are online. This, of course, has implications for a censorship / exclusion attack.

Where is this research at? I wasn’t able to find a paper describing the view-merge algorithm or any adjacent research (besides of course [the classic Vitalik ethresear.ch post](https://ethresear.ch/t/responding-to-51-attacks-in-casper-ffg/6363) on 51% attack responses in Casper FFG).

## Replies

**adompeldorius** (2022-09-12):

Could it be [this](https://www.paradigm.xyz/2022/09/goldfish)?

---

**fradamt** (2022-09-19):

Other than that, there’s this: [Change fork choice rule to mitigate balancing and reorging attacks](https://ethresear.ch/t/change-fork-choice-rule-to-mitigate-balancing-and-reorging-attacks/11127)

More to come soon

---

**anand** (2022-11-03):

Thanks, that mentions it. It also links explicitly to this, which was helpful: [View-merge as a replacement for proposer boost](https://ethresear.ch/t/view-merge-as-a-replacement-for-proposer-boost/13739).

