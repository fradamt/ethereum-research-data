---
source: ethresearch
topic_id: 4941
title: Is there good justification to choose POS on plasma instead of POA?
author: boolafish
date: "2019-02-03"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/is-there-good-justification-to-choose-pos-on-plasma-instead-of-poa/4941
views: 2126
likes: 2
posts_count: 7
---

# Is there good justification to choose POS on plasma instead of POA?

As from the previous thread about [possible consensus on plasma](https://ethresear.ch/t/what-consensus-algorithms-are-possible-to-use-in-plasma-chains/1026),  it seems like practical consensus for plasma would be POA and POS.

As for plasma where the security relies on root chain, I can see big benefit that using POA (centralized) would be efficient and the system would be much more simple. And the security relies on root chain any way, we should go for whatever more efficient or simple system design.

The only benefit of POS is to add an extra layer of trust provided by the POS validator. However, it would either be:

1. Not as fast/efficient as POA as too many validators come and the consensus become slow.
2. Or, not providing enough trust with few validators but being more efficient

Both scenario I don’t see good reason to choose POS instead of POA. Just wondering is there some good justification or scenario that POS on Plasma is actually better than POA?

## Replies

**bharathrao** (2019-02-04):

POS would mitigate the data unavailability issues a bit.

---

**joeykrug** (2019-02-05):

Redundancy as well, particularly redundancy in terms of censorship resistance + node / uptime failures. Also operating plasma as a POA operator seems extremely legally risky

---

**vaibhavchellani** (2019-02-06):

POS would allow the us to mitigate the data availability issues , adds a trust layer which might decrease the throughput a bit but will definitely increase the stability of the chain as more people mean less chances of fraud or mass exit . Validator nodes also can be seen as incentivised watchtowers.

---

**boolafish** (2019-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/joeykrug/48/3181_2.png) joeykrug:

> Redundancy as well, particularly redundancy in terms of censorship resistance + node / uptime failures. Also operating plasma as a POA operator seems extremely legally risky

Do you mind to elaborate “legally risky” part more? Though POS would make system more decentralized and secure, but as for legal part I would imaging a centralized system to be more easy to audit (I might be totally wrong about this :P) and would be easier to work with legal issue.

POA can/should still have multiple nodes for availability. Would this works as same as the benefit/mitigate the concern you’ve brought up?

---

**boolafish** (2019-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vaibhavchellani/48/3716_2.png) vaibhavchellani:

> POS would allow the us to mitigate the data availability issues , adds a trust layer which might decrease the throughput a bit but will definitely increase the stability of the chain as more people mean less chances of fraud or mass exit . Validator nodes also can be seen as incentivised watchtowers.

As well as mentioned by [bharathrao](/u/bharathrao), I guess I missed data availability benefit brought by POS.

> Validator nodes also can be seen as incentivised watchtowers.

I also agree on this a lot!

Just curious, is there any research on in which situation it would be better to use POA and when to use POS?

---

**bharathrao** (2019-02-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/boolafish/48/2031_2.png) boolafish:

> Just curious, is there any research on in which situation it would be better to use POA and when to use POS?

In general, POA will aways be faster and have one or two orders of magnitude higher throughput than POS. This is because the fastest known POS block time is about 2 seconds (Ripple/EOS/bitShares). This is a physical limit due to ping times across the globe. You could have a faster POS within a tiny geography but that is pointless for a global chain.

One way to address this is by splitting the transaction creation and block creation roles. In Gluon Plasma, the *exchange role* create transactions and are unencumbered by consensus delay. Block creation is by *validator role* POS and incurs a 2 second delay once every block. As long as the block time is large enough to absorb this (say 10 min blocks) the throughput impact should be negligible. Note that this is only possible because transaction order is pre-determined. Gluon blocks are simply commitment hashes and do not generally require relaying transaction history between nodes.

