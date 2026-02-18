---
source: ethresearch
topic_id: 3233
title: Dynamic token bonding curves and incentivising communities
author: mrdavey
date: "2018-09-05"
category: Economics
tags: [bonding-curves]
url: https://ethresear.ch/t/dynamic-token-bonding-curves-and-incentivising-communities/3233
views: 2273
likes: 4
posts_count: 5
---

# Dynamic token bonding curves and incentivising communities

Hi there! I’ve been doing some research and writing in essentially tokenising ‘equity’ of a community (the real world meetup type, not the ICO type) and distributing it to community participants, to incentivise community participation and contribution. This is open source work so not tied to any company at the moment. There’s a combination of cryptoeconomics and game theory, which is why I posted it in this category.

In summary:

Using a dynamic token bonding curve (‘price’ is based on the person’s portion of the total token supply), we can mint and award participants according to some contribution criteria. (E.g. if you complete X, then you will receive 100 tokens.) As you earn more tokens, the individual ‘price’ of each token *you own* increases due to cumulative effect of your portion of the token supply. This also creates an ‘inflation penalty’ if you are an inactive member of the community. If we prevent buying against the bonding curve and only allow selling, then the main way to receive these tokens are to earn them from your contributions to the community.

I think this could be interesting for a number of reasons:

- Early adopters are awarded for their contribution, but do not maintain a large portion of the supply as the community grows (as it mints and awards new tokens)
- In-active community members (or free riders) are penalised by inflation, making their tokens worth less unless they actively contribute
- Since no one is allowed to buy from the bonding curve, we can then fund the curve from community revenues (sponsorships, grants, ticket sales, etc). Therefore if you really believe in the community, then you will continue to earn more tokens as the funds backing the curve will increase as the community grows, increasing the economic value of your tokens.
- If you hold a large portion of the supply, you are incentivised to sell your tokens back to the curve (as your tokens are worth more), essentially redistributing the token supply away from whales. This also helps new comers join and start earning, since their portion of the supply shouldn’t be too far from the average person’s portion of the supply.

Theres a few more aspects to it, but that is the summary of my research so far. I have a medium post but i’m not sure on the rules around posting links to blog posts here.

I would love to hear what the ethresear.ch community thinks of this.

## Replies

**kwikiel** (2018-09-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/mrdavey/48/13852_2.png) mrdavey:

> As you earn more tokens, the individual ‘price’ of each token you own increases due to cumulative effect of your portion of the token supply

Where the Ethereum for selling is coming from?

---

**mrdavey** (2018-09-06):

See the third dot point:

> Since no one is allowed to buy from the bonding curve, we can then fund the curve from community revenues (sponsorships, grants, ticket sales, etc). Therefore if you really believe in the community, then you will continue to earn more tokens as the funds backing the curve will increase as the community grows, increasing the economic value of your tokens.

---

**mrdavey** (2018-10-30):

Reviving and posting the link to my medium article with more details as per [@vbuterin](/u/vbuterin)’s suggestion: https://tokeneconomy.co/dynamic-token-bonding-curves-41d36e43befa

I’d love to hear more input from the community on the viability of this model.

---

**kwikiel** (2018-10-31):

It’s quite similar to already working thing:

- Early adopters are awarded for their contribution, but do not maintain a large portion of the supply as the community grows (as it mints and awards new tokens)

The idea is to issue equity tokens proportionally to the contribution

https://slicingpie.com/

