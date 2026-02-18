---
source: ethresearch
topic_id: 7896
title: Impermanent Lossless AMM Model Using PostTrade Price
author: pr0toshi
date: "2020-08-24"
category: Economics
tags: []
url: https://ethresear.ch/t/impermanent-lossless-amm-model-using-posttrade-price/7896
views: 2282
likes: 0
posts_count: 3
---

# Impermanent Lossless AMM Model Using PostTrade Price

Hey so Imperm Loss is probably the biggest risk LPs face and is the largest barrier to entry for them to provide funds, reducing the size and liquidity of DeFi Markets. So I made an algo to fix this by using post trade price as the rate of exchange rather than pretrade price. This makes it so that if price moves to any value n then if a single trade is made that will set the previous value to n then the trader will get a fair rate on the assets, itll make it so that LPs suffer no imperm loss and itll allow for the protocol to grow as risk is reduced. Do note that this model only removes IL in cases where there is a market maker that is able to trade with the AMM such that it always keeps the price tracking realtime price. This could be incentivised by a small part of the fees going to the MM which would be a smart contract and so as the liquidity grows for the AMM the MM will become better funded in order to be able to deploy the capital required to do the new price in 1 single trade. If a trade is not enough to set the new price using the inbal/outbal = price then there will be IL. This will in reality probably be a IL reducing algo not a ILless algo. But if designed well a system would be able to use fees and automate the MM to be able to make IL in almost all cases 0.

price(amount_in)

bar = 1 - (token_in_balance / (token_in_balance +  amount_in));

amount_out = token_out_balance * bar;

inbal = token_in_balance + amount_in;

outbal = token_out_balance  - amount out;

price = inbal/outbal

return price;

amount_out = amount_in/ price

token_in_balance=+ amount_in

token_out_balance = - amount out

## Replies

**denett** (2020-08-27):

I think the problem with your solution is that the impermanent loss is mostly the result of the price drifting over time. So there will be a lot of small changes instead of one big jump. For big trades the user could split the trade into smaller pieces to get a better price at the cost of higher gas fees. I don’t think this is an improvement over the original.

Btw, the latest improvement of the AMM design is from Mooniswap.

They are updating the price slowly after a big trade, such that the liquidity providers are getting a cut in the arbitrage income of getting the pool back to normal prices levels.

https://medium.com/@1inch.exchange/1inch-revolutionizes-automated-market-maker-amm-segment-with-mooniswap-e068c20d94c

---

**HuobiResearch-create** (2020-10-12):

I think your model has some problem, because the impermanence loss is not caused by the quotation, but under the AMM mechanism. If the price of non-stable assets in the liquidity pool rises or falls, the market maker will completely automatically act in the opposite direction to traders. The higher the price, the more you sell, the lower the price, the more you buy.

Therefore, If the price of the asset in the pool rises, its quantity will decrease, and if the price of the asset drops, its quantity will increase. This is determined by the AMM mechanism itself, and any deviation from the initial price will cause impermanent loss. The corresponding impermanent loss chart is as follows:

Among them, %Price Change is the current non-stable currency price change ratio,

[![1](https://ethresear.ch/uploads/default/optimized/2X/d/d961e8d9b31be819b299de7b38a48352e67e56ec_2_499x375.png)1800×600 26.7 KB](https://ethresear.ch/uploads/default/d961e8d9b31be819b299de7b38a48352e67e56ec)

and %Impermanent Loss is the ratio of the current asset value in the liquidity pool to the price change ratio of the asset portfolio if it does not provide liquidity. That is, regardless of the price rise or fall, the reverse operation of the liquidity provider under the AMM mechanism will cause a certain impermanent loss.

For traders, if you want to get the real transaction price, you can calculate it by the following method:

The basic formula of the AMM mechanism is:

R_α×R_β=K

Valuation in β coins

After a transaction occurs (using β coins to buy α coins)

The equation of the pool becomes:

（R_α-∆_α）×（R_β+（1-τ）×∆_β）=K

Variable interpretation:

| Variable | interpretation |
| --- | --- |
| R_α | Initial amount of α coins |
| R_β | Initial amount of β coins |
| ∆_β | Variation of α coins |
| ∆_α | Variation of β coins |
| τ | Transaction fee |
| K | Fixed constant |

Initial price:

Initial price=R_β/R_α

Actual price:

Actual price=∆_β/∆_α

