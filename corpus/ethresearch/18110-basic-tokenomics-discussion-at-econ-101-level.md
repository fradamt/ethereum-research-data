---
source: ethresearch
topic_id: 18110
title: Basic tokenomics discussion at econ-101 level
author: noamnisan
date: "2024-01-01"
category: Economics
tags: []
url: https://ethresear.ch/t/basic-tokenomics-discussion-at-econ-101-level/18110
views: 2326
likes: 15
posts_count: 6
---

# Basic tokenomics discussion at econ-101 level

I tried to write down a very generic point of view – from first principles – on how to start looking at tokenomics of Web3 systems (with proof of stake and utility tokens).  See https://www.cs.huji.ac.il/~noam/pages/Tokenomics.pdf

The basic claim is:

(1) The main “micro-tokenomic” issue is that of determining transaction fees.  The claim is that these should best be set to be the marginal costs of transactions, including congestion costs (rather than, e.g., the average costs).

(2) The main “macro-tokenomic” issues are that of determining the minting rate and the staking rewards.  The claim is that new minting should be used to pay for staking “capital costs” (hence in effect covering transactions’ fixed costs) and is to be set at a level that results in a staking rate that provides sufficient security.

Will be glad for any feedback / opinions / other points of view.

## Replies

**0xeminence** (2024-01-03):

while this sounds fine, there is regulation through fee market design as well right which should be added to the macro tokenomic issues i think or a third other thing? The reason almost every token on the first page isnt quite like eth is because its ETH fee market burn causes the staking rate to be much more effective (since net issuance is almost ~0 empirically) and on top of that stakers make 4-5%.

---

**maanav** (2024-01-04):

This is interesting. Curious if you’ve found any data on the price elasticity of the demand for staking rewards (i.e. if the minting rate is reduced, are stakers quick to leave or is there some stickiness), and if this depends on things like the perceived risk/quality of the token, etc.

---

**Pfed-prog** (2024-01-06):

It would be interesting to further explore how these principles could be practically implemented and how different economic mechanisms could impact the overall sustainability and effectiveness of such platforms.

More than anything I am curios to learn about the equation of exchange and how it can be applied in crypto.

**MV = PY** , where M is money supply, V is the velocity of money, P is price level or inflation, and Y is the real output or real GDP.

---

**bmaia18** (2024-01-15):

I would say not only supply and demand but how to implement to create equilibrium to avoid strong deflationary or inflationary scenarios to dominate. Preferably the intrinsic usage of the token in the product/protocol dynamics should be the extra element on providing such equilibrium.

ETH and its fast community and protocol usage was the very first one to implement such a mechanism and control the inflationary spiral, so it can keep incentive mechanisms (fundamental to align ecosystem stakeholders) while not falling into the problem most fiat economies have (endless inflation curve)

---

**samlaf** (2024-01-18):

Would encourage you to add a section on how eigenlayer and shared security can change the macro-economics perspective.

