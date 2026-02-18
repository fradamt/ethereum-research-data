---
source: ethresearch
topic_id: 12762
title: Delaying Difficulty Bomb to mid August 2022
author: ericmartihaynes
date: "2022-06-01"
category: The Merge
tags: []
url: https://ethresear.ch/t/delaying-difficulty-bomb-to-mid-august-2022/12762
views: 4741
likes: 9
posts_count: 13
---

# Delaying Difficulty Bomb to mid August 2022

Discussion for [EIP-draft_difficulty_bomb_delay](https://github.com/ericmartihaynes/EIPs/edit/master/EIPS/eip-draft_difficulty_bomb_delay.md)

## Replies

**quickBlocks** (2022-06-01):

This spreadsheet might help think about when to reset and by how much. I’d love an extra set of eyes on it.



      [docs.google.com](https://docs.google.com/spreadsheets/d/13bPCmuVhrWhL3KzIsjLWptRKNhS43gpFjKMgqBuFd14/edit#gid=0)



    https://docs.google.com/spreadsheets/d/13bPCmuVhrWhL3KzIsjLWptRKNhS43gpFjKMgqBuFd14/edit#gid=0

###

Sheet1

1. If you want this period...
                   Period
Change this ==&gt;,37,38,39,40,41,42
2. And Real Block is...,3. Then set the offset to this...
Real Block,                Block...

---

**quickBlocks** (2022-06-07):

I guess the bomb is here.

[![image](https://ethresear.ch/uploads/default/optimized/2X/4/48ff0dc6b05cb7f81253353ee8b333992bb2ec50_2_690x449.png)image3200×2086 467 KB](https://ethresear.ch/uploads/default/48ff0dc6b05cb7f81253353ee8b333992bb2ec50)

---

**quickBlocks** (2022-06-08):

The link to the EIP appears to be broken. [adding junk so I can post]

---

**ericmartihaynes** (2022-06-08):

I just noticed as well, but can’t seem to edit it. Any clues?

---

**mr.yalamanchi** (2022-06-09):

[@ericmartihaynes](/u/ericmartihaynes) no worries. Picked up the EIP-5133 from your fork.

Here’s the link: [EIPs/eip-5133.md at 2573d17a8016c236e02ba69984742b0de379d986 · ericmartihaynes/EIPs · GitHub](https://github.com/ericmartihaynes/EIPs/blob/2573d17a8016c236e02ba69984742b0de379d986/EIPS/eip-5133.md)

---

**quickBlocks** (2022-06-10):

I’m not a Pythonista. (I’m basically a copy-and-paster.) When I copy and paste the python in the EIP into `file` and do `python file`, I get no result.

Here’s another script that Tim Beiko posted previously: [v bomb script · GitHub](https://gist.github.com/timbeiko/4c6d32852a1fab8c61b183ca3c273417).

---

**ericmartihaynes** (2022-06-10):

[@quickBlocks](/u/quickblocks) You can just paste it here and it should work as well: https://replit.com/languages/python3

You might need to add “print(diff_adjust_coeff)” at the end to print the result

---

**ericmartihaynes** (2022-06-13):

[EIP-5133](https://github.com/ethereum/EIPs/blob/cd901d240aeaefc22d9aa12f2169bbc0f6b942c0/EIPS/eip-5133.md)

---

**timbeiko** (2022-06-13):

Cross posting from the [R&D discord](https://discord.com/channels/595666850260713488/745077610685661265/985944445461626910):

> For context, earlier today we had a regularly scheduled testing call between client & testing teams where the difficulty bomb pushback ended up being the main/only topic we covered.

> Given the rushed conversation about it on Friday’s AllCoreDevs + confusion here over the weekend,  I wanted to make sure all EL client teams were on the same page.

> The first bit was about how much of a block time increase is acceptable, and whether we should aim for the delay to start kicking in when we expect to be ready to merge, or for blocks to not be exceeding X time. After some back and forth, we’ve converged on the former: trying to Merge before block times noticeably slow down.

> The second bit was then about whether the 500,000 blocks proposed in EIP-5133 was the right amount. More context here: the script used in the EIP (and the Arrow Glacier bomb pushback, and previous ones too) underestimates when the bomb starts showing up. The best way to predict the (starting) impact is simply to look at the number of blocks being added, and use that as an offset. If we delay it by 500,000 blocks, then we’ll be in the same spot 500,00 blocks from now.

> Given these two things, we tried to find a number for the delay which leads the bomb to start showing at a time when we think we can run The Merge on mainnet. The rough consensus there was that mid-September felt right. Earlier is possible, but hinges on basically not hitting any hiccups. We therefore agreed to make the delay 700,000 blocks. This means that late September, we’d be at roughly the same block time as now (~14.5s) and so 2 weeks before, in mid-Sept, the effects will start being noticeable (>13.5s blocks, similar to early June block times).

---

**ericmartihaynes** (2022-06-13):

The EIP has changed to reflect increasing the delay to 700K blocks. We also modified the script to more clearly communicate assumptions. The previous script worked well in order to predict when the difficulty bomb would first go off, but assumed that block times would remain at 13.3s. Once the bomb detonates this doesn’t hold true anymore.

The new script predicts the block number at which the bomb will go off after the delay. The bomb is considered active when the `diff_adjust_coeff` is 0.1, as [previously discussed](https://ethereum-magicians.org/t/eip-3554-ice-age-delay-targeting-december-2021/6188/5) regarding EIP-3554.

As for the delays after the bomb is activated, like [@timbeiko](/u/timbeiko) mentioned above, we would experience block times similar to the ones now (~14.5s) around late September.

---

**ericmartihaynes** (2022-06-14):

Discussion for EIP moved here: https://ethereum-magicians.org/t/eip-5133-delaying-difficulty-bomb-to-mid-september-2022/9622

---

**quickBlocks** (2022-06-21):

One more. Just to keep people informed. The red line is at June 29. The dashed pink line is Mar. 9 which was block 14,350,000 or 700,000 blocks prior to 15,050,000.

[![image](https://ethresear.ch/uploads/default/optimized/2X/b/b62161dc92434d646390c1fec88f86cd50194cc2_2_690x451.png)image2910×1904 374 KB](https://ethresear.ch/uploads/default/b62161dc92434d646390c1fec88f86cd50194cc2)

