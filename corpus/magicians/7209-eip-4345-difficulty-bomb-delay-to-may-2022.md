---
source: magicians
topic_id: 7209
title: "EIP-4345: Difficulty Bomb Delay to May 2022"
author: timbeiko
date: "2021-10-05"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-4345-difficulty-bomb-delay-to-may-2022/7209
views: 46609
likes: 11
posts_count: 8
---

# EIP-4345: Difficulty Bomb Delay to May 2022

Discussion link for [EIP-4345](https://eips.ethereum.org/EIPS/eip-4345)

## Replies

**jdetychey** (2021-10-05):

[Following up on the messages we exchanged on [Github](https://github.com/ethereum/EIPs/pull/4345), copy-pasting it bellow to keep it all here]

**Jerome:**

`- As the Merge is getting ready, why not merging and canceling the Ice Age all together?`

*Tim:*

`Ideally, we never "reach" this difficulty bomb because we've merged before. But, if we haven't, I think it's better to have to push it back again. The alternatives are (1) remove the bomb altogether, which I don't think we should do (makes it easier for the PoW chain to keep going, also to launch scam forks) or (2) push the bomb *way* back, which is sort of equivalent to removing it in this context.`

---

The Difficulty bomb was introduced has a mean to strongly incentivize the Ethereum community to switch to PoS. The difficulty bomb schedules a network slowdown when its deadline is missed. The network suffered from previous bombs:

- Blocktime went up to ~30s before EIP-649 came to the rescue
- Blocktime went up to ~20s before EIP-1234 saved the day
- Blocktime went up to ~17s before EIP-2387 cut the right wire
- Blocktime wasn’t impacted as EIP-3554 pushed back the bomb even started ticking

This EIP is proposing to diffuse and delay the bomb for the 5th time. I assume no one would argue that the 4 previous intervention were not justified, the readiness of the switch to PoS was miles away from what it is today. I assume that, with the state of the network today, having even 0.1 sec more delay between blocks would greatly impact the user experience (transaction fees likely going to the roof). Nevertheless, I am concerned that removing all together or delaying the bomb again would arm the credibility of the Merge.

If the Merge is close to ready, if we start to tease on social media that tests of merge from clients is going well, let’s the just not delay and do the Merge.

---

**timbeiko** (2021-10-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> Nevertheless, I am concerned that removing all together or delaying the bomb again would arm the credibility of the Merge.
> If the Merge is close to ready, if we start to tease on social media that tests of merge from clients is going well, let’s the just not delay and do the Merge.

I think this is the crux of things. Even though the merge testing *is* going well, it isn’t going to happen until the difficulty bomb is due to go off again (early December, as per EIP-3554). We are not ~1 month away from having client releases ready for the merge, so we *need* to push the bomb back again.

I used this value as a rough proxy of when I think we could ship the merge if everything goes relatively well. If things didn’t go well, then we’d have to push the bomb back again. Obviously the EIP is still a draft and the specific time will need to be discussed further.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jdetychey/48/66_2.png) jdetychey:

> I assume that, with the state of the network today, having even 0.1 sec more delay between blocks would greatly impact the user experience (transaction fees likely going to the roof).

That’s a fair point. In the EIP, I assume that ~1 sec is what starts to be significant for UX impact, but I could be wrong here. If you think that even a 0.1 sec is very bad, then we can push back the block to target a 0.1 sec delay happening after we think the merge would realistically happen.

---

**EmpireBuilding** (2021-10-10):

Would it be correct to assume that there is no chance the the merge occurs prior to the difficulty bomb going off? Information seems to suggest that the transition will be dictated by a selected “Terminal total difficulty” I assume that difficulty target would be set in such a way that it would occur post bomb but before block times get too high?

---

**timbeiko** (2021-10-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/e/ebca7d/48.png) EmpireBuilding:

> Would it be correct to assume that there is no chance the the merge occurs prior to the difficulty bomb going off?

No chance it happens prior to “this” difficulty bomb (i.e. December). We should aim to have it happen before the next one, but if something went wrong in the planning/testing of the merge, we may have to push back the bomb again.

---

**timbeiko** (2021-10-12):

Great write-up by [@tjayrush](/u/tjayrush) about the EIP: [Adventures in Difficulty Bombing. An exercise in predicting the future… | by Thomas Jay Rush | Oct, 2021 | Medium](https://tjayrush.medium.com/adventures-in-difficulty-bombing-837890476630)

TL;DR: he proposes an offset of 10,700,000 so that the bomb starts showing around mid-May. The EIP currently proposes 10,500,000. If we wanted to do early May, then we could “meet in the middle” at 10,600,000.

---

**timbeiko** (2021-10-15):

We agreed on ACD124 to use 10.7m rather than 10.5m. PR for the update: [Update offset and calculations by timbeiko · Pull Request #4372 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4372)

---

**ilkersen3** (2022-05-08):

Could you please postpone the difficulty bomb to a few months later? We want the merge to go smoothly. As an Ethereum magic person, the slightest possibility of error is unacceptable. a few months late, but as long as we don’t make mistakes. Any negative situation during the merge, technical error, means that my savings that I invested in PoS will melt.

