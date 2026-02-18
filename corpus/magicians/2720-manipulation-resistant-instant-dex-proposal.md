---
source: magicians
topic_id: 2720
title: Manipulation resistant instant dex proposal
author: svechinsky
date: "2019-02-22"
category: Magicians > Primordial Soup
tags: [dex]
url: https://ethereum-magicians.org/t/manipulation-resistant-instant-dex-proposal/2720
views: 753
likes: 0
posts_count: 1
---

# Manipulation resistant instant dex proposal

Over the past 2 years with the surge in open finance solutions and tokens, a problem that has been constantly bugging me is the lack of a proper decentralized exchange for them. Despite the recent proliferation and advancement in the dex space, all defi apps use either an oracle or a centralized on chain exchange as a pricing source due to front running concerns.

In this post I would like to present a new dex architecture called Ping-Pong.

I’m posting here to get comments, opinions, and thoughts to know if this is something that should be polished and brought to a more usable level or dropped down at this point.

This new dex, created with the help of  [Oliver](https://twitter.com/ProficieNtOCE) & the twitterless Alon Pluda:

1. Is fully on chain, supporting uncensorable exchange of all ERC20 tokens
2. Is manipulation/ front-running resistant
3. Easily enables limit orders and aggregates liquidity
4. Instantly settles trades

## Outline

Let’s consider an exchange with fixed price order book where ETH is traded against TOKEN at fixed prices. For example, prices are pre-fixed at S percent intervals. Meaning that starting from a 1:1 ratio (1 TOKEN for 1ETH) all the pricing levels are:

P_n = (1 + S)^n

This kind of exchange allows us to aggregate large amounts of liquidity in those fixed price levels. This lowers gas costs enough to enable an on chain order book. On the downside it does force an artificial spread on price levels in the market, creating worse prices for smaller orders.

With the ping pong dex however we combine this order model with an automated market (x*y=k). Any time the price of the market-maker DEX hits one of the limit order fixed price walls it starts buying from it, either filling it completely and passing it or bouncing back (like ping pong between two walls).

In my opinion this kind of exchange could be ideal as a pricing source for dapps due to the manipulation resistance and replace pricing oracles.

A more detailed overview can be found here:


      ![](https://cardo.gitbook.io/project/~gitbook/image?url=https%3A%2F%2F3359331998-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fspaces%252F-LTwLCCToeYu4LHB5UXo%252Favatar.png%3Fgeneration%3D1545053199524805%26alt%3Dmedia&width=48&height=48&sign=f9a77308&sv=2)

      [cardo.gitbook.io](https://cardo.gitbook.io/project/ping-pong-dex-1/intro-and-motivation)



    ![](https://cardo.gitbook.io/project/~gitbook/ogimage/-LU6snouk1IpWzd_le0j)

###



Ping Pong is a fully on-chain DEX enabling instant trade execution, limit orders while being resistant to front running.










The code for an initial version of the smart contracts lives here:



      [github.com](https://github.com/kreator/ping-pong-dex)




  ![image](https://opengraph.githubassets.com/2c5ca74b550523a19c3fda9745df8dfe/kreator/ping-pong-dex)



###



A front running resistant always liquid decentralized exchange
