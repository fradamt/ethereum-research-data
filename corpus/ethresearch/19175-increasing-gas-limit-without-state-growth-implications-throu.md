---
source: ethresearch
topic_id: 19175
title: Increasing Gas Limit Without State Growth Implications Through Periodic Scheduled Downtime
author: MaxResnick
date: "2024-04-01"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/increasing-gas-limit-without-state-growth-implications-through-periodic-scheduled-downtime/19175
views: 1427
likes: 12
posts_count: 3
---

# Increasing Gas Limit Without State Growth Implications Through Periodic Scheduled Downtime

Lately there has been increased discussion of raising the block gas limit from 30m gas to 40m gas. Critics of this proposal argue that increasing the gas limit risks excessive state bloat which could impact the ability to run full nodes on consumer hardware. With stateless light clients still far away we argue that a different solution could allow us to increase the gas limit without contributing to state bloat. We suggest periodic scheduled downtime outside 9 am-5 pm EST.

Periodic scheduled downtime has a number of advantages:

1. Reduced state growth: By having scheduled downtime, the Ethereum network would have regular periods where no new transactions are being processed. This means that the state would not be growing during these times, helping to control the overall state size.
2. Node maintenance: Scheduled downtime provides an opportunity for node operators to perform necessary maintenance tasks, such as pruning the state, switching to RETH, or plugging in more hard drives. This can help ensure that nodes continue to run efficiently and can handle the increased gas limit.
3. Missed Slots: Fewer blocks per day means fewer opportunities for missed slots caused by optimistic relays and other bugs.
4. Network resilience: Regularly scheduled downtime can help identify and address potential issues with the network before they become critical. For example, if an entity is engaging in a socially slashable activity, regularly scheduled downtime allows time for us to coordinate with the social slashing committee and prepare a hard fork before activity resumes.
5. MEV smoothing: Data shows that MEV rewards are higher during EST business hours (see Figure 1 below for Average MEV-Boost payments by hour of day, this is based on 200,000 blocks from … to … ). This is unfair to solo stakers who randomly propose their blocks at night. By scheduling downtime at night, we avoid the unfair distribution of MEV rewards.

[![meme](https://ethresear.ch/uploads/default/optimized/2X/f/f3ae5fbdbaf3ed34099a896b63eacd0244a9655d_2_690x377.jpeg)meme1280×700 73.2 KB](https://ethresear.ch/uploads/default/f3ae5fbdbaf3ed34099a896b63eacd0244a9655d)

Of course, there are some disadvantages— a key one that comes to mind is that this arrangement may be unfair to Solo stakers in RoW: While a 9 am – 5pm chain will be ideal for solo stakers based in North America, it can be incredibly inconvenient for a staker in e.g. Asia (straightforward calculations show that this will be 11pm–7am for a staker in Singapore). Nevertheless we believe the stated advantages overwhelm these.

In conclusion, implementing periodically scheduled downtime outside of peak hours could provide a balanced solution that allows for increased gas limits while mitigating the risks of excessive state growth. As the Ethereum network continues to evolve, it is crucial to explore and adopt innovative approaches to scaling that maintain the network’s decentralization and accessibility.

## Replies

**LefterisJP** (2024-04-01):

For any future readers of this(especially crypto journalists) please understand, the post was written on April 1st ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

---

**abcoathup** (2024-04-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> Periodic scheduled downtime

Only if you label a chain as Beta.

![](https://ethresear.ch/user_avatar/ethresear.ch/lefterisjp/48/15126_2.png) LefterisJP:

> especially crypto journalists

I wonder how many crypto journalists read everything in Eth Research?

