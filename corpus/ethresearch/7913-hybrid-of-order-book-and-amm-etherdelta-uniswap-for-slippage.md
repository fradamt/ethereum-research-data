---
source: ethresearch
topic_id: 7913
title: Hybrid of order-book and AMM (EtherDelta + Uniswap) for slippage reduction
author: jieyilong
date: "2020-08-29"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/hybrid-of-order-book-and-amm-etherdelta-uniswap-for-slippage-reduction/7913
views: 5420
likes: 7
posts_count: 12
---

# Hybrid of order-book and AMM (EtherDelta + Uniswap) for slippage reduction

Hey guys, I had some ideas on reducing AMM slippage by incorporating limit orders. Note that [@haydenadams](/u/haydenadams) proposed similar ideas in his [earlier post](https://ethresear.ch/t/limit-orders-and-slippage-resistance-in-x-y-k-market-makers/2071). But here let’s describe the mechanism slightly more formally.

The basic idea is straightforward. The DEX consists of a Uniswap-like liquidity pool, and an order-book which records the **limit** buy/sell orders. Whenever there is a token swap request, the limit orders will be taken first. Then, tokens in the liquidity pool get consumed, which moves the price, until it hits the next limit order. This process repeats until the swap is done. To describe the swap mechanism more formally, let us look at a trading pair A/B:

**Definitions**

Before we dive into the token swap algorithm, we define the following terminologies/symbols:

x_o: the total number of A tokens in the limit-buy order book

x_l: the total number of A tokens in the liquidity pool

y_o: the total number of B tokens in the limit-sell order book

y_l: the total number of B tokens in the liquidity pool

The state of the DEX can thus be described with this tuple: (x_o, y_o, x_l, y_l). In addition, we define the following quantities:

p = x_l / y_l: the “price” of token B in terms of A, i.e. the exchange rate between B and A.

x_o(p): the total number of A tokens in the buy orders at price point p. Note that x_o(p) can be viewed as a function of p.

y_o(p): the total number of B tokens in the sells orders at price point p. Similarly, note that y_o(p) can also be viewed as a function of p.

**Token Swap Mechanism**

Let us look at the scenario where a user wants to swap \Delta x number of A tokens into B tokens. Suppose that before the swap, the DEX state is (x_o, y_o, x_l, y_l). After the swap, the DEX state becomes (x^{\prime}_o , y^{\prime}_o, x^{\prime}_l, y^{\prime}_l). Given \Delta x, the swap() function of the DEX needs to properly determine the following four differences:

\Delta x_o = x^{\prime}_o - x_o, \Delta x_l = x^{\prime}_l - x_l, \Delta y_o = y^{\prime}_o - y_o, and \Delta y_l = y^{\prime}_l - y_l

With these values, the amount of B tokens returned to the user can thus be calculated by \Delta y = -(\Delta y_o + \Delta y_l).

Roughly speaking, the swap() function works like this: The limit sell orders at the current price point p = x_l / y_l will be taken first. If there are insufficient limit sell orders (i.e.  p \cdot y_o(p) < \Delta x) at price point p, tokens from the liquidity pool will be taken. This in turn results in price increase and might trigger the next limit sell orders. This process continues until all \Delta x A tokens are swapped.

Now let us see how to mathematically determine the four differences \Delta x_o, \Delta x_l, \Delta y_o, and \Delta y_l given the amount of input token \Delta x.

First, since the user is swapping A token for B token, none of the x_o buy orders are consumed. Thus, \Delta x_o = 0.

To determine the remaining three quantities, we note that the liquidity pool needs to maintain the following invariant:

(x_l + \Delta x_l) \cdot (y_l + \Delta y_l) = x_l \cdot y_l = k

Thus, before the swap, the starting price point can be written as p_s = p = \frac{x_l}{y_l} = \frac{k}{y^2_l}. After the swap is done, the ending price point would be p_e = \frac{x_l + \Delta x_l}{y_l + \Delta y_l} = \frac{k}{(y_l + \Delta y_l)^2}. Based on the swap() algorithm described above, we can write down the following equation:

\Delta x = \int^{p_e}_{p_s} p \cdot y_o(p) dp + \Delta x_l, where \Delta x_l \geq 0.

The equation above should be pretty intuitive, since the y_o(p) B tokens that are available as limit-sell orders at price point p can be swapped with p \cdot y_o(p) A tokens. Thus, the integral gives the total number of A tokens needed for swapping with the limit-sell orders of B between p_s and p_e. One small caveat is that the right-hand-side of the above equation may “overshoot” since the limit-sell orders at price point p_e has more more tokens than enough for the swap. Just consider the simple case where the current price is p = 1, and there is a limit-sell order of 100 B tokens, while \Delta x = 20 A tokens. Obviously, the swap will only consumes 20 out of the 100 B tokens. To handle such scenarios, we introduce a variable r to represent the “excess” of the limit-sell orders at price point p_e, we can instead rewrite the equations as a minimization problem:

---

Minimize \Delta x_l, subject to

(x_l + \Delta x_l) \cdot (y_l + \Delta y_l) = k

\Delta x = \int^{p_e}_{p_s} p \cdot y_o(p) dp - p_e \cdot r + \Delta x_l , where  p_s = \frac{k}{y^2_l}, p_e = \frac{k}{(y_l + \Delta y_l)^2}

0 \leq r \leq y_o(p_e)

\Delta x_l \geq 0

---

Notice that the upper bound of p_e can be derived by p_e = \frac{k}{(y_l + \Delta y_l)^2} = \frac{(x_l + \Delta x_l)^2}{k} \leq \frac{(x_l + \Delta x)^2}{k}, since \Delta x_l \leq \Delta x. As a result, \Delta y_l = \sqrt{k/p_e} - y_l  is also lower-bounded by \frac{k}{x_l + \Delta x} - y_l. On the other hand, we know that \Delta y_l \leq 0 since token B in the liquidity pool can only be consumed for this swap. Thus, the above minimization problem can be solved efficiently by **performing a binary search of \Delta y_l between [\frac{k}{x_l + \Delta x} - y_l, 0]**.

Solving the minimization problem gets up \Delta x_l and \Delta y_l. As a byproduct, we can also calculate \Delta y_o = -\int^{p_e}_{p_s} y_o(p) dp, just need to keep in mind that the limit-sell orders at price point p_e might not be fully taken.

Finally, the swap() function can return the user \Delta y = -(\Delta y_l + \Delta y_o) amount of token B.

Please let me know if you guys have any thoughts/comments. Any feedback is appreciated!

## Replies

**denett** (2020-08-29):

One of the best features of uniswap is that it is gas efficient. Doing a trade against an orderbook with potentially hundreds of orders will cost a lot of gas.

Here some thoughts on how to keep the gas fees low and predictable.

- Only allowing limit-orders at fixed intervals (say every 0.5%)
- Queue when orders have the same price.
- Taker does the order against the queue. Determining the precise limit-order to transfer the tokens to, is left to the owneners of the limit-orders in the queue, so they have to collect their tokens afterwards.

This way the taker has predictable gas fees and only big trades have higher fees.

Determining if your limit order was executed is not easy when the queue was only partially sold out. I guess we could solve that using a binary tree and it will take O(log n) time.

p.s. Limit orders steal liquidity from the pool, so I guess the fees should go to the liquidity providers.

---

**vbuterin** (2020-09-01):

> The state of the DEX can thus be described with this tuple: (x_o,y_o,x_l,y_l)

This confuses me. Isn’t the set of orders an entire mapping `{price: orders_at_that_price}`? How would you combine limit orders at different price levels together?

If this is a mistake and you do actually have a map to represent limit orders, then I definitely agree with the suggestion of only allowing them at specific price points (0.5% apart sounds reasonable, could do 1% too) to preserve gas efficiency.

---

**jieyilong** (2020-09-01):

Great feedback, thanks! Agree with your suggestions on how to keep gas cost low and predictable. A few questions:

> Taker does the order against the queue. Determining the precise limit-order to transfer the tokens to, is left to the owneners of the limit-orders in the queue, so they have to collect their tokens afterwards.

Did you mean the smart contract would act as an escrow, and a limit-order maker needs to post an on-chain transaction to collect the swapped tokens?

> p.s. Limit orders steal liquidity from the pool, so I guess the fees should go to the liquidity providers.

In a sense, the limit orders also provide liquidity (similar to the limit orders in CEX). So it may be fair to split the fees among the liquidity providers and the limit-order makers?

---

**denett** (2020-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/jieyilong/48/1899_2.png) jieyilong:

> Did you mean the smart contract would act as an escrow, and a limit-order maker needs to post an on-chain transaction to collect the swapped tokens?

Yes.

![](https://ethresear.ch/user_avatar/ethresear.ch/jieyilong/48/1899_2.png) jieyilong:

> In a sense, the limit orders also provide liquidity (similar to the limit orders in CEX). So it may be fair to split the fees among the liquidity providers and the limit-order makers?

The makers get an order without a fee, so they are all ready better off than executing an order.

The fee structure will determine how the liquidity will be divided between limit-orders and the pool, but I don’t think there is a clear best way to do it, so make it parameterizable and do some experiments.

---

**jieyilong** (2020-09-01):

> This confuses me. Isn’t the set of orders an entire mapping  {price: orders_at_that_price} ? How would you combine limit orders at different price levels together?

Good catch [@vbuterin](/u/vbuterin) ! Yeah I was using (x_o, y_o, x_l, y_l) to represent the DEX state just to simplify the description of how to calculate \Delta y, the number of B tokens swapped. For an actual implementation, the smart contract needs to maintain the map `{price: orders_at_that_price}` (or equivalently the functions x_o(p) and y_o(p) in the original post). `orders_at_that_price` itself might need to be a list or a map to record the makers of each limit-order.

> If this is a mistake and you do actually have a map to represent limit orders, then I definitely agree with the suggestion of only allowing them at specific price points (0.5% apart sounds reasonable, could do 1% too) to preserve gas efficiency.

Yeah, I also think that’s a good suggestion. For further gas cost reduction, we are also considering the possibility of combining Uniswap with the 0x “off-chain order relay with on-chain settlement” approach, instead of relying on a fully on-chain order-book. Will post more on this topic later.

---

**denett** (2020-09-02):

Instead of having limit orders we could also add multiple supplemental liquidity pools which have a straight line as the price curve.

These extra liquidity pools have a min and max price. Is the price below the min, then the pool contains only token A, is the price above the max price, then the pool contains only token B. Is the price between the min and max then the ratio of the two tokens is a linear function of the price.

These liquidity pools could be stacked back to back to make sure there will always be one supplemental pool for every price. If we use pools that are 10% wide, the majority of the trades will use just one supplemental pool and will be very gas efficient.

The liquidity providers will be able to add and remove liquidity in O(1), because we no longer need a queue.

---

**jieyilong** (2020-09-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> These liquidity pools could be stacked back to back to make sure there will always be one supplemental pool for every price. If we use pools that are 10% wide, the majority of the trades will use just one supplemental pool and will be very gas efficient.

Interesting ideas! Limit orders can be viewed as an extreme case I guess, where the price of each “limit order liquidity pool” handles a fixed price point instead of a range.

---

**denett** (2020-09-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jieyilong/48/1899_2.png) jieyilong:

> Limit orders can be viewed as an extreme case I guess, where the price of each “limit order liquidity pool” handles a fixed price point instead of a range.

Yes, but a liquidity pool will sell the tokens it just bought when the price moves the other way. Although you could allow LP to choose to exit the pool once it is fully cleared, then it can be used like a limit-order.

But I think having bigger supplemental pools will be much more gas efficient and could attract a lot of liquidity in a capital efficient way, at the price level it matters (the current price).

---

**vaibhavchellani** (2020-09-10):

For order books looking at something like [this](https://ethresear.ch/t/doing-priority-queues-on-top-of-tries-more-efficiently-with-witnesses/94/2) is also pretty interesting.

---

**HAOYUatHZ** (2020-09-23):

Is Theta working on this?

---

**0xrelapse** (2022-10-01):

What happens if after executing limit sells up to p_e, the new lower price of the pool triggers limit buys? How do you stop infinite loops?

