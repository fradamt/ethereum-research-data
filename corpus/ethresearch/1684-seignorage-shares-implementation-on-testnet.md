---
source: ethresearch
topic_id: 1684
title: Seignorage Shares implementation on Testnet
author: k26dr
date: "2018-04-09"
category: Economics
tags: []
url: https://ethresear.ch/t/seignorage-shares-implementation-on-testnet/1684
views: 4576
likes: 8
posts_count: 27
---

# Seignorage Shares implementation on Testnet

I’ve coded a Solidity implementation of [@rmsams](/u/rmsams) Seignorage Shares. The contract is up and running on the Rinkeby testnet.

SeignorageController:

https://rinkeby.etherscan.io/address/0xcb8c6d00c7d303b6d24794cf960659c4682c3e47

Shares:

https://rinkeby.etherscan.io/address/0x75071ac8edfd1a060b3d7298cc89f5fac44a1994

Coins:

https://rinkeby.etherscan.io/address/0x1bdd0c76810e17475a4d0303aa1777f5143d18ff

The source code is uploaded to Etherscan under the inidividual contracts and also available on Github:


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/k26dr/seignorage-shares/tree/master/contracts)





###



Solidity implementation of Robert Sams Seignorage Shares - k26dr/seignorage-shares










Some implementation notes:

- A single oracle (me) has control of the price feed for now. The next step is to change this to either a multi-oracle or Schelling point scheme.
- The MINT_CONSTANT determines the the percentage change in supply for a percentage change in price. Currently a 1% change in price leads to 0.1% change in supply per cycle.
- The CYCLE_INTERVAL is currently set to 2000 blocks (~10 hours). An auction is held every cycle for newly printed shares/coins.
- The auction design is pulled from the EOS crowdsale. Users send their orders to a common pool. The sum total of all orders for a cycle is divided by the printed amount of coins/shares to determine the exchange price. Arbitrageurs are incentivized to place orders and bid up the price until the auction exchange price reaches the market price.
- The auction method requires the number of shares to mint to be known ahead of time, so two oracles are required (share price + coin price) instead of one like in the original white paper.

If you’re interested in the project and want some coins/shares on the testnet, shoot me your address in a reply.

## Replies

**vbuterin** (2018-04-10):

> The auction design is pulled from the EOS crowdsale. Users send their orders to a common pool. The sum total of all orders for a cycle is divided by the printed amount of coins/shares to determine the exchange price. Arbitrageurs are incentivized to place orders and bid up the price until the auction exchange price reaches the market price.

As I understand the EOS crowdsale design this is a bad idea. The problem is that no one buying before the last second has any certainty about what valuation they’ll be buying at, and so the mechanism basically optimizes for noobs buying in early thinking they’re buying cheap, but actually getting a relatively unfavorable price.

I personally would just recommend a plain old regular commit/reveal frequent batch auction.

> The auction method requires the number of shares to mint to be known ahead of time, so two oracles are required (share price + coin price) instead of one like in the original white paper.

Why? Why not just keep minting some fixed quantity until the coin price stops being above or below $1? As I understand, the goal is that the auction itself should be the only mechanism by which the protocol learns about the share price, so you should only need one oracle.

---

**EazyC** (2018-04-10):

> The problem is that no one buying before the last second has any certainty about what valuation they’ll be buying at, and so the mechanism basically optimizes for noobs buying in early thinking they’re buying cheap, but actually getting a relatively unfavorable price.

This is only true (or more like only a massive problem) if the time frame of the EOS-style reverse Dutch auction is exorbitantly large, such as the EOS crowdsale itself being 23 hours per period. If the “buckets” for each auction is sufficiently small, such as 10 minutes, it should greatly reduce the end of auction surging issue. The plus of the reverse Dutch auction style is the simplicity of the implementation in solidity, but commit/reveal auction could work as well.

Agreed about the two oracle point, I don’t think more than 1 is needed. Personally, I am a Schelling point type of dude and hope that there is a way to do Schelling point “expand/contract” signals instead of listening to a trusted feed.

---

**vbuterin** (2018-04-10):

> Personally, I am a Schelling point type of dude and hope that there is a way to do Schelling point “expand/contract” signals instead of listening to a trusted feed.

Agree! It’s also worth noting that because seignorage shares systems have no external assets inside the contracts, if people disagree with the result of a corrupted feed, they can always “hard fork” the system into another contract.

---

**k26dr** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The problem is that no one buying before the last second has any certainty about what valuation they’ll be buying at, and so the mechanism basically optimizes for noobs buying in early thinking they’re buying cheap, but actually getting a relatively unfavorable price.

I don’t have a problem with noobs getting fleeced. That’s how markets work. The purpose of the auction is to remove coins from circulation and it does that effectively. 80% of the action occurs in the last 10 minutes in the EOS crowdsale and I used to buy in early knowing that I would get the market price whatever it was at the end of the period so I don’t think there’s that many noobs participating. It’s mostly arbitrageurs.

