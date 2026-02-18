---
source: ethresearch
topic_id: 9501
title: A price is not a number -- a quick word on price feeds
author: nikolai
date: "2021-05-14"
category: Economics
tags: []
url: https://ethresear.ch/t/a-price-is-not-a-number-a-quick-word-on-price-feeds/9501
views: 940
likes: 4
posts_count: 2
---

# A price is not a number -- a quick word on price feeds

A price is not a number. Show me a system that trades both ways using a price defined as a single number and I will show you a strategy to bankrupt it. At the very least, it is *two* numbers: a bid and an ask.

But this is also a simplification. When you ask for a price, you’re always implicitly asking for a quantity too. Perhaps something like “what would be the price if we liquidated 10% of all of a certain collateral type”.

A price is a pair of cost-curves. In reality, these curves are composite of many different cost curves that are in constant flux. Imagine what an order book looks like, the different shapes you observe in the wild.

Perhaps there is a reasonable model that is good enough, in the sense that it can be used to answer the questions “how much can we sell with a max slippage of X” and “how much would the price move if we tried to sell Y”.

I don’t know the right model to use, but I can offer a suggestion: A simple quadratic curve. Deep order books look suspiciously like square roots, and quadratic costs show up all the time in these mechanisms. But maybe it’s not a square root shape but `log(x)` or maybe that’s just an illusion and it’s not concave at all but convex. You tell me. My head is spinning already.

We can use all the different AMM curves as a starting point.

I also insist that a bid and an ask should be expressed as two different asks in opposite basis units.

Instead of

`ETH/USD: p`

we might see

`ETH/USD: ax^2 + bx + c`

and

`USD/ETH: dx^2 + ex + f`.

So a ‘price feed’ still submits just a few data points (a, b, c).

`x` is the quantity. If you want the point price, use `x=0`, the `c` and `f` are your bid and ask (modulo mixing up the orientations – you know what I mean).

Who has some better insights into this? Let’s push the space forward a bit and discourage using single point prices where they don’t make sense.

## Replies

**kelvin** (2021-05-15):

In many theoretical models for markets, it is possible to trade quantity  q  at price  p = p_0 + \lambda q . In these models, it makes sense to say that the current price is p_0, and current liquidity is 1/\lambda. So one could have a feed both for price and for current liquidity, although the latter is not as easy to estimate. Of course we could have more complicated models, and these may be particularly useful to applications that provide leverage and need to decide on large-scale liquidations, but for many simpler applications this may not be needed.

Here is a classical paper: [Continuous Auctions and Insider Trading](http://www.fsa.ulaval.ca/personnel/phgre5/files/kyle_1985.pdf).

What would a square root order book be? The price impact is proportional to square root of the quantity? If so, I’ve never seen a model generate such a result.

