---
source: magicians
topic_id: 3188
title: Community Call with Swarm - Storage Rent
author: boris
date: "2019-04-24"
category: Working Groups > Ethereum 1.x Ring
tags: [storage-rent, community-call, swarm]
url: https://ethereum-magicians.org/t/community-call-with-swarm-storage-rent/3188
views: 1484
likes: 15
posts_count: 10
---

# Community Call with Swarm - Storage Rent

From a discussion on Twitter about Storage Rent and Swarm:

https://twitter.com/AFDudley0/status/1121077041233842176

Please follow this thread if you are interested in a community call, and we’ll update it with timing – likely week of May 6th.

[@AFDudley](/u/afdudley) [@AlexeyAkhunov](/u/alexeyakhunov)

## Replies

**edinalovas** (2019-04-25):

Hi All,

This is Edina from Swarm. I would like to organize a call with you guys, shall I set up a doodle?

At the Swarm Orange Summit in Madrid (May 23-25) we will have a workshop on Ethereum Blockchain on Swarm and would like to invite you there to discuss this further.

Best,

Edina

---

**tgerring** (2019-04-25):

Is there a particular time that workshop is scheduled for and are there any other topics that might intersect with this theme?

If there is sufficient interest, maybe it’s worth setting aside non-summit time to meet as well.

---

**tvanepps** (2019-05-02):

It really depends on [@AFDudley](/u/afdudley) / [@AlexeyAkhunov](/u/alexeyakhunov)’s availability. I will try to reach them.

A doodle poll would be good to coordinate on if they have time this week!

---

**AlexeyAkhunov** (2019-05-02):

I had a call with some of the Swarm team members yesterday. I suggest doing community call as a part of summit (if there is a space in the agenda)

---

**boris** (2019-05-02):

Ok. Or afterwards with a summary. Mainly want to help the Swarm team tell their story and have people have an opportunity to ask questions live. Will leave this for now - let us know if we can help.

---

**jpitts** (2019-05-02):

Are there conversations/topics which we can get started here in the meantime? It may help get organized before the “kick-off call” from the summit.

[@tgerring](/u/tgerring) [@nonsense](/u/nonsense) [@AFDudley](/u/afdudley) …  and also [@tjayrush](/u/tjayrush) from the Data Ring

---

**tgerring** (2019-05-26):

On Day 3 of Swarm Summit, we had a 90 minute discussion on improvements towards Ethereum based on Swarm.

We agreed that it would be useful to store  Ethereum block data on Swarm as an idea to improve the synchronization experience of adaptive nodes.

[@pipermerriam](/u/pipermerriam) Was so kind as to capture this in the following proposal:  https://github.com/ethersphere/user-stories/issues/9

---

**shemnon** (2019-05-26):

The linked spec has only headers in its subprotocol.  Why only headers?  To do a full sync bodies are needed and a fast sync also requires receipts.  If you are only validating the chain head then you can use headers only.

---

**tgerring** (2019-05-27):

Lacking a more robust answer from someone else, my understanding is that it was a result of the desire to start simple and build complexity over time