I see your point about how the first 9.5 hours of the 10 hour auction is wasted time though.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I personally would just recommend a plain old regular commit/reveal frequent batch auction.

I tried that method initially but the code for identifying the winning bids is complex and consumes a lot of gas as the number of bids placed gets very large. The simplicity of the EOS method is what drew me to it. Again, point taken on the need for increased frequency.

![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png) EazyC:

> If the “buckets” for each auction is sufficiently small, such as 10 minutes, it should greatly reduce the end of auction surging issue.

95% of auction time is wasted with 10 hour cycle lengths. This makes a lot of sense, I’ll make that change.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the auction itself should be the only mechanism by which the protocol learns about the share price, so you should only need one oracle.

That would be ideal.

![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png) EazyC:

> Personally, I am a Schelling point type of dude and hope that there is a way to do Schelling point “expand/contract” signals instead of listening to a trusted feed.

I really like this idea. It replaces both oracles with a single Schelling point and solves the problem of figuring out how many shares print at the same time. I’m assuming this means the Schelling point requires players to bid on a specific amount of shares/coins to print for each cycle? A Schelling point should be much more effective at identifying market needs than a simple linear response to price.

Combining this with increased frequency auctions seems like it would make for a good system. I’ll start coding this version of the Schelling point.

---

**k26dr** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why? Why not just keep minting some fixed quantity until the coin price stops being above or below $1?

I can realistically see the price of the shares being anywhere from $1 all the way up to $1000. What’s a good fixed quantity to print to ensure an effective and timely response to a price change? How would this number be identified without an oracle?

---

**vbuterin** (2018-04-10):

> What’s a good fixed quantity to print to ensure an effective and timely response to a price change?

A quantity equal to 1% of the current supply.

Another approach is to make the printing exponential: 0.01% in the first hour, then doubling every hour until the coin price falls back to $1 again.

---

**k26dr** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A quantity equal to 1% of the current supply.

That actually seems pretty reasonable. And simple.

It would still require an oracle though, and if that oracle is going to be a Schelling point, the players might as well just give a number of shares/coins to print.

---

**vbuterin** (2018-04-10):

> if that oracle is going to be a Schelling point, the players might as well just give a number of shares/coins to print.

Disagree with that. Such an approach would make it harder for users to understand if the system is behaving honestly. I’d still say a schelling point based oracle for price, and then basing everything else off that, would work best.

---

**EazyC** (2018-04-10):

When you say “harder for users to understand if the system is behaving honestly” do you mean actual users glancing at the smart contract have to do some mental math to see if everything is running smoothly? Or is there some attack vector I don’t understand.

If you are going to have a Schelling competition for a price feed in order to expand/contract supply of a coin, what is the issue with having the Schelling competition be the actual expansion/retraction signal itself rather than a price feed for the smart contract to then calculate the expansion/retraction amount? Is it because it could be more difficult to arrive at a common, salient Schelling point if it’s the expansion/retraction signal since it’s a more difficult computation for players to report?

---

**vbuterin** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png) EazyC:

> Is it because it could be more difficult to arrive at a common, salient Schelling point if it’s the expansion/retraction signal since it’s a more difficult computation for players to report?

Basically yes.

The difference between computing the function in-contract and out-of-contract is fairly small; it’s not all that computationally or gas-intensive, so it seems clearer to have the logic be explicit.

---

**SRALee** (2018-04-11):

This is both a good AND bad thing. So on one hand, pure seigniorage shares implementation allows for easy forking should the feed get corrupted or the monetary policies of the network be unpopular (for example, say there is contention about whether to transition the price peg from USD to CPI). But on the other hand, with no external assets inside the contracts, it does not create a second layer of network effects on the system which builds cohesion and very strongly incentivizes resolution of contentious conflicts since the non-canonical contract will end up with no assets. I’m not quite sure the best way for a seigniorage shares implementation to accrue external assets (there were ways proposed by other users here), but it would be a smart idea to actually try both implementations on ETH and see which one accrues a large network effect + community faster and stronger.

---

**k26dr** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The difference between computing the function in-contract and out-of-contract is fairly small; it’s not all that computationally or gas-intensive, so it seems clearer to have the logic be explicit.

It’s not just about having the logic being explicit though. Having the players signal contraction/expansion amounts directly is more flexible than standardized 1% moves.

[@EazyC](/u/eazyc) The next question I have would be can we trust the players to legitimately be able to figure out what the right number should be? Oracles are for bringing external truth into the system. I’m not sure the exact amount to print to stabilize the price is a known quantity. The price on the other hand is a known number

I’m leaning towards using the 1% method to start because it’s simpler and feels more secure.

---

**k26dr** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/sralee/48/1134_2.png) SRALee:

> I’m not quite sure the best way for a seigniorage shares implementation to accrue external assets

