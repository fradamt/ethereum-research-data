---
source: magicians
topic_id: 6188
title: "EIP-3554: Ice Age delay targeting December 2021"
author: MadeofTin
date: "2021-05-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-3554-ice-age-delay-targeting-december-2021/6188
views: 10989
likes: 6
posts_count: 13
---

# EIP-3554: Ice Age delay targeting December 2021

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3554.md)





####

  [master](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3554.md)



```md
---
eip: 3554
title: Difficulty Bomb Delay to December 2021
author: James Hancock (@madeoftin)
discussions-to: https://ethereum-magicians.org/t/eip-3554-ice-age-delay-targeting-december-2021/6188
status: Final
type: Standards Track
category: Core
created: 2021-05-06
---

## Simple Summary
Delays the difficulty bomb to show effect the first week of December 2021.

## Abstract
Starting with `FORK_BLOCK_NUMBER` the client will calculate the difficulty based on a fake block number suggesting to the client that the difficulty bomb is adjusting 9,700,000 blocks later than the actual block number.

## Motivation
Targeting for the Shanghai upgrade and/or the Merge to occur before December 2021. Either the bomb can be readjusted at that time, or removed all together.

```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3554.md)










The delay is 500,000 extra blocks from the previous delay.

The adjustment is less than would be expected because the difficulty is so much higher today than previous adjustments.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5a499ee65b8434e0417d9e876fd94da19cd806a5_2_690x301.png)image2774×1212 176 KB](https://ethereum-magicians.org/uploads/default/5a499ee65b8434e0417d9e876fd94da19cd806a5)

There is a script in there as well to play around with cr: [@vbuterin](/u/vbuterin)

It will be helpful to re-run the numbers from time to time as the difficulty changes to make sure we are on target. A severe drop In difficulty could lead to increased block times seemingly out of nowhere.

## Replies

**MadeofTin** (2021-05-10):

The block prediction in the formula isn’t very accurate. I am rerunning the simulation using a targeted specific block number. https://etherscan.io/block/countdown/13766666

which is currently **Sat Dec 04 2021**

---

**timbeiko** (2021-05-12):

[@MadeofTin](/u/madeoftin) could we perhaps add 200,000 blocks to the delay to get one extra month?

As per [your comment on Github](https://github.com/ethereum/pm/issues/256#issuecomment-836560747) we would start to see the bomb go off in November:

> Reference block 12382958 (May-06-2021 08:38:33 PM +UTC)
> Nov - 5 months - 1.9% + .2 seconds
> Dec - 6 months - 7.6% + 1 second
> Jan - 7 months - 30% + 4 seconds
> Feb - 8 months - 121% + 16 seconds
> March - 9 months - 487% + 64 seconds

I personally would feel more confident if that first delay started in December vs. November.

Roughly, it seems there are ~200 000 blocks in a month (2.628e+6 secs ./ ~13 sec = 202153 ~= 200000). Would this change be as simple as swapping 9,500,000 for 9,**7**00,000 ?

---

**timbeiko** (2021-05-12):

[This commit](https://github.com/ethereum/EIPs/pull/3563/commits/eff4560790e4677e3b10ae8bc9a410aba512d070) addresses my concern above.

---

**MadeofTin** (2021-05-14):

I backtested for all of the times the difficulty bomb was first visible.

```auto
#First bomb sight May 1st 2017  (Coeff = 0.10)
#diff_adjust_coeff = predict_diff_bomb_effect(3630000,336173000000000,0,0)

#Second Bomb Sighting Dec 20th 2018 (Coeff=0.12)
#diff_adjust_coeff = predict_diff_bomb_effect(6920000,2263365000000000,3000000,0)

#Third Bomb Sighting Nov 10th 2019 (Coeff=0.11)
#diff_adjust_coeff = predict_diff_bomb_effect(8910000,2532534000000000,5000000,0)
```

This confirms the bomb should be seen when the Coeff reaches 0.1

---

**MadeofTin** (2021-05-14):

The first time the diff_adjustment_coeff is greater than `0.1` is at block Height 13800000 https://etherscan.io/block/countdown/13800000

This is because the difficulty bomb steps up only ever 10,000 blocks.

13700000 = 0.0761

13800000 = 0.1522

---

**timbeiko** (2021-05-17):

This is great, thanks!

Small ask: could we change the name of the EIP to " EIP-3554: Difficulty Bomb Delay to December ~~1st~~ 2021" so that it just mentions the month and not specific day?

---

**MadeofTin** (2021-05-21):

I did some further analysis and modeled what the difficulty bomb would look like under half the current difficulty and under double the current difficulty.

You can see if under the bomb will show 100_000 blocks early.

If double, the bomb will show 100_000 blocks later

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e5ab8d42a1ab4698514b5425612a65c7ec85c1fe_2_690x346.png)image908×456 20 KB](https://ethereum-magicians.org/uploads/default/e5ab8d42a1ab4698514b5425612a65c7ec85c1fe)

---

**MadeofTin** (2021-05-21):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/0/05ac2527e0ebee96430641a6d1999fdb7fd6bdc3_2_690x382.png)image807×447 7.92 KB](https://ethereum-magicians.org/uploads/default/05ac2527e0ebee96430641a6d1999fdb7fd6bdc3)

More accurate graph

---

**poojaranjan** (2021-07-04):

An overview of Difficulty bomb and EIP-3554 by [@MadeofTin](/u/madeoftin)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/6/6135afa8c9ef92b963cba49efb2c6fd06878b069.jpeg)](https://www.youtube.com/watch?v=QwCPrw-4d98)

---

**zemek** (2021-07-16):

As far as I understand – miners will start feeling this bomb someday in June 2022 and then it’ll be more and more noticeable.

But they still will be able to mine till ~June 2023 with a lot less rewards / lot more effort?

Or is this a race between difficulty bomb and the PoS transition?

Sorry if those are dumb questions, just spend a week trying to analyse miner’s perspectives and I’m still kind of lost. Warm hugs to [@MadeofTin](/u/madeoftin) for his interview, it got me some insights on the process.

---

**Evolution** (2021-08-06):

I would love this answered.  Is your statement accurate?

---

**snowpl** (2021-09-14):

Would love to hear response for [@zemek](/u/zemek) if mining will still be possible with a lot fewer rewards after POS (and for some time it will be a hybrid model) or once POS is there it will be not a single block to mine?

