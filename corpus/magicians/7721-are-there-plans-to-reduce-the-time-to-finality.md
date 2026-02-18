---
source: magicians
topic_id: 7721
title: Are there plans to reduce the time-to-finality?
author: nicszerman
date: "2021-12-08"
category: Uncategorized
tags: [questions]
url: https://ethereum-magicians.org/t/are-there-plans-to-reduce-the-time-to-finality/7721
views: 798
likes: 0
posts_count: 3
---

# Are there plans to reduce the time-to-finality?

Much of the conversation regarding the future of Ethereum has been around improving transactions per second, privacy, security, data storage, and some specific applications. I think there is another very important metric which seems to be mostly left out: time to finality (TTF).

The TTF metric seems crucial to me for many applications. You probably want it to be at most in the seconds to make payments to merchants in person, for example. You want it to be in the sub seconds for many games or for high frequency trading.

Are there any plans to improve the TTF in the future? Would it be possible to have an L2 which sacrifices some security but enables faster TTF? It seems to me that naively reducing the number of blocks required for finality is a bad idea, since the security decreases exponentially to achieve a linear improvement in TTF.

## Replies

**AndersonTray** (2021-12-10):

I have only heard from a friend that they are planning to do so in the next coming year

---

**nicszerman** (2021-12-11):

Vitalik made a proposal recently about the time to finality:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 20 Sep 21](https://ethresear.ch/t/a-model-for-cumulative-committee-based-finality/10259/18)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          Consensus






Interesting! One argument against this attack is that it’s extremely unlikely that a committee will be a coordinated group among themselves but not have a stake in the rewards of the other validators. Realistically, for any committee attack the be...