Auctioning off coins for the assets would work for any Ethereum-based assets. As cross-blockchain communication improves and OmiseGo launches, I’m hoping we’ll see more ERC20 versions of non-Ethereum assets so that the restriction isn’t limiting.

---

**vbuterin** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/sralee/48/1134_2.png) SRALee:

> I’m not quite sure the best way for a seigniorage shares implementation to accrue external assets

I believe that this is called MakerDAO. My stance on this is: let them try the external asset backed approach, and keep seignorage shares as a “pure” coins-backed-by-shares-and-nothing-else scheme. Both models are worthwhile and have different tradeoffs.

---

**SRALee** (2018-04-12):

I’m aware of MakerDAO. I don’t think their CDP based approach is the same/similar thing I was insinuating here.

The difference here is that you’re looking at Seigniorage Shares vs. MakerDAO as 2 approaches at producing a stable unit of account while not giving credence to the idea that in order to create the most stable asset possible (assuming that is the goal here), that the monetary policy of the dapp we are discussing needs to have ample flexibility in creating a balance sheet of not just liabilities (the circulating coins) but also assets.

Take a look at the Federal Reserve’s balance sheet. They don’t simply hold bonds as the only asset to balance their liabilities. They have a very diverse set of assets including a massive portfolio of mortgage backed securities. https://www.federalreserve.gov/monetarypolicy/files/quarterly_balance_sheet_developments_report_201803.pdf

If you look at the Federal Reserve for some inspiration, their notes (USD) are not collateral backed (which MakerDAO’s is) but their monetary policy includes holding assets that form a “stability fund” of sorts. Perhaps that is a good middle ground to shoot for here. In essence, what I am saying is that the USD is not an asset-backed unit of account (which Dai is, so comparing them is futile) but the issuer of USD holds assets as part of the stabilizing effort. Pretty big difference.

If all seigniorage shares is going to be is another “stablecoin experiment“ to see if we can keep a coin value stable using a different, novel approach, then sure. I think it doesn’t need any kind of option to hold assets in addition to its liabilities. But if we are trying to come up with a system in which we could potentially produce the first non-nation state backed fiat cryptocurrency with the backing of a DAO-Fed then I think the 2 token system of seigniorage shares is too inflexible and simplistic. But perhaps we are talking about two different aims and visions.

Just for the record, don’t get me wrong, I think SS is the best proposal for a collateral-less backed stable unit of account, I just personally think it is an ‘incomplete’ system if we would like to build a decentralized Fed.

---

**k26dr** (2018-04-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A quantity equal to 1% of the current supply.

I’ve run into a problem while testing this. When the share price is $100 and there are equal amounts of shares and coins, increasing the share supply during contractions by 1% wipes out the whole coin supply.

[@mkoeppelmann](/u/mkoeppelmann) from Gnosis had a good solution to this. A price feed can be constructed from previous auctions and used without the need for a share price oracle.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png)
    [PID control with stablecoins](https://ethresear.ch/t/pid-control-with-stablecoins/1623/51) [Economics](/c/economics/16)



> Slightly off-topic but someone pointed me to this comment.
> We have build an exchange based on dutch auctions. The parameters are:
>
> Anyone can register a new token pair.
> auctions will start at 2x the previous price and fall down to 0 after 24h. They reach the previous price after 6h
> thus on average an auction should run 6h
> the system will always start two parallel auctions (selling A for B; selling B for A)
> auction start 15min after previous auctions closes - but only if a threshold in sell vo…

---

**vbuterin** (2018-04-14):

> When the share price is $100 and there are equal amounts of shares and coins, increasing the share supply during contractions by 1% wipes out the whole coin supply.

Ah, I was thinking 1% of the current coin supply, not the current share supply.

---

**k26dr** (2018-04-14):

Ok, that’s what I had in my mind with my first iteration but the auction system I’m using requires me to know the exact number of shares to print for contractions ahead of time. Without a share price oracle, I don’t know how many shares a 1% coin supply contraction requires. The two options I see are:

1. Use a more sophisticated auction system that halts after 1% of the coin supply has been retracted. Totally doable, but I like the simplicity of the current method.
2. Determine the share price somehow

Since I have previous price data available in the contract, I might as well use that to compute a share price instead of coding a more complex auction system.

---

**vbuterin** (2018-04-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/k26dr/48/1172_2.png) k26dr:

> Without a share price oracle, I don’t know how many shares a 1% coin supply contraction requires.

Why do you need to? **The purpose of the auction** is to determine how many shares a 1% coin supply contraction requires. I don’t think it’s more complex at all; you let people submit bids and then fill bids going up until the point where 1% of the coins are removed from circulation.

---

**k26dr** (2018-04-14):

if you’re filling bids as you go and don’t have a price target, how do you prevent low-ball bids from getting filled? You’d have to have a bidding period, then sort all bids to figure out which ones get filled. This leads to attack vectors where you can submit 1000s of bids to balloon the gas fees for the sorting operation.


*(6 more replies not shown)*
