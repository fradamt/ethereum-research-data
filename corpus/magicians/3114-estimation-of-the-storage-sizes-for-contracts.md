---
source: magicians
topic_id: 3114
title: Estimation of the storage sizes for contracts
author: AlexeyAkhunov
date: "2019-04-10"
category: Working Groups
tags: [storage-rent, ethereum-1x]
url: https://ethereum-magicians.org/t/estimation-of-the-storage-sizes-for-contracts/3114
views: 1179
likes: 3
posts_count: 5
---

# Estimation of the storage sizes for contracts

Just published this: https://medium.com/@akhounov/estimation-approximate-of-the-size-of-contracst-in-ethereum-4642fe92d6fe

And I would like the idea of such estimation to be discussed, before we get down to the specifications

## Replies

**carver** (2019-04-11):

> Martin Swende: Interesting. I need to read it more thorougly to fully understand the charts, but my main question is: is it gameable? Can contracts use slots more intelligently (with help off-chain) to evade the estimator?

A contract with predetermined and static storage could game this estimation, afaict. Gaming it with storage changes would be very tough because the probe points shift with the new storage root.

Also note that gaming static contracts gets harder and harder as they get bigger. As you build it locally the probe points shift randomly with each new entry. Then if you try to move the storage slot to align with the probe points, the probe points move again.

It starts to look very much like pow mining, where you can’t guide gaming, you can only stumble onto gaming by trying lots of different slots. So maybe you could game 10s or 100s of slots, but gaming 10 thousand slots smells impractical (assuming we pick an appropriate number of probe points). Somewhere in between might be possible with a “storage underestimate mining rig”.

---

**AlexeyAkhunov** (2019-04-11):

I would also add that the plan is to have this estimation performed **once per contract**, whenever the contract is first modified. After that, the contract storage is updated correctly by SSTORE operations, and then, at the second hard-fork, the estimates are replaced by the accurate numbers.

---

**poemm** (2019-04-12):

Thank you for your effort to raise the gas limit.

Why can’t clients just count exact storage sizes? They can maintain these counts until a hard-fork introduces consensus on these counts.

Your random probe and sample idea is nice. Below is feedback, but maybe you have already dismissed similar ideas.

- A VDF can be used to produce unbiasable randomness. But this adds delays.
- Observing smaller differences at the last sampled items means that further items should be explored.
- An adaptive method can place probes until some percent of the address-space is covered, and this percent may depend on avg_diff. This will stabilize avg_diff, giving better estimates. But this adaptive method must have some limit on time.
- The worst-offender gasToken accounts with abnormally large deep subtries can be identified and voted on by miners. These votes include where to place extra probes, resulting in over-estimation of their storage. This requires an honest majority of miners to participate in this voting.

---

**AlexeyAkhunov** (2019-04-12):

First of all, thank you very much for the review!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poemm/48/1340_2.png) poemm:

> Why can’t clients just count exact storage sizes? They can maintain these counts until a hard-fork introduces consensus on these counts.

Yes, I have been thinking about this for quite a while. The main obstacle I see to this is that software releases do not necessarily mean that the users actually upgrade and start running the new version. Unless there is a hard fork. Therefore, there can be some users who will never upgrade from now until just before the hard fork that introduces the values into consensus. I don’t know how to make all ethereum clients to do the off-line work to correctly calculate the sizes of all contracts and then compare it with what it needs to be. Because they will all be doing it at different times, so there won’t be one test suite for everyone. All in all, I think operationally this is harder than doing an extra hard fork.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poemm/48/1340_2.png) poemm:

> A VDF can be used to produce unbiasable randomness. But this adds delays.

VDF might be a bit of an overkill, given that the estimation is done only one per contract.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poemm/48/1340_2.png) poemm:

> Observing smaller differences at the last sampled items means that further items should be explored.

One of the design principles for the estimator was to make it “fixed cost”, where there is a reasonable upper bound on the running time. That is why I went for a non-adaptive method with fixed number of probes

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poemm/48/1340_2.png) poemm:

> An adaptive method can place probes until some percent of the address-space is covered, and this percent may depend on avg_diff. This will stabilize avg_diff, giving better estimates. But this adaptive method must have some limit on time.

Yes, that would increase accuracy. I did not go into this direction to make the change as simple as I could, because it would need to be done in the next hard fork, if we decide to.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poemm/48/1340_2.png) poemm:

> The worst-offender gasToken accounts with abnormally large deep subtries can be identified and voted on by miners. These votes include where to place extra probes, resulting in over-estimation of their storage. This requires an honest majority of miners to participate in this voting.

Actually, the gastoken (more specifically GasToken2) does not create storage, it creates empty contracts. The largest contract in terms of storage is IDEX, with 7 or 8 million items.

