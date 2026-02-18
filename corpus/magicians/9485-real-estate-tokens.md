---
source: magicians
topic_id: 9485
title: Real Estate Tokens
author: zmckinnon
date: "2022-06-05"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/real-estate-tokens/9485
views: 687
likes: 0
posts_count: 7
---

# Real Estate Tokens

My team is currently working on an NFT to represent ownership of a home. We are essentially having to [modify ERC-721](https://github.com/RoofstockOnChain/hot-token) so that owners cannot transfer tokens at all. Instead, an authorized operator will have to do the transfers.

The reason for this is that the token receiver needs to be KYC’d.

My questions are:

- Do you have any thoughts on other ideas of how to get around this KYC issue?
- Should we propose a standard for real estate that works in this way?
- How should I get started with drafting the spec? Just start reading the docs and writing?

## Replies

**coindation_com** (2022-06-05):

Store the KYC info as metadata.

Would be interested in what you currently have in terms of standart?

---

**zmckinnon** (2022-06-05):

Sure, we are still pretty early in developing the standard, but we are documenting as we go so feel free to review: [Executive Summary - Home Ownership Tokens](https://roofstock-onchain.gitbook.io/home-ownership-tokens/)

The technical portion of that is very idealistic, so if you are interested in the details of the tech portion, I am trying to keep it up to date here: `https://roofstock-onchain.gitbook.io/roofstock-ideas/home-ownership-token` (sorry, can’t put two links in a post)

Both are very much WIP.

I took a quick peek at coindation. We know we have a ton of similar use cases to real world assets (because, ya know, ours is a real world asset).  I’d love to understand your use case.

Does ERC-721 fit the RWA use case? Does coindation need some ultimate control to determine who owns the token?

Thanks for the post!

---

**Chris2** (2022-06-05):

Wouldn’t it be better to just create a corporation that offers the tokens as entry tickets to property owned by the corporation? Aka you buy the token and have exclusive use to a property in perpetuity but are required to pay X (taxes+maintenance) monthly. Helps avoid the KYC requirement. Or perhaps offer it as a rental where Xtokens are required monthly to rent a property and you can create your own internal stablecoin.

---

**zmckinnon** (2022-06-06):

Interesting idea.

The issue with this is that token owners can only resell the tokens to other token holders.

Ultimately, our vision is to make it so that owners have the option to sell the property in a traditional real estate transaction. The value of the property should be limited to the crypto market, ya know?

Perhaps, this includes the right to take title to the property given that you pass KYC and there is no lien? ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

It’s a really good potential solution though. I dropped the idea to the team. It’s something we could certainly experiment with.

---

**zmckinnon** (2022-06-06):

I’m not sure how this model would work with single family rental homes.

The token owner would have rights to the property, but they’d defer those rights to a renter in exchange for money?

I still think ideally whatever solution we come up with, we want the token owner to be the owner of the home and can do what they want with it.

---

**Chris2** (2022-06-07):

There’s a couple ways it could be done. The simplest  is probably a REIT DAO

I know that you can’t have stocks tied to crypto yet but I assume there’s some way to do it through an equity dao where the company buys stocks and you can buy the company’s governance/ownership coin which they repurchase with profits and the governors decide what % goes to repurchase and what % goes to buying more property.

For individual rental properties you could just have NFT’s that represent each property and your own coin that people receive instead of rent that they can use to purchase more NFT property off you. As for buying/selling it’s not exclusive as it’s an erc-20 token that’ll end up on defi exchanges.

I’m not offering an one size fits all solution you’d have to figure out what works best for your corporation given the legal laws in your country of operation. That being said being able to avoid KYC is a huge benefit of owning everything through a corporation and I’d suggest giving up on direct property ownership.

Being able to buy/sell property with no tax instantly is the golden goose. I can instantly sell my summer house in Canada for a winter house in Arizona ![:+1:t2:](https://ethereum-magicians.org/images/emoji/twitter/+1/2.png?v=12)

