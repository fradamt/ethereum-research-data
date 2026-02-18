---
source: ethresearch
topic_id: 6330
title: Daily demand cycle and intraday gas price volatility
author: osolmaz
date: "2019-10-15"
category: Economics
tags: []
url: https://ethresear.ch/t/daily-demand-cycle-and-intraday-gas-price-volatility/6330
views: 2690
likes: 1
posts_count: 2
---

# Daily demand cycle and intraday gas price volatility

I’ve been working on a [problem statement](https://docs.google.com/document/d/1Fdj7IFPIU9Nfat3NsymgHouVqEJwEggvzGm0nq3nQSg/edit?usp=sharing) about gas price volatility for the Diffusion hackathon, and discovered that some patterns that are much more periodic than I anticipated. I’m not aware of any other post that addresses this issue, so I’m posting here.

To summarize my point in a single picture, here is a 5 day graph of hourly averaged gas usage and gas price. I chose the interval so because it’s demonstrative, but feel free to look at other days.

[![Screenshot%20at%202019-10-10%2014-48-13](https://ethresear.ch/uploads/default/optimized/2X/1/1f085d038193bc994153545bc1113661226cddee_2_690x289.png)Screenshot%20at%202019-10-10%2014-48-131697×712 86.2 KB](https://ethresear.ch/uploads/default/1f085d038193bc994153545bc1113661226cddee)

What you see in the graph are the peaks and troughs of gas usage and price, representative of the shift in daily demand. As you also can see, they are highly correlated. Moreover, they seem to follow a cycle that repeats daily. This is caused by the heterogeneous geographic distribution of the demand for Ethereum.

I crunched the numbers and obtained how the load profile looks like for an average day.

[![Screenshot%20at%202019-10-10%2014-47-50](https://ethresear.ch/uploads/default/optimized/2X/0/0005501a1a54d1f92c152ebc219f1e91a63773bb_2_690x423.png)Screenshot%20at%202019-10-10%2014-47-501364×838 78 KB](https://ethresear.ch/uploads/default/0005501a1a54d1f92c152ebc219f1e91a63773bb)

I think it’s no coincidence that the dips correspond to periods when geographically dense areas are asleep, followed immediately by rises.

I computed the ratio of the highest to lowest price for every day as a measure of price volatility, and obtained the following graph

[![Screenshot%20at%202019-10-10%2016-08-25](https://ethresear.ch/uploads/default/optimized/2X/d/dd03da324bafb8ba4c2369e17a3728d195babdfc_2_690x330.png)Screenshot%20at%202019-10-10%2016-08-251690×809 120 KB](https://ethresear.ch/uploads/default/dd03da324bafb8ba4c2369e17a3728d195babdfc)

which shows that in 2019, daily price difference stayed over 2x on average. The cycle’s effect is high enough to consider it as a recurring phenomenon that requires its own solution. I hope this post arouses enough interest to have people start working on this.

I think the narrative that gas price volatility is caused only by the occasional game/scam hype is **incomplete**—in a blockchain that has gained mainstream adoption such as Ethereum, the **daily cycle of demand** by itself is enough to cause volatility that harms the UX for everyone around the globe.

P.S. The [problem statement](https://docs.google.com/document/d/1Fdj7IFPIU9Nfat3NsymgHouVqEJwEggvzGm0nq3nQSg/edit?usp=sharing) has more details and I encourage everyone to read it. We will be presenting challenges regarding this problem in the [Token Engineering track](https://medium.com/@Angela.Kreitenweis/token-genies-your-mission-and-mentors-part-2-9fc349e91d61) at the [Diffusion hackathon in Berlin](https://diffusion.events). We will be using [cadCAD](https://medium.com/block-science/introducing-complex-adaptive-dynamics-computer-aided-design-cadcad-38b63b541eb8) to model the problem for a deeper understanding. If you are in Berlin, you are invited to join on October 19 to hack or discuss.

## Replies

**Mauacgon** (2024-01-08):

Hey! I am interested in reading the problem statement, but even if I click on the link that was supposed to me moved to I think it broken. Would you kindly provide me with a working link?

