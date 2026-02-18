---
source: ethresearch
topic_id: 4515
title: Self-referential proxy exchange - does this exist?
author: LegitStack
date: "2018-12-08"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/self-referential-proxy-exchange-does-this-exist/4515
views: 1637
likes: 4
posts_count: 9
---

# Self-referential proxy exchange - does this exist?

Hi everyone, this is my first post here on this form.

I’m wondering if anyone has heard of a… well I suppose it would be classified as a decentralized exchange… that works according to these rules:

1. the exchange has its own token.
2. the exchange can accept and hold various crypto assets in exchange for its own token.
3. The holders of that token can vote on the exchange rate between the token and other crypto assets (individually).

I’ve spoken to many people about this idea but nobody I’ve talked to has heard of a dapp that does this. People say it can’t work because the market will just be gamed by voters, but I’m not so sure; I suppose that’s a question I could pose in the ‘Economics’ category. But for now, I wanted to know if anyone has heard of a decentralized exchange or even more generally a decentralized app that conforms to the rules above?

Anything comes to mind? if it already exists, I think that would be ideal (that way I could just investigate it and see if it works rather than speculate).

## Replies

**nullchinchilla** (2018-12-08):

I think 3. is problematic. You’re essentially letting token holders collectively price-fix the token on the exchange disregarding market forces; price-fixing is bad for the obvious reasons. Wouldn’t it make a lot more sense for the token to simply trade freely on the exchange? The value of the token can simply come from transaction fees on the exchange.

---

**LegitStack** (2018-12-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> You’re essentially letting token holders collectively price-fix the token on the exchange disregarding market forces

Yes that’s right except for one market force: the assets that the exchange holds essentially ‘backs’ the token. So there is a market incentive not to destroy the value of the token.

That’s really why I hesitated calling it an exchange - because it’s more than that. You can use it to exchange in and out of various crypto assets, but you must use this token as the intermediary unlike typical exchanges.

And you could just hold that token. So in that sense it’s like a crowdsourced hedge fund; one where the holders of the shares of the fund get to choose what the fund invests in.

In that way it serves as a prediction market for all prices of all assets that back the token; because the holders of the token have incentive to predict the current optimal distribution of assets for future growth of the value of the token.

I don’t know what to call this system since it’s not just an exchange so I’ve been calling it “proxy token” since a token like this can serve as a proxy for crypto in general, as it represents the optional basket of crypto assets.

---

**ratikesh9** (2018-12-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/legitstack/48/2930_2.png) LegitStack:

> In that way it serves as a prediction market for all prices of all assets that back the token; because the holders of the t

1. When you are predicting the prices of any asset based on future growth then it becomes something like Futures in financial market.

2.If I am getting this correct, then the token which acts as a crowdsource hedge fund will be used to bet on these Futures  or can be used for settlement of the exchange of other assets.

But this can be done using current DEX platforms and building such model on top of them may be certain type of protocols for Futures.

---

**LegitStack** (2018-12-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/ratikesh9/48/2932_2.png) ratikesh9:

> But this can be done using current DEX platforms and building such model on top of them may be certain type of protocols for Futures.

Are you saying this design already exists? Or that it could be made on DEX platforms?

---

**ratikesh9** (2018-12-08):

No, their is no Futures protocol on DEX platform, I am suggesting such protocol can be made.

---

**LegitStack** (2018-12-08):

I think this kind of a system, taken to its ultimate end becomes somewhat akin to what Andreas speculated about in this talk https://youtu.be/rC0cnKq0_m4?t=1073

---

**nullchinchilla** (2018-12-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/legitstack/48/2930_2.png) LegitStack:

> Yes that’s right except for one market force: the assets that the exchange holds essentially ‘backs’ the token. So there is a market incentive not to destroy the value of the token.

I still don’t see why a peg is needed. The value of the exchange is already going to back tokens that act as dividend-paying “shares” no matter whether pegs are used. Pegs simply cause unnecessary distortions; for example, if the “exchange token” trades at a different price on a different exchange, this will cause an persistent arbitrage opportunity which can be used to profit at the  tokenholders’ expense.

---

**LegitStack** (2018-12-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> The value of the exchange is already going to back tokens that act as dividend-paying “shares” no matter whether pegs are used.

Indeed, that is the value of an exchange but this design is more than an exchange. It’s something else (I don’t know the best name, perhaps we could call it the index coin) first, exchange second. Which means we need a way to give the coin itself value, not just the exchange.

![](https://ethresear.ch/user_avatar/ethresear.ch/nullchinchilla/48/2606_2.png) nullchinchilla:

> I still don’t see why a peg is needed. Pegs simply cause unnecessary distortions

Quite right you are, when considering this as nothing more than an exchange, but if you consider it to be something else entirely, the peg is necessary because that distortion is actually what we are after.

The distortion is the leading indicator for where the price is going, and the distortion creates pressure on the price to move in that direction.

As for concerns about arbitrage, I think there are ways to disallow that which basically come down to widening the spread.

This thing is not just an exchange. It’s a self-referential system. Those that own the coin can vote on the exchange rate of the coin to any asset. That means they control the distribution of the coin. It ties all assets together and gives the world a universal price for all things.

The more widely used this system becomes the more those that have voting rights are able to sway the economy outside the coin since the coin itself can be publicly traded. So if you have a vote you have manipulative power over the markets. And that is influence you can sell.

This idea represents a democratization of political power, and a market solution to basic income. I know that sounds grandiose but, self-referential systems that loop in the outside environment are often a strange loop.

