---
source: ethresearch
topic_id: 5470
title: Can someone help me understand the flaws with proof of capacity?
author: Econymous
date: "2019-05-18"
category: Mining
tags: []
url: https://ethresear.ch/t/can-someone-help-me-understand-the-flaws-with-proof-of-capacity/5470
views: 1325
likes: 1
posts_count: 3
---

# Can someone help me understand the flaws with proof of capacity?

From the little I can gather, proof of capacity is not suitable for sharding via random sampling.

Is this the only flaw associated with it?

Sorry if this isn’t the right place to ask.

I’m asking, because my scaling solution doesn’t require random sampling.

## Replies

**adlerjohn** (2019-05-18):

Using commodity hardware to rate-limit Sybils is a terrible idea. See: https://blog.sia.tech/choosing-asics-for-sia-b318505b5b51

---

**Econymous** (2019-05-18):

Even that article says pow has centralization risks.

Storage just seems so much more decentralizable  because anyone can own a hard drive. It’s a one time expense instead of an ongoing one.

Isn’t eth’s pow still using commodity hardware?

Ideally,  if poc was used, it would be nice if everyone’s buying power was known when the network launches. If we can know a large percentage of the storage hardware (across the world) that will be purposed for poc, is still held by a fairly distributed diverse number of participants then maybe we can assume the network is safe for the future. At that point no one can whale the network out.

That’s a marketing issue. And an issue when it comes to estimating how much storage hardware is out there.

Assuming a substantial amount of the hardware is being used on the network a Sybil attack would still need to grind through every block to take over

