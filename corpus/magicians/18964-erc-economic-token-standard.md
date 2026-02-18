---
source: magicians
topic_id: 18964
title: ERC Economic Token Standard
author: robertgenito
date: "2024-02-27"
category: ERCs
tags: [erc, nft, token, erc-721, erc-1155]
url: https://ethereum-magicians.org/t/erc-economic-token-standard/18964
views: 948
likes: 2
posts_count: 10
---

# ERC Economic Token Standard

The tokens engineered today are much more complex than when the original ERC-20 token standard was proposed.  The ERC-20 standard led developers to easily have their tokens compatible with decentralized exchanges and usable by many other smart contracts.  This was an important step forward with Ethereum’s application layer.

Likewise, this new ERC Economic Token Standard will lead the way for developers to make tokens that are compatible in a way where we can only imagine the future.  Imagine: smart contracts that can tell you the price and market cap of its own token and other tokens.  Therefore, you may also imagine smart contracts that can exchange value with one another, similar to a decentralized exchange, without using a “middleman” contract.

This will not only benefit the application layer of Ethereum, it will also benefit coin aggregator websites such as CoinGecko and Coin Paprika who have no standard to follow when it comes to understanding the proper ways to calculate a token’s market cap, fully-diluted market cap, and even the token’s “price”!  Currently, aggregator services must simply guess the economic and capitalization calculations for tokens.  At best, some aggregators even suggest token developers to maintain servers to act as API endpoints to communicate pertinent economic data about their token.  Clearly, there is room for more decentralization, and this standard will show us how.

Tokens engineered today also have accounting that is more complex than simply knowing an account’s balance.  Tokens have begun utilizing more complex accounting terms and operations for tokens “burned”, such as the burning and re-minting of dynamically staked tokens (“mining” tokens), and other tokens have even begun utilizing “virtual” accounting for new financial technology innovations.  This standard is intended for the next generation of decentralized applications (DeFi, gaming, NFTs, etc.) which are all becoming their very own separate economies; economies that can now standardize how they will work with one another on more than a transactional basis, but now on an economical basis.

Stay tuned for the repository link for the ERC Economic Token Standard interface, and I am looking forward to discussing this standard with you all! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

## Replies

**ZWJKFLC** (2024-02-27):

In the second paragraph, do you mean it is similar to the credit currency system in reality?

But this may mean that people need to manage and manipulate currency prices and have the concept of foreign exchange reserves.

---

**robertgenito** (2024-02-27):

Exactly…you got it! :).  This is where the “virtual” accounting supply comes in.  Should have the EIPs fork posted here today, and then a quick reference implementation to follow.  We were concerned that explaining this ERC may be an issue, but so far it has been well received.  My hopes are that the Magicians also grasp it and have useful criticism.  Thank you for your response!

---

**djrthree** (2024-02-27):

This would be awesome. I’d be curious on how those tokens would create their own price, and how it could be externally validated. What prevents some bad actor from saying, “Oh, hey! I’m AwesomeCoin and my price is $10k/coin.” I’d want some proof of value in the standard. If it could do that, there would definitely be more transparency and decentralization in assessing values.

I love the idea of being able to trade for other tokens without a middleman, and I’m imagining it could open the doors to new types of DeFi applications. I’d be curious on how different the transaction costs, fees, slippage, etc would be compared to decentralized exchanges. Is it possible to make a wrapper of existing coins and tokens with the standard?

---

**bl2** (2024-02-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/robertgenito/48/11865_2.png) robertgenito:

> Exactly…you got it! :). This is where the “virtual” accounting supply comes in. Should have the EIPs fork posted here today, and then a quick reference implementation to follow. We were concerned that explaining this ERC may be an issue, but so far it has been well received. My hopes are that the Magicians also grasp it and have useful criticism. Thank you for your response!

I am also considering submitting a proposal about the tokenization of equity.

Look forward to further discussion.

---

**bl2** (2024-02-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/b/9e8a1a/48.png) bl2:

> I am considering this model and plan to submit a token standard with price evaluation.
> The method involves introducing multiple guarantors, each of whom can offer different prices, assume different guarantee obligations,
> and enjoy different guarantee rights.

I am considering this model and plan to submit a token standard with price evaluation.

The method involves introducing multiple guarantors, each of whom can offer different prices, assume different guarantee obligations,

and enjoy different guarantee rights.

---

**ZWJKFLC** (2024-02-28):

If you don’t want unlimited token issuance, Uniswap may be able to meet your requirements.

---

**drllau** (2024-02-28):

The unix philosophy is to have a few simple (and thus testable) commands that can be piped together. The web3 equiv is simple composable contracts that can be chained together. Once a single contract gets monolithic and complicated, then you start accmulating technical debt. Give me a reasoned argument that your **ERC will shift the dial on composability** over the existing proposals. Its all applepie stuff saying what is desireable, its whether details in claims match the rhetoric that counts.

I hope you can pleasantly surprise us.

---

**robertgenito** (2024-03-01):

Hi everyone, here’s an update:

1. I propose this is renamed…because the accounting and data nature allows Artificial Intelligence to become a part of the token’s functionality (without the use of an oracle).
2. My colleague and I are almost done with the Ethereum Request for Comment

---

**pyrobit** (2024-03-11):

!Blaze indeed. Economicalized Tokens.

