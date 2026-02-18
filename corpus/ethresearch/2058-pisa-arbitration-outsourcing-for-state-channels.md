---
source: ethresearch
topic_id: 2058
title: "Pisa: Arbitration Outsourcing for State Channels"
author: stonecoldpat
date: "2018-05-23"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/pisa-arbitration-outsourcing-for-state-channels/2058
views: 2111
likes: 1
posts_count: 2
---

# Pisa: Arbitration Outsourcing for State Channels

Hey,

I’d like to introduce Pisa which is a solution to the Monitor problem for state (and payment) channels:

http://hackingdistributed.com/2018/05/22/pisa/

The blog post covers the high-level idea quite well, but to summarise:

- A generic state channel construction (from Sprites) to build any application in a state channel
- An accountable third-party agent called the Custodian who can be hired to watch the channel on behalf of the customer.

Over the next few months, we plan to implement and evaluate some applications using the state channel construction, and of course to build the custodian. I’d love to get everyones feedback on whether this might be useful to their project!

p.s. We’ve taken care (and a significant amount of time) to write our paper in the most approachable manner possible. Let me know if we succeeded or not!

Links to paper:



      [cs.cornell.edu](https://www.cs.cornell.edu/~iddo/pisa.pdf)



    https://www.cs.cornell.edu/~iddo/pisa.pdf

###



1213.52 KB

## Replies

**kosecki123** (2018-07-06):

Great paper, thank you for sharing.

One topic that wasn’t addressed in the paper is the mechanism of hiring the custodian. I’m wondering whether

Pisa essentially be a vertical solution for state channels monitoring or protocol that enables the market for 2nd layer availability market?

